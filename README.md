# Hero Cycles Pricing Engine

A pricing tool for the Hero Cycles sales team. Part prices change over time, so every quote is priced for a chosen date.

Live demo: https://hero-cycles-pricing.netlify.app (the API runs there as a Netlify Function using the same price table and rules as the Python engine).

## What it does

- Looks up each part's price for the quote date. A price starts on its `valid_from` day and stops the day before `valid_until`, so a change day always gets the new price.
- Rejects a tubeless tyre together with a tube, unknown part IDs, and dates that have no price in the catalogue, instead of quietly leaving them out of the total.
- CLI reads a JSON quote request and prints the price grouped by component.
- Web page lets you pick parts and a date and updates the quote as you go.

Built with Python, FastAPI and plain HTML/CSS/JavaScript.

## Setup

Needs Python 3.9 or newer.

```bash
git clone https://github.com/koushikxy/hero-cycles-pricing.git
cd hero-cycles-pricing
pip install -r requirements.txt
```

The CLI and tests need nothing beyond Python; FastAPI and Uvicorn are only for the web page.

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

## Web page

```bash
python -m uvicorn main:app --reload
```

Then open http://127.0.0.1:8000.

## Tests

```bash
python -m unittest test_engine.py
```

The tests cover prices before and after a change, the change day itself, a full cycle, the tube/tubeless conflict, unknown parts, dates before the catalogue starts, and that the Netlify price table matches the Python one.

## Files

- `src/` - models, price table and pricing engine
- `ui/` - web page
- `main.py` - FastAPI server
- `cli.py` - command-line tool
- `test_engine.py` - tests
- `quote_request.json` - sample CLI input
- `netlify/` - serverless version of the API for the live demo
- `Thinking.md` - problem breakdown and data model
- `UI_NOTES.md` - UI decisions
