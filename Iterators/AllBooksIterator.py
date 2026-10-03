class AllBooksIterator:
    def __init__(self, books):
        self.books = books
        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.books):
            book = self.books[self.current_index]
            self.current_index += 1
            return book
        raise StopIteration