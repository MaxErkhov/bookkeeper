"""
Класс для отображения бюджета
"""

from dataclasses import dataclass


@dataclass
class Budget:
    amount: float = 0.0
    pk_: int = 0
