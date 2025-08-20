import pytest
from unittest.mock import patch
import sys
sys.path.append('..')

from book import Book
from library import Library
from library_cli import LibraryCLI


class TestBasicFunctionality:
    """Basic tests for core functionality"""
    
    def test_book_creation(self):
        """Test creating a book"""
        book = Book("Test Title", "Test Author", "1234567890")
        assert book.title == "Test Title"
        assert book.author == "Test Author"
        assert book.isbn == "1234567890"
    
    def test_book_string_representation(self):
        """Test book string representation"""
        book = Book("Tutunamayanlar", "Oğuz Atay", "9781234567890")
        expected = "Tutunamayanlar by Oğuz Atay (ISBN: 9781234567890)"
        assert str(book) == expected
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_library_empty_creation(self, mock_load, mock_client):
        """Test creating empty library"""
        library = Library([])
        assert len(library.books) == 0
        mock_load.assert_called_once()
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_library_add_book(self, mock_load, mock_client_class):
        """Test adding a book to library"""
        mock_book = Book("Test Book", "Test Author", "1234567890")
        
        mock_client_instance = mock_client_class.return_value
        mock_client_instance.get_book_by_isbn.return_value = mock_book
        
        library = Library([])
        library.add_book("1234567890")
        
        assert len(library.books) == 1
        assert library.books[0].title == mock_book.title
        assert library.books[0].author == mock_book.author
        assert library.books[0].isbn == mock_book.isbn
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_library_unique_isbn_validation(self, mock_load, mock_client):
        """Test ISBN uniqueness validation"""
        mock_book1 = Book("Book One", "Author One", "1234567890")
        mock_book2 = Book("Book Two", "Author Two", "1234567890")
        mock_client.return_value.get_book_by_isbn.side_effect = [mock_book1, mock_book2]
        
        library = Library([])
        library.add_book("1234567890")
        
        with pytest.raises(ValueError, match="ISBN must be unique"):
            library.add_book("1234567890")
    
    @patch('library.OpenLibraryClient')
    @patch.object(Library, 'load_books')
    def test_library_find_books(self, mock_load, mock_client):
        """Test finding books by different criteria"""
        library = Library([])
        book1 = Book("Tehlikeli Oyunlar", "Oğuz Atay", "1111111111")
        book2 = Book("Martin Eden", "Jack London", "2222222222")
        
        # Directly add books to test find functionality
        library.books = [book1, book2]
        
        # Find by title
        results = library.find_book("Tehlike", "title")
        assert len(results) == 1
        assert results[0] == book1
        
        # Find by author
        results = library.find_book("Jack", "author")
        assert len(results) == 1
        assert results[0] == book2
        
        # Find by ISBN
        results = library.find_book("1111111111", "isbn")
        assert len(results) == 1
        assert results[0] == book1
    
    def test_cli_initialization(self):
        """Test CLI initialization"""
        with patch('library.OpenLibraryClient'):
            with patch.object(Library, 'load_books'):
                cli = LibraryCLI()
                assert cli.library is not None
                assert hasattr(cli.library, 'books')
    
    def test_cli_menu_display(self):
        """Test CLI menu display"""
        with patch('library.OpenLibraryClient'):
            with patch.object(Library, 'load_books'):
                cli = LibraryCLI()
                
                with patch('builtins.print') as mock_print:
                    cli.display_menu()
                    
                    # Check that menu was printed
                    assert mock_print.call_count > 0
                    
                    # Get all printed text
                    calls = [str(call) for call in mock_print.call_args_list]
                    menu_text = ' '.join(calls)
                    
                    # Check for key menu items
                    assert "LIBRARY MANAGEMENT SYSTEM" in menu_text
                    assert "Add a new book" in menu_text
                    assert "Exit" in menu_text
    
    def test_cli_handle_choice_exit(self):
        """Test CLI exit choice"""
        with patch('library.OpenLibraryClient'):
            with patch.object(Library, 'load_books'):
                cli = LibraryCLI()
                
                with patch('builtins.print') as mock_print:
                    result = cli.handle_choice('8')
                    
                    assert result is False  # Should return False to exit
                    mock_print.assert_called_with("👋 Thank you for using Library Management System!")
    
    def test_cli_handle_choice_invalid(self):
        """Test CLI invalid choice"""
        with patch('library.OpenLibraryClient'):
            with patch.object(Library, 'load_books'):
                cli = LibraryCLI()
                
                with patch('builtins.print') as mock_print:
                    result = cli.handle_choice('99')
                    
                    assert result is True  # Should continue
                    mock_print.assert_called_with("❌ Invalid choice! Please enter 1-8.")
