import streamlit as st
import requests

# ======================
# 1. Config
# ======================

API_URL = "http://127.0.0.1:8000/ask"  # ⚠️ Deploy qilganda yangilang

st.set_page_config(page_title="UzChess AI Assistant", page_icon="♟️")

# Logo va sarlavha
col1, col2 = st.columns([1, 3])
with col1:
    st.image("./images/uzchess.jpg", width=100)  # ⚠️ Fayl shu papkada bo‘lishi kerak
with col2:
    st.title("♟️ UzChess AI Assistant")

# Vazifalar ro‘yxati
st.markdown("### 🤖 Botning vazifalari")
st.write("""
- 📚 UzChess ilovasidagi kurslar haqida ma'lumot berish  
- 📖 Shaxmat kitoblarini tavsiya qilish  
- 🤖 AI botlarni tanlashda yordam berish  
- 🧩 Boshqotirmalar (puzzles) haqida tushuntirish  
- 🎥 Video darslar va mashg'ulot rejalari bo‘yicha maslahat berish  
- ♟️ Umumiy shaxmat qoidalari va strategiyalarini tushuntirish  
""")

# ======================
# 2. Session
# ======================

if "session_id" not in st.session_state:
    st.session_state["session_id"] = "session_1"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ======================
# 3. Oldingi xabarlarni chiqarish
# ======================

st.divider()
st.subheader("💬 AI Assistant bilan suhbat")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# 4. Chat UI
# ======================

if user_input := st.chat_input("Savolingizni yozing..."):

    # User xabarini chiqarish
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API chaqirish
    payload = {"session_id": st.session_state["session_id"], "text": user_input}
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        answer = response.json().get("answer", "⚠️ Javob olinmadi.")
    except requests.exceptions.RequestException as e:
        answer = f"❌ API bilan bog‘lanishda xatolik: {e}"

    # Bot javobi
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
