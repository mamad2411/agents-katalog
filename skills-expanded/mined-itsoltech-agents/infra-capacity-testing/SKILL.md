---
name: infra-capacity-testing
description: "Plan load, stress, and soak tests for capacity, bottlenecks, and autoscaling."
---

# Infra Capacity Testing

Review measured capacity, bottlenecks, scaling assumptions, limits, and alerts before production risk grows.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-nomad-capacity.md](./references/01-nomad-capacity.md) - Nomad Capacity
- [02-traffic-stateful-capacity.md](./references/02-traffic-stateful-capacity.md) - Traffic Stateful Capacity
