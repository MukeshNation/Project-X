from fastapi import FastAPI
from pydantic import BaseModel

from modules.chatbot.service import ChatbotService

app = FastAPI(
    title="Project X API",
    version="1.0.0"
)

bot = ChatbotService()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Project X API is running 🚀"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    reply = bot.ask(request.message)
    return {
        "reply": reply
    }