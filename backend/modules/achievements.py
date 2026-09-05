from frontend.chapters.achievements_interface import AchievementsInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality

import csv

from PyQt6.QtWidgets import QMainWindow


class Achievements(AchievementsInterface, BasicWindowFunctionality):
    """
    Реализует backend часть раздела с достижениями игрока. Наследуется
    от класса с базовыми функциями BasicWindowFunctionality и от класса с интерфейсом
    раздела AchievementsInterface. Реализует логику загрузки и показа достижений
    """

    def __init__(self, menu_chapter: QMainWindow):
        # 1. Перезапускам классы родителей и передаем параметры
        AchievementsInterface.__init__(self)
        BasicWindowFunctionality.__init__(self, menu_chapter)

        # 2. Подключаем кнопки к функциям. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.to_menu_button: self.open_menu_chapter
        }
        self.connect_buttons_and_funcs(buttons)

        # 3. Загружаем достижения игрока
        self.load_achievements()

    
    def load_achievements(self) -> None:
        """
        Метод-координатор процесса загрузки достижений. Получает данные
        и запускает их процессинг
        """
        data = self.load_achievements_data()
        self.process_achievements(data)


    def load_achievements_data(self) -> dict:
        """
        Является вспомогательным для метода load_achievements. Осуществляет
        загрузку данных
        """
        with open(self.config.backend.data.achievements, 'r', encoding='utf8') as csv_file:
            data = {row[0]: row[1] for row in csv.reader(csv_file, delimiter=';')}
            return data


    def get_achievements_config(self) -> dict:
        """
        Вспомогательный метод для load_achievements. Осуществляет загрузку конфига
        для каждого из параметров
        """
        return {
            'count_wins': {
                'text': self.config.backend.achievements.texts.count_wins_text,
                'value': self.config.backend.achievements.values.count_wins_value,
                'checkbox': self.count_wins_checkbox
            },
            'marked_mines': {
                'text': self.config.backend.achievements.texts.count_marked_mines_text,
                'value': self.config.backend.achievements.values.count_marked_mines_value,
                'checkbox': self.count_marked_mines_checkbox
            },
            'beginner_level': {
                'text': self.config.backend.achievements.texts.complete_beginner_level_text,
                'checkbox': None    # используется в составных достижениях
            },
            'professional_level': {
                'text': self.config.backend.achievements.texts.complete_professional_level_text,
                'checkbox': None    # используется в составных достижениях
            }
        }


    def process_achievements(self, data: dict) -> None:
        """
        Вспомогательный метод для load_achievements. Координирует проверку
        достижений двух типов: простых и составных
        """
        config = self.get_achievements_config()
        self.check_simple_achievements(data, config)
        self.check_composite_achievements(data, config)


    @staticmethod
    def check_simple_achievements(data: dict, config: dict) -> None:
        """
        Вспомогательный метод, осуществляющий проверку простых достижений, таких
        как: количество побед и отмеченных флагом мин
        """
        for key in ['count_wins', 'marked_mines']:
            achievement = config[key]
            text_key = achievement['text']
            if text_key in data:
                current_value = int(data[text_key])   # получаем текущее значение из .csv
                required_value = achievement['value']   # находим необходимое значение
                if current_value >= required_value:
                    achievement['checkbox'].setChecked(True)


    def check_composite_achievements(self, data: dict, config: dict) -> None:
        """
        Вспомогательный метод, осуществляющий проверку достижения на прохождение
        всех уровней сложности
        """
        levels = [      
            data.get(config['beginner_level']['text'], '0'),
            data.get(config['professional_level']['text'], '0')
        ]
        
        # проверяем выполнение всех условий
        if all(level == '1' for level in levels):
            self.complete_all_levels_checkbox.setChecked(True)

