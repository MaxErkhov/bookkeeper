"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    waste_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk_ - id записи в базе данных
    """
    amount: float = 0.0
    category: int = 0
    waste_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk_: int = 0
