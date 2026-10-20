---
name: nginx-hardening
description: "Review Nginx reverse-proxy security settings, TLS, headers, request limits, and upstream boundaries. Use for focused hardening work."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["nginx", "hardening", "tls", "rate-limit", "reverse-proxy", "security-headers"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# NGINX Reverse Proxy Hardening AI Skill Guide

## Overview

This skill focuses on **edge hardening** for NGINX as a reverse proxy or ingress TLS terminator - not general static-site or PHP app cookbook material (see related `nginx` skill for broader NGINX usage). Hardening means enforcing modern TLS, security headers, rate limits, body size caps, careful `proxy_*` buffering, and denying abusive request patterns before they reach upstreams.

```
Internet clients
      |
      v
NGINX edge (TLS + rate limit + headers)
      |
      v
Upstream (app / API gateway / k8s service)
```

## When to use

- Placing NGINX in front of APIs or web apps as TLS reverse proxy
- Adding rate limits, connection limits, and request size guards
- Tightening cipher suites, HSTS, and security headers
- Reviewing proxy configs for header injection / SSRF-ish misrouting risks

## Operational directives

1. Terminate TLS at the edge with strong protocols (`TLSv1.2`/`TLSv1.3` only).
2. Set explicit `client_max_body_size` and timeouts; never leave unlimited upload defaults on public APIs.
3. Prefer `limit_req` + `limit_conn` on login and expensive routes.
4. Pass only required headers upstream; override `Host` / `X-Forwarded-*` deliberately.
5. Validate config with `nginx -t` before reload; use graceful reload.

## Concrete examples

### TLS reverse proxy core

```nginx
# /etc/nginx/conf.d/api.conf
limit_req_zone $binary_remote_addr zone=api_per_ip:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

upstream api_upstream {
  server 10.0.1.10:8080 max_fails=3 fail_timeout=30s;
  keepalive 32;
}

server {
  listen 443 ssl http2;
  server_name api.example.com;

  ssl_certificate     /etc/ssl/certs/api.fullchain.pem;
  ssl_certificate_key /etc/ssl/private/api.key;
  ssl_protocols       TLSv1.2 TLSv1.3;
  ssl_prefer_server_ciphers off;

  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header Referrer-Policy "no-referrer" always;
  add_header Content-Security-Policy "default-src 'none'; frame-ancestors 'none'" always;

  client_max_body_size 1m;
  client_body_timeout 10s;
  client_header_timeout 10s;

  location /login {
    limit_req zone=api_per_ip burst=20 nodelay;
    limit_conn addr 10;
    proxy_pass http://api_upstream;
    include proxy_params_hardened.conf;
  }

  location / {
    limit_req zone=api_per_ip burst=40 nodelay;
    proxy_pass http://api_upstream;
    include proxy_params_hardened.conf;
  }
}
```

### Hardened proxy params

```nginx
# /etc/nginx/proxy_params_hardened.conf
proxy_http_version 1.1;
proxy_set_header Connection "";
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_hide_header X-Powered-By;
proxy_read_timeout 30s;
proxy_connect_timeout 5s;
proxy_send_timeout 30s;
proxy_buffering on;
```

### Validate and reload

```bash
nginx -t
nginx -s reload
curl -I https://api.example.com/health
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates
```

## Hardening checklist table

| Control | Target |
| :--- | :--- |
| TLS | 1.2+ only; valid chain; HSTS |
| Methods | Deny unexpected verbs if API is POST-only |
| Size | Small `client_max_body_size` per route class |
| Rate | Separate zones for auth vs read APIs |
| Upstream | Fixed servers or resolved private DNS; no open proxy |

## Best practices

1. Redirect `:80` to `:443` without serving sensitive content on cleartext.
2. Keep OCSP stapling / automated renewals working (pair with Let's Encrypt skill).
3. Log `$request_id` / trace headers for abuse forensics; avoid logging secrets.
4. Run NGINX as non-root where packaging allows; restrict config file perms on keys.

## Limitations

- Rate limits are coarse IP-based; behind CDNs you must key on real client IP carefully.
- WAF rulesets are out of scope - use a dedicated WAF when required.
- HTTP/3 / QUIC depends on build and OS support.

## Related skills

- `nginx` - general NGINX configuration and serving patterns
- `lets-encrypt` - certificate issuance/renewal for the edge
- `cloudflare-dns` - DNS + optional CDN in front of origin
- `opentelemetry` - propagate trace headers through proxy
