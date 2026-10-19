from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.engine import calculate_quote
from src.models import CycleConfiguration
from src.database import parts_db

app = FastAPI()


class QuoteRequest(BaseModel):
    date: str
    parts: list[str]


@app.get("/api/parts")
def get_parts():
    catalog = {}
    for part_id, part in parts_db.items():
        catalog.setdefault(part.component, {})[part_id] = part.name
    return catalog


@app.post("/api/calculate")
def get_quote(request: QuoteRequest):
    try:
        quote_date = date.fromisoformat(request.date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Pick a valid date.")
    try:
        total, items = calculate_quote(CycleConfiguration(quote_date, request.parts))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"total": total, "items": items}


app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
