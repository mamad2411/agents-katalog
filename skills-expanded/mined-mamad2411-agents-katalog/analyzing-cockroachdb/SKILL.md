---
name: analyzing-cockroachdb
description: |
  Use when working with Cockroachdb — cockroachDB cluster health, range
  distribution, SQL statistics, schema change monitoring, and query
  optimization.
connection_type: cockroachdb
preload: false
---

# CockroachDB Analysis Skill

Analyze and optimize CockroachDB clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Cluster overview
cockroach node status --certs-dir="$CERTS_DIR" --host="$CRDB_HOST"

# 2. List databases
cockroach sql --certs-dir="$CERTS_DIR" --host="$CRDB_HOST" -e "SHOW DATABASES;"

# 3. List tables in a database
cockroach sql --certs-dir="$CERTS_DIR" --host="$CRDB_HOST" -e "SHOW TABLES FROM mydb;"

# 4. Get table schema
cockroach sql --certs-dir="$CERTS_DIR" --host="$CRDB_HOST" -e "SHOW CREATE TABLE mydb.mytable;"

# 5. Check column names
cockroach sql --certs-dir="$CERTS_DIR" --host="$CRDB_HOST" -e "SHOW COLUMNS FROM mydb.mytable;"
```

**Phase 1 outputs:**
- Cluster topology and node liveness
- List of databases and tables
- Table schemas with confirmed column names

### Phase 2: Analysis (only after Phase 1)

Only reference databases, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core SQL runner — always use this
crdb_sql() {
    local query="$1"
    cockroach sql --certs-dir="${CERTS_DIR:-certs}" --host="${CRDB_HOST:-localhost}" \
        --format=tsv -e "$query" 2>/dev/null
}

# Admin UI API helper (if available)
crdb_api() {
    local endpoint="$1"
    curl -sk "https://${CRDB_HOST:-localhost}:8080/_admin/v1/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database or table** without confirming via `SHOW DATABASES` / `SHOW TABLES`
- **NEVER reference column names** without seeing them in `SHOW COLUMNS` or `SHOW CREATE TABLE`
- **NEVER assume node IDs** — always get them from `node status`
- **NEVER guess range counts** — always query `crdb_internal.ranges`
- **NEVER assume cluster version** — check with `SHOW CLUSTER SETTING version`

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, EXPLAIN, system catalog queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, SET CLUSTER SETTING without explicit user request
- **ALWAYS add `LIMIT`** to queries on user tables
- **Use `EXPLAIN ANALYZE`** carefully — it executes the query
- **Prefer `EXPLAIN`** (no ANALYZE) for plan inspection without execution

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Node Status ==="
crdb_sql "SELECT node_id, address, is_live, ranges, locality FROM crdb_internal.gossip_nodes ORDER BY node_id;"

echo ""
echo "=== Store Status ==="
crdb_sql "SELECT node_id, store_id, used, available, range_count FROM crdb_internal.kv_store_status ORDER BY node_id;"

echo ""
echo "=== Cluster Settings (non-default) ==="
crdb_sql "SHOW ALL CLUSTER SETTINGS;" | grep -v "default"

echo ""
echo "=== Version ==="
crdb_sql "SELECT version, crdb_internal.node_id() as node_id;"
```

### Range Distribution Analysis

```bash
#!/bin/bash
echo "=== Range Distribution per Node ==="
crdb_sql "SELECT lease_holder, count(*) as range_count FROM crdb_internal.ranges GROUP BY lease_holder ORDER BY lease_holder;"

echo ""
echo "=== Hot Ranges (top 10 by QPS) ==="
crdb_sql "SELECT range_id, table_name, start_pretty, lease_holder, queries_per_second FROM crdb_internal.ranges ORDER BY queries_per_second DESC LIMIT 10;"

echo ""
echo "=== Under-replicated Ranges ==="
crdb_sql "SELECT range_id, table_name, replicas, learner_replicas FROM crdb_internal.ranges WHERE array_length(replicas, 1) < 3;"
```

### SQL Statistics Analysis

```bash
#!/bin/bash
echo "=== Top Slow Queries (by mean latency) ==="
crdb_sql "SELECT substring(metadata->>'query', 1, 80) as query, statistics->'execution_statistics'->>'cnt' as exec_count, statistics->'execution_statistics'->>'meanRunLatency' as mean_lat FROM crdb_internal.statement_statistics ORDER BY (statistics->'execution_statistics'->>'meanRunLatency')::float DESC LIMIT 15;"

echo ""
echo "=== Schema Changes in Progress ==="
crdb_sql "SELECT job_id, description, status, running_status, fraction_completed FROM crdb_internal.jobs WHERE job_type = 'SCHEMA CHANGE' AND status IN ('running', 'paused', 'pending') ORDER BY created DESC LIMIT 10;"
```

### Table Analysis

```bash
#!/bin/bash
DB_NAME="${1:-defaultdb}"
TABLE="${2:-mytable}"

echo "=== Table Stats ==="
crdb_sql "SHOW STATISTICS FOR TABLE $DB_NAME.$TABLE;"

echo ""
echo "=== Index Usage ==="
crdb_sql "SELECT * FROM crdb_internal.index_usage_statistics WHERE table_id = (SELECT id FROM crdb_internal.tables WHERE name = '$TABLE' AND database_name = '$DB_NAME');"

echo ""
echo "=== Table Ranges ==="
crdb_sql "SELECT count(*) as range_count, sum(range_size_mb) as total_mb FROM crdb_internal.ranges WHERE table_name = '$TABLE';"
```

## Output Format

Present results as a structured report:
```
Analyzing Cockroachdb Report
════════════════════════════
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

- **Multi-region latency**: Cross-region queries have higher latency — check locality settings
- **Contention on hot keys**: Sequential key generation causes range hotspots — use UUID or hash-sharded indexes
- **Schema change locks**: Long-running schema changes can block writes — check job status
- **Range splits**: Tables with rapid growth may need manual pre-splitting
- **Transaction retries**: CockroachDB uses serializable isolation — application must handle retry errors (40001)
- **Clock skew**: Node clock skew > 500ms causes errors — check node status for clock offset
