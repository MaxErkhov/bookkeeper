"""
Модуль наполняет окно виджетами
"""
from PySide6 import QtWidgets


from .waste_widget import WasteWidget
from .budget_widget import BudgetWidget
from .editing_window import EditingWindow


class StartWindow(QtWidgets.QMainWindow):
    """
    Главное окно приложения, включающее в себя
    виджеты для работы с расходами,
    категориями расходов и бюджетом
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Erkhov's Bookkeeper")

        layout = QtWidgets.QVBoxLayout()
        category_editor = EditingWindow([[]])
        waste_widget = WasteWidget(category_editor)
        budget_widget = BudgetWidget(waste_widget.presenter)

        category_editor.category_changed.connect(waste_widget.update_categorys)
        waste_widget.waste_changed.connect(budget_widget.retrieve_waste)

        waste_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        budget_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
        category_editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                      QtWidgets.QSizePolicy.Expanding)

        edit_layout = QtWidgets.QHBoxLayout()
        edit_layout.addWidget(budget_widget)
        edit_layout.addWidget(category_editor)
        edit_widget = QtWidgets.QWidget()
        edit_widget.setLayout(edit_layout)

        layout.addWidget(waste_widget)
        layout.addWidget(edit_widget)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
