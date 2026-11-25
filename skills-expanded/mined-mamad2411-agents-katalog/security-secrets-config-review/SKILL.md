---
name: security-secrets-config-review
description: "Review changes to secret sources, scope, injection, logging, packaging, rotation, or access."
---

# Security Secrets Config Review

Check secret source, scope, exposure in logs/builds/images, rotation, environment separation, and least-privilege access.

## Trigger boundary

Use this skill when a change sources, scopes, injects, logs, builds, packages, rotates, or grants access to secrets or environment configuration, including public variables and CI/CD.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no secret, configuration, environment, build, logging, or access impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-secrets-config-ci.md](./references/01-secrets-config-ci.md) - Secrets Config And CI
- [02-audit-and-vulnerability-response.md](./references/02-audit-and-vulnerability-response.md) - Audit And Vulnerability Response
