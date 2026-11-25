---
name: clickhouse-dictionaries
description: >
  Design and operate ClickHouse dictionaries: sources (HTTP, MySQL, CH, file), layouts
  (hashed, complex_key_hashed, range_hashed, cache, direct), lifetime/invalidate,
  dictGet performance, and failure modes. Use on owned ClickHouse for dimension
  lookups and enrichment — not as a replacement for JOINs on huge fact-fact relations
  or for access-control design (see clickhouse-access-control).
---

# ClickHouse Dictionaries

## Scope And Authorization

- **In scope:** owned ClickHouse and authorized dimension sources (DB/HTTP/files).
- **Out of scope:** pulling third-party data without license/authorization; using dict credentials to pivot networks.
- Prefer staging for new external sources; external DB credentials in vault.
- Redact connection strings and API tokens from dictionary DDL in tickets.
- Pair with `clickhouse-access-control` for who may CREATE DICTIONARY.

## When To Use

- Enrichment lookups (`dictGet`) for dimensions (user→plan, id→geo) at query time.
- Caching external reference data with controlled refresh (`LIFETIME`).
- Replacing repeated JOINs to small/medium dimension tables.
- Tokens: CREATE DICTIONARY, dictGet, LAYOUT, SOURCE, LIFETIME, invalidate_query, hierarchical.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Users/roles/grants | `clickhouse-access-control` |
| Materialized views | `clickhouse-materialized-views-ops` |
| Replication / RMT | `clickhouse-replicated-merge-tree` |
| General SQL modeling only | analytics modeling practice |
| Secrets storage | `secrets-management-hygiene` |

## Layout Cheat Sheet

| Layout | Best for | Caveats |
| --- | --- | --- |
| `FLAT` | Small dense integer keys | Memory; key range |
| `HASHED` | Many keys, single key | Memory ≈ cardinality |
| `COMPLEX_KEY_HASHED` | Composite keys | Same memory concerns |
| `RANGE_HASHED` | Key + date ranges | Overlapping range rules |
| `CACHE` | Large dims, subset hot | Miss latency; set size |
| `DIRECT` | Always hit source | Source must be fast; no local cache |
| `IP_TRIE` | IP → attribute | IP data quality |

## Workflow

### 1. Confirm scope and success criteria

1. Dictionary purpose, key(s), attributes, max cardinality, freshness SLO, source owner.
2. Success: dictGet hit latency OK; refresh succeeds; source outage behavior documented (exception vs default).
3. Rollback: DROP/REPLACE dictionary; feature flag queries to JOIN fallback if needed.

### 2. Inventory existing dictionaries

```sql
SELECT name, status, origin, type, key.names, attribute.names, bytes_allocated, element_count, load_factor
FROM system.dictionaries;

SHOW CREATE DICTIONARY db.dim_users;
```

1. Note failing statuses (`FAILED`, `NOT_LOADED`).
2. Map credentials used by HTTP/MySQL sources.

### 3. Choose source + layout

| Source | When |
| --- | --- |
| ClickHouse | Same cluster dimension table |
| MySQL/Postgres | Operational DB system of record |
| HTTP | Internal API with bulk export |
| File / S3 | Periodic dumps |
| Cassandra/Mongo | Less common; check version support |

1. Estimate memory: `cardinality * (key + attrs + overhead)`.
2. Prefer **CACHE/DIRECT** if full hashed set does not fit RAM.
3. Define **LIFETIME** min/max or `invalidate_query` for controlled reload.

### 4. Create and load

```sql
CREATE DICTIONARY IF NOT EXISTS analytics.dim_user_plan
(
    user_id UInt64,
    plan String,
    tier UInt8
)
PRIMARY KEY user_id
SOURCE(CLICKHOUSE(
    HOST 'localhost' PORT 9000
    USER 'dict_reader' PASSWORD '[REDACTED]'
    DB 'analytics' TABLE 'user_plan_src'
))
LAYOUT(HASHED())
LIFETIME(MIN 300 MAX 600);
```

**HTTP source sketch:**

```sql
SOURCE(HTTP(
    URL 'https://dims.internal.example/user_plan.tsv'
    FORMAT 'TabSeparated'
    CREDENTIALS(USER 'dict' PASSWORD '[REDACTED]')
))
```

**invalidate_query pattern:**

```sql
SOURCE(CLICKHOUSE(
    ...
    INVALIDATE_QUERY 'SELECT max(updated_at) FROM analytics.user_plan_src'
))
LIFETIME(MIN 0 MAX 300)
```

1. Use least-privilege **dict_reader** account (SELECT only on source).
2. Prefer secure private network to sources; TLS where supported.
3. Attributes: set explicit types; avoid huge String blobs in hot dicts.

### 5. Query patterns and verify

```sql
SELECT
  e.user_id,
  dictGet('analytics.dim_user_plan', 'plan', e.user_id) AS plan
FROM analytics.events AS e
LIMIT 10;

-- defaults / missing keys
SELECT dictGetOrDefault('analytics.dim_user_plan', 'plan', toUInt64(0), 'unknown');

SYSTEM RELOAD DICTIONARY analytics.dim_user_plan;
SELECT name, status, last_successful_update_time, loading_duration
FROM system.dictionaries
WHERE name = 'dim_user_plan';
```

1. Compare dictGet vs JOIN for correctness on sample keys.
2. Fault inject: block source → observe status and query errors; decide `dictGetOrDefault` policy.
3. Load test: QPS with cache layout vs hashed.

### 6. Operate

1. Alert on dictionary `FAILED` / long `loading_duration` / memory growth.
2. Stagger LIFETIME across many dicts to avoid thundering reloads.
3. Document key type mismatches (UInt64 vs String) — common silent miss cause.
4. Hierarchical dictionaries only when parent/child dims are real requirements.

### 7. Hand off

1. Catalog: dict name, source, owner, freshness, memory budget.
2. Runbook: RELOAD, fallback JOIN, rotate source credentials.
3. Grants: who can CREATE DICTIONARY / dictGet across DBs (`clickhouse-access-control`).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Fit | Dimension enrichment | Multi-GB fact lookup every row without cache plan |
| Credentials | Vault + SELECT-only | Superuser password in DDL in git |
| Missing keys | OrDefault + metrics | Assume 100% hit |
| Refresh | invalidate_query / bounded LIFETIME | Never reload stale dims |
| Layout | Sized for RAM | HASHED OOM on huge keyspace |

## Output Checklist

- [ ] Purpose, keys, cardinality, freshness SLO recorded
- [ ] Source and layout chosen with memory estimate
- [ ] Least-privilege source credentials
- [ ] Dictionary created; status LOADED
- [ ] Correctness vs JOIN sample validated
- [ ] Outage behavior tested (default vs exception)
- [ ] RELOAD/ops alerts documented
- [ ] Owners and grants documented
- [ ] Residual staleness risk accepted explicitly

## Rules

- Owned data sources only; respect license and PII boundaries.
- Prefer reversible CREATE OR REPLACE with known-good previous DDL.
- Do not store live passwords in skill notes or git.
- Focus on **dictionaries**; RBAC, MVs, and replication are sibling skills.
