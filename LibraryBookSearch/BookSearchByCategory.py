from LibraryBookSearch.BookSearch import BookSearch


class BookSearchByCategory(BookSearch):

    def search(self,books, keyword):
        result = []
        for book in books:
            if keyword.lower() in book.category.lower():
                result.append(book)
        return result