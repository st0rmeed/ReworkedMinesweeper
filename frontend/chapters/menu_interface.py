from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config

class MenuInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела меню игры. Из него можно попасть
    в другие разделы: Achievements, Game, Leaderboard, Authors
    и Settings, а также выйти из игры. Наследуется от базового класса
    BasicWindowInterface. Содержит в себе следующие кнопки:
        1. Выход
        2. Настройки
        3. Таблица лидеров
        4. Сама игра
        5. Достижения
        6. Авторы
    """

    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки из конфига
        super().__init__(
            ui_path=self.config.frontend.ui_files.menu,
            window_size=self.config.frontend.other_frontend.window_size,
            logo_path=self.config.frontend.logo.logo,
            background_path=self.config.frontend.backgrounds.menu_background
        )

        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        self.buttons = {
            self.start_game_button : self.config.frontend.buttons.play_button,
            self.settings_button : self.config.frontend.buttons.settings,
            self.exit_button : self.config.frontend.buttons.exit,
            self.leaderboard_button : self.config.frontend.buttons.leaderboard,
            self.achievements_button : self.config.frontend.buttons.achievements,
            self.authors_button : self.config.frontend.buttons.authors,
        }
        self.change_icon(self.buttons)



