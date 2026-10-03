import csv
import unittest
import os

from LibraryManagment.Library import Library
from LibraryManagment.book import Book
from Logger.Logger import Logger
from User.LibraryUser import LibraryUser


class TestLibraryWithLogs(unittest.TestCase):
    def setUp(self):
        print("Setting up the test...")
        self.log_file = os.path.join(os.path.dirname(__file__), "log.txt")
        print(f"Log file will be created at: {self.log_file}")
        logger = Logger()
        base_dir = os.path.dirname(__file__)
        csv_file_path = os.path.join(base_dir, "books.csv")
        self.library = Library(csv_file_path, logger)
        self.library_user = LibraryUser()



    def read_log(self):

        with open(self.log_file, "r") as f:
            return f.read()


    def add_book_and_create_instance(self, title, author, category, year, copies):

        self.library.add_book(title, author, category, year, copies)

        with open(self.library.csv_file, "r") as f:
            reader = csv.DictReader(f)
            last_row = None
            for row in reader:
                last_row = row

        if not last_row:
            raise ValueError("Not find")

        return Book(
            title=last_row['title'],
            author=last_row['author'],
            category=last_row['genre'],
            year=int(last_row['year']),
            total_copies=int(last_row['copies']),
            is_loaned=last_row['is_loaned'],
            copies_status={int(k): bool(int(v)) for k, v in
                           (pair.split(":") for pair in str(last_row['copies_status']).split(","))},
            wait_list=[
                {"name": entry.split(":")[0], "phone": entry.split(":")[1]}
                for entry in str(last_row.get('wait_list', '')).split(";") if ":" in entry
            ]
        )

    def test_register_user_successfully_logs(self):
        self.library_user.register_user("test_user", "test_password")
        log_content = self.read_log()
        self.assertIn("registered successfully", log_content)

    def test_register_user_fail_logs(self):
        self.library_user.register_user("test_user", "test_password")
        self.library_user.register_user("test_user", "test_password")  # Duplicate
        log_content = self.read_log()
        self.assertIn("registered fail", log_content)

    def test_authenticate_user_successfully_logs(self):
        self.library_user.register_user("test_user", "test_password")
        self.library_user.authenticate_user("test_user", "test_password")
        log_content = self.read_log()
        self.assertIn("logged in successfully", log_content)

    def test_authenticate_user_fail_logs(self):
        self.library_user.authenticate_user("wrong_user", "wrong_password")
        log_content = self.read_log()
        self.assertIn("logged in fail", log_content)

    def test_add_book_successfully_logs(self):
        self.library.add_book("Test Book", "Test Author", "Test Category", "2025", "5")
        log_content = self.read_log()
        self.assertIn("Book added successfully", log_content)

    def test_add_book_fail_logs(self):
        self.library.add_book("", "", "", "", "")
        log_content = self.read_log()
        self.assertIn("Book added  fail", log_content)

    def test_add_book_fail_logs(self):
        self.library.add_book("Test Book", "Test Author", "Test Category", "2025", "0")
        log_content = self.read_log()
        self.assertIn("Book added  fail", log_content)

    def test_add_book_fail_logs(self):
        self.library.add_book("Test Book", "Test Author", "Test Category", "e", "1")
        log_content = self.read_log()
        self.assertIn("Book added  fail", log_content)

    def test_remove_book_successfully_logs(self):
        self.library.add_book("Test Book", "Test Author", "Test Category", "2025", "5")
        self.library.remove_book("Test Book", "Test Author")
        log_content = self.read_log()
        self.assertIn("Book removed successfully", log_content)

    def test_remove_book_fail_logs(self):
        self.library.remove_book("Nonexistent Book", "Nonexistent Author")
        log_content = self.read_log()
        self.assertIn("Book removed fail", log_content)

    def test_borrow_book_successfully_logs(self):
        book = self.add_book_and_create_instance("Borrowable Book", "Author", "Category", 2025, 2)
        self.library.borrow_book(book)
        log_content = self.read_log()
        self.assertIn("Book borrowed successfully", log_content)

    def test_borrow_book_fail_logs(self):
        book = self.add_book_and_create_instance("Unborrowable Book", "Author", "Category", 2025, 1)
        self.library.borrow_book(book)
        self.library.borrow_book(book)
        log_content = self.read_log()
        self.assertIn("Book borrowed fail", log_content)

    def test_return_book_fail_logs(self):
        self.library.return_book("Nonexistent Book", "Nonexistent Author")
        log_content = self.read_log()
        self.assertIn("Book returned fail", log_content)

    def test_display_all_books_logs(self):
        self.library.display_all_books()
        log_content = self.read_log()
        if not self.library.books:
            self.assertIn("Displayed all books fail", log_content)
        else:
            self.assertIn("Displayed all books successfully", log_content)

    def test_display_popular_books_logs(self):
        self.library.display_popular_books()
        log_content = self.read_log()
        if not self.library.books:
            self.assertIn("Displayed popular books fail", log_content)
        else:
            self.assertIn("Displayed popular books successfully", log_content)

    def test_search_books_logs(self):

        from LibraryBookSearch.BookSearchByAuthor import BookSearchByAuthor
        self.library.add_book("Searchable Book", "Author", "Category", "2025", "1")
        self.library.search_books(BookSearchByAuthor(), "Author")
        log_content = self.read_log()
        self.assertIn('Search book "Author" by author completed successfully', log_content)

    def test_display_books_by_filter_logs(self):
        self.library.display_books_by_filter("available")
        log_content = self.read_log()
        self.assertIn("Displayed available books successfully", log_content)

    def test_get_categories(self):
        self.library.add_book("Book1", "Author1", "Fiction", "2025", "1")
        self.library.add_book("Book2", "Author2", "Science", "2025", "1")
        categories = self.library.get_categories()
        self.assertEqual(categories, ["Fiction", "Science"])


