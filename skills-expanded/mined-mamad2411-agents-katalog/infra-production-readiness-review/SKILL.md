---
name: infra-production-readiness-review
description: "Review releases or operational changes affecting deploy, rollback, data, secrets, or production gates."
---

# Infra Production Readiness Review

Check production gates across artifacts, runtime, routing, data, secrets, observability, security, rollback, and deployment process.

## Trigger boundary

Use this skill when a release or operational diff changes deploy/rollback, routing, data migration, secrets, observability, security, capacity, backups, runbooks, or production gates.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no release, runtime, data, security, or operational impact; follow the repository's established convention directly.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Deployment strategie; Bezpieczeństwo hosta; IaC, GitOps i drift
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; użyj ich jako końcowego przekrojowego rubryku readiness
