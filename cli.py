import json
import argparse
from datetime import date
from src.models import CycleConfiguration
from src.engine import calculate_quote
from src.database import parts_db

def run_cli():
    parser = argparse.ArgumentParser(description="Hero Cycles CLI Pricing Engine")
    parser.add_argument("--config", default="quote_request.json", help="Path to JSON config file")
    args = parser.parse_args()

    # 1. Read JSON file
    try:
        with open(args.config, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {args.config}")
        return

    # 2. Configure Quote
    quote_date = date.fromisoformat(data['date'])
    config = CycleConfiguration(config_date=quote_date, parts=data['parts'])

    # 3. Run Engine
    try:
        total_price, items = calculate_quote(config)
    except Exception as e:
        print(f"Engine Error: {e}")
        return

    # 4. Group by High-Level Component
    component_totals = {}
    for part_id in config.parts:
        if part_id in parts_db:
            part_obj = parts_db[part_id]
            comp_name = part_obj.component
            price = next((item['price'] for item in items if item['name'] == part_obj.name), 0)
            
            if comp_name not in component_totals:
                component_totals[comp_name] = 0
            component_totals[comp_name] += price

    # 5. Print Output
    formatted_date = quote_date.strftime("%d %b %Y")
    print(f"\nCycle Price Breakdown - {formatted_date}")
    print("-" * 40)
    for comp, price in component_totals.items():
        print(f"{comp}: ₹{price:,.0f}")
    print("-" * 40)
    print(f"TOTAL: ₹{total_price:,.0f}\n")

if __name__ == "__main__":
    run_cli()