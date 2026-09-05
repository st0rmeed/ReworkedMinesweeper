from frontend.chapters.menu_interface import MenuInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality
from backend.modules.achievements import Achievements
from backend.modules.authors import Authors
from backend.modules.game import Game
from backend.modules.leaderboard import Leaderboard
from backend.modules.settings import Settings

from PyQt6.QtWidgets import QMessageBox

import sys


class Menu(MenuInterface, BasicWindowFunctionality):
    """
    Реализует backend часть раздела меню. Наследуется от двух классов:
    MenuInterface - frontend часть раздела меню, BasicWindowFunctionality - базовый
    backend функционал. Осуществляет связь между всеми разделами игры
    """

    def __init__(self):
        # 1. Перезапускам классы родителей и передаем параметры
        MenuInterface.__init__(self)
        BasicWindowFunctionality.__init__(self)

        # 2. Подключаем кнопки к функциям. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.settings_button: self.open_settings_chapter,
            self.leaderboard_button: self.open_leaderboard_chapter,
            self.start_game_button: self.open_game_chapter,
            self.achievements_button: self.open_achievements_chapter,
            self.exit_button: self.confirm_exit,
            self.authors_button: self.open_authors_chapter
        }
        self.connect_buttons_and_funcs(buttons)


    def open_settings_chapter(self) -> None:
        """
        Метод, позволяющий открыть раздел настроек
        """
        frame_geometry = self.frameGeometry()   # получаем положение окна
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.hide() # скрываем, но не закрываем главное меню, чтобы не было дубликатов!

        self.settings_chapter = Settings(menu_chapter=self) # создаем экземпляр окна настроек, передаем 
        # ссылку на себя для возврата в главное меню и предотвращения появления дубликатов
        self.settings_chapter.open_window(frame_x, frame_y) # открываем окно настроек с заданным положением


    def open_leaderboard_chapter(self) -> None:
        """
        Метод, позволяющий открыть раздел таблицы лидеров
        """
        frame_geometry = self.frameGeometry()
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.hide() # скрываем, но не закрываем главное меню, чтобы не было дубликатов!

        self.leaderboard_chapter = Leaderboard(menu_chapter=self)
        self.leaderboard_chapter.open_window(frame_x, frame_y)


    def open_game_chapter(self) -> None:
        """
        Метод, позволяющий открыть раздел самой игры
        """
        frame_geometry = self.frameGeometry()
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.hide()

        self.game_chapter = Game(menu_chapter=self)
        self.game_chapter.open_window(frame_x, frame_y)


    def open_achievements_chapter(self) -> None:
        """
        Метод, позволяющий открыть раздел достижений
        """
        frame_geometry = self.frameGeometry()
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.hide()

        self.achievements_chapter = Achievements(menu_chapter=self)
        self.achievements_chapter.open_window(frame_x, frame_y)


    def open_authors_chapter(self) -> None:
        """
        Метод, позволяющий открыть раздел создателей игры
        """
        frame_geometry = self.frameGeometry()
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.hide()
        
        self.authors_chapter = Authors(menu_chapter=self)
        self.authors_chapter.open_window(frame_x, frame_y)


    def confirm_exit(self) -> None:
        """
        Метод, осуществляющий возможность выхода из игры с помощью диалогового окна
        """
        reply = QMessageBox.question(
            self,
            "Подтверждение",    # заголовок окна
            "Вы уверены, что желаете выйти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # кнопки "Да" и "Нет"
            QMessageBox.StandardButton.No,  # кнопка "Нет" по умолчанию
        )

        if reply == QMessageBox.StandardButton.Yes:
            sys.exit() # завершает работу игры