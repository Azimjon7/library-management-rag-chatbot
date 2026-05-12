# Test Evidence Plan

## 10 Successful System-Related Q&A Pairs
1. Q: What is the Library Management System?  
   Expected: Explains system purpose.
2. Q: What roles exist in the system?  
   Expected: Student, Librarian, Admin.
3. Q: How can a student borrow a book?  
   Expected: Search book, check availability, borrow.
4. Q: How can a book be returned?  
   Expected: Return endpoint/process and available copy increase.
5. Q: How can a librarian add a book?  
   Expected: Librarian manages catalog.
6. Q: What API endpoint searches books?  
   Expected: GET /api/books/search?q=...
7. Q: What API endpoint is used for chatbot?  
   Expected: POST /api/chat.
8. Q: What is the architecture of the chatbot?  
   Expected: Build-time ingestion + runtime retrieval.
9. Q: What database is used for vector storage?  
   Expected: ChromaDB.
10. Q: How is the system deployed?  
    Expected: Python/Uvicorn locally, Docker/Render/Railway for cloud.

## 5 Rejection Cases
1. Q: Who is Messi?  
   Expected: I can only answer questions related to our Library Management System.
2. Q: What is the capital of France?  
   Expected: Rejection.
3. Q: Tell me World War II history.  
   Expected: Rejection.
4. Q: Give me personal relationship advice.  
   Expected: Rejection.
5. Q: Generate a restaurant app.  
   Expected: Rejection.
