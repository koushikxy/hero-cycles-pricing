import argparse
import json
import sys
from datetime import date
from src.models import CycleConfiguration
from src.engine import calculate_quote


def run_cli():
    parser = argparse.ArgumentParser(description="Hero Cycles CLI Pricing Engine")
    parser.add_argument("--config", default="quote_request.json", help="Path to JSON config file")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    try:
        with open(args.config, encoding="utf-8") as file:
            data = json.load(file)
        quote_date = date.fromisoformat(data["date"])
        total_price, items = calculate_quote(CycleConfiguration(quote_date, data["parts"]))
    except FileNotFoundError:
        sys.exit(f"Error: Could not find {args.config}")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        sys.exit(f"Error: {e}")

    component_totals = {}
    for item in items:
        component_totals[item["component"]] = component_totals.get(item["component"], 0) + item["price"]

    print(f"\nCycle Price Breakdown - {quote_date.strftime('%d %b %Y')}")
    print("-" * 40)
    for comp, price in component_totals.items():
        print(f"{comp}: ₹{price:,.0f}")
    print("-" * 40)
    print(f"TOTAL: ₹{total_price:,.0f}\n")


if __name__ == "__main__":
    run_cli()
