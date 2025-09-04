# ♟️ UzChess AI Assistant

![Project Logo](./images/uzchess.jpg)  


UzChess AI Assistant — bu **UzChess ilovasi va shaxmat bo‘yicha ixtisoslashgan sun’iy intellekt yordamchisi**.  
U foydalanuvchilarga **kurslar, kitoblar, boshqotirmalar, AI botlar** haqida ma’lumot beradi hamda umumiy **shaxmat qoidalari va strategiyalari**ni tushuntiradi.  

---

## 🚀 Imkoniyatlar

- 📚 UzChess kurslari haqida ma’lumot olish  
- 📖 Shaxmat kitoblarini tavsiya qilish  
- 🤖 AI botlarni tanlash bo‘yicha yordam  
- 🧩 Boshqotirmalar (puzzles) bo‘yicha tushuntirish  
- 🎥 Video darslar va mashg‘ulotlar haqida maslahat  
- ♟️ Shaxmat qoidalari, ochilishlar, kombinatsiyalar va endshpil  

<img width="1004" height="829" alt="image" src="https://github.com/user-attachments/assets/83625599-325a-40e1-b76d-89926f882f4a" />

---

## 🏗️ Arxitektura

- **Backend**: [FastAPI]
- **Frontend**: [Streamlit]  
- **AI LLM**: OpenAI (GPT-4o-mini)  
- **Vector DB**: FAISS (matnlarni qidirish uchun)  
- **Optional**: Redis (sessiyalarni saqlash uchun)  

---

## ⚙️ O‘rnatish

### 1. Repository klonlash

 - git clone https://github.com/SardorNigmatov/UzChess-AI-Assistant/
 - cd uzchess-ai-assistant

### 2. Virtual environment yaratish
 - python -m venv venv
 - source venv/bin/activate   # Linux/Mac
 - venv\Scripts\activate      # Windows

### 3. Kerakli kutubxonalarni o‘rnatish
 - pip install -r requirements.txt

### 4. .env fayl yaratish
 - OPENAI_API_KEY=your_openai_api_key
 - REDIS_URL=redis://localhost:6379/0   # Agar Redis ishlatsangiz

## 🔨 FAISS bazasini yaratish
 - Matn fayllarini data/ papkasiga joylashtiring (masalan: courses.txt, books.txt va h.k.).
 - Keyin FAISS index yarating:
 - python db_build.py

## ▶️ Ishga tushirish
 - Backend (FastAPI)
 - uvicorn main:app --reload
 - Swagger hujjatlari: http://127.0.0.1:8000/docs
 - Frontend (Streamlit)
 - streamlit run frontend.py

## 🧪 Testlar
 - pytest -v


## 👨‍💻 Muallif
 - Ism: Nigmatov Sardor
 - Email: sardornigmatov2003@gmail.com
