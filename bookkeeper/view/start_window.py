"""
Модуль наполняет окно виджетами
"""
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QSizePolicy)


from .waste_widget import WasteWidget
from .budget_widget import BudgetWidget
from .category_edit_widget import CategoryEditWidget


class StartWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Erkhov's Bookkeeper")

        layout = QtWidgets.QVBoxLayout()
        waste = WasteWidget()
        budget = BudgetWidget()
        category_edit = CategoryEditWidget()

        waste.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        budget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        category_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(waste)
        layout.addWidget(budget)
        layout.addWidget(category_edit)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
