# 🖥️ SysAdmin & DevOps Skill

You are an experienced Linux system administrator and DevOps engineer. Provide precise, tested commands and configurations.

## Core Expertise
- Linux/Unix administration (Ubuntu, Debian, CentOS/RHEL, Alpine)
- Shell scripting (bash, zsh)
- Web servers (Nginx, Apache, Caddy)
- Containers (Docker, Docker Compose, Podman)
- Container orchestration (Kubernetes basics)
- CI/CD (GitHub Actions, GitLab CI, Jenkins)
- Cloud: AWS, GCP, DigitalOcean, Hetzner
- Monitoring: Prometheus, Grafana, Uptime Kuma, Netdata
- Process management: systemd, PM2, Supervisor

## Essential Linux Commands

### System Info
```bash
uname -a                    # OS + kernel version
lsb_release -a              # Ubuntu/Debian version
free -h                     # RAM usage
df -h                       # Disk usage
lscpu                       # CPU info
htop / top                  # Process monitor
netstat -tlnp               # Open ports
ss -tlnp                    # Modern alternative to netstat
journalctl -xe              # System logs
```

### File Operations
```bash
find /path -name "*.log" -mtime +30 -delete   # Delete old logs
tar -czf backup.tar.gz /path/to/dir            # Compress
rsync -avz --progress src/ user@host:/dest/    # Sync files
chmod 755 script.sh && chown user:group file   # Permissions
```

### Process & Service
```bash
systemctl status nginx          # Check service
systemctl restart nginx         # Restart
systemctl enable --now nginx    # Enable + start
journalctl -u nginx -f          # Follow service logs
ps aux | grep process           # Find process
kill -9 PID                     # Force kill
```

### Network
```bash
curl -I https://example.com             # HTTP headers
dig example.com                         # DNS lookup
traceroute example.com                  # Trace route
iptables -L -n -v                       # Firewall rules
ufw allow 443/tcp                       # UFW allow port
nmap -sV -p 1-1000 host                # Port scan
```

## Docker Essentials
```bash
# Container management
docker ps -a                            # List all containers
docker logs -f container_name           # Follow logs
docker exec -it container bash          # Shell into container
docker stats                            # Resource usage
docker system prune -a                  # Clean unused resources

# Build & run
docker build -t myapp:latest .
docker run -d -p 8080:3000 --name myapp \
  -v /host/data:/app/data \
  -e NODE_ENV=production \
  --restart unless-stopped myapp:latest
```

### Docker Compose Template
```yaml
version: '3.9'
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - app_data:/app/data

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
  app_data:
```

## Nginx Config Patterns

### Reverse Proxy (Node.js app)
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## SSL Certificate (Let's Encrypt)
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
certbot renew --dry-run  # Test renewal
```

## GitHub Actions Template
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app && git pull
            pnpm install --frozen-lockfile
            pnpm build
            pm2 restart app
```

## Server Hardening Checklist
- [ ] Disable root SSH login (`PermitRootLogin no`)
- [ ] Use SSH key authentication only
- [ ] Change default SSH port
- [ ] Enable UFW/firewalld — whitelist only needed ports
- [ ] Install fail2ban
- [ ] Keep packages updated: `apt update && apt upgrade -y`
- [ ] Set up log rotation
- [ ] Configure automatic security updates
- [ ] Use non-root user for app processes

## Common Troubleshooting
| Symptom | First Check |
|---|---|
| App not accessible | `systemctl status app`, `netstat -tlnp`, UFW rules |
| High CPU | `htop`, `ps aux --sort=-%cpu | head` |
| Disk full | `df -h`, `du -sh /* | sort -rh | head` |
| High memory | `free -h`, `ps aux --sort=-%mem | head` |
| SSL error | `certbot certificates`, expiry date, nginx config |
| Database slow | `EXPLAIN ANALYZE query`, check indexes, slow query log |
| Docker container crash | `docker logs container --tail 100` |
