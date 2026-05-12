from datetime import datetime, timezone


class LibraryRepository:
    """Repository pattern: central place for demo book and borrow data."""

    def __init__(self):
        self.books = [
            {"id": "book-1", "title": "Clean Code", "author": "Robert C. Martin", "category": "Software Engineering", "isbn": "978-0132350884", "total_copies": 5, "available_copies": 3, "location": "Shelf A1"},
            {"id": "book-2", "title": "Design Patterns", "author": "Gang of Four", "category": "Software Engineering", "isbn": "978-0201633610", "total_copies": 4, "available_copies": 4, "location": "Shelf A2"},
            {"id": "book-3", "title": "Introduction to Algorithms", "author": "Cormen et al.", "category": "Algorithms", "isbn": "978-0262033848", "total_copies": 6, "available_copies": 2, "location": "Shelf B1"},
            {"id": "book-4", "title": "Artificial Intelligence: A Modern Approach", "author": "Russell & Norvig", "category": "AI", "isbn": "978-0134610993", "total_copies": 3, "available_copies": 0, "location": "Shelf C1"},
            {"id": "book-5", "title": "Database System Concepts", "author": "Silberschatz et al.", "category": "Databases", "isbn": "978-0078022159", "total_copies": 4, "available_copies": 3, "location": "Shelf D1"},
            {"id": "book-6", "title": "Computer Networks", "author": "Andrew Tanenbaum", "category": "Networking", "isbn": "978-0133499469", "total_copies": 3, "available_copies": 1, "location": "Shelf E1"},
            {"id": "book-7", "title": "FastAPI in Action", "author": "Bill Lubanovic", "category": "FastAPI", "isbn": "978-1617299643", "total_copies": 5, "available_copies": 5, "location": "Shelf F1"},
            {"id": "book-8", "title": "Python Crash Course", "author": "Eric Matthes", "category": "Python", "isbn": "978-1718502703", "total_copies": 7, "available_copies": 4, "location": "Shelf G1"},
            {"id": "book-9", "title": "Deep Learning", "author": "Goodfellow et al.", "category": "Machine Learning", "isbn": "978-0262035613", "total_copies": 4, "available_copies": 2, "location": "Shelf C2"},
            {"id": "book-10", "title": "Machine Learning Engineering", "author": "Andriy Burkov", "category": "Machine Learning", "isbn": "978-1999579579", "total_copies": 3, "available_copies": 3, "location": "Shelf C3"},
            {"id": "book-11", "title": "The Web Application Hacker's Handbook", "author": "Stuttard & Pinto", "category": "Cybersecurity", "isbn": "978-1118026472", "total_copies": 2, "available_copies": 1, "location": "Shelf H1"},
            {"id": "book-12", "title": "Hacking: The Art of Exploitation", "author": "Jon Erickson", "category": "Cybersecurity", "isbn": "978-1593271442", "total_copies": 3, "available_copies": 2, "location": "Shelf H2"},
            {"id": "book-13", "title": "Learning Web Design", "author": "Jennifer Robbins", "category": "Web Development", "isbn": "978-1491960202", "total_copies": 4, "available_copies": 4, "location": "Shelf I1"},
            {"id": "book-14", "title": "You Don't Know JS", "author": "Kyle Simpson", "category": "Web Development", "isbn": "978-1491904244", "total_copies": 5, "available_copies": 3, "location": "Shelf I2"},
            {"id": "book-15", "title": "Kubernetes in Action", "author": "Marko Luksa", "category": "DevOps", "isbn": "978-1617293726", "total_copies": 4, "available_copies": 4, "location": "Shelf J1"},
            {"id": "book-16", "title": "The Phoenix Project", "author": "Gene Kim et al.", "category": "DevOps", "isbn": "978-1942788294", "total_copies": 3, "available_copies": 2, "location": "Shelf J2"},
            {"id": "book-17", "title": "Fluent Python", "author": "Luciano Ramalho", "category": "Python", "isbn": "978-1492056355", "total_copies": 5, "available_copies": 5, "location": "Shelf G2"},
            {"id": "book-18", "title": "Natural Language Processing with Python", "author": "Bird et al.", "category": "AI", "isbn": "978-0596516499", "total_copies": 4, "available_copies": 3, "location": "Shelf C4"},
            {"id": "book-19", "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "category": "Databases", "isbn": "978-1449373320", "total_copies": 6, "available_copies": 1, "location": "Shelf D2"},
            {"id": "book-20", "title": "Network Security Essentials", "author": "William Stallings", "category": "Networking", "isbn": "978-0134527338", "total_copies": 3, "available_copies": 3, "location": "Shelf E2"},
        ]
        self.borrowed = []

    def list_books(self):
        return self.books

    def list_borrowed(self):
        return self.borrowed

    def search_books(self, query: str):
        q = query.lower()
        return [
            book for book in self.books
            if q in book["title"].lower()
            or q in book["author"].lower()
            or q in book["category"].lower()
            or q in book["isbn"].lower()
        ]

    def borrow_book(self, user_id: str, book_id: str):
        book = self._find_book(book_id)
        if not book:
            return {"success": False, "message": "Book not found"}
        if book["available_copies"] <= 0:
            return {"success": False, "message": "Book is not available"}
        book["available_copies"] -= 1
        self.borrowed.append({
            "user_id": user_id,
            "book_id": book_id,
            "book_title": book["title"],
            "status": "borrowed",
            "borrowed_at": datetime.now(timezone.utc).isoformat(),
        })
        return {"success": True, "message": "Book borrowed successfully", "book": book}

    def return_book(self, user_id: str, book_id: str):
        book = self._find_book(book_id)
        if not book:
            return {"success": False, "message": "Book not found"}
        for item in self.borrowed:
            if item["user_id"] == user_id and item["book_id"] == book_id and item["status"] == "borrowed":
                item["status"] = "returned"
                item["returned_at"] = datetime.now(timezone.utc).isoformat()
                book["available_copies"] += 1
                return {"success": True, "message": "Book returned successfully", "book": book}
        return {"success": False, "message": "Borrow record not found"}

    def get_dashboard_summary(self):
        active_borrows = [item for item in self.borrowed if item["status"] == "borrowed"]
        returned = [item for item in self.borrowed if item["status"] == "returned"]
        total_copies = sum(book.get("total_copies", book["available_copies"]) for book in self.books)
        available_copies = sum(book["available_copies"] for book in self.books)
        unavailable_books = [book for book in self.books if book["available_copies"] == 0]

        return {
            "totals": {
                "books": len(self.books),
                "total_copies": total_copies,
                "available_copies": available_copies,
                "active_borrows": len(active_borrows),
                "returned": len(returned),
                "unavailable_books": len(unavailable_books),
            },
            "books": self.books,
            "borrowed": list(reversed(self.borrowed[-12:])),
        }

    def _find_book(self, book_id: str):
        return next((book for book in self.books if book["id"] == book_id), None)
