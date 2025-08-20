# Librarian - Library Management System

A simple and effective library management system. Features book addition, search, deletion, and advanced book information retrieval through Open Library API integration.

## Features

- **Terminal-based CLI**: Interactive command-line interface
- **FastAPI REST API**: Modern web API server
- **Open Library Integration**: Automatic book information retrieval via ISBN
- **JSON Data Storage**: Local file-based data persistence
- **Comprehensive Test Suite**: Automated tests for all components

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/myaseminsungur/librarian.git
cd librarian
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Stage 1-2: Terminal Application

To start the CLI (Command Line Interface) application:

```bash
python main.py
```

**Available features:**
- Add books 
- Search books (by title, author, ISBN)
- Delete books
- List all books
- Save/load library data

### Stage 3: API Server

To start the FastAPI web server:

```bash
uvicorn api:app --reload
```

The API server will run at `http://localhost:8000`.

**API Documentation:** `http://localhost:8000/docs`

## API Documentation

### Endpoints

#### GET /books
Lists all books in the library.

**Response:**
```json
[
  {
    "title": "Book Title",
    "author": "Author Name", 
    "isbn": "9781234567890"
  }
]
```

#### POST /books
Adds a book to the library by fetching information from Open Library using ISBN.

**Request Body:**
```json
{
  "isbn": "9782848300443"
}
```

**Response:**
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "9782848300443"
}
```

#### DELETE /books/{isbn}
Removes a book with the specified ISBN from the library.

**Response:**
```json
{
  "message": "Book with ISBN 9782848300443 has been removed"
}
```

#### GET /books/search
Searches books in the library.

**Query Parameters:**
- `query`: Search term
- `search_by`: Search type (`title`, `author`, `isbn`) - default: `title`

**Example:** `GET /books/search?query=python&search_by=title`

**Response:**
```json
[
  {
    "title": "Python Programming",
    "author": "John Doe",
    "isbn": "9781234567890"
  }
]
```

#### GET /books/search/online
Searches books in Open Library API.

**Query Parameters:**
- `query`: Search term

**Example:** `GET /books/search/online?query=python`

**Response:**
```json
[
  {
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "isbn": "9781593279288"
  }
]
```

## Test Scenarios

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test Categories

#### API Tests
```bash
python -m pytest tests/test_api.py -v
```

#### Library Core Tests
```bash
python -m pytest tests/test_library.py -v
```

#### CLI Tests
```bash
python -m pytest tests/test_library_cli.py -v
```

#### Book Model Tests
```bash
python -m pytest tests/test_book.py -v
```

### Test Coverage

**Total: 63 Tests**
- **API Tests (14)**: FastAPI endpoints
- **Library Tests (14)**: Library core functionality
- **CLI Tests (20)**: Command-line interface
- **Book Tests (5)**: Book model
- **Basic Tests (10)**: Basic system tests

### Manual Test Examples

#### API Test Examples (using curl)

**Add book:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "9782848300443"}'
```

**List all books:**
```bash
curl "http://localhost:8000/books"
```

**Search books:**
```bash
curl "http://localhost:8000/books/search?query=python&search_by=title"
```

**Online search:**
```bash
curl "http://localhost:8000/books/search/online?query=python"
```

**Delete book:**
```bash
curl -X DELETE "http://localhost:8000/books/9782848300443"
```

## Project Structure

```
librarian/
├── api.py                 # FastAPI application
├── book.py               # Book model class
├── library.py            # Library core class
├── library_cli.py        # CLI interface
├── main.py              # CLI application entry point
├── open_library.py      # Open Library API client
├── library.json         # Data file
├── requirements.txt     # Python dependencies
├── README.md           # Documentation (Turkish)
├── README_EN.md        # Documentation (English)
└── tests/              # Test files
    ├── test_api.py
    ├── test_library.py
    ├── test_library_cli.py
    ├── test_book.py
    └── test_basic.py
```

## Technologies

- **Python 3.7+**
- **FastAPI**: Modern web API framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pytest**: Test framework
- **HTTPX**: HTTP client (testing)
- **Open Library API**: Book information service

## Development Stages

- ✅ **Stage 1**: Basic CLI application
- ✅ **Stage 2**: Open Library API integration
- ✅ **Stage 3**: FastAPI REST API

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
