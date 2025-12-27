from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

# FastAPI app
app = FastAPI(title="AI Firewall Dashboard")

# Static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# In-memory log storage
logs: List[dict] = []

# Sample ML prediction logic
class SampleData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float

def mock_random_forest(data: SampleData):
    # Dummy rule: sum of features > 2 -> 1 else 0
    return 1 if sum(data.dict().values()) > 2 else 0

def mock_isolation_forest(data: SampleData):
    # Dummy rule: any feature < 0.1 -> anomaly
    return "Anomaly" if any(v < 0.1 for v in data.dict().values()) else "Normal"

# Root dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs})

# Endpoint for adding sample data
@app.post("/sample_data")
async def add_sample_data(data: SampleData):
    rf_pred = mock_random_forest(data)
    iso_pred = mock_isolation_forest(data)
    log_entry = {
        **data.dict(),
        "RandomForest_prediction": rf_pred,
        "IsolationForest_prediction": iso_pred
    }
    logs.append(log_entry)
    return JSONResponse(log_entry)

