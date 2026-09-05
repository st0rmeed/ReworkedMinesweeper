from frontend.chapters.authors_interface import AuthorsInterface

from backend.modules.basic_window_of_functionality import BasicWindowFunctionality

from PyQt6.QtWidgets import QListWidgetItem

from PyQt6.QtWidgets import QMainWindow


class Authors(AuthorsInterface, BasicWindowFunctionality):
    """
    Реализует backend часть раздела с разработчиками. Наследуется
    от двух классов: AuthorsInterface (frontend часть раздела) и BasicWindowFunctionality
    (класс с базовым функционалом). Реализует логику загрузки и показа списка авторов
    """

    def __init__(self, menu_chapter: QMainWindow):
        # 1. Перезапускам классы родителей и передаем параметры
        AuthorsInterface.__init__(self)
        BasicWindowFunctionality.__init__(self, menu_chapter)

        # 2. Подключаем кнопки к функциям. Словарь в формате: {кнопка: функция_вызывающаяся_по_нажатию}
        buttons = {
            self.to_menu_button: self.open_menu_chapter
        }
        self.connect_buttons_and_funcs(buttons)
        
        # 3. Загружаем список авторов
        self.load_authors()


    def load_authors(self) -> None:
        """
        Метод, координирующий заполнение таблицы. Состоит из двух
        подфункций
        """
        lines = self.load_authors_data()
        self.filling_in_table(lines)


    def load_authors_data(self) -> list:
        """
        Вспомогательный метод для load_authors, отвечающий за
        загрузку данных
        """
        with open(self.config.backend.data.authors, 'r', encoding='utf8') as txt_file:
            lines = txt_file.readlines()
            return lines


    def filling_in_table(self, lines: list) -> None:
        """
        Вспомогательный метод для load_authors, отвечающий за
        заполнение таблицы данными
        """
        for line in lines:
            if line:
                item = QListWidgetItem(line.strip())
                self.authors_list_widget.addItem(item)
