from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config


class AuthorsInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела, содержащего
    список авторов игры. Попасть можно только из главного меню. Наследуется
    от базового класс BasicWindowInterface. Содержит в себе:
        1. Кнопку выхода в главное меню
        2. Поле с авторами
    """
    
    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки
        super().__init__(
            ui_path=self.config.frontend.ui_files.authors,
            window_size=self.config.frontend.other_frontend.window_size,
            logo_path=self.config.frontend.logo.logo,
            background_path=self.config.frontend.backgrounds.other_background
        )

        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        buttons = {
            self.to_menu_button: self.config.frontend.buttons.exit,
        }
        self.change_icon(buttons)
