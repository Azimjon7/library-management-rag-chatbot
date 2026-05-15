import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "data")
DB_DIR = os.getenv("DB_DIR", "chroma_db")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:4b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-minilm")
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.05"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "6"))
LLM_NUM_PREDICT = int(os.getenv("LLM_NUM_PREDICT", "180"))
USE_OLLAMA_RAG = os.getenv("USE_OLLAMA_RAG", "false").lower() in {"1", "true", "yes", "on"}
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "library2026")
