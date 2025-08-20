import pytest
from book import Book


class TestBook:
    """Test cases for the Book class"""
    
    def test_book_creation(self):
        """Test creating a book with valid parameters"""
        book = Book("Test Title", "Test Author", "1234567890")
        
        assert book.title == "Test Title"
        assert book.author == "Test Author"
        assert book.isbn == "1234567890"
    
    def test_book_str_representation(self):
        """Test the string representation of a book"""
        book = Book("Python Programming", "John Doe", "9781234567890")
        expected = "Python Programming by John Doe (ISBN: 9781234567890)"
        
        assert str(book) == expected
    
    def test_book_with_empty_strings(self):
        """Test creating a book with empty strings"""
        book = Book("", "", "")
        
        assert book.title == ""
        assert book.author == ""
        assert book.isbn == ""
    
    def test_book_with_special_characters(self):
        """Test creating a book with special characters"""
        book = Book("Çakıl'ın Hayatı", "Müslüm Öztürk", "978-605-123-456-7")
        
        assert book.title == "Çakıl'ın Hayatı"
        assert book.author == "Müslüm Öztürk"
        assert book.isbn == "978-605-123-456-7"
    
    def test_book_equality_not_implemented(self):
        """Test that books don't have equality comparison by default"""
        book1 = Book("Same Title", "Same Author", "1234567890")
        book2 = Book("Same Title", "Same Author", "1234567890")
        
        # Books are different objects even with same content
        assert book1 is not book2
