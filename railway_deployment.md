# Deploy to Railway.app

## What is Railway?
Railway is a deployment platform that makes it easy to deploy Python apps with zero configuration.

## Prerequisites
- GitHub account
- Your ML service files (already have them!)

---

## Step 1: Prepare Files

Create these files in `ml_service/` directory:

### 1. `runtime.txt`
```
python-3.11.0
```

### 2. `Procfile`
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

### 3. `.gitignore`
```
__pycache__/
*.pyc
.env
*.log
artifacts/backup/
```

### 4: Update `app.py` to read PORT from environment

Add this near the top of app.py:
```python
import os
PORT = int(os.environ.get("PORT", 8000))
```

And at the bottom, change:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository: `hanapbahay-ml-service`
3. Don't initialize with README

In your local `ml_service` folder:
```bash
git init
git add .
git commit -m "Initial commit - ML service"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hanapbahay-ml-service.git
git push -u origin main
```

---

## Step 3: Deploy to Railway

1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select `hanapbahay-ml-service`
6. Railway will auto-detect Python and deploy!

---

## Step 4: Set Environment Variables

In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add:
   ```
   HANAPBAHAY_API_KEY=your_secure_production_key
   ```

---

## Step 5: Get Your Public URL

Railway will give you a URL like:
```
https://hanapbahay-ml-service-production.up.railway.app
```

---

## Step 6: Update PHP on Production

In your Hostinger `includes/config.php`:
```php
// Production ML Service
define('ML_BASE', 'https://hanapbahay-ml-service-production.up.railway.app');
define('ML_KEY', 'your_secure_production_key');
```

---

## Step 7: Test It

```bash
curl https://hanapbahay-ml-service-production.up.railway.app/version
```

---

## Free Tier Limits
- $5 free credit per month
- Enough for ~500 hours runtime
- Perfect for small-medium traffic

---

## Cost After Free Tier
- ~$5-10/month for typical usage
- Only pay for what you use
