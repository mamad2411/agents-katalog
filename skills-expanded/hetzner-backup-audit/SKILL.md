---
name: hetzner-backup-audit
description: Assess backup and restore-readiness evidence for stateful Hetzner, PostgreSQL, Redis, and volume assets.
---

# Backup and Restore Audit

Read metadata only. Never create, restore, delete, download, mount, or modify a backup or snapshot. Required inputs are provider backup/snapshot metadata, application backup declarations, retention, encryption/access policy, and owner-provided restore-test evidence.

Distinguish provider snapshots from application-consistent database recovery. Missing provider backup evidence is not proof that no backup exists. Mark absence-based candidates `needs_validation` unless all applicable mechanisms were collected. Assess blast radius, credential separation, retention, replication, and most recent successful restore exercise. Output recovery assumptions and safe owner-observed validation steps.

