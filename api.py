from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from library import Library
from book import Book

app = FastAPI(title="Library API", description="Simple library management API")

library = Library()

# Pydantic models
class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

class ISBN(BaseModel):
    isbn: str

class BookSearch(BaseModel):
    query: str
    search_by: Optional[str] = "title"

class ErrorResponse(BaseModel):
    error: str


@app.get("/books", response_model=List[BookResponse])
async def get_books():
    return library.books

@app.post("/books", response_model=BookResponse)
async def add_book(book_data: ISBN):
    try:
        library.add_book(book_data.isbn)
        
        matching_books = library.find_book(book_data.isbn, "isbn")
        if matching_books:
            library.save_books()  
            return matching_books[0]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add book: {str(e)}")


@app.delete("/books/{isbn}")
async def delete_book(isbn: str):
    book_exists = any(book.isbn == isbn for book in library.books)
    if not book_exists:
        raise HTTPException(status_code=404, detail=f"Book with ISBN {isbn} not found")
    
    library.remove_book(isbn)
    library.save_books()
    return {"message": f"Book with ISBN {isbn} has been removed"}


@app.get("/books/search", response_model=List[BookResponse])
async def search_books(query: str, search_by: str = "title"):
    try:
        matching_books = library.find_book(query, search_by)
        return matching_books
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/books/search/online", response_model=List[BookResponse])
async def search_books_online(query: str):
    books = library.open_library_client.search_books(query)
    return books


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
