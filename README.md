# HanapBahay ML Service

Local Python-based machine learning service for HanapBahay rental price predictions.

## 🎯 What This Does

Replaces Google Colab + ngrok with a **local Python FastAPI service** that runs on your Windows machine.

### Benefits

✅ **No external dependencies** - Runs locally, no internet required
✅ **Faster** - Local network, no ngrok latency
✅ **More secure** - Not exposed to public internet
✅ **Always available** - No Colab session timeouts
✅ **Free** - No Colab Pro or ngrok costs
✅ **Database integration** - Can train models directly from MySQL/PostgreSQL

## 📁 File Structure

```
ml_service/
├── app.py                      # FastAPI ML service
├── requirements.txt            # Python dependencies
├── db_connector.py            # Database connection (optional)
├── start_service.bat          # Start service manually
├── install_service.bat        # Install as Windows service
├── test_service.bat           # Test endpoints
├── artifacts/                 # Model files (download from Colab)
│   ├── model_latest.joblib
│   └── meta.json
├── SETUP_INSTRUCTIONS.md      # Detailed setup guide
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Download Model Files from Colab

In your Colab notebook, run:

```python
from google.colab import files
!zip -r hanapbahay_artifacts.zip /content/hanapbahay_artifacts/
files.download('hanapbahay_artifacts.zip')
```

Extract to `ml_service/artifacts/`

### 2. Install Dependencies

```bash
cd ml_service
python -m pip install -r requirements.txt
```

### 3. Start the Service

**Option A: Manual (for testing)**
```bash
start_service.bat
```

**Option B: Windows Service (for production)**
```bash
# Run as Administrator
install_service.bat
```

### 4. Test It

```bash
test_service.bat
```

Or test with PHP:
```bash
cd ..
php -l api/ml_suggest_price.php
curl -X POST http://localhost/api/ml_suggest_price.php ^
  -H "Content-Type: application/json" ^
  -d "{\"inputs\":[{\"Capacity\":2,\"Bedroom\":1,\"unit_sqm\":20,\"cap_per_bedroom\":2,\"Type\":\"Apartment\",\"Kitchen\":\"Yes\",\"Kitchen type\":\"Private\",\"Gender specific\":\"Mixed\",\"Pets\":\"Allowed\",\"Location\":\"Quezon City\"}]}"
```

## 🔧 Configuration

The service reads configuration from:
- **Environment variables** (recommended for security)
- **Default values** (fallback)

### API Key

Set via environment variable:
```bash
set HANAPBAHAY_API_KEY=your_secure_key_here
```

Or edit `start_service.bat` or `app.py`

### Database (Optional - for training)

```bash
set DB_TYPE=mysql
set DB_HOST=localhost
set DB_PORT=3306
set DB_NAME=u412552698_dbhanapbahay
set DB_USER=root
set DB_PASS=yourpassword
```

## 📡 API Endpoints

### `GET /version`
- **Auth:** None (public)
- **Returns:** Version and feature info

### `GET /health`
- **Auth:** Required (X-API-KEY header)
- **Returns:** Service health status

### `POST /predict`
- **Auth:** Required (X-API-KEY header)
- **Body:**
  ```json
  {
    "inputs": [{
      "Capacity": 2,
      "Bedroom": 1,
      "unit_sqm": 20,
      "cap_per_bedroom": 2,
      "Type": "Apartment",
      "Kitchen": "Yes",
      "Kitchen type": "Private",
      "Gender specific": "Mixed",
      "Pets": "Allowed",
      "Location": "Quezon City"
    }]
  }
  ```
- **Returns:** Price predictions

### `POST /price_interval`
- **Auth:** Required (X-API-KEY header)
- **Body:**
  ```json
  {
    "inputs": [...],
    "noise": 0.08
  }
  ```
- **Returns:** Price ranges (low, pred, high)

## 🔄 Training Models Locally

Instead of using Colab, you can train models directly from your database:

1. Set database environment variables
2. Create `train_model.py`:
   ```python
   from db_connector import fetch_training_data, calculate_derived_features

   # Fetch data
   df = fetch_training_data()
   df = calculate_derived_features(df)

   # Train model (copy your Colab training code here)
   # ...

   # Save artifacts
   joblib.dump(model, 'artifacts/model_latest.joblib')
   ```

3. Run: `python train_model.py`

## 🐛 Troubleshooting

### Service won't start

1. Check Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Verify model files exist: `dir artifacts\`

### Port 8000 in use

```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Predictions fail

1. Check model files are present
2. Verify API key matches in PHP config
3. Test with `test_service.bat`

### PHP can't connect

1. Ensure service is running: `curl http://localhost:8000/version`
2. Check [config.php](c:\xampp\htdocs\public_html\includes\config.php:11) has correct URL
3. Verify API key matches

## 📚 Documentation

- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Detailed setup guide
- [app.py](app.py) - Service source code
- [db_connector.py](db_connector.py) - Database integration

## 🔐 Security Notes

- The service runs on `127.0.0.1` (localhost only) by default
- Change API key in production
- Use environment variables for secrets
- Don't expose port 8000 to the internet

## 📞 Support

If you encounter issues:
1. Check logs in the terminal where service is running
2. Review [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
3. Test with `test_service.bat`
