---
name: nginx-patterns
description: "When to activate: nginx, reverse proxy, load balancer, server block, upstream, ssl, rate limiting, caching, location"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Nginx Patterns

## Reverse Proxy

```nginx
upstream backend {
    least_conn;
    server app1:8080 weight=3;
    server app2:8080 weight=3;
    server app3:8080 backup;
    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_stapling on;
    ssl_stapling_verify on;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }
}
```

## Rate Limiting

```nginx
http {
    # Define zones in http block
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    limit_conn_zone $binary_remote_addr zone=conn:10m;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_conn conn 10;
            limit_req_status 429;
            proxy_pass http://backend;
        }

        location /auth/login {
            limit_req zone=login burst=5;
            proxy_pass http://backend;
        }
    }
}
```

## Static File Caching

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location / {
    add_header Cache-Control "no-cache, must-revalidate";
    try_files $uri $uri/ /index.html;
}
```

## Gzip Compression

```nginx
http {
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1000;
    gzip_types
        text/plain text/css text/xml text/javascript
        application/json application/javascript application/xml
        application/rss+xml image/svg+xml;
}
```

## Security Headers

```nginx
add_header X-Frame-Options            "DENY"                always;
add_header X-Content-Type-Options     "nosniff"             always;
add_header X-XSS-Protection           "1; mode=block"       always;
add_header Referrer-Policy            "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security  "max-age=31536000; includeSubDomains; preload" always;
add_header Permissions-Policy         "camera=(), microphone=(), geolocation=()" always;
add_header Content-Security-Policy    "default-src 'self'; script-src 'self' 'nonce-$request_id'" always;
```

## Health Check Endpoint (internal only)

```nginx
location /nginx-health {
    access_log off;
    allow 10.0.0.0/8;
    deny all;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

## Key Rules
- Always redirect HTTP → HTTPS with 301
- Use `http2` for TLS servers
- Set `proxy_read_timeout` — default 60s may be too short for slow backends
- Log format should include `$request_time` and `$upstream_response_time`
- Test config before reload: `nginx -t && nginx -s reload`
