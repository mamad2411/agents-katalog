---
name: analyzing-snowflake
description: |
  Use when working with Snowflake — snowflake data warehouse analysis, query
  performance tuning, cost optimization, warehouse management, and schema
  inspection. Covers QUERY_HISTORY analysis, credit consumption, warehouse
  utilization, storage analysis, data sharing, and Time Travel. Read this skill
  before any Snowflake operations — it enforces two-phase execution,
  anti-hallucination rules, and read-only safety constraints.
connection_type: snowflake
preload: false
---

# Snowflake Analysis Skill

Analyze and optimize Snowflake data warehouse — cost, performance, and schema.

## MANDATORY: Two-Phase Execution

**Always discover databases, schemas, and tables before querying. Never assume object names.**

### Phase 1: Discovery

```bash
#!/bin/bash

snow_cmd() {
    snowsql -a "$SNOWFLAKE_ACCOUNT" \
            -u "$SNOWFLAKE_USER" \
            -p "$SNOWFLAKE_PASSWORD" \
            --warehouse "$SNOWFLAKE_WAREHOUSE" \
            -o output_format=tsv \
            -o header=false \
            -o timing=false \
            -q "$1" 2>/dev/null
}

echo "=== Databases ==="
snow_cmd "SHOW DATABASES;" | awk '{print $2, $4, $5}' | head -20

echo ""
echo "=== Warehouses ==="
snow_cmd "SHOW WAREHOUSES;" | awk '{print $1, $2, $6}' | head -10

echo ""
echo "=== Current Role & Context ==="
snow_cmd "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();"

echo ""
echo "=== Schemas in Target Database ==="
snow_cmd "SHOW SCHEMAS IN DATABASE ${SNOWFLAKE_DATABASE};" | awk '{print $2, $3}' | head -20
```

**After Phase 1:** Only reference databases, schemas, and warehouses confirmed above.

## Helper Function

```bash
#!/bin/bash

snow_query() {
    snowsql -a "$SNOWFLAKE_ACCOUNT" \
            -u "$SNOWFLAKE_USER" \
            -p "$SNOWFLAKE_PASSWORD" \
            --warehouse "${SNOWFLAKE_WAREHOUSE}" \
            --database "${SNOWFLAKE_DATABASE:-}" \
            --schema "${SNOWFLAKE_SCHEMA:-}" \
            -o output_format=tsv \
            -o header=false \
            -o timing=false \
            -q "$1" 2>/dev/null
}
```

## Anti-Hallucination Rules

- **NEVER reference a table** without first running `SHOW TABLES IN SCHEMA <schema>`
- **NEVER reference a column** without first running `DESCRIBE TABLE <table>`
- **NEVER assume warehouse names** — always list via `SHOW WAREHOUSES`
- **ALWAYS use `LIMIT`** on all `SELECT` queries — never unbounded scans on production tables
- **AVOID `SELECT *`** from large tables — always specify columns after inspecting schema

## Safety Rules

- **READ-ONLY by default**: SELECT, SHOW, DESCRIBE, INFORMATION_SCHEMA queries only
- **FORBIDDEN without explicit request**: INSERT, UPDATE, DELETE, DROP, TRUNCATE, CREATE
- **ALWAYS add `LIMIT`** — default cap 1000 rows for data queries
- **Use `INFORMATION_SCHEMA`** for metadata queries over `SHOW` where possible (SQL-standard)
- **Warehouse suspension**: Never suspend/resize warehouses without explicit user request

## Common Operations

### Cost & Credit Analysis

```bash
#!/bin/bash
echo "=== Credit Consumption Last 30 Days ==="
snow_query "
    SELECT
        DATE_TRUNC('day', START_TIME) AS day,
        WAREHOUSE_NAME,
        ROUND(SUM(CREDITS_USED), 2) AS credits,
        COUNT(*) AS query_count
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    GROUP BY 1, 2
    ORDER BY 1 DESC, 3 DESC
    LIMIT 60;" | column -t

echo ""
echo "=== Top Warehouses by Cost (30 days) ==="
snow_query "
    SELECT
        WAREHOUSE_NAME,
        ROUND(SUM(CREDITS_USED), 2) AS total_credits,
        ROUND(SUM(CREDITS_USED_COMPUTE), 2) AS compute_credits,
        ROUND(SUM(CREDITS_USED_CLOUD_SERVICES), 2) AS cloud_service_credits,
        COUNT(*) AS sessions
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10;" | column -t

echo ""
echo "=== Storage Costs ==="
snow_query "
    SELECT
        DATE_TRUNC('month', USAGE_DATE) AS month,
        ROUND(AVG(STORAGE_BYTES)/POWER(1024,3), 2) AS avg_storage_tb,
        ROUND(AVG(STAGE_BYTES)/POWER(1024,3), 2) AS avg_stage_tb,
        ROUND(AVG(FAILSAFE_BYTES)/POWER(1024,3), 2) AS avg_failsafe_tb
    FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE
    WHERE USAGE_DATE >= DATEADD('month', -3, CURRENT_DATE())
    GROUP BY 1
    ORDER BY 1 DESC;" | column -t
```

### Query Performance Analysis

```bash
#!/bin/bash
echo "=== Slowest Queries (last 24h) ==="
snow_query "
    SELECT
        QUERY_ID,
        QUERY_TYPE,
        WAREHOUSE_NAME,
        USER_NAME,
        ROUND(TOTAL_ELAPSED_TIME/1000, 1) AS elapsed_sec,
        ROUND(BYTES_SCANNED/POWER(1024,3), 2) AS scanned_gb,
        ROUND(CREDITS_USED_CLOUD_SERVICES, 4) AS credits,
        LEFT(QUERY_TEXT, 80) AS query_preview
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE START_TIME >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
      AND EXECUTION_STATUS = 'SUCCESS'
    ORDER BY TOTAL_ELAPSED_TIME DESC
    LIMIT 15;" | column -t

echo ""
echo "=== Queries with Full Table Scans ==="
snow_query "
    SELECT
        USER_NAME,
        WAREHOUSE_NAME,
        ROUND(PARTITIONS_SCANNED/NULLIF(PARTITIONS_TOTAL,0)*100, 1) AS pct_partitions_scanned,
        ROUND(BYTES_SCANNED/POWER(1024,3), 2) AS scanned_gb,
        ROUND(TOTAL_ELAPSED_TIME/1000, 1) AS elapsed_sec,
        LEFT(QUERY_TEXT, 80) AS query_preview
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE START_TIME >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
      AND PARTITIONS_TOTAL > 10
      AND PARTITIONS_SCANNED/NULLIF(PARTITIONS_TOTAL,0) > 0.9
    ORDER BY BYTES_SCANNED DESC
    LIMIT 10;" | column -t

echo ""
echo "=== Failed Queries (last 24h) ==="
snow_query "
    SELECT
        ERROR_CODE,
        ERROR_MESSAGE,
        COUNT(*) AS count,
        USER_NAME,
        WAREHOUSE_NAME
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE START_TIME >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
      AND EXECUTION_STATUS = 'FAIL'
    GROUP BY 1, 2, 4, 5
    ORDER BY 3 DESC
    LIMIT 10;" | column -t
```

### Warehouse Utilization

```bash
#!/bin/bash
echo "=== Warehouse Utilization ==="
snow_query "
    SELECT
        WAREHOUSE_NAME,
        COUNT(*) AS total_queries,
        ROUND(AVG(TOTAL_ELAPSED_TIME/1000), 1) AS avg_elapsed_sec,
        ROUND(AVG(QUEUED_OVERLOAD_TIME/1000), 1) AS avg_queue_sec,
        MAX(QUEUED_OVERLOAD_TIME/1000) AS max_queue_sec,
        ROUND(SUM(BYTES_SCANNED)/POWER(1024,4), 2) AS total_tb_scanned
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10;" | column -t

echo ""
echo "=== Warehouse Auto-Suspend Opportunities ==="
snow_query "
    SELECT
        WAREHOUSE_NAME,
        ROUND(SUM(CREDITS_USED), 2) AS credits_used,
        COUNT(DISTINCT DATE_TRUNC('hour', START_TIME)) AS active_hours,
        ROUND(SUM(CREDITS_USED)/NULLIF(COUNT(DISTINCT DATE_TRUNC('hour', START_TIME)), 0), 2) AS credits_per_hour
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    GROUP BY 1
    HAVING credits_per_hour < 0.1  -- Barely used warehouses
    ORDER BY 2 DESC;" | column -t
```

### Schema Analysis

```bash
#!/bin/bash
DB="${1:-$SNOWFLAKE_DATABASE}"
SCHEMA="${2:-PUBLIC}"

echo "=== Tables in $DB.$SCHEMA ==="
snow_query "
    SELECT
        TABLE_NAME,
        ROW_COUNT,
        ROUND(BYTES/POWER(1024,3), 3) AS data_gb,
        CLUSTERING_KEY,
        IS_TRANSIENT
    FROM ${DB}.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = '${SCHEMA}'
      AND TABLE_TYPE = 'BASE TABLE'
    ORDER BY BYTES DESC NULLS LAST
    LIMIT 25;" | column -t

echo ""
echo "=== Tables Missing Clustering Keys (large tables) ==="
snow_query "
    SELECT TABLE_NAME, ROW_COUNT, ROUND(BYTES/POWER(1024,3), 2) AS data_gb
    FROM ${DB}.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = '${SCHEMA}'
      AND CLUSTERING_KEY IS NULL
      AND BYTES > 10*POWER(1024,3)  -- > 10GB
    ORDER BY BYTES DESC
    LIMIT 10;" | column -t
```

### Data Freshness / Time Travel

```bash
#!/bin/bash
DB="${1:-$SNOWFLAKE_DATABASE}"
TABLE="${2:?Table name required}"
SCHEMA="${3:-PUBLIC}"

echo "=== Table: $DB.$SCHEMA.$TABLE ==="
snow_query "DESCRIBE TABLE ${DB}.${SCHEMA}.${TABLE};" | head -20

echo ""
echo "=== Row Count ==="
snow_query "SELECT COUNT(*) FROM ${DB}.${SCHEMA}.${TABLE};"

echo ""
echo "=== Recent Changes (Time Travel — if enabled) ==="
snow_query "
    SELECT
        QUERY_ID,
        QUERY_TYPE,
        ROUND(ROWS_PRODUCED, 0) AS rows_affected,
        START_TIME
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE QUERY_TEXT ILIKE '%${TABLE}%'
      AND QUERY_TYPE IN ('INSERT', 'UPDATE', 'DELETE', 'MERGE', 'COPY')
      AND START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
    ORDER BY START_TIME DESC
    LIMIT 10;" | column -t
```

### User Activity Audit

```bash
#!/bin/bash
echo "=== Top Users by Query Count (30 days) ==="
snow_query "
    SELECT
        USER_NAME,
        COUNT(*) AS query_count,
        ROUND(SUM(TOTAL_ELAPSED_TIME/1000/3600), 1) AS total_hours,
        ROUND(SUM(BYTES_SCANNED)/POWER(1024,4), 2) AS total_tb_scanned
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10;" | column -t

echo ""
echo "=== Login History (failed logins) ==="
snow_query "
    SELECT
        USER_NAME,
        CLIENT_IP,
        FIRST_AUTHENTICATION_FACTOR,
        ERROR_MESSAGE,
        EVENT_TIMESTAMP
    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
    WHERE IS_SUCCESS = 'NO'
      AND EVENT_TIMESTAMP >= DATEADD('day', -7, CURRENT_TIMESTAMP())
    ORDER BY EVENT_TIMESTAMP DESC
    LIMIT 15;" | column -t
```

## Output Format

Present results as a structured report:
```
Analyzing Snowflake Report
══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **`ACCOUNT_USAGE` latency**: Data in `ACCOUNT_USAGE` views has a 45-minute to 3-hour delay — for real-time use `INFORMATION_SCHEMA` (14-day retention, no delay)
- **Credit vs dollar cost**: Credits vary by cloud/region pricing — multiply by rate for dollar estimate; never assume $3/credit
- **`PARTITIONS_SCANNED` null**: Can be null for metadata-only queries — use `NULLIF()` in calculations
- **Case sensitivity**: Snowflake objects default to UPPERCASE when unquoted — `"MyTable"` vs `MYTABLE` are different
- **`SHOW` output format**: `SHOW` commands output varies by client — prefer `INFORMATION_SCHEMA` for programmatic use
- **Warehouse auto-resume**: Warehouses auto-resume on query — don't assume current `SHOW WAREHOUSES` status reflects recent queries
- **Clustering depth**: Poor clustering causes high `PARTITIONS_SCANNED/PARTITIONS_TOTAL` ratio — key signal for missing clustering keys
- **Time Travel period**: Default 1 day, Enterprise 90 days — always check `DATA_RETENTION_TIME_IN_DAYS` before querying historical data
- **Cloud Services credits**: If >10% of credits come from cloud services, there may be small query storms — check `QUERY_HISTORY` for high-frequency tiny queries
