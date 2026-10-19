import json
import os
import tempfile
import unittest
from datetime import date

os.environ["HERO_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")

from src import database as db
from src.engine import calculate_quote
from src.models import CycleConfiguration


def quote(d, parts, catalog=db.SEED):
    return calculate_quote(CycleConfiguration(d, parts), catalog)[0]


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
              for k, p in db.SEED.items()}
        self.assertEqual(web, py)


class TestDatabase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(db.DB_PATH):
            os.remove(db.DB_PATH)
        db.init_db()

    def test_seeded_prices_match_seed(self):
        self.assertEqual(quote(date(2026, 12, 15), ["steel_frame", "spokes"], db.load_parts()), 1460)

    def test_new_price_splits_the_current_window(self):
        db.add_price("steel_frame", 1250, date(2026, 5, 1))
        parts = db.load_parts()
        self.assertEqual(quote(date(2026, 4, 30), ["steel_frame"], parts), 1200)
        self.assertEqual(quote(date(2026, 5, 1), ["steel_frame"], parts), 1250)
        self.assertEqual(quote(date(2026, 7, 31), ["steel_frame"], parts), 1250)
        self.assertEqual(quote(date(2026, 8, 1), ["steel_frame"], parts), 1300)

    def test_price_on_existing_start_day_replaces_it(self):
        db.add_price("steel_frame", 1999, date(2026, 8, 1))
        parts = db.load_parts()
        self.assertEqual(len(parts["steel_frame"].price_history), 3)
        self.assertEqual(quote(date(2026, 8, 1), ["steel_frame"], parts), 1999)

    def test_price_before_catalog_fills_the_gap(self):
        db.add_price("steel_frame", 1100, date(2025, 6, 1))
        parts = db.load_parts()
        self.assertEqual(quote(date(2025, 12, 31), ["steel_frame"], parts), 1100)
        self.assertEqual(quote(date(2026, 1, 1), ["steel_frame"], parts), 1200)

    def test_bad_price_changes_are_rejected(self):
        with self.assertRaises(ValueError):
            db.add_price("steel_frame", 0, date(2026, 5, 1))
        with self.assertRaises(ValueError):
            db.add_price("no_such_part", 100, date(2026, 5, 1))

    def test_saved_quote_keeps_its_prices(self):
        d = date(2026, 10, 1)
        total, items = calculate_quote(CycleConfiguration(d, ["steel_frame", "v_brakes"]), db.load_parts())
        quote_id = db.save_quote(d, total, items)
        db.add_price("steel_frame", 5000, date(2026, 9, 1))
        saved = db.get_quote(quote_id)
        self.assertEqual(saved["total"], 2200)
        self.assertEqual([i["price"] for i in saved["items"]], [1300, 900])
        self.assertEqual(db.list_quotes()[0]["id"], quote_id)
        self.assertIsNone(db.get_quote(quote_id + 1))


if __name__ == "__main__":
    unittest.main()
