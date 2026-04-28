import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QComboBox, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QHeaderView)

class MovieLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Library")
        self.resize(800, 500)
        self.data_file = "movies.json"
        self.movies = self.load_data()

        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Форма ввода
        self.setup_form()
        # Фильтры
        self.setup_filters()
        # Таблица
        self.setup_table()
        
        self.update_table(self.movies)

    def setup_form(self):
        form_layout = QHBoxLayout()
        self.title_input = QLineEdit(placeholderText="Название")
        self.genre_input = QLineEdit(placeholderText="Жанр")
        self.year_input = QLineEdit(placeholderText="Год")
        self.rating_input = QLineEdit(placeholderText="Рейтинг (0-10)")
        
        add_btn = QPushButton("Добавить фильм")
        add_btn.clicked.connect(self.add_movie)

        for w in [self.title_input, self.genre_input, self.year_input, self.rating_input, add_btn]:
            form_layout.addWidget(w)
        self.layout.addLayout(form_layout)

    def setup_filters(self):
        filter_layout = QHBoxLayout()
        self.filter_genre = QLineEdit(placeholderText="Фильтр по жанру")
        self.filter_genre.textChanged.connect(self.apply_filters)
        
        self.filter_year = QLineEdit(placeholderText="Фильтр по году")
        self.filter_year.textChanged.connect(self.apply_filters)

        filter_layout.addWidget(QLabel("Поиск:"))
        filter_layout.addWidget(self.filter_genre)
        filter_layout.addWidget(self.filter_year)
        self.layout.addLayout(filter_layout)

    def setup_table(self):
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Название", "Жанр", "Год", "Рейтинг"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

    def add_movie(self):
        title = self.title_input.text().strip()
        genre = self.genre_input.text().strip()
        year = self.year_input.text().strip()
        rating = self.rating_input.text().strip()

        # Валидация
        if not (title and genre and year and rating):
            return QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
        
        if not year.isdigit():
            return QMessageBox.warning(self, "Ошибка", "Год должен быть числом!")
        
        try:
            r = float(rating)
            if not (0 <= r <= 10): raise ValueError
        except ValueError:
            return QMessageBox.warning(self, "Ошибка", "Рейтинг должен быть от 0 до 10!")

        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(movie)
        self.save_data()
        self.apply_filters()
        
        # Очистка полей
        self.title_input.clear()
        self.genre_input.clear()
        self.year_input.clear()
        self.rating_input.clear()

    def apply_filters(self):
        g_filter = self.filter_genre.text().lower()
        y_filter = self.filter_year.text()

        filtered = [
            m for m in self.movies 
            if g_filter in m['genre'].lower() and y_filter in m['year']
        ]
        self.update_table(filtered)

    def update_table(self, data_list):
        self.table.setRowCount(0)
        for movie in data_list:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(movie['title']))
            self.table.setItem(row, 1, QTableWidgetItem(movie['genre']))
            self.table.setItem(row, 2, QTableWidgetItem(movie['year']))
            self.table.setItem(row, 3, QTableWidgetItem(movie['rating']))

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieLibrary()
    window.show()
    sys.exit(app.exec())
