# Library Management System

A simple command-line library management system written in Python.

## Features

- Add, remove, and list books
- Search books by title, author, or ISBN
- ISBN uniqueness validation
- Save/load library data to/from JSON files
- Interactive CLI interface

## Quick Start

```bash
python3 main.py
```

## Project Structure

```
librarian/
├── main.py           # Entry point
├── library_cli.py    # CLI interface
├── library.py        # Library class
├── book.py           # Book class
├── library.json      # Data storage
└── tests/            # Test suite
```

## Running Tests

### Install Dependencies
```bash
pip install pytest pytest-cov
```

### Run Tests
```bash
# All working tests
pytest tests/test_basic.py tests/test_library_cli.py -v

# Specific test file
pytest tests/test_basic.py -v

# With coverage
pytest tests/test_basic.py tests/test_library_cli.py --cov=. --cov-report=html
```

### Test Coverage
- ✅ Book creation and validation
- ✅ Library operations (add, remove, find)
- ✅ ISBN uniqueness enforcement
- ✅ CLI menu operations and user input handling
- ✅ File save/load operations

## Usage Example

```python
from library import Library
from book import Book

# Create books
book1 = Book("Tutunamayanlar", "Oğuz Atay", "9781234567890")
book2 = Book("Martin Eden", "Jack London", "9780987654321")

# Create library
library = Library([book1, book2])

# Find books
results = library.find_book("Oğuz", "author")
```