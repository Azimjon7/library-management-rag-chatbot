# 5-Minute Demo Script

## 0:00 - 0:40 Introduction
Hello everyone. Our project is a Library Management System integrated with a RAG-based chatbot. The chatbot is not a general chatbot. It answers only questions about our system using our documentation.

## 0:40 - 1:30 Show Library UI
This page shows the library catalog. Users can search books by title, author, category, or ISBN. For example, I search for "Clean Code" and the system returns the matching book.

## 1:30 - 2:30 System Question Demo
Question: What is the Library Management System?
Expected answer: The bot explains that the system manages books, users, borrowing, returning, overdue tracking, and administration.

## 2:30 - 3:20 API Question Demo
Question: What API endpoints are available?
Expected answer: The bot lists endpoints such as `/api/books`, `/api/books/search`, `/api/borrow`, `/api/return`, and `/api/chat`.

## 3:20 - 4:00 Multi-turn Demo
Question 1: How can a student borrow a book?
Question 2: What happens if the book is not available?
Expected answer: The bot explains availability check and error response.

## 4:00 - 4:40 Rejection Demo
Question: Who is Messi?
Expected answer: I can only answer questions related to our Library Management System.

## 4:40 - 5:00 Conclusion
This project demonstrates document ingestion, chunking, embeddings, ChromaDB vector storage, retrieval, context-aware answer generation, source attribution, rejection handling, and UI integration.
