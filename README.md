# Library Management System

A desktop library management system built in Python, developed as an Object-Oriented
Programming course assignment. The project models a real library workflow — user
registration, book search, borrowing/returning, and waiting-list notifications — and is
built around four classic design patterns rather than ad-hoc logic.

## Features

- **User management** — registration and login/logout authentication.
- **Book management** — add, remove (only if not currently borrowed), lend, and return
  books; removal and lending are blocked when business rules are violated.
- **Flexible search** — search the catalog by title, author, or category, including
  partial-word matches on title.
- **Waiting-list notifications** — users are notified automatically when a book they
  were waiting for becomes available again.
- **Persistent storage** — book and user data is kept in `books.csv` / `users.csv` so
  state survives between runs.
- **Action logging** — every meaningful action (add, borrow, return, remove, register)
  is written to `log.txt` for traceability.
- **Desktop GUI** — a Tkinter-based interface exposes all functionality through buttons
  instead of a command-line menu.

## Design Patterns

| Pattern | Where | Why |
|---|---|---|
| **Observer** | `Notifications/` | Notifies users on the waiting list the moment a book becomes available again. |
| **Iterator** | `Iterators/` | Custom iterators traverse different book subsets (all books, available, borrowed, by category) without exposing the underlying collection. |
| **Strategy** | `LibraryBookSearch/` | Each search mode (by title, author, category, year) is a swappable strategy implementing a common search interface. |
| **Decorator** | `LibraryManagment/Library.py` | An `auto_save` decorator wraps state-changing methods (add/borrow/return/remove) so every mutation is persisted to `books.csv` automatically, with no repeated save calls. |

## Project Structure

```
Library/
├── Main.py                   # Entry point
├── User/                     # User model + authentication
├── LibraryManagment/         # Core Library/Book classes (Decorator-based persistence)
├── LibraryBookSearch/        # Search strategies (Strategy pattern)
├── Iterators/                # Book collection iterators (Iterator pattern)
├── Notifications/            # Observer/Publisher for availability alerts
├── LibraryGUI/                # Tkinter GUI
├── Logger/                   # Action logging to log.txt
├── LibraryTest/               # Unit tests
├── books.csv / users.csv     # Persisted data
```

## Running

```bash
python Main.py
```

Register a user first (**Register**), then log in (**Login**) to access lending,
returning, and search features through the GUI.

## Tech Stack

Python · Tkinter (GUI) · CSV-based persistence · `unittest`
