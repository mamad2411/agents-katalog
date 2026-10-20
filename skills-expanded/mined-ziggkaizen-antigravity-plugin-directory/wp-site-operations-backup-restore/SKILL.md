---
name: wp-site-operations-backup-restore
description: Plans and reviews recoverable WordPress database-and-file backup sets, restore drills, recovery objectives, retention, integrity checks, and rollback procedures. Use before risky changes or when recovery readiness is uncertain.
---

# wp-site-operations-backup-restore

Use this skill for backup design, pre-change recovery points, restore testing, rollback preparation, and recovery evidence.

## Principles

- Database and files form one recoverable set.
- A completed backup command is not proof of a usable backup.
- Recovery objectives determine frequency, retention, and restore architecture.
- Backups must remain available when the live host, account, site, or credentials fail.
- Restore testing is the strongest routine evidence.
- Rollback can lose data created after the recovery point; plan reconciliation.

## Workflow

Use [`workflows/plan-wordpress-backup-restore-workflow.md`](workflows/plan-wordpress-backup-restore-workflow.md).

## Resource

Use [`resources/backup-restore-checklist.md`](resources/backup-restore-checklist.md).

## Completion Evidence

Produce backup-set identifiers, scope, time, integrity results, off-site location, retention, encryption, restore steps, restore-test results, measured recovery time, reconciliation needs, and named recovery owners.
