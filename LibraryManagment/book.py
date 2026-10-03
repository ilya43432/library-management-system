class Book:
    """
        Represents a book in the library system. This class manages book details,
        availability, borrowing, returning, and waiting lists.
        """
    def __init__(self, title, author, category, year, total_copies=1, is_loaned="No",copies_status=None, wait_list=None):
        """
                Initializes a Book instance.

                :param title: The title of the book.
                :param author: The author of the book.
                :param category: The category or genre of the book.
                :param year: The year the book was published.
                :param total_copies: The total number of copies available (default is 1).
                :param is_loaned: Indicates if the book is currently fully loaned ("Yes" or "No").
                :param copies_status: A dictionary tracking the status of individual copies (borrowed or not).
                :param wait_list: A list of users waiting for this book.
                """
        self.title = title
        self.author = author
        self.category = category
        self.year = year
        self.total_copies = total_copies
        self.copies_status = copies_status or {i: False for i in range(1, total_copies + 1)}
        self.is_loaned = is_loaned
        self._sync_is_loaned()
        self.wait_list = wait_list or []

    def __eq__(self, other):
        """
                Compares this book to another book instance for equality.

                :param other: Another Book instance.
                :return: True if both books have the same title, author, category, and year.
                """
        if not isinstance(other, Book):
            return False
        return (self.title == other.title and
                self.author == other.author and
                self.category == other.category and
                self.year == other.year)
    @property
    def available_copies(self):
        """
                Calculates the number of available (not borrowed) copies.

                :return: The number of available copies.
                """
        return sum(1 for status in self.copies_status.values() if not status)

    @property
    def borrow_count(self):
        """
                Calculates the number of borrowed copies.

                :return: The number of borrowed copies.
                """
        return sum(1 for status in self.copies_status.values() if status)

    def borrow_copy(self):
        """
                Marks one copy of the book as borrowed if available.

                :return: A message indicating the result of the borrowing operation.
                """
        for copy_id, is_borrowed in self.copies_status.items():
            if not is_borrowed:
                self.copies_status[copy_id] = True
                print(f"{self.borrow_count}")
                print(copy_id, self.copies_status[copy_id])
                self._sync_is_loaned()
                return f'Borrowed copy #{copy_id} of "{self.title}".'
        return f'No available copies of "{self.title}".'

    def return_copy(self):
        """
                Marks one copy of the book as returned.

                :return: A message indicating the result of the return operation.
                """
        copy_id = next((cid for cid, status in self.copies_status.items() if status), None)
        if copy_id is None:
            return f'There is no borrowed copy of "{self.title}".'
        else:
            self.copies_status[copy_id] = False
            self._sync_is_loaned()
            return f'Returned copy #{copy_id} of "{self.title}".'


    def add_copies(self, count):
        """
                Adds additional copies of the book to the library.

                :param count: The number of copies to add.
                :return: A message indicating the number of copies added.
                """
        start_id = self.total_copies + 1
        for i in range(start_id, start_id + count):
            self.copies_status[i] = False
        self.total_copies += count
        self._sync_is_loaned()
        return f'Added {count} copies of "{self.title}".'

    def is_wait_list_empty(self) -> bool:
        """
               Checks if the waiting list for this book is empty.

               :return: True if the waiting list is empty, False otherwise.
               """
        if len(self.wait_list) == 0:
            return True
        else:
            return False



    def _sync_is_loaned(self):
        """
                Updates the 'is_loaned' status based on the number of available copies.
                """
        self.is_loaned = "Yes" if self.available_copies == 0 else "No"

    def __str__(self):
        """
                Returns a string representation of the book.

                :return: A formatted string with book details.
                """
        return f'"{self.title}" by {self.author} ({self.category}) ,{self.year} - {self.available_copies}/{self.total_copies} available.'
