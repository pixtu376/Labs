# database.py
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
    c.execute("""CREATE TABLE IF NOT EXISTS store_books (
                store_name text,
                book_title text,
                PRIMARY KEY (store_name, book_title),
                FOREIGN KEY (store_name) REFERENCES stores(name),
                FOREIGN KEY (book_title) REFERENCES books(title)
                )""")
    conn.commit()

def add_book(conn, title, author, genre, price):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                 (title, author, genre, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_author(conn, name):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO authors VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_genre(conn, name):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO genres VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_customer(conn, name):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO customers VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_store(conn, name):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO stores VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_book_to_store(conn, store_name, book_title):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO store_books VALUES (?, ?)", 
                 (store_name, book_title))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_store_books(conn, store_name):
    c = conn.cursor()
    c.execute("""SELECT b.title, b.author, b.genre, b.price 
                FROM books b JOIN store_books sb ON b.title = sb.book_title
                WHERE sb.store_name = ?""", (store_name,))
    return c.fetchall()

def get_all_books(conn):
    c = conn.cursor()
    c.execute("SELECT title, author, genre, price FROM books")
    return c.fetchall()

def get_all_authors(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM authors")
    return [row[0] for row in c.fetchall()]

def get_all_genres(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM genres")
    return [row[0] for row in c.fetchall()]

def get_all_stores(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM stores")
    return [row[0] for row in c.fetchall()]

def get_all_customers(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM customers")
    return [row[0] for row in c.fetchall()]

def main():
    conn = sqlite3.connect('books.db')
    create_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()