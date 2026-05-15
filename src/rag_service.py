from langchain_core.prompts import ChatPromptTemplate

from .config import RELEVANCE_THRESHOLD, USE_OLLAMA_RAG
from .model_factory import ModelFactory
from .vector_store import VectorStoreManager


REJECTION_MESSAGE = "I can only answer questions related to our Library Management System."
LOCAL_SOURCE = {"source": "data/library_system_knowledge.md", "page": "N/A"}


class RagService:
    """RAG chatbot service for Library Management System."""

    def __init__(self):
        self.vector_db = VectorStoreManager.get_vector_store() if USE_OLLAMA_RAG else None
        self.llm = ModelFactory.create_llm() if USE_OLLAMA_RAG else None

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant for a Library Management System.

Answer the user's question using the provided context.
If the question is not related to the Library Management System, say:
"I can only answer questions related to our Library Management System."

You can answer questions about:
- system overview
- how the system works
- book search
- borrowing books
- returning books
- user roles
- APIs
- authentication
- RAG architecture
- FastAPI, LangChain, ChromaDB, Ollama

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

            results = self.vector_db.similarity_search_with_relevance_scores(
                question,
                k=4
            )

            if not results:
                return self._fallback_or_reject(fallback_answer)

            best_score = max(score for _, score in results)
            relevant_docs = [
                doc for doc, score in results
                if score >= RELEVANCE_THRESHOLD
            ]

            if best_score < RELEVANCE_THRESHOLD or not relevant_docs:
                return self._fallback_or_reject(fallback_answer)

            context = "\n\n".join(doc.page_content for doc in relevant_docs)

            chain = self.prompt | self.llm
            response = chain.invoke(
                {
                    "context": context,
                    "question": question,
                }
            )

            sources = []
            for doc in relevant_docs:
                sources.append(
                    {
                        "source": doc.metadata.get("source", "unknown"),
                        "page": doc.metadata.get("page", "N/A"),
                    }
                )

            return response.content, sources

        except Exception:
            return self._fallback_or_reject(fallback_answer)

    def _fallback_or_reject(self, fallback_answer: str | None):
        if fallback_answer:
            return fallback_answer, [LOCAL_SOURCE]

        return REJECTION_MESSAGE, []

    def _answer_from_local_knowledge(self, question: str):
        text = question.lower().strip()

        related_terms = [
            "library", "book", "borrow", "return", "overdue", "student",
            "librarian", "admin", "role", "api", "endpoint", "auth",
            "login", "password", "catalog", "search", "rag", "chatbot",
            "architecture", "deployment", "vector", "chroma", "ollama",
            "system", "project", "works", "work", "ai", "assistant",
            "what are you", "who are you", "how", "this", "explain",
            "tell me", "about", "function", "feature", "fastapi",
            "langchain", "database", "knowledge", "semantic",
            "kitob", "qarz", "qaytar", "kutubxona", "foydalanuvchi",
        ]

        if not any(term in text for term in related_terms):
            return None

        if any(term in text for term in ["what are you", "who are you", "ai", "assistant", "chatbot"]):
            return (
                "I am a RAG-based AI assistant for the Library Management System. "
                "I help users understand how the system works, including book search, "
                "borrowing, returning, APIs, user roles, authentication, and system architecture. "
                "I use FastAPI, LangChain, ChromaDB, Ollama, and a local AI model to answer questions."
            )

        if any(term in text for term in ["how this works", "how does this system work", "how system works", "system work", "project", "explain", "tell me about"]):
            return (
                "The Library Management System works through three main parts. "
                "First, the frontend allows users to search books and interact with the chatbot. "
                "Second, the FastAPI backend receives requests and handles book search, borrowing, returning, and chatbot APIs. "
                "Third, the RAG chatbot uses LangChain and ChromaDB to retrieve relevant knowledge, then Ollama and Gemma 3 generate the final answer."
            )

        if any(term in text for term in ["api", "endpoint", "fastapi"]):
            return (
                "The system uses FastAPI endpoints for different operations. "
                "Main endpoints include GET /api/health for checking server status, "
                "GET /api/books for listing books, GET /api/books/search for searching books, "
                "POST /api/borrow for borrowing books, POST /api/return for returning books, "
                "and POST /api/chat for chatbot questions."
            )

        if any(term in text for term in ["borrow", "borrowing", "take book", "student borrow", "qarz", "olish"]):
            return (
                "A student can borrow a book by searching for the book, checking if copies are available, "
                "and sending a borrow request. The system checks availability, records the transaction, "
                "updates the available copy count, and provides borrowing information."
            )

        if any(term in text for term in ["return", "returning", "give back", "qaytar"]):
            return (
                "A student or librarian can return a borrowed book. "
                "The system closes the borrow transaction, updates the book availability, "
                "and increases the available copy count."
            )

        if any(term in text for term in ["admin", "role", "roles", "user", "student", "librarian", "foydalanuvchi"]):
            return (
                "The system has different user roles. Students can search and borrow books. "
                "Librarians can manage catalog and circulation. Admins can manage users, roles, reports, "
                "borrowing limits, and overall system activity."
            )

        if any(term in text for term in ["auth", "login", "password", "authentication"]):
            return (
                "The system can use email and password authentication with role-based access control. "
                "In a production version, passwords should be hashed securely and protected endpoints "
                "should use JWT or session-based authentication."
            )

        if any(term in text for term in ["architecture", "rag", "vector", "chroma", "chromadb", "ollama", "langchain", "embedding", "semantic"]):
            return (
                "The project uses RAG architecture. Documents are split into chunks and converted into embeddings. "
                "These embeddings are stored in ChromaDB. When a user asks a question, LangChain retrieves relevant context "
                "from ChromaDB and sends it to the Gemma 3 model through Ollama to generate an answer."
            )

        if any(term in text for term in ["search", "catalog", "book", "books", "isbn", "category", "kitob"]):
            return (
                "The catalog stores book title, author, ISBN, category, copy count, availability, and shelf location. "
                "Users can search books by title, author, ISBN, or category."
            )

        if any(term in text for term in ["feature", "function", "functions"]):
            return (
                "The main features of the system are book search, book catalog display, borrowing, returning, "
                "AI chatbot support, API explanation, role explanation, and off-topic question rejection."
            )

        return (
            "The Library Management System is a web-based application that manages books, users, borrowing, returning, "
            "overdue tracking, administration, and an AI-powered RAG chatbot. The chatbot helps users understand the system "
            "and answers questions using the project knowledge base."
        )