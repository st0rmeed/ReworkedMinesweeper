from typing import Callable, Union
from PyQt6.QtWidgets import QPushButton

from PyQt6.QtWidgets import QMainWindow


class BasicWindowFunctionality:
    """
    Базовый класс, реализующий основные backend методы для всех остальных
    разделов игры: Achievements, Authors, Game, Leaderboard и Settings
    """

    def __init__(self, menu_chapter: Union[QMainWindow, bool] = False):
        if menu_chapter: # если запуск происходит не из раздела Menu
            self.menu_chapter = menu_chapter


    def open_menu_chapter(self) -> None:
        """
        Отвечает за открытие главного меню игры
        """
        frame_geometry = self.frameGeometry()   # сохраняем текущие положение окна
        frame_x, frame_y = frame_geometry.x(), frame_geometry.y()

        self.menu_chapter.open_window(frame_x, frame_y) # открываем меню игры в прежних координатах
        self.close()    # закрываем себя (окно, из которого открывалось окно главного меню)


    def open_window(self, frame_x, frame_y) -> None:
        """
        Реализует открытие и перемещение окна заданные координаты
        """
        self.move(frame_x, frame_y)
        self.show()


    @staticmethod
    def connect_buttons_and_funcs(buttons: dict[QPushButton, Callable]) -> None:
        """
        Соединяет метод и кнопку, по нажатию на которую будет вызываться метод
        """
        for button, func in buttons.items():
            button.clicked.connect(func)


    