---
name: infra-secrets-config
description: "Design secrets and runtime config across env, Vault, rotation, exposure, and CI/CD."
---

# Infra Secrets Config

Review where secrets live, how they reach runtime, who can read them, and whether logs/images/state can leak them.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Konfiguracja środowisk; Nomad - konfiguracja i sekrety; Nomad - template, Vault i workload identity
- [Shared infrastructure review checklist](../_shared/references/infrastructure/container-review-checklist.md) - wspólne fakty i bramka review; zastosuj je do sekretów i konfiguracji
