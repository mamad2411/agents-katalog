---
name: infra-backup-dr
description: "Design backup and disaster recovery with RPO/RTO, retention, restore tests, and recovery."
---

# Infra Backup DR

Review backup coverage, restore proof, RPO/RTO, ownership, retention, and rollback or roll-forward paths.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-stateful-workloads-and-storage.md](./references/01-stateful-workloads-and-storage.md) - Stateful Workloads And Storage
- [02-backup-dr-geo-review.md](./references/02-backup-dr-geo-review.md) - Backup DR Geo And Review
