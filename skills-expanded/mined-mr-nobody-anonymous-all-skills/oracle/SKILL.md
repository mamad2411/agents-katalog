---
name: oracle
description: "Work with Oracle Database: AWR and ASH diagnosis, execution plans, tablespace and undo sizing, partitioning, RMAN backups and safe DDL."
type: procedural
category: databases
domain: databases
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - oracle slow query
  - awr report analysis
  - ora- error troubleshooting
  - oracle tablespace full
  - oracle rman backup
keywords:
  - oracle
  - plsql
  - awr
  - ash
  - rman
  - tablespace
  - explain-plan
source: custom
enabled: true
---

# Oracle Database

## Purpose

Work with Oracle Database: AWR and ASH diagnosis, execution plans, tablespace and undo sizing, partitioning, RMAN backups and safe DDL.

## When to Use

- An Oracle workload regressed and you need AWR/ASH evidence rather than guesses.
- A tablespace, undo segment or temp space alert needs a capacity decision.
- A DDL migration must avoid invalidating dependent objects or locking hot tables.

## When NOT to Use

- The database is PostgreSQL/MySQL/SQL Server; use the matching engine skill.
- The task is purely application SQL portability with no Oracle-specific behaviour.
- You cannot obtain AWR/ASH access and the question is diagnosis-only; state the limit instead of guessing.

## Capabilities

- Read AWR and ASH output to separate DB time from wait events and top SQL.
- Size undo, temp and tablespaces from measured growth, not from defaults.
- Choose partitioning and index options with maintenance cost in mind.
- Script RMAN backup and restore validation with evidence of a successful restore.

## Inputs

- Oracle version and edition plus any Diagnostics/Tuning Pack licensing constraints.
- The failing SQL text, its bind variables and the observed elapsed time.
- Space metrics: tablespace usage, undo retention target, temp usage peak.

## Workflow

1. Collect an AWR snapshot pair or ASH sample over the window where the problem occurs.
2. Rank DB time by wait class; identify whether the bottleneck is I/O, CPU, locks or application waits.
3. Confirm the plan with `DBMS_XPLAN.DISPLAY_CURSOR` including runtime statistics.
4. Apply the smallest change (statistics, index, SQL plan baseline) and re-snapshot for the delta.
5. Document the rollback: plan baseline drop, index drop or restored backup.

## Tools

- SQL*Plus / SQLcl
- AWR, ASH and `DBMS_XPLAN`
- RMAN

## Examples

- `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(format => 'ALLSTATS LAST'));`
- `SELECT tablespace_name, used_percent FROM dba_tablespace_usage_metrics;`
- `RMAN> BACKUP DATABASE PLUS ARCHIVELOG; RESTORE DATABASE VALIDATE;`

## Safety

- Never modify a production plan without a SQL plan baseline you can revert to.
- DDL on hot tables takes exclusive locks; schedule it or use online redefinition deliberately.
- RMAN backups are only proven by a restore test on a separate host.

## Source

All-Skills canonical library (`skills/databases/oracle`). First-party skill, maintained in this repository.

## Notes

- `EXPLAIN PLAN` shows the optimizer's intention; `DISPLAY_CURSOR` shows what actually ran.
- Licensing: Diagnostics and Tuning Pack features are not free; ask before relying on them.
- Pairs with: `databases/schema-evolution`, `observability/opentelemetry`.
