---
name: infra-incident-debugging
description: "Diagnose infra incidents across logs, metrics, routing, containers, Nomad, and TLS."
---

# Infra Incident Debugging

Debug from observed symptoms, recent deploys, logs, metrics, allocation state, routing path, and config diffs before changing infrastructure.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Health checks; Nomad - restart, reschedule i awarie alokacji; Nomad - migrate i node drain
- [02-logi-i-cardinality.md](./references/02-logi-i-cardinality.md) - Logi i cardinality; Edge case'y, które często powodują awarie
