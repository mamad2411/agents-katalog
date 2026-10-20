---
name: kong-gateway
description: API gateway and service mesh with Kong
version: 1.0.0
tags: [api, gateway, networking, microservices]
---

# Kong – API Gateway

Kong is a cloud-native API gateway for managing, securing, and
orchestrating APIs and microservices at scale.

- **GitHub**: github.com/Kong/kong (40 000+ ⭐)
- **License**: Apache-2.0
- **Security**: CNCF project. Enterprise-grade. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{KONG_ADMIN_URL}}` | Kong Admin API URL (default: :8001) |

## Usage Examples

### List services

```bash
curl -s "{{KONG_ADMIN_URL}}/services"
```

### Add a service

```bash
curl -s -X POST "{{KONG_ADMIN_URL}}/services" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-api", "url": "http://backend:3000"}'
```

### Add a route

```bash
curl -s -X POST "{{KONG_ADMIN_URL}}/services/my-api/routes" \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/api/v1"]}'
```

### Enable rate limiting plugin

```bash
curl -s -X POST "{{KONG_ADMIN_URL}}/services/my-api/plugins" \
  -H "Content-Type: application/json" \
  -d '{"name": "rate-limiting", "config": {"minute": 100}}'
```

## AI Agent Tips

- Plugin architecture: rate-limiting, auth, logging, caching, etc.
- Admin API enables dynamic configuration without restarts.
- Supports REST, gRPC, GraphQL, and WebSocket protocols.
- Declarative config via DB-less mode for GitOps workflows.
