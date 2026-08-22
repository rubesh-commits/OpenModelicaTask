import sys

from PyQt6.QtWidgets import QApplication

from omc_runner.controller import AppController
from omc_runner.view import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = AppController(window) 

    window.resize(640, 560)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
