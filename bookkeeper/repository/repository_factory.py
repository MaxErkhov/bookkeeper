"""
Модуль для создания экземпляров репозиториев.
"""


from .sqlite_repository import SQLiteRepository


class RepositoryFactory:
    """
    Фабрика для создания экземпляров репозиториев
    """
    def get(self, cls):
        """
        Создает и возвращает экземпляр репозитория для указанного класса
        """
        return SQLiteRepository[cls]("databases/ui_client.db", cls)
