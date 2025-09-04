import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "UzChess Chatbot API ishlayapti!"}

def test_ask_with_valid_session():
    response = client.post(
        "/ask",
        json={"session_id": "user123", "text": "Salom, shaxmat qoidalari qanday?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)

def test_ask_multiple_users():
    # user1
    r1 = client.post("/ask", json={"session_id": "user1", "text": "Shaxmatda ot qanday yuradi?"})
    # user2
    r2 = client.post("/ask", json={"session_id": "user2", "text": "Shaxmatda fil qanday yuradi?"})

    assert r1.status_code == 200
    assert r2.status_code == 200

    d1 = r1.json()
    d2 = r2.json()

    assert "answer" in d1
    assert "answer" in d2
    assert isinstance(d1["answer"], str)
    assert isinstance(d2["answer"], str)

def test_invalid_request():
    # session_id bermasak, valid emas bo‘lishi kerak
    response = client.post("/ask", json={"text": "Bu noto‘g‘ri so‘rov"})
    assert response.status_code == 422  # validation error

def test_ask_with_valid_session():
    response = client.post(
        "/ask",
        json={"session_id": "user123", "text": "Salom, shaxmat qoidalari qanday?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)


def test_ask_multiple_users():
    r1 = client.post("/ask", json={"session_id": "user1", "text": "Ot qanday yuradi?"})
    r2 = client.post("/ask", json={"session_id": "user2", "text": "Fil qanday yuradi?"})

    assert r1.status_code == 200
    assert r2.status_code == 200

    d1 = r1.json()
    d2 = r2.json()

    assert "answer" in d1
    assert "answer" in d2
    assert isinstance(d1["answer"], str)
    assert isinstance(d2["answer"], str)

def test_invalid_request():
    response = client.post("/ask", json={"text": "Noto‘g‘ri so‘rov"})
    assert response.status_code == 422
