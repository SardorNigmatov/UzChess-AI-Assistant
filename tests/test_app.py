import pytest
from fastapi.testclient import TestClient
import sys
import os

# ======================
# 1. Path sozlash
# ======================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


# ======================
# 2. Root endpoint testlari
# ======================

def test_root_endpoint():
    """Root endpoint ishlayotganini tekshirish"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "UzChess Chatbot API ishlayapti!"}


# ======================
# 3. /ask endpoint testlari
# ======================

def test_ask_with_valid_session():
    """To‘g‘ri sessiya va savol yuborilganda javob qaytishi kerak"""
    response = client.post(
        "/ask",
        json={"session_id": "user123", "text": "Salom, shaxmat qoidalari qanday?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)


def test_ask_multiple_users():
    """Bir vaqtning o‘zida ikki foydalanuvchi savol bersa ham ishlashi kerak"""
    r1 = client.post("/ask", json={"session_id": "user1", "text": "Shaxmatda ot qanday yuradi?"})
    r2 = client.post("/ask", json={"session_id": "user2", "text": "Shaxmatda fil qanday yuradi?"})

    assert r1.status_code == 200
    assert r2.status_code == 200

    d1 = r1.json()
    d2 = r2.json()

    assert "answer" in d1 and isinstance(d1["answer"], str)
    assert "answer" in d2 and isinstance(d2["answer"], str)


def test_invalid_request_missing_session_id():
    """session_id berilmagan bo‘lsa, 422 qaytishi kerak"""
    response = client.post("/ask", json={"text": "Bu noto‘g‘ri so‘rov"})
    assert response.status_code == 422
