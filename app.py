from datetime import datetime, timezone
from secrets import compare_digest, token_urlsafe

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.config import ADMIN_PASSWORD, ADMIN_USERNAME, DB_DIR, EMBED_MODEL, LLM_MODEL
from src.library_repository import LibraryRepository
from src.rag_service import RagService

app = FastAPI(
    title="Library Management System API with RAG Chatbot",
    description="FastAPI backend for a Library Management System integrated with a RAG-based AI assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = LibraryRepository()
rag_service: RagService | None = None
admin_sessions: dict[str, str] = {}


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, example="How can a student borrow a book?")


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


class BorrowRequest(BaseModel):
    user_id: str = Field(..., example="student-001")
    book_id: str = Field(..., example="book-001")


class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1, example="admin")
    password: str = Field(..., min_length=1, example="library2026")


class AdminLoginResponse(BaseModel):
    token: str
    username: str


def require_admin(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required",
        )

    token = authorization.removeprefix("Bearer ").strip()
    username = admin_sessions.get(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin session",
        )
    return username


@app.on_event("startup")
def startup_event():
    """Load the already-created Chroma vector database when the API starts."""
    global rag_service
    rag_service = RagService()


@app.get("/api/health")
def health():
    return {"status": "ok", "backend": "FastAPI", "ai": "Ollama + LangChain + ChromaDB"}


@app.get("/api/books")
def list_books():
    return repo.list_books()


@app.get("/api/books/search")
def search_books(q: str):
    return repo.search_books(q)


@app.post("/api/borrow")
def borrow_book(request: BorrowRequest):
    return repo.borrow_book(request.user_id, request.book_id)


@app.post("/api/return")
def return_book(request: BorrowRequest):
    return repo.return_book(request.user_id, request.book_id)


@app.post("/api/admin/login", response_model=AdminLoginResponse)
def admin_login(request: AdminLoginRequest):
    is_valid_username = compare_digest(request.username, ADMIN_USERNAME)
    is_valid_password = compare_digest(request.password, ADMIN_PASSWORD)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = token_urlsafe(32)
    admin_sessions[token] = request.username
    return {"token": token, "username": request.username}


@app.post("/api/admin/logout")
def admin_logout(authorization: str | None = Header(default=None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        admin_sessions.pop(token, None)
    return {"success": True}


@app.get("/api/admin/summary")
def admin_summary(username: str = Depends(require_admin)):
    summary = repo.get_dashboard_summary()
    summary["admin"] = {
        "username": username,
        "signed_in_at": datetime.now(timezone.utc).isoformat(),
    }
    summary["system"] = {
        "llm_model": LLM_MODEL,
        "embedding_model": EMBED_MODEL,
        "vector_database": DB_DIR,
        "backend": "FastAPI",
    }
    return summary


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if rag_service is None:
        raise HTTPException(status_code=503, detail="RAG service is not ready")
    answer, sources = rag_service.ask(request.question)
    return {"answer": answer, "sources": sources}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
