# HanapBahay ML Service - Local Setup Instructions

This guide helps you migrate from Google Colab to a local Python ML service.

## Prerequisites

1. **Python 3.9 or higher** installed on your system
2. **pip** (Python package manager)
3. Your trained model artifacts from Colab

## Step 1: Download Model Artifacts from Colab

In your Colab notebook, run this cell to download the model files:

```python
# Download model artifacts from Colab
from google.colab import files
import os

# Zip the artifacts directory
!zip -r hanapbahay_artifacts.zip /content/hanapbahay_artifacts/

# Download the zip file
files.download('hanapbahay_artifacts.zip')
```

## Step 2: Extract Model Files

1. Extract `hanapbahay_artifacts.zip` to `ml_service/artifacts/`
2. You should have these files:
   - `ml_service/artifacts/model_latest.joblib`
   - `ml_service/artifacts/meta.json`

## Step 3: Install Python Dependencies

Open Command Prompt in the `ml_service` directory and run:

```bash
cd c:\xampp\htdocs\public_html\ml_service
python -m pip install -r requirements.txt
```

## Step 4: Test the ML Service

```bash
# Set API key (optional, for security)
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

# Start the service
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Step 5: Test the API

Open a new terminal and test:

```bash
# Test version endpoint (no auth)
curl http://localhost:8000/version

# Test prediction (with auth)
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -H "X-API-KEY: hanapbahay_ml_local_2024" ^
  -d "{\"inputs\":[{\"Capacity\":2,\"Bedroom\":1,\"unit_sqm\":20,\"cap_per_bedroom\":2,\"Type\":\"Apartment\",\"Kitchen\":\"Yes\",\"Kitchen type\":\"Private\",\"Gender specific\":\"Mixed\",\"Pets\":\"Allowed\",\"Location\":\"Quezon City\"}]}"
```

## Step 6: Update PHP Configuration

Edit `includes/config.php`:

```php
// OLD (Colab + ngrok)
// define('ML_BASE', 'https://revolvingly-uncombining-genia.ngrok-free.dev');
// define('ML_KEY', 'hanapbahay_ml_secure_2024_permanent_key_v1');

// NEW (Local Python service)
define('ML_BASE', 'http://127.0.0.1:8000');
define('ML_KEY', 'hanapbahay_ml_local_2024');
```

## Step 7: Run as Background Service (Production)

### Option A: Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When the computer starts"
4. Action: "Start a program"
5. Program: `C:\path\to\python.exe`
6. Arguments: `C:\xampp\htdocs\public_html\ml_service\app.py`

### Option B: Using NSSM (Non-Sucking Service Manager)

```bash
# Download NSSM from https://nssm.cc/download

# Install as Windows service
nssm install HanapBahayML "C:\path\to\python.exe" "C:\xampp\htdocs\public_html\ml_service\app.py"
nssm start HanapBahayML
```

### Option C: Simple Batch Script

Create `ml_service/start_service.bat`:

```batch
@echo off
cd /d "%~dp0"
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024
python app.py
```

Then run it on system startup.

## Training Models Locally (Optional)

If you want to train models directly from your database instead of using Colab:

### 1. Set Environment Variables

```bash
set DB_TYPE=mysql
set DB_HOST=localhost
set DB_PORT=3306
set DB_NAME=u412552698_dbhanapbahay
set DB_USER=root
set DB_PASS=yourpassword
```

### 2. Create Training Script

Copy your Colab training cells into `train_model.py` and modify to use `db_connector.py`:

```python
from db_connector import fetch_training_data, calculate_derived_features

# Fetch data from database
df = fetch_training_data()
df = calculate_derived_features(df)

# Continue with your existing training code...
```

### 3. Run Training

```bash
python train_model.py
```

This will save new artifacts to `ml_service/artifacts/`.

## Troubleshooting

### Port 8000 already in use

```bash
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module not found errors

```bash
python -m pip install --upgrade -r requirements.txt
```

### Model file not found

Make sure you extracted the artifacts to the correct location:
- `ml_service/artifacts/model_latest.joblib`
- `ml_service/artifacts/meta.json`

## Advantages of Local Setup

✅ **No external dependencies** - No need for Colab or ngrok
✅ **Faster predictions** - Local network, no internet latency
✅ **More secure** - API runs locally, not exposed to internet
✅ **Always available** - No Colab timeouts or session limits
✅ **Database integration** - Can train directly from your database
✅ **Free** - No costs for Colab Pro or ngrok domains

## Next Steps

- Set up automatic model retraining (weekly/monthly)
- Add monitoring and logging
- Create model versioning system
- Add A/B testing for new models