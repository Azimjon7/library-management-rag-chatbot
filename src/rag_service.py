from langchain_core.prompts import ChatPromptTemplate
from .config import RELEVANCE_THRESHOLD, USE_OLLAMA_RAG
from .model_factory import ModelFactory
from .vector_store import VectorStoreManager

REJECTION_MESSAGE = "I can only answer questions related to our Library Management System."
LOCAL_SOURCE = {"source": "data/library_system_knowledge.md", "page": "N/A"}


class RagService:
    """Facade pattern: simple chat interface hiding RAG internals."""

    def __init__(self):
        self.vector_db = VectorStoreManager.get_vector_store() if USE_OLLAMA_RAG else None
        self.llm = ModelFactory.create_llm() if USE_OLLAMA_RAG else None
        self.prompt = ChatPromptTemplate.from_template(
            """
You are a helpful RAG assistant for a Library Management System.

Rules:
1. Answer using ONLY the provided context.
2. If the answer is not in the context or the question is unrelated, say exactly:
"I can only answer questions related to our Library Management System."
3. Be concise and practical.
4. Mention the source section or file when useful.

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def ask(self, question: str):
        fallback_answer = self._answer_from_local_knowledge(question)
        if not USE_OLLAMA_RAG:
            return self._fallback_or_reject(fallback_answer)

        try:
            if self.vector_db is None or self.llm is None:
                return self._fallback_or_reject(fallback_answer)

            results = self.vector_db.similarity_search_with_relevance_scores(question, k=4)

            if not results:
                return self._fallback_or_reject(fallback_answer)

            best_score = max(score for _, score in results)
            relevant_docs = [doc for doc, score in results if score >= RELEVANCE_THRESHOLD]

            if best_score < RELEVANCE_THRESHOLD or not relevant_docs:
                return self._fallback_or_reject(fallback_answer)

            context = "\n\n".join(doc.page_content for doc in relevant_docs)
            chain = self.prompt | self.llm
            response = chain.invoke({"context": context, "question": question})

            sources = []
            for doc in relevant_docs:
                sources.append({
                    "source": doc.metadata.get("source", "unknown"),
                    "page": doc.metadata.get("page", "N/A"),
                })

            return response.content, sources
        except Exception:
            return self._fallback_or_reject(fallback_answer)

    def _fallback_or_reject(self, fallback_answer: str | None):
        if fallback_answer:
            return fallback_answer, [LOCAL_SOURCE]
        return REJECTION_MESSAGE, []

    def _answer_from_local_knowledge(self, question: str):
        text = question.lower()
        related_terms = [
            "library", "book", "borrow", "return", "overdue", "student",
            "librarian", "admin", "role", "api", "endpoint", "auth",
            "login", "password", "catalog", "search", "rag", "chatbot",
            "architecture", "deployment", "vector", "chroma", "ollama",
            "kitob", "qarz", "qaytar", "kutubxona", "admin", "foydalanuvchi",
        ]
        if not any(term in text for term in related_terms):
            return None

        if any(term in text for term in ["api", "endpoint"]):
            return (
                "The system exposes FastAPI endpoints for health checks, catalog access, "
                "book search, borrowing, returning, and chatbot questions. Key endpoints: "
                "GET /api/health, GET /api/books, GET /api/books/search?q=clean, "
                "POST /api/borrow, POST /api/return, and POST /api/chat."
            )

        if any(term in text for term in ["borrow", "qarz", "olish"]):
            return (
                "A student can borrow a book when at least one copy is available and the "
                "student has not exceeded the borrowing limit. The API accepts "
                "POST /api/borrow with user_id and book_id."
            )

        if any(term in text for term in ["return", "qaytar"]):
            return (
                "A student or librarian can return a borrowed book. The system closes the "
                "borrow transaction and increases the available copy count. The API accepts "
                "POST /api/return with user_id and book_id."
            )

        if any(term in text for term in ["admin", "role", "user", "foydalanuvchi"]):
            return (
                "Admins manage users, assign roles, view reports, configure borrowing "
                "limits, and monitor system activity. Students use catalog and borrowing "
                "features, while librarians manage the catalog and circulation."
            )

        if any(term in text for term in ["auth", "login", "password"]):
            return (
                "The documented system uses email and password authentication with "
                "role-based access control. In production, protected endpoints should use "
                "secure password hashing and JWT or session-based authentication."
            )

        if any(term in text for term in ["architecture", "rag", "vector", "chroma", "ollama", "deployment"]):
            return (
                "The project uses a modular monolith architecture with FastAPI, a static "
                "web UI, LangChain, Ollama models, and ChromaDB. Documents are ingested "
                "into a vector database, then the chatbot retrieves relevant context to "
                "answer Library Management System questions."
            )

        if any(term in text for term in ["search", "catalog", "book", "kitob"]):
            return (
                "The catalog stores book title, author, ISBN, category, copy counts, and "
                "shelf location. Users can search books by title, author, category, or ISBN."
            )

        return (
            "The Library Management System manages books, users, borrowing, returning, "
            "overdue tracking, administration, and a RAG chatbot that answers questions "
            "about the system."
        )
