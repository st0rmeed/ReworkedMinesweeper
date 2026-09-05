from backend.modules.menu import Menu

from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    application = QApplication(sys.argv)

    menu = Menu()
    menu.show()

    sys.exit(application.exec())