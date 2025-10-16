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

# ===== AMENITIES UPLIFT FUNCTIONALITY =====

def _as_bool(v):
    """Normalize a YES/NO/checkbox-ish amenity value from incoming rows"""
    if v is None:
        return False
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    return s in {"1", "y", "yes", "true", "on", "checked"}

# Map UI amenity labels -> column names you pass in rows
AMENITY_FIELDS = {
    "Wi-Fi": "Wi-Fi",
    "Parking": "Parking", 
    "Air Conditioning": "Air Conditioning",
    "Kitchen": "Kitchen",  # already a feature, still ok
    "Laundry": "Laundry",
    "Furnished": "Furnished",
    "Security/CCTV": "Security/CCTV",
    "Balcony": "Balcony",
    "Elevator": "Elevator",
    "Gym": "Gym",
    "Pool": "Pool",
    "Pet Friendly": "Pet Friendly",
    "Bathroom": "Bathroom",
    "Sink": "Sink",
    "Electricity (Submeter)": "Electricity (Submeter)",
    "Water (Submeter)": "Water (Submeter)",
}

# Tunable percentage uplifts per amenity (very modest by default)
AMENITY_UPLIFT = {
    "Wi-Fi": 0.01,   # +1%
    "Parking": 0.02,   # +2%
    "Air Conditioning": 0.03,   # +3%
    "Kitchen": 0.00,   # already priced via core features
    "Laundry": 0.01,
    "Furnished": 0.05,   # bigger effect
    "Security/CCTV": 0.01,
    "Balcony": 0.02,
    "Elevator": 0.01,
    "Gym": 0.02,
    "Pool": 0.03,
    "Pet Friendly": 0.01,
    "Bathroom": 0.00,   # baseline assumption: 1 bathroom
    "Sink": 0.00,
    "Electricity (Submeter)": 0.01,
    "Water (Submeter)": 0.01,
}

# Optional safety cap so amenities can't blow up the price
AMENITIES_UPLIFT_CAP = 0.15   # ≤ +15% total

def amenity_uplift_factor(row: dict) -> float:
    """
    Compute 1 + uplift from amenities found in `row`.
    Adds small % per amenity; capped by AMENITIES_UPLIFT_CAP.
    """
    uplift = 0.0
    for label, key in AMENITY_FIELDS.items():
        if _as_bool(row.get(key)):
            uplift += AMENITY_UPLIFT.get(label, 0.0)
    if uplift > AMENITIES_UPLIFT_CAP:
        uplift = AMENITIES_UPLIFT_CAP
    return 1.0 + uplift

def predict_price_with_uplift(rows: List[Dict[str, Any]]) -> List[float]:
    """
    Post-prediction calibration that layers amenity uplift over the raw pipeline prediction.
    """
    # Get base predictions using only core features
    df = prepare_df(rows)
    base_predictions = _model.predict(df)
    
    # Apply amenities uplift
    out = []
    for row, base_pred in zip(rows, base_predictions):
        uplift_factor = amenity_uplift_factor(row)
        adjusted_price = float(base_pred) * uplift_factor
        out.append(adjusted_price)
    
    return out

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
        # Use amenities uplift functionality
        predictions = predict_price_with_uplift(req.inputs)
        return PredictResponse(
            version=VERSION,
            n=len(predictions),
            predictions=predictions
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
        # Use amenities uplift functionality for predictions
        predictions = predict_price_with_uplift(req.inputs)

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