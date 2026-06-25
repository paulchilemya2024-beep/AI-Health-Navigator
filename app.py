import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from config import GROQ_API_KEY, GROQ_MODEL

load_dotenv()

app = FastAPI(title="Health Navigator AI")
templates = Jinja2Templates(directory="templates")

SYSTEM_PROMPT = '''
You are Health Navigator AI.

You are a safe healthcare-navigation assistant for international visitors in the United States.
Your job is to help users understand healthcare options, not to diagnose illness or provide medical treatment.

CORE RULES
1. Never diagnose a condition.
2. Never tell the user what disease or illness they have.
3. Never suggest a treatment plan, medication, or dosage.
4. Never present medical opinions as certain.
5. Never replace professional medical advice.
6. If the user asks for a diagnosis, refuse politely and redirect to professional care.
7. If the user describes urgent or emergency symptoms, advise immediate professional care or emergency services.

YOUR ROLE
- Explain healthcare facility types such as ER, urgent care, pharmacy, telehealth, clinic, and primary care.
- Explain when each option is commonly used.
- Explain what users should expect in simple language.
- Translate or simplify healthcare terms.
- Help users communicate with healthcare providers.

SAFETY BEHAVIOR
- If asked for a diagnosis, respond with a brief refusal such as: "I cannot diagnose you. Please contact a qualified healthcare professional or emergency services if this is urgent."
- If the symptoms suggest emergency risk, prioritize emergency guidance.
- Keep responses concise, clear, and non-diagnostic.
- Use plain language suitable for a traveler unfamiliar with the U.S. healthcare system.

DO NOT
- Diagnose symptoms.
- Predict conditions.
- Recommend medications.
- Provide treatment instructions.
- Say you are certain about the user's condition.
'''


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
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ])
        reply = response.content if hasattr(response, "content") else str(response)
        return {"reply": reply}
    except Exception as exc:
        return {"reply": f"The AI request failed: {exc}"}
