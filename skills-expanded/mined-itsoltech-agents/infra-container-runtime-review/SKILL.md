---
name: infra-container-runtime-review
description: "Review container runtime changes to limits, health checks, lifecycle, volumes, or secrets."
---

# Infra Container Runtime Review

Review runtime limits, health checks, lifecycle, persistent state, restart behavior, environment, and operational diagnostics.

## Trigger boundary

Use this skill when container runtime configuration changes limits, health checks, lifecycle/shutdown, persistent volumes, restart behavior, environment/secrets, or diagnostics.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no container runtime, secret, resource, or operational impact; follow the repository's established convention directly.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Runtime kontenerów; Health checks; Docker Compose na produkcji
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; zastosuj je do zachowania runtime opisanego wyżej
