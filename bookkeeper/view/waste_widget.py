"""
Виджет для отображения расходов
"""
from datetime import datetime
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidget,
                               QMenu, QMessageBox, QTableWidgetItem)

from bookkeeper.models.expense import Expense
from bookkeeper.repository.repository_factory import RepositoryFactory
from .presenters import PresenterWaste
from .category_edit_widget import EditingWindow


class TableRow():
    """
    Класс для представления строки таблицы с данными о расходе
    """
    def __init__(self, waste: Expense):
        self.waste = waste


class TableEntity(QTableWidgetItem):
    """
    Класс для представления элемента таблицы с данными о расходе.
    Обеспечивает валидацию и обновление данных о расходе, а также восстановление
    значения элемента из данных о расходе
    """
    def __init__(self, row: TableRow):
        super().__init__()
        self.row = row
        self.restore()

    def validate(self) -> bool:
        """
        Проверяет, является ли текущее значение элемента действительным
        """
        return True

    def restore(self):
        """
        Восстанавливает значение элемента из данных о расходе
        """
        self.setText(self.row.waste.comment)

    def update(self):
        """
        Обновляет данные о расходе на основе значения элемента
        """
        self.row.waste.comment = self.text()

    def get_err_msg(self) -> str:
        """
        Возвращает сообщение об ошибке для недействительного значения
        """
        return "Ошибка - недействительное значение"

    def should_emit_on_upd(self) -> bool:
        """
        Определяет, должен ли сигнал обновления расхода быть
        отправлен после обновления элемента
        """
        return False


class TableAmountEntity(TableEntity):
    """
    Класс для представления суммы расхода в таблице.
    Обеспечивает валидацию и обновление суммы расхода, а также восстановление
    значения суммы из данных о расходе
    """
    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        """
        Проверяет, является ли текущее значение действительным числом
        """
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self):
        """
        Восстанавливает значение суммы расхода из данных о расходе
        """
        self.setText(str(self.row.waste.amount))

    def update(self):
        """
        Обновляет сумму расхода на основе значения элемента
        """
        self.row.waste.amount = float(self.text())

    def get_err_msg(self) -> str:
        """
        Возвращает сообщение об ошибке для недействительного числового значения
        """
        return 'Введите действительное число'

    def should_emit_on_upd(self) -> bool:
        """
        Определяет, должен ли сигнал обновления расхода быть
        отправлен после обновления элемента
        """
        return True


class TableCategoryEntity(TableEntity):
    """
    Класс для представления категории расхода в таблице.
    Обеспечивает валидацию и обновление категории расхода, а также восстановление
    значения категории из данных о расходе
    """
    def __init__(self, row: TableRow, exp_view):
        self.category_view = exp_view.category_view
        self.retriever = exp_view.category_retriever
        super().__init__(row)

    def validate(self) -> bool:
        """
        Проверяет, является ли текущее значение существующей категорие
        """
        category_name = self.text()
        return not self.category_view.category_checker(category_name)

    def restore(self):
        """
        Восстанавливает значение категории расхода из данных о расходе
        """
        category = self.retriever(self.row.waste.category)
        if category is None:
            category_item = self.category_view.get_selected_category()
            if category_item is None:
                raise ValueError('Категория не установлена')
            category = category_item.category.name
            self.row.waste.category = category_item.category.pk_
        self.setText(category)

    def update(self):
        """
        Обновляет категорию расхода на основе значения элемента
        """
        pk_ = self.category_view.category_finder(self.text())
        assert pk_ is not None
        self.row.waste.category = pk_

    def get_err_msg(self) -> str:
        """
        Возвращает сообщение об ошибке для недействительной категории
        """
        return 'Нужно ввести существующую категорию.'


class TableDateEntity(TableEntity):
    """
    Класс для представления даты расхода в таблице.
    Обеспечивает валидацию и обновление даты расхода, а также восстановление
    значения даты из данных о расходе
    """
    fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        """
        Проверяет, является ли текущее значение действительной датой
        """
        date_str = self.text()
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            return False
        return True

    def restore(self):
        """
        Восстанавливает значение даты расхода из данных о расходе
        """
        date = self.row.waste.waste_date
        self.setText(date.strftime(self.fmt))

    def get_err_msg(self) -> str:
        """
        Возвращает сообщение об ошибке для недействительной даты
        """
        return f'Неверный формат даты.\nНадо так: {self.fmt}'

    def update(self):
        """
        Обновляет дату расхода на основе значения элемента
        """
        self.row.waste.waste_date = datetime.fromisoformat(self.text())

    def should_emit_on_upd(self) -> bool:
        """
        Определяет, должен ли сигнал обновления расхода
        быть отправлен после обновления элемента
        """
        return True


class Table(QTableWidget):
    """
    Виджет таблицы для отображения и управления данными о расходах.
    Предоставляет функциональность для добавления, удаления и обновления строк таблицы,
    а также для работы с контекстным меню.
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels("Дата "
                                       "Сумма "
                                       "Категория "
                                       "Комментарий".split())

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QTableWidget {
                gridline-color: #ddd;
                background-color: #f5f5f5;
                font: 14px;
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

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.verticalHeader().hide()

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_waste_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_waste_event)

        self.itemChanged.connect(self.update_waste_event)

    def update_waste_event(self, waste_item: TableEntity):
        """
        Обрабатывает событие изменения элемента таблицы с данными о расходе
        """
        if not waste_item.validate():
            self.itemChanged.disconnect()
            QMessageBox.critical(self, 'Ошибка', waste_item.get_err_msg())
            waste_item.restore()
            self.itemChanged.connect(self.update_waste_event)
            return

        waste_item.update()

        if waste_item.should_emit_on_upd():
            self.parent.emit_waste_changed()

        self.parent.waste_updater(waste_item.row.waste)

    def add_waste_line(self, waste: Expense):
        """
        Добавляет новую строку в таблицу с данными о расходе
        """
        row = TableRow(waste)
        category_item = TableCategoryEntity(row, self.parent)
        rc_ = self.rowCount()
        self.setRowCount(rc_+1)
        self.itemChanged.disconnect()
        self.setItem(rc_, 0, TableDateEntity(row))
        self.setItem(rc_, 1, TableAmountEntity(row))
        self.setItem(rc_, 2, category_item)
        self.setItem(rc_, 3, TableEntity(row))
        self.itemChanged.connect(self.update_waste_event)

    def delete_waste_event(self):
        """
        Обрабатывает событие удаления строки из таблицы с данными о расходе
        """
        row = self.currentRow()
        if row == -1:
            return
        confirm = QMessageBox.warning(self, 'Внимание',
                                      'Вы уверены, что хотите удалить текущую запись?"',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return
        self.removeRow(row)
        waste_to_del = self.item(row, 0).row.waste
        self.parent.waste_deleter(waste_to_del)
        self.parent.emit_waste_changed()

    def add_waste_event(self):
        """
        Обрабатывает событие добавления нового расхода
        """
        waste = Expense()
        try:
            self.add_waste_line(waste)
        except ValueError as ve_:
            QMessageBox.critical(self, 'Ошибка', f'{ve_}')
            return
        self.parent.waste_adder(waste)
        self.parent.emit_waste_changed()

    def contextMenuEvent(self, event):
        """
        Обрабатывает событие вызова контекстного меню
        """
        self.menu.exec_(event.globalPos())

    def update_categorys(self):
        """
        Обновляет категории в таблице, восстанавливая их из данных о расходах
        """
        try:
            for row in range(self.rowCount()):
                self.item(row, 2).restore()
        except ValueError as ve_:
            QMessageBox.critical(self, 'Ошибка',
                                 f'Критическая ошибка.\n{ve_}.\nНекоректные категории.')


class WasteWidget(QWidget):
    """
    Виджет для отображения и управления расходами.
    Предоставляет функциональностьдля добавления, удаления и обновления расходов,
    а также для управления категориями расходов
    """
    waste_changed = QtCore.Signal()

    def __init__(self, category_view: EditingWindow) -> None:
        super().__init__()
        self.category_view = category_view
        self.category_retriever = None
        self.waste_adder = None
        self.waste_deleter = None
        self.waste_updater = None

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(message)

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
        """)

        self.table = Table(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.presenter = PresenterWaste(self, RepositoryFactory())

    def register_category_retriever(self, handler):
        """
        Регистрирует обработчик получения категории расхода
        """
        self.category_retriever = handler

    def register_waste_adder(self, handler):
        """
        Регистрирует обработчик добавления нового расхода
        """
        self.waste_adder = handler

    def register_waste_deleter(self, handler):
        """
        Регистрирует обработчик удаления расхода
        """
        self.waste_deleter = handler

    def register_waste_updater(self, handler):
        """
        Регистрирует обработчик обновления данных о расходе
        """
        self.waste_updater = handler

    def set_waste_list(self, data: list[Expense]):
        """
        Устанавливает список расходов для отображения в таблице
        """
        list_to_delete: list[Expense] = []
        for i in data:
            try:
                self.table.add_waste_line(i)
            except ValueError as ve_:
                QMessageBox.critical(self, 'Ошибка', f'Критическая ошибка.\n{ve_}.\n'
                                     f'Запись будет удалена.')
                list_to_delete.append(i)
        for i in list_to_delete:
            self.waste_deleter(i)

    def update_categorys(self):
        """
        Обновляет категории в таблице, восстанавливая их из данных о расходах
        """
        self.table.update_categorys()

    def emit_waste_changed(self):
        """
        Отправляет сигнал о том, что данные о расходах были изменены
        """
        self.waste_changed.emit()
