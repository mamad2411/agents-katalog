---
name: analyzing-mariadb
description: |
  Use when working with Mariadb — mariaDB Galera cluster status, MaxScale
  routing, ColumnStore engine analysis, performance schema tuning, and
  replication health.
connection_type: mariadb
preload: false
---

# MariaDB Analysis Skill

Analyze and optimize MariaDB clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. MariaDB version
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "SELECT VERSION();"

# 2. List databases
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "SHOW DATABASES;"

# 3. List tables
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "SHOW TABLES FROM my_database;"

# 4. Describe table (never assume column names)
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "DESCRIBE my_database.my_table;"

# 5. Check for Galera
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "SHOW STATUS LIKE 'wsrep_%';" 2>/dev/null

# 6. Check for ColumnStore
mariadb -h "$MDB_HOST" -u "$MDB_USER" -p"$MDB_PASSWORD" -e "SELECT ENGINE FROM information_schema.ENGINES WHERE ENGINE = 'Columnstore';" 2>/dev/null
```

**Phase 1 outputs:**
- MariaDB version and engine capabilities
- Databases and tables
- Cluster type (standalone, Galera, replication)

### Phase 2: Analysis (only after Phase 1)

Only reference databases, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core MariaDB query runner — always use this
mdb_query() {
    local query="$1"
    mariadb -h "${MDB_HOST:-localhost}" -P "${MDB_PORT:-3306}" \
        -u "${MDB_USER:-root}" -p"${MDB_PASSWORD}" \
        -N -B -e "$query"
}

# MaxScale API helper (if MaxScale is in use)
maxscale_api() {
    local endpoint="$1"
    curl -s -u "${MAXSCALE_USER:-admin}:${MAXSCALE_PASSWORD:-mariadb}" \
        "http://${MAXSCALE_HOST:-localhost}:8989/v1/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database or table** without confirming via SHOW commands
- **NEVER reference column names** without running DESCRIBE
- **NEVER assume Galera cluster** — always check wsrep status first
- **NEVER assume MaxScale is present** — check separately
- **NEVER assume ColumnStore engine** — verify via ENGINES table

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, EXPLAIN, information_schema/performance_schema queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, SET GLOBAL without explicit user request
- **ALWAYS add `LIMIT`** to user table queries
- **Use `EXPLAIN`** before running expensive queries
- **Never modify Galera cluster state** without explicit user request

## Common Operations

### Galera Cluster Status

```bash
#!/bin/bash
echo "=== Galera Cluster Overview ==="
mdb_query "SHOW STATUS LIKE 'wsrep_cluster_size';"
mdb_query "SHOW STATUS LIKE 'wsrep_cluster_status';"
mdb_query "SHOW STATUS LIKE 'wsrep_local_state_comment';"
mdb_query "SHOW STATUS LIKE 'wsrep_ready';"
mdb_query "SHOW STATUS LIKE 'wsrep_connected';"

echo ""
echo "=== Node Status ==="
mdb_query "SHOW STATUS WHERE Variable_name IN ('wsrep_local_recv_queue_avg', 'wsrep_local_send_queue_avg', 'wsrep_flow_control_paused', 'wsrep_cert_deps_distance', 'wsrep_last_committed');"

echo ""
echo "=== Replication Health ==="
mdb_query "SHOW STATUS WHERE Variable_name LIKE 'wsrep_local%' OR Variable_name LIKE 'wsrep_received%';"
```

### MaxScale Routing Analysis

```bash
#!/bin/bash
echo "=== MaxScale Servers ==="
maxscale_api "servers" | jq '.data[] | {id, attributes: {state: .attributes.state, address: .attributes.parameters.address, port: .attributes.parameters.port}}'

echo ""
echo "=== MaxScale Services ==="
maxscale_api "services" | jq '.data[] | {id, attributes: {router: .attributes.router, state: .attributes.state, connections: .attributes.connections}}'

echo ""
echo "=== MaxScale Monitors ==="
maxscale_api "monitors" | jq '.data[] | {id, attributes: {module: .attributes.module, state: .attributes.state}}'
```

### Performance Schema Analysis

```bash
#!/bin/bash
echo "=== Slow Queries ==="
mdb_query "SELECT DIGEST_TEXT, COUNT_STAR, ROUND(AVG_TIMER_WAIT/1000000000, 2) as avg_ms, SUM_ROWS_EXAMINED, SUM_ROWS_SENT FROM performance_schema.events_statements_summary_by_digest ORDER BY AVG_TIMER_WAIT DESC LIMIT 15;"

echo ""
echo "=== Table I/O ==="
mdb_query "SELECT OBJECT_SCHEMA, OBJECT_NAME, COUNT_READ, COUNT_WRITE, SUM_TIMER_READ/1000000000 as read_ms, SUM_TIMER_WRITE/1000000000 as write_ms FROM performance_schema.table_io_waits_summary_by_table WHERE OBJECT_SCHEMA NOT IN ('mysql', 'performance_schema', 'information_schema') ORDER BY SUM_TIMER_WAIT DESC LIMIT 15;"

echo ""
echo "=== InnoDB Status ==="
mdb_query "SHOW ENGINE INNODB STATUS\G" | head -50
```

### ColumnStore Analysis

```bash
#!/bin/bash
echo "=== ColumnStore Tables ==="
mdb_query "SELECT TABLE_SCHEMA, TABLE_NAME, ENGINE, TABLE_ROWS, ROUND(DATA_LENGTH/1024/1024, 2) as data_mb FROM information_schema.tables WHERE ENGINE = 'Columnstore' ORDER BY DATA_LENGTH DESC;"

echo ""
echo "=== ColumnStore System Info ==="
mdb_query "SELECT * FROM columnstore_info.system_status;" 2>/dev/null || echo "ColumnStore not available"

echo ""
echo "=== ColumnStore Extents ==="
mdb_query "SELECT * FROM columnstore_info.extent_map LIMIT 20;" 2>/dev/null || echo "ColumnStore not available"
```

## Output Format

Present results as a structured report:
```
Analyzing Mariadb Report
════════════════════════
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

- **Galera SST blocking**: State Snapshot Transfer blocks the donor node — monitor `wsrep_local_state_comment`
- **Flow control**: Galera flow control pauses writes when a node falls behind — check `wsrep_flow_control_paused`
- **Multi-master conflicts**: Galera rejects conflicting writes — monitor certification failures
- **MaxScale failover**: MaxScale automatic failover can cause brief connection drops
- **ColumnStore vs InnoDB**: ColumnStore is for analytics, InnoDB for OLTP — do not mix workload types
- **GTID replication**: Galera uses its own GTID — do not confuse with MariaDB GTID replication
