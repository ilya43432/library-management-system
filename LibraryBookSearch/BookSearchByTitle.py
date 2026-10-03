from LibraryBookSearch.BookSearch import BookSearch


class BookSearchByTitle(BookSearch):

    def search(self,books, keyword):
        result = []
        for book in books:
            if keyword.lower() in book.title.lower():
                result.append(book)
        return result