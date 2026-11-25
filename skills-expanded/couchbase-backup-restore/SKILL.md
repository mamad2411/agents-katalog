---
name: couchbase-backup-restore
description: "Plan and execute Couchbase backup and restore operations. Use whenever the user asks about backup, restore, cbbackupmgr, backup repository, backup archive, full backup, incremental backup, differential backup, backup schedule, retention policy, backup verification, Capella managed backup, backup to S3, backup to filesystem, restoring a bucket, restoring specific documents, admin_backup_* tools, or 'how do I back up / restore Couchbase.' Distinct from couchbase-migration-execution (one-time data migration to a new cluster) and couchbase-mcp (operating the tools). Use proactively for DR planning, RPO/RTO requirements, backup verification workflows, and pre-upgrade snapshots."
license: MIT
---

# Couchbase Backup & Restore

A skill for *planning and executing* Couchbase backup and restore operations — both self-managed (cbbackupmgr) and Capella-managed.

Distinct from:
- `couchbase-migration-execution` — one-time data migration, not recurring backup
- `couchbase-mcp` — the `admin_backup_*` tools that interact with the Backup service

## When this skill applies

- "How do I back up Couchbase?"
- "What's cbbackupmgr?"
- "How do I set up a backup schedule?"
- "Full vs incremental backup — what's the difference?"
- "How do I restore from backup?"
- "How do I restore just one bucket, or just a few documents?"
- "How do I back up to S3?"
- "How do I verify my backups are actually working?"
- "What's the RPO/RTO I can achieve?"
- "How does Capella handle backups?"

## Pick the right reference

| Question | Read |
|---|---|
| "cbbackupmgr commands — config, backup, restore, list, merge, examine" | `references/cbbackupmgr.md` |
| "Backup strategy — full vs incremental, schedules, retention, S3" | `references/strategy.md` |
| "How to restore — full cluster, single bucket, single document, point-in-time" | `references/restore.md` |
| "Capella managed backups — schedules, retention, restore" | `references/capella-backups.md` |

## Three core principles

**Principle 1 — An untested backup is not a backup.**
Run a restore drill regularly — quarterly at minimum, monthly for production data. `cbbackupmgr examine` lets you inspect backup contents without a full restore. A restore drill to a staging cluster is the only way to know your backups are complete and your restore procedure works.

**Principle 2 — Incremental backups depend on the full backup chain.**
Couchbase incremental backups are differential (each increment contains only mutations since the prior backup). To restore to a point in time, you need the full backup plus every increment up to that point. A corrupted full backup invalidates the entire chain. Keep multiple full backup generations, not just increments.

**Principle 3 — Backup is not DR.**
Backup protects against data corruption, accidental deletion, and ransomware. It does not protect against site loss with your RPO — that's what XDCR active-passive is for. Most deployments need both: XDCR for RTO (fast failover), backup for RPO (data recovery from logical errors that XDCR would have replicated).

## Quick tool map

| Task | Tool |
|---|---|
| List backup repositories | `admin_backup_list_repositories` |
| Get repository info | `admin_backup_get_repository` |
| Trigger a backup | `admin_backup_trigger_backup` |
| Get backup history | `admin_backup_get_backup_info` |
| Trigger a restore | `admin_backup_trigger_restore` |
| Get restore status | `admin_backup_get_restore_status` |

These tools interact with the Couchbase Backup Service (available in Couchbase 7.0+ EE). For older clusters or more control, use `cbbackupmgr` CLI directly.

## RPO/RTO guidance

| Approach | RPO | RTO | Notes |
|---|---|---|---|
| Incremental backup hourly | ~1 hour | Hours (depends on data size) | Standard for most workloads |
| Incremental backup every 15 min | ~15 min | Hours | Increases backup storage and I/O |
| XDCR active-passive + backup | Near-zero (XDCR) / hours (backup) | Minutes (XDCR failover) | Best of both for production |
| Capella managed (daily + auto) | Up to 24 hours | Hours | Acceptable for non-critical data |

## Related skills

- `couchbase-xdcr` — XDCR for near-zero RPO / low RTO (complements backup, not a replacement)
- `couchbase-mcp` — `admin_backup_*` tools
- `couchbase-migration-execution` — one-time migration (uses similar tooling)
