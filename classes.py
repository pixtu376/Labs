import sqlite3

class Entity:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def update(self, name):
        self.name = name


class Book(Entity):
    total_books = 0

    def __init__(self, title, author, genre, price):
        super().__init__(title)
        self.author = author
        self.genre = genre
        self.price = price
        Book.total_books += 1

    def __str__(self):
        return f"Название: {self.name}, Автор: {self.author.name}, Жанр: {self.genre.name}, Цена: {self.price}Р"

    def update(self, title=None, author=None, genre=None, price=None):
        if title:
            self.name = title
        if author:
            self.author = author
        if genre:
            self.genre = genre
        if price:
            self.price = price

    @staticmethod
    def get_total_books():
        return Book.total_books


class Genre(Entity):
    def __init__(self, name):
        super().__init__(name)


class Author(Entity):
    def __init__(self, name):
        super().__init__(name)

    def update(self, name):
        self.name = name


class Customer(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.books = []

    def buy_book(self, book):
        self.books.append(book)


class Store(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.library = []

    def __add__(self, book):
        return self.add_book(book)

    def add_book(self, book):
        self.library.append(book)
        print(f"Книга '{book.name}' добавлена в библиотеку магазина '{self.name}'.")

    def add_book_with_conn(self, conn, book):
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE title = ?", (book.name,))
        existing_book = c.fetchone()
        
        if any(b.name == book.name for b in self.library):
            print("Книга с таким названием уже существует в библиотеке.")
            return
        
        print(f"Проверка существования книги '{book.name}' в базе данных...")
        if existing_book is None:
            c.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                      (book.name, book.author.name, book.genre.name, book.price))
            conn.commit()
            self.add_book(book)
            print(f"Книга '{book.name}' добавлена в базу данных магазина '{self.name}'.")
        else:
            self.add_book(book)
            print("Книга с таким названием уже существует в базе данных, но добавлена в библиотеку.")

    def remove_book(self, conn, book_title):
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE title = ?", (book_title,))
        self.library = [b for b in self.library if b.name != book_title]
        conn.commit()
        print(f"Книга '{book_title}' удалена из магазина.")

    def show_library(self):
        print(f"Библиотека магазина '{self.name}':")
        for book in self.library:
            print(book)
