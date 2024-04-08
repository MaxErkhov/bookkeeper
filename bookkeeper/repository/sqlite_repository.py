"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def to_string(value: str | int) -> str | int:
    """
    Преобразует значение в строку.
    """
    if isinstance(value, str):
        return f'\'{value}\''
    return value


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий для работы с SQLite базой данных.
    """

    def __init__(self, file_dbase: str, cls: type) -> None:
        self.file_dbase = file_dbase
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk_')
        self.cls_ty = cls

        with sqlite3.connect(self.file_dbase) as con:
            self._create_table(con)
        con.close()

    def _create_table(self, con: sqlite3.Connection) -> None:
        """
        Создает таблицу в базе данных на основе аннотаций класса.
        """
        with con:
            cursor = con.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            query = f'CREATE TABLE {self.table_name} (id INTEGER PRIMARY KEY'
            for name, typ in self.fields.items():
                query += f', {name} {self._get_type(typ)}'
            query += ')'
            cursor.execute(query)

    def _get_type(self, attr_type: Any) -> str:
        """
        Определяет тип данных в соответствии с аннотацией.
        """
        type_mapping = {
            int: 'INTEGER',
            float: 'REAL',
            str: 'TEXT',
        }
        return type_mapping.get(attr_type, 'TEXT')

    def is_in_dbase(self, cursor: Any, pk_: int) -> bool:
        """
        Проверяет, существует ли запись с данным primary key.
        """
        query = f'SELECT * FROM {self.table_name} WHERE id = {pk_}'
        res = cursor.execute(query).fetchone()
        return res is not None

    def add(self, obj: T) -> int:
        """
        Добавляет объект в базу данных.
        """
        if getattr(obj, 'pk_', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk_` attribute')
        names = ', '.join(self.fields.keys())
        qmarks = ', '.join("?" * len(self.fields))
        values = [getattr(obj, i) for i in self.fields]
        with sqlite3.connect(self.file_dbase) as con:
            cursor = con.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')
            cursor.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({qmarks})',
                values
            )
            if not cursor.lastrowid:
                raise ValueError("No assignable pk_")
            obj.pk_ = int(cursor.lastrowid)

        con.close()
        return obj.pk_

    def fill_object(self, result: Any) -> T:
        """
        Заполняет атрибуты объекта на основе результата запроса к базе данных.
        """
        obj: T = self.cls_ty()
        obj.pk_ = result[0]
        for i, res in zip(self.fields, result[1:]):
            setattr(obj, i, res)
        return obj

    def get(self, pk_: int) -> T | None:
        """
        Возвращает объект из базы данных по primary key.
        """
        with sqlite3.connect(self.file_dbase) as con:
            query = f'SELECT * FROM {self.table_name} WHERE id = {pk_}'
            result = con.cursor().execute(query).fetchone()
            if result is None:
                return None
            obj: T = self.fill_object(result)
        con.close()
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Возвращает все объекты из базы данных.
        """
        query = f'SELECT * FROM {self.table_name}'
        condition = ''
        if where is not None:
            condition = ' WHERE'
            for key, val in where.items():
                condition += f' {key} = {to_string(val)} AND'
            query += condition.rsplit(' ', 1)[0]

        with sqlite3.connect(self.file_dbase) as con:
            results = con.cursor().execute(query).fetchall()
            objs = [self.fill_object(result) for result in results]

        con.close()
        return objs

    def update(self, obj: T) -> None:
        """
        Обновляет объект в базе данных.
        """
        values = [to_string(getattr(obj, i)) for i in self.fields]
        setter = [f'{col} = {val}' for col, val in zip(self.fields, values)]
        upd_stm = ', '.join(setter)

        with sqlite3.connect(self.file_dbase) as con:
            if not self.is_in_dbase(con.cursor(), obj.pk_):
                raise ValueError(f'No object with id={obj.pk_} in DB.')
            query = f'UPDATE {self.table_name} SET {upd_stm} WHERE id = {obj.pk_}'
            con.cursor().execute(query)
        con.close()

    def delete(self, pk_: int) -> None:
        """
        Удаляет запись из базы данных.
        """
        with sqlite3.connect(self.file_dbase) as con:
            if not self.is_in_dbase(con.cursor(), pk_):
                raise KeyError(f'No object with id={pk_} in DB.')
            query = f'DELETE FROM {self.table_name} WHERE id = {pk_}'
            con.cursor().execute(query)
        con.close()

    def delete_all(self) -> None:
        """
        Удаляет все записи из базы данных.
        """
        with sqlite3.connect(self.file_dbase) as con:
            query = f'DELETE FROM {self.table_name}'
            con.cursor().execute(query)
        con.close()
