from frontend.chapters.leaderboard_interface import LeaderboardInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality

import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class Leaderboard(LeaderboardInterface, BasicWindowFunctionality):
    """
    Реализует backend часть раздела игры с достижениями игрока. Наследуется от
    двух классов: LeaderboardInterface - интерфейс раздела,
    BasicWindowFunctionality - класс с базовыми backend функциями
    """

    def __init__(self, menu_chapter: QMainWindow):
        # 1. Перезапускам классы родителей и передаем параметры 
        LeaderboardInterface.__init__(self)
        BasicWindowFunctionality.__init__(self, menu_chapter)
        
        # 2. Подключаем кнопки к функциям. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.to_menu_button: self.open_menu_chapter,
            self.update_leaderboard_button: self.update_leaderboard
        }
        self.connect_buttons_and_funcs(buttons)

        # 3. Загружаем таблицу лидеров
        self.update_leaderboard()


    def update_leaderboard(self) -> None:
        """
        Метод, координирующий заполнение таблицы. Получает выбранный уровень
        сложности, загружает данные для данного уровня сложности и заполняет
        таблицу
        """
        selected_text = self.get_selected_level_text()
        data = self.load_leaderboard_data(selected_text)
        self.filling_in_table(data)


    def load_leaderboard_data(self, selected_text) -> list:
        """
        Вспомогательный метод для update_leaderboard, осуществляющий
        получение данных по указанному уровню сложности
        """
        con = sqlite3.connect(self.config.backend.data.storage)
        cur = con.cursor()

        result = cur.execute(
            '''
            SELECT
                nickname, time
            FROM
                leaders
            WHERE
                field_size = ?
            ORDER BY
                time
            ''',
            (selected_text, )
        ).fetchall() 
        con.close()

        return result


    def get_selected_level_text(self) -> str:
        """
        Вспомогательный метод для update_leaderboard, осуществляющий
        получение текущего выбранного уровня сложности
        """
        selected_text = self.choose_field_size.currentText()
        return selected_text
    

    def filling_in_table(self, data: list) -> None:
        """
        Вспомогательный метод для update_leaderboard, осущетсвляющий заполнение
        таблицы лидеров по входным данным
        """
        if not data: # если нету ни одной записи о завершении игры
            self.label_result_of_search.setText(
                'Unforunately, nothing was found'
            )
            self.leaderboard_table_widget.setRowCount(0)

        else:   # если есть хотя бы одна запись о завершении игры
            self.label_result_of_search.setText('')
            self.leaderboard_table_widget.setColumnCount(3)    # количество столбцов
            self.leaderboard_table_widget.setRowCount(len(data))    # количество строк, равное количеству записей

            # заголовки
            self.leaderboard_table_widget.setHorizontalHeaderLabels(
                ["Position", "Nickname", "Time"]
            )
            self.leaderboard_table_widget.verticalHeader().setVisible(False)

            # размеры колонок таблицы лидеров
            self.leaderboard_table_widget.setColumnWidth(0, 80)
            self.leaderboard_table_widget.setColumnWidth(1, 200)
            self.leaderboard_table_widget.setColumnWidth(2, 118)

            # проходимся по каждой записи
            for row_index, elem in enumerate(data):
                # устанавливаем порядковый номер в таблице
                position_item = QTableWidgetItem(str(row_index + 1)) # создаем модель элемента
                position_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # располагаем по центру
                self.leaderboard_table_widget.setItem(row_index, 0, position_item) # устанавливаем элемент в таблицу

                # проходимся по каждому никнейму и соответсвующему ему времени
                for j, val in enumerate(elem):
                    item = QTableWidgetItem(str(val)) # создаем модель элемента
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # располагаем по центру
                    self.leaderboard_table_widget.setItem(row_index, j + 1, item) # устанавливаем элемент в таблицу


                # получаем цвет, зависящий от номера столбца
                color = self.choose_color(row_index)

                # раскрашиваем каждый столбец данной строки
                for col in range(self.leaderboard_table_widget.columnCount()): 
                    self.leaderboard_table_widget.item(row_index, col).setBackground(color) 


    @staticmethod
    def choose_color(row_index: int) -> QColor:
        """
        Вспомогательный метод для filling_in_table, осуществляющий выбор
        цвета в зависимости от номера строки таблицы
        """
        if row_index == 0:
            return QColor(255, 215, 0)
        elif row_index == 1:
            return QColor(192, 192, 192)
        elif row_index == 2:
            return QColor(204, 127, 51)
        else:
            return QColor(255, 255, 255)

