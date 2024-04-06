"""
Модуль наполняет окно виджетами
"""
from PySide6 import QtWidgets


from .waste_widget import WasteWidget
from .budget_widget import BudgetWidget
from .editing_window import EditingWindow


class StartWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Erkhov's Bookkeeper")

        layout = QtWidgets.QVBoxLayout()
        categoryEditor = EditingWindow([[]])
        wasteWidget = WasteWidget(categoryEditor)
        budgetWidget = BudgetWidget(wasteWidget.presenter)

        categoryEditor.category_changed.connect(wasteWidget.update_categorys)
        wasteWidget.waste_changed.connect(budgetWidget.retrieve_waste)

        wasteWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        budgetWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        categoryEditor.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                     QtWidgets.QSizePolicy.Expanding)

        editLayout = QtWidgets.QHBoxLayout()
        editLayout.addWidget(budgetWidget)
        editLayout.addWidget(categoryEditor)
        editWidget = QtWidgets.QWidget()
        editWidget.setLayout(editLayout)

        layout.addWidget(wasteWidget)
        layout.addWidget(editWidget)

        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
