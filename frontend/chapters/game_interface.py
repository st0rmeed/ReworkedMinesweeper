from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config


class GameInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела с самой игры. В
    раздел можно попасть только из главного меню. Наследуется от базового
    класса BasicWindowInterface. Содержит в себе кнопки:
        1. Подсказка
        2. Перезапуск игры
        3. Выход в главное меню
        4. Установка флага

    В backend части проекта в этот раздел добавится поле для игры. Оно зависит от уровня
    сложности и не может быть сразу сгенерировано
    """
    
    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки из конфига
        super().__init__(
            ui_path=self.config.frontend.ui_files.game,  # путь до .ui файла
            window_size=self.config.frontend.other_frontend.window_size, # размер окна
            logo_path=self.config.frontend.logo.logo, # логотип окна
            background_path=self.config.frontend.backgrounds.other_background # фоновое изображение
        )

        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        buttons = {
            self.clue_button: self.config.frontend.buttons.clue,
            self.restart_game_button: self.config.frontend.buttons.restart,
            self.install_flag_button: self.config.frontend.buttons.flag,
            self.to_menu_button: self.config.frontend.buttons.exit
        }
        self.change_icon(buttons)