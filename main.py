import sqlite3

class Entity():
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
        Book.total_books += 1  # инкремент статического поля при создании нового экземпляра

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
    def get_total_books():  # статический метод
        return Book.total_books

    # Перегрузка операторов
    def __add__(self, other):
        try:
            return Book(self.name + " and " + other.name, self.author + " and " + other.author, self.genre + " and " + other.genre, self.price + other.price)
        except Exception as e:
            print(f"Ошибка: {e}")

    def __sub__(self, other):
        try:
            return Book(self.name + " without " + other.name, self.author + " without " + other.author, self.genre + " without " + other.genre, self.price - other.price)
        except Exception as e:
            print(f"Ошибка: {e}")

    def __mul__(self, other):
        try:
            return Book(self.name + " times " + other.name, self.author + " times " + other.author, self.genre + " times " + other.genre, self.price * other.price)
        except Exception as e:
            print(f"Ошибка: {e}")

    def __eq__(self, other):
        try:
            return self.name == other.name and self.author == other.author and self.genre == other.genre and self.price == other.price
        except Exception as e:
            print(f"Ошибка: {e}")

    def __ne__(self, other):
        try:
            return not self == other
        except Exception as e:
            print(f"Ошибка: {e}")

    # Методы для управления состоянием объектов
    def set_title(self, title):
        self.name = title

    def get_title(self):
        return self.name

    def set_author(self, author):
        self.author = author

    def get_author(self):
        return self.author

    def set_genre(self, genre):
        self.genre = genre

    def get_genre(self):
        return self.genre

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price


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

    def add_book(self, book):
        self.library.append(book)

    def remove_book(self, book_title):
        self.library = [b for b in self.library if b.name != book_title]


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


def add_book(conn, authors, genres, store):
    try:
        title = input("Введите название книги: ")
        title = title.strip()  # Удаление пробелов в начале и конце строки
        title = title.lower()  # Преобразование строки в нижний регистр
        author_name = input("Введите имя автора: ")
        author_name = author_name.strip()  # Удаление пробелов в начале и конце строки
        author_name = author_name.lower()  # Преобразование строки в нижний регистр
        author = authors.get(author_name)
        if not author:
            print("Автор с таким именем не найден.")
            return
        genre_name = input("Введите название жанра: ")
        genre_name = genre_name.strip()  # Удаление пробелов в начале и конце строки
        genre_name = genre_name.lower()  # Преобразование строки в нижний регистр
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
        book_title = input("Введите название книги для изменения: ")
        book_title = book_title.strip()  # Удаление пробелов в начале и конце строки
        book_title = book_title.lower()  # Преобразование строки в нижний регистр
        book = books.get(book_title)
        if not book:
            print("Книга с таким названием не найдена.")
            return

        print("Что вы хотите изменить?")
        print("1. Название")
        print("2. Автор")
        print("3. Жанр")
        print("4. Цена")
        choice = input("Выберите опцию: ")

        if choice == '1':
            new_title = input("Введите новое название: ")
            new_title = new_title.strip()  # Удаление пробелов в начале и конце строки
            new_title = new_title.lower()  # Преобразование строки в нижний регистр
            book.update(title=new_title)
        elif choice == '2':
            author_name = input("Введите имя нового автора: ")
            author_name = author_name.strip()  # Удаление пробелов в начале и конце строки
            author_name = author_name.lower()  # Преобразование строки в нижний регистр
            author = authors.get(author_name)
            if not author:
                print("Автор с таким именем не найден.")
                return
            book.update(author=author)
        elif choice == '3':
            genre_name = input("Введите название нового жанра: ")
            genre_name = genre_name.strip()  # Удаление пробелов в начале и конце строки
            genre_name = genre_name.lower()  # Преобразование строки в нижний регистр
            genre = genres.get(genre_name)
            if not genre:
                print("Жанр с таким именем не найден.")
                return
            book.update(genre=genre)
        elif choice == '4':
            price = float(input("Введите новую цену: "))
            book.update(price=price)
        else:
            print("Неверный выбор")
            return

        c = conn.cursor()
        c.execute("UPDATE books SET title = ?, author = ?, genre = ?, price = ? WHERE title = ?",
                  (book.name, book.author.name, book.genre.name, book.price, book_title))
        conn.commit()
        print("Книга обновлена.")
    except Exception as e:
        print(f"Ошибка: {e}")


def delete_book(conn, store):
    try:
        book_title = input("Введите название книги для удаления: ")
        book_title = book_title.strip()  # Удаление пробелов в начале и конце строки
        book_title = book_title.lower()  # Преобразование строки в нижний регистр
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE title = ?", (book_title,))
        conn.commit()
        print("Книга удалена.")
    except Exception as e:
        print(f"Ошибка: {e}")


def add_author(conn, authors):
    try:
        name = input("Введите имя автора: ")
        name = name.strip()  # Удаление пробелов в начале и конце строки
        name = name.lower()  # Преобразование строки в нижний регистр
        author = Author(name)
        c = conn.cursor()
        c.execute("INSERT INTO authors VALUES (?)", (author.name,))
        conn.commit()
        authors[author.name] = author
        print(f"Автор '{name}' добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")


def edit_author(conn, authors):
    try:
        author_name = input("Введите имя автора для изменения: ")
        author_name = author_name.strip()  # Удаление пробелов в начале и конце строки
        author_name = author_name.lower()  # Преобразование строки в нижний регистр
        author = authors.get(author_name)
        if not author:
            print("Автор с таким именем не найден.")
            return
        new_name = input("Введите новое имя: ")
        new_name = new_name.strip()  # Удаление пробелов в начале и конце строки
        new_name = new_name.lower()  # Преобразование строки в нижний регистр
        author.update(new_name)
        c = conn.cursor()
        c.execute("UPDATE authors SET name = ? WHERE name = ?", (new_name, author_name))
        conn.commit()
        print("Автор обновлен")
    except Exception as e:
        print(f"Ошибка: {e}")


def delete_author(conn, authors):
    try:
        author_name = input("Введите имя автора для удаления: ")
        author_name = author_name.strip()  # Удаление пробелов в начале и конце строки
        author_name = author_name.lower()  # Преобразование строки в нижний регистр
        author = authors.get(author_name)
        if not author:
            print("Автор с таким именем не найден.")
            return
        c = conn.cursor()
        c.execute("DELETE FROM authors WHERE name = ?", (author_name,))
        conn.commit()
        del authors[author_name]
        print("Автор удален.")
    except Exception as e:
        print(f"Ошибка: {e}")


def buy_book(conn, customers, stores):
    try:
        customer_name = input("Введите имя покупателя: ")
        customer_name = customer_name.strip()  # Удаление пробелов в начале и конце строки
        customer_name = customer_name.lower()  # Преобразование строки в нижний регистр
        customer = customers.get(customer_name)
        if not customer:
            print("Покупатель с таким именем не найден.")
            return

        store_name = input("Введите название магазина: ")
        store_name = store_name.strip()  # Удаление пробелов в начале и конце строки
        store_name = store_name.lower()  # Преобразование строки в нижний регистр
        store = stores.get(store_name)
        if not store:
            print("Магазин с таким названием не найден.")
            return

        print("Доступные книги в магазине:")
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        for book in books:
            print(book)

        book_title = input("Введите название книги для покупки: ")
        book_title = book_title.strip()  # Удаление пробелов в начале и конце строки
        book_title = book_title.lower()  # Преобразование строки в нижний регистр
        c.execute("SELECT * FROM books WHERE title = ?", (book_title,))
        book = c.fetchone()
        if not book:
            print("Книга с таким названием не найдена.")
            return

        customer.buy_book(book)
        c.execute("DELETE FROM books WHERE title = ?", (book_title,))
        conn.commit()
        print(f"Книга '{book_title}' куплена покупателем '{customer_name}'.")
    except Exception as e:
        print(f"Ошибка: {e}")


def overload_operators(conn, books):
    try:
        print("\nМеню перегрузки операторов")
        print("1. Сложение книг")
        print("2. Вычитание книг")
        print("3. Умножение книг")
        print("4. Сравнение книг")
        print("0. Назад")
        operator_choice = input("Выберите операцию: ")

        if operator_choice == "1":
            # Сложение книг
            book1_title = input("Введите название первой книги: ")
            book2_title = input("Введите название второй книги: ")
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE title = ?", (book1_title,))
            book1 = c.fetchone()
            c.execute("SELECT * FROM books WHERE title = ?", (book2_title,))
            book2 = c.fetchone()
            if not book1 or not book2:
                print("Одна из книг не найдена.")
                return
            book = Book(book1[0], book1[1], book1[2], book1[3]) + Book(book2[0], book2[1], book2[2], book2[3])
            print(book)

        elif operator_choice == "2":
            # Вычитание книг
            book1_title = input("Введите название первой книги: ")
            book2_title = input("Введите название второй книги: ")
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE title = ?", (book1_title,))
            book1 = c.fetchone()
            c.execute("SELECT * FROM books WHERE title = ?", (book2_title,))
            book2 = c.fetchone()
            if not book1 or not book2:
                print("Одна из книг не найдена.")
                return
            book = Book(book1[0], book1[1], book1[2], book1[3]) - Book(book2[0], book2[1], book2[2], book2[3])
            print(book)

        elif operator_choice == "3":
            # Умножение книг
            book1_title = input("Введите название первой книги: ")
            book2_title = input("Введите название второй книги: ")
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE title = ?", (book1_title,))
            book1 = c.fetchone()
            c.execute("SELECT * FROM books WHERE title = ?", (book2_title,))
            book2 = c.fetchone()
            if not book1 or not book2:
                print("Одна из книг не найдена.")
                return
            book = Book(book1[0], book1[1], book1[2], book1[3]) * Book(book2[0], book2[1], book2[2], book2[3])
            print(book)

        elif operator_choice == "4":
            # Сравнение книг
            book1_title = input("Введите название первой книги: ")
            book2_title = input("Введите название второй книги: ")
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE title = ?", (book1_title,))
            book1 = c.fetchone()
            c.execute("SELECT * FROM books WHERE title = ?", (book2_title,))
            book2 = c.fetchone()
            if not book1 or not book2:
                print("Одна из книг не найдена.")
                return
            if Book(book1[0], book1[1], book1[2], book1[3]) == Book(book2[0], book2[1], book2[2], book2[3]):
                print("Книги равны")
            else:
                print("Книги не равны")

        elif operator_choice == "0":
            return

        else:
            print("Неверный выбор")
    except Exception as e:
        print(f"Ошибка: {e}")


def main():
    conn = sqlite3.connect('books.db')
    create_tables(conn)
    books = {}
    genres = {"Детская литература": Genre("Детская литература"), "Мистика": Genre("Мистика"), "Научная литература": Genre("Научная литература")}
    authors = {"Стивен": Author("Стивен")}
    customers = {"Байден": Customer("Байден")}
    stores = {"Магазин на Ленина": Store("Магазин на Ленина"), "Магазин на Пролетарской": Store("Магазин на Пролетарской")}

    while True:
        print("\nМеню управления системой мониторинга книжными магазинами")
        print("1. Книги")
        print("2. Жанры")
        print("3. Авторы")
        print("4. Покупатели")
        print("5. Магазины")
        print("6. Перегрузка операторов")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":  
            while True:
                print(f"Меню управления книгами")
                print(f"1. Показать все книги")
                print(f"2. Добавить книгу")
                print(f"3. Изменить книгу")
                print(f"4. Удалить книгу")
                print("5. Показать общее количество книг")
                print("0. Назад")
                book_choice = input("Выберите действие для книг: ")
                if book_choice == "1":
                    c = conn.cursor()
                    c.execute("SELECT * FROM books")
                    books = c.fetchall()
                    for book in books:
                        print(book)
                elif book_choice == "2":
                    store_name = input("Введите название магазина, куда добавить книгу: ")
                    store_name = store_name.strip()  # Удаление пробелов в начале и конце строки
                    store_name = store_name.lower()  # Преобразование строки в нижний регистр
                    store = stores.get(store_name)
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    add_book(conn, authors, genres, store)
                elif book_choice == "3":
                    store_name = input("Введите название магазина, где находится книга для изменения: ")
                    store_name = store_name.strip()  # Удаление пробелов в начале и конце строки
                    store_name = store_name.lower()  # Преобразование строки в нижний регистр
                    store = stores.get(store_name)
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    edit_book(conn, books, authors, genres)
                elif book_choice == "4":
                    store_name = input("Введите название магазина, где находится книга для удаления: ")
                    store_name = store_name.strip()  # Удаление пробелов в начале и конце строки
                    store_name = store_name.lower()  # Преобразование строки в нижний регистр
                    store = stores.get(store_name)
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    delete_book(conn, store)
                elif book_choice == "5":
                    print(f"Общее количество книг: {Book.get_total_books()}")
                elif book_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "2":  
            while True:
                print("Список жанров:")
                for genre in genres.values():
                    print(genre)
                print("0. Назад")
                store_choice = input("Выберите действие для списка жанров: ")
                if store_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "3":  
            while True:
                print(f"Меню управления авторами")
                print(f"1. Показать всех авторов")
                print(f"2. Добавить автора")
                print(f"3. Изменить автора")
                print(f"4. Удалить автора")
                print("0. Назад")
                author_choice = input("Выберите действие для авторов: ")
                if author_choice == "1":
                    for author in authors.values():
                        print(author)
                elif author_choice == "2":
                    add_author(conn, authors)
                elif author_choice == "3":
                    edit_author(conn, authors)
                elif author_choice == "4":
                    delete_author(conn, authors)
                elif author_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "4":  
            while True:
                print("Список покупателей:")
                for customer in customers.values():
                    print(customer)
                    print("Купленные книги:")
                    for book in customer.books:
                        print(book)
                print("1. Купить книгу")
                print("0. Назад")
                store_choice = input("Выберите действие для списка покупателей: ")
                if store_choice == "0":
                    break
                elif store_choice == "1":
                    buy_book(conn, customers, stores)
                else:
                    print("Неверный ввод")

        elif choice == "5":  
            while True:
                print("Список магазинов:")
                for store in stores.values():
                    print(store)
                print("0. Назад")
                store_choice = input("Выберите действие для списка магазинов: ")
                if store_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "6":  
            overload_operators(conn, books)

        elif choice == "0":  
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")

    conn.close()

if __name__ == "__main__":
    main()