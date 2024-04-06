"""
Виджет для изменения категории
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QComboBox)
from .editing_window import EditingWindow


def setting_data(box: QComboBox, cats: list[str]) -> None:
    """
    Заполняет QComboBox (выпадающий список) категориями
    """
    for cat in cats:
        box.addItem(cat)


class CategoryEditWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: g;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(15)

        message = QtWidgets.QLabel("Редактирование")
        layout.addWidget(message)

        glayout = QtWidgets.QGridLayout()
        glayout.setSpacing(15)

        sum_label = QtWidgets.QLabel("Сумма")
        cat_label = QtWidgets.QLabel("Категория")
        add_button = QtWidgets.QPushButton("Добавить")
        cat_edit_button = QtWidgets.QPushButton("Редактировать")
        sum_line = QtWidgets.QLineEdit("0")
        cats_box = QtWidgets.QComboBox()

        glayout.addWidget(sum_label, 0, 0)
        glayout.addWidget(sum_line, 0, 1)
        glayout.addWidget(cat_label, 1, 0)
        glayout.addWidget(cats_box, 1, 1)
        glayout.addWidget(cat_edit_button, 1, 2)
        glayout.addWidget(add_button, 2, 1)

        gwidget = QWidget()
        gwidget.setLayout(glayout)
        layout.addWidget(gwidget)

        self.cat_list = ["Донаты", "Книги", "Еда", "Кофе переход ГК-НК"]
        setting_data(cats_box, self.cat_list)

        cat_edit_button.clicked.connect(self.open_window)

        self.setLayout(layout)

    def open_window(self):
        """
        Открывает окно редактирования категорий
        """
        self.edit_win = EditingWindow(self.cat_list)
        self.edit_win.show()
