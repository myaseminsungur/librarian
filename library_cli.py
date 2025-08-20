from library import Library
from book import Book

class LibraryCLI:
    def __init__(self):
        self.library = Library()
        
    def display_menu(self):
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("Enter the number of the action you want to perform:")
        print("1. Add a new book")
        print("2. Remove a book (by ISBN)")
        print("3. List all books")
        print("4. Find books")
        print("5. Load books from file")
        print("6. Save books to file")
        print("7. Search books online")
        print("8. Exit")
        print("=" * 35)

    def add_book_menu(self):
        print("\n--- Add New Book ---")
        # title = input("Enter book title: ").strip()
        # author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()

        # if not title or not author or not isbn:
        #     print("❌ All fields are required!")
        #     return
        if not isbn:
            print("❌ ISBN is required!")
            return
        
        try:
            self.library.add_book(isbn)
            print(f"✅ Successfully added {isbn}")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def search_books_menu(self):
        print("\n--- Search Books Online ---")
        query = input("Enter search term: ").strip()
        if not query:
            print("❌ Search term is required!")
            return
        self.library.search_books_online(query)
        
    def remove_book_menu(self):
        print("\n--- Remove Book ---")
        isbn = input("Enter ISBN of book to remove: ").strip()
        
        if not isbn:
            print("❌ ISBN is required!")
            return
        
        self.library.remove_book(isbn)

    def list_books_menu(self):
        print("\n📚 All Books in Library:")
        if self.library.books:
            self.library.list_books()
        else:
            print("📭 No books in library!")

    def find_books_menu(self):
        print("\n--- Find Books ---")
        print("Search by:")
        print("1. Title")
        print("2. Author") 
        print("3. ISBN")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice not in ['1', '2', '3']:
            print("❌ Invalid choice!")
            return
        
        query = input("Enter search term: ").strip()
        if not query:
            print("❌ Search term is required!")
            return
        
        search_by_map = {'1': 'title', '2': 'author', '3': 'isbn'}
        search_by = search_by_map[choice]
        
        results = self.library.find_book(query, search_by)
        
        if results:
            print(f"\n📚 Found {len(results)} book(s):")
            for book in results:
                print(f"  • {book}")
        else:
            print("❌ No books found!")

    def load_books_menu(self):
        print("\n--- Load Books from File ---")
        file_path = input("Enter file path (default: library.json): ").strip()
        
        if not file_path:
            file_path = "library.json"
        
        self.library.load_books(file_path)
        print(f"✅ Attempted to load books from {file_path}")

    def save_books_menu(self):
        print("\n--- Save Books to File ---")
        file_path = input("Enter file path (default: library.json): ").strip()
        
        if not file_path:
            file_path = "library.json"
        
        try:
            self.library.save_books(file_path)
            print(f"✅ Successfully saved {len(self.library.books)} books to {file_path}")
        except Exception as e:
            print(f"❌ Error saving: {e}")

    def handle_choice(self, choice):
        """Handle user menu choice and return True to continue, False to exit"""
        if choice == '1':
            self.add_book_menu()
        elif choice == '2':
            self.remove_book_menu()
        elif choice == '3':
            self.list_books_menu()
        elif choice == '4':
            self.find_books_menu()
        elif choice == '5':
            self.load_books_menu()
        elif choice == '6':
            self.save_books_menu()
        elif choice == '7':
            self.search_books_menu()
        elif choice == '8':
            print("👋 Thank you for using Library Management System!")
            return False
        else:
            print("❌ Invalid choice! Please enter 1-8.")
        
        return True
