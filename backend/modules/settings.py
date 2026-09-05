from frontend.chapters.settings_interface import SettingsInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality

import sqlite3

from PyQt6.QtWidgets import QButtonGroup, QRadioButton, QMainWindow
from PyQt6.QtGui import QIcon
from typing import Callable


class Settings(SettingsInterface, BasicWindowFunctionality):
    """
    Реализует backend часть раздела настроек игры. Унаследован от: SettingsInterface - frontend
    часть раздела настроек игры, BasicWindowFunctionality - класс с базовыми функциями backend
    окна. Реализует загрузку настроек игрока, их изменение и сохранение
    """

    def __init__(self, menu_chapter: QMainWindow):
        # 1. Перезапускам классы родителей и передаем параметры 
        SettingsInterface.__init__(self)
        BasicWindowFunctionality.__init__(self, menu_chapter)

        # 2. Создаем группы радио кнопок
        self.game_difficulty_group = QButtonGroup() # уровень сложности
        self.game_difficulty_group.addButton(self.beginner_radiobutton)
        self.game_difficulty_group.addButton(self.professional_radiobutton)

        self.game_mode_group = QButtonGroup()   # режим игры
        self.game_mode_group.addButton(self.timed_radiobutton)
        self.game_mode_group.addButton(self.casual_radiobutton)

        self.clue_group = QButtonGroup() # подсказки
        self.clue_group.addButton(self.clue_on_radiobutton)
        self.clue_group.addButton(self.clue_off_radiobutton)

        # 3. Подключаем радио кнопки к функциям. Словарь имеет 
            # структуру: {радио_кнопка: функция_вызывающая_при_измении_состоянии_радио_кнопки}

            # список всех кнопок
        radio_buttons = [self.beginner_radiobutton, self.professional_radiobutton, 
                   self.timed_radiobutton, self.casual_radiobutton, 
                   self.clue_on_radiobutton, self.clue_off_radiobutton]

            # для каждой кнопки назначаем функцию, вызывающая при измении состояния
        package = {}
        for radio_button in radio_buttons:
            package[radio_button] = self.radio_button_toggled

        self.connect_radiobuttons_and_funcs(package)


        # 4. Подключаем кнопки к функциями. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.apply_settings_button: self.save_settings,
            self.to_menu_button: self.open_menu_chapter
        }
        self.connect_buttons_and_funcs(buttons)

        # 5. Загружаем настройки пользователя
        self.load_settings()


    def load_settings(self) -> None:
        """
        Метод, координирующий загрузку настроек пользователя. Получает данные и
        применяет эти данные к радио кнопкам
        """
        data = self.load_settings_data()
        self.arrange_checkboxes(data)
        

    def load_settings_data(self) -> list:
        """
        Вспомогательный метод для load_settings, осуществляющий загрузку
        настроек пользователя
        """
        con = sqlite3.connect(self.config.backend.data.storage)
        cur = con.cursor()

        data = cur.execute(
            '''
            SELECT
                game_difficulty, game_mode, clue
            FROM
                settings
            WHERE
                key = 0
            '''
        ).fetchall()
        con.close()

        return data[0]


    def arrange_checkboxes(self, data: list) -> None:
        """
        Вспомогательный метод для load_settings, осуществляющий применение
        настроек к радио кнопкам по переданным данным
        """
        button_group = [
            self.game_difficulty_group,
            self.game_mode_group,
            self.clue_group
        ]

        # проходим по каждой паре радио кнопок
        for i, button_group in enumerate(button_group):
            for button in button_group.buttons(): # проходим по каждой кнопке в группе
                if button.text() == data[i]: # проверяем равенство текста кнопки и текста из настроек
                    button.setChecked(True)
            self.update_group_icons(button_group)   # обновляем иконки радио кнопок из данной группы


    def update_group_icons(self, group: QButtonGroup) -> None:
        """
        Вспомогательный метод для arrange_checkboxes, осуществляющий
        загрузку иконок для переданной группы радио кнопок. Отличается от
        метода radio_button_toggled и позволяет избегать багов с иконками
        """
        checked_button = group.checkedButton()
        for button in group.buttons():
            if button == checked_button: # если кнопка выбрана
                button.setIcon(QIcon(self.config.frontend.radio_buttons.selected_dot))
            else:
                button.setIcon(QIcon(self.config.frontend.radio_buttons.not_selected_dot))


    def radio_button_toggled(self) -> None:
        """
        Метод, вызывающийся при каждом изменении состояния радио кнопки. Изменяет иконки
        радио кнопок, в зависимости от того, какая из них выбрана
        """
         # получаем кнопку, которая вызвала метод
        sender = self.sender()
        # находим другую кнопку из той же группы
        other = [button for button in sender.group().buttons() if sender != button][0]

        if sender.isChecked():
            sender.setIcon(QIcon(self.config.frontend.radio_buttons.selected_dot))
            other.setIcon(QIcon(self.config.frontend.radio_buttons.not_selected_dot))
        else:
            other.setIcon(QIcon(self.config.frontend.radio_buttons.selected_dot))
            sender.setIcon(QIcon(self.config.frontend.radio_buttons.not_selected_dot))


    def save_settings(self) -> None:
        """
        Метод, координирующий загрузку настроек пользователя. Получает
        настройки пользователя и применяет их
        """
        data = self.get_chosen_radio_buttons()
        self.upload_settings_data(data)


    def get_chosen_radio_buttons(self) -> None:
        """
        Вспомогательный метод для save_settings. Осуществляет
        получение выбранных пользователем настроек
        """
        data = (self.game_difficulty_group.checkedButton().text(),
                self.game_mode_group.checkedButton().text(),
                self.clue_group.checkedButton().text())
        return data


    def upload_settings_data(self, data: tuple) -> None:
        """
        Вспомогательный метод для save_settings, осуществляющий
        загрузку в базу данных настроек пользователя
        """
        con = sqlite3.connect(self.config.backend.data.storage)
        cur = con.cursor()

        cur.execute(
            '''
            UPDATE
                settings
            SET
                game_difficulty = ?,
                game_mode = ?,
                clue = ?
            WHERE
                key = 0
            ''', data
        )
        con.commit()
        con.close()


    @staticmethod
    def connect_radiobuttons_and_funcs(radiobuttons: dict[QRadioButton, Callable]) -> None:
        """
        Связывает метод и радио кнопку, по изменению состояния которой будет
        вызван метод
        """
        for radiobutton, func in radiobuttons.items():
            radiobutton.toggled.connect(func)