# Library Management System with RAG Chatbot

This project is a Software Engineering final assessment project. It integrates a RAG-based chatbot into a Library Management System.

## What the chatbot does
- Answers questions about the Library Management System.
- Explains features, roles, APIs, authentication, architecture, and deployment.
- Shows source metadata from retrieved documents.
- Rejects unrelated questions.

## Run locally

### 1. Install Ollama and pull models
```bash
ollama pull nomic-embed-text
ollama pull gemma3:4b
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Build vector database once
```bash
python ingest.py
```

### 4. Run terminal chatbot
```bash
python chat.py
```

### 5. Run web app
```bash
uvicorn api:app --reload
```

Open:
```text
http://127.0.0.1:8000
```

## Important files
- `ingest.py`: creates ChromaDB vector database from `data/` documents.
- `chat.py`: command-line chatbot.
- `api.py`: FastAPI backend and frontend server.
- `src/rag_service.py`: RAG retrieval and answer generation.
- `data/library_system_knowledge.md`: system knowledge base.
- `docs/technical_documentation.md`: documentation for submission.
- `docs/demo_script.md`: 5-minute presentation script.
- `docs/test_evidence.md`: Q&A and rejection test plan.

## Git workflow
Use branch:
```bash
git checkout -b feature/rag-chatbot
```
Commit example:
```bash
git add .
git commit -m "Add RAG chatbot integration"
git push origin feature/rag-chatbot
```

## Notes
The vector database is not committed by default because it is generated locally. Run `python ingest.py` after installing Ollama models.


## FastAPI Backend

This version uses **FastAPI** as the backend. The main backend file is `app.py`.

Run the project:

```bash
pip install -r requirements.txt
ollama pull gemma3:4b
ollama pull nomic-embed-text
python ingest.py
uvicorn app:app --reload
```

Then open:

- Web UI: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin.html
- API docs: http://127.0.0.1:8000/docs
- Chat endpoint: POST http://127.0.0.1:8000/api/chat

Default demo admin credentials:

```text
username: admin
password: library2026
```

You can override them with `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`.

Chat mode:

```text
USE_OLLAMA_RAG=false
```

The default `false` mode keeps the web chatbot fast by answering from the local Library Management System knowledge base. Set it to `true` when Ollama is responsive and you want full vector retrieval + LLM generation.

AI stack used:

- LLM: Ollama `gemma3:4b`
- Embeddings: Ollama `nomic-embed-text`
- Vector DB: ChromaDB
- RAG framework: LangChain
- Backend: FastAPI
