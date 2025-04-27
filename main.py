import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QListWidget,
    QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QMessageBox, QFrame, QListWidgetItem
)
from PyQt5.QtGui import QDoubleValidator, QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QLibraryInfo

from classes import Book, Author, Genre, Store, Customer
import database
from logger import logger

class BookStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление книжным магазином")
        self.setFixedSize(800, 450)
        
        # Подключение к базе данных
        self.conn = sqlite3.connect('books.db')
        database.create_tables(self.conn)
        
        # Загрузка данных
        self.load_data()
        
        # Инициализация текущей категории и индекса
        self.current_category = None
        self.current_index = 0
        
        # Создаем зеленую иконку для списка
        self.green_icon = self.create_green_icon()
        
        # Настройка интерфейса
        self.setup_ui()
        
        # Показать стартовую страницу (книги)
        self.show_category("books")

    def create_green_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPixmap(16, 16)
        pixmap.fill(QColor(0, 128, 0))  # Зеленый цвет
        icon = QIcon(pixmap)
        return icon

    def load_data(self):
        """Загрузка данных из базы данных"""
        self.books = []
        self.authors = []
        self.genres = []
        self.stores = []
        self.customers = []
        
        cur = self.conn.cursor()
        
        # Загрузка авторов
        cur.execute("SELECT name FROM authors")
        self.authors = [Author(row[0]) for row in cur.fetchall()]
        
        # Загрузка жанров
        cur.execute("SELECT name FROM genres")
        self.genres = [Genre(row[0]) for row in cur.fetchall()]
        
        # Загрузка книг
        cur.execute("SELECT title, author, genre, price FROM books")
        self.books = [Book(row[0], Author(row[1]), Genre(row[2]), row[3]) for row in cur.fetchall()]
        
        # Загрузка магазинов
        cur.execute("SELECT name FROM stores")
        for row in cur.fetchall():
            store = Store(row[0])
            # Загрузка книг для магазина
            cur.execute("SELECT book_title FROM store_books WHERE store_name = ?", (row[0],))
            for book_row in cur.fetchall():
                book = next((b for b in self.books if b.name == book_row[0]), None)
                if book:
                    store.library.append(book)
            self.stores.append(store)
        
        # Загрузка покупателей
        cur.execute("SELECT name FROM customers")
        self.customers = [Customer(row[0]) for row in cur.fetchall()]

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(2)
        
        # Верхняя панель навигации (выровнена по правому краю)
        self.setup_top_navigation(main_layout)
        
        # Центральная область с информационными блоками
        self.setup_info_blocks(main_layout)
        
        # Панель кнопок добавления (по центру)
        self.setup_action_buttons(main_layout)
        
        # Установка стилей
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
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
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                margin: 6px;
                color: #333;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #a0c0a0;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #a0c0a0;
                border-radius: 4px;
                background-color: white;
            }
        """)

    def setup_top_navigation(self, main_layout):
        """Настройка верхней панели навигации (выровнена по правому краю)"""
        nav_frame = QFrame()
        nav_frame.setStyleSheet("background-color: green;")  # Зеленый фон блока
        nav_frame.setFixedHeight(int(35 * 1.6))  # Высота блока 160% от высоты кнопки
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(2)
        
        # Добавляем растягивающий элемент слева
        nav_layout.addStretch()
        
        # Кнопки навигации
        self.books_btn = QPushButton("Книги")
        self.authors_btn = QPushButton("Авторы")
        self.genres_btn = QPushButton("Жанры")
        self.stores_btn = QPushButton("Магазины")
        self.customers_btn = QPushButton("Покупатели")
        
        # Установка размера и стиля
        for btn in [self.books_btn, self.authors_btn, self.genres_btn, 
                   self.stores_btn, self.customers_btn]:
            btn.setFixedSize(int(100 * 1.1), 35)  # Кнопки на 10% шире
            btn.setFont(QFont("Arial", 10))
            btn.setStyleSheet(
                "background-color: #4B0000;"  # Тёмно-багровый фон кнопок
                "color: white;"               # Белый цвет текста
                "border-radius: 6px;"         # Немного закругленные углы
            )
        
        # Подключение обработчиков
        self.books_btn.clicked.connect(lambda: self.show_category("books"))
        self.authors_btn.clicked.connect(lambda: self.show_category("authors"))
        self.genres_btn.clicked.connect(lambda: self.show_category("genres"))
        self.stores_btn.clicked.connect(lambda: self.show_category("stores"))
        self.customers_btn.clicked.connect(lambda: self.show_category("customers"))
        
        # Добавление в layout
        nav_layout.addWidget(self.books_btn)
        nav_layout.addWidget(self.authors_btn)
        nav_layout.addWidget(self.genres_btn)
        nav_layout.addWidget(self.stores_btn)
        nav_layout.addWidget(self.customers_btn)
        
        main_layout.addWidget(nav_frame)

    def setup_info_blocks(self, main_layout):
        """Настройка информационных блоков с кнопками навигации"""
        self.info_blocks = []
        
        # Кнопка "назад" слева
        self.prev_btn = QPushButton("←")
        self.prev_btn.setFixedSize(60, 60)
        self.prev_btn.setFont(QFont("Arial", 24))
        self.prev_btn.setStyleSheet("padding: 10px;")  # Внутренний отступ кнопки
        self.prev_btn.clicked.connect(lambda: self.navigate_blocks(-1, 5))
        
        # Кнопка "вперед" справа
        self.next_btn = QPushButton("→")
        self.next_btn.setFixedSize(60, 60)
        self.next_btn.setFont(QFont("Arial", 24))
        self.next_btn.setStyleSheet("padding: 10px;")  # Внутренний отступ кнопки
        self.next_btn.clicked.connect(lambda: self.navigate_blocks(1, 5))
        
        # Вертикальный layout для двух рядов блоков
        blocks_layout = QVBoxLayout()
        blocks_layout.setSpacing(1)  # Уменьшенное расстояние между рядами
        
        # Первый ряд: 3 блока информации
        top_row = QHBoxLayout()
        top_row.setSpacing(5)
        
        # Создаем 3 блока для верхнего ряда
        for i in range(3):
            block = QGroupBox()
            block.setFixedSize(200, 160)
            block_layout = QVBoxLayout(block)
            
            title = QLabel()
            title.setFont(QFont("Arial", 12, QFont.Bold))
            block_layout.addWidget(title)
            
            content = QLabel()
            content.setFont(QFont("Arial", 10))
            content.setWordWrap(True)
            block_layout.addWidget(content)
            
            self.info_blocks.append((block, title, content))
            top_row.addWidget(block)
        
        # Второй ряд: 1 блок слева, общая информация по центру, 1 блок справа
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(1)
        
        # Создаем левый блок нижнего ряда
        left_block = QGroupBox()
        left_block.setFixedSize(200, 140)
        left_block_layout = QVBoxLayout(left_block)
        
        self.left_block_title = QLabel()
        self.left_block_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_block_layout.addWidget(self.left_block_title)
        
        self.left_block_content = QLabel()
        self.left_block_content.setFont(QFont("Arial", 10))
        self.left_block_content.setWordWrap(True)
        left_block_layout.addWidget(self.left_block_content)
        
        self.info_blocks.append((left_block, self.left_block_title, self.left_block_content))
        bottom_row.addWidget(left_block)
        
        # Центральный блок (общая информация)
        self.center_block = QGroupBox()
        self.center_block.setFixedSize(200, 140)
        center_block_layout = QVBoxLayout(self.center_block)
        
        self.center_block_title = QLabel("Общая информация")
        self.center_block_title.setFont(QFont("Arial", 12, QFont.Bold))
        center_block_layout.addWidget(self.center_block_title)
        
        self.center_block_content = QLabel()
        self.center_block_content.setFont(QFont("Arial", 10))
        self.center_block_content.setWordWrap(True)
        center_block_layout.addWidget(self.center_block_content)
        
        bottom_row.addWidget(self.center_block)
        
        # Создаем правый блок нижнего ряда
        right_block = QGroupBox()
        right_block.setFixedSize(200, 140)
        right_block_layout = QVBoxLayout(right_block)
        
        self.right_block_title = QLabel()
        self.right_block_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_block_layout.addWidget(self.right_block_title)
        
        self.right_block_content = QLabel()
        self.right_block_content.setFont(QFont("Arial", 10))
        self.right_block_content.setWordWrap(True)
        right_block_layout.addWidget(self.right_block_content)
        
        self.info_blocks.append((right_block, self.right_block_title, self.right_block_content))
        bottom_row.addWidget(right_block)
        
        # Создаем основной горизонтальный layout для кнопок и двух рядов
        main_blocks_layout = QHBoxLayout()
        main_blocks_layout.setSpacing(5)
        
        # Добавляем кнопку "назад" слева
        main_blocks_layout.addWidget(self.prev_btn, alignment=Qt.AlignVCenter)
        
        # Создаем вертикальный layout для двух рядов
        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(1)
        rows_layout.addLayout(top_row)
        rows_layout.addLayout(bottom_row)
        
        main_blocks_layout.addLayout(rows_layout)
        
        # Добавляем кнопку "вперед" справа
        main_blocks_layout.addWidget(self.next_btn, alignment=Qt.AlignVCenter)
        
        blocks_layout.addLayout(main_blocks_layout)
        
        # Добавляем blocks_layout в основной layout для отображения
        main_layout.addLayout(blocks_layout)

    def navigate_blocks(self, direction, block_index):
        """Навигация по блокам информации"""
        logger.log_info(f"navigate_blocks called with direction={direction}, block_index={block_index}, current_index={self.current_index}, current_category={self.current_category}")
        self.current_index += direction
        
        # Проверка границ
        items = []
        if self.current_category == "books":
            items = self.books
        elif self.current_category == "authors":
            items = self.authors
        elif self.current_category == "genres":
            items = self.genres
        elif self.current_category == "stores":
            items = self.stores
        elif self.current_category == "customers":
            items = self.customers
        
        logger.log_info(f"Items count: {len(items)} before boundary check, current_index: {self.current_index}")
        if self.current_index < 0:
            self.current_index = 0
        max_index = max(0, len(items) - block_index)
        if self.current_index > max_index:
            self.current_index = max_index
        logger.log_info(f"Adjusted current_index: {self.current_index}")
        
        self.update_info_blocks()

    def setup_action_buttons(self, main_layout):
        """Настройка кнопок действий (по центру)"""
        action_frame = QFrame()
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(2)
        
        # Добавляем растягивающие элементы с обеих сторон
        action_layout.addStretch()
        
        # Основная кнопка добавления
        self.add_btn = QPushButton()
        self.add_btn.setFixedSize(180, 40)
        self.add_btn.setFont(QFont("Arial", 12))
        
        # Кнопка "Добавить книгу в магазин"
        self.add_to_store_btn = QPushButton("Добавить книгу в магазин")
        self.add_to_store_btn.setFixedSize(200, 40)
        self.add_to_store_btn.setFont(QFont("Arial", 12))
        self.add_to_store_btn.clicked.connect(self.show_add_to_store_dialog)
        self.add_to_store_btn.hide()
        
        # Кнопка "Показать библиотеку"
        self.show_store_btn = QPushButton("Показать библиотеку")
        self.show_store_btn.setFixedSize(200, 40)
        self.show_store_btn.setFont(QFont("Arial", 12))
        self.show_store_btn.clicked.connect(self.show_store_books_dialog)
        self.show_store_btn.hide()
        
        action_layout.addWidget(self.add_btn)
        action_layout.addWidget(self.add_to_store_btn)
        action_layout.addWidget(self.show_store_btn)
        
        # Добавляем растягивающий элемент с другой стороны
        action_layout.addStretch()
        
        main_layout.addWidget(action_frame)

    def show_category(self, category):
        """Отображение выбранной категории"""
        self.current_category = category
        self.current_index = 0
        
        # Скрываем специальные кнопки
        self.add_to_store_btn.hide()
        self.show_store_btn.hide()
        
        # Отключаем предыдущие соединения кнопки добавления
        try:
            self.add_btn.clicked.disconnect()
        except TypeError:
            pass
        
        # Устанавливаем текст кнопки добавления
        if category == "books":
            self.add_btn.setText("Добавить книгу")
            self.add_btn.clicked.connect(self.show_add_book_dialog)
            self.add_to_store_btn.show()
        elif category == "authors":
            self.add_btn.setText("Добавить автора")
            self.add_btn.clicked.connect(self.show_add_author_dialog)
        elif category == "genres":
            self.add_btn.setText("Добавить жанр")
            self.add_btn.clicked.connect(self.show_add_genre_dialog)
        elif category == "stores":
            self.add_btn.setText("Добавить магазин")
            self.add_btn.clicked.connect(self.show_add_store_dialog)
            self.show_store_btn.show()
        elif category == "customers":
            self.add_btn.setText("Добавить покупателя")
            self.add_btn.clicked.connect(self.show_add_customer_dialog)
        
        # Обновляем информацию
        self.update_info_blocks()

    def update_info_blocks(self):
        """Обновление информационных блоков"""
        logger.log_info(f"update_info_blocks called with current_index={self.current_index}, current_category={self.current_category}")
        items = []
        if self.current_category == "books":
            items = self.books
        elif self.current_category == "authors":
            items = self.authors
        elif self.current_category == "genres":
            items = self.genres
        elif self.current_category == "stores":
            items = self.stores
        elif self.current_category == "customers":
            items = self.customers
        
        logger.log_info(f"Items count: {len(items)}")
        # Обновляем первые 3 блока
        for i in range(3):
            idx = self.current_index + i
            logger.log_info(f"Updating block {i} with idx={idx}")
            block, title, content = self.info_blocks[i]
            
            if idx < len(items):
                item = items[idx]
                if self.current_category == "books":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Автор: {item.author.name}\nЖанр: {item.genre.name}\nЦена: {item.price}р")
                elif self.current_category == "authors":
                    book_count = sum(1 for book in self.books if book.author.name == item.name)
                    genres = set(book.genre.name for book in self.books if book.author.name == item.name)
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {book_count}\nЖанры: {', '.join(genres) if genres else 'нет'}")
                elif self.current_category == "genres":
                    book_count = sum(1 for book in self.books if book.genre.name == item.name)
                    authors = set(book.author.name for book in self.books if book.genre.name == item.name)
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {book_count}\nАвторы: {', '.join(authors) if authors else 'нет'}")
                elif self.current_category == "stores":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {len(item.library)}")
                elif self.current_category == "customers":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText("Информация о покупках")
            else:
                title.setText(self.current_category.capitalize())
                title.setAlignment(Qt.AlignCenter)
                content.setText("Нет данных")
        
        # Обновляем левый и правый блоки (4 и 5 элементы)
        for i in range(2):
            idx = self.current_index + 3 + i
            logger.log_info(f"Updating side block {i} with idx={idx}")
            block, title, content = self.info_blocks[3 + i]
            
            if idx < len(items):
                item = items[idx]
                if self.current_category == "books":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Автор: {item.author.name}\nЖанр: {item.genre.name}\nЦена: {item.price}р")
                elif self.current_category == "authors":
                    book_count = sum(1 for book in self.books if book.author.name == item.name)
                    genres = set(book.genre.name for book in self.books if book.author.name == item.name)
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {book_count}\nЖанры: {', '.join(genres) if genres else 'нет'}")
                elif self.current_category == "genres":
                    book_count = sum(1 for book in self.books if book.genre.name == item.name)
                    authors = set(book.author.name for book in self.books if book.genre.name == item.name)
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {book_count}\nАвторы: {', '.join(authors) if authors else 'нет'}")
                elif self.current_category == "stores":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText(f"Книг: {len(item.library)}")
                elif self.current_category == "customers":
                    title.setText(item.name)
                    title.setAlignment(Qt.AlignCenter)
                    content.setText("Информация о покупках")
            else:
                title.setText(self.current_category.capitalize())
                title.setAlignment(Qt.AlignCenter)
                content.setText("Нет данных")
        
        # Обновляем центральный блок с общей информацией
        if self.current_category == "books":
            avg_price = sum(book.price for book in self.books) / len(self.books) if self.books else 0
            self.center_block_content.setText(f"Всего книг: {len(self.books)}\nСредняя цена: {avg_price:.2f}р")
        elif self.current_category == "authors":
            avg_books = len(self.books) / len(self.authors) if self.authors else 0
            self.center_block_content.setText(f"Всего авторов: {len(self.authors)}\nСреднее книг на автора: {avg_books:.1f}")
        elif self.current_category == "genres":
            avg_books = len(self.books) / len(self.genres) if self.genres else 0
            self.center_block_content.setText(f"Всего жанров: {len(self.genres)}\nСреднее книг на жанр: {avg_books:.1f}")
        elif self.current_category == "stores":
            total_books = sum(len(store.library) for store in self.stores)
            self.center_block_content.setText(f"Всего магазинов: {len(self.stores)}\nВсего книг в магазинах: {total_books}")
        elif self.current_category == "customers":
            self.center_block_content.setText(f"Всего покупателей: {len(self.customers)}")

    def show_add_book_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить книгу")
        dialog.setFixedSize(400, 250)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить книгу")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
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

    def add_new_book(self, title, author_name, genre_name, price_str, dialog):
        try:
            if not all([title, author_name, genre_name, price_str]):
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
                return
            
            price = float(price_str)
            
            if author_name not in [a.name for a in self.authors]:
                if database.add_author(self.conn, author_name):
                    self.authors.append(Author(author_name))
            
            if genre_name not in [g.name for g in self.genres]:
                if database.add_genre(self.conn, genre_name):
                    self.genres.append(Genre(genre_name))
            
            if database.add_book(self.conn, title, author_name, genre_name, price):
                new_book = Book(title, Author(author_name), Genre(genre_name), price)
                self.books.append(new_book)
                self.update_info_blocks()
                QMessageBox.information(self, "Успех", "Книга успешно добавлена")
                dialog.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить книгу")
                
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def show_add_to_store_dialog(self):
        """Диалог добавления книги в магазин"""
        if not self.books or not self.stores:
            QMessageBox.warning(self, "Ошибка", "Нет доступных книг или магазинов")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить книгу в магазин")
        dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить книгу в библиотеку")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form = QFormLayout()
        
        book_combo = QComboBox()
        # Remove icon setting, just add items
        book_combo.clear()
        for b in self.books:
            book_combo.addItem(b.name)
        # Add custom style sheet for green dropdown arrow
        book_combo.setStyleSheet("""
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(icons/green_down_arrow.png);
                width: 18px;
                height: 18px;
            }
        """)
        form.addRow("Название книги:", book_combo)
        
        store_combo = QComboBox()
        store_combo.addItems([s.name for s in self.stores])
        # Add same style sheet for green dropdown arrow
        store_combo.setStyleSheet("""
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(icons/green_down_arrow.png);
                width: 18px;
                height: 18px;
            }
        """)
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

    def add_book_to_store(self, book_title, store_name, dialog):
        """Добавление книги в магазин"""
        try:
            book = next((b for b in self.books if b.name == book_title), None)
            store = next((s for s in self.stores if s.name == store_name), None)
            
            if book and store:
                if database.add_book_to_store(self.conn, store.name, book.name):
                    store.add_book(book)
                    self.update_info_blocks()
                    QMessageBox.information(self, "Успех", "Книга добавлена в магазин")
                    dialog.accept()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить книгу в магазин")
            else:
                QMessageBox.warning(self, "Ошибка", "Книга или магазин не найдены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def show_store_books_dialog(self):
        """Диалог просмотра книг в магазине"""
        if not self.stores:
            QMessageBox.warning(self, "Ошибка", "Нет доступных магазинов")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Книги в магазине")
        dialog.setFixedSize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        store_combo = QComboBox()
        store_combo.addItems([s.name for s in self.stores])
        # Add custom style sheet for green dropdown arrow
        store_combo.setStyleSheet("""
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(icons/green_down_arrow.png);
                width: 18px;
                height: 18px;
            }
        """)
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

    def show_add_author_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить автора")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить автора")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Имя автора:", name_input)
        
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
        
        if database.add_author(self.conn, name):
            self.authors.append(Author(name))
            self.update_info_blocks()
            QMessageBox.information(self, "Успех", "Автор успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить автора")

    def show_add_genre_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить жанр")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить жанр")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название жанра:", name_input)
        
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
        
        if database.add_genre(self.conn, name):
            self.genres.append(Genre(name))
            self.update_info_blocks()
            QMessageBox.information(self, "Успех", "Жанр успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить жанр")

    def show_add_store_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить магазин")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить магазин")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Название магазина:", name_input)
        
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
        
        if database.add_store(self.conn, name):
            self.stores.append(Store(name))
            self.update_info_blocks()
            QMessageBox.information(self, "Успех", "Магазин успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить магазин")

    def show_add_customer_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить покупателя")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        title_label = QLabel("# Добавить покупателя")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        form.addRow("Имя покупателя:", name_input)
        
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
        
        if database.add_customer(self.conn, name):
            self.customers.append(Customer(name))
            self.update_info_blocks()
            QMessageBox.information(self, "Успех", "Покупатель успешно добавлен")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить покупателя")

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    # Убедимся, что используем правильный API
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = QLibraryInfo.location(QLibraryInfo.PluginsPath)
    
    try:
        window = BookStoreApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Не удалось запустить приложение: {str(e)}")
        sys.exit(1)
