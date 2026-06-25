"""
config.py
Central configuration for the FIFA World Cup Healthcare Navigation Assistant.
Loads from .env and defines all constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "llama-3.3-70b-versatile"   # free, fast, multilingual

# ── RAG ──────────────────────────────────────────────────────────────────────
CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME: str = "healthcare_kb"
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
CHUNK_SIZE: int = 500          # tokens per chunk
CHUNK_OVERLAP: int = 50
TOP_K: int = 3

# ── LOGGING ───────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ── EMERGENCY KEYWORDS ────────────────────────────────────────────────────────
EMERGENCY_KEYWORDS: list[str] = [
    "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
    "not breathing", "unconscious", "passed out", "unresponsive",
    "stroke", "facial drooping", "face drooping", "arm weakness",
    "speech difficulty", "can't speak", "severe allergic", "anaphylaxis",
    "uncontrolled bleeding", "bleeding won't stop", "poisoning", "overdose",
    "heart attack", "seizure", "convulsion", "choking", "severe chest",
    "crushing chest", "can't move", "paralyzed", "suicidal", "suicide",
    # Spanish
    "dolor en el pecho", "no puedo respirar", "dificultad para respirar",
    "inconsciente", "derrame cerebral", "sangrado sin control",
    # Portuguese
    "dor no peito", "não consigo respirar", "inconsciente", "derrame",
    # Arabic
    "ألم في الصدر", "لا أستطيع التنفس",
    # French
    "douleur thoracique", "ne peut pas respirer", "inconscient",
]

# ── SUPPORTED LANGUAGES ───────────────────────────────────────────────────────
SUPPORTED_LANGUAGES: list[str] = [
    "English", "Spanish", "Portuguese", "Arabic", "French",
    "Japanese", "Korean", "German", "Wolof", "Darija",
]

# ── HOST CITIES ───────────────────────────────────────────────────────────────
HOST_CITIES: list[str] = [
    "New York, NY",
    "Los Angeles, CA",
    "Dallas, TX",
    "Houston, TX",
    "Atlanta, GA",
    "Seattle, WA",
    "San Francisco, CA",
    "Kansas City, MO",
    "Philadelphia, PA",
    "Boston, MA",
    "Miami, FL",
]

# ── KNOWLEDGE BASE FILE ───────────────────────────────────────────────────────
KB_FILE: str = "rag_knowledge_base.json"
CONVERSATIONS_FILE: str = "conversation_training_data.json"