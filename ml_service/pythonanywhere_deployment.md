# Deploy to PythonAnywhere

## Why PythonAnywhere?
- Free tier available
- Web-based file upload (no git required)
- Easy for Python apps
- Good for beginners

---

## Free Tier Limitations
- One web app only
- CPU time limits
- Subdomain only (yourusername.pythonanywhere.com)
- Need paid plan for custom domain

---

## Step 1: Sign Up

1. Go to https://www.pythonanywhere.com/
2. Create free account

---

## Step 2: Upload Files

### Via Web Interface:
1. Go to "Files" tab
2. Create folder: `hanapbahay_ml`
3. Upload:
   - `app.py`
   - `requirements.txt`
   - Zip and upload `artifacts/` folder

### Or via Bash console:
1. Open "Bash" console
2. Clone your repo:
   ```bash
   git clone https://github.com/your_username/hanapbahay-ml-service.git
   ```

---

## Step 3: Install Dependencies

In Bash console:
```bash
cd hanapbahay_ml
pip install --user -r requirements.txt
```

---

## Step 4: Create WSGI File

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10

Edit the WSGI file:
```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/hanapbahay_ml'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['HANAPBAHAY_API_KEY'] = 'your_secure_key'

# Import the app
from app import app as application
```

---

## Step 5: Configure Web App

In the Web tab:
- Set working directory: `/home/yourusername/hanapbahay_ml`
- Enable HTTPS (free SSL)
- Reload web app

---

## Step 6: Get Your URL

Your service will be at:
```
https://yourusername.pythonanywhere.com
```

---

## Step 7: Update PHP

```php
define('ML_BASE', 'https://yourusername.pythonanywhere.com');
define('ML_KEY', 'your_secure_key');
```

---

## Upgrade for Custom Domain

To use hanapbahay.online/ml:
- Need paid plan ($5/month)
- Can map custom domain
- More CPU time
