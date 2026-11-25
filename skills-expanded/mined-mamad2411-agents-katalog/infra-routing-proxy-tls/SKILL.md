---
name: infra-routing-proxy-tls
description: "Design or debug proxies, routing, TLS, redirects, CORS, ingress, and discovery."
---

# Infra Routing Proxy TLS

Review public exposure, TLS termination, routing ownership, proxy headers, long connections, DNS/CDN, and load balancing behavior.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Nomad - Traefik jako ingress; Nomad - NGINX jako reverse proxy; Routing i reverse proxy
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; zastosuj je do ingressu, proxy i TLS
