"""
Виджет с описанием бюджета
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QTableWidget)


def setting_data(table: QTableWidget, spent: list[float], day_budget: float) -> None:
    """
    Заполняет QTableWidget данными о потраченных и оставшемся бюджете
    """
    budget = [day_budget, day_budget * 7, day_budget * 30]
    for i, [lost, limit] in enumerate(zip(spent, budget)):
        table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(lost)))
        table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(limit)))


class BudgetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

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
            QTableWidget {
                gridline-color: #ddd;
                background-color: #ffffff;
                font: 14px;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #e0e0e0;
                color: #000000;
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

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(15)

        budget_icon = QtWidgets.QLabel("Бюджет")
        layout.addWidget(budget_icon)

        expenses_table = QtWidgets.QTableWidget(2, 3)
        expenses_table.setColumnCount(2)
        expenses_table.setRowCount(3)
        expenses_table.setHorizontalHeaderLabels("Сумма "
                                                 "Бюджет ".split())
        expenses_table.setVerticalHeaderLabels("День "
                                               "Неделя "
                                               "Месяц ".split())

        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        setting_data(expenses_table, [0, 0, 0], 1)

        layout.addWidget(expenses_table)
        self.setLayout(layout)
