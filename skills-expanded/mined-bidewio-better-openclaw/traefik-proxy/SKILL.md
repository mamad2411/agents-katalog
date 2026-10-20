---
name: traefik-proxy
description: Cloud-native reverse proxy with Traefik
version: 1.0.0
tags: [networking, proxy, ssl, docker, kubernetes]
---

# Traefik – Cloud-Native Reverse Proxy

Traefik is a modern reverse proxy and load balancer for microservices
with automatic service discovery, SSL, and Docker/K8s integration.

- **GitHub**: github.com/traefik/traefik (55 000+ ⭐)
- **License**: MIT
- **Security**: CNCF project. CII Best Practices certified. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{TRAEFIK_URL}}` | Base URL of the Traefik API |

## Usage Examples

### Get routers

```bash
curl -s "{{TRAEFIK_URL}}/api/http/routers"
```

### Get services

```bash
curl -s "{{TRAEFIK_URL}}/api/http/services"
```

### Check entrypoints

```bash
curl -s "{{TRAEFIK_URL}}/api/entrypoints"
```

## AI Agent Tips

- Auto-discovers Docker containers and applies routing rules via labels.
- Let's Encrypt integration provides automatic SSL certificates.
- Dashboard gives real-time visibility into routes and services.
- Middleware stack supports rate limiting, auth, compression, and more.
