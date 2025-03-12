import json
import os
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://MugheesPython:mughees16@cluster0.2r2rb.mongodb.net/" 
client = MongoClient(MONGO_URI)
print(client)
db = client["LibraryDB"]
collection = db["Books"]

FILE_NAME = "library.txt"

def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

def save_to_mongodb(library):
    collection.delete_many({})
    if library:
        collection.insert_many(library)

def display_menu():
    print("\n--- Personal Library Manager ---")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = True if read_input == "yes" else False

    book = {
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read
    }

    library.append(book)
    print("Book added successfully!")

def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip().lower()
    found = False
    for book in library:
        if book["Title"].lower() == title:
            library.remove(book)
            found = True
            print("Book removed successfully!")
            break
    if not found:
        print("Book not found.")

def search_book(library):
    print("Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice: ")

    query = input("Enter your search text: ").strip().lower()
    results = []

    if choice == "1":
        results = [book for book in library if query in book["Title"].lower()]
    elif choice == "2":
        results = [book for book in library if query in book["Author"].lower()]

    if results:
        print("\nMatching Books:")
        for i, book in enumerate(results, 1):
            print(f"{i}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}")
    else:
        print("No matching books found.")

def display_books(library):
    if not library:
        print("Library is empty.")
        return

    print("\nYour Library:")
    for i, book in enumerate(library, 1):
        print(f"{i}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {'Read' if book['Read'] else 'Unread'}")

def display_statistics(library):
    total = len(library)
    read_count = sum(1 for book in library if book["Read"])
    percent = (read_count / total * 100) if total > 0 else 0
    print(f"\nTotal books: {total}")
    print(f"Percentage read: {percent:.2f}%")

def main():
    library = load_library()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library)
            save_to_mongodb(library)
            print("Library saved to library.txt and MongoDB. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
