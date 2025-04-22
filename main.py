import sys
import os
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QLineEdit, QComboBox, QListWidget,
                            QTabWidget, QFormLayout, QMessageBox, QStackedWidget, QDialog,
                            QDialogButtonBox, QGridLayout, QFrame, QGroupBox, QSizePolicy)
from PyQt5.QtGui import QDoubleValidator, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QLibraryInfo, QSize
from database import create_tables, add_book, add_author, add_genre, add_store, add_customer
from classes import Book, Author, Genre, Store, Customer
from logger import logger

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = QLibraryInfo.location(QLibraryInfo.PluginsPath) + '\\platforms'

class BookStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.log_info("Инициализация приложения")
        
        try:
            # Подключение к базе данных
            self.conn = sqlite3.connect('books.db')
            create_tables(self.conn)
            logger.log_info("База данных подключена")
            
            # Загрузка данных
            self.books = []
            self.authors = []
            self.genres = []
            self.stores = []
            self.customers = []
            self.load_initial_data()
            
            # Настройка интерфейса
            self.setup_ui()
            logger.log_info("Интерфейс настроен")
            
        except Exception as e:
            logger.log_error(f"Ошибка инициализации: {str(e)}")
            raise

    def load_initial_data(self):
        """Загрузка начальных данных из базы"""
        try:
            # Загрузка книг
            cur = self.conn.cursor()
            cur.execute("SELECT title, author, genre, price FROM books")
            self.books = [Book(title, Author(author), Genre(genre), price) 
                         for title, author, genre, price in cur.fetchall()]
            
            # Загрузка авторов
            cur.execute("SELECT name FROM authors")
            self.authors = [Author(name[0]) for name in cur.fetchall()]
            
            # Загрузка жанров
            cur.execute("SELECT name FROM genres")
            self.genres = [Genre(name[0]) for name in cur.fetchall()]
            
            # Загрузка магазинов
            cur.execute("SELECT name FROM stores")
            self.stores = [Store(name[0]) for name in cur.fetchall()]
            
            # Загрузка покупателей
            cur.execute("SELECT name FROM customers")
            self.customers = [Customer(name[0]) for name in cur.fetchall()]
            
            logger.log_info("Данные успешно загружены")
        except Exception as e:
            logger.log_error(f"Ошибка загрузки данных: {str(e)}")
            raise

    def setup_ui(self):
        """Настройка пользовательского интерфейса по макетам"""
        self.setWindowTitle("Управление книжным магазином")
        self.setGeometry(100, 100, 1200, 800)
        
        # Зелёная цветовая схема
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f9f0;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #333;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
                color: #333;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #a0c0a0;
                border-radius: 4px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #a0c0a0;
                border-radius: 4px;
                background-color: white;
            }
        """)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Верхняя панель с кнопками навигации
        self.top_nav = QHBoxLayout()
        self.top_nav.setSpacing(10)
        
        self.books_btn = QPushButton("Книги")
        self.authors_btn = QPushButton("Авторы")
        self.genres_btn = QPushButton("Жанры")
        self.stores_btn = QPushButton("Магазины")
        self.customers_btn = QPushButton("Покупатели")
        
        self.books_btn.clicked.connect(lambda: self.show_category("books"))
        self.authors_btn.clicked.connect(lambda: self.show_category("authors"))
        self.genres_btn.clicked.connect(lambda: self.show_category("genres"))
        self.stores_btn.clicked.connect(lambda: self.show_category("stores"))
        self.customers_btn.clicked.connect(lambda: self.show_category("customers"))
        
        # Устанавливаем фиксированный размер для кнопок
        for btn in [self.books_btn, self.authors_btn, self.genres_btn, 
                   self.stores_btn, self.customers_btn]:
            btn.setFixedSize(120, 40)
        
        self.top_nav.addWidget(self.books_btn)
        self.top_nav.addWidget(self.authors_btn)
        self.top_nav.addWidget(self.genres_btn)
        self.top_nav.addWidget(self.stores_btn)
        self.top_nav.addWidget(self.customers_btn)
        self.top_nav.addStretch()
        
        main_layout.addLayout(self.top_nav)
        
        # Центральная область с информационными блоками
        self.central_area = QVBoxLayout()
        
        # Верхняя строка с 5 блоками
        self.top_row = QHBoxLayout()
        self.top_row.setSpacing(15)
        
        # Создаем 5 информационных блоков одинакового размера
        self.info_blocks = []
        for i in range(5):
            block = QGroupBox()
            block.setFixedSize(220, 220)  # Фиксированный размер блоков
            block_layout = QVBoxLayout(block)
            
            title = QLabel()
            title.setStyleSheet("font-weight: bold; font-size: 16px;")
            block_layout.addWidget(title)
            
            content = QLabel()
            content.setWordWrap(True)
            block_layout.addWidget(content)
            
            self.info_blocks.append((block, title, content))
            self.top_row.addWidget(block)
        
        self.central_area.addLayout(self.top_row)
        
        # Нижний информационный блок с кнопками
        self.bottom_block = QGroupBox()
        bottom_layout = QVBoxLayout(self.bottom_block)
        
        self.bottom_content = QLabel()
        self.bottom_content.setWordWrap(True)
        bottom_layout.addWidget(self.bottom_content)
        
        # Кнопки действий
        self.action_buttons = QHBoxLayout()
        
        self.add_btn = QPushButton()
        self.add_btn.setFixedSize(150, 40)
        
        self.add_to_store_btn = QPushButton("Добавить книгу в магазин")
        self.add_to_store_btn.setFixedSize(180, 40)
        self.add_to_store_btn.clicked.connect(self.show_add_to_store_dialog)
        self.add_to_store_btn.hide()
        
        self.show_store_btn = QPushButton("Показать библиотеку")
        self.show_store_btn.setFixedSize(150, 40)
        self.show_store_btn.clicked.connect(self.show_store_books_dialog)
        self.show_store_btn.hide()
        
        self.action_buttons.addWidget(self.add_btn)
        self.action_buttons.addWidget(self.add_to_store_btn)
        self.action_buttons.addWidget(self.show_store_btn)
        self.action_buttons.addStretch()
        
        bottom_layout.addLayout(self.action_buttons)
        
        self.central_area.addWidget(self.bottom_block)
        
        main_layout.addLayout(self.central_area)
        
        # Инициализируем данные для книг (стартовая страница)
        self.show_category("books")

    def show_category(self, category):
        """Показывает информацию для выбранной категории"""
        # Сначала отключаем только если есть подключения
        try:
            self.add_btn.clicked.disconnect()
        except TypeError:
            pass  # Нет подключений, ничего делать не нужно
        
        # Скрываем все специальные кнопки
        self.add_to_store_btn.hide()
        self.show_store_btn.hide()
        
        if category == "books":
            self.update_books_info()
            self.add_btn.setText("Добавить книгу")
            self.add_btn.clicked.connect(self.show_add_book_dialog)
            self.add_to_store_btn.show()
        elif category == "authors":
            self.update_authors_info()
            self.add_btn.setText("Добавить автора")
            self.add_btn.clicked.connect(self.show_add_author_dialog)
        elif category == "genres":
            self.update_genres_info()
            self.add_btn.setText("Добавить жанр")
            self.add_btn.clicked.connect(self.show_add_genre_dialog)
        elif category == "stores":
            self.update_stores_info()
            self.add_btn.setText("Добавить магазин")
            self.add_btn.clicked.connect(self.show_add_store_dialog)
            self.show_store_btn.show()
        elif category == "customers":
            self.update_customers_info()
            self.add_btn.setText("Добавить покупателя")
            self.add_btn.clicked.connect(self.show_add_customer_dialog)

    def update_books_info(self):
        """Обновляет информацию о книгах"""
        # Обновляем 5 информационных блоков
        for i, (block, title, content) in enumerate(self.info_blocks[:5]):
            if i < len(self.books):
                book = self.books[i]
                title.setText(f"Книга: {book.name}")
                text = f"Автор: {book.author.name}\nЖанр: {book.genre.name}\nЦена: {book.price}р"
                content.setText(text)
            else:
                title.setText("Книга")
                content.setText("Нет данных")
        
        # Обновляем нижний блок
        self.bottom_block.setTitle("Общее о книгах")
        self.bottom_content.setText(f"Всего книг: {len(self.books)}\nСредняя цена: {self.calculate_avg_price():.2f}р")

    def update_authors_info(self):
        """Обновляет информацию об авторах"""
        for i, (block, title, content) in enumerate(self.info_blocks[:5]):
            if i < len(self.authors):
                author = self.authors[i]
                book_count = sum(1 for book in self.books if book.author.name == author.name)
                genres = set(book.genre.name for book in self.books if book.author.name == author.name)
                
                title.setText(f"Автор: {author.name}")
                text = f"Книг: {book_count}\nЖанры: {', '.join(genres) if genres else 'нет'}"
                content.setText(text)
            else:
                title.setText("Автор")
                content.setText("Нет данных")
        
        self.bottom_block.setTitle("Общее об авторах")
        self.bottom_content.setText(f"Всего авторов: {len(self.authors)}\nСреднее книг на автора: {len(self.books)/len(self.authors) if self.authors else 0:.1f}")

    def update_genres_info(self):
        """Обновляет информацию о жанрах"""
        for i, (block, title, content) in enumerate(self.info_blocks[:5]):
            if i < len(self.genres):
                genre = self.genres[i]
                book_count = sum(1 for book in self.books if book.genre.name == genre.name)
                authors = set(book.author.name for book in self.books if book.genre.name == genre.name)
                
                title.setText(f"Жанр: {genre.name}")
                text = f"Книг: {book_count}\nАвторы: {', '.join(authors) if authors else 'нет'}"
                content.setText(text)
            else:
                title.setText("Жанр")
                content.setText("Нет данных")
        
        self.bottom_block.setTitle("Общее о жанрах")
        self.bottom_content.setText(f"Всего жанров: {len(self.genres)}\nСреднее книг на жанр: {len(self.books)/len(self.genres) if self.genres else 0:.1f}")

    def update_stores_info(self):
        """Обновляет информацию о магазинах"""
        for i, (block, title, content) in enumerate(self.info_blocks[:5]):
            if i < len(self.stores):
                store = self.stores[i]
                title.setText(f"Магазин: {store.name}")
                text = f"Книг: {len(store.library)}\n"
                content.setText(text)
            else:
                title.setText("Магазин")
                content.setText("Нет данных")
        
        self.bottom_block.setTitle("Общее о магазинах")
        total_books = sum(len(store.library) for store in self.stores)
        self.bottom_content.setText(f"Всего магазинов: {len(self.stores)}\nВсего книг в магазинах: {total_books}")

    def update_customers_info(self):
        """Обновляет информацию о покупателях"""
        for i, (block, title, content) in enumerate(self.info_blocks[:5]):
            if i < len(self.customers):
                customer = self.customers[i]
                title.setText(f"Покупатель: {customer.name}")
                content.setText("Информация о покупках")
            else:
                title.setText("Покупатель")
                content.setText("Нет данных")
        
        self.bottom_block.setTitle("Общее о покупателях")
        self.bottom_content.setText(f"Всего покупателей: {len(self.customers)}")

    def calculate_avg_price(self):
        """Вычисляет среднюю цену книг"""
        if not self.books:
            return 0
        return sum(book.price for book in self.books) / len(self.books)

    # Диалоговые окна добавления (остаются без изменений)
    def show_add_book_dialog(self):
        """Диалог добавления книги"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить книгу")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить книгу")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        title_input = QLineEdit()
        form.addRow("Название:", title_input)
        
        author_input = QComboBox()
        author_input.addItems([a.name for a in self.authors])
        form.addRow("Автор:", author_input)
        
        genre_input = QComboBox()
        genre_input.addItems([g.name for g in self.genres])
        form.addRow("Жанр:", genre_input)
        
        price_input = QLineEdit()
        price_input.setValidator(QDoubleValidator())
        form.addRow("Цена:", price_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_new_book(
            title_input.text(),
            author_input.currentText(),
            genre_input.currentText(),
            price_input.text(),
            dialog
        ))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def show_add_to_store_dialog(self):
        """Диалог добавления книги в магазин"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить книгу в библиотеку")
        dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить книгу в библиотеку")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        book_combo = QComboBox()
        book_combo.addItems([b.name for b in self.books])
        form.addRow("Название книги:", book_combo)
        
        store_combo = QComboBox()
        store_combo.addItems([s.name for s in self.stores])
        form.addRow("Название магазина:", store_combo)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_book_to_store(
            book_combo.currentText(),
            store_combo.currentText(),
            dialog
        ))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def show_store_books_dialog(self):
        """Диалог просмотра книг магазина"""
        if not self.stores:
            QMessageBox.warning(self, "Ошибка", "Нет доступных магазинов")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Книги в магазине")
        dialog.setFixedSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        store_combo = QComboBox()
        store_combo.addItems([s.name for s in self.stores])
        layout.addWidget(store_combo)
        
        books_list = QListWidget()
        layout.addWidget(books_list)
        
        def update_books_list():
            store_name = store_combo.currentText()
            store = next((s for s in self.stores if s.name == store_name), None)
            books_list.clear()
            if store and store.library:
                for book in store.library:
                    books_list.addItem(f"{book.name} ({book.author.name})")
        
        store_combo.currentTextChanged.connect(update_books_list)
        update_books_list()
        
        dialog.exec_()

    # Методы добавления новых элементов
    def add_new_book(self, title, author_name, genre_name, price_str, dialog):
        try:
            if not all([title, author_name, genre_name, price_str]):
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
                return
            
            price = float(price_str)
            
            if author_name not in [a.name for a in self.authors]:
                if add_author(self.conn, author_name):
                    self.authors.append(Author(author_name))
            
            if genre_name not in [g.name for g in self.genres]:
                if add_genre(self.conn, genre_name):
                    self.genres.append(Genre(genre_name))
            
            if add_book(self.conn, title, author_name, genre_name, price):
                new_book = Book(title, Author(author_name), Genre(genre_name), price)
                self.books.append(new_book)
                self.update_books_info()
                QMessageBox.information(self, "Успех", "Книга успешно добавлена")
                dialog.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить книгу")
                
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def add_book_to_store(self, book_title, store_name, dialog):
        try:
            book = next((b for b in self.books if b.name == book_title), None)
            store = next((s for s in self.stores if s.name == store_name), None)
            
            if book and store:
                store.add_book_with_conn(self.conn, book)
                self.update_stores_info()
                QMessageBox.information(self, "Успех", "Книга добавлена в магазин")
                dialog.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти книгу или магазин")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def show_add_author_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить автора")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить объект")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название:", name_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_new_author(name_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def add_new_author(self, name, dialog):
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя автора")
            return
        
        if add_author(self.conn, name):
            self.authors.append(Author(name))
            self.update_authors_info()
            QMessageBox.information(self, "Успех", "Автор успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить автора")

    def show_add_genre_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить жанр")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить объект")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название:", name_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_new_genre(name_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def add_new_genre(self, name, dialog):
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название жанра")
            return
        
        if add_genre(self.conn, name):
            self.genres.append(Genre(name))
            self.update_genres_info()
            QMessageBox.information(self, "Успех", "Жанр успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить жанр")

    def show_add_store_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить магазин")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить объект")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название:", name_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_new_store(name_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def add_new_store(self, name, dialog):
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название магазина")
            return
        
        if add_store(self.conn, name):
            self.stores.append(Store(name))
            self.update_stores_info()
            QMessageBox.information(self, "Успех", "Магазин успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить магазин")

    def show_add_customer_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить покупателя")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("# Добавить объект")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название:", name_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_new_customer(name_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

    def add_new_customer(self, name, dialog):
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя покупателя")
            return
        
        if add_customer(self.conn, name):
            self.customers.append(Customer(name))
            self.update_customers_info()
            QMessageBox.information(self, "Успех", "Покупатель успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить покупателя")

    def closeEvent(self, event):
        self.conn.close()
        logger.log_info("Приложение закрыто")
        event.accept()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = BookStoreApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.log_error(f"Критическая ошибка: {str(e)}")
        QMessageBox.critical(None, "Ошибка", f"Не удалось запустить приложение: {str(e)}")
        sys.exit(1)