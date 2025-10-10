# Deploy to Render.com

## Why Render?
- Generous free tier (750 hours/month)
- Easy GitHub integration
- Auto-deploys on git push
- Free SSL certificates

---

## Step 1: Prepare Files

Create `render.yaml` in `ml_service/`:

```yaml
services:
  - type: web
    name: hanapbahay-ml
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: HANAPBAHAY_API_KEY
        sync: false
```

---

## Step 2: Update app.py for PORT

Add at the bottom of `app.py`:
```python
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## Step 3: Deploy

1. Push to GitHub (same as Railway steps)
2. Go to https://render.com/
3. Sign up with GitHub
4. Click "New" → "Web Service"
5. Connect your repository
6. Render auto-detects Python
7. Click "Create Web Service"

---

## Step 4: Set Environment Variable

In Render dashboard:
1. Go to "Environment"
2. Add: `HANAPBAHAY_API_KEY` = `your_key`
3. Save changes

---

## Step 5: Get Your URL

Render gives you:
```
https://hanapbahay-ml.onrender.com
```

---

## Free Tier Limits
- Services spin down after 15 min inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month free

---

## Keeping Service Awake (Optional)

Use a free uptime monitor:
- https://uptimerobot.com
- Ping your service every 14 minutes
