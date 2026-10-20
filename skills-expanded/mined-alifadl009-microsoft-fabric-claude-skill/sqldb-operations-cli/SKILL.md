---
name: sqldb-operations-cli
description: >
  Diagnose SQL database in Fabric performance via sqlcmd against Query Store, DMVs,
  sys.dm_db_resource_stats, and Extended Events on the OLTP endpoint. Identifies the top
  resource-consuming, slowest, or most expensive queries and handles query-performance
  ranking, blocking-chain, missing-index, and plan-regression diagnostics. For routine data
  queries use the sqldb-consumption-cli skill; for schema changes use the sqldb-authoring-cli skill.
  Triggers: "query store slow query analysis sqldb top queries",
  "top resource-consuming queries from query store sqldb",
  "slowest queries sql database in Fabric query store",
  "most expensive queries sqldb query store",
  "sql database in Fabric blocked sessions head blocker chain sqlcmd",
  "sqldb missing index recommendation",
  "sqldb regressed plan instability sqlcmd",
  "sqldb extended events trace".
---

> **Update Check — ONCE PER SESSION (mandatory)**
> The first time this skill is used in a session, run the **check-updates** skill before proceeding.
> - **GitHub Copilot CLI / VS Code**: invoke the `check-updates` skill.
> - **Claude Code / Cowork / Cursor / Windsurf / Codex**: compare local vs remote package.json version.
> - Skip if the check was already performed earlier in this session.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering

# SQL Database in Fabric — Operations & Diagnostics CLI Skill

Deep performance diagnostics for **SQL database in Fabric** via **`sqlcmd`** against Query Store, DMVs, `sys.dm_db_resource_stats`, and Extended Events. All analytical queries are read-only; the optional XE session creation is dropped at the end of the investigation.

## Prerequisites

- Tools and auth: see [COMMON-CLI.md § Authentication Recipes](../../common/COMMON-CLI.md#authentication-recipes) and [§ SQL / TDS Data-Plane Access](../../common/COMMON-CLI.md#sql--tds-data-plane-access).
- Permissions: `VIEW DATABASE STATE` for DMVs; `ALTER ANY EVENT SESSION` to create XE sessions.
- Connect to the **SQL database (OLTP) endpoint** — the SQL analytics endpoint has no Query Store/DMVs.

## Table of Contents

| Topic | Reference |
|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) — **read first** |
| SQL / TDS Data-Plane Access (sqlcmd, auth) | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../common/COMMON-CLI.md#sql--tds-data-plane-access) |
| CLI Gotchas (audience, escaping, expiry) | [COMMON-CLI.md § Gotchas & Troubleshooting](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) |
| Endpoint Selection (use OLTP) | [SQLDB-CONSUMPTION-CORE.md § Endpoint Selection](../../common/SQLDB-CONSUMPTION-CORE.md#endpoint-selection) |
| Performance and Monitoring foundations | [SQLDB-CONSUMPTION-CORE.md § Performance and Monitoring](../../common/SQLDB-CONSUMPTION-CORE.md#performance-and-monitoring) |
| Limitations Reference (unsupported features, DMVs) | [SQLDB-AUTHORING-CORE.md § Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference) |
| Mirroring Considerations | [SQLDB-AUTHORING-CORE.md § Mirroring Considerations](../../common/SQLDB-AUTHORING-CORE.md#mirroring-considerations) |
| **All diagnostic T-SQL** | [references/query-reference.md](references/query-reference.md) |
| **Investigation Workflows** | [SKILL.md § Investigation Workflows](#investigation-workflows) |
| **Examples** | [references/examples.md](references/examples.md) |

For Fabric topology, capacity, and platform auth basics see [COMMON-CORE.md](../../common/COMMON-CORE.md).

---

## Connection

Diagnostics run against the **SQL database (OLTP) endpoint**. For endpoint discovery, authentication, and `sqlcmd` connection guidance, use the shared CLI instructions in [COMMON-CLI.md](../../common/COMMON-CLI.md) rather than inline setup here.

Once connected, use the diagnostic workflows below and the full T-SQL catalog in [query-reference.md](references/query-reference.md).

---

## Diagnostic Areas

All SQL is in [query-reference.md](references/query-reference.md). Step-by-step orchestration in [Investigation Workflows](#investigation-workflows) below.

### Performance Investigation
- **Volatile Query Detection** ([SQL](references/query-reference.md#volatile-query-detection-coefficient-of-variation)) — CV% > 100 = blocking, plan regression, or parameter sniffing. **First** step for intermittent slowness.
- **Wait Category Analysis** ([SQL](references/query-reference.md#wait-category-analysis)) — Lock vs CPU vs IO vs Memory; follow Root Cause Decision Tree.
- **Top Resource Consumers** ([SQL](references/query-reference.md#top-resource-consuming-queries--by-duration-last-hour)) — by duration / IO / CPU.
- **Recently Regressed Queries** ([SQL](references/query-reference.md#recently-regressed-queries)) — last hour vs prior 24h.
- **Multi-Plan Queries** ([SQL](references/query-reference.md#multi-plan-queries-plan-instability)) — `sys.sp_query_store_force_plan` is supported but use sparingly; auto-tuning may correct over time.

### Pressure Diagnostics
- **CPU Pressure** ([SQL](references/query-reference.md#cpu-pressure-investigation)) — `avg_cpu_percent ≥ 80` over 10 min = sustained; `non_cpu_to_cpu_ratio > 5` = waiting on resources, not CPU-bound.
- **IO Pressure** ([SQL](references/query-reference.md#io-pressure-investigation)) — `avg_data_io_percent ≥ 80` (data); `avg_log_write_percent ≥ 80` (log, often un-batched DML).
- **Resource Trend** ([SQL](references/query-reference.md#resource-usage-overview)) — `sys.dm_db_resource_stats` retains only **1 hour** of 15-second samples; persist or use Query Store for longer windows.

### Blocking Diagnostics
> Optimized locking is on by default — no traditional lock escalation. Most blocking comes from long-running transactions, app-side held transactions, or hot-row contention.
- **Live Blocking** ([SQL](references/query-reference.md#live-blocking)) — blocked sessions, head blocker, chain. If head blocker is **idle with `open_transaction_count > 0`** → application is holding an open transaction; fix client code.
- **Intermittent Blocking** ([SQL](references/query-reference.md#blocking--setup-extended-events-session)) — XE session create / read / clean-up. **`ON DATABASE` only** (not `ON SERVER`); use `ring_buffer` target. Always clean up.

### Index and Statistics Health
- **Auto-Tuning** ([SQL](references/query-reference.md#auto-tuning-recommendations-check-first)) — **always check first**; engine auto-creates/drops indexes.
- **DMV Missing Index** ([SQL](references/query-reference.md#dmv-missing-index-recommendations)) — only if auto-tuning has nothing pending. Rank by `index_advantage = user_seeks * avg_total_user_cost * (avg_user_impact * 0.01)`. DMV stats reset on restart.
- **Statistics Staleness** ([SQL](references/query-reference.md#statistics-staleness-check)) — defaults: `≥ 100,000 rows` and `≥ 10%` modification.
- **Table Access Patterns** ([SQL](references/query-reference.md#table-access-patterns)) — hot tables for indexing/denormalization candidates.

---

## Investigation Workflows

Step-by-step orchestration. Each step links to the corresponding query in [query-reference.md](references/query-reference.md).

### Workflow 1: "Why is my SQL database in Fabric slow?"
1. [Resource Usage Overview](references/query-reference.md#resource-usage-overview) (last 30 min) — confirm pressure.
2. If sustained CPU/IO pressure → [CPU Pressure](references/query-reference.md#cpu-pressure-investigation) or [IO Pressure](references/query-reference.md#io-pressure-investigation).
3. [Volatile Query Detection](references/query-reference.md#volatile-query-detection-coefficient-of-variation).
4. [Wait Category Analysis](references/query-reference.md#wait-category-analysis); follow the Root Cause Decision Tree.
5. If Lock-dominant → Workflow 3 (Blocking). If CPU/IO-dominant → [Top Resource Consumers](references/query-reference.md#top-resource-consuming-queries--by-duration-last-hour) and [Multi-Plan Queries](references/query-reference.md#multi-plan-queries-plan-instability).

### Workflow 2: "Has performance degraded recently?"
1. [Recently Regressed Queries](references/query-reference.md#recently-regressed-queries) (1h vs 24h).
2. For each regressed query → [Multi-Plan Queries](references/query-reference.md#multi-plan-queries-plan-instability) to detect plan changes.
3. [Resource Usage Overview](references/query-reference.md#resource-usage-overview) to check for new pressure.
4. [Auto-Tuning Recommendations](references/query-reference.md#auto-tuning-recommendations-check-first) — recent recommendations may indicate workload shift.

### Workflow 3: "Diagnose blocking"
1. [Live Blocking](references/query-reference.md#live-blocking) (Blocked Sessions, Head Blocker, Chain).
2. If blocking found → inspect head blocker's `open_transaction_count`, SQL text, `program_name`.
3. If head blocker is **idle with `open_transaction_count > 0`** → application bug; fix client code (uncommitted transaction).
4. If intermittent (no live rows) → [Setup XE Session](references/query-reference.md#blocking--setup-extended-events-session), wait, then [Read XE Data](references/query-reference.md#read-xe-session-data) and [Clean Up](references/query-reference.md#clean-up-xe-session).
5. Resolution patterns: reduce transaction scope; use RCSI for hot-row contention; check for missing indexes causing scans.

### Workflow 4: "Should I add an index?"
1. [Auto-Tuning Recommendations](references/query-reference.md#auto-tuning-recommendations-check-first) **first**.
2. If nothing pending → [DMV Missing Index Recommendations](references/query-reference.md#dmv-missing-index-recommendations).
3. For a specific table → [Missing Indexes for a Specific Table](references/query-reference.md#missing-indexes-for-a-specific-table).
4. [Statistics Staleness Check](references/query-reference.md#statistics-staleness-check) — stale stats can produce false "missing index" symptoms.

### Workflow 5: "Resource consumption baseline"
1. [Resource Usage Overview](references/query-reference.md#resource-usage-overview) (last 30 min).
2. [Top Resource Consumers](references/query-reference.md#top-resource-consuming-queries--by-duration-last-hour) by CPU (last 24h).
3. [Table Access Patterns](references/query-reference.md#table-access-patterns) — identify hot tables.

---

## Fabric SQL DB Constraints (NEVER recommend)

Full list of unsupported features: [SQLDB-AUTHORING-CORE.md § Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference). Operations-critical items:

| Do NOT Recommend | Why | Recommend Instead |
|---|---|---|
| Server-scoped DMVs (`sys.dm_os_*`, `sys.configurations`) | Not exposed | `sys.dm_db_resource_stats`, Query Store views |
| `EXECUTE AS` for security testing | Not supported | Connect as the actual user identity |
| `CREATE EVENT SESSION ... ON SERVER`, file-target XE | Database-scoped only | `... ON DATABASE` with `ring_buffer` target |
| Trace flags / `DBCC TRACEON` | Not supported | Re-architect query or use Query Store hints |
| Manual lock escalation tuning | Optimized locking eliminates escalation | Address root cause (long transactions, hot rows) |
| SQL analytics endpoint for diagnostics | DMVs/Query Store don't exist there | Connect to the SQL database (OLTP) endpoint |
| Aggressive `sp_query_store_force_plan` | Masks root cause | Fix stats / parameter sniffing first; force only as a stop-gap |

---

## Best Practices

For consumption foundations see [SQLDB-CONSUMPTION-CORE.md § Performance and Monitoring](../../common/SQLDB-CONSUMPTION-CORE.md#performance-and-monitoring).

- **Volatile detection first** — narrows scope quickly for intermittent slowness.
- **Use the OLTP endpoint** — the analytics endpoint has no Query Store/DMVs.
- **Trust auto-tuning** — only override after a recommendation has been pending for a representative period.
- **Always clean up XE sessions** at the end of an investigation.
- **Adjust `DATEADD` lookback windows** to the user's investigation scope.
- **Persist `sys.dm_db_resource_stats`** if you need > 1 hour of history.
- **High CV% over time** → structural fix needed (RCSI, parameterization, index strategy), not plan forcing.

---

## Gotchas, Rules, Troubleshooting

CLI/auth issues: [COMMON-CLI.md § Gotchas](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific). Platform issues: [SQLDB-CONSUMPTION-CORE.md § Gotchas](../../common/SQLDB-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference).

### MUST DO
- Check [Constraints](#fabric-sql-db-constraints-never-recommend) before recommending optimizations.
- Connect to the **SQL database (OLTP) endpoint** — never analytics.
- Run **volatile detection first** for intermittent slowness.
- Check **auto-tuning** before suggesting manual indexes.
- **Clean up XE sessions** when finished.
- Report actual query output — do not fabricate.

### PREFER
- Start with high-level signals (resource trend, volatile detection) before drilling into individual queries.
- Use the **wait category** decision tree to choose between blocking, CPU, IO, or memory paths.
- Combine queries via the [Investigation Workflows](#investigation-workflows) for end-to-end investigations.
- Use `-i file.sql` for the XE session creation block (here-doc has portability quirks).
- Use the SQL Database **Performance Dashboard** (Fabric portal) for visual context alongside CLI queries.
- Set `SET NOCOUNT ON;` at the top of multi-statement scripts to keep CSV output clean.

### AVOID
- Recommending Fabric-unsupported features (CDC, Always Encrypted, in-memory, ledger, server-scoped DMVs, file-target XE).
- Running diagnostics on the **SQL analytics endpoint**.
- Manually creating indexes without checking auto-tuning first.
- Leaving XE sessions running after an investigation.
- Forcing plans via `sp_query_store_force_plan` instead of fixing root cause.
- Recommending lock-escalation tuning (optimized locking eliminates escalation).

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Invalid object name 'sys.query_store_*'` | Querying analytics endpoint | Connect to OLTP endpoint |
| Volatile detection returns no rows | Lookback too short / no recent activity | Expand `DATEADD(MINUTE, -60, ...)` to `-1440` |
| `sys.dm_db_resource_stats` empty | Lookback exceeds 1-hour retention | Reduce window; or use Query Store |
| Permission error on DMVs | Missing `VIEW DATABASE STATE` | `GRANT VIEW DATABASE STATE TO [user@tenant.com]` |
| Permission error on `CREATE EVENT SESSION` | Missing `ALTER ANY EVENT SESSION` | `GRANT ALTER ANY EVENT SESSION TO [user@tenant.com]` |
| XE session captures nothing | LIKE filter too narrow / session in `STOP` state | Check `sys.dm_xe_database_sessions.state`; widen filter |
| Multi-plan query has no obvious bad plan | Parameter sniffing | `OPTION (RECOMPILE)` or `OPTIMIZE FOR` hint |

---

## Examples

See [references/examples.md](references/examples.md) for full prompt/response patterns covering:
- **Diagnose intermittent slowness** — volatile query detection → wait analysis
- **Diagnose live blocking** — head blocker with idle open transaction
- **Recommend an index** — auto-tuning check → DMV ranking → DDL suggestion
