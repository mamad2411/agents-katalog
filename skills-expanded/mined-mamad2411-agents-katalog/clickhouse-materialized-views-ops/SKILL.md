---
name: clickhouse-materialized-views-ops
description: >
  Operate ClickHouse materialized views safely: insert-triggered MVs, target engine
  choice, rebuilds, lag/backfill, storage growth, and POPULATE pitfalls. Use for owned
  CH analytics pipelines when adding aggregations or fixing stuck/oversized MVs —
  not for generic app caching or ClickHouse RBAC (see clickhouse-access-control).
---

# ClickHouse Materialized Views Ops

## Scope And Authorization

- **In scope:** owned ClickHouse analytics clusters; authorized schema changes.
- **Out of scope:** destructive DROP/TRUNCATE on production without change control and backup plan.
- Prefer non-peak rebuilds; estimate bytes written before POPULATE.
- Redact query text with PII from ops tickets when possible.
- Pair DDL with `code-quality-standards` and access skill for who may ALTER.

## When To Use

- Creating or altering **MATERIALIZED VIEW** pipelines (source → MV → target table).
- Fixing lag, missing data after schema change, or runaway parts/storage.
- Rebuilding aggregates after bug in MV SELECT.
- Tokens: materialized view, POPULATE, TO table, AggregatingMergeTree, refreshable MV (version-dependent).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Access control / grants | `clickhouse-access-control` |
| Dictionaries | `clickhouse-dictionaries` |
| ReplicatedMergeTree replication repair | `clickhouse-replicated-merge-tree` |
| Application cache invalidation | caching skills |
| Kafka engine deep dive | Kafka/CH integration runbook |

## MV Mental Model

| Piece | Role |
| --- | --- |
| Source table | Inserts (or engine stream) trigger MV |
| MV SELECT | Transform/aggregate applied to **inserted blocks** |
| Target table | Stores MV output; query this, not the MV “storage” in modern style |
| POPULATE | One-shot backfill of existing source data (can be heavy / inconsistent) |

**Important:** classic MVs process **new inserts**, not arbitrary updates/deletes on source. Design accordingly.

## Workflow

### 1. Confirm scope and success criteria

1. Pipeline name, source/target, grain of aggregation, freshness SLO, owners.
2. Success: inserts flow; target row counts/metrics match expectations; storage within budget.
3. Rollback: detach MV, pause producers, restore target snapshot if needed.

### 2. Inventory MVs and dependencies

```sql
SELECT database, name, engine, as_select, create_table_query
FROM system.tables
WHERE engine LIKE '%MaterializedView%';

SHOW CREATE TABLE analytics.mv_events_1m;
SELECT * FROM system.replicas WHERE table = 'events_1m';  -- if replicated target
```

1. Map source → MV → target → downstream consumers.
2. Note whether target is Summing/Aggregating/Replacing MergeTree.

### 3. Baseline metrics

```sql
SELECT table, sum(rows), formatReadableSize(sum(bytes_on_disk))
FROM system.parts
WHERE active AND database = 'analytics'
GROUP BY table;

-- insert rate / lag proxies via max(event_time) vs now()
SELECT max(event_time), now() FROM analytics.events_1m;
```

1. Capture parts count, detached parts, replication queue if any.
2. Record current MV definition hash/version in git.

### 4. Create or change MVs safely

**Recommended pattern: explicit target + MV TO target**

```sql
CREATE TABLE IF NOT EXISTS analytics.events_1m
(
    window_start DateTime,
    tenant_id UInt32,
    events AggregateFunction(count, UInt64)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(window_start)
ORDER BY (tenant_id, window_start);

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_events_1m
TO analytics.events_1m
AS
SELECT
    toStartOfMinute(ts) AS window_start,
    tenant_id,
    countState() AS events
FROM analytics.events_raw
GROUP BY window_start, tenant_id;
```

**Backfill without risky POPULATE when possible:**

```sql
INSERT INTO analytics.events_1m
SELECT
    toStartOfMinute(ts) AS window_start,
    tenant_id,
    countState() AS events
FROM analytics.events_raw
WHERE ts >= toDateTime('2026-01-01 00:00:00')
GROUP BY window_start, tenant_id;
```

1. Avoid `POPULATE` on huge sources during peak; prefer batched `INSERT SELECT`.
2. Schema changes: often **create new target + new MV**, dual-write/backfill, swap consumers, drop old.
3. Filter MVs early (`WHERE`) to cut storage.
4. Align PARTITION/ORDER with query patterns; TTL on target for retention.

### 5. Verify with evidence

```sql
-- Compare source vs aggregate for a fixed window
SELECT count() FROM analytics.events_raw
WHERE ts >= X AND ts < Y AND tenant_id = 1;

SELECT countMerge(events) FROM analytics.events_1m
WHERE window_start >= X AND window_start < Y AND tenant_id = 1;

SYSTEM FLUSH LOGS;
-- Check query/insert errors in system.text_log / query_log as available
```

1. Insert a known test row; confirm it appears in target within SLO.
2. Detach MV and confirm inserts to source no longer land in target (control test in staging).
3. Storage: parts count stable; merges not backlogged forever.

### 6. Operate: lag, rebuild, incidents

| Symptom | Checks | Actions |
| --- | --- | --- |
| Target lagging | max(ts), insert errors, disk | Fix SELECT errors; scale insert; pause heavy merges |
| Duplicate aggregates | engine choice, double MV | Ensure single MV path; use AggMergeTree correctly |
| Too many parts | insert patterns | Batch inserts; adjust merge settings carefully |
| Bad historical data | logic bug | Rebuild new table; atomic consumer cutover |
| MV blocks inserts | MV exception on insert | Fix MV; `DETACH` temporarily with ticket |

```sql
DETACH TABLE analytics.mv_events_1m;  -- emergency, authorized
-- fix, then ATTACH
ATTACH TABLE analytics.mv_events_1m;
```

### 7. Hand off

1. Document grain, watermark, rebuild procedure, disk budget.
2. Alerts: lag, failed inserts, parts explosion, disk > threshold.
3. Grants for INSERT on source vs SELECT on target (`clickhouse-access-control`).

## POPULATE / Refresh Notes

| Approach | Use when | Risk |
| --- | --- | --- |
| No POPULATE + INSERT SELECT batches | Large history | Operational effort |
| POPULATE | Small tables / labs | Long locks/load; race with live inserts |
| Refreshable MV (newer versions) | Periodic full refresh semantics | Version gate; different ops model |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Shape | MV TO AggregatingMergeTree target | Selecting * into MV storage ad hoc |
| Backfill | Batched INSERT SELECT | Blind POPULATE on multi-TB |
| Change | New MV + cutover | In-place ambiguous ALTER mid-stream |
| Verification | Window count reconcile | “Dashboard looks ok” |
| Emergency | Ticketed DETACH | Silent drop of target |

## Output Checklist

- [ ] Pipeline topology and SLOs documented
- [ ] Baseline storage and lag captured
- [ ] Target engine and ORDER/PARTITION justified
- [ ] MV created/changed without unplanned prod POPULATE
- [ ] Correctness reconcile for sample windows
- [ ] Alerts and rebuild runbook published
- [ ] Dual-write/cutover plan if replacing logic
- [ ] Access rights reviewed
- [ ] Residual lag/storage risks accepted

## Rules

- Authorized clusters only; treat DETACH/DROP as production incidents.
- Prefer reversible cutovers over in-place mystery rebuilds.
- Evidence via count/merge reconcile over intuition.
- Focus on **MV operations**; RBAC, dictionaries, RMT repair are separate skills.
