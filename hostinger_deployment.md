# Deploy to Hostinger VPS/Cloud

## If You Have VPS Access

If your Hostinger plan includes VPS or SSH access, you can deploy directly there.

---

## Step 1: Check if You Have SSH Access

Contact Hostinger support or check your control panel for:
- SSH/Terminal access
- VPS or Cloud hosting (not shared hosting)

**Note:** Most basic shared hosting plans DON'T support Python apps.

---

## Step 2: Connect via SSH

```bash
ssh your_username@hanapbahay.online
```

---

## Step 3: Install Python & Dependencies

```bash
# Update system
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Create directory
mkdir -p /var/www/ml_service
cd /var/www/ml_service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Upload Files

Via FTP/SFTP, upload:
- `app.py`
- `requirements.txt`
- `artifacts/` folder (with model files)

Or use git:
```bash
git clone https://github.com/your_username/hanapbahay-ml-service.git .
```

---

## Step 5: Run as Service

Create systemd service:

```bash
sudo nano /etc/systemd/system/hanapbahay-ml.service
```

Add:
```ini
[Unit]
Description=HanapBahay ML Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ml_service
Environment="PATH=/var/www/ml_service/venv/bin"
Environment="HANAPBAHAY_API_KEY=your_secure_key"
ExecStart=/var/www/ml_service/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000

Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable hanapbahay-ml
sudo systemctl start hanapbahay-ml
sudo systemctl status hanapbahay-ml
```

---

## Step 6: Configure Reverse Proxy

Add to your Apache config:

```apache
<VirtualHost *:443>
    ServerName hanapbahay.online

    # Your existing PHP config...

    # ML Service proxy
    ProxyPass /ml/ http://127.0.0.1:8000/
    ProxyPassReverse /ml/ http://127.0.0.1:8000/
</VirtualHost>
```

Restart Apache:
```bash
sudo systemctl restart apache2
```

---

## Step 7: Update PHP Config

```php
// Use same domain with /ml/ prefix
define('ML_BASE', 'https://hanapbahay.online/ml');
define('ML_KEY', 'your_secure_key');
```

---

## Pros:
- No additional cost
- Full control
- Fast (same server)

## Cons:
- Requires VPS/SSH access
- More technical setup
- You manage updates/security
