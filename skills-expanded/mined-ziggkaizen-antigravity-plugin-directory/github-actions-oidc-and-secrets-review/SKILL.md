---
name: github-actions-oidc-and-secrets-review
description: Reviews GitHub Actions OIDC, id-token permissions, cloud trust boundaries, long-lived secrets, environment secrets, and credential exposure risks.
---


# GitHub Actions OIDC and Secrets Review

Use this skill when workflows use `secrets.*`, `vars.*`, `id-token: write`, cloud login actions, package registry tokens, or protected environments.

## Review Focus

- secret scope
- environment protection
- OIDC subject/audience restrictions
- minimal `id-token: write`
- removal of long-lived credentials
- safe logging
- safe artifact/cache behavior

## Workflow

Use `workflows/oidc-secrets-review-workflow.md`.

## Resources

- `resources/oidc-secrets-checklist.md`

