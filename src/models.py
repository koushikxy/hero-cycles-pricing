from datetime import date
from typing import List, Optional

class PriceEntry:
    """Represents a price during a specific window of time."""
    def __init__(self, valid_from: date, valid_until: Optional[date], price: float):
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.price = price

class Part:
    """Represents a physical cycle part and its historical prices."""
    def __init__(self, part_id: str, name: str, component: str, price_history: List[PriceEntry]):
        self.id = part_id
        self.name = name
        self.component = component
        self.price_history = price_history

class CycleConfiguration:
    """Represents the quote request from the salesperson."""
    def __init__(self, config_date: date, parts: List[str]):
        self.date = config_date
        self.parts = parts