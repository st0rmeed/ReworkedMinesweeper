from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config


class LeaderboardInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела с лидерами. В
    раздел можно попасть только из главного меню. Наследуется от базового
    BasicWindowInterface. Содержит в себе:
        1. Кнопку обновления таблицы лидеров
        2. Таблицу лидеров
        3. Выпадающий список с выбором уровня сложности (Beginner/Professional)
        4. Кнопку выхода в главное меню
    """
    
    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки из конфига
        super().__init__(
            ui_path=self.config.frontend.ui_files.leaderboard, # путь до .ui файла
            window_size=self.config.frontend.other_frontend.window_size, # размер окна
            logo_path=self.config.frontend.logo.logo, # логотип окна
            background_path=self.config.frontend.backgrounds.other_background # фоновое изображение
        )

        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        buttons = {
            self.to_menu_button: self.config.frontend.buttons.exit,
            self.update_leaderboard_button: self.config.frontend.buttons.update_table
        }
        self.change_icon(buttons)

        # 4. В выпадающий список добавляем два уровня сложности
        self.choose_field_size.addItem("Beginner")
        self.choose_field_size.addItem("Professional")
