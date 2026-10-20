---
name: analyzing-mysql
description: |
  Use when working with Mysql — mySQL and MariaDB database analysis, performance
  tuning, query optimization, and health monitoring. Covers slow query
  investigation, index analysis, table statistics, replication health, InnoDB
  status, connection pool analysis, and schema inspection.
connection_type: mysql
preload: false
---

# MySQL Analysis Skill

Analyze and optimize MySQL/MariaDB databases using safe, read-only operations.

## MANDATORY: Two-Phase Execution

**Always discover schema before querying. Skipping Phase 1 causes hallucinated table/column names.**

### Phase 1: Discovery (ALWAYS first)

```bash
#!/bin/bash
# Run this FIRST — discover actual databases, tables, and columns

mysql_cmd() {
    mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" \
          --silent --skip-column-names "$@"
}

echo "=== Databases ==="
mysql_cmd -e "SHOW DATABASES;" | grep -v -E '^(information_schema|performance_schema|mysql|sys)$'

echo ""
echo "=== Tables in target DB (with row counts) ==="
mysql_cmd -e "
    SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH/1024/1024 AS data_mb,
           INDEX_LENGTH/1024/1024 AS index_mb, ENGINE
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    ORDER BY DATA_LENGTH DESC;" "$TARGET_DB" 2>/dev/null || \
mysql_cmd -e "SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'your_db' ORDER BY TABLE_ROWS DESC LIMIT 20;"

echo ""
echo "=== Columns (sample table) ==="
mysql_cmd -e "DESCRIBE your_table;" "$TARGET_DB"
```

### Phase 2: Analysis

Only reference tables and columns confirmed in Phase 1.

## Helper Function

```bash
#!/bin/bash

mysql_cmd() {
    mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" \
          --silent --skip-column-names -e "$1" "${2:-}"
}

# For multi-line queries from file
mysql_file() {
    mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" \
          --silent --skip-column-names "${1:-}" < "$2"
}
```

## Anti-Hallucination Rules

- **NEVER reference a table** without confirming it in `information_schema.TABLES`
- **NEVER reference a column** without confirming it in `information_schema.COLUMNS` or `DESCRIBE`
- **NEVER assume index names** — always `SHOW INDEX FROM table`
- **NEVER modify data** — only SELECT, SHOW, EXPLAIN, DESCRIBE, information_schema queries

## Safety Rules

- **READ-ONLY**: Only `SELECT`, `SHOW`, `EXPLAIN`, `DESCRIBE` — no DDL or DML
- **ALWAYS add `LIMIT`**: Default cap 1000 rows unless aggregating
- **Use `EXPLAIN`** before heavy queries on large tables
- **Avoid `SELECT *`** — always specify needed columns
- **Use `information_schema`** for metadata, not `SHOW` commands when possible (more portable)

## Common Operations

### Server Health Overview

```bash
#!/bin/bash
echo "=== MySQL Server Status ==="
{
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Uptime';" &
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Threads_connected';" &
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Questions';" &
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Slow_queries';" &
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read_requests';" &
    mysql_cmd "SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_reads';" &
}
wait

echo ""
echo "=== Buffer Pool Hit Rate ==="
mysql_cmd "
    SELECT 100 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests * 100) AS hit_rate_pct
    FROM (
        SELECT
            (SELECT variable_value FROM information_schema.GLOBAL_STATUS WHERE variable_name = 'Innodb_buffer_pool_reads') AS Innodb_buffer_pool_reads,
            (SELECT variable_value FROM information_schema.GLOBAL_STATUS WHERE variable_name = 'Innodb_buffer_pool_read_requests') AS Innodb_buffer_pool_read_requests
    ) t;"

echo ""
echo "=== Current Connections ==="
mysql_cmd "SHOW PROCESSLIST;" | awk '{print $5}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== MySQL Version & Config ==="
mysql_cmd "SELECT VERSION(), @@max_connections, @@innodb_buffer_pool_size/1024/1024 AS buffer_pool_mb, @@query_cache_size/1024/1024 AS qcache_mb;"
```

### Slow Query Analysis

```bash
#!/bin/bash
DB_NAME="${1:-}"

echo "=== Slow Query Log Status ==="
mysql_cmd "SHOW VARIABLES LIKE 'slow_query_log%';"
mysql_cmd "SHOW VARIABLES LIKE 'long_query_time';"

echo ""
echo "=== Top Slow Queries from Performance Schema ==="
mysql_cmd "
    SELECT
        DIGEST_TEXT,
        COUNT_STAR AS exec_count,
        ROUND(AVG_TIMER_WAIT/1e9, 2) AS avg_latency_ms,
        ROUND(MAX_TIMER_WAIT/1e9, 2) AS max_latency_ms,
        ROUND(SUM_ROWS_EXAMINED/COUNT_STAR) AS avg_rows_examined,
        ROUND(SUM_ROWS_SENT/COUNT_STAR) AS avg_rows_sent
    FROM performance_schema.events_statements_summary_by_digest
    WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
    ORDER BY AVG_TIMER_WAIT DESC
    LIMIT 15;" 2>/dev/null | head -20

echo ""
echo "=== Currently Running Long Queries (>5s) ==="
mysql_cmd "
    SELECT ID, USER, HOST, DB, COMMAND, TIME, LEFT(INFO, 100) AS query_preview
    FROM information_schema.PROCESSLIST
    WHERE COMMAND != 'Sleep' AND TIME > 5
    ORDER BY TIME DESC;"
```

### Index Analysis

```bash
#!/bin/bash
DB_NAME="${1:-}"

echo "=== Tables Without Primary Key ==="
mysql_cmd "
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM information_schema.TABLES t
    WHERE TABLE_TYPE = 'BASE TABLE'
      AND TABLE_SCHEMA NOT IN ('information_schema','performance_schema','mysql','sys')
      AND NOT EXISTS (
          SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
          WHERE TABLE_SCHEMA = t.TABLE_SCHEMA
            AND TABLE_NAME = t.TABLE_NAME
            AND CONSTRAINT_TYPE = 'PRIMARY KEY'
      )
    ${DB_NAME:+AND TABLE_SCHEMA = '$DB_NAME'}
    LIMIT 20;"

echo ""
echo "=== Duplicate Indexes ==="
mysql_cmd "
    SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA NOT IN ('information_schema','performance_schema','mysql','sys')
    ${DB_NAME:+AND TABLE_SCHEMA = '$DB_NAME'}
    ORDER BY TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX
    LIMIT 50;"

echo ""
echo "=== Index Usage (Performance Schema) ==="
mysql_cmd "
    SELECT OBJECT_SCHEMA, OBJECT_NAME, INDEX_NAME,
           COUNT_READ, COUNT_WRITE, COUNT_FETCH
    FROM performance_schema.table_io_waits_summary_by_index_usage
    WHERE OBJECT_SCHEMA NOT IN ('performance_schema','mysql','sys')
      AND INDEX_NAME IS NOT NULL
    ORDER BY COUNT_READ ASC
    LIMIT 20;" 2>/dev/null
```

### Table Statistics

```bash
#!/bin/bash
DB_NAME="${1:?Usage: $0 <database>}"

echo "=== Table Sizes in $DB_NAME ==="
mysql_cmd "
    SELECT
        TABLE_NAME,
        TABLE_ROWS,
        ROUND(DATA_LENGTH/1024/1024, 2) AS data_mb,
        ROUND(INDEX_LENGTH/1024/1024, 2) AS index_mb,
        ROUND((DATA_LENGTH+INDEX_LENGTH)/1024/1024, 2) AS total_mb,
        ENGINE,
        TABLE_COLLATION
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_TYPE = 'BASE TABLE'
    ORDER BY (DATA_LENGTH+INDEX_LENGTH) DESC
    LIMIT 25;"

echo ""
echo "=== Fragmented Tables (needs OPTIMIZE) ==="
mysql_cmd "
    SELECT TABLE_NAME,
           ROUND(DATA_FREE/1024/1024, 2) AS free_space_mb,
           ROUND(DATA_LENGTH/1024/1024, 2) AS data_mb,
           ROUND(DATA_FREE/DATA_LENGTH*100, 1) AS fragmentation_pct
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '$DB_NAME'
      AND DATA_FREE > 0
      AND DATA_LENGTH > 0
    ORDER BY DATA_FREE DESC
    LIMIT 15;"
```

### Replication Health

```bash
#!/bin/bash
echo "=== Replication Status ==="
mysql_cmd "SHOW SLAVE STATUS\G" 2>/dev/null || mysql_cmd "SHOW REPLICA STATUS\G" 2>/dev/null || echo "Not a replica"

echo ""
echo "=== Replication Lag ==="
mysql_cmd "SHOW SLAVE STATUS\G" 2>/dev/null | grep -E 'Seconds_Behind_Master|Slave_IO_Running|Slave_SQL_Running' || \
mysql_cmd "SHOW REPLICA STATUS\G" 2>/dev/null | grep -E 'Seconds_Behind_Source|Replica_IO_Running|Replica_SQL_Running'

echo ""
echo "=== Binary Log Status ==="
mysql_cmd "SHOW MASTER STATUS\G" 2>/dev/null || mysql_cmd "SHOW BINARY LOG STATUS\G" 2>/dev/null
mysql_cmd "SHOW BINARY LOGS;" 2>/dev/null | awk '{sum+=$2} END {print "Total binlog size:", sum/1024/1024, "MB"}'
```

### InnoDB Health

```bash
#!/bin/bash
echo "=== InnoDB Buffer Pool ==="
mysql_cmd "
    SELECT
        variable_name,
        ROUND(variable_value/1024/1024, 1) AS value_mb
    FROM information_schema.GLOBAL_STATUS
    WHERE variable_name IN (
        'Innodb_buffer_pool_bytes_data',
        'Innodb_buffer_pool_bytes_dirty',
        'Innodb_buffer_pool_pages_total',
        'Innodb_buffer_pool_pages_free'
    );"

echo ""
echo "=== InnoDB Lock Waits ==="
mysql_cmd "
    SELECT
        r.trx_id AS waiting_trx,
        r.trx_mysql_thread_id AS waiting_thread,
        LEFT(r.trx_query, 80) AS waiting_query,
        b.trx_id AS blocking_trx,
        b.trx_mysql_thread_id AS blocking_thread
    FROM information_schema.INNODB_LOCK_WAITS w
    JOIN information_schema.INNODB_TRX r ON r.trx_id = w.requesting_trx_id
    JOIN information_schema.INNODB_TRX b ON b.trx_id = w.blocking_trx_id
    LIMIT 10;" 2>/dev/null

echo ""
echo "=== Long Running Transactions ==="
mysql_cmd "
    SELECT trx_id, trx_started, trx_state,
           TIMESTAMPDIFF(SECOND, trx_started, NOW()) AS duration_sec,
           LEFT(trx_query, 80) AS query_preview
    FROM information_schema.INNODB_TRX
    WHERE TIMESTAMPDIFF(SECOND, trx_started, NOW()) > 30
    ORDER BY trx_started ASC
    LIMIT 10;"
```

### Query Explain

```bash
#!/bin/bash
DB_NAME="$1"
QUERY="$2"

echo "=== EXPLAIN for query ==="
mysql_cmd "EXPLAIN FORMAT=JSON $QUERY" "$DB_NAME" | jq '.query_block | {
    select_type: .select_type,
    table: .table.table_name,
    access_type: .table.access_type,
    key: .table.key,
    key_length: .table.key_length,
    rows: .table.rows_examined_per_scan,
    filtered: .table.filtered,
    extra: .table.attached_condition
}'

echo ""
echo "=== EXPLAIN ANALYZE (MySQL 8+) ==="
mysql_cmd "EXPLAIN ANALYZE $QUERY" "$DB_NAME" 2>/dev/null || echo "EXPLAIN ANALYZE requires MySQL 8.0+"
```

## Output Format

Present results as a structured report:
```
Analyzing Mysql Report
══════════════════════
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

- **`SHOW SLAVE STATUS` deprecated**: Use `SHOW REPLICA STATUS` in MySQL 8.0.22+ and MariaDB 10.5+
- **`information_schema.TABLES` row counts**: `TABLE_ROWS` is an estimate for InnoDB — use `COUNT(*)` for exact counts
- **Performance Schema disabled**: Some setups disable performance_schema — check with `SHOW VARIABLES LIKE 'performance_schema'`
- **`SELECT * FROM large_table`**: Always add `LIMIT` — NEVER run unbounded queries on tables with millions of rows
- **Character set issues**: If seeing `?` or garbled text, add `--default-character-set=utf8mb4` to connection
- **InnoDB vs MyISAM**: Lock behavior differs significantly — check ENGINE before recommending solutions
- **`ANALYZE TABLE` side effects**: This updates statistics but requires table lock on MyISAM — use cautiously
- **MySQL 5.7 vs 8.0 syntax**: Many performance_schema queries differ — always check version in Phase 1
