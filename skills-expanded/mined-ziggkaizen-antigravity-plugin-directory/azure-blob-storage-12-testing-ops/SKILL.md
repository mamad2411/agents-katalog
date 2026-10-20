---
name: azure-blob-storage-12-testing-ops
description: Tests, scans, debugs, and verifies Azure Blob Storage SDK v12 integrations. Use for repository scans, storage failure triage, emulator/local testing, retries, diagnostics, public artifact checks, and operational readiness.
license: MIT
compatibility: Requires repository access. Optional Azure access may be needed for live integration diagnostics.
---

# Azure Blob Storage 12 Testing and Ops Skill

Use this skill for quality, diagnostics, and operational readiness work.

## When To Use

Use when the task involves:

- Writing or repairing tests for Blob Storage SDK v12 code.
- Debugging authentication, authorization, networking, throttling, upload/download, ETag, lease, or delete failures.
- Running a repository scan for legacy SDK usage or risky credentials.
- Preparing a release involving Blob Storage changes.
- Reviewing observability and operational runbooks.
- Verifying public/private path separation, public artifact safety, or immutability controls.

## Required First Steps

1. Read `resources/test-and-ops-checklist.md`.
2. Run scripts with `--help` before use.
3. Determine whether the task can be completed with unit tests, local emulator tests, mocked clients, or requires real Azure integration tests.
4. Never run destructive commands against real Azure resources without explicit approval.

## Workflows

- `workflows/debug-storage-failure-workflow.md`: Use for incident triage and difficult failure diagnosis.
- `workflows/pre-release-verification-workflow.md`: Use before merging or releasing Blob Storage changes.

## Resources

- `resources/test-and-ops-checklist.md`: Test, diagnostics, and release checklist.

## Scripts

- `scripts/azure-blob-storage-12-project-scan.py`: Scans a repository for legacy SDK references and common secret-risk patterns.

Run:

```bash
python3 scripts/azure-blob-storage-12-project-scan.py --help
```

## Testing Rules

- Unit-test application behavior without requiring live Azure where possible.
- Use integration tests for auth, RBAC, real SDK behavior, transfer behavior, and service-specific edge cases.
- Isolate test containers by unique prefix and clean them up safely.
- Do not use production storage accounts for automated tests.
- Do not print SAS URLs or connection strings in test output.
