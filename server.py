from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask  

app = FastAPI()

class Question(BaseModel):
    session_id: str
    text: str

@app.post("/ask")
def ask_agent(req: Question):
    return {"answer": ask(req.session_id, req.text)}

@app.get("/")
def root():
    return {"message": "UzChess Chatbot API ishlayapti!"}
