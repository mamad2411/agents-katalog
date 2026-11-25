---
name: azure-postgresql-flexible-server-18-backup-restore-review
description: Reviews Azure Database for PostgreSQL Flexible Server 18 backup, PITR, restore-test, geo-redundant backup, RPO, RTO, and disaster-recovery readiness. Use before production launch, destructive changes, migrations, and major upgrades.
license: MIT
compatibility: Requires Azure CLI for Azure backup configuration checks.
---

# Azure PostgreSQL Flexible Server 18 Backup and Restore Review

## When to Use This Skill

Use this skill when reviewing:

- Backup retention.
- Point-in-time restore readiness.
- Restore-test process.
- Geo-redundant backup decisions.
- Recovery objectives before production launch.
- Recovery safety before destructive changes, migrations, or upgrades.

## Core Guidance

- Require explicit RPO, RTO, backup retention, and restore-test cadence.
- Use restore tests to separate assumptions from verified behavior.
- Restore to a separate server and prevent accidental application writes.
- Do not approve destructive data changes without a validated restore path.
- Run scripts with `--help` before use.

## Workflows

- [backup-restore-review-workflow](workflows/backup-restore-review-workflow.md)
- [restore-test-workflow](workflows/restore-test-workflow.md)

## Resources

- [backup-restore-review-checklist.md](resources/backup-restore-review-checklist.md)

## Scripts

- `scripts/check-backup-config.sh`

## Examples

- [restore-test-cli-example.md](examples/restore-test-cli-example.md)
