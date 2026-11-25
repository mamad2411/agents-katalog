---
name: delta-lake-time-travel-ops
description: >
  Operate Delta Lake time travel safely: version/timestamp AS OF queries, DESCRIBE HISTORY,
  RESTORE TABLE, retention vs VACUUM, deletedFileRetentionDuration, logRetentionDuration,
  and recovery after bad writes. Use when Delta Lake time travel, VACUUM retention, restore
  previous version, @v or TIMESTAMP AS OF, transaction log history, or accidental overwrite
  recovery on owned lakes — not general Spark tuning or non-Delta warehouse backups.
---

# Delta Lake Time Travel Ops

## Scope And Authorization

- **In scope:** Delta tables and storage accounts you own or operate under written change control.
- **Out of scope:** Accessing other tenants’ lake data; bypassing access controls; destructive VACUUM on shared prod without approval.
- Prefer dry-runs and staging clones before RESTORE or VACUUM on production.
- Redact paths that embed account keys, SAS tokens, or customer identifiers in tickets and logs.
- Pair pipeline code changes with `code-quality-standards`; pair schema migrations with `database-migration-safety` when applicable.

## When To Use

- Recovering from bad MERGE/overwrite or bad ETL deploy via time travel or RESTORE.
- Setting retention so auditors can query historical versions without keeping files forever.
- Diagnosing “file not found” after aggressive VACUUM.
- Documenting ops runbooks for Delta `@vN` / `TIMESTAMP AS OF` reads.
- Tuning `delta.deletedFileRetentionDuration` and `delta.logRetentionDuration`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Non-Delta Iceberg/Hudi time travel | catalog skill for that table format |
| Generic Spark job performance | Spark/job performance skills |
| Full disaster recovery / cross-region backup | backup-DR runbook for your platform |
| SQL migration safety patterns | `database-migration-safety` |
| Secrets in notebooks/pipelines | `secrets-management-hygiene` |
| Implementation style baseline | `code-quality-standards` |

## Domain Concepts

| Concept | Meaning |
| --- | --- |
| Transaction log | `_delta_log` JSON/checkpoint; source of truth for versions |
| Time travel read | Query table at version or timestamp without changing data |
| RESTORE | Rewind table current state to a prior version (new commit) |
| VACUUM | Delete unreferenced data files older than retention |
| Retention | How long time travel and restore remain possible after deletes |
| Checkpoint | Compacted log for faster startup; still versioned history |

**Critical rule:** VACUUM permanently removes data files. Time travel cannot recover files already vacuumed past retention.

## Workflow

### 1. Confirm scope and success criteria

1. Record catalog/schema/table, environment (dev/stage/prod), owner, and blast radius (downstream jobs, BI).
2. Define success: e.g. restore to version N with row-count parity; or retention ≥ 7 days for audit.
3. Identify rollback: clone table first; avoid VACUUM until restore verified.

### 2. Inventory table history and properties

```sql
-- Spark SQL / Databricks SQL (owned table)
DESCRIBE HISTORY catalog.schema.table_name;
SHOW TBLPROPERTIES catalog.schema.table_name;
```

1. Note latest version, last write operation type (WRITE, MERGE, DELETE, RESTORE), and user/job id.
2. Capture current properties:

| Property | Typical concern |
| --- | --- |
| `delta.deletedFileRetentionDuration` | Default often 7 days; shorter breaks recovery |
| `delta.logRetentionDuration` | History visibility / log size |
| `delta.enableChangeDataFeed` | CDF consumers may depend on history |

3. Estimate storage cost vs recovery window with storage/metrics owners.

### 3. Baseline before destructive ops

1. Record `COUNT(*)`, partition stats, and a hash/sample of critical keys at current version.
2. Optionally `CREATE TABLE ... DEEP CLONE` or shallow clone to a recovery sandbox.
3. Snapshot relevant job configs and the commit that caused the incident.

### 4. Time travel reads (non-destructive)

```sql
-- Read historical snapshot
SELECT * FROM catalog.schema.table_name VERSION AS OF 42;
SELECT * FROM catalog.schema.table_name TIMESTAMP AS OF '2026-07-01T12:00:00';

-- Path-style (engine-specific)
-- SELECT * FROM delta.`/path/to/table`@v42
```

```python
# PySpark
df = spark.read.format("delta").option("versionAsOf", 42).load(path)
df_ts = spark.read.format("delta").option("timestampAsOf", "2026-07-01").load(path)
```

1. Validate business predicates on the historical snapshot before RESTORE.
2. Prefer exporting a corrected subset forward (INSERT/MERGE fix-forward) when full RESTORE is too disruptive.

### 5. RESTORE when rewind is required

```sql
-- Rewinds current pointer via a new commit (history preserved)
RESTORE TABLE catalog.schema.table_name TO VERSION AS OF 42;
-- or TO TIMESTAMP AS OF '...'
DESCRIBE HISTORY catalog.schema.table_name;  -- confirm RESTORE entry
```

1. Pause writers (jobs, streams) during RESTORE to avoid races.
2. Re-run validation counts and downstream smoke tests.
3. Communicate new “current” version to streaming consumers and CDF users.

### 6. VACUUM and retention policy (authorized change window)

```sql
-- Dry-run style: list what would be deleted (engine-specific; Databricks supports DRY RUN)
VACUUM catalog.schema.table_name RETAIN 168 HOURS DRY RUN;

-- Destructive: only after approval; retention must be >= deletedFileRetentionDuration intent
VACUUM catalog.schema.table_name RETAIN 168 HOURS;
```

```sql
-- Align table properties with policy (example: 7 days)
ALTER TABLE catalog.schema.table_name
SET TBLPROPERTIES (
  'delta.deletedFileRetentionDuration' = '7 days',
  'delta.logRetentionDuration' = '30 days'
);
```

1. Never set retention to 0 hours on shared prod to “save space” without approval.
2. Disable or carefully control `spark.databricks.delta.retentionDurationCheck.enabled` overrides—bypassing checks is a foot-gun.
3. Coordinate with legal/audit minimum retention for the dataset class.

### 7. Verify, observe, hand off

1. After restore: history shows RESTORE; metrics and job success green; sample queries match baseline.
2. After VACUUM: confirm expected free space; attempt time travel only within retention (older should fail as expected).
3. Document runbook: who can VACUUM/RESTORE, retention SLOs, clone-before-vacuum checklist.
4. Alert on unexpected large deletes, failed vacuums, or history gaps.

## Incident decision tree

| Symptom | First action |
| --- | --- |
| Bad ETL overwrite today | DESCRIBE HISTORY → time travel validate → RESTORE or fix-forward |
| “File does not exist” on old version | Likely vacuumed; recover from clone/backup only |
| Time travel works but storage huge | Plan VACUUM with retention ≥ policy; clone critical tables |
| Streaming broke after RESTORE | Reset offsets/checkpoints per stream design; re-bootstrap |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Recovery | Clone + validate + RESTORE in window | VACUUM first “to clean up” |
| Retention | Policy-aligned 7d+ for prod | 0h retention to cut cost |
| Reads | VERSION/TIMESTAMP AS OF for forensics | Silent overwrite without history check |
| Access | Job identity least privilege on path | Shared keys in notebooks |
| Change | Ticketed vacuum with DRY RUN | Ad-hoc vacuum on prod during peak |

## Output Checklist

- [ ] Table identity, owner, env, authorization recorded
- [ ] DESCRIBE HISTORY and TBLPROPERTIES captured
- [ ] Baseline counts/samples before RESTORE/VACUUM
- [ ] Non-destructive time travel validation completed when recovering
- [ ] RESTORE or fix-forward applied with writers paused as needed
- [ ] VACUUM only with approved retention and evidence of dry-run/intent
- [ ] Retention properties match org policy
- [ ] Downstream jobs/streams verified
- [ ] Runbook updated; residual risk noted
- [ ] `code-quality-standards` applied if pipeline code changed

## Rules

- Owned/authorized lakes only; never VACUUM to hide evidence of an incident.
- Prefer fix-forward when RESTORE breaks long-running consumers.
- Time travel is not a backup substitute for cross-region disaster recovery.
- Keep originals of clone/backup paths documented; redact credentials.
- Focus this skill on Delta time travel, RESTORE, retention, and VACUUM safety.
