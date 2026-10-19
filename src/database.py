import os
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from src.models import Part, PriceEntry

DB_PATH = os.environ.get("HERO_DB", "hero_cycles.db")

SEED = {
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


@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db():
    with connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS parts (id TEXT PRIMARY KEY, name TEXT NOT NULL, component TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS prices (
                part_id TEXT NOT NULL REFERENCES parts(id),
                price REAL NOT NULL,
                valid_from TEXT NOT NULL,
                valid_until TEXT,
                PRIMARY KEY (part_id, valid_from)
            );
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                quote_date TEXT NOT NULL,
                total REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS quote_items (
                quote_id INTEGER NOT NULL REFERENCES quotes(id),
                name TEXT NOT NULL,
                component TEXT NOT NULL,
                price REAL NOT NULL
            );
        """)
        if conn.execute("SELECT COUNT(*) FROM parts").fetchone()[0] == 0:
            for part_id, part in SEED.items():
                conn.execute("INSERT INTO parts VALUES (?, ?, ?)", (part_id, part.name, part.component))
                conn.executemany("INSERT INTO prices VALUES (?, ?, ?, ?)", [
                    (part_id, e.price, e.valid_from.isoformat(), e.valid_until and e.valid_until.isoformat())
                    for e in part.price_history])


def load_parts():
    with connect() as conn:
        parts = {r["id"]: Part(r["name"], r["component"], [])
                 for r in conn.execute("SELECT * FROM parts ORDER BY rowid")}
        for r in conn.execute("SELECT * FROM prices ORDER BY valid_from"):
            parts[r["part_id"]].price_history.append(PriceEntry(
                r["price"], date.fromisoformat(r["valid_from"]),
                r["valid_until"] and date.fromisoformat(r["valid_until"])))
    return parts


def add_price(part_id, price, start):
    if price <= 0:
        raise ValueError("Price must be more than 0.")
    with connect() as conn:
        if not conn.execute("SELECT 1 FROM parts WHERE id = ?", (part_id,)).fetchone():
            raise ValueError(f"Unknown part: '{part_id}'.")
        day = start.isoformat()
        current = conn.execute(
            "SELECT * FROM prices WHERE part_id = ? AND valid_from <= ? AND (valid_until IS NULL OR ? < valid_until)",
            (part_id, day, day)).fetchone()
        if current and current["valid_from"] == day:
            conn.execute("UPDATE prices SET price = ? WHERE part_id = ? AND valid_from = ?", (price, part_id, day))
            return
        if current:
            until = current["valid_until"]
            conn.execute("UPDATE prices SET valid_until = ? WHERE part_id = ? AND valid_from = ?",
                         (day, part_id, current["valid_from"]))
        else:
            nxt = conn.execute("SELECT MIN(valid_from) FROM prices WHERE part_id = ? AND valid_from > ?",
                               (part_id, day)).fetchone()[0]
            until = nxt
        conn.execute("INSERT INTO prices VALUES (?, ?, ?, ?)", (part_id, price, day, until))


def save_quote(quote_date, total, items):
    with connect() as conn:
        quote_id = conn.execute("INSERT INTO quotes (created_at, quote_date, total) VALUES (?, ?, ?)",
                                (datetime.now().isoformat(timespec="seconds"), quote_date.isoformat(), total)).lastrowid
        conn.executemany("INSERT INTO quote_items VALUES (?, ?, ?, ?)",
                         [(quote_id, i["name"], i["component"], i["price"]) for i in items])
    return quote_id


def list_quotes(limit=20):
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM quotes ORDER BY id DESC LIMIT ?", (limit,))]


def get_quote(quote_id):
    with connect() as conn:
        quote = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
        if quote is None:
            return None
        items = conn.execute("SELECT name, component, price FROM quote_items WHERE quote_id = ? ORDER BY rowid",
                             (quote_id,))
        return {**dict(quote), "items": [dict(i) for i in items]}
