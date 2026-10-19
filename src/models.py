from datetime import date
from typing import List, Optional


class PriceEntry:
    def __init__(self, price: float, valid_from: date, valid_until: Optional[date] = None):
        self.price = price
        self.valid_from = valid_from
        self.valid_until = valid_until


class Part:
    def __init__(self, name: str, component: str, price_history: List[PriceEntry]):
        self.name = name
        self.component = component
        self.price_history = price_history


class CycleConfiguration:
    def __init__(self, config_date: date, parts: List[str]):
        self.date = config_date
        self.parts = parts
