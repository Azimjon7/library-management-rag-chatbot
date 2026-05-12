# Library Management System Knowledge Base

## System Purpose
The Library Management System is a web-based application for managing books, users, borrowing, returning, overdue tracking, and library administration. It helps students find books, borrow available books, return borrowed books, and see their borrowing history. It helps librarians manage the catalog and monitor overdue books. It helps admins manage users and system settings.

## User Roles
1. Student: can register, login, search books, view book details, borrow available books, return borrowed books, view borrowing history, and ask the chatbot for system guidance.
2. Librarian: can login, add books, update book information, remove books, approve or record borrow requests, process returns, and check overdue items.
3. Admin: can manage users, manage roles, view reports, configure borrowing limits, and monitor system activity.

## Core Features
- Authentication: users login with email and password. Role-based access controls define which actions are allowed.
- Book catalog: stores title, author, ISBN, category, publication year, total copies, available copies, and shelf location.
- Book search: users can search books by title, author, category, or ISBN.
- Borrow book: a student can borrow a book if at least one copy is available and the student has not exceeded the borrow limit.
- Return book: a student or librarian can return a borrowed book. The system increases available copies and closes the borrow transaction.
- Overdue tracking: the system marks books as overdue after the due date.
- Notifications: the system can notify students about due dates and overdue items.
- RAG chatbot: the chatbot answers questions about this system only, using this documentation as its knowledge source.

## Functional Requirements
FR-01 The system shall allow users to register and login using email and password.
FR-02 The system shall allow students to search books by title, author, category, and ISBN.
FR-03 The system shall allow students to borrow available books.
FR-04 The system shall allow students or librarians to return borrowed books.
FR-05 The system shall allow librarians to add, update, and delete books.
FR-06 The system shall allow admins to manage users and assign roles.
FR-07 The system shall display borrowing history for each student.
FR-08 The system shall track overdue books based on due dates.
FR-09 The chatbot shall answer questions about system purpose, features, APIs, authentication, architecture, deployment, and roles.
FR-10 The chatbot shall reject unrelated questions politely.

## Non-Functional Requirements
NFR-01 Performance: normal API responses should complete within 2 seconds.
NFR-02 Usability: a new student should be able to search and borrow a book within 5 minutes of training.
NFR-03 Security: password handling should use secure hashing in a production implementation, and protected endpoints should require authentication.
NFR-04 Availability: the deployed system should be reachable through a public URL during the final demo.
NFR-05 Maintainability: code should be separated into ingestion, retrieval, API, and UI modules.
NFR-06 Portability: the system should include Docker support so it can run consistently across environments.

## API Endpoints
GET /api/health
Description: check if the backend is running.
Response: {"status":"ok"}

GET /api/books
Description: return all books in the demo catalog.
Response: list of book objects with id, title, author, category, isbn, available_copies, and location.

GET /api/books/search?q=clean
Description: search books by title, author, category, or ISBN.
Request parameter: q is the search term.
Response: list of matched books.

POST /api/borrow
Description: borrow a book.
Request body: {"user_id":"student-1", "book_id":"book-1"}
Successful response: {"success":true,"message":"Book borrowed successfully"}
Error response: {"success":false,"message":"Book is not available"}

POST /api/return
Description: return a borrowed book.
Request body: {"user_id":"student-1", "book_id":"book-1"}
Successful response: {"success":true,"message":"Book returned successfully"}

POST /api/chat
Description: ask the RAG chatbot a question about the Library Management System.
Request body: {"question":"How can a student borrow a book?"}
Response: {"answer":"...", "sources":[...]}

## Authentication and Authorization
The demo version uses simplified authentication information in documentation. In production, the system should use JWT or session-based authentication. Students can access catalog, borrow, return, and history features. Librarians can manage book catalog and borrowing operations. Admins can manage users and roles.

## Architecture
The project uses a modular monolith architecture because it is suitable for a small student team and easier to deploy for an MVP. The web UI, API layer, business logic, and data access are organized in separate modules. The RAG chatbot uses a build-time ingestion pipeline and a runtime chat pipeline.

Build time RAG pipeline:
1. Load documents from the data folder.
2. Split documents into overlapping chunks.
3. Generate embeddings using Ollama embedding model.
4. Store embeddings in ChromaDB persistent vector store.

Runtime RAG pipeline:
1. User asks a question in the chat UI.
2. The backend embeds the question.
3. ChromaDB retrieves top relevant chunks.
4. The LLM receives the retrieved context and the question.
5. The chatbot answers using only the context and returns source attribution.
6. If the context is insufficient, the chatbot rejects the question.

## Design Patterns Used
- Facade Pattern: RagService provides one simple interface for chat while hiding retrieval, prompting, and LLM logic.
- Singleton Pattern: VectorStoreManager loads and reuses one ChromaDB connection.
- Factory Method Pattern: ModelFactory creates Ollama LLM and embedding model objects based on configuration.
- Repository Pattern: LibraryRepository manages book and borrow data access.
- Adapter Pattern: OllamaAdapter wraps Ollama model calls so the rest of the application is not tightly coupled to the provider.

## Deployment
The project can run locally with Python and Ollama. It can also be containerized with Docker. For cloud deployment, use a PaaS provider such as Render or Railway. Environment variables should store model names, data directory, database directory, and any secrets.

## Common Troubleshooting
If the chatbot says it cannot answer, check that the question is related to the Library Management System and that the vector database was created with python ingest.py.
If Ollama connection fails, install Ollama and pull the required models.
If ChromaDB is empty, delete chroma_db and run python ingest.py again.
If packages are missing, run pip install -r requirements.txt.

## Off-topic Rejection Policy
The chatbot must only answer questions about the Library Management System. If a user asks about sports, politics, history, unrelated coding tasks, personal advice, or other systems, the chatbot should respond: I can only answer questions related to our Library Management System.
