"""
Презентеры
"""
from typing import Protocol
from datetime import datetime, timedelta

from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class AbstractView(Protocol):
    def set_category_list(notused: list[Category]) -> None:
        pass

    def register_category_updater(handler):
        pass

    def register_category_adder(handler):
        pass

    def register_category_checker(handler):
        pass

    def register_category_finder(handler):
        pass

    def register_category_deleter(handler):
        pass

    def register_category_retriever(handler):
        pass

    def register_budget_updater(handler):
        pass

    def register_budget_getter(handler):
        pass

    def register_waste_getter(handler):
        pass


class PresenterCategory:
    """
    Презентер категорий
    """
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.category_repo = repository_factory.get(Category)

        self.categories = self.category_repo.get_all()
        self.view.set_category_list(self.categories)
        self.view.register_category_updater(self.update_category)
        self.view.register_category_adder(self.add_category)
        self.view.register_category_checker(self.used_name)
        self.view.register_category_deleter(self.delete_category)
        self.view.register_category_finder(self.find_by_name)

    def update_category(self, category: Category) -> None:
        """
        Обновляет категорию в репозитории
        """
        self.category_repo.update(category)

    def used_name(self, name: str) -> bool:
        """
        Проверяет, существует ли категория с данным именем
        """
        if name in [c.name for c in self.categories]:
            return False
        return True

    def find_by_name(self, name: str) -> int | None:
        """
        Находит категорию по имени и возвращает ее первичный ключ
        """
        for x in self.categories:
            if x.name == name:
                return x.pk_
        return None

    def add_category(self, category: Category) -> None:
        """
        Добавляет новую категорию в репозиторий и представление
        """
        self.category_repo.add(category)
        self.categories.append(category)

    def delete_category(self, top_lvl_category: Category) -> None:
        """
        Удаляет категорию и все ее подкатегории из репозитория и представления
        """
        queue = [top_lvl_category]
        to_delete = list()

        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.categories if x.parent == proc.pk_])

        for x in to_delete:
            self.categories.remove(x)
            self.category_repo.delete(x.pk_)


class PresenterBudget:
    """
    Презентер бюджета
    """
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.waste_presenter = self.view.waste_presenter
        self.repo = repository_factory.get(Budget)
        self.view.register_budget_updater(self.update_budget)
        self.view.register_budget_getter(self.get_budget)
        self.view.register_waste_getter(self.get_waste)

    def get_waste(self) -> list[float]:
        """
        Возвращает суммы расходов за день, неделю и месяц
        """
        now = datetime.now()
        day = now - timedelta(days=1)
        week = now - timedelta(weeks=1)
        month = now - timedelta(days=30)

        waste_day = sum(self.waste_presenter.get_waste_from_period(now, day))
        waste_week = sum(self.waste_presenter.get_waste_from_period(now, week))
        waste_month = sum(self.waste_presenter.get_waste_from_period(now, month))
        return [waste_day, waste_week, waste_month]

    def update_budget(self, budget: Budget):
        """
        Обновляет бюджет в репозитории
        """
        self.repo.update(budget)

    def get_budget(self) -> Budget:
        """
        Возвращает текущий бюджет
        """
        budgets = self.repo.get_all()
        if len(budgets) == 0:
            budget = Budget(0)
            self.repo.add(budget)
            budgets.append(budget)

        assert len(budgets) == 1
        return budgets.pop()


class PresenterWaste:
    """
    Презентер расходов
    """
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.repo = repository_factory.get(Expense)
        self.category_repo = repository_factory.get(Category)

        self.wastings = self.repo.get_all()
        self.view.register_waste_adder(self.add_waste)
        self.view.register_waste_deleter(self.delete_waste)
        self.view.register_waste_updater(self.update_waste)
        self.view.register_category_retriever(self.retrieve_category)
        self.view.set_waste_list(self.wastings)

    def retrieve_category(self, pk_: int) -> str:
        """
        Возвращает имя категории по ее первичному ключу
        """
        category = self.category_repo.get(pk_)
        if category is None:
            return None
        return category.name

    def add_waste(self, waste: Expense):
        """
        Добавляет новый расход в репозиторий и представление
        """
        self.repo.add(waste)
        self.wastings.append(waste)

    def delete_waste(self, waste: Expense):
        """
        Удаляет расход из репозитория и представления
        """
        self.wastings.remove(waste)
        self.repo.delete(waste.pk_)

    def update_waste(self, waste: Expense):
        """
        Обновляет расход в репозитории
        """
        self.repo.update(waste)

    def get_waste_from_period(self, start: datetime, end: datetime) -> list[float]:
        """
        Возвращает суммы расходов за указанный период
        """
        assert start > end
        wastings = [x.amount for x in self.wastings
                    if x.waste_date < start and x.waste_date > end]
        return wastings
