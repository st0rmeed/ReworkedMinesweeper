from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtGui import QIcon, QBrush, QPixmap, QPalette
from PyQt6 import uic
from PyQt6.QtCore import QSize


class BasicWindowInterface(QMainWindow):
    """
    Базовое класс, на основе которого будут реализовываться frontend части
    остальных окон: MainWindow, Game, Settings, Achievements, Peoples,
    Settings, Leaderboard
    """

    def __init__(self, logo_path, window_size, ui_path, background_path):
        # 1. Инициализируем родительский класс QMainWindow
        super().__init__()

        # 2. По переданным аргументам настраиваем окно: иконка, размер окна и дизайн
        self.setWindowIcon(QIcon(logo_path))        # изменяем иконку окна приложения
        self.setFixedSize(*window_size)     # изменяем размер окна и делаем его фиксированным
        uic.loadUi(ui_path, self)       # загружаем готовый дизайн

        # 3. Устанавливаем фоновую картинку окна
        palette = self.palette()        # получаем текущую палитру           
        pixmap = QPixmap(background_path)       # создаем полотно с картинкой на фоне  
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))     # настраиваем кисть
        self.setPalette(palette)        # устанавливаем палитру


    @staticmethod
    def remove_strict_button_frames(button: QPushButton) -> None:
        """
        Ф-я работает как подфункция для set_icon(). Отвечает за удаление
        строгих границ кнопки. В противном случае, .png картинка будет
        накладываться на видимый серый прямоугольник
        """
        button.setStyleSheet(''' 
            QPushButton {
                border: none; 
                padding: 0px;
                margin: 0px;
            }''')


    def change_icon(self, buttons: dict[QPushButton, str]) -> None:
        """
        Метод отвечает за изменение иконок кнопок. Включает в себе подфункцию
        """
        for button, path in buttons.items():
            button.setIcon(QIcon(path))     # установка иконки
            button.setIconSize(QSize(button.size()))      # изменение размеров иконки
            self.remove_strict_button_frames(button)    # удаление строгих границ кнопки 
