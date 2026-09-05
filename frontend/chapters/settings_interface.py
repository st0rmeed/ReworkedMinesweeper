from frontend.chapters.basic_window_of_interface import BasicWindowInterface

from data import load_config

from PyQt6.QtWidgets import QRadioButton

class SettingsInterface(BasicWindowInterface):
    """
    Реализует frontend часть раздела настроек игрока. В раздел можно попасть
    только из главного меню. Класс наследуется от базового BasicWindowInterface.
    Содержит в себе:
        1. Кнопку выхода в главное меню
        2. Кнопку применения настроек
        3. Три группы чек боксов для режимов игры:
            a) уровень сложности игры
            б) с подсказками или без
            в) на время или обычный
    """

    def __init__(self):
        # 1. Загружаем конфиг с настройками
        self.config = load_config()

        # 2. Инициализируем родительский класс и передаем в него заготовки из конфига
        super().__init__(
            ui_path=self.config.frontend.ui_files.settings,  # путь до .ui файла
            window_size=self.config.frontend.other_frontend.window_size, # размер окна
            logo_path=self.config.frontend.logo.logo, # логотип окна
            background_path=self.config.frontend.backgrounds.other_background   # фоновое изображение
        )


        # 3. Изменяем иконки кнопок: устанавливаем новые, изменяем размер иконок и удаляем
            # строгие границы. Словарь в формате: {кнопка: путь_до_иконки_кнопки}
        buttons = {
            self.apply_settings_button: self.config.frontend.buttons.apply,
            self.to_menu_button: self.config.frontend.buttons.exit
        }
        self.change_icon(buttons)


        # 4. Отключаем стандартные иконки радио кнопок для того,
        #   чтобы в дальнейшем использовать кастомные
        radio_buttons = [self.beginner_radiobutton, self.professional_radiobutton,
                         self.timed_radiobutton, self.casual_radiobutton,
                         self.clue_on_radiobutton, self.clue_off_radiobutton]
        self.remove_radio_button_indicator(radio_buttons)


    @staticmethod
    def remove_radio_button_indicator(elements: list[QRadioButton]) -> None:
        """
        Метод удаляет у радио кнопок индикатор выбора, позволяя
        сделать иконку, наложенную на радио кнопку, видимой
        """
        for element in elements:
            element.setStyleSheet('''
                QRadioButton::indicator { 
                    width: 0px; 
                    height: 0px; 
                    image: none;
                }''')



