from library_cli import LibraryCLI

def main():
    cli = LibraryCLI()
    
    print("🎉 Welcome to the Library Management System!")
    
    while True:
        cli.display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if not cli.handle_choice(choice):
            break
            
        input("\nPress Enter for main menu...")

if __name__ == "__main__":
    main()