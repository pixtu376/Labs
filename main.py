class Book:
    def __init__(self, title, author, genre, price):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price

    def __str__(self):
        return f"Название: {self.title}, Автор: {self.author.name}, Жанр: {self.genre.name}, Цена: {self.price}Р"

    def update(self, title=None, author=None, genre=None, price=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if genre:
            self.genre = genre
        if price:
            self.price = price


class Genre:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Жанр: {self.name}"


class Author:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Автор: {self.name}"

    def update(self, name):
        self.name = name


class Customer:
    def __init__(self, name):
        self.name = name
        self.books = []

    def __str__(self):
        return f"Имя покупателя: {self.name}"

    def buy_book(self, book):
        self.books.append(book)


class Store:
    def __init__(self, name):
        self.name = name
        self.library = []

    def add_book(self, book):
        self.library.append(book)

    def remove_book(self, book_title):
        self.library = [b for b in self.library if b.title != book_title]

    def __str__(self):
        return f"Название магазина: {self.name}"


def display_menu():
    print("\nМеню управления системой мониторинга книжными магазинами")
    print("1. Книги")
    print("2. Жанры")
    print("3. Авторы")
    print("4. Покупатели")
    print("5. Магазины")
    print("0. Выход")


def add_book(authors, genres, store):
    title = input("Введите название книги: ")
    author_name = input("Введите имя автора: ")
    author = None
    for a in authors:
        if a.name == author_name:
            author = a
            break
    if not author:
        print("Автор с таким именем не найден.")
        return
    genre_name = input("Введите название жанра: ")
    genre = None
    for g in genres:
        if g.name == genre_name:
            genre = g
            break
    if not genre:
        print("Жанр с таким именем не найден.")
        return
    price = float(input("Введите цену книги: "))
    book = Book(title, author, genre, price)
    store.add_book(book)
    print(f"Книга '{title}' добавлена.")


def edit_book(books, authors, genres):
    book_title = input("Введите название книги для изменения: ")
    book = None
    for b in books:
        if b.title == book_title:
            book = b
            break
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
        book.update(title=new_title)
    elif choice == '2':
        author_name = input("Введите имя нового автора: ")
        author = None
        for a in authors:
            if a.name == author_name:
                author = a
                break
        if not author:
            print("Автор с таким именем не найден.")
            return
        book.update(author=author)
    elif choice == '3':
        genre_name = input("Введите название нового жанра: ")
        genre = None
        for g in genres:
            if g.name == genre_name:
                genre = g
                break
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

    print("Книга обновлена.")


def delete_book(store):
    book_title = input("Введите название книги для удаления: ")
    store.remove_book(book_title)
    print("Книга удалена.")


def add_author(authors):
    name = input("Введите имя автора: ")
    author = Author(name)
    authors.append(author)
    print(f"Автор '{name}' добавлен.")


def edit_author(authors):
    author_name = input("Введите имя автора для изменения: ")
    author = None
    for a in authors:
        if a.name == author_name:
            author = a
            break
    if not author:
        print("Автор с таким именем не найден.")
        return
    new_name = input("Введите новое имя: ")
    author.update(new_name)
    print("Автор обновлен")


def delete_author(authors):
    author_name = input("Введите имя автора для удаления: ")
    author = None
    for a in authors:
        if a.name == author_name:
            author = a
            break
    if not author:
        print("Автор с таким именем не найден.")
        return
    authors.remove(author)
    print("Автор удален.")


def buy_book(customers, stores):
    customer_name = input("Введите имя покупателя: ")
    customer = None
    for c in customers:
        if c.name == customer_name:
            customer = c
            break
    if not customer:
        print("Покупатель с таким именем не найден.")
        return

    store_name = input("Введите название магазина: ")
    store = None
    for s in stores:
        if s.name == store_name:
            store = s
            break
    if not store:
        print("Магазин с таким названием не найден.")
        return

    print("Доступные книги в магазине:")
    for i, book in enumerate(store.library):
        print(f"{i+1}. {book.title} - {book.author.name} - {book.genre.name} - {book.price}Р")

    book_choice = input("Введите номер книги для покупки: ")
    try:
        book_choice = int(book_choice)
        if book_choice < 1 or book_choice > len(store.library):
            print("Неправильный номер книги.")
            return
    except ValueError:
        print("Неправильный номер книги.")
        return

    book = store.library[book_choice - 1]
    customer.buy_book(book)
    store.remove_book(book.title)
    print(f"Книга '{book.title}' куплена покупателем '{customer.name}'.")


def main():
    books = []
    genres = [Genre("Детская литература"), Genre("Мистика"), Genre("Научная литература")]
    authors = [Author("Стивен")]
    customers = [Customer("Байден")]
    stores = [Store("Магазин на Ленина"), Store("Магазин на Пролетарской")]

    while True:
        display_menu()
        choice = input("Выберите действие: ")

        if choice == "1":  # Книги
            while True:
                print(f"Меню управления книгами")
                print(f"1. Показать все книги")
                print(f"2. Добавить книгу")
                print(f"3. Изменить книгу")
                print(f"4. Удалить книгу")
                print("0. Назад")
                book_choice = input("Выберите действие для книг: ")
                if book_choice == "1":
                    for store in stores:
                        print(f"{store.name}")
                        for b in store.library:
                            print(b)
                elif book_choice == "2":
                    store_name = input("Введите название магазина, куда добавить книгу: ")
                    store = None
                    for s in stores:
                        if s.name == store_name:
                            store = s
                            break
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    add_book(authors, genres, store)
                elif book_choice == "3":
                    store_name = input("Введите название магазина, где находится книга для изменения: ")
                    store = None
                    for s in stores:
                        if s.name == store_name:
                            store = s
                            break
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    edit_book(store.library, authors, genres)
                elif book_choice == "4":
                    store_name = input("Введите название магазина, где находится книга для удаления: ")
                    store = None
                    for s in stores:
                        if s.name == store_name:
                            store = s
                            break
                    if not store:
                        print("Магазин с таким названием не найден.")
                        continue
                    delete_book(store)
                elif book_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "2":  # Жанры
            while True:
                print("Список жанров:")
                for g in genres:
                    print(g)
                print("0. Назад")
                store_choice = input("Выберите действие для списка жанров: ")
                if store_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "3":  # Авторы
            while True:
                print(f"Меню управления авторами")
                print(f"1. Показать всех авторов")
                print(f"2. Добавить автора")
                print(f"3. Изменить автора")
                print(f"4. Удалить автора")
                print("0. Назад")
                author_choice = input("Выберите действие для авторов: ")
                if author_choice == "1":
                    for a in authors:
                        print(a)
                elif author_choice == "2":
                    add_author(authors)
                elif author_choice == "3":
                    edit_author(authors)
                elif author_choice == "4":
                    delete_author(authors)
                elif author_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "4":  # Покупатели
            while True:
                print("Список покупателей:")
                for c in customers:
                    print(c)
                    print("Купленные книги:")
                    for b in c.books:
                        print(b)
                print("1. Купить книгу")
                print("0. Назад")
                store_choice = input("Выберите действие для списка покупателей: ")
                if store_choice == "0":
                    break
                elif store_choice == "1":
                    buy_book(customers, stores)
                else:
                    print("Неверный ввод")

        elif choice == "5":  # Магазины
            while True:
                print("Список магазинов:")
                for s in stores:
                    print(s)
                print("0. Назад")
                store_choice = input("Выберите действие для списка магазинов: ")
                if store_choice == "0":
                    break
                else:
                    print("Неверный ввод")

        elif choice == "0":  # Выход
            break
        else:
            print("Неверный ввод. Попробуйте еще раз.")

main()