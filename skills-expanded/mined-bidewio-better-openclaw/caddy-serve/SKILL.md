---
name: caddy-serve
description: Automatic HTTPS web server with Caddy
version: 1.0.0
tags: [web-server, https, proxy, ssl]
---

# Caddy – Automatic HTTPS Web Server

Caddy is a powerful web server with automatic HTTPS via Let's Encrypt,
reverse proxying, and simple configuration.

- **GitHub**: github.com/caddyserver/caddy (62 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Memory-safe Go. Auto-renewes SSL certificates. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{CADDY_ADMIN_URL}}` | Caddy admin API URL (default: localhost:2019) |

## Usage Examples

### Get current config

```bash
curl -s "{{CADDY_ADMIN_URL}}/config/"
```

### Add a reverse proxy

```bash
curl -s -X POST "{{CADDY_ADMIN_URL}}/config/apps/http/servers/srv0/routes" \
  -H "Content-Type: application/json" \
  -d '{"match": [{"host": ["app.example.com"]}], "handle": [{"handler": "reverse_proxy", "upstreams": [{"dial": "localhost:3000"}]}]}'
```

## AI Agent Tips

- Zero-config HTTPS — automatically obtains and renews TLS certificates.
- Caddyfile provides human-readable configuration.
- Admin API enables dynamic configuration changes without restarts.
- Supports HTTP/3, wildcard certs, and on-demand TLS.
