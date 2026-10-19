from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src import database as db
from src.engine import calculate_quote
from src.models import CycleConfiguration

app = FastAPI()
db.init_db()


class QuoteRequest(BaseModel):
    date: str
    parts: list[str]


class PriceChange(BaseModel):
    part_id: str
    price: float
    valid_from: str


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Pick a valid date.")


def quote_for(request):
    quote_date = parse_date(request.date)
    try:
        total, items = calculate_quote(CycleConfiguration(quote_date, request.parts), db.load_parts())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return quote_date, total, items


@app.get("/api/parts")
def get_parts():
    catalog = {}
    for part_id, part in db.load_parts().items():
        catalog.setdefault(part.component, {})[part_id] = part.name
    return catalog


@app.get("/api/prices")
def get_prices():
    return [{"id": part_id, "name": p.name, "component": p.component,
             "prices": [[e.price, e.valid_from.isoformat(), e.valid_until and e.valid_until.isoformat()]
                        for e in p.price_history]}
            for part_id, p in db.load_parts().items()]


@app.post("/api/prices")
def add_price(change: PriceChange):
    try:
        db.add_price(change.part_id, change.price, parse_date(change.valid_from))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@app.post("/api/calculate")
def get_quote(request: QuoteRequest):
    _, total, items = quote_for(request)
    return {"total": total, "items": items}


@app.post("/api/quotes")
def create_quote(request: QuoteRequest):
    quote_date, total, items = quote_for(request)
    return {"id": db.save_quote(quote_date, total, items)}


@app.get("/api/quotes")
def recent_quotes():
    return db.list_quotes()


@app.get("/api/quotes/{quote_id}")
def one_quote(quote_id: int):
    quote = db.get_quote(quote_id)
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found.")
    return quote


app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
