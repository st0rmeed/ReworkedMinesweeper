from frontend.chapters.game_interface import GameInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality

import sqlite3
import csv

import random

from PyQt6.QtWidgets import QPushButton, QInputDialog, QWidget, QMainWindow
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize, QTimer

from data import load_config


class Game(GameInterface, BasicWindowFunctionality):
    config = load_config()
    """
    Реализует backend часть раздела самой игры. Наследуется от двух классов:
    GameInterface (frontend часть самой игры) и BasicWindowFunctionality (класс
    с базовыми backend функциями). Реализует логику загрузки поля, мин, установки
    флага и многое другое
    """

    def __init__(self, menu_chapter: QMainWindow):
        # 1. Перезапускам классы родителей и передаем параметры
        GameInterface.__init__(self)
        BasicWindowFunctionality.__init__(self, menu_chapter)

        # 2. Подключаем кнопки к функциям. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.to_menu_button: self.open_menu_chapter,
            self.install_flag_button: self.change_click_mode,
            self.restart_game_button: self.restart_game,
            self.clue_button: self.show_mine
        }
        self.connect_buttons_and_funcs(buttons)

        # 3. Загружаем конфиг с настройками
        self.config = load_config()

        # 4. Загружаем настройки пользователя: уровень сложности, режим игры, с подсказками или без
        self.settings = self.get_player_settings()
        self.difficulty, self.mode, self.clue = self.settings['difficulty'], self.settings['mode'], self.settings['clue']

        # 5. Выбираем размер поля и количество мин в зависимости от уровня сложности
        levels_and_settings = {
            "Beginner": self.config.backend.game_parameters.field_sizes.beginner,
            "Professional": self.config.backend.game_parameters.field_sizes.professional,
        }
        self.field_size_and_count_mines = levels_and_settings[self.difficulty]
        self.field_size = levels_and_settings[self.difficulty][0]
        self.count_mines = levels_and_settings[self.difficulty][1]

        # 6. Предстартовая подготовка. Инициализируем переменные заранее, чтобы избежать их
        # инициализации в методах
            # поле в двумерном массиве, с отображением клеток, в которых расположены мины
        self.revealed = [
            [False for _ in range(self.field_size)]
                         for _ in range(self.field_size)
        ]

            # поле в двумерном массиве, с отображением клеток, в которых установлен флаг
            # в отличие от flags.positions, необходим для отслеживания состояния всего поля
        self.flags = [
            [False for _ in range(self.field_size)]
            for _ in range(self.field_size)
        ]

            # списки с позициями мин и подсказок
        self.mines_positions, self.clues_positions = [], []

            # список клеток, в которых пользователь верно установил флаг, необходимо для
            # отслеживания достижения
        self.flags_positions = []

            # делает ли пользователь сейчас первый ход, необходимо для инициализации мин
        self.first_move = True

            # пользователь устанавливает флаг на клетке или открывает ее
        self.flag_setting_mode = False

            # выключаем кнопки флага и подсказок (так как в первом ходе еще попросту
            # не инициализированы мины)
        self.install_flag_button.setEnabled(False)
        self.clue_button.setEnabled(False)

            # инициализируем переменные заранее, чтобы избежать их инициализации в методах
        self.count_wins, self.beginner_level = None, None
        self.professional_level, self.count_marked_mines = None, None
        self.width, self.height = None, None
        self.shift, self.x, self.y, self.start_x = None, None, None, None
        self.font_family, self.font_size = None, None
        self.buttons = []

        # 7. Создаем поле
        self.generate_field()

        # 8. Включаем/выключаем кнопку подсказок в зависимости от настроек пользователя
        self.update_clue_button()

        # 9. Подготавливаем таймер
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.time_elapsed = 0


    def generate_field(self) -> None:
        """
        Координирующий метод, осуществляющий загрузку настроек
        для поля, рисующий поле и подключающий клетки поля к
        lambda функции
        """
        self.load_cell_parameters()
        self.draw_field()
        self.connect_field_buttons_and_funcs()


    def load_cell_parameters(self) -> None:
        """
        Вспомогательный метод для generate_field, осуществляющий
        загрузку настроек поля
        """
        difficulty_parameters = {
            "Beginner": self.config.backend.game_parameters.cell_parameters.beginner_cell_parameters,
            "Professional": self.config.backend.game_parameters.cell_parameters.professional_cell_parameters
        }

        self.width, self.height = difficulty_parameters[self.difficulty].cell_size  # габариты клетки
        self.shift = difficulty_parameters[self.difficulty].shift   # интервал между клетками
        self.x, self.y = difficulty_parameters[self.difficulty].start_position  # позиция левой верхней клетки
        self.start_x = self.x

        self.font_family = self.config.backend.game_parameters.font_settings.font_family # шрифт
        self.font_size = self.config.backend.game_parameters.font_settings.font_size # размер шрифта


    def draw_field(self) -> None:
        """
        Вспомогательный метод для generate_field, осуществляющий загрузку
        поля
        """
        for _ in range(self.field_size):
            row_buttons = []     # ряд кнопок
            for _ in range(self.field_size):
                button = QPushButton(self)

                font = QFont(self.font_family, self.font_size)  # изменяем шрифт
                button.setFont(font)

                button.resize(self.width, self.height)  # изменяем геометрию кнопки
                button.move(self.x, self.y)

                row_buttons.append(button)  # добавляем кнопку к остальным кнопкам этого ряда

                button.setIcon(QIcon(self.config.frontend.game_utils.field)) # изменяем иконку
                button.setIconSize(QSize(self.width, self.height))

                # убираем строгий контур кнопок и делаем цвет текста черным в отключенном состоянии
                button.setStyleSheet(
                    """
                            QPushButton {
                                color: black;
                                border: none;
                                padding: 0px;
                                margin: 0px;
                            }
                            QPushButton:disabled {
                                color: black;
                            }
                    """
                )
                self.x += self.shift

            self.y += self.shift
            self.x = self.start_x
            self.buttons.append(row_buttons)   # добавляем ряд кнопок к остальным кнопкам


    def connect_field_buttons_and_funcs(self) -> None:
        """
        Вспомогательный метод для generate_field, осуществляющий соединение
        кнопок поля (игровых клеток) к lambda функции
        """
        for row_index, row in enumerate(self.buttons):
            for col_index, button in enumerate(row):
                button.clicked.connect(
                    lambda _, r=row_index, c=col_index: self.on_button_click(r, c)
                )


    def on_button_click(self, row: int, col: int) -> None:
        """
        Метод, к которому подключена каждая кнопка поля. Координирует множество функций:
        инициализация мин (при первом нажатии), окончание игры (при нажатии
        на клетку с миной или раскрытии всех клеток), открытие клетки (если нету мины),
        установка флага в клетку, поиск количества соседних мин, изменение достижений
        пользователя и многое другое
        """
        button = self.buttons[row][col]

        if self.first_move: # если первый ход
            self.initialize_mines(row, col) # инициализируем мины

            self.first_move = False
            count = self.count_adjacent_mines(row, col) # выводим количество соседних мин
            button.setText(f"{count}")
            button.setEnabled(False)  # отключаем кнопку, чтобы нельзя было нажать еще раз
            button.setIcon(QIcon())
            self.revealed[row][col] = True  # добавляем в список открытых ячеек

            self.install_flag_button.setEnabled(True)   # разрешаем установку флага

            if self.mode == "Casual":
                self.clue_button.setEnabled(True)
                self.label.hide()   # скрываем надпись "Timer: "
            else:
                self.start_timer()

        elif self.flag_setting_mode:    # если у нас выбран режим установки флага
            self.toggle_flag(row, col)

            # если раннее в этой клетки не было флага и в этой клетке есть мина
            if (row, col) in self.mines_positions and (row, col) not in self.flags:
                self.flags_positions.append((row, col))

                if self.mode == "Timed":
                    self.unpack_player_achievements()   # получаем достижения игрока
                    self.count_marked_mines = str(int(self.count_marked_mines) + 1) # добавляем одну отмеченную флагом мину
                    self.update_player_achievements(self.pack_player_achievements()) # обновляем таблицу достижений
                    self.check_is_game_finished()   # проверяем на окончание игры

        elif (row, col) not in self.mines_positions:    # если мы попали в клетку без мины
            count = self.count_adjacent_mines(row, col) # отображаем количество мин рядом с данной клеткой
            button.setText(f"{count}")
            button.setEnabled(False)
            button.setIcon(QIcon())
            self.revealed[row][col] = True
            self.check_is_game_finished()   # проверяем на окончание игры

        elif (row, col) in self.mines_positions:    # если нажали на клетку с миной
            self.stop_timer()
            self.disable_all_buttons()
            self.game_win_over_label.setText("You have lost")
            self.show_mines()


    def check_is_game_finished(self) -> None:
        """
        Проверяет игру на окончание. Сравнивает сумму открытых ячек и количества
        мин с количеством ячеек на поле
        """
        count = self.count_true(self.revealed)

        if count + self.count_mines == self.field_size ** 2:
            self.stop_game()


    def unpack_player_achievements(self) -> None:
        """
        Получает достижения игрока и отображает их
        """
        achievements = self.get_player_achievements()

        for achievement, achievement_item in achievements.items():
            if achievement == self.config.backend.achievements.texts.count_wins_text:
                self.count_wins = achievement_item
            elif achievement == self.config.backend.achievements.texts.complete_beginner_level_text:
                self.beginner_level = achievement_item
            elif achievement == self.config.backend.achievements.texts.complete_professional_level_text:
                self.professional_level = achievement_item
            elif achievement == self.config.backend.achievements.texts.count_marked_mines_text:
                self.count_marked_mines = achievement_item


    def stop_game(self) -> None:
        """
        Осуществляет окончание игры: останавливает таймер, отключает все кнопки,
        выводит текст об окончании, получает никнейм игрока и обновляет его достижения
        """
        self.stop_timer()
        self.disable_all_buttons()

        self.game_win_over_label.setText("You have won!")

        if self.mode == "Timed":    # если игра была на время
            self.update_leaders(self.get_user_name(), self.field_size)  # обновляем таблицу лидеров

            self.unpack_player_achievements()   # получаем достижения пользователя

            self.count_wins = str(int(self.count_wins) + 1) # обновляем достижения пользователя

            if self.difficulty == "Beginner":
                self.beginner_level = "1"
            elif self.difficulty == "Professional":
                self.professional_level = "1"

            self.update_player_achievements(self.pack_player_achievements())    # загружаем обновленные достижения


    def pack_player_achievements(self) -> dict:
        """
        Запаковывает достижения игрока в словарь для дальнейшей загрузки
        в таблицу
        """
        # словарь в формате: {"Название достижения": значение_достижения_пользователя}
        return {
            self.config.backend.achievements.texts.count_wins_text: self.count_wins,
            self.config.backend.achievements.texts.complete_beginner_level_text: self.beginner_level,
            self.config.backend.achievements.texts.complete_professional_level_text: self.professional_level,
            self.config.backend.achievements.texts.count_marked_mines_text: self.count_marked_mines
        }


    def update_leaders(self, name: str, field_size: int) -> None:
        """
        Вносит в таблицу лидеров нового игрока: его никнейм,
        уровень сложности, на котором он завершил игру, и его время прохождения
        """
        con = sqlite3.connect(self.config.backend.data.storage) # подключаемся к таблице
        cur = con.cursor()

        cur.execute(    # обновляем таблицу
            """
        INSERT INTO
            leaders (nickname, time, field_size)
        VALUES
            (?, ?, ?)        
        """,
            (name, self.timer_label.text(), self.difficulty),
        )

        con.commit()    # сохраняем результат
        con.close()


    @staticmethod
    def get_user_name() -> None:
        """
        Осуществляет запуск диалогового окна и получение никнейма
        игрока
        """
        name, ok = QInputDialog.getText(QWidget(), "Input your name", "Your name: ")
        return name.strip() if ok and name.strip() else "Unknown"


    def start_timer(self) -> None:
        """
        Запускает таймер (в игре на время)
        """
        self.timer.start(1000)


    def stop_timer(self) -> None:
        """
        Останвливает таймер (в игре на время)
        """
        self.timer.stop()


    def update_time(self) -> None:
        """
        Обновляет значение таймера: добавляет 1 секунду времени каждую
        секунду (в игре на время)
        """
        self.time_elapsed += 1  # обновляем значение таймера
        self.timer_label.setText(str(self.time_elapsed))   # выводим новое значение таймера


    def reset_timer(self) -> None:
        """
        Перезапускает таймер (в игре на время)
        """
        self.timer.stop() # останавливаем таймер
        self.time_elapsed = 0 # приравниваем значение таймера к нулю
        self.timer_label.setText(str(self.time_elapsed))    # отображаем новое значение таймера


    def get_player_settings(self) -> dict:
        """
        Получает настройки пользователя и возвращает их в удобном формате
        """
        con = sqlite3.connect(self.config.backend.data.storage)
        cur = con.cursor()

        row = cur.execute(
            """
        SELECT
            game_difficulty, game_mode, clue
        FROM
            settings
        WHERE
            key=0
        """
        ).fetchall()[0]

        return {"difficulty": row[0], "mode": row[1], 'clue': row[2]} 


    def get_player_achievements(self) -> dict:
        """
        Получает текущие данные из таблицы достижений пользователя
        """
        with open(self.config.backend.data.achievements, "r", encoding="utf8") as csvfile:
            rows = list(csv.reader(csvfile, delimiter=";", quotechar='"'))
            return {row[0]: row[1] for row in rows}


    def update_player_achievements(self, player_achievements: dict) -> None:
        """
        Обновляет таблицу достижений пользователя, загружая в нее новые данные
        """
        with open(self.config.backend.data.achievements, "w", newline="", encoding="utf8") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows(list([k, v] for k, v in player_achievements.items()))


    def show_mine(self) -> None:
        """
        Отображает на поле случайную мину (вызывается пользователем при помощи
        кнопки подсказки)
        """
        if self.clues_positions:
            coordinates = random.choice(self.clues_positions)
            for item in self.clues_positions:
                if item == coordinates:
                    self.clues_positions.remove(coordinates)
            self.buttons[coordinates[0]][coordinates[1]].setIcon(
                QIcon(self.config.frontend.game_utils.mine)
            )


    def show_mines(self) -> None:
        """
        Отображает все мины на поле (используется в случае проигрыша пользователя)
        """
        for item in self.mines_positions:
            self.buttons[item[0]][item[1]].setIcon(QIcon(self.config.frontend.game_utils.mine))


    @staticmethod
    def count_true(field: list[list]) -> int:
        """
        Осуществляет подсчет количества True в
        в переданном поле. Например, считает количество открытых ячеек
        """
        count = 0
        for row in field: # для каждого ряда
            for cell in row:    # для каждой ячейки в ряду
                if cell:
                    count += 1
        return count


    def restart_game(self) -> None:
        """
        Сбрасывает все настройки для перезапуска игры: отключает кнопки (подсказки и установки
        флага), включает режим первого шага, сбрасывает открытые ячейки и так далее
        """
        self.clue_button.setEnabled(False)
        self.install_flag_button.setEnabled(False)
        self.first_move = True

        self.revealed = [
            [False for _ in range(self.field_size_and_count_mines[0])]
            for _ in range(self.field_size_and_count_mines[0])
        ]
        self.game_win_over_label.setText("")

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].setIcon(QIcon(self.config.frontend.game_utils.field))
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyleSheet(
                        """
                            QPushButton {
                                color: black;
                                border: none;
                                padding: 0px;
                                margin: 0px;
                            }
                            QPushButton:disabled {
                                color: black;
                            }
                        """
                )

        if self.mode == "Timed":
            self.reset_timer()  # сбрасываем таймер

        for row in self.buttons: # включаем каждую кнопку и убираем у нее текст
            for button in row:
                button.setText("")
                button.setEnabled(True)


    def toggle_flag(self, row: int, col: int) -> None:
        """
        Осуществляет установку флага в указанную клетку:
        изменяет иконку клетки, добавляет в список клеток с флагом
        """
        if not self.revealed[row][col]:
            if self.flags[row][col]:
                self.buttons[row][col].setIcon(QIcon(self.config.frontend.game_utils.field))
            else:
                self.buttons[row][col].setIcon(QIcon(self.config.frontend.buttons.flag_on_field))
            self.flags[row][col] = not self.flags[row][col]


    def change_click_mode(self) -> None:
        """
        Осуществляет переключение между двумя режимами: установка флага
        и открытие клетки
        """
        if self.flag_setting_mode:
            self.flag_setting_mode = False
        else:
            self.flag_setting_mode = True


    def disable_all_buttons(self) -> None:
        """
        Делает все кнопки (поля) недоступными для нажатия
        """
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)
                button.setStyleSheet(
                    """
                    QPushButton {
                            color: black;
                            border: none;
                            padding: 0px;
                            margin: 0px;
                        }
                    QPushButton:disabled {
                        color: grey;
                    }
                    """
                )


    def count_adjacent_mines(self, row: int, col: int) -> int | str:
        """
        Осуществляет подсчет количества мин в соседних клетках относительно
        данной
        """
        count = 0

        # цикл проходится по каждому соседнему ряду и каждому соседнему столбцу относительно данной ячейки
        for r in range(max(0, row - 1), min(self.field_size, row + 2)):
            for c in range(max(0, col - 1), min(self.field_size, col + 2)):
                if (r, c) in self.mines_positions:
                    count += 1

        if count == 0:  # если не найдено количество мин, в клетку установится ""
            return ""

        return count    # в противном случае в клетку установится str(count)


    def initialize_mines(self, first_move_row: int, first_move_col: int) -> None:
        """
        Генерирует позиции мин на поле, исключаяя клетку первого хода
        """
        positions = [
            (r, c)
            for r in range(self.field_size)
            for c in range(self.field_size)
            if r != first_move_row or c != first_move_col
        ]


        self.mines_positions = random.sample(positions, self.count_mines) # генерируем count_mines пар row-col
        self.clues_positions = self.mines_positions[:]


    def update_clue_button(self) -> None:
        """
        Включает/отключает кнопку подсказок в зависимости от выбранных
        пользователем настроек
        """
        if self.clue == "Off":
            self.clue_button.hide()
        elif self.clue == "On":
            self.clue_button.show()
