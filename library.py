import json
from typing import Literal
from book import Book
from open_library import OpenLibraryClient

class Library():
    def __init__(self, books:list[Book]=[], file_path:str="library.json"):
        self.books = books
        self.load_books(file_path)
        self.open_library_client = OpenLibraryClient()

    def add_book(self, isbn:str):
        for existing_book in self.books:
            if existing_book.isbn == isbn:
                raise ValueError(f"ISBN must be unique. Already exists: {existing_book}")
        
        book = self.open_library_client.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")
        self.books.append(book)
    
    def search_books_online(self, query:str):
        books = self.open_library_client.search_books(query)
        for book in books:
            print(book)

    def remove_book(self, isbn:str):
        for ix,book in enumerate(self.books):
            if book.isbn == isbn:
                self.books.pop(ix)
                print(f"Removed {book.title} from the library")
                break
        else:
            print(f"Book with ISBN {isbn} not found")
        
    def list_books(self):
        for book in self.books:
            print(book)
        

    def find_book(self, query: str, search_by: Literal["title", "author", "isbn"] = "title"):
        query_lower = query.lower()
        matching_books = []
        
        for book in self.books:
            if search_by == "title" and query_lower in book.title.lower():
                matching_books.append(book)
            elif search_by == "author" and query_lower in book.author.lower():
                matching_books.append(book)
            elif search_by == "isbn" and query_lower == book.isbn.lower():
                matching_books.append(book)
        
        return matching_books
    
    def load_books(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                books_data = json.load(file)
                for book_data in books_data:
                    book = Book(**book_data)
                    if any(existing_book.isbn == book.isbn for existing_book in self.books):
                        continue
                    self.books.append(book)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def save_books(self, file_path: str = "library.json"):
        books_data = [book.__dict__ for book in self.books]
        with open(file_path, 'w') as file:
            json.dump(books_data, file, ensure_ascii=False, indent=4)
    
