---
name: design-backup-dr-recovery
description: Designs and validates backup, point-in-time-recovery, and disaster-recovery strategy for datastores — sets RPO/RTO targets, configures snapshot plus continuous WAL/binlog/oplog archiving for PITR, 3-2-1 immutable retention, automated test-restores, and cross-region replica failover with split-brain fencing.
when_to_use: When a stateful service needs a credible answer to "what if the database is lost or corrupted" — setting RPO/RTO, wiring snapshots + continuous log archiving for PITR, designing cross-region failover, scheduling tested restores, or auditing a never-restore-tested backup. Distinct from db-migration-safety (forward schema change safety) and incident-response-sre (running the live outage, not designing recoverability).
---

## When to Use

Reach for this skill when the question is **"can we get the data back, and how fast"** — not how to change the schema:

- "Set RPO/RTO for this database and prove we can hit them"
- "We have nightly snapshots but no way to restore to 2:47pm — add PITR"
- "Stand up cross-region DR / a warm standby we can promote"
- "Our backups have never been restore-tested — audit and fix that"
- "Recover a single dropped table without rolling back the whole DB"
- "Defend backups against ransomware / a fat-fingered `DROP DATABASE`"

NOT this skill:
- Making a forward schema migration safe/reversible (expand-contract, online DDL) → db-migration-safety
- Running the live incident — paging, comms, mitigation timeline → incident-response-sre
- Protecting/rotating the backup-store credentials and KMS keys → secrets-management
- Alerting that a backup job failed / dashboards for restore lag → observability-instrument
- Trimming snapshot/storage spend → cloud-cost-optimize

## Steps

1. **Set RPO and RTO per datastore from business impact — these two numbers drive every later choice.** RPO = max tolerable data loss (how far back you may rewind). RTO = max tolerable downtime (how long restore may take). Pick a tier, don't invent per-DB:

   | Tier | Example data | RPO | RTO | Implied mechanism |
   |---|---|---|---|---|
   | Tier 0 (money/orders) | payments ledger, auth | ≤ seconds | ≤ minutes | sync replica + continuous WAL, automated promotion |
   | Tier 1 (core app) | primary OLTP DB | ≤ 5 min | ≤ 1 hr | snapshot + async WAL archiving (PITR), warm standby |
   | Tier 2 (supporting) | analytics, search index | ≤ 1 hr | ≤ 4 hr | hourly snapshot, rebuild-from-source allowed |
   | Tier 3 (derived/cache) | caches, rebuildable views | n/a | n/a | no backup — document the rebuild procedure instead |

   RPO ≤ snapshot interval is a lie unless you also archive logs continuously (step 2). Write the chosen numbers down; an untargeted "we back up nightly" has an implicit 24h RPO nobody agreed to.

2. **Two backup layers: periodic base + continuous log archiving. Snapshot-only cannot do PITR.** A snapshot gets you to *snapshot time*; the log stream replays forward to any timestamp in between.

   | Engine | Base backup | Continuous log (the PITR engine) | Restore = base + replay |
   |---|---|---|---|
   | PostgreSQL | `pg_basebackup` / disk snapshot | WAL via `archive_command` → object store (pgBackRest/WAL-G) | `restore_command` + `recovery_target_time` |
   | MySQL/MariaDB | `xtrabackup` / `mysqldump` | binlog (`log_bin`, `binlog_format=ROW`) shipped off-host | restore base, `mysqlbinlog --stop-datetime` apply |
   | MongoDB | `mongodump` / filesystem snapshot | oplog (replica set required) | restore + `--oplogReplay --oplogLimit` |
   | SQLite | `.backup` / file copy | WAL file is local-only — ship full DB on a cron | copy file (no true PITR) |
   | Managed (RDS/Cloud SQL) | automated snapshots | provider-managed transaction logs | "restore to point in time" API |

   Default for any Tier 0/1 SQL store: **pgBackRest/WAL-G (Postgres) or Percona XtraBackup + binlog (MySQL)** with logs archived every ≤60s. Logical dumps (`pg_dump`/`mysqldump`) are a *secondary* portable copy, not your primary — they're slow to restore and lock/strain a large live DB.

3. **Retention and layout: 3-2-1 with at least one immutable copy.** 3 copies, 2 media/accounts, 1 off-site/cross-region. Make ≥1 copy **immutable** so ransomware or a compromised admin can't delete it:
   - Object-lock the bucket: S3 Object Lock **Compliance mode** (`--object-lock-mode COMPLIANCE`), or GCS bucket retention lock, or Azure immutable blob. Compliance mode = nobody, including root, can delete before expiry.
   - Put backups in a **separate account/project** from production with write-only (no-delete) IAM for the backup writer — same-account backups die with the account.
   - Lifecycle: hot (last 7d, fast restore) → warm (30d) → cold/Glacier (90–365d per compliance). Cold tiers add hours to RTO — never put your RTO-critical recent backups in Glacier.
   - Retention must cover **detection lag**: corruption found on day 10 needs a day-9 good copy, so retain > realistic time-to-detect.

4. **Verify restorability automatically — an untested backup is a hypothesis, not a backup.** Schedule a job that restores to a *scratch* environment and validates, on every backup or at least nightly:
   ```bash
   # nightly restore drill (Postgres / pgBackRest), exits non-zero on any failure
   pgbackrest --stanza=main --type=time \
     --target="$(date -u -d '10 min ago' +'%Y-%m-%d %H:%M:%S')" restore
   pg_ctl start -D "$PGDATA" -w -t 600
   # validate: structural + content, not just "it started"
   psql -tAc "SELECT count(*) FROM orders"            | grep -qE '^[0-9]+$'
   psql -tAc "SELECT pg_catalog.pg_database_size('app')"   # > 0
   RESTORE_SECS=$SECONDS; echo "restore took ${RESTORE_SECS}s (RTO budget: 3600s)"
   [ "$RESTORE_SECS" -le 3600 ] || { echo "RTO BREACH"; exit 1; }
   ```
   Validate **content** (row counts vs a known watermark, `pg_amcheck`/`CHECKSUM TABLE`, app-level invariant query), measure wall-clock restore time, and **fail the job loud** (page) if it breaks or exceeds RTO. The restore time you measure here *is* your real RTO — the planned number is fiction until measured.

5. **Have a procedure for each recovery shape — they are not the same command.**
   - **Full restore (host lost):** provision, restore latest base, replay logs to "now", re-point app.
   - **PITR (bad deploy/poison write at 14:32):** restore base before 14:32, replay to `recovery_target_time = '14:31:59'`, `pause_at_recovery_target=on`, inspect, then promote. Recover to *just before* the bad event.
   - **Single-table / logical restore:** restore into a throwaway instance, `pg_dump -t orders` (or `mysqldump --no-create-info`) that table, load into prod — never restore the whole cluster to fix one table.
   - **Corruption:** do **not** overwrite the only good copy. Restore to a new instance, run `pg_amcheck`/`mongod --repair`/`CHECK TABLE`, diff, cut over only after validation. Promote a healthy replica only after confirming the corruption didn't already replicate.

6. **Cross-region/replica DR: pick sync vs async deliberately, and fence against split-brain.**

   | | Sync replication | Async replication |
   |---|---|---|
   | RPO | ~0 (no committed loss) | replica lag (seconds–minutes) |
   | Write latency | + cross-region RTT every commit | none (local commit) |
   | Use for | Tier 0 only, regions < ~10ms apart | everything else (default) |

   Default to **async** unless RPO≈0 is mandated and you accept the write-latency tax. Failover = promote standby + cut traffic over. **Split-brain is the real danger**: if the old primary comes back and also takes writes, you get divergent histories that can't be merged. Enforce a quorum/leader-election (Patroni + etcd/Consul, Orchestrator, or RDS Multi-AZ which fences for you) and **STONITH-fence** the old primary (revoke its network/credentials) *before* promoting. Cut traffic via low-TTL DNS (≤30s) or, better, a connection proxy (PgBouncer/HAProxy/ProxySQL) that flips backends instantly — DNS TTL caching makes raw DNS failover slow and uneven.

7. **Write the runbook with exact commands, and rehearse it (game day).** The runbook lists per scenario: detection signal → exact restore/promote commands (copy-pasteable, with placeholders) → validation queries → traffic-cutover step → rollback-of-the-rollback. Store it **outside** the system it recovers (it's useless if it lives only in the DB that's down). Schedule a **DR drill quarterly** (Tier 0: monthly) that actually fails over to the standby/restored copy under timing — measure RTO/RPO against target, file the gaps. A runbook never executed end-to-end is presumed broken.

## Common Errors

- **Never restore-testing.** The #1 cause of "we had backups but couldn't recover." A backup that has never been restored is unproven; automate the drill (step 4) so success/failure is observed continuously, not discovered during the outage.
- **Snapshot-only, calling it PITR.** Nightly snapshots = up to 24h RPO and you can only land on snapshot boundaries. PITR requires continuous WAL/binlog/oplog archiving (step 2). If asked for "restore to any second," snapshots alone cannot.
- **Same blast radius.** Backups in the same account/region/bucket as prod die with it — one compromised credential, one region outage, one `DROP` and both the data and its backup are gone. Cross-account + cross-region + immutable is the point.
- **No immutability → ransomware/insider wipes the backups too.** Mutable backups are deleted in the same attack that hit prod. Use object-lock Compliance mode / retention lock on ≥1 copy.
- **Replica treated as a backup.** A replica faithfully replicates `DELETE FROM users` and corruption in milliseconds. Replication is for availability/failover; it is **not** a backup and gives zero protection against logical errors. You need both.
- **Logical dump as the primary backup for a large DB.** `pg_dump`/`mysqldump` of a multi-TB DB takes hours to restore and strains/locks the live DB while running — blows RTO. Use physical base + log archiving; keep logical dumps as a secondary portable copy only.
- **RTO ignores restore *and* warm-up.** Real RTO = provision + transfer + restore + log replay + cache/index warm-up + cutover. Cold-tier (Glacier) retrieval alone can be hours. Measure end-to-end; don't quote the `restore` command's runtime.
- **Failover with no split-brain fencing.** Promoting a standby while the old primary still accepts writes forks history irrecoverably. Fence (STONITH) the old primary and use quorum-based promotion before flipping traffic.
- **DNS-only cutover with long TTL.** A 300s+ TTL means clients keep hitting the dead primary long past promotion. Use TTL ≤30s, or a connection proxy that switches backends instantly.
- **Backup job "succeeds" but the file is empty/corrupt.** Exit-0 ≠ valid backup. Verify object size > expected floor, checksum, and a test-restore — not just the job's return code.
- **Retention shorter than detection lag.** Corruption noticed on day 10 with 7-day retention = no clean copy exists. Retain past your realistic time-to-detect, and keep a longer-interval cold copy.

## Verify

1. **RPO/RTO are written and tiered.** Every stateful datastore has an explicit RPO and RTO number tied to a business tier (step 1) — not an implicit "nightly."
2. **PITR proven, not assumed.** Restore to an *arbitrary* timestamp between two base backups (e.g. 14:31:59 yesterday) lands the data at that second — proves continuous log archiving works, not just snapshots.
3. **Automated restore drill is green and timed.** The nightly/per-backup test-restore to scratch passes (structural + content + invariant checks) and its measured wall-clock ≤ RTO budget; a failure or RTO breach **pages**.
4. **3-2-1 + immutability holds.** ≥3 copies across ≥2 accounts/regions, ≥1 with object-lock Compliance/retention-lock that even root cannot delete before expiry — confirm by attempting (and failing) to delete a locked object.
5. **Independent blast radius.** Deleting/encrypting the prod bucket/account leaves a usable backup intact in another account/region.
6. **Each recovery shape has a tested path:** full restore, PITR-to-timestamp, single-table logical restore, and corruption-to-new-instance — each with copy-pasteable commands in the runbook.
7. **Failover fences and cuts over fast.** A drill promotion fences the old primary (it cannot take writes post-promotion) and traffic moves via ≤30s-TTL DNS or a proxy; no split-brain divergence after.
8. **Game day actually ran.** A dated DR drill within the cadence (≤1 quarter; Tier 0 ≤1 month) failed over end-to-end, measured RPO/RTO vs target, and logged the gaps.

Done = every datastore has written RPO/RTO targets, PITR (base + continuous logs) restoring to an arbitrary timestamp, an automated restore drill that is green and within RTO, ≥1 immutable cross-account/region copy, and a runbook proven by a dated end-to-end DR drill — restore time **measured**, never merely planned.
