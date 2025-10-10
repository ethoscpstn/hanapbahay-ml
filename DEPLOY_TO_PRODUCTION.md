# Deploy ML Service to Production

## ✅ Files Ready for Deployment

Your `ml_service` folder now includes:
- ✅ `app.py` (updated for cloud deployment)
- ✅ `requirements.txt` (dependencies)
- ✅ `Procfile` (deployment command)
- ✅ `runtime.txt` (Python version)
- ✅ `.gitignore` (files to exclude)
- ✅ `artifacts/` (model files)

---

## 🚀 Recommended: Railway.app (5 Minutes Setup)

### Step 1: Create GitHub Repository

```bash
cd c:\xampp\htdocs\public_html\ml_service

# Initialize git
git init
git add .
git commit -m "Initial ML service deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hanapbahay-ml.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click "Login" → Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `hanapbahay-ml` repository
6. Railway auto-deploys! ⚡

### Step 3: Add Environment Variable

1. Click your project
2. Go to "Variables" tab
3. Click "New Variable"
   - Key: `HANAPBAHAY_API_KEY`
   - Value: `your_secure_production_key_123`
4. Click "Add"

### Step 4: Get Your Public URL

Railway generates a URL like:
```
https://hanapbahay-ml-production-abc123.up.railway.app
```

Copy this URL!

### Step 5: Update Production PHP

SSH/FTP to your Hostinger server and edit `includes/config.php`:

```php
<?php
// Machine Learning Service Configuration

if ($_SERVER['HTTP_HOST'] === 'localhost') {
    // Local development
    define('ML_BASE', 'http://127.0.0.1:8000');
    define('ML_KEY', 'hanapbahay_ml_local_2024');
} else {
    // Production (hanapbahay.online)
    define('ML_BASE', 'https://hanapbahay-ml-production-abc123.up.railway.app');
    define('ML_KEY', 'your_secure_production_key_123');
}
```

### Step 6: Test Production

```bash
# Test Railway deployment
curl https://hanapbahay-ml-production-abc123.up.railway.app/version

# Test from your website
curl https://hanapbahay.online/api/ml_suggest_price.php \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"Capacity":2,"Bedroom":1,"unit_sqm":20,"cap_per_bedroom":2,"Type":"Apartment","Kitchen":"Yes","Kitchen type":"Private","Gender specific":"Mixed","Pets":"Allowed","Location":"Quezon City"}]}'
```

---

## 🎯 Alternative: Render.com

Follow similar steps:

1. Push to GitHub (same as above)
2. Go to https://render.com
3. Sign up with GitHub
4. "New" → "Web Service"
5. Connect repository
6. Add environment variable
7. Deploy!

Your URL will be: `https://hanapbahay-ml.onrender.com`

**Note:** Free tier spins down after 15 min inactivity (first request takes ~30 seconds to wake up)

---

## 💰 Cost Comparison

| Platform | Free Tier | After Free | Best For |
|----------|-----------|------------|----------|
| **Railway** | $5 credit/mo (~500 hrs) | Pay per use (~$5-10/mo) | Active sites |
| **Render** | 750 hrs/mo | $7/mo | Low-traffic sites |
| **PythonAnywhere** | Very limited | $5/mo | Beginners |

---

## 🔒 Security Tips

1. **Change API Key:**
   ```python
   # Use strong random key for production
   import secrets
   secrets.token_urlsafe(32)
   ```

2. **Enable CORS only for your domain:**
   In `app.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://hanapbahay.online"],  # Only your domain
       allow_methods=["POST"],
       allow_headers=["*"],
   )
   ```

3. **Monitor usage:**
   - Check Railway/Render dashboard regularly
   - Set up billing alerts

---

## 📊 After Deployment

### Your Architecture Will Be:

```
User Browser
    ↓
hanapbahay.online (Hostinger - PHP)
    ↓
Railway/Render (ML Service - Python)
    ↓
Returns price prediction
```

### Development vs Production:

**Local (Development):**
- Windows PC → Anaconda → ML Service (localhost:8000)
- XAMPP → PHP → ML Service

**Production (Live Website):**
- User → hanapbahay.online → Railway ML Service
- Always available, no need to run anything locally

---

## 🔄 Updating the Model

When you retrain in Colab:

1. Download new artifacts
2. Replace in `ml_service/artifacts/`
3. Commit and push:
   ```bash
   git add artifacts/
   git commit -m "Update ML model"
   git push
   ```
4. Railway/Render auto-deploys!

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Deployed to Railway/Render
- [ ] Environment variable set
- [ ] Public URL obtained
- [ ] Production PHP config updated
- [ ] Tested /version endpoint
- [ ] Tested /predict endpoint
- [ ] Tested from live website

---

## 🆘 Troubleshooting

**"Application failed to respond"**
- Check logs in Railway/Render dashboard
- Verify model files are in artifacts/
- Check environment variable is set

**"401 Unauthorized"**
- API key in Railway matches PHP config
- Check header is `X-API-KEY` (case-sensitive)

**"Module not found"**
- Verify requirements.txt has all dependencies
- Check build logs in dashboard

---

Ready to deploy? Start with Railway.app - it's the easiest!
