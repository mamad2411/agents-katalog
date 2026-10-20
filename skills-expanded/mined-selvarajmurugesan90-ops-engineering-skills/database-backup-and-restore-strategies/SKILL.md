---
name: database-backup-and-restore-strategies
description: >
  Cross-database backup tooling and restore-testing discipline:
  pg_dump/pg_basebackup for PostgreSQL, mysqldump/Percona XtraBackup for
  MySQL/MariaDB, and mongodump/mongorestore for MongoDB — logical vs.
  physical backup trade-offs, point-in-time recovery, and why an
  untested restore is not a real backup. Use when the user asks to
  "set up database backups," "restore from a pg_basebackup," "why did
  our mysqldump restore fail," "test our backup/restore process," "set
  up point-in-time recovery," or "design a backup retention policy."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Database Backup and Restore Strategies

## Purpose

A backup that has never been restored is a hypothesis, not a safety
net — the single most common cause of a "we had backups but couldn't
recover" incident is a backup process that ran successfully (per its
own logs/exit code) but produced an artifact that was never actually
tested end-to-end against a real restore. This skill covers the
dominant backup tooling for the three most common relational/document
engines — **pg_dump**/**pg_basebackup** for PostgreSQL,
**mysqldump**/**Percona XtraBackup** for MySQL/MariaDB, and
**mongodump**/**mongorestore** for MongoDB — the logical-vs-physical
backup trade-off that applies across all of them, and the restore-
testing discipline that turns a backup process into an actual, provable
recovery capability rather than an assumption.

## When to use

- Designing a new backup strategy for a database that doesn't have one,
  or auditing an existing one for gaps (untested restores, missing
  point-in-time recovery, retention that doesn't match compliance
  requirements).
- Choosing between a logical backup (`pg_dump`, `mysqldump`,
  `mongodump`) and a physical backup (`pg_basebackup`, XtraBackup, a
  filesystem/volume snapshot) for a specific database's size and
  recovery-time requirements.
- Setting up point-in-time recovery (PITR) so a restore can target a
  specific moment (e.g. just before an accidental destructive
  operation) rather than only the last full backup.
- A restore attempt fails, is much slower than expected, or produces
  data that doesn't match what was expected.
- Before any operation flagged destructive elsewhere in this repo
  (`TRUNCATE`, `DROP DATABASE`/`DROP KEYSPACE`, an untested migration
  rollback, a retention policy that permanently deletes data) — this
  skill is the prerequisite safety net those warnings point back to.

## Prerequisites & environment

- Sufficient storage for backup artifacts, sized for the *retention
  policy* (how many historical backups are kept), not just one backup's
  size — a common under-provisioning mistake.
- Network/IAM access from the backup process to wherever artifacts are
  stored (object storage, a separate backup host) — credentials scoped
  specifically to backup write access, not broad database-admin
  credentials reused for convenience.
- For physical backups: enough free disk/I/O headroom on the source
  database during the backup window, since streaming a full physical
  copy is I/O- and often CPU-intensive (compression) while the database
  continues serving live traffic.
- A separate, isolated environment (not the production database itself)
  to actually perform restore tests against — a "successful" backup
  validated only by re-reading the archive's own metadata, without an
  independent restore, does not confirm the backup is usable.
- For point-in-time recovery specifically: continuous WAL archiving
  (PostgreSQL), binary log retention (MySQL/MariaDB), or oplog-based
  replication (MongoDB) already configured and retained for at least as
  long as the interval between full backups — PITR requires the
  continuous log, not just periodic full snapshots.

## Step-by-step guidance

### 1. Choose logical vs. physical backups deliberately, per database size and recovery-time requirement

**Logical backups** (`pg_dump`, `mysqldump`, `mongodump`) export data as
a portable, engine-version-independent representation (SQL statements or
a structured document dump) — the resulting artifact is
human-inspectable, can be restored into a different major version or
even a differently-configured instance, and is the natural choice for
smaller databases or for extracting a specific subset of data. They
scale poorly for large databases: both dump and restore that touch every
row take time proportional to data volume, and a large logical restore
can take hours where a physical restore of the same data takes minutes.

**Physical backups** (`pg_basebackup`, Percona XtraBackup, filesystem/
block-storage snapshots) copy the database's actual on-disk files —
much faster for both backup and restore at scale, since they don't
serialize/deserialize every row, but the resulting artifact is tied to
the same major engine version and (for some tools) similar
configuration, and isn't naturally human-inspectable or partially
restorable to a subset of data the way a logical dump is.

Choose based on database size and required recovery time objective
(RTO): a multi-hundred-GB-plus production database with a tight RTO
needs physical backups (and likely PITR via WAL/binlog replay) as the
primary strategy, with logical dumps reserved for smaller
databases, ad hoc data extraction, or as a supplementary,
version-portable safety net alongside the primary physical strategy.

### 2. PostgreSQL: pg_dump for logical, pg_basebackup + WAL archiving for physical/PITR

```bash
# Logical: portable, human-inspectable, slow to restore at scale
pg_dump -h <HOST> -U <USER> -Fc -f appdb_backup.dump appdb
```
```bash
# Physical base backup: fast at scale, requires matching major version to restore
pg_basebackup -h <PRIMARY_HOST> -U replicator -D /backup/base -Fp -Xs -P
```
For point-in-time recovery, pair a periodic `pg_basebackup` with
continuous WAL archiving (`archive_mode = on`, `archive_command`
shipping WAL segments to durable storage) so a restore can replay WAL
up to any specific target timestamp/LSN, not just the base backup's
moment:
```ini
# postgresql.conf on the source
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'   # or a script shipping to object storage
```
```conf
# recovery target on the restored instance, e.g. to recover to just
# before an accidental production DELETE
recovery_target_time = '2026-07-28 14:32:00'
```
Validate this against the more general replication/WAL guidance in
[postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md),
since WAL retention sizing and archiving overlap directly with
replication slot management there.

### 3. MySQL/MariaDB: mysqldump for logical, XtraBackup for physical/hot backups

```bash
# Logical: fine for smaller databases, or extracting a specific schema/table
mysqldump -h <HOST> -u <USER> -p --single-transaction --routines --triggers appdb > appdb_backup.sql
```
`--single-transaction` takes a consistent snapshot for InnoDB tables
without locking them for the dump's full duration — omit it and
`mysqldump` instead takes table-level locks, which blocks writes on a
live production database for however long the dump takes, a common
accidental-outage mistake.
```bash
# Physical hot backup via Percona XtraBackup — no downtime, faster restore at scale
xtrabackup --backup --target-dir=/backup/full --user=<USER> --password=<PASSWORD>
xtrabackup --prepare --target-dir=/backup/full   # applies redo log to make the backup consistent
```
XtraBackup's `--prepare` step is not optional — a backup directory that
hasn't been prepared is not yet consistent and cannot be safely used to
start a MySQL instance from; always confirm `--prepare` completed
successfully (check its exit code and log output for
"completed OK") before considering the backup restore-ready. For
point-in-time recovery, retain binary logs covering at least the
interval since the last full backup and replay them from the backup's
recorded position forward:
```bash
mysqlbinlog --start-datetime="2026-07-28 00:00:00" \
  --stop-datetime="2026-07-28 14:32:00" \
  binlog.000123 | mysql -u <USER> -p appdb
```

### 4. MongoDB: mongodump/mongorestore, and oplog-based point-in-time recovery

```bash
mongodump --uri="mongodb://<HOST>:27017" --db=appdb --out=/backup/appdb
```
```bash
mongorestore --uri="mongodb://<TARGET_HOST>:27017" --db=appdb /backup/appdb/appdb
```
`mongodump` against a replica set member (rather than the primary)
avoids adding backup load to the node serving live writes, but confirm
the replica isn't so far behind (see oplog-window guidance in
[mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md))
that the backup reflects meaningfully stale data. For point-in-time
recovery, `mongodump --oplog` captures the oplog alongside the data
dump, allowing `mongorestore --oplogReplay` to bring the restored data
forward to a consistent point matching when the dump completed, rather
than a data set that's inconsistent across collections captured at
slightly different moments during a long-running dump.
```bash
mongodump --uri="mongodb://<HOST>:27017" --oplog --out=/backup/appdb
mongorestore --oplogReplay /backup/appdb
```
For a sharded cluster, back up each shard's replica set independently
plus the config server replica set — a backup missing the config
server's metadata cannot be restored into a coherent sharded topology.

### 5. Test every restore path — this is the step most backup processes skip

A backup strategy is not validated by a successful backup job exit
code alone. At a cadence matched to the data's actual criticality
(monthly at minimum for production-critical data; more frequently for
anything with a tight RTO), perform an actual restore into an isolated
environment and verify:
```bash
# Restore into an isolated, non-production instance
pg_basebackup ... # or the equivalent restore command for the tool in use

# Then verify data integrity independently — row counts, checksums,
# or an application-level smoke test against the restored instance
psql -h <RESTORED_HOST> -c "SELECT count(*) FROM orders;"
```
Record and track **actual measured restore time** from each test — this
is the only reliable input for whether the backup strategy meets its
recovery time objective; a restore that "should" take twenty minutes
based on data size but has never actually been timed is not a validated
RTO, it's a guess.

### 6. Design retention to match compliance and operational recovery needs, separately

Retention has two distinct drivers that are easy to conflate: how far
back you need to be able to *restore* for operational recovery (often
weeks), and how long you're required to *retain* data for compliance/
audit (often much longer, sometimes years). Configure them as
separate policies rather than one retention setting serving both —
a short operational-recovery retention window is fine for disaster
recovery but inadequate for a compliance audit requiring data from
eighteen months ago, and conversely, keeping every daily backup
indefinitely "just in case" for compliance reasons is wasteful storage
cost when only the most recent few weeks are ever actually restored
from in practice.

## Best practices

- Test a real restore into an isolated environment on a recurring
  schedule, and treat "we have backups" as an unverified claim until
  that test has actually happened — a passing backup job is not
  evidence of a working restore path.
- Choose logical vs. physical backup type based on actual database size
  and RTO, not habit — a multi-terabyte production database backed up
  only via `mysqldump`/`pg_dump` with no physical/PITR strategy is a
  common, expensive-to-discover gap.
- Configure point-in-time recovery (WAL archiving, binlog retention,
  oplog capture) wherever the recovery requirement is "restore to just
  before a specific bad event," not just "restore to last night's
  backup" — most real incidents need the former.
- Scope backup credentials narrowly (backup-write access only, not
  general database-admin credentials reused for convenience) so a
  compromised backup process/host has limited blast radius.
- Separate operational-recovery retention from compliance retention as
  distinct, independently configured policies rather than one setting
  trying to serve both purposes.
- Record actual measured restore time from every restore test, and
  treat a restore that exceeds the required RTO as a finding to act on,
  not just a data point to log.

## Common pitfalls

- **Symptom:** A restore is attempted for the first time during a real
  incident, and it fails, is missing data, or takes far longer than
  anyone expected.
  **Fix:** The backup process had never been validated with an actual
  restore — only its own success exit code was trusted. This is the
  single most common and most expensive backup failure mode; establish
  a recurring restore-test schedule immediately, even retroactively
  after an incident, and measure real restore time against the
  required RTO going forward.

- **Symptom:** A `mysqldump`-based backup of a large production
  database causes a noticeable application slowdown or outage during
  the backup window.
  **Fix:** `--single-transaction` was omitted (or isn't applicable
  because some tables use a non-transactional storage engine), so
  `mysqldump` took table-level locks for the dump's duration. Add
  `--single-transaction` for InnoDB tables, and consider XtraBackup's
  hot-backup approach instead for a large production database where
  even a brief mysqldump-induced slowdown is unacceptable.

- **Symptom:** A Percona XtraBackup restore fails to start MySQL, or
  starts but is missing recent transactions.
  **Fix:** The `--prepare` step was skipped or failed silently, leaving
  the backup directory in an inconsistent, unprepared state — a raw
  `--backup` output directory is not directly usable to start an
  instance from. Always run and verify `--prepare` completes
  successfully as part of the backup process itself, not as an
  afterthought at restore time.

- **Symptom:** A `mongorestore` into a sharded cluster produces an
  incoherent topology (chunks missing, or the cluster doesn't recognize
  its own shard metadata).
  **Fix:** The backup captured each shard's data but not the config
  server replica set's metadata (or captured it at an inconsistent
  point relative to the shard backups). Always back up the config
  server replica set alongside every shard, and use `--oplog`/
  `--oplogReplay` consistently across the whole cluster's backup/
  restore so all components restore to the same consistent point in
  time.

- **Symptom:** Someone runs a restore directly against the production
  instance "to fix" corrupted data, overwriting current production data
  with an older backup, without first confirming what data would be
  lost in the gap between the backup and now.
  **Fix:** This is a destructive action against production if done
  without care — a restore replaces (or, depending on tooling,
  merges awkwardly with) current data, and any writes since the
  backup's timestamp not captured by PITR replay are gone.
  > **Warning — destructive action.** Never restore directly on top of
  > a live production instance as a first step. Restore into an
  > isolated environment first, confirm the restored data is what's
  > actually needed (using PITR to target the correct moment if
  > available), and only then plan a deliberate, communicated cutover
  > — treating the restore itself the same way a
  > [database-schema-migration-with-liquibase-and-flyway](../database-schema-migration-with-liquibase-and-flyway/SKILL.md)
  > migration rollback is treated: a real production change requiring
  > sign-off, not an emergency shortcut.

## Worked example

**Scenario:** A team discovers, during a post-incident review, that
their PostgreSQL production database (600GB) has been backed up nightly
via `pg_dump` for two years, but no restore has ever been tested, and
the last incident took over 14 hours to (partially) recover from
because the logical restore was far slower than anyone expected.

1. Measure the actual problem: a test logical restore of the full
   600GB dump into an isolated instance is timed at just under 11
   hours — confirming logical restore time scales badly with size and
   is incompatible with the business's actual RTO requirement of under
   2 hours.
2. Switch the primary backup strategy to physical: nightly
   `pg_basebackup` plus continuous WAL archiving to object storage,
   keeping the existing `pg_dump` as a supplementary, smaller-footprint
   safety net (useful for extracting a specific table without a full
   restore) rather than removing it entirely.
   ```ini
   archive_mode = on
   archive_command = 'aws s3 cp %p s3://<BACKUP_BUCKET>/wal/%f'
   ```
3. Test a physical restore end-to-end into an isolated environment,
   timing it: full restore plus WAL replay to a specific target time
   completes in 38 minutes — comfortably inside the 2-hour RTO.
4. Establish a recurring monthly restore-test schedule (automated where
   possible: spin up an isolated instance, restore the latest backup,
   run an application-level smoke test, tear down), with restore time
   tracked as a standing metric rather than assumed from the one test.
5. Separately configure retention: 30 days of physical backups plus WAL
   for operational recovery, and a distinct 7-year logical-dump archive
   in cold object storage to satisfy the business's actual compliance
   retention requirement, confirmed with the compliance team rather
   than guessed at.
6. Document the tested, timed restore procedure as the team's actual
   incident-response runbook, replacing the previous untested
   assumption that "we have nightly backups" was itself sufficient.

## Cross-references

- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — WAL/replication-slot management that overlaps directly with continuous WAL archiving for PostgreSQL point-in-time recovery.
- [mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md) — binary log retention and GTID-based replication that a MySQL/MariaDB point-in-time recovery strategy depends on.
- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — oplog window sizing, which directly bounds how far back `mongodump --oplog`-based point-in-time recovery can reach.
- [timescaledb-time-series-operations-and-configuration](../timescaledb-time-series-operations-and-configuration/SKILL.md) — retention policies there permanently drop chunks; this skill's archive-before-drop discipline is the safety net that should precede enabling one on data with any retention requirement.
