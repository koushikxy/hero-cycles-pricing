# Hero Cycles Pricing Engine

![tests](https://github.com/koushikxy/hero-cycles-pricing/actions/workflows/tests.yml/badge.svg)

A pricing tool for the Hero Cycles sales team. Part prices change over time, so every quote is priced for a chosen date.

Live demo: https://hero-cycles-pricing.netlify.app

## What it does

- Looks up each part's price for the quote date. A price starts on its `valid_from` day and stops the day before `valid_until`, so a change day always gets the new price.
- Rejects a tubeless tyre together with a tube, unknown part IDs, and dates that have no price, instead of quietly leaving them out of the total.
- Prices live in SQLite. The Prices page shows each part's price history and lets you add a price change from any date; the current window is split so older quotes are not affected.
- Quotes can be saved. Each saved quote keeps the prices it was made with and opens as a printable page that can be saved as a PDF.
- A CLI reads a JSON quote request and prints the price grouped by component.

Built with Python, FastAPI, SQLite and plain HTML/CSS/JavaScript. GitHub Actions runs the tests on every push.

## Setup

Needs Python 3.9 or newer.

```bash
git clone https://github.com/koushikxy/hero-cycles-pricing.git
cd hero-cycles-pricing
pip install -r requirements.txt
```

The database file `hero_cycles.db` is created and filled with the starting prices the first time the app or CLI runs. Delete it to start over.

## Web app

```bash
python -m uvicorn main:app --reload
```

Then open http://127.0.0.1:8000. The Prices page is at `/admin.html`.

## CLI

```bash
python cli.py
python cli.py --config my_quote.json
```

It reads `quote_request.json` by default:

```
Cycle Price Breakdown - 15 Dec 2026
----------------------------------------
Frame: ₹1,300
Handle Bar & Brakes: ₹1,220
Seating: ₹420
Tyres: ₹1,650
Rims: ₹370
Chain Assembly: ₹1,000
----------------------------------------
TOTAL: ₹5,960
```

## API

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/api/parts` | Parts grouped by component |
| POST | `/api/calculate` | Price a list of parts for a date |
| GET | `/api/prices` | Every part with its price history |
| POST | `/api/prices` | Add a price change |
| POST | `/api/quotes` | Price and save a quote |
| GET | `/api/quotes` | Last 20 saved quotes |
| GET | `/api/quotes/{id}` | One saved quote with its items |

## Tests

```bash
python -m unittest test_engine.py
npm test
```

The Python tests cover prices before, after and on a change day, the tube/tubeless conflict, unknown parts, dates with no price, adding price changes, saved quotes keeping their prices, and that the Netlify starting prices match the Python ones. `npm test` runs the same kind of checks against the Netlify function.

## Live demo

Netlify only serves static files and functions, so the demo runs the API as a JavaScript function (`netlify/functions/api.mjs`) with the same rules, storing prices and quotes in Netlify Blobs instead of SQLite. Anyone can change prices on the demo.

## Files

- `src/` - models, database and pricing engine
- `ui/` - quote page, prices page and printable quote
- `main.py` - FastAPI server
- `cli.py` - command-line tool
- `test_engine.py` - Python tests
- `tests/` - tests for the Netlify function
- `quote_request.json` - sample CLI input
- `netlify/` - serverless version of the API for the live demo
- `Thinking.md` - problem breakdown and data model
- `UI_NOTES.md` - UI decisions
