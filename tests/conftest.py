import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_books():
    """Fixture providing sample books for testing"""
    from book import Book
    return [
        Book("The Python Guide", "John Smith", "9781234567890"),
        Book("Data Science Handbook", "Jane Doe", "9780987654321"),
        Book("Machine Learning Basics", "Bob Johnson", "9781111111111")
    ]

@pytest.fixture
def empty_library():
    """Fixture providing an empty library"""
    from library import Library
    return Library([])

@pytest.fixture
def library_with_books(sample_books):
    """Fixture providing a library with sample books"""
    from library import Library
    return Library(sample_books)

@pytest.fixture
def sample_json_data():
    """Fixture providing sample JSON data for testing file operations"""
    return [
        {
            "title": "Test Book 1",
            "author": "Test Author 1", 
            "isbn": "1111111111"
        },
        {
            "title": "Test Book 2",
            "author": "Test Author 2",
            "isbn": "2222222222"
        }
    ]
