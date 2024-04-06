"""
Окно с выбором категорий для изменения
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QListWidget)


def setting_data(table: QListWidget, data: list[str]) -> None:
    """
    Заполняет QListWidget категориями
    """
    for ctg in data:
        table.addItem(ctg)


class EditingWindow(QWidget):
    def __init__(self, ctgs: list[str]) -> None:
        super().__init__()

        self.setWindowTitle("Изменение категорий")
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font: 14px;
                border-radius: 5px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
            }

        """)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(15)

        message = QtWidgets.QLabel("Категории")
        layout.addWidget(message)

        ctgs_widget = QtWidgets.QListWidget()
        setting_data(ctgs_widget, ctgs)

        layout.addWidget(ctgs_widget)
        self.setLayout(layout)
        self.resize(400, 300)
