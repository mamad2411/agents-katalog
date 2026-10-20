---
name: clickhouse-patterns
description: "When to activate: ClickHouse, columnar, analytics, OLAP, MergeTree, materialized view, dictionaries, CHProxy"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# ClickHouse Patterns

## MergeTree Engines

```sql
-- ReplacingMergeTree — deduplicate on merge
CREATE TABLE events (
  event_date  Date,
  user_id     UInt64,
  event_type  String,
  properties  String,  -- JSON as string
  created_at  DateTime DEFAULT now(),
  version     UInt64   DEFAULT toUnixTimestamp(now())
) ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, user_id, event_type);

-- AggregatingMergeTree — pre-aggregate on merge
CREATE TABLE page_views_agg (
  date       Date,
  page       String,
  views      AggregateFunction(count),
  uniq_users AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree()
ORDER BY (date, page);

-- SummingMergeTree — sum numeric columns on merge
CREATE TABLE revenue_daily (
  date    Date,
  user_id UInt64,
  revenue Decimal(18, 2)
) ENGINE = SummingMergeTree(revenue)
ORDER BY (date, user_id);
```

## Materialized Views

```sql
-- Real-time aggregation pipeline
CREATE MATERIALIZED VIEW hourly_stats
ENGINE = SummingMergeTree()
ORDER BY (hour, page)
AS SELECT
  toStartOfHour(created_at) AS hour,
  page,
  count()       AS views,
  uniqExact(user_id) AS unique_users
FROM page_events
GROUP BY hour, page;

-- Populate from existing data
INSERT INTO hourly_stats
SELECT toStartOfHour(created_at) AS hour, page,
       count(), uniqExact(user_id)
FROM page_events GROUP BY hour, page;
```

## Dictionaries (Key-Value Lookup)

```sql
-- Flat dictionary from PostgreSQL
CREATE DICTIONARY user_dict (
  user_id UInt64,
  name    String,
  country String
)
PRIMARY KEY user_id
SOURCE(POSTGRESQL(
  host 'pg-host' port 5432 database 'app'
  table 'users' user 'clickhouse' password 'secret'
))
LIFETIME(MIN 300 MAX 600)
LAYOUT(FLAT());

-- Use in query
SELECT user_id, dictGet('user_dict', 'country', user_id) AS country
FROM events LIMIT 100;
```

## Query Patterns

```sql
-- Array functions
SELECT
  arrayFilter(x -> x > 0, [1, -2, 3]) AS positives,
  arrayMap(x -> x * 2, prices)         AS doubled,
  arraySum(prices)                      AS total,
  groupArray(price)                     AS all_prices
FROM orders;

-- Window functions
SELECT
  user_id,
  amount,
  sum(amount) OVER (PARTITION BY user_id ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running,
  row_number() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn
FROM orders;

-- SAMPLE — fast approximate queries
SELECT uniq(user_id) * 10 AS approx_users
FROM events SAMPLE 0.1;  -- 10% sample, scale up

-- JSON extraction
SELECT
  JSONExtractString(payload, 'action')     AS action,
  JSONExtractUInt(payload, 'duration_ms')  AS duration
FROM raw_events;
```

## Performance Tips

```sql
-- Check part sizes and merges
SELECT table, partition, rows, bytes_on_disk
FROM system.parts WHERE active ORDER BY bytes_on_disk DESC LIMIT 20;

-- Query log analysis
SELECT query, read_rows, memory_usage, query_duration_ms
FROM system.query_log
WHERE type = 'QueryFinish' AND query_duration_ms > 1000
ORDER BY query_duration_ms DESC LIMIT 10;

-- Force merge (after bulk insert)
OPTIMIZE TABLE events FINAL;
```

- Primary key = `ORDER BY` key — choose high-cardinality prefix wisely
- Partition by date, not by user_id — avoids too-many-parts
- Use `LowCardinality(String)` for columns with < 10k distinct values
- Batch inserts: minimum 1000 rows, ideally 100k–1M rows per insert
- Avoid `SELECT *` — ClickHouse reads only projected columns
