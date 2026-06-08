from src.models import CycleConfiguration
from src.database import parts_db

def calculate_quote(config: CycleConfiguration):
    # Cannot have Tubeless Tyre and Tube together
    if "tubeless_tyre" in config.parts and "tube" in config.parts:
        raise ValueError("Conflict: Cannot select both 'Tubeless Tyre' and 'Tube' in one cycle.")

    total_price = 0.0
    items = []

    for part_id in config.parts:
        if part_id not in parts_db:
            continue
            
        part = parts_db[part_id]
        active_price = None

        # find the price for the specific date
        for entry in part.price_history:
            start = entry.valid_from
            end = entry.valid_until
            
            if config.date >= start and (end is None or config.date < end):
                active_price = entry.price
                break
        
        if active_price is not None:
            total_price += active_price
            items.append({
                "name": part.name, 
                "price": active_price
            })
            
    return total_price, items