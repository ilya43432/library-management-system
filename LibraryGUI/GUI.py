import tkinter as tk
from tkinter import messagebox, simpledialog

from LibraryBookSearch.BookSearchByAuthor import BookSearchByAuthor
from LibraryBookSearch.BookSearchByCategory import BookSearchByCategory
from LibraryBookSearch.BookSearchByTitle import BookSearchByTitle
from LibraryBookSearch.BookSearchByYear import BookSearchByYear
from LibraryManagment.Library import Library
from Logger.Logger import Logger
from User.LibraryUser import LibraryUser

class GUI:



    def __init__(self,csv_file):
        """
        Initializes the GUI with the provided CSV file.

        :param csv_file: Path to the books.csv file.
        """
        logger = Logger()
        self.library = Library(csv_file, logger)
        self.root = tk.Tk()
        self.root.title("User Authentication")
        self.root.geometry("300x200")
        self.user_manager = LibraryUser()
        self.setup_auth_screen()


    def setup_auth_screen(self):
        """
                Sets up the authentication screen with options for login, registration, and exit.
                """

        tk.Label(self.root, text="Library System Login", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login_user, width=20).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_user, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=10)



    def login_user(self):
        """
                Opens the login window where users can enter their credentials to log in.
                Authenticates the user and opens the main window upon success.
                """


        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x300")

        tk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(login_window, width=30)
        username_entry.pack(pady=5)

        tk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(login_window, width=30, show="*")
        password_entry.pack(pady=5)

        def submit_login():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Both username and password are required!")
            else:
                if self.user_manager.authenticate_user(username, password):
                    self.user_manager.logged_in_user = username
                    self.library.add_user_as_observer(self.user_manager)
                    login_window.destroy()
                    self.root.withdraw()
                    self.open_main_window()
                else:
                    messagebox.showerror("Error", "Invalid username or password!")


        tk.Button(login_window, text="Login", command=submit_login).pack(pady=10)


        tk.Button(login_window, text="Cancel", command=login_window.destroy).pack(pady=5)


    def register_user(self):
        """
                Opens the registration window for users to create an account.
                Ensures validation of input fields and password confirmation.
                """

        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("300x250")

        tk.Label(register_window, text="New Username:").pack(pady=5)
        username_entry = tk.Entry(register_window, width=30)
        username_entry.pack(pady=5)

        tk.Label(register_window, text="New Password:").pack(pady=5)
        password_entry = tk.Entry(register_window, width=30, show="*")
        password_entry.pack(pady=5)

        tk.Label(register_window, text="Confirm Password:").pack(pady=5)
        confirm_password_entry = tk.Entry(register_window, width=30, show="*")
        confirm_password_entry.pack(pady=5)

        def submit_registration():
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not username or not password or not confirm_password:
                messagebox.showerror("Error", "All fields are required!")
            elif password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
            else:
                if self.user_manager.register_user(username, password):
                    messagebox.showinfo("Success", "Registration successful! You can now log in.")
                    register_window.destroy()
                else:
                    messagebox.showerror("Error", "Username already exists!")

        tk.Button(register_window, text="Register", command=submit_registration).pack(pady=10)

        tk.Button(register_window, text="Cancel", command=register_window.destroy).pack(pady=5)

    def logout_user(self,main_window):
        """
                Logs out the currently logged-in user and redirects to the authentication screen.

                :param main_window: The main library management window to be closed.
                """
        if self.user_manager.logged_in_user:
            self.user_manager.logout()
            main_window.destroy()
            self.root.deiconify()
            messagebox.showinfo("Success", "You have been logged out.")
        else:
            messagebox.showerror("Error", "No user is currently logged in.")

    def open_main_window(self):
        """
                Opens the main window with options for managing books and viewing library features.
                """

        main_window = tk.Toplevel(self.root)
        main_window.title("Library Management System")
        main_window.geometry("400x400")

        tk.Button(main_window, text="Add Book",command=self.add_book, width=20).pack(pady=10)
        tk.Button(main_window, text="Remove Book"'',command=self.remove_book, width=20).pack(pady=10)
        tk.Button(main_window, text="View Books",command=self.view_books, width=20).pack(pady=10)
        tk.Button(main_window, text="Lend Book",command=self.lend_book, width=20).pack(pady=10)
        tk.Button(main_window, text="Return Book",command=self.return_book, width=20).pack(pady=10)
        tk.Button(main_window, text="Popular Books",command=self.popular_books, width=20).pack(pady=10)
        tk.Button(main_window, text="Search Book",command=self.search_books ,width=20).pack(pady=10)
        tk.Button(main_window, text="Logout", command=lambda: self.logout_user(main_window), width=20).pack(pady=10)

        main_window.protocol("WM_DELETE_WINDOW", self.root.quit)


    def add_book(self):
        """
              Opens a form for adding a new book to the library. Validates user input.
              """
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")
        add_window.geometry("400x500")

        tk.Label(add_window, text="Enter the title:").pack(pady=5)
        title_entry = tk.Entry(add_window, width=30)
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Enter the author:").pack(pady=5)
        author_entry = tk.Entry(add_window, width=30)
        author_entry.pack(pady=5)

        tk.Label(add_window, text="Enter the genre/category:").pack(pady=5)
        category_entry = tk.Entry(add_window, width=30)
        category_entry.pack(pady=5)

        tk.Label(add_window, text="Enter the year of publication:").pack(pady=5)
        year_entry = tk.Entry(add_window, width=30)
        year_entry.pack(pady=5)

        tk.Label(add_window, text="Enter the number of copies:").pack(pady=5)
        copies_entry = tk.Entry(add_window, width=30)
        copies_entry.pack(pady=5)

        def submit_book():
            title = title_entry.get()
            author = author_entry.get()
            category = category_entry.get()
            year = (year_entry.get())
            copies = (copies_entry.get())



            result = self.library.add_book(title, author, category, year, copies)

            if result:
                messagebox.showinfo("Success", f"Book '{title}' by {author} added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add book. Check logs for more details.")

        tk.Button(add_window, text="Add Book", command=submit_book, width=20).pack(pady=20)

        tk.Button(add_window, text="Cancel", command=add_window.destroy, width=20).pack(pady=10)

    def remove_book(self):
        """
                Removes a book from the library. Prompts the user to enter the book's title and author.
                """
        title = simpledialog.askstring("Remove Book", "Enter the title:")
        author = simpledialog.askstring("Remove Book", "Enter the author:")

        if not all([title, author]):
            messagebox.showerror("Error", "Both title and author are required!")
            return

        result = self.library.remove_book(title, author)
        if result:
            messagebox.showinfo("Success", "Book removed successfully")
        else:
            messagebox.showerror("Error", "Book removed fail")




    def lend_book(self):
        """
                Manages the lending of books. Allows users to search for books and borrow them.
                Offers the option to join a waiting list if no copies are available.
                """

        lend_window = tk.Toplevel(self.root)
        lend_window.title("Lend Book")
        lend_window.geometry("600x400")

        search_frame = tk.Frame(lend_window)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter the title :").pack(side=tk.LEFT,pady=5)
        title_entry = tk.Entry(search_frame, width=40)
        title_entry.pack(side=tk.LEFT,pady=5)

        tk.Label(lend_window, text="Search Results:").pack(pady=5)
        result_listbox = tk.Listbox(lend_window, height=10, width=70, selectmode=tk.SINGLE)
        result_listbox.pack(pady=5)

        search_results = []
        selected_book = None

        def search_books():

            nonlocal search_results, selected_book
            selected_book = None

            title = title_entry.get()

            strategy = BookSearchByTitle()
            search_results = self.library.search_books(strategy, title)

            result_listbox.delete(0, tk.END)
            if search_results:
                for book in search_results:
                    result_listbox.insert(tk.END, str(book))
            else:
                result_listbox.insert(tk.END, "No books found.")

        def select_book(event):
            nonlocal selected_book
            selection = result_listbox.curselection()
            if selection:
                selected_index = selection[0]
                selected_book = search_results[selected_index]

        def lend_selected_book():

            if not selected_book:
                messagebox.showerror("Error", "No book selected!")
                return
            result = self.library.borrow_book(selected_book)
            if result == "Book borrowed successfully":
                messagebox.showinfo("Success", "Book borrowed successfully")
                lend_window.destroy()
            elif result == "Book borrowed fail":
                response = messagebox.askquestion(
                    "No Copies Available",
                    "No copies are currently available. Would you like to join the waiting list?"
                )

                if response == "yes":
                    name = simpledialog.askstring("Join Waiting List", "Enter your name:")
                    while True:
                         phone = simpledialog.askstring("Join Waiting List", "Enter your phone:")
                         try:
                             phone = int(phone)
                         except ValueError:
                             messagebox.showerror("Error", "Phone must be a valid integer!")
                             continue
                         break

                    if not all([name, phone]):
                        messagebox.showerror("Error", "Name and phone are required to join the waiting list!")
                        return


                    result = self.library.add_to_waitlist(selected_book, name, phone)
                    if result == "Added to waiting list":
                        messagebox.showinfo("Success", f"{name} has been added to the waiting list.")
                    else:
                        messagebox.showerror("Error", "Failed to join the waiting list.")
                else:
                    return

        result_listbox.bind("<<ListboxSelect>>", select_book)

        tk.Button(search_frame, text="Search", command=search_books, width=15).pack(side=tk.LEFT,pady=5)
        tk.Button(lend_window, text="Lend Book", command=lend_selected_book, width=15).pack(pady=5)
        tk.Button(lend_window, text="Cancel", command=lend_window.destroy, width=15).pack(pady=10)

    def return_book(self):
        """
                Handles the return of borrowed books. Updates the waiting list if applicable.
                """
        title = simpledialog.askstring("Return Book", "Enter the title:")
        author = simpledialog.askstring("Return Book", "Enter the author:")

        if not all([title, author]):
            messagebox.showerror("Error", "Both title and author are required!")
            return

        result = self.library.return_book(title, author)
        if result:
            messagebox.showinfo("Success", "Book returned successfully")
        elif result == "Borrowed from waiting list":
            messagebox.showinfo("Success", "Book returned successfully and borrowed from waiting list")
        else:
            messagebox.showerror("Error", "Book returned fail")

    def view_books(self):
        """
                Displays all books in the library with filtering options for available, borrowed, or category-based views.
                """
        view_window = tk.Toplevel(self.root)
        view_window.title("View Books")
        view_window.geometry("700x600")

        text_area = tk.Text(view_window, wrap=tk.WORD, height=30, width=80)
        text_area.pack(padx=10, pady=10)

        def update_text_area(content):

            text_area.config(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", content)
            text_area.config(state=tk.DISABLED)

        def show_all_books():
            books = self.library.display_all_books()
            update_text_area(books)

        def show_available_books():
            books = self.library.display_books_by_filter("available")
            update_text_area(books)

        def show_borrowed_books():
            books = self.library.display_books_by_filter("borrowed")
            update_text_area(books)

        def filter_by_category(category):
            if not category:
                update_text_area("No category selected.")
            else:
                books = self.library.display_books_by_filter("category", category)
                update_text_area(books)


        filter_frame = tk.Frame(view_window)
        filter_frame.pack(pady=10)

        tk.Button(filter_frame, text="View All Books", command=show_all_books, width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(filter_frame, text="Available Books", command=show_available_books, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(filter_frame, text="Borrowed Books", command=show_borrowed_books, width=15).grid(row=2, column=0, padx=5, pady=5)

        categories = self.library.get_categories()
        if categories:
            selected_category = tk.StringVar(view_window)
            selected_category.set("Select a Category")  # Placeholder
            category_menu = tk.OptionMenu(filter_frame, selected_category, *categories, command=filter_by_category)
            category_menu.grid(row=3, column=0, padx=5, pady=5)
        else:
            tk.Label(filter_frame, text="No categories available", font=("Arial", 12)).pack(side=tk.TOP, pady=5)






    def search_books(self):
        """
                Opens a window for searching books by title, author, category, or year.
                Displays search results in a new window.
                """
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Books")
        search_window.geometry("300x300")

        def handle_search(strategy):
            query = simpledialog.askstring(
                "Search Books",
                f"Enter your search query by {strategy.__class__.__name__.replace('BookSearchBy', '').lower()}:"
            )
            if not query:
                messagebox.showerror("Error", "Search query is required!")
                return

            results = self.library.search_books(strategy, query)
            if not results:
                messagebox.showinfo("No Results", "No books found.")
            else:
                result_window = tk.Toplevel(self.root)
                result_window.title("Search Results")
                text_area = tk.Text(result_window, wrap=tk.WORD, height=20, width=60)
                text_area.insert("1.0", "\n".join(str(book) for book in results))
                text_area.config(state=tk.DISABLED)
                text_area.pack(padx=10, pady=10)




        tk.Button(search_window, text="By Title", command=lambda: handle_search(BookSearchByTitle()), width=20).pack(
            pady=10)
        tk.Button(search_window, text="By Author", command=lambda: handle_search(BookSearchByAuthor()), width=20).pack(
            pady=10)
        tk.Button(search_window, text="By Category", command=lambda: handle_search(BookSearchByCategory()),
                  width=20).pack(pady=10)
        tk.Button(search_window, text="By Year", command=lambda: handle_search(BookSearchByYear()), width=20).pack(
            pady=10)


    def popular_books(self):
        """
                Displays a list of the most popular books in the library.
                """
        books = self.library.display_popular_books()

        if books == "No popular books available.":
            messagebox.showerror("Error", books)
        else:
            result_window = tk.Toplevel(self.root)
            result_window.title("Popular Books")

            text_area = tk.Text(result_window, wrap=tk.WORD, height=40, width=100)
            text_area.insert("1.0", books)
            text_area.config(state=tk.DISABLED)
            text_area.pack(padx=10, pady=10)

    def run(self):
        """
                Starts the Tkinter main event loop to run the application.
                """
        self.root.mainloop()


