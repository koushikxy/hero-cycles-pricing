from datetime import date

class PriceEntry:
    def __init__(self, price, valid_from, valid_until=None):
        self.price = price
        self.valid_from = valid_from
        self.valid_until = valid_until

class Part:
    def __init__(self, name, component, price_history):
        self.name = name
        self.component = component
        self.price_history = price_history

parts_db = {
    # --- Frame ---
    "steel_frame": Part("Steel Frame", "Frame", [
        PriceEntry(1200, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(1300, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(1400, date(2027, 1, 1), None)
    ]),
    "aluminium_frame": Part("Aluminium Frame", "Frame", [
        PriceEntry(2500, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(2600, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(2750, date(2027, 1, 1), None)
    ]),

    # --- Handle Bar & Brakes ---
    "standard_handlebar": Part("Standard Handlebar", "Handle Bar & Brakes", [
        PriceEntry(300, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(320, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(350, date(2027, 1, 1), None)
    ]),
    "v_brakes": Part("V-Brakes", "Handle Bar & Brakes", [
        PriceEntry(850, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(900, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(950, date(2027, 1, 1), None)
    ]),
    "disc_brakes": Part("Disc Brakes", "Handle Bar & Brakes", [
        PriceEntry(1200, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(1300, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(1400, date(2027, 1, 1), None)
    ]),

    # --- Seating ---
    "basic_saddle": Part("Basic Saddle", "Seating", [
        PriceEntry(400, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(420, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(450, date(2027, 1, 1), None)
    ]),
    "ergonomic_saddle": Part("Ergonomic Saddle", "Seating", [
        PriceEntry(700, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(750, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(800, date(2027, 1, 1), None)
    ]),

    # --- Rims & Accessories ---
    "standard_rim": Part("Standard Rim", "Rims", [
        PriceEntry(200, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(210, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(230, date(2027, 1, 1), None)
    ]),
    "tube": Part("Tube", "Rims", [
        PriceEntry(100, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(110, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(120, date(2027, 1, 1), None)
    ]),
    "spokes": Part("Spokes", "Rims", [
        PriceEntry(150, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(160, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(175, date(2027, 1, 1), None)
    ]),
    
    # --- Tyres ---
    "tubeless_tyre": Part("Tubeless Tyre", "Tyres", [
        PriceEntry(1580, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(1650, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(1750, date(2027, 1, 1), None)
    ]),
    "standard_tyre": Part("Standard Tyre", "Tyres", [
        PriceEntry(300, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(350, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(400, date(2027, 1, 1), None)
    ]),

    # --- Chain Assembly ---
    "single_speed_chain": Part("Single-Speed Chain", "Chain Assembly", [
        PriceEntry(500, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(525, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(550, date(2027, 1, 1), None)
    ]),
    "4_gear_assembly": Part("4-Gear Assembly", "Chain Assembly", [
        PriceEntry(950, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(1000, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(1100, date(2027, 1, 1), None)
    ]),
    "7_gear_assembly": Part("7-Gear Assembly", "Chain Assembly", [
        PriceEntry(1400, date(2026, 1, 1), date(2026, 8, 1)),
        PriceEntry(1500, date(2026, 8, 1), date(2027, 1, 1)),
        PriceEntry(1650, date(2027, 1, 1), None)
    ])
}