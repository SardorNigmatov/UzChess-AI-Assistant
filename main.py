from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask

# ======================
# 1. App yaratish
# ======================

app = FastAPI(
    title="UzChess Chatbot API",
    description="UzChess va shaxmat bo‘yicha AI Assistant uchun API",
    version="1.0.0"
)


# ======================
# 2. Pydantic model
# ======================

class QuestionRequest(BaseModel):
    """Foydalanuvchidan keladigan savol modeli"""
    session_id: str
    text: str


# ======================
# 3. Routes
# ======================

@app.get("/", status_code=200)
def root():
    """API ishlayotganini tekshirish uchun"""
    return {"message": "UzChess Chatbot API ishlayapti!"}


@app.post("/ask", status_code=200)
def ask_agent(request: QuestionRequest):
    """
    AI Assistantga savol berish endpointi.

    Args:
        request (QuestionRequest): Foydalanuvchi sessiya ID va savoli.

    Returns:
        dict: AI javobi {"answer": "..."}
    """
    answer = ask(request.session_id, request.text)
    return {"answer": answer}
