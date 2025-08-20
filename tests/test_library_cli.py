import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('..')

from library_cli import LibraryCLI
from library import Library
from book import Book


class TestLibraryCLI:
    """Test cases for the LibraryCLI class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        with patch('open_library.OpenLibraryClient'):
            with patch.object(Library, 'load_books'):
                self.cli = LibraryCLI()
                # Ensure we start with an empty library for each test
                self.cli.library.books = []
    
    def test_cli_initialization(self):
        """Test CLI initialization creates a library"""
        assert self.cli.library is not None
        assert hasattr(self.cli.library, 'books')
    
    def test_display_menu(self):
        """Test menu display prints correct options"""
        with patch('builtins.print') as mock_print:
            self.cli.display_menu()
            
            # Check that menu items are printed
            calls = [str(call) for call in mock_print.call_args_list]
            menu_text = ' '.join(calls)
            
            assert "LIBRARY MANAGEMENT SYSTEM" in menu_text
            assert "Add a new book" in menu_text
            assert "Remove a book" in menu_text
            assert "List all books" in menu_text
            assert "Find books" in menu_text
            assert "Load books from file" in menu_text
            assert "Save books to file" in menu_text
            assert "Exit" in menu_text
    
    @patch('builtins.input')
    def test_add_book_menu_success(self, mock_input):
        """Test adding a book through menu successfully"""
        mock_input.return_value = "1111111111"
        
        # Mock the Open Library client to return a book
        test_book = Book("Test Title", "Test Author", "1111111111")
        with patch.object(self.cli.library.open_library_client, 'get_book_by_isbn', return_value=test_book):
            with patch('builtins.print') as mock_print:
                self.cli.add_book_menu()
                
                # Check success message was printed
                calls = [str(call) for call in mock_print.call_args_list]
                success_message = ' '.join(calls)
                assert "Successfully added" in success_message
            
            # Check book was added to library
            assert len(self.cli.library.books) == 1
            assert self.cli.library.books[0].title == "Test Title"
    
    @patch('builtins.input')
    def test_add_book_menu_empty_fields(self, mock_input):
        """Test adding book with empty ISBN shows error"""
        mock_input.return_value = ""
        
        with patch('builtins.print') as mock_print:
            self.cli.add_book_menu()
            
            mock_print.assert_called_with("❌ ISBN is required!")
        
        # No book should be added
        assert len(self.cli.library.books) == 0
    
    @patch('builtins.input')
    def test_add_book_menu_duplicate_isbn(self, mock_input):
        """Test adding book with duplicate ISBN shows error"""
        # Add a book first
        existing_book = Book("Existing", "Author", "2222222222")
        self.cli.library.books.append(existing_book)
        
        mock_input.return_value = "2222222222"
        
        with patch('builtins.print') as mock_print:
            self.cli.add_book_menu()
            
            # Check error message was printed
            calls = [str(call) for call in mock_print.call_args_list]
            error_message = ' '.join(calls)
            assert "Error" in error_message and "ISBN must be unique" in error_message
    
    @patch('builtins.input')
    def test_remove_book_menu_success(self, mock_input):
        """Test removing a book through menu successfully"""
        # Add a book first
        test_book = Book("Test Book", "Test Author", "3333333333")
        self.cli.library.books.append(test_book)
        
        mock_input.return_value = "3333333333"
        
        with patch('builtins.print') as mock_print:
            self.cli.remove_book_menu()
            
            # Library's remove_book method should have been called
            assert len(self.cli.library.books) == 0
    
    @patch('builtins.input')
    def test_remove_book_menu_empty_isbn(self, mock_input):
        """Test removing book with empty ISBN shows error"""
        mock_input.return_value = ""
        
        with patch('builtins.print') as mock_print:
            self.cli.remove_book_menu()
            
            mock_print.assert_called_with("❌ ISBN is required!")
    
    def test_list_books_menu_with_books(self):
        """Test listing books when library has books"""
        # Directly add book to library for testing
        test_book = Book("Test Book", "Test Author", "4444444444")
        self.cli.library.books.append(test_book)
        
        with patch('builtins.print') as mock_print:
            self.cli.list_books_menu()
            
            # Check that books header and book are printed
            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            assert "All Books in Library" in output
    
    def test_list_books_menu_empty(self):
        """Test listing books when library is empty"""
        with patch('builtins.print') as mock_print:
            self.cli.list_books_menu()
            
            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            assert "No books in library" in output
    
    @patch('builtins.input')
    def test_find_books_menu_success(self, mock_input):
        """Test finding books through menu successfully"""
        test_book = Book("Python Guide", "John Doe", "5555555555")
        self.cli.library.books.append(test_book)
        
        mock_input.side_effect = ["1", "Python"]  # Search by title for "Python"
        
        with patch('builtins.print') as mock_print:
            self.cli.find_books_menu()
            
            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            assert "Found 1 book" in output
    
    @patch('builtins.input')
    def test_find_books_menu_invalid_choice(self, mock_input):
        """Test finding books with invalid search choice"""
        mock_input.return_value = "4"  # Invalid choice
        
        with patch('builtins.print') as mock_print:
            self.cli.find_books_menu()
            
            mock_print.assert_called_with("❌ Invalid choice!")
    
    @patch('builtins.input')
    def test_find_books_menu_empty_query(self, mock_input):
        """Test finding books with empty search term"""
        mock_input.side_effect = ["1", ""]  # Valid choice, empty query
        
        with patch('builtins.print') as mock_print:
            self.cli.find_books_menu()
            
            mock_print.assert_called_with("❌ Search term is required!")
    
    @patch('builtins.input')
    def test_load_books_menu_default_file(self, mock_input):
        """Test loading books with default filename"""
        mock_input.return_value = ""  # Use default
        
        with patch.object(self.cli.library, 'load_books') as mock_load:
            with patch('builtins.print') as mock_print:
                self.cli.load_books_menu()
                
                mock_load.assert_called_with("library.json")
                mock_print.assert_called_with("✅ Attempted to load books from library.json")
    
    @patch('builtins.input')
    def test_load_books_menu_custom_file(self, mock_input):
        """Test loading books with custom filename"""
        mock_input.return_value = "custom.json"
        
        with patch.object(self.cli.library, 'load_books') as mock_load:
            with patch('builtins.print'):
                self.cli.load_books_menu()
                
                mock_load.assert_called_with("custom.json")
    
    @patch('builtins.input')
    def test_save_books_menu_success(self, mock_input):
        """Test saving books successfully"""
        mock_input.return_value = "test.json"
        
        with patch.object(self.cli.library, 'save_books') as mock_save:
            with patch('builtins.print') as mock_print:
                self.cli.save_books_menu()
                
                mock_save.assert_called_with("test.json")
                calls = [str(call) for call in mock_print.call_args_list]
                output = ' '.join(calls)
                assert "Successfully saved" in output
    
    @patch('builtins.input')
    def test_save_books_menu_error(self, mock_input):
        """Test saving books with error"""
        mock_input.return_value = "test.json"
        
        with patch.object(self.cli.library, 'save_books', side_effect=Exception("File error")):
            with patch('builtins.print') as mock_print:
                self.cli.save_books_menu()
                
                calls = [str(call) for call in mock_print.call_args_list]
                output = ' '.join(calls)
                assert "Error saving" in output
    
    def test_handle_choice_add_book(self):
        """Test handle_choice for add book option"""
        with patch.object(self.cli, 'add_book_menu') as mock_add:
            result = self.cli.handle_choice('1')
            
            mock_add.assert_called_once()
            assert result is True
    
    def test_handle_choice_exit(self):
        """Test handle_choice for exit option"""
        with patch('builtins.print') as mock_print:
            result = self.cli.handle_choice('8')
            
            mock_print.assert_called_with("👋 Thank you for using Library Management System!")
            assert result is False
    
    def test_handle_choice_invalid(self):
        """Test handle_choice for invalid option"""
        with patch('builtins.print') as mock_print:
            result = self.cli.handle_choice('99')
            
            mock_print.assert_called_with("❌ Invalid choice! Please enter 1-8.")
            assert result is True