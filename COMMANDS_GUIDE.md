# HanapBahay ML Service - Command Reference Guide

## 🚀 Quick Start Commands

### **Daily Usage - Start ML Service**

**Open Anaconda Prompt and run:**
```bash
conda activate hanapbahay
cd c:\xampp\htdocs\public_html\ml_service
python app.py
```

**That's it!** Keep this window open while working.

---

## 📋 Common Commands

### **1. Start ML Service (Anaconda Prompt)**
```bash
# Activate environment
conda activate hanapbahay

# Navigate to ML service directory
cd c:\xampp\htdocs\public_html\ml_service

# Start the service
python app.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### **2. Test ML Service (Regular CMD/PowerShell)**

**Open a NEW Command Prompt window (keep ML service running in Anaconda)**

```bash
# Test if service is running
curl http://localhost:8000/version

# Test prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -H "X-API-KEY: hanapbahay_ml_local_2024" -d "{\"inputs\":[{\"Capacity\":2,\"Bedroom\":1,\"unit_sqm\":20,\"cap_per_bedroom\":2,\"Type\":\"Apartment\",\"Kitchen\":\"Yes\",\"Kitchen type\":\"Private\",\"Gender specific\":\"Mixed\",\"Pets\":\"Allowed\",\"Location\":\"Quezon City\"}]}"

# Or use the test script
cd c:\xampp\htdocs\public_html\ml_service
test_service.bat
```

---

### **3. Test PHP Integration (CMD)**

```bash
# Make sure XAMPP Apache is running first!

# Test PHP endpoint
curl -X POST http://localhost/api/ml_suggest_price.php -H "Content-Type: application/json" -d "{\"inputs\":[{\"Capacity\":2,\"Bedroom\":1,\"unit_sqm\":20,\"cap_per_bedroom\":2,\"Type\":\"Apartment\",\"Kitchen\":\"Yes\",\"Kitchen type\":\"Private\",\"Gender specific\":\"Mixed\",\"Pets\":\"Allowed\",\"Location\":\"Quezon City\"}]}"
```

---

### **4. Check Model Information (Anaconda Prompt)**

```bash
conda activate hanapbahay
cd c:\xampp\htdocs\public_html\ml_service
python check_model_info.py
```

Shows:
- Model version and creation date
- Features used
- Which notebook was used

---

### **5. Stop ML Service**

In the Anaconda Prompt where the service is running:
- Press **Ctrl+C**
- Wait for shutdown message

---

## 🔧 Maintenance Commands

### **Update Dependencies (Anaconda Prompt)**
```bash
conda activate hanapbahay
pip install --upgrade fastapi uvicorn pydantic
```

### **Update Model from Colab**
```bash
# 1. Download new model from Colab (in Colab notebook)
# 2. Extract to Downloads folder
# 3. In CMD, backup old model:
mkdir c:\xampp\htdocs\public_html\ml_service\artifacts\backup
copy c:\xampp\htdocs\public_html\ml_service\artifacts\*.* c:\xampp\htdocs\public_html\ml_service\artifacts\backup\

# 4. Copy new files from Downloads to artifacts folder
# 5. Restart ML service (Ctrl+C, then python app.py)
```

### **Verify Setup (Anaconda Prompt)**
```bash
cd c:\xampp\htdocs\public_html\ml_service
verify_setup.bat
```

---

## 🎯 Complete Workflow

### **Every Time You Want to Use ML Features:**

1. **Start Anaconda Prompt**
   ```bash
   conda activate hanapbahay
   cd c:\xampp\htdocs\public_html\ml_service
   python app.py
   ```

2. **Start XAMPP**
   - Open XAMPP Control Panel
   - Start Apache (and MySQL if needed)

3. **Use Your Website**
   - ML predictions will now work!
   - PHP calls the local ML service

4. **When Done**
   - Press Ctrl+C in Anaconda Prompt to stop ML service
   - Stop Apache in XAMPP

---

## 🔄 Troubleshooting Commands

### **Port 8000 Already in Use**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual number)
taskkill /PID <PID> /F
```

### **Check if Service is Running**
```bash
curl http://localhost:8000/version
```

### **View Service Logs**
Logs appear in the Anaconda Prompt window where you ran `python app.py`

### **Reinstall Environment (if broken)**
```bash
# Remove old environment
conda deactivate
conda env remove -n hanapbahay

# Create fresh environment
conda create -n hanapbahay python=3.11 -y
conda activate hanapbahay
conda install -c conda-forge scikit-learn pandas numpy joblib -y
pip install fastapi uvicorn pydantic python-multipart
```

---

## 📝 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│          HANAPBAHAY ML - QUICK COMMANDS                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  START ML SERVICE (Anaconda Prompt):                    │
│    conda activate hanapbahay                            │
│    cd c:\xampp\htdocs\public_html\ml_service            │
│    python app.py                                        │
│                                                         │
│  STOP ML SERVICE:                                       │
│    Press Ctrl+C                                         │
│                                                         │
│  TEST SERVICE (New CMD):                                │
│    curl http://localhost:8000/version                   │
│    (or run test_service.bat)                            │
│                                                         │
│  CHECK MODEL INFO (Anaconda Prompt):                    │
│    python check_model_info.py                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Pro Tips

### **Tip 1: Use Batch Files**
Instead of typing commands, just run:
- `start_service_conda.bat` - Starts ML service
- `test_service.bat` - Tests all endpoints
- `verify_setup.bat` - Checks installation

### **Tip 2: Keep Service Running**
Leave Anaconda Prompt with ML service running in the background while you work.

### **Tip 3: Auto-Start on Boot**
Install as Windows Service so it starts automatically:
```bash
# Run as Administrator
install_service.bat
```

### **Tip 4: Multiple Terminal Windows**
- **Window 1 (Anaconda):** ML service running
- **Window 2 (CMD):** Testing/development commands
- **Window 3:** XAMPP/PHP logs

---

## ❓ Common Questions

**Q: Do I need to run conda activate every time?**
A: Yes, every time you open a new Anaconda Prompt.

**Q: Can I close the Anaconda Prompt window?**
A: Not if you want ML to keep working. The service stops when you close it.

**Q: How do I know if it's working?**
A: Run `curl http://localhost:8000/version` in CMD. If you get JSON response, it's working.

**Q: Do I need internet to run ML locally?**
A: No! Everything runs offline once installed.

**Q: What if I restart my computer?**
A: You need to start the ML service again with the commands above.

---

## 🎓 Training New Models

### **In Colab:**
1. Open your notebook in Colab
2. Make changes to training code
3. Run all cells
4. Run export cell:
   ```python
   from google.colab import files
   import shutil

   shutil.make_archive("/content/hanapbahay_artifacts", "zip",
                       "/content/hanapbahay_artifacts")
   files.download("/content/hanapbahay_artifacts.zip")
   ```

### **On Local Machine:**
1. Stop ML service (Ctrl+C in Anaconda)
2. Backup old model:
   ```bash
   mkdir artifacts\backup
   copy artifacts\*.* artifacts\backup\
   ```
3. Extract new model to `artifacts\`
4. Restart ML service:
   ```bash
   python app.py
   ```

---

## 📞 Need Help?

If something doesn't work:

1. Check service is running: `curl http://localhost:8000/version`
2. Check XAMPP Apache is running
3. Check model files exist: `dir artifacts`
4. Run verification: `verify_setup.bat`
5. Check logs in Anaconda Prompt window

---

**Last Updated:** October 10, 2025
**Version:** 1.0
