---
name: analyzing-alloydb
description: |
  Use when working with Alloydb — google AlloyDB instance analysis, query
  insights, columnar engine optimization, maintenance windows, and cluster
  health.
connection_type: gcp
preload: false
---

# AlloyDB Analysis Skill

Analyze and optimize AlloyDB clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated cluster/instance names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List AlloyDB clusters
gcloud alloydb clusters list --project="$GCP_PROJECT" --region="$REGION" --format=json

# 2. List instances in a cluster
gcloud alloydb instances list --cluster="$CLUSTER_NAME" --region="$REGION" --project="$GCP_PROJECT" --format=json

# 3. List databases
psql "$ALLOYDB_URI" -c "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;"

# 4. List tables (never assume names)
psql "$ALLOYDB_URI" -c "SELECT schemaname, tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema') ORDER BY schemaname, tablename;"

# 5. Describe table
psql "$ALLOYDB_URI" -c "\d my_schema.my_table"
```

**Phase 1 outputs:**
- AlloyDB clusters and instances
- Databases, schemas, and tables
- Table schemas with confirmed column names

### Phase 2: Analysis (only after Phase 1)

Only reference clusters, instances, databases, and tables confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core AlloyDB query runner — always use this
alloydb_query() {
    local query="$1"
    psql "${ALLOYDB_URI}" -t -A -F$'\t' -c "$query"
}

# gcloud AlloyDB helper
alloydb_cmd() {
    gcloud alloydb "$@" --project="${GCP_PROJECT}" --region="${REGION}" --format=json
}
```

## Anti-Hallucination Rules

- **NEVER reference a cluster or instance** without confirming via `gcloud alloydb clusters/instances list`
- **NEVER reference database/table names** without confirming via catalog queries
- **NEVER reference column names** without running `\d` or `information_schema` queries
- **NEVER assume columnar engine status** — always check configuration
- **NEVER guess maintenance window** — always query cluster settings

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, EXPLAIN, pg_catalog/information_schema queries, gcloud list/describe
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, gcloud alloydb instances delete without explicit user request
- **ALWAYS add `LIMIT`** to user table queries
- **Use `EXPLAIN ANALYZE`** carefully — it executes the query

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== AlloyDB Clusters ==="
alloydb_cmd clusters list | jq '.[] | {name: .name, state: .state, databaseVersion: .databaseVersion, network: .network}'

echo ""
echo "=== Instances ==="
alloydb_cmd instances list --cluster="$CLUSTER_NAME" | jq '.[] | {name: .name, instanceType: .instanceType, state: .state, machineConfig: .machineConfig, availabilityType: .availabilityType}'

echo ""
echo "=== Database Sizes ==="
alloydb_query "SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database WHERE datistemplate = false ORDER BY pg_database_size(datname) DESC;"

echo ""
echo "=== PostgreSQL Version ==="
alloydb_query "SELECT version();"
```

### Query Insights

```bash
#!/bin/bash
echo "=== Slow Queries (last 1h) ==="
alloydb_query "SELECT calls, ROUND(total_exec_time::numeric, 2) as total_ms, ROUND(mean_exec_time::numeric, 2) as mean_ms, rows, SUBSTRING(query, 1, 100) as query_preview FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;"

echo ""
echo "=== Active Queries ==="
alloydb_query "SELECT pid, state, EXTRACT(EPOCH FROM (now() - query_start))::int as runtime_sec, wait_event_type, wait_event, SUBSTRING(query, 1, 80) as query_preview FROM pg_stat_activity WHERE state = 'active' AND pid != pg_backend_pid() ORDER BY runtime_sec DESC;"

echo ""
echo "=== Table I/O Statistics ==="
alloydb_query "SELECT schemaname, relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 15;"
```

### Columnar Engine Analysis

```bash
#!/bin/bash
echo "=== Columnar Engine Status ==="
alloydb_query "SHOW google_columnar_engine.enabled;" 2>/dev/null || echo "Columnar engine setting not available"

echo ""
echo "=== Columnar Engine Tables ==="
alloydb_query "SELECT * FROM g_columnar_recommended_columns ORDER BY estimated_size_reduction DESC LIMIT 20;" 2>/dev/null || echo "Columnar recommendations not available"

echo ""
echo "=== Columnar Cache Usage ==="
alloydb_query "SELECT * FROM g_columnar_relations;" 2>/dev/null || echo "No columnar relations found"
```

### Maintenance & Backup Status

```bash
#!/bin/bash
echo "=== Maintenance Window ==="
alloydb_cmd clusters describe "$CLUSTER_NAME" | jq '.maintenanceUpdatePolicy'

echo ""
echo "=== Backups ==="
gcloud alloydb backups list --project="$GCP_PROJECT" --region="$REGION" --format=json | jq '.[] | {name: .name, state: .state, type: .type, createTime: .createTime, sizeBytes: .sizeBytes}'

echo ""
echo "=== Instance Metrics ==="
gcloud monitoring time-series list \
    --project="$GCP_PROJECT" \
    --filter='metric.type="alloydb.googleapis.com/database/cpu/utilization"' \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format="table(points.value)" 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Analyzing Alloydb Report
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

- **AlloyDB is PostgreSQL-compatible**: Most pg_* system views work, but some extensions differ
- **Columnar engine**: Auto-columnar may not cover all tables — check recommendations
- **Read pool routing**: Read replicas serve read traffic — ensure connection string targets the correct pool
- **IAM authentication**: AlloyDB supports IAM auth — check if password or IAM is configured
- **VPC-only**: AlloyDB instances are VPC-only — ensure network connectivity before debugging
- **pg_stat_statements**: Must be enabled in database flags — check before relying on query stats
