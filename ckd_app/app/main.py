from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from .schemas import PatientInput, PredictionOutput
from .model import predict_stage, load_model

app = FastAPI(title="CKD Prediction App")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_model=PredictionOutput)
async def predict(data: PatientInput):
    try:
        stage, probabilities = predict_stage(data)
        return PredictionOutput(stage=stage, probabilities=probabilities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
