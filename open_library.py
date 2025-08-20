import httpx
from typing import Optional, Dict, Any, List
from book import Book


class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"
    SEARCH_URL = f"{BASE_URL}/search.json"
    BOOKS_URL = f"{BASE_URL}/api/books"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def search_books(self, query: str, limit: int = 10) -> List[Book]:
        params = {
            "q": query,
            "limit": limit,
            "fields": "title,author_name,isbn"
        }
        
        try:
            response = self.client.get(self.SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()

            books = []
            docs = data.get("docs", [])
            
            for doc in docs:
                book = self._parse_search_result(doc)
                if book:
                    books.append(book)
            
            return books
            
        except httpx.RequestError as e:
            print(f"Error searching books: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        params = {
            "bibkeys": f"ISBN:{isbn}",
            "jscmd": "data",
            "format": "json"
        }
        
        try:
            response = self.client.get(self.BOOKS_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            isbn_key = f"ISBN:{isbn}"
            if isbn_key in data:
                return self._parse_book_data(data[isbn_key], isbn)
            
            return None
            
        except httpx.RequestError as e:
            print(f"Error fetching book by ISBN: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def _parse_search_result(self, doc: Dict[str, Any]) -> Optional[Book]:
        try:
            title = doc.get("title", "Unknown Title")
            authors = doc.get("author_name", [])
            isbn_list = doc.get("isbn", [])
            
            author = authors[0] if authors else "Unknown Author"
            isbn = isbn_list[0] if isbn_list else "Unknown ISBN"
            
            return Book(title, author, isbn)
            
        except Exception as e:
            print(f"Error parsing search result: {e}")
            return None
    
    def _parse_book_data(self, book_data: Dict[str, Any], isbn: str) -> Book:
        title = book_data.get("title", "Unknown Title")
        
        authors = []
        if "authors" in book_data:
            authors = [author.get("name", "") for author in book_data["authors"]]
        
        author = authors[0] if authors else "Unknown Author"
        
        return Book(title, author, isbn)
    

def main():
    with OpenLibraryClient() as client:
        query = input("Enter a query: ")
        
        print(f"🔍 Searching for '{query}'...")
        books = client.search_books(query, limit=3)
        
        for i, book in enumerate(books, 1):
            print(f"\n📚 Book {i}: {book}")
        
        print("\n" + "="*50)
        print("📖 Getting book by ISBN...")
        
        isbn = input("Enter ISBN: ")
        book = client.get_book_by_isbn(isbn)
        if book:
            print(f"Found: {book}")
        else:
            print("Book not found!")


if __name__ == "__main__":
    main()
