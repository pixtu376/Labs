import sqlite3
from classes import Book, Author, Genre, Customer, Store

def create_tables(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS books (
                title text PRIMARY KEY,
                author text,
                genre text,
                price real
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS authors (
                name text PRIMARY KEY
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS genres (
                name text PRIMARY KEY
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
                name text PRIMARY KEY
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS stores (
                name text PRIMARY KEY
                )""")
    conn.commit()

def add_book(conn, authors, genres):
    try:
        title = input("Введите название книги: ")
        author_name = input("Введите имя автора: ")
        author = authors.get(author_name)
        if not author:
            print("Автор с таким именем не найден.")
            return
        genre_name = input("Введите название жанра: ")
        genre = genres.get(genre_name)
        if not genre:
            print("Жанр с таким именем не найден.")
            return
        price = float(input("Введите цену книги: "))
        book = Book(title, author, genre, price)
        c = conn.cursor()
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                  (book.name, book.author.name, book.genre.name, book.price))
        conn.commit()
        print(f"Книга '{title}' добавлена.")
    except Exception as e:
        print(f"Ошибка: {e}")

def edit_book(conn, books, authors, genres):
    try:
        title = input("Введите название книги для редактирования: ")
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE title = ?", (title,))
        book_data = c.fetchone()
        if not book_data:
            print("Книга не найдена.")
            return
        new_title = input("Введите новое название книги (оставьте пустым для пропуска): ")
        new_author_name = input("Введите нового автора (оставьте пустым для пропуска): ")
        new_genre_name = input("Введите новый жанр (оставьте пустым для пропуска): ")
        new_price = input("Введите новую цену (оставьте пустым для пропуска): ")

        if new_title:
            title = new_title
        if new_author_name:
            author = authors.get(new_author_name)
            if author:
                book_data[1] = author.name
            else:
                print("Автор не найден.")
        if new_genre_name:
            genre = genres.get(new_genre_name)
            if genre:
                book_data[2] = genre.name
            else:
                print("Жанр не найден.")
        if new_price:
            book_data[3] = float(new_price)

        c.execute("UPDATE books SET title = ?, author = ?, genre = ?, price = ? WHERE title = ?",
                  (book_data[0], book_data[1], book_data[2], book_data[3], title))
        conn.commit()
        print("Книга успешно отредактирована.")
    except Exception as e:
        print(f"Ошибка: {e}")

def delete_book(conn, title):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE title = ?", (title,))
        conn.commit()
        print(f"Книга '{title}' удалена.")
    except Exception as e:
        print(f"Ошибка: {e}")

def add_author(conn, name):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Автор '{name}' добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def edit_author(conn, old_name, new_name):
    try:
        c = conn.cursor()
        c.execute("UPDATE authors SET name = ? WHERE name = ?", (new_name, old_name))
        conn.commit()
        print(f"Автор '{old_name}' изменен на '{new_name}'.")
    except Exception as e:
        print(f"Ошибка: {e}")

def delete_author(conn, name):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM authors WHERE name = ?", (name,))
        conn.commit()
        print(f"Автор '{name}' удален.")
    except Exception as e:
        print(f"Ошибка: {e}")

def buy_book(conn, customer_name, book_title):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM customers WHERE name = ?", (customer_name,))
        customer = c.fetchone()
        if not customer:
            print("Покупатель не найден.")
            return
        c.execute("SELECT * FROM books WHERE title = ?", (book_title,))
        book = c.fetchone()
        if not book:
            print("Книга не найдена.")
            return
        c.execute("INSERT INTO purchases (customer_name, book_title) VALUES (?, ?)", (customer_name, book_title))
        conn.commit()
        print(f"Книга '{book_title}' куплена покупателем '{customer_name}'.")
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    global conn
    conn = sqlite3.connect('books.db')
    create_tables(conn)

if __name__ == "__main__":
    main()
