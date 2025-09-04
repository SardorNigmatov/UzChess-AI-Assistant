from typing import Dict
import os
import redis
from dotenv import load_dotenv

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ===============================
# Konfiguratsiya va muhit sozlamalari
# ===============================

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
FAISS_PATH = "./faiss_index"

redis_client = redis.Redis.from_url(REDIS_URL)

# ===============================
# Model va embedding
# ===============================

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

if not os.path.exists(FAISS_PATH):
    raise FileNotFoundError("❌ FAISS index topilmadi. Avval db_build.py ni ishga tushiring.")

vector_store = FAISS.load_local(
    FAISS_PATH,
    embedding,
    allow_dangerous_deserialization=True
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# ===============================
# Tools
# ===============================

@tool
def db_search(query: str) -> str:
    """
    UzChess haqidagi savollar uchun faqat fayldan ma'lumot qidiradi.
    """
    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "Hech qanday ma'lumot topilmadi."
    return "\n\n".join([doc.page_content for doc in docs])


search_tool = DuckDuckGoSearchRun()
tools = [db_search, search_tool]

# ===============================
# Prompt
# ===============================

SYSTEM_PROMPT = """
Siz UzChess ilovasi va shaxmat bo'yicha ixtisoslashgan yordamchisiz.
Siz faqat quyidagi ikki mavzuda javob bera olasiz:
1) UzChess ilovasi (kurslar, kitoblar, botlar, boshqotirmalar, video darslar, YouTube kanali, AI botlar).
2) Umumiy shaxmat (qoidalar, strategiya, mashqlar, tarix, ochilishlar, kombinatsiyalar, endshpil).
3) Shuningdek, shaxmat o'rganish uchun yoshi va darajasidan kelib chiqib kunlik yoki haftalik reja tuzib berishingiz kerak.

❌ Boshqa mavzularga (siyosat, geografiya, texnologiya, san'at va h.k.) javob bermang.
Agar foydalanuvchi boshqa mavzuda savol bersa, quyidagicha javob bering:
"Men faqat UzChess va shaxmat haqida ma'lumot bera olaman."

🔑 UzChess haqidagi barcha faktlarni faqat berilgan fayllardan oling. Yangi nomlar yoki kurslarni o'ylab topmang.
🔑 Umumiy shaxmat savollarida esa umumiy bilimlaringizdan foydalanishingiz mumkin.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# ===============================
# Agent va tarix
# ===============================

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """Redis asosida chat tarixini olish"""
    return RedisChatMessageHistory(session_id=session_id, url=REDIS_URL)


agent_with_history = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history"
)


# ===============================
# Foydalanuvchi uchun asosiy funksiya
# ===============================

def ask(session_id: str, text: str) -> str:
    """
    Chat sessiyasi bilan savol berish funksiyasi.

    Args:
        session_id (str): Foydalanuvchi sessiya ID.
        text (str): Savol matni.

    Returns:
        str: Agentning javobi.
    """
    config = {"configurable": {"session_id": session_id}}
    response = agent_with_history.invoke({"input": text}, config=config)
    return response["output"]
