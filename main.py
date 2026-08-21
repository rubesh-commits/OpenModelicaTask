"""
Entry point for the OpenModelica Model Runner app.

Run with:
    python main.py
"""

import sys

from PyQt6.QtWidgets import QApplication

from omc_runner.controller import AppController
from omc_runner.view import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = AppController(window)  # noqa: F841 - keeps controller alive

    window.resize(640, 560)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
