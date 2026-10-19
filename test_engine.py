import json
import unittest
from datetime import date
from src.database import parts_db
from src.models import CycleConfiguration
from src.engine import calculate_quote


def quote(d, parts):
    return calculate_quote(CycleConfiguration(d, parts))[0]


class TestPricingEngine(unittest.TestCase):

    def test_pre_hike_pricing(self):
        self.assertEqual(quote(date(2026, 5, 1), ["steel_frame", "v_brakes"]), 2050)

    def test_post_hike_pricing(self):
        self.assertEqual(quote(date(2026, 10, 1), ["steel_frame", "v_brakes"]), 2200)

    def test_change_day_uses_new_price(self):
        self.assertEqual(quote(date(2026, 7, 31), ["steel_frame"]), 1200)
        self.assertEqual(quote(date(2026, 8, 1), ["steel_frame"]), 1300)
        self.assertEqual(quote(date(2027, 1, 1), ["steel_frame"]), 1400)

    def test_full_configuration_total(self):
        parts = ["steel_frame", "v_brakes", "tubeless_tyre", "4_gear_assembly"]
        self.assertEqual(quote(date(2026, 10, 1), parts), 4850)

    def test_tube_with_tubeless_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(date(2026, 10, 1), ["tube", "tubeless_tyre"])

    def test_unknown_part_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(date(2026, 1, 1), ["non_existent_part"])

    def test_date_before_catalog_is_rejected(self):
        with self.assertRaises(ValueError):
            quote(date(2025, 12, 31), ["steel_frame"])

    def test_netlify_prices_match_python(self):
        with open("netlify/functions/parts.json") as f:
            web = json.load(f)
        py = {k: {"name": p.name, "component": p.component,
                  "prices": [[e.price, e.valid_from.isoformat(), e.valid_until and e.valid_until.isoformat()]
                             for e in p.price_history]}
              for k, p in parts_db.items()}
        self.assertEqual(web, py)


if __name__ == "__main__":
    unittest.main()
