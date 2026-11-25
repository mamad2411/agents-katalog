---
name: azure-hsm-key-lifecycle-review
description: Reviews Azure Key Vault Managed HSM key lifecycle work, including key creation, import, backup, restore, rotation, version cutover, retirement, recovery, delete, purge, and consuming workload impact. Use when the user mentions Managed HSM keys, BYOK, CMK, key versions, key rotation, key URI changes, key operations, or key retirement.
license: MIT
compatibility: Requires current Azure documentation for exact commands; optional Azure CLI for the included read-only inventory script.
---

# Azure HSM Key Lifecycle Review Skill

Use this skill when reviewing Managed HSM keys and the systems that depend on them.

## Approach

1. Identify key owner, purpose, environment, consuming services, allowed operations, and recovery requirements.
2. Confirm key type, algorithm, operations, expiration, tags, and compliance assumptions.
3. Confirm the workload uses managed identity and least-privilege local RBAC.
4. Review versioned versus versionless key URI behavior.
5. Plan staged rotation, application cutover, monitoring, rollback, and old-key retention.
6. Treat backup, restore, delete, purge, release, and exportable-key settings as high-risk.
7. Verify current official syntax before producing implementation commands.

## Workflow

Use `workflows/key-lifecycle-review-workflow.md` for structured key lifecycle and rotation reviews.

## Resource

Use `resources/key-lifecycle-review-checklist.md` for coverage.

## Script

Use `scripts/azure-hsm-key-inventory.sh` for read-only key inventory. Run it with `--help` before use.

## Example

Use `examples/rotation-cutover-review.md` for a practical rotation review pattern.
