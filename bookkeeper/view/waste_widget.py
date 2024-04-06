"""
Виджет для отображения расходов
"""
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (QWidget, QTableWidget)


def setting_data(table: QTableWidget, data: list[list[str]]) -> None:
    """
    Заполняет данные о расходах, включая дату, сумму, категорию и комментарий
    """
    font = QtGui.QFont()
    font.setPointSize(25)

    for i, row in enumerate(data):
        for j, x in enumerate(row):
            item = QtWidgets.QTableWidgetItem(x.capitalize())
            item.setFont(font)
            table.setItem(i, j, item)


class WasteWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)

        message = QtWidgets.QLabel("Последние расходы")
        message.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(message)

        expenses_table = QtWidgets.QTableWidget(4, 10)
        expenses_table.setColumnCount(4)
        expenses_table.setRowCount(10)
        expenses_table.setHorizontalHeaderLabels("Дата "
                                                 "Сумма "
                                                 "Категория "
                                                 "Комментарий".split())

        expenses_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: #f5f5f5;
                font: 10px;
                border-radius: 5px;

            }
            QTableWidget::item {
                padding: 5px;
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTableWidget::item:selected {
                background-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                             stop: 0 #007bff, stop: 1 #0056b3);
                color: white;
                padding: 5px;
                border: 1px solid #ddd;
                font: 14px;
                border-radius: 5px;
            }
        """)

        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        expenses_table.verticalHeader().hide()
        setting_data(expenses_table, [])

        layout.addWidget(expenses_table)
        self.setLayout(layout)
