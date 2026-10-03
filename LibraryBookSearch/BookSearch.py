# here we are going to implement the strategy method. the main point here is to provide quick and
# efficient way to search
# for the books that we want in the library. the strategy is to search the desired books by 3 main categories:
# 1. search by author.
# 2. search by year.
# 3. search name.
from abc import ABC, abstractmethod

class BookSearch(ABC):
    @abstractmethod
    def search(self, books, query):
        pass