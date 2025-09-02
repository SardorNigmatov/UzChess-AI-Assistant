import streamlit as st
import requests

# FastAPI URL (deploy qilganingizda manzilni yangilaysiz)
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="UzChess AI Assistant")

# Logo va sarlavha
col1, col2 = st.columns([1, 3])
with col1:
    st.image("uzchess-logo.png", width=100)  # 👉 logotip faylni shu papkaga qo‘ying
with col2:
    st.title("♟️ UzChess AI assistant")

# Vazifalar ro‘yxati
st.markdown("### 🤖 Botning vazifalari")
st.write("""
- 📚 UzChess ilovasidagi kurslar haqida ma'lumot berish  
- 📖 Shaxmat kitoblarini tavsiya qilish  
- 🤖 AI botlarni tanlashda yordam berish  
- 🧩 Boshqotirmalar (puzzles) haqida tushuntirish  
- 🎥 Video darslar va mashg'ulot rejalari bo'yicha maslahat berish  
- ♟️ Umumiy shaxmat qoidalari va strategiyalarini tushuntirish  
""")

# ======================
# 2. Chat Interface
# =====================
st.divider()
st.subheader("💬 AI Assistant bilan suhbat")

# ======================
# Session
# ======================
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "session_1"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Oldingi xabarlarni chiqarish
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# Chat qismi
# ======================
if prompt := st.chat_input("Savolingizni yozing..."):
    # User xabari
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API chaqirish
    payload = {"session_id": st.session_state["session_id"], "text": prompt}
    try:
        res = requests.post(API_URL, json=payload, timeout=60)
        res.raise_for_status()
        answer = res.json()["answer"]
    except Exception as e:
        answer = f"❌ API bilan bog‘lanishda xatolik: {e}"

    # Bot javobi
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
