import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from config import GROQ_API_KEY, GROQ_MODEL

load_dotenv()

app = FastAPI(title="Health Navigator AI")
templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})


@app.post("/chat")
def chat(req: ChatRequest):
    message = (req.message or "").strip()
    if not message:
        return {"reply": "Please enter a message so I can help."}

    if not GROQ_API_KEY:
        return {
            "reply": "Groq API key is not configured yet. Add it to the .env file and restart the server."
        }

    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=0.2,
        )
        response = llm.invoke([HumanMessage(content=(
            "You are Health Navigator AI, a helpful healthcare navigation assistant. "
            "Give safe, non-diagnostic guidance. Keep it concise and practical. "
            f"User message: {message}"
        ))])
        reply = response.content if hasattr(response, "content") else str(response)
        return {"reply": reply}
    except Exception as exc:
        return {"reply": f"The AI request failed: {exc}"}
