---
name: "kong-gateway-deck-best-practices"
description: "Kong API gateway with decK declarative config: services/routes/plugins/consumers/upstreams to FRONT an existing backend (upstream stays AS-IS), env overlays, GitOps with deck sync/diff/validate. Use when generating or reviewing a Kong gateway."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# Kong Gateway + decK Best Practices

Use case: Kong fronts an EXISTING backend (e.g. a MuleSoft/Node service). The upstream is NOT modified.

## Declarative config (kong.yaml)
```yaml
_format_version: "3.0"
services:
  - name: <svc>
    url: https://<existing-backend-host>:<port>   # from source_reference (e.g. Mule request-config)
    routes:
      - name: <route>
        paths: ["/<context>/<version>"]            # mirror the source listener path
        strip_path: false
    plugins:
      - name: rate-limiting
      - name: cors
      - name: correlation-id
upstreams:
  - name: <svc>-upstream
    targets: [{ target: "<host>:<port>" }]
    healthchecks: { active: { healthy: {}, unhealthy: {} } }
consumers: []
```

## Standards
- One service per backend; routes mirror the source paths/methods; `strip_path` matches the backend expectation.
- Plugins implement the source's policies: auth (key-auth/jwt/oauth2), rate-limiting, cors, request/response-transformer, proxy-cache, prometheus. Order matters (auth before rate-limit).
- Preserve NFRs from the source (e.g. timeouts) via `connect_timeout`/`read_timeout`/`write_timeout` on the service.
- Env-specific values via decK overlays / `${{ env "..." }}`; secrets via Kong vault/env, never inline.
- GitOps: `deck gateway validate` in CI, `deck gateway diff` on PR, `deck gateway sync` on deploy.
