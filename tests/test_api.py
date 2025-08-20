import pytest
from fastapi.testclient import TestClient
import json
import os
import tempfile
from api import app
from library import Library

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def temp_library_file():
    """Create a temporary library file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([], f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)

class TestAPIEndpoints:
    
    def test_get_books_empty(self, client):
        """Test GET /books with empty library"""
        response = client.get("/books")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_books_with_data(self, client):
        """Test GET /books with existing books"""
        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert isinstance(books, list)
        # Check that each book has required fields
        for book in books:
            assert "title" in book
            assert "author" in book
            assert "isbn" in book
    
    def test_add_book_valid_isbn(self, client):
        """Test POST /books with valid ISBN"""
        test_isbn = "9782848300443"
        response = client.post("/books", json={"isbn": test_isbn})
        
        if response.status_code == 200:
            book = response.json()
            assert book["isbn"] == test_isbn
            assert "title" in book
            assert "author" in book
        elif response.status_code == 400:
            # Book might already exist or ISBN might be invalid
            assert "error" in response.json()["detail"].lower() or "already exists" in response.json()["detail"].lower()
    
    def test_add_book_invalid_isbn(self, client):
        """Test POST /books with invalid ISBN"""
        response = client.post("/books", json={"isbn": "invalid-isbn"})
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_add_book_duplicate_isbn(self, client):
        """Test POST /books with duplicate ISBN"""
        test_isbn = "9782848300443"
        
        # Try to add the same book twice
        client.post("/books", json={"isbn": test_isbn})
        response = client.post("/books", json={"isbn": test_isbn})
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
    
    def test_delete_book_existing(self, client):
        """Test DELETE /books/{isbn} with existing book"""
        test_isbn = "9782848300443"
        
        # First add a book
        add_response = client.post("/books", json={"isbn": test_isbn})
        if add_response.status_code == 200:
            # Then delete it
            delete_response = client.delete(f"/books/{test_isbn}")
            assert delete_response.status_code == 200
            assert "removed" in delete_response.json()["message"].lower()
    
    def test_delete_book_nonexistent(self, client):
        """Test DELETE /books/{isbn} with non-existent book"""
        response = client.delete("/books/nonexistent-isbn")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_search_books_in_library(self, client):
        """Test GET /books/search"""
        response = client.get("/books/search?query=test&search_by=title")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_books_online(self, client):
        """Test GET /books/search/online"""
        response = client.get("/books/search/online?query=python")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        # If results exist, check structure
        if results:
            for book in results[:3]:  # Check first 3 results
                assert "title" in book
                assert "author" in book
                assert "isbn" in book

class TestAPIValidation:
    
    def test_post_books_missing_isbn(self, client):
        """Test POST /books without ISBN field"""
        response = client.post("/books", json={})
        assert response.status_code == 422  # Validation error
    
    def test_post_books_empty_isbn(self, client):
        """Test POST /books with empty ISBN"""
        response = client.post("/books", json={"isbn": ""})
        assert response.status_code == 400
    
    def test_search_missing_query(self, client):
        """Test search endpoints without query parameter"""
        response = client.get("/books/search")
        assert response.status_code == 422  # Missing required parameter
        
        response = client.get("/books/search/online")
        assert response.status_code == 422  # Missing required parameter
    
    def test_search_invalid_search_by(self, client):
        """Test search with invalid search_by parameter"""
        response = client.get("/books/search?query=test&search_by=invalid")
        # Should still return results, just might not find anything
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestAPIIntegration:
    
    def test_full_book_lifecycle(self, client):
        """Test complete add -> get -> delete cycle"""
        test_isbn = "9782848300443"
        
        # 1. Add book
        add_response = client.post("/books", json={"isbn": test_isbn})
        if add_response.status_code == 400 and "already exists" in add_response.json()["detail"].lower():
            # Book already exists, delete it first
            client.delete(f"/books/{test_isbn}")
            add_response = client.post("/books", json={"isbn": test_isbn})
        
        assert add_response.status_code == 200
        added_book = add_response.json()
        
        # 2. Verify book is in library
        get_response = client.get("/books")
        assert get_response.status_code == 200
        books = get_response.json()
        assert any(book["isbn"] == test_isbn for book in books)
        
        # 3. Search for the book
        search_response = client.get(f"/books/search?query={test_isbn}&search_by=isbn")
        assert search_response.status_code == 200
        found_books = search_response.json()
        assert len(found_books) == 1
        assert found_books[0]["isbn"] == test_isbn
        
        # 4. Delete book
        delete_response = client.delete(f"/books/{test_isbn}")
        assert delete_response.status_code == 200
        
        # 5. Verify book is gone
        final_search = client.get(f"/books/search?query={test_isbn}&search_by=isbn")
        assert final_search.status_code == 200
        assert len(final_search.json()) == 0
