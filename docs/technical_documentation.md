# Technical Documentation: Library Management System with RAG Chatbot

## 1. Overview
This project integrates a Retrieval-Augmented Generation chatbot into a Library Management System. The chatbot works as a help assistant for the application. It answers questions about system purpose, features, API endpoints, authentication, roles, architecture, deployment, and troubleshooting. It rejects unrelated questions.

## 2. Requirement Coverage
The final assessment requires a RAG chatbot integrated into an existing system, with source code, documentation, test evidence, and live demonstration. This project includes all required parts: document ingestion, chunking, embeddings, ChromaDB vector storage, runtime retrieval, context-aware LLM answer generation, source attribution, rejection handling, web UI, and deployment files.

## 3. RAG Architecture
Build time:
1. `ingest.py` loads documentation from `data/`.
2. Documents are split into 800-character chunks with 150-character overlap.
3. `OllamaEmbeddings` generates vector embeddings.
4. ChromaDB stores vectors persistently in `chroma_db/`.

Runtime:
1. User enters a question in the web chat or terminal chat.
2. The system embeds the question.
3. ChromaDB retrieves top relevant chunks.
4. The prompt tells the LLM to answer only using retrieved context.
5. If the best relevance score is below the threshold, the system rejects the question.
6. The answer is returned with source metadata.

## 4. Build Time vs Runtime Separation
The original example code rebuilt the vector database every time. This project fixes that by splitting the logic:
- `ingest.py` creates the vector database once.
- `chat.py` and `api.py` only load the existing database at runtime.

This reduces latency and follows production RAG practice.

## 5. Technology Stack
- Python 3.11
- FastAPI for backend API
- Static HTML/CSS/JavaScript frontend
- LangChain for orchestration
- Ollama for local LLM and embeddings
- ChromaDB for vector storage
- Docker for containerization
- GitHub Actions for CI smoke testing

## 6. Design Patterns
- Facade: `RagService` hides RAG complexity behind a simple `ask()` method.
- Singleton: `VectorStoreManager` loads the ChromaDB vector store once.
- Factory Method: `ModelFactory` creates LLM and embedding objects from configuration.
- Repository: `LibraryRepository` manages demo book catalog and borrow/return operations.
- Adapter idea: model creation is isolated so the provider can be changed later.

## 7. Main Files
- `requirements.txt`: Python dependencies.
- `ingest.py`: creates vector database.
- `chat.py`: terminal chatbot.
- `api.py`: FastAPI backend and static frontend server.
- `src/rag_service.py`: retrieval + prompt + LLM response.
- `src/library_repository.py`: demo library catalog and borrow/return logic.
- `data/library_system_knowledge.md`: system documentation used by RAG.
- `static/`: web UI.
- `Dockerfile`: container deployment.
- `.github/workflows/ci-pipeline.yml`: CI pipeline.

## 8. Setup Steps
1. Install Ollama.
2. Pull models:
   ```bash
   ollama pull nomic-embed-text
   ollama pull gemma3:4b
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Build vector database:
   ```bash
   python ingest.py
   ```
5. Run terminal chatbot:
   ```bash
   python chat.py
   ```
6. Run web app:
   ```bash
   uvicorn api:app --reload
   ```
7. Open browser:
   ```text
   http://127.0.0.1:8000
   ```

## 9. Demo Scenarios
System questions:
- What is the Library Management System?
- How can a student borrow a book?
- How can a librarian add a book?
- What API endpoints are available?
- What user roles exist?

Rejection examples:
- Who is Messi?
- Tell me about World War II.
- Write code for a restaurant app.
- What is the capital of France?
- Give me personal advice.

## 10. Deployment Plan
For local demo, run the app with Uvicorn. For cloud deployment, use Render or Railway. Add environment variables in the provider dashboard. Do not hardcode secrets. Keep `chroma_db/` persistent or run `python ingest.py` during setup.
