---
name: infra-nomad-deployment
description: "Implement Nomad jobs, canaries, rollback, templates, Vault, and constraints."
---

# Infra Nomad Deployment

Review Nomad job specs through allocation lifecycle, service discovery, secrets, update strategy, resources, and failure behavior.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Nomad - rola w architekturze; Nomad - podstawowy model pojęć; Nomad - standard job speca
- [02-nomad-update-rollback-i-canary.md](./references/02-nomad-update-rollback-i-canary.md) - Nomad - update, rollback i canary; Nomad - restart, reschedule i awarie alokacji; Nomad - migrate i node drain; Nomad - sieć, porty i service discovery
- [03-nomad-template-vault-i-workload-identity.md](./references/03-nomad-template-vault-i-workload-identity.md) - Nomad - template, Vault i workload identity; Nomad - lifecycle tasks i sidecary; Nomad - storage i stateful workloads; Nomad - namespaces, ACL i dostęp operatorski
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; zastosuj je do deploymentu Nomad opisanego wyżej
