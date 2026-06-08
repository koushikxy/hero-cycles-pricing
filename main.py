from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import date
from src.engine import calculate_quote
from src.models import CycleConfiguration
from src.database import parts_db

app = FastAPI()

class QuoteRequest(BaseModel):
    date: str
    parts: list

@app.get("/api/parts")
def get_parts():
    # This gathers the parts and components from your database.py
    # and sends them to the browser as a JSON object.
    catalog = {}
    for part_id, part in parts_db.items():
        comp = part.component
        if comp not in catalog:
            catalog[comp] = {}
        catalog[comp][part_id] = part.name
    return catalog

@app.post("/api/calculate")
def get_quote(request: QuoteRequest):
    try:
        config = CycleConfiguration(
            config_date=date.fromisoformat(request.date),
            parts=request.parts
        )
        total, items = calculate_quote(config)
        return {"total": total, "items": items}
    
    except ValueError as e:
        # This catches the error from engine.py and sends it to the UI
        raise HTTPException(status_code=400, detail=str(e))

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")