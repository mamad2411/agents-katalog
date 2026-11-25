---
name: github-actions-security-hardening
description: Hardens GitHub Actions workflows against excessive token permissions, unsafe triggers, untrusted input injection, action supply-chain risk, secret exposure, and deployment abuse.
---


# GitHub Actions Security Hardening

Use this skill to harden workflow security before merging CI/CD, release, deployment, package publishing, or agentic workflow changes.

## Security Priorities

- Explicit least-privilege `permissions`
- Safe trigger selection
- Trusted runner boundaries
- Safe handling of untrusted event context
- Secrets and environment isolation
- OIDC instead of long-lived cloud credentials
- Third-party action review and pinning
- Cache and artifact integrity
- Deployment gate safety

## Workflow

Use `workflows/security-hardening-workflow.md`.

## Resources

- `resources/security-hardening-checklist.md`

## Scripts

This skill owns:

```text
scripts/audit-github-actions-security.py
```

Run the script with `--help` before use.

