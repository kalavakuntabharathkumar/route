from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database import seed_shipments, get_shipment
from .agent import run_agent

app = FastAPI(title="RouteAgent", version="1.0.0")
seed_shipments()

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/shipments/{tracking_id}")
def shipment(tracking_id: str):
    item = get_shipment(tracking_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return item

@app.get("/shipments/{tracking_id}/risk")
def risk(tracking_id: str):
    result = run_agent(f"Give delay risk for {tracking_id}")
    return result["results"][-1]["result"]

@app.post("/agent/query")
def query(payload: Query):
    return run_agent(payload.query)
