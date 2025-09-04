# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_core.runnables import RunnableWithMessageHistory
# from langchain_core.tools import tool
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain_chroma import Chroma
# from dotenv import load_dotenv
# from typing import Dict
# import os
#
# # .env yuklash
# load_dotenv()
#
# # Model
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
#
# # Embedding
# emb = OpenAIEmbeddings(model="text-embedding-3-small")
#
# # Persist directory
# persist_directory = "./chroma_db"
# if not os.path.exists(persist_directory):
#     raise FileNotFoundError(f"Persist directory '{persist_directory}' topilmadi. Avval db_build.py ni ishga tushiring.")
#
# vs = Chroma(
#     persist_directory=persist_directory,
#     embedding_function=emb,
#     collection_name="my_collection"
# )
#
# # Retriever
# retriever = vs.as_retriever(search_kwargs={"k": 3})
#
# # Tool
# @tool
# def db_search(text: str) -> str:
#     """UzChess haqidagi savollar uchun faqat fayl ma'lumotidan foydalanadi."""
#     docs = retriever.get_relevant_documents(text)
#     if not docs:
#         return "Hech qanday ma'lumot topilmadi."
#     return "\n\n".join([doc.page_content for doc in docs])
#
# search_tool = DuckDuckGoSearchRun()
# tools = [db_search, search_tool]
#
# # System prompt (soddalashtirilgan variantini qoldiring)
# system_prompt = """
# Siz UzChess ilovasi va shaxmat bo'yicha ixtisoslashgan yordamchisiz.
# Siz faqat quyidagi ikki mavzuda javob bera olasiz:
# 1) UzChess ilovasi (kurslar, kitoblar, botlar, boshqotirmalar, video darslar, YouTube kanali, AI botlar).
# 2) Umumiy shaxmat (qoidalar, strategiya, mashqlar, tarix, ochilishlar, kombinatsiyalar, endshpil).
# 3) Shunindek, shaxmat o'rganish uchun yoshi va darajasidan kelib chiqib kunlik yoki haftalik reja tuzib berishin kerak.
#
# ❌ Boshqa mavzularga (masalan, siyosat, geografiya, texnologiya, san'at va h.k.) javob bermang.
# Agar foydalanuvchi boshqa mavzuda savol bersa, quyidagicha javob bering:
# "Men faqat UzChess va shaxmat haqida ma'lumot bera olaman."
#
# 🔑 UzChess haqidagi barcha faktlarni faqat berilgan fayllardan oling. Yangi nomlar yoki kurslarni o'ylab topmang.
# 🔑 Umumiy shaxmat savollarida esa umumiy bilimlaringizdan foydalanishingiz mumkin.
#
# """
#
# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{input}"),
#     MessagesPlaceholder("agent_scratchpad")
# ])
#
# # Agent
# agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
# agent = AgentExecutor(agent=agent, tools=tools, verbose=True)
#
# # Session store
# _store: Dict[str, InMemoryChatMessageHistory] = {}
#
# def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
#     if session_id not in _store:
#         _store[session_id] = InMemoryChatMessageHistory()
#     return _store[session_id]
#
# # Agent with history
# agent_with_history = RunnableWithMessageHistory(
#     agent,
#     get_session_history,
#     input_messages_key="input",
#     output_messages_key="output",
#     history_messages_key="chat_history"
# )
#
# # Savol berish funksiyasi
# def ask(session_id: str, text: str) -> str:
#     cfg = {"configurable": {"session_id": session_id}}
#     response = agent_with_history.invoke({"input": text}, config=cfg)
#     return response["output"]
#

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from typing import Dict
import os
import redis

# .env yuklash
load_dotenv()

# Redis client
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

# Model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# Embedding
emb = OpenAIEmbeddings(model="text-embedding-3-small")

# FAISS yuklash
if not os.path.exists("./faiss_index"):
    raise ("❌ FAISS index topilmadi. Avval db_build.py ni ishga tushiring.")


vs = FAISS.load_local("./faiss_index", emb, allow_dangerous_deserialization=True)
retriever = vs.as_retriever(search_kwargs={"k": 3})

# Tool
@tool
def db_search(text: str) -> str:
    """UzChess haqidagi savollar uchun faqat fayl ma'lumotidan foydalanadi."""
    docs = retriever.get_relevant_documents(text)
    if not docs:
        return "Hech qanday ma'lumot topilmadi."
    return "\n\n".join([doc.page_content for doc in docs])

search_tool = DuckDuckGoSearchRun()
tools = [db_search, search_tool]

# System prompt
system_prompt = """
Siz UzChess ilovasi va shaxmat bo'yicha ixtisoslashgan yordamchisiz.
    Siz faqat quyidagi ikki mavzuda javob bera olasiz:
    1) UzChess ilovasi (kurslar, kitoblar, botlar, boshqotirmalar, video darslar, YouTube kanali, AI botlar).
    2) Umumiy shaxmat (qoidalar, strategiya, mashqlar, tarix, ochilishlar, kombinatsiyalar, endshpil).
    3) Shunindek, shaxmat o'rganish uchun yoshi va darajasidan kelib chiqib kunlik yoki haftalik reja tuzib berishin kerak.
    
    ❌ Boshqa mavzularga (masalan, siyosat, geografiya, texnologiya, san'at va h.k.) javob bermang.
    Agar foydalanuvchi boshqa mavzuda savol bersa, quyidagicha javob bering:
    Men faqat UzChess va shaxmat haqida ma'lumot bera olaman."
    
    🔑 UzChess haqidagi barcha faktlarni faqat berilgan fayllardan oling. Yangi nomlar yoki kurslarni o'ylab topmang.
    🔑 Umumiy shaxmat savollarida esa umumiy bilimlaringizdan foydalanishingiz mumkin.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# Agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Redis session store
def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id=session_id, url=REDIS_URL)

# Agent with history
agent_with_history = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history"
)

# Savol berish funksiyasi
def ask(session_id: str, text: str) -> str:
    cfg = {"configurable": {"session_id": session_id}}
    response = agent_with_history.invoke({"input": text}, config=cfg)
    return response["output"]
