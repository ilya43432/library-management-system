import pandas as pd

from Iterators.AvailableBooksIterator import AvailableBooksIterator
from Iterators.BorrowedBooksIterator import BorrowedBooksIterator
from Iterators.CategoryBooksIterator import CategoryBooksIterator
from LibraryBookSearch.BookSearch import BookSearch
from Notifications.Publisher import Publisher
from .book import Book
from Iterators.AllBooksIterator import AllBooksIterator
from Logger.Logger import Logger


class Library:
    POPULAR_BOOKS_LIMIT = 10
    '''
    The Library class manages books, users, and library operations such as adding, removing, borrowing, and returning books.
        It also supports features like notifications, searching, and filtering.
    '''
    def __init__(self, csv_file, logger):
        '''
        Initializes the Library object.

        :param csv_file: Path to the CSV file containing book data.
        :param logger: Logger instance for recording events.
        '''
        self.csv_file = csv_file
        self.logger = Logger()
        self.books = self._load_books()
        self.notification_manager = Publisher()

    def _load_books(self):
        """
                Loads books from the CSV file into the system.

                :return: A list of Book objects loaded from the CSV file.
                """

        try:
            df = pd.read_csv(self.csv_file)
            return [
                Book(
                    title=row['title'],
                    author=row['author'],
                    category=row['genre'],
                    year=int(row['year']),
                    total_copies=int(row['copies']),
                    is_loaned=row['is_loaned'],
                    copies_status={int(i): False for i in
                                   range(1, int(row['copies']) + 1)} if 'copies_status' not in row
                    else {int(k): bool(int(v)) for k, v in
                          (pair.split(":") for pair in str(row['copies_status']).split(","))},

                    wait_list=[
                        {"name": entry.split(":")[0], "phone": entry.split(":")[1]}
                        for entry in str(row.get('wait_list', '')).split(";")
                        if ":" in entry and len(entry.split(":")) == 2
                    ]
                )
                for _, row in df.iterrows()
            ]
        except FileNotFoundError:
            return []

    def _save_books(self):
        """
               Saves the current state of books to the CSV file.
               """

        df = pd.DataFrame([
            {
                'title': book.title,
                'author': book.author,
                'genre': book.category,
                'year': book.year,
                'copies': book.total_copies,
                'is_loaned': book.is_loaned,
                'copies_status': ",".join(f"{cid}:{'1' if status else '0'}" for cid, status in book.copies_status.items()),
                'wait_list': ";".join(f"{entry['name']}:{entry['phone']}" for entry in book.wait_list)
        }
            for book in self.books
        ])

        df.to_csv(self.csv_file, index=False)


    def auto_save(func):
        """
               Decorator to automatically save the state of books after a method call.
               """
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._save_books()
            return result

        return wrapper

    @auto_save
    def add_book(self, title, author, category, year, copies):
            """
               Adds a new book to the library.

               :param title: Title of the book.
               :param author: Author of the book.
               :param category: Category or genre of the book.
               :param year: Year of publication.
               :param copies: Number of copies to add.
               :return: True if successful, False otherwise.
               """
            try:

                if not all([title, author, category, year, copies]):
                    self.logger.log_warning("Book added  fail")
                    return ""


                try:
                    year = int(year)
                    copies = int(copies)
                    if copies <= 0:
                        self.logger.log_warning("Book added  fail")
                        return False
                except ValueError as e:
                    self.logger.log_warning("Book added  fail")
                    return False

                for book in self.all_books_iterator():
                    if book.title == title and book.author == author:
                        book.add_copies(copies)
                        self.logger.log_info("Book added successfully")
                        return True

                new_book = Book(title, author, category, year, copies)
                self.books.append(new_book)
                self.logger.log_info("Book added successfully")
                return True
            except  Exception as e:
              self.logger.log_info("Book added fail")
              return False

    @auto_save
    def remove_book(self, title, author):
        """
                Removes a book from the library if it is not borrowed.

                :param title: Title of the book to remove.
                :param author: Author of the book to remove.
                :return: True if successful, False otherwise.
                """
        for book in self.all_books_iterator():
            if book.title == title and book.author == author:
                if book.borrow_count == 0:
                  self.books.remove(book)
                  self.logger.log_info("Book removed successfully")
                  return True

        self.logger.log_warning("Book removed fail")
        return False

    @auto_save
    def borrow_book(self, book):
        """
                Borrows a book from the library if available.

                :param book: Book object to borrow.
                :return: Message indicating success or failure.
                """
        if book.available_copies > 0:
            book.borrow_copy()
            self.logger.log_info("Book borrowed successfully")
            return "Book borrowed successfully"
        else:
            self.logger.log_info("Book borrowed fail")
            return "Book borrowed fail"
    @auto_save
    def add_to_waitlist(self,book, name, phone):
         """
                Adds a user to the waitlist for a book.

                :param book: Book object to join the waitlist for.
                :param name: Name of the user.
                :param phone: Phone number of the user.
                :return: Confirmation message.
                """
         book.wait_list.append({"name": name, "phone": phone})
         return "Added to waiting list"


    @auto_save
    def return_book(self, title, author ):
        """
                Returns a borrowed book to the library.

                :param title: Title of the book to return.
                :param author: Author of the book to return.
                :return: Message indicating the result of the return.
                """
        for book in self.all_books_iterator():
            if book.title == title and book.author == author:
                if book.borrow_count > 0:
                  book.return_copy()
                  if book.wait_list:
                    row = book.wait_list.pop(0)
                    name, phone = row['name'], row['phone']
                    self.borrow_book(title,author,name,phone)
                    self.notification_manager.notify_observers(
                        f"Book '{title}' by {author} has been returned and then borrowed for {name} from the waitlist.")
                    return "Borrowed from waiting list"
                  self.logger.log_info("Book returned successfully")
                  return True

        self.logger.log_warning("Book returned fail")
        return False

    def search_books(self, strategy: BookSearch, query: str):
        """
                Searches for books based on a given strategy.

                :param strategy: Search strategy to use (e.g., by title, author).
                :param query: Search query.
                :return: List of books matching the query.
                """
        result = strategy.search(self.books, query)
        extarct_name = strategy.__class__.__name__.replace("BookSearchBy", "").lower()

        if not result:
            self.logger.log_info(f'Search book "{query}" by {extarct_name} completed fail')
            return []
        else:
            self.logger.log_info(f'Search book "{query}" by {extarct_name} completed successfully')
            return result
    def display_all_books(self):
        """
                Displays all books in the library.

                :return: A formatted string of all books.
                """
        if not self.books:
            self.logger.log_warning("Displayed all books fail")
            return "No books in the library."

        self.logger.log_info("Displayed all books successfully")
        return "\n".join(str(book) for book in self.books)


    def get_popular_books(self):
        """
                Retrieves the most popular books based on borrow count and waitlist size.

                :return: A list of popular books.
                """
        popular_books = sorted(
            self.books,
            key=lambda book: book.borrow_count + len(book.wait_list),
            reverse=True
        )[:self.POPULAR_BOOKS_LIMIT]
        return popular_books

    def display_popular_books(self):
        """
                Displays the most popular books in the library.

                :return: A formatted string of popular books.
                """
        popular_books = self.get_popular_books()
        if not popular_books:
            self.logger.log_warning("Displayed popular books fail.")
            return "No popular books available."

        self.logger.log_info("Displayed popular books successfully.")
        return "\n".join(str(book) for book in popular_books)


    def all_books_iterator(self):
        """
                Creates an iterator for all books in the library.

                :return: AllBooksIterator object.
                """
        return AllBooksIterator(self.books)

    def display_books_by_filter(self, filter_type, value=None):
        """
                Displays books based on a filter.

                :param filter_type: Type of filter (e.g., "available", "borrowed", "category").
                :param value: Value for the filter (e.g., category name).
                :return: A formatted string of filtered books.
                """

        if filter_type == "available":
            iterator = AvailableBooksIterator(self.books)
        elif filter_type == "borrowed":
            iterator = BorrowedBooksIterator(self.books)
        elif filter_type == "category" and value:
            iterator = CategoryBooksIterator(self.books, value)
        else:
            return "\n".join(str(book) for book in self.books)

        filtered_books = list(iterator)
        if not filtered_books:
            self.logger.log_info(f"Displayed {filter_type} books fail")
            return "No books match the criteria."
        self.logger.log_info(f"Displayed {filter_type} books successfully")
        return "\n".join(str(book) for book in filtered_books)

    def get_categories(self):
        """
                Retrieves a list of all unique categories in the library.

                :return: Sorted list of categories.
                """
        categories = {book.category for book in self.books if book.category}
        return sorted(categories)


    def add_user_as_observer(self, user):
        """
                Adds a user as an observer to receive notifications.

                :param user: User to add as an observer.
                """
        self.notification_manager.add_observer(user)


    def remove_user_as_observer(self, user):
        """
                Removes a user as an observer.

                :param user: User to remove as an observer.
                """
        self.notification_manager.remove_observer(user)
