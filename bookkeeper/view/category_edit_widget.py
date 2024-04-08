"""
Виджет для изменения категории
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)
from .editing_window import EditingWindow


class CategoryEditWidget(QWidget):
    """
    Виджет для редактирования категорий, включает в себя элементы
    управления для ввода суммы и добавления новой категории,
    а также виджет для редактирования существующих категорий
    """
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Редактирование")
        layout.addWidget(message)

        edit_widget = QWidget()

        split_layout = QtWidgets.QHBoxLayout()

        sum_label = QtWidgets.QLabel("Сумма")
        add_button = QtWidgets.QPushButton("Добавить")
        sum_line = QtWidgets.QLineEdit("0")

        sum_widget = QWidget()
        sum_layout = QtWidgets.QHBoxLayout()
        sum_layout.addWidget(sum_label)
        sum_layout.addWidget(sum_line)
        sum_widget.setLayout(sum_layout)

        adding_widget = QWidget()
        adding_layout = QtWidgets.QVBoxLayout()
        adding_layout.addWidget(sum_widget)
        adding_layout.addWidget(add_button)
        adding_widget.setLayout(adding_layout)

        edit_category_widget = EditingWindow([])
        split_layout.addWidget(adding_widget)
        split_layout.addWidget(edit_category_widget)

        edit_widget.setLayout(split_layout)
        layout.addWidget(edit_widget)

        self.setLayout(layout)
