---
name: deployment-vps
description: "Apply when deploying applications to VPS, bare metal, or cloud VMs. Covers: systemd services, nginx reverse proxy, SSL with Certbot, zero-downtime deployment, firewall setup. Trigger for: deploy, VPS, server, nginx, production deploy, systemd, SSL."
---

# DEPLOYMENT VPS — Production Setup

## systemd Service
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My FastAPI App
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
EnvironmentFile=/opt/myapp/.env
ExecStart=/opt/myapp/venv/bin/uvicorn src.main:app \
    --host 127.0.0.1 --port 8000 \
    --workers 4 --no-access-log
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload && systemctl enable --now myapp
```

## Nginx Reverse Proxy + SSL
```nginx
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate     /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```
```bash
certbot --nginx -d api.example.com
```

## Zero-Downtime Deploy Script
```bash
#!/bin/bash
set -e
APP_DIR=/opt/myapp

cd $APP_DIR
git pull origin main
source venv/bin/activate
pip install -r requirements.txt -q
alembic upgrade head

# Reload without downtime (systemd)
systemctl reload myapp || systemctl restart myapp
echo "✅ Deployed $(git rev-parse --short HEAD)"
```

## Firewall (ufw)
```bash
ufw default deny incoming
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## Forbidden
❌ Running app as root
❌ No SSL (plain HTTP)
❌ Exposing app port directly (bypass nginx)
❌ `.env` file world-readable (`chmod 600 .env`)
❌ No firewall
❌ `git pull` on production without migration
