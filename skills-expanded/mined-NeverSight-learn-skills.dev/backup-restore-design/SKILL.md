---
name: backup-restore-design
description: Design backup, restore, sync, export, recovery, data durability, cloud/local storage, versioning, migration, deletion, and disaster recovery systems. Use when building or reviewing backup strategy for SaaS, mobile apps, desktop utilities, games, user-generated content, account data, or business-critical workflows.
---

# Backup Restore Design

Use this skill to design data durability as a product feature and operational system.

## Workflow

1. Identify data classes: user content, settings, purchases, game progress, files, account state, audit records, analytics, secrets.
2. Read `references/backup-restore-patterns.md`.
3. Define RPO/RTO, retention, encryption, ownership, export, deletion, and support visibility.
4. Design backup, restore, conflict resolution, migration, and recovery drills.
5. Produce event schema and failure modes.

## Output format

```text
Data classes:
Durability target:
Backup design:
Restore design:
Conflict handling:
Support/admin tooling:
Failure modes:
```
