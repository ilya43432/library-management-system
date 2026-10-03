from LibraryBookSearch.BookSearch import BookSearch


class BookSearchByYear(BookSearch):

    def search(self,books, keyword):
        result = []
        for book in books:
            if keyword in str(book.year):
                result.append(book)
        return result
