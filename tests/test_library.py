import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
import sys
sys.path.append('..')

from library import Library
from book import Book


class TestLibrary:
    """Test cases for the Library class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.book1 = Book("Book One", "Author One", "1111111111")
        self.book2 = Book("Book Two", "Author Two", "2222222222")
        self.book3 = Book("Python Guide", "Author One", "3333333333")
    
    @patch.object(Library, 'load_books')
    def test_library_creation_empty(self, mock_load):
        """Test creating an empty library"""
        library = Library([])
        assert len(library.books) == 0
        mock_load.assert_called_once()
    
    @patch.object(Library, 'load_books')
    def test_library_creation_with_books(self, mock_load):
        """Test creating a library with initial books"""
        books = [self.book1, self.book2]
        library = Library(books)
        assert len(library.books) == 2
        assert self.book1 in library.books
        assert self.book2 in library.books
        mock_load.assert_called_once()
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_add_book_success(self, mock_load, mock_client_class):
        """Test adding a book successfully"""
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.get_book_by_isbn.return_value = self.book1
        
        library = Library([])
        library.add_book(self.book1.isbn)
        
        assert len(library.books) == 1
        assert library.books[0].isbn == self.book1.isbn
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_add_book_duplicate_isbn(self, mock_load, mock_client_class):
        """Test adding a book with duplicate ISBN raises error"""
        library = Library([self.book1])
        
        with pytest.raises(ValueError, match="ISBN must be unique"):
            library.add_book("1111111111")  # Same ISBN as self.book1
    
    @patch.object(Library, 'load_books')
    def test_remove_book_success(self, mock_load):
        """Test removing a book successfully"""
        library = Library([self.book1, self.book2])
        
        with patch('builtins.print') as mock_print:
            library.remove_book("1111111111")
            mock_print.assert_called_with("Removed Book One from the library")
        
        assert len(library.books) == 1
        assert self.book1 not in library.books
        assert self.book2 in library.books
    
    @patch.object(Library, 'load_books')
    def test_remove_book_not_found(self, mock_load):
        """Test removing a non-existent book"""
        library = Library([self.book1])
        
        with patch('builtins.print') as mock_print:
            library.remove_book("9999999999")
            mock_print.assert_called_with("Book with ISBN 9999999999 not found")
        
        assert len(library.books) == 1
    
    @patch.object(Library, 'load_books')
    def test_list_books(self, mock_load):
        """Test listing all books"""
        library = Library([self.book1, self.book2])
        
        with patch('builtins.print') as mock_print:
            library.list_books()
            
            # Check that print was called for each book
            assert mock_print.call_count == 2
    
    @patch.object(Library, 'load_books')
    def test_find_book_by_title(self, mock_load):
        """Test finding books by title"""
        library = Library([self.book1, self.book2, self.book3])
        
        # Exact match
        results = library.find_book("Book One", "title")
        assert len(results) == 1
        assert self.book1 in results
        
        # Partial match
        results = library.find_book("book", "title")
        assert len(results) == 2
        
        # Case insensitive
        results = library.find_book("BOOK ONE", "title")
        assert len(results) == 1
        assert self.book1 in results
    
    @patch.object(Library, 'load_books')
    def test_find_book_by_author(self, mock_load):
        """Test finding books by author"""
        library = Library([self.book1, self.book2, self.book3])
        
        results = library.find_book("Author One", "author")
        assert len(results) == 2
        assert self.book1 in results
        assert self.book3 in results
    
    @patch.object(Library, 'load_books')
    def test_find_book_by_isbn(self, mock_load):
        """Test finding books by ISBN"""
        library = Library([self.book1, self.book2])
        
        # Exact match only for ISBN
        results = library.find_book("1111111111", "isbn")
        assert len(results) == 1
        assert self.book1 in results
        
        # Partial match should not work for ISBN
        results = library.find_book("1111", "isbn")
        assert len(results) == 0
    
    @patch.object(Library, 'load_books')
    def test_find_book_no_results(self, mock_load):
        """Test finding books with no matches"""
        library = Library([self.book1])
        
        results = library.find_book("Nonexistent", "title")
        assert len(results) == 0
    
    @patch.object(Library, 'load_books')
    def test_save_books_success(self, mock_load):
        """Test saving books to file successfully"""
        library = Library([self.book1, self.book2])
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_path = temp_file.name
        
        try:
            library.save_books(temp_path)
            
            # Verify file was created and contains correct data
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            assert len(data) == 2
            assert data[0]['title'] == "Book One"
            assert data[1]['title'] == "Book Two"
            
        finally:
            os.unlink(temp_path)
    
    @patch('library.OpenLibraryClient')
    def test_load_books_success(self, mock_client_class):
        """Test loading books from file successfully"""
        # Create library with mocked client and bypassing initial load_books
        with patch.object(Library, 'load_books'):
            library = Library([])
        
        test_data = [
            {"title": "Test Book", "author": "Test Author", "isbn": "1234567890"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name
        
        try:
            # Call the actual load_books method
            Library.load_books(library, temp_path)
            
            assert len(library.books) == 1
            assert library.books[0].title == "Test Book"
            assert library.books[0].author == "Test Author"
            assert library.books[0].isbn == "1234567890"
            
        finally:
            os.unlink(temp_path)
    
    @patch('library.OpenLibraryClient')
    def test_load_books_file_not_found(self, mock_client_class):
        """Test loading books from non-existent file"""
        library = Library([])
        
        with patch('builtins.print') as mock_print:
            # Call the real load_books method
            library.load_books("nonexistent.json")
            
            # Should print an error message
            mock_print.assert_called()
            error_message = str(mock_print.call_args[0][0])
            assert "An error occurred" in error_message
    
    @patch('library.OpenLibraryClient')
    def test_load_books_duplicate_isbn_in_file(self, mock_client_class):
        """Test loading books with duplicate ISBN from file"""
        # Create library bypassing initial load_books
        with patch.object(Library, 'load_books'):
            library = Library([])
        library.books = [self.book1]  # Pre-existing book (add after initialization)
        
        test_data = [
            {"title": "Duplicate", "author": "Test", "isbn": "1111111111"}  # Same ISBN as book1
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name
        
        try:
            # Call the actual load_books method
            Library.load_books(library, temp_path)
            
            # Original book should still be there, duplicate not added
            assert len(library.books) == 1
            
        finally:
            os.unlink(temp_path)