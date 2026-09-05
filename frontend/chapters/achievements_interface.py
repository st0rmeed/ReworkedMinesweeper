from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config

from PyQt6.QtWidgets import QCheckBox

class AchievementsInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела, содержащего достижения
    игрока. В раздел можно попасть только из главного меню. Наследуется
    от базового класса BasicWindowInterface. Содержит в себе:
        1. Кнопку выхода в главное меню
        2. Три чекбокса с достижениями игрока
    """

    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки из конфига
        super().__init__(
            ui_path=self.config.frontend.ui_files.achievements,  # путь до .ui файла
            window_size=self.config.frontend.other_frontend.window_size, # размер окна
            logo_path=self.config.frontend.logo.logo, # логотип окна
            background_path=self.config.frontend.backgrounds.other_background # фоновое изображение
        )

        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        buttons = {
            self.to_menu_button: self.config.frontend.buttons.exit  
        }
        self.change_icon(buttons)


        # 4. Отключаем чек боксы и изменяем их цвет в выключенном состоянии
            # с серого на черный
        checkboxes = [self.count_wins_checkbox,
            self.complete_all_levels_checkbox,
            self.count_marked_mines_checkbox,
        ]
        self.disable_and_change_checkbox_color(checkboxes)

        # 5. Устанавливаем тексты для чек боксов, которые нельзя изначально задать в .ui файле
            # (текст для чекбокса complete_all_levels_checkbox задан в .ui)
        self.count_wins_checkbox.setText(f"Win the game {self.config.backend.achievements.values.count_wins_value} times")
        self.count_marked_mines_checkbox.setText(f'Mark {self.config.backend.achievements.values.count_marked_mines_value} mines')


    @staticmethod
    def disable_and_change_checkbox_color(elements: list[QCheckBox]) -> None:
        """
        Метод изменяет цвет текста чек боксов (на черный) в отключенном состоянии
        и, соответственно, отключает чек боксы
        """
        for element in elements:
            # устанавливаем цвет текста
            element.setStyleSheet('''
                QCheckBox:disabled {
                    color: black; 
                }''')
            # делаем недоступным для нажатия чекбокс
            element.setDisabled(True)