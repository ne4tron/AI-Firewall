from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Store logs in memory
logs = []

# Sample data model
class SampleData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Pass logs to template
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs})

@app.post("/sample_data")
async def sample_data(data: SampleData):
    # Simulate ML predictions
    rf_prediction = random.choice([0, 1])
    iso_prediction = random.choice(["Normal", "Anomaly"])

    # Save to logs
    log_entry = {
        "features": data.dict(),
        "RandomForest": rf_prediction,
        "IsolationForest": iso_prediction
    }
    logs.append(log_entry)

    return {
        "RandomForest_prediction": rf_prediction,
        "IsolationForest_prediction": iso_prediction
    }

