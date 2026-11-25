---
name: infra-deployment-design
description: "Design deployment topology, environments, ownership, rollout, and rollback."
---

# Infra Deployment Design

Design the deployment path from edge to app to data stores before writing runtime configuration.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-deployment-model.md](./references/01-deployment-model.md) - Deployment Model
- [02-environment-decisions-and-runtime.md](./references/02-environment-decisions-and-runtime.md) - Environment Decisions And Runtime
