import os
import streamlit as st
from dotenv import load_dotenv

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.vectorstores import FAISS

# ======================
# 1. Setup
# ======================

load_dotenv()
st.set_page_config(page_title="UzChess AI Assistant", page_icon="♟️")

# Logo va sarlavha
col1, col2 = st.columns([1, 3])
with col1:
    st.image("./images/uzchess.jpg", width=100)
with col2:
    st.title("UzChess AI Assistant")

st.markdown("### 🤖 Botning vazifalari")
st.write("""
- 📚 UzChess kurslari haqida ma'lumot berish  
- 📖 Shaxmat kitoblarini tavsiya qilish  
- 🤖 AI botlarni tanlashda yordam berish  
- 🧩 Boshqotirmalar haqida tushuntirish  
- 🎥 Video darslar va mashg'ulotlar bo‘yicha maslahat berish  
- ♟️ Umumiy shaxmat qoidalari va strategiyalarini tushuntirish  
""")

# ======================
# 2. Model va Vector Store
# ======================

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# FAISS yuklash
FAISS_PATH = "./faiss_index"
if not os.path.exists(FAISS_PATH):
    st.error("❌ FAISS index topilmadi. Avval db_build.py ni ishga tushiring.")
    st.stop()

vector_store = FAISS.load_local(
    FAISS_PATH,
    embedding,
    allow_dangerous_deserialization=True
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# ======================
# 3. Tools
# ======================

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

# ======================
# 4. Prompt va Agent
# ======================

SYSTEM_PROMPT = """
Siz UzChess ilovasi va shaxmat bo‘yicha ixtisoslashgan yordamchisiz. 
Faqat shu ikki mavzuda javob bera olasiz:
1) UzChess (kurslar, kitoblar, botlar, boshqotirmalar, video darslar, YouTube kanali, AI botlar).
2) Shaxmat (qoidalar, strategiya, mashqlar, ochilishlar, endshpil, kombinatsiyalar).
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent, tools=tools, verbose=False)

# ======================
# 5. Chat Tarixi
# ======================

if "history" not in st.session_state:
    st.session_state["history"] = InMemoryChatMessageHistory()

agent_with_history = RunnableWithMessageHistory(
    agent,
    lambda _: st.session_state["history"],
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history"
)

# ======================
# 6. Chat UI
# ======================

st.divider()
st.subheader("💬 AI Assistant bilan suhbat")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Oldingi xabarlarni chiqarish
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Foydalanuvchi input
if prompt_text := st.chat_input("Savolingizni yozing..."):
    # User message
    st.session_state["messages"].append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    # Agent javobi
    config = {"configurable": {"session_id": "session_1"}}
    response = agent_with_history.invoke({"input": prompt_text}, config=config)
    answer = response["output"]

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
