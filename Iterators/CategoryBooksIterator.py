class CategoryBooksIterator:
    def __init__(self, books, category):
        self.books = [book for book in books if book.category == category]
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.books):
            book = self.books[self.current_index]
            self.current_index += 1
            return book
        raise StopIteration