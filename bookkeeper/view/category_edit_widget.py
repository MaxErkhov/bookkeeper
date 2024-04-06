"""
Виджет для изменения категории
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)
from .editing_window import EditingWindow


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
                padding: 14px;
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
        """)

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
