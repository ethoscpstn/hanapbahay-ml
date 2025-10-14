"""
HanapBahay ML Service - Local Python FastAPI Server
Replaces Google Colab + ngrok with local deployment
"""
import os
import json
import joblib
import sklearn
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

print(f"[startup] scikit-learn version: {sklearn.__version__}", flush=True)
# Configuration
ART_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')
MODEL_PATH = os.path.join(ART_DIR, 'model_latest.joblib')
META_PATH = os.path.join(ART_DIR, 'meta.json')
API_KEY = os.environ.get('HANAPBAHAY_API_KEY', 'hanapbahay_ml_local_2024')

# Load model and metadata
_model = None
_meta = None

def load_artifacts():
    global _model, _meta
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    if not os.path.exists(META_PATH):
        raise FileNotFoundError(f"Metadata not found: {META_PATH}")

    _model = joblib.load(MODEL_PATH)
    with open(META_PATH, 'r') as f:
        _meta = json.load(f)

load_artifacts()

FEATURES = _meta.get("features", [])
VERSION = _meta.get("version", "local")

# Pydantic models
class PredictRequest(BaseModel):
    inputs: List[Dict[str, Any]] = Field(..., description="Input features for prediction")

class PredictResponse(BaseModel):
    version: str
    n: int
    predictions: List[float]

class IntervalRequest(BaseModel):
    inputs: List[Dict[str, Any]]
    noise: float = 0.08

class IntervalResponse(BaseModel):
    version: str
    n: int
    intervals: List[Dict[str, float]]

class HealthResponse(BaseModel):
    status: str
    version: str
    features: List[str]

# FastAPI app
app = FastAPI(title="HanapBahay ML API", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def require_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

def prepare_df(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare input DataFrame with expected features"""
    df = pd.DataFrame(rows)

    # Add missing features with defaults
    for f in FEATURES:
        if f not in df.columns:
            df[f] = 0

    # Enforce column order
    return df[FEATURES]

@app.get("/health", response_model=HealthResponse)
def health(x_api_key: Optional[str] = Header(default=None, alias="X-API-KEY")):
    require_key(x_api_key)
    return HealthResponse(
        status="ok",
        version=VERSION,
        features=FEATURES
    )

@app.get("/version")
def version():
    """Public endpoint - no auth required"""
    return {
        "version": VERSION,
        "features": FEATURES,
        "status": "running"
    }

@app.post("/predict", response_model=PredictResponse)
def predict(
    req: PredictRequest,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-KEY")
):
    require_key(x_api_key)
    try:
        df = prepare_df(req.inputs)
        predictions = _model.predict(df)
        return PredictResponse(
            version=VERSION,
            n=len(predictions),
            predictions=[float(p) for p in predictions]
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Prediction error: {str(e)}")

@app.post("/price_interval", response_model=IntervalResponse)
def price_interval(
    req: IntervalRequest,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-KEY")
):
    require_key(x_api_key)
    try:
        df = prepare_df(req.inputs)
        predictions = _model.predict(df)

        intervals = []
        for pred in predictions:
            intervals.append({
                "low": float(pred * (1 - req.noise)),
                "pred": float(pred),
                "high": float(pred * (1 + req.noise))
            })

        return IntervalResponse(
            version=VERSION,
            n=len(intervals),
            intervals=intervals
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Interval calculation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Read PORT from environment (for cloud deployment) or default to 8000 (for local)
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    uvicorn.run(app, host=host, port=port)
