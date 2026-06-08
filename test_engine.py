import unittest
from datetime import date
from src.models import CycleConfiguration
from src.engine import calculate_quote

class TestPricingEngine(unittest.TestCase):

    def test_pre_hike_pricing(self):
        """1. Verify correct pricing logic before price change (e.g., May 2026)."""
        config = CycleConfiguration(date(2026, 5, 1), ["steel_frame", "v_brakes"])
        # Steel Frame (1200) + V-Brakes (850) = 2050
        total, _ = calculate_quote(config)
        self.assertEqual(total, 2050.0)

    def test_post_hike_pricing(self):
        """2. Verify correct pricing logic after price change (e.g., Oct 2026)."""
        config = CycleConfiguration(date(2026, 10, 1), ["steel_frame", "v_brakes"])
        # Steel Frame (1300) + V-Brakes (900) = 2200
        total, _ = calculate_quote(config)
        self.assertEqual(total, 2200.0)

    def test_full_configuration_total(self):
        """3. Verify calculation of a full cycle configuration (Oct 2026 rates)."""
        config = CycleConfiguration(
            date(2026, 10, 1), 
            ["steel_frame", "v_brakes", "tubeless_tyre", "4_gear_assembly"]
        )
        # Frame(1300) + Brakes(900) + Wheels(1650) + Gears(1000) = 4850
        total, _ = calculate_quote(config)
        self.assertEqual(total, 4850.0)

    def test_invalid_part_handling(self):
        """4. Verify engine robustness when an invalid part ID is provided."""
        config = CycleConfiguration(date(2026, 1, 1), ["non_existent_part"])
        total, _ = calculate_quote(config)
        self.assertEqual(total, 0.0)

if __name__ == "__main__":
    unittest.main()