---
name: infra-edge-protection
description: "Design edge protection with WAF, rate limits, bot and DDoS controls, and CDN."
---

# Infra Edge Protection

Review what is public, what is rate-limited, body/time limits, cache safety, and abuse controls at the edge.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-edge-network-model.md](./references/01-edge-network-model.md) - Edge Network Model
- [02-dns-proxy-cache-review.md](./references/02-dns-proxy-cache-review.md) - DNS Proxy Cache And Review
