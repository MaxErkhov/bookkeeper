"""
Модуль для создания окна с графическим интерфейсом
"""
import sys

from PySide6 import QtWidgets
from view.start_window import StartWindow

app = QtWidgets.QApplication(sys.argv)
window = StartWindow()
window.resize(800, 600)
window.show()
sys.exit(app.exec())
