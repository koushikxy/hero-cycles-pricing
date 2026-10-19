from src.models import CycleConfiguration
from src.database import parts_db


def calculate_quote(config: CycleConfiguration):
    if "tubeless_tyre" in config.parts and "tube" in config.parts:
        raise ValueError("Conflict: Cannot select both 'Tubeless Tyre' and 'Tube' in one cycle.")

    items = []
    for part_id in config.parts:
        part = parts_db.get(part_id)
        if part is None:
            raise ValueError(f"Unknown part: '{part_id}'.")
        price = next((e.price for e in part.price_history
                      if e.valid_from <= config.date and (e.valid_until is None or config.date < e.valid_until)), None)
        if price is None:
            raise ValueError(f"No price for '{part.name}' on {config.date.isoformat()}.")
        items.append({"name": part.name, "component": part.component, "price": price})

    return sum(i["price"] for i in items), items
