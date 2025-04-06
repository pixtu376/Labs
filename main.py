import sqlite3
from database import create_tables, add_book, edit_book, delete_book, add_author, edit_author, delete_author, buy_book
from classes import Book, Author, Genre, Customer, Store

def load_books(conn):
    c = conn.cursor()
    c.execute("SELECT title, author, genre, price FROM books")
    rows = c.fetchall()
    books = []
    for row in rows:
        title, author_name, genre_name, price = row
        author = Author(author_name)
        genre = Genre(genre_name)
        book = Book(title, author, genre, price)
        books.append(book)
    return books

def main():
    global conn
    conn = sqlite3.connect('books.db')
    create_tables(conn)

    books = load_books(conn)

    authors = {
        "Стивен": Author("Стивен"),
        "Дж.К.": Author("Дж.К."),
        "Агата": Author("Агата")
    }
    genres = {
        "Детская литература": Genre("Детская литература"),
        "Мистика": Genre("Мистика"),
        "Научная литература": Genre("Научная литература")
    }
    stores = {
        "Магазин на Ленина": Store("Магазин на Ленина"),
        "Магазин на Пролетарской": Store("Магазин на Пролетарской"),
        "Книжный мир": Store("Книжный мир")
    }
    customers = {
        "Байден": Customer("Байден"),
        "Путин": Customer("Путин"),
        "Трамп": Customer("Трамп")
    }

    while True:
        print("\nМеню управления системой мониторинга книжными магазинами")
        print("1. Книги")
        print("2. Жанры")
        print("3. Авторы")
        print("4. Покупатели")
        print("5. Магазины")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            while True:
                print(f"Меню управления книгами")
                print(f"1. Показать все книги")
                print(f"2. Добавить книгу в базу данных")
                print(f"3. Добавить книгу в библиотеку")
                print(f"0. Назад")
                book_choice = input("Выберите действие для книг: ")
                if book_choice == "1":
                    for book in books:
                        print(book)
                elif book_choice == "2":
                    book_title = input("Введите название книги: ")
                    author_name = input("Введите имя автора: ")
                    genre_name = input("Введите название жанра: ")
                    price = float(input("Введите цену книги: "))
                    
                    new_book = Book(book_title, Author(author_name), Genre(genre_name), price)
                    add_book(conn, book_title, author_name, genre_name, price)
                    books.append(new_book)
                    print(f"Книга '{book_title}' добавлена в базу данных.")
                elif book_choice == "3":
                    print("Доступные книги:")
                    for idx, book in enumerate(books):
                        print(f"{idx + 1}. {book.name} - Автор: {book.author.name}, Жанр: {book.genre.name}, Цена: {book.price}Р")
                    
                    book_choice = int(input("Выберите номер книги для добавления в библиотеку: ")) - 1
                    store_name = input("Введите название магазина: ")
                    
                    if store_name in stores:
                        selected_book = books[book_choice]
                        stores[store_name].add_book_with_conn(conn, selected_book)
                        print(f"Книга '{selected_book.name}' добавлена в библиотеку магазина '{store_name}'.")
                    else:
                        print("Магазин не найден.")
                elif book_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "2":  # Управление жанрами
            while True:
                print("Меню управления жанрами")
                print("1. Показать все жанры")
                print("2. Добавить жанр")
                print("0. Назад")
                genre_choice = input("Выберите действие для жанров: ")
                if genre_choice == "1":
                    for genre in genres.values():
                        print(genre)
                elif genre_choice == "2":
                    genre_name = input("Введите название жанра: ")
                    new_genre = Genre(genre_name)
                    genres[genre_name] = new_genre
                    print(f"Жанр '{genre_name}' добавлен.")
                elif genre_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "3":  # Управление авторами
            while True:
                print("Меню управления авторами")
                print("1. Показать всех авторов")
                print("2. Добавить автора")
                print("0. Назад")
                author_choice = input("Выберите действие для авторов: ")
                if author_choice == "1":
                    for author in authors.values():
                        print(author)
                elif author_choice == "2":
                    author_name = input("Введите имя автора: ")
                    new_author = Author(author_name)
                    authors[author_name] = new_author
                    print(f"Автор '{author_name}' добавлен.")
                elif author_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "4":  # Управление покупателями
            while True:
                print("Меню управления покупателями")
                print("1. Показать всех покупателей")
                print("2. Добавить покупателя")
                print("0. Назад")
                customer_choice = input("Выберите действие для покупателей: ")
                if customer_choice == "1":
                    for customer in customers.values():
                        print(customer)
                elif customer_choice == "2":
                    customer_name = input("Введите имя покупателя: ")
                    new_customer = Customer(customer_name)
                    customers[customer_name] = new_customer
                    print(f"Покупатель '{customer_name}' добавлен.")
                elif customer_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "5":  # Управление магазинами
            while True:
                print("Меню управления магазинами")
                print("1. Показать все магазины")
                print("2. Добавить магазин")
                print("3. Показать библиотеку магазина")
                print("0. Назад")
                store_choice = input("Выберите действие для магазинов: ")
                if store_choice == "1":
                    for store in stores.values():
                        print(store)
                elif store_choice == "2":
                    store_name = input("Введите название магазина: ")
                    new_store = Store(store_name)
                    stores[store_name] = new_store
                    print(f"Магазин '{store_name}' добавлен.")
                elif store_choice == "3":
                    store_name = input("Введите название магазина для просмотра библиотеки: ")
                    if store_name in stores:
                        print(f"Библиотека магазина '{store_name}':")
                        for book in stores[store_name].library:
                            print(book)
                    else:
                        print("Магазин не найден.")
                elif store_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "0":
            break
        else:
            print("Неверный ввод")

    conn.close()

if __name__ == "__main__":
    main()

store_example = Store("Пример Магазина")
book_example = Book("Пример Книги", Author("Автор Примера"), Genre("Жанр Примера"), 100)
store_example + book_example
print(f"Книги в магазине '{store_example.name}':")
for book in store_example.library:
    print(book)