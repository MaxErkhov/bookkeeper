"""
Виджет с описанием бюджета
"""
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidgetItem, QMessageBox)
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.budget import Budget
from .common_styles import COMMON_STYLESHEET

from .presenters import PresenterBudget


class BudgetPerDay(QTableWidgetItem):
    """
    Класс для отображения дневного бюджета в виджете
    """
    def __init__(self, budget: Budget):
        super().__init__()
        self.update(budget)

    def get_value(self):
        """
        Возвращает значение дневного бюджета
        в виде числа с плавающей точкой
        """
        try:
            return float(self.text())
        except ValueError:
            return None

    def update(self, budget: Budget):
        """
        Обновляет значение элемента таблицы
        с бюджетом на день
        """
        self.budget = budget
        self.setText(str(self.budget.amount))


class BudgetPerWeek(QTableWidgetItem):
    """
    Класс для отображения недельного бюджета в виджете
    """
    def __init__(self, budget: Budget):
        super().__init__()
        self.update(budget)

    def get_value(self):
        """
        Возвращает значение недельного бюджета
        в виде числа с плавающей точкой
        """
        try:
            return float(self.text()) / 7
        except ValueError:
            return None

    def update(self, budget: Budget):
        """
        Обновляет значение элемента таблицы
        с бюджетом на неделю
        """
        self.budget = budget
        self.setText(str(self.budget.amount * 7))


class BudgetPerMonth(QTableWidgetItem):
    """
    Класс для отображения месячного бюджета в виджете
    """
    def __init__(self, budget: Budget):
        super().__init__()
        self.update(budget)

    def get_value(self):
        """
        Возвращает значение недельного бюджета
        в виде числа с плавающей точкой
        """
        try:
            return float(self.text()) / 30
        except ValueError:
            return None

    def update(self, budget: Budget):
        """
        Обновляет значение элемента таблицы
        с бюджетом на месяц
        """
        self.budget = budget
        self.setText(str(self.budget.amount * 30))


class BudgetWidget(QWidget):
    """
    Класс описывающий виджет бюджета
    """
    def __init__(self, waste_presenter) -> None:
        super().__init__()

        self.waste_presenter = waste_presenter
        self.budget_getter = None
        self.budget_modifier = None
        self.waste_getter = None

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(15)

        budget_icon = QtWidgets.QLabel("Бюджет")
        layout.addWidget(budget_icon)

        self.setStyleSheet(COMMON_STYLESHEET)

        self.wastings_table = QtWidgets.QTableWidget(2, 3)
        self.wastings_table.setColumnCount(2)
        self.wastings_table.setRowCount(3)
        self.wastings_table.setHorizontalHeaderLabels("Сумма "
                                                      "Бюджет ".split())
        self.wastings_table.setVerticalHeaderLabels("День "
                                                    "Неделя "
                                                    "Месяц ".split())

        header = self.wastings_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        for i in range(3):
            lost_item = QtWidgets.QTableWidgetItem()
            lost_item.setFlags(lost_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.wastings_table.setItem(i, 0, lost_item)

        budget: Budget = Budget(1)
        self.wastings_table.setItem(0, 1, BudgetPerDay(budget))
        self.wastings_table.setItem(1, 1, BudgetPerWeek(budget))
        self.wastings_table.setItem(2, 1, BudgetPerMonth(budget))
        self.wastings_table.itemChanged.connect(self.edit_budget_event)

        layout.addWidget(self.wastings_table)
        self.setLayout(layout)

        self.presenter = PresenterBudget(self, RepositoryFactory())

        wastings = self.waste_getter()
        budget = self.budget_getter()

        self.update_wastings(wastings)
        self.update_budget(budget)

    def register_budget_getter(self, handler):
        """
        Регистрирует обработчик получения бюджета
        """
        self.budget_getter = handler

    def register_budget_updater(self, handler):
        """
        Регистрирует обработчик обновления бюджета
        """
        self.budget_modifier = handler

    def register_waste_getter(self, handler):
        """
        Регистрирует обработчик получения расходов
        """
        self.waste_getter = handler

    def edit_budget_event(self, budget_item: QTableWidgetItem):
        """
        Обрабатывает событие изменения бюджета
        """
        value = budget_item.get_value()
        if value is None:
            QMessageBox.critical(self, 'Ошибка', 'Используйте только числа.')
        else:
            budget_item.budget.amount = value
            self.budget_modifier(budget_item.budget)

        self.update_budget(budget_item.budget)

    def update_wastings(self, wastings: list[float]) -> None:
        """
        Обновляет таблицу расходов
        """
        self.wastings_table.itemChanged.disconnect()
        assert len(wastings) == 3
        for i, waste in enumerate(wastings):
            self.wastings_table.item(i, 0).setText(str(waste))
        self.wastings_table.itemChanged.connect(self.edit_budget_event)

    def update_budget(self, budget: Budget) -> None:
        """
        Обновляет таблицу бюджета
        """
        self.wastings_table.itemChanged.disconnect()
        for i in range(3):
            self.wastings_table.item(i, 1).update(budget)
        self.wastings_table.itemChanged.connect(self.edit_budget_event)

    def retrieve_waste(self):
        """
        Получает и обновляет расходы
        """
        self.update_wastings(self.waste_getter())
