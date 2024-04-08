"""
Окно с выбором категорий для изменения
"""
from typing import Any
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTreeWidgetItem, QMenu, QMessageBox)

from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.category import Category
from .presenters import PresenterCategory


class CategoryEntity(QTreeWidgetItem):
    """
    Элемент дерева для категории, позволяющий редактировать имя категории
    """
    def __init__(self, parent: Any, category: Category):
        super().__init__(parent, [category.name])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.category = category

    def update(self, name: str) -> None:
        """
        Обновляет имя категории
        """
        self.category.name = name

    def __str__(self) -> str:
        """
        Возвращает имя категории в виде строки
        """
        return self.category.name


class EditingWindow(QWidget):
    """
    Окно для редактирования категорий, включает в себя дерево категорий и контекстное меню
    """
    category_changed = QtCore.Signal()

    def __init__(self, categories: list[str]):
        super().__init__()

        self.setWindowTitle("Изменение категорий")

        layout = QtWidgets.QVBoxLayout()

        self.categorys_widget = QtWidgets.QTreeWidget()
        self.categorys_widget.setColumnCount(1)
        self.categorys_widget.setHeaderLabel('Категории')
        self.category_adder = None
        self.category_updater = None
        self.category_checker = None
        self.category_deleter = None
        self.category_finder = None

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

        layout.addWidget(self.categorys_widget)
        self.setLayout(layout)
        self.presenter = PresenterCategory(self, RepositoryFactory())

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_category_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_category_event)

        self.categorys_widget.itemChanged.connect(self.edit_category_event)

    def get_selected_category(self) -> QTreeWidgetItem:
        """
        Возвращает выбранный элемент категории
        """
        return self.categorys_widget.currentItem()

    def register_category_adder(self, handler) -> None:
        """
        Регистрирует обработчик добавления категории
        """
        self.category_adder = handler

    def register_category_updater(self, handler) -> None:
        """
        Регистрирует обработчик изменения категории
        """
        self.category_updater = handler

    def register_category_checker(self, handler) -> None:
        """
        Регистрирует обработчик проверки уникальности имени категории
        """
        self.category_checker = handler

    def register_category_deleter(self, handler) -> None:
        """
        Регистрирует обработчик удаления категории
        """
        self.category_deleter = handler

    def register_category_finder(self, handler) -> None:
        """
        Регистрирует обработчик поиска категории
        """
        self.category_finder = handler

    def set_category_list(self, categories: list[Category]) -> None:
        """
        Устанавливает список категорий в виджете
        """
        table = self.categorys_widget
        uniq_pk: dict[int, CategoryEntity] = {}

        set_once: bool = False

        for i in categories:
            pk_ = i.pk_
            parent = i.parent

            parent_category: Any = table
            if parent is not None:
                parent_category = uniq_pk.get(int(parent))

            category_item = CategoryEntity(parent_category, i)
            uniq_pk.update({pk_: category_item})
            if not set_once:
                table.setCurrentItem(category_item)
                set_once = True

    def contextMenuEvent(self, event) -> None:
        """
        Обрабатывает событие контекстного меню
        """
        self.menu.exec_(event.globalPos())

    def delete_category(self, category_item: CategoryEntity, *_) -> None:
        """
        Удаляет категорию из дерева
        """
        root = self.categorys_widget.invisibleRootItem()
        (category_item.parent() or root).removeChild(category_item)

    def rename_category(self, category_item: CategoryEntity, column: int) -> None:
        """
        Переименовывает категорию
        """
        category_item.setText(column, category_item.category.name)

    def edit_category_event(self, category_item: CategoryEntity, column: int) -> None:
        """
        Обрабатывает событие изменения категории
        """
        entered_text = category_item.text(column)

        if category_item.category.pk_ == 0:
            action: Any = self.category_adder
            revert: Any = self.delete_category
        else:
            action = self.category_updater
            revert = self.rename_category

        if not self.category_checker(entered_text):
            QMessageBox.critical(self, 'Ошибка', 'Такая категория уже есть!')
            self.categorys_widget.itemChanged.disconnect()
            revert(category_item, column)
            self.categorys_widget.itemChanged.connect(self.edit_category_event)
        else:
            category_item.update(entered_text)
            action(category_item.category)
            self.category_changed.emit()

    def add_category_event(self) -> None:
        """
        Обрабатывает событие добавления новой категории
        """
        category_items = self.categorys_widget.selectedItems()
        if len(category_items) == 0:
            parent_item: Any = self.categorys_widget
            parent_pk = None
        else:
            assert len(category_items) == 1
            parent_item = category_items.pop()
            parent_pk = parent_item.category.pk_

        self.categorys_widget.itemChanged.disconnect()
        new_category = CategoryEntity(parent_item, Category(parent=parent_pk))
        self.categorys_widget.itemChanged.connect(self.edit_category_event)
        self.categorys_widget.setCurrentItem(new_category)
        self.categorys_widget.edit(self.categorys_widget.currentIndex())

    def delete_category_event(self) -> None:
        """
        Обрабатывает событие удаления категории
        """
        category_item = self.categorys_widget.currentItem()
        confirm = QMessageBox.warning(self, 'Предупреждение!',
                                      f'Точно далить текущую категорию "'
                                      f'{category_item.category.name}" и все дочерние?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return

        assert isinstance(category_item, CategoryEntity)
        self.delete_category(category_item)
        if category_item.category.pk_ == 0:
            return
        self.category_deleter(category_item.category)
        self.category_changed.emit()
