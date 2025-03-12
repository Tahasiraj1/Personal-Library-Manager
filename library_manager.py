import click
import json
import os

LIBRARY = 'library.json'

# Load books
def load_books():
    if not os.path.exists(LIBRARY):
        return []
    with open(LIBRARY, 'r') as file:
        return json.load(file)
    

#save books
def save_books(books):
    with open(LIBRARY, 'w') as file:
        json.dump(books, file, indent=4)


# LibraryManager class to handle crud operation like adding books ,deleting books, search books, displaying all books, and display statistics. 
class LibraryManager:
    #Add book
    def add_book(self, title, author, year, genre, status):
        """Add book"""
        books = load_books()
        new_book = {
            "title": title,
            "author": author,
            "publication_year": year,
            "genre": genre,
            "read": status
        }
        books.append(new_book)
        save_books(books)  # Save after adding
        click.echo(click.style(f"\nAdded '{title}' to the library!", fg="green", bold=True))


    #Remove book
    def remove_book(self, title):
        """Remove book by title"""
        books = load_books()
        for book in books:
            if book["title"] == title:
                books.remove(book)
                save_books(books)  # Save after removal
                click.echo(click.style(f"\nRemoved '{title}' from the library!", fg="red", bold=True))
                return
        click.echo(click.style(f"\nCannot find '{title}' in the library.", fg='red', bold=True))


    # Display all books
    def display_all_books(self):
        """Display list of all books with status and index"""
        books = load_books()
        if not books:
            click.echo("No books found.")
            return
        for index, book in enumerate(books, 1):
            read_status = "✓" if book["read"] == True else "✗"
            click.echo(f"\n{index}. {book['title']} by {book['author']} ({book['publication_year']}) - {book['genre']} - {read_status}")


    # Search book
    def search_book(self, title=None, author=None):
        """Search books either by title or author"""
        books = load_books()
        search_list = []

        if not title and not author:
            click.acho(f"\nPlease provide either a title or an author to search.")
            return
        
        if title:
            search_list = [book for book in books if book['title'].lower() == title.lower()]

        elif author:
            search_list = [book for book in books if book['author'].lower() == author.lower()]

        if search_list:
            for book in search_list:
                click.echo(f"\n{book['title']} - {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read'] else 'Not Read'}")
        else:
            click.echo(click.style("\nNo books found matching your search.", fg='red', bold=True))


    def display_statistics(self):
        """Display statistics"""
        books = load_books()

        if not books:
            click.echo(click.style("\nNo books available in the library.", fg='red', bold=True))
            return
        
        total_books = len(books)
        read_books = sum(1 for book in books if book.get("read", False))
        percentage_read = (read_books / total_books) * 100

        click.echo(click.style(f"\nTotal books: {total_books}", bg='green'))
        click.echo(click.style(f"Percentage read: {percentage_read:.1f}%", bg='green'))

    


# CLI Menu
def main():
    library = LibraryManager()

    while True:
        click.echo(click.style("\nWelcome to your Personal Library Manager!", fg="cyan", bold=True))
        click.echo(click.style("1.", fg="yellow") + " Add a book 📖")
        click.echo(click.style("2.", fg="yellow") + " Remove a book 🗑️")
        click.echo(click.style("3.", fg="yellow") + " Search for a book 🔎")
        click.echo(click.style("4.", fg="yellow") + " Display all books 📚")
        click.echo(click.style("5.", fg="yellow") + " Display statistics 📊")
        click.echo(click.style("6.", fg="red", bold=True) + " Exit 🚪")


        choice = click.prompt(click.style("Enter your choice", fg="green"), type=int)

        if choice == 1:
            title = click.prompt("Enter book title: ")
            author = click.prompt("Enter author name: ")
            year = click.prompt("Enter publication year: ", type=int)
            genre = click.prompt("Enter your genre: ")
            status = click.prompt("Have you read it? (yes/no) ").strip().lower()
            library.add_book(title, author, year, genre, status)

        elif choice == 2:
            title = click.prompt("Enter book title to remove: ")
            library.remove_book(title)

        elif choice == 3:
            search_type = click.prompt("Search by title or author? ", type=str.lower())
            if search_type == "title":
                title = click.prompt("Enter book title: ")
                library.search_book(title=title)
            elif search_type == "author":
                author = click.prompt("Enter author name: ")
                library.search_book(author=author)
            else:
                click.echo(click.style("Invalid search type.", bg='red'))
        
        elif choice == 4:
            library.display_all_books()

        elif choice == 5:
            library.display_statistics()

        elif choice == 6:
            click.echo(click.style("\nExiting the Library Manager. Goodbye!", bg="green"))
            break

        else:
            click.echo(click.style("\nInvalid choice! Please enter a number between 1 and 6.", bg='red', bold=True))


if __name__ == "__main__":
    main()