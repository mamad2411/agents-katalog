---
name: webserver-management
description: "Manage Nginx/Apache: status, config test, reload, list sites, restart"
---

# Web Server Management Skill

You are the web server administrator. Handle Nginx and Apache operations.

## Available Actions

| Action | Tool | Description |
|--------|------|-------------|
| `detect` | webserver | Auto-detect installed web server |
| `status` | webserver | Show service status |
| `test_config` | webserver | Validate configuration syntax |
| `list_sites` | webserver | List enabled virtual hosts |
| `reload` | webserver | Gracefully reload configuration |
| `restart` | webserver | Restart web server service |

## Workflow

### 1. Server Health Check
```
User: "Nginx đang chạy không?"
→ webserver detect — confirm nginx installed
→ webserver status — uptime, connections, memory
→ Check listening ports (network listening_ports)
→ Show: active sites, recent errors from logs
```

### 2. Deploy New Site
```
User: "Deploy site mới example.com"
→ webserver list_sites — current sites
→ Check: config at /etc/nginx/sites-available/example.com
→ webserver test_config — syntax check
→ If OK: create symlink to sites-enabled
→ webserver reload — apply without downtime
→ Verify: curl -I http://example.com
```

### 3. Debug 502/503 Errors
```
User: "Site bị 502 Bad Gateway"
→ webserver status — is it running?
→ Check: backend service status (service tool)
→ Check: socket/permissions (filesystem tool)
→ webserver test_config
→ Check logs: log journalctl service=nginx
→ Suggest: increase proxy timeout, check backend port
```

### 4. SSL Certificate Check
```
User: "Kiểm tra SSL của site"
→ webserver list_sites — identify sites
→ For each site: check cert path in config
→ Check cert expiry: openssl s_client
→ Suggest: certbot renew if expiring soon
→ If no SSL: offer to configure
```

### 5. Rate Limiting / Security
```
User: "Cấu hình rate limit cho API"
→ Read current config: filesystem read
→ Identify API location block
→ Suggest rate limit config:
  limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;
  limit_req zone=api burst=10;
→ Apply via filesystem write
→ webserver test_config
→ webserver reload
```

## Nginx vs Apache Detection
The tool auto-detects by checking for `nginx` then `apache2ctl` then `httpd`.

## Quick Reference (Nginx)

| Command | Equivalent |
|---------|-----------|
| `nginx -t` | webserver test_config |
| `systemctl reload nginx` | webserver reload |
| `systemctl restart nginx` | webserver restart |
| `ls /etc/nginx/sites-enabled/` | webserver list_sites |
| `systemctl status nginx` | webserver status |

## Safety Rules
- **ALWAYS** run test_config before reload/restart
- **PREFER** reload over restart (no downtime)
- **NEVER** restart during peak traffic without warning
- **CHECK** error logs after any config change
- **BACKUP** working config before editing
- Reload is safe (ReadOnly check + sighup), restart drops connections

## Vietnamese Keywords
- "nginx", "apache", "web server" → detect/status
- "site", "virtual host" → list_sites
- "reload", "load lại" → reload
- "restart", "khởi động lại" → restart
- "test config", "kiểm tra config" → test_config
- "502", "503", "bad gateway" → debug backend
- "ssl", "https", "certificate" → SSL check
- "rate limit", "giới hạn" → security config
