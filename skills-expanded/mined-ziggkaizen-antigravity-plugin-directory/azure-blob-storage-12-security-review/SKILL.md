---
name: azure-blob-storage-12-security-review
description: Reviews Azure Blob Storage SDK v12 code and commands for RBAC, managed identity, SAS, account-key exposure, public access, encryption, retention, destructive operations, access policy boundaries, and data exfiltration risk.
license: MIT
compatibility: Requires repository access. Optional Azure CLI or Azure MCP context may improve reviews but is not required.
---

# Azure Blob Storage 12 Security Review Skill

Use this skill for security reviews of Azure Blob Storage SDK v12 integrations and operational commands.

## When To Use

Use when the task mentions:

- Storage account keys
- Connection strings
- SAS tokens
- User delegation SAS
- Managed identity
- RBAC
- Access policies
- Public container access
- Blob URLs
- Browser uploads
- Private endpoints
- Encryption
- Soft delete
- Versioning
- Immutability
- Retention
- Destructive Azure Storage commands

## Required First Steps

1. Read `resources/security-review-checklist.md`.
2. For access policy reviews, read `resources/access-policy-review-matrix.md`.
3. If reviewing commands, run the script with `--help` before relying on it.
4. Identify whether the operation is data-plane, management-plane, or application-level.
5. Confirm whether the environment is local development, CI/CD, staging, or production.
6. Never request or expose secrets.

## Workflows

- `workflows/security-review-workflow.md`: Use for a structured security review.
- `workflows/access-review-workflow.md`: Use for focused access policy/RBAC/SAS review.

## Resources

- `resources/security-review-checklist.md`: Security control checklist.
- `resources/access-policy-review-matrix.md`: Access policy review matrix.

## Scripts

- `scripts/azure-blob-storage-12-command-guard.py`: Hook-safe command guard for destructive or secret-sensitive Azure Storage commands.

Run:

```bash
python3 scripts/azure-blob-storage-12-command-guard.py --help
```

## Examples

- `examples/sas-and-rbac-antipatterns.md`: Common unsafe patterns and safer alternatives.

## Review Rules

- Prefer RBAC and Azure Identity.
- Treat account keys as emergency or compatibility credentials, not default application credentials.
- Treat SAS as delegated access that must be narrow, short-lived, logged safely, and revocable through design.
- Require explicit approval for destructive data operations.
- Flag public access unless it is explicitly justified.
- Flag logs that include SAS query strings, connection strings, bearer tokens, or account keys.
