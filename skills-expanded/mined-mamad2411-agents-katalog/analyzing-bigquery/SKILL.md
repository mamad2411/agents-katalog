---
name: analyzing-bigquery
description: |
  Use when working with Bigquery — google BigQuery job analysis, slot
  utilization, cost analysis, dataset management, and query optimization.
connection_type: gcp
preload: false
---

# BigQuery Analysis Skill

Analyze and optimize BigQuery with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated dataset/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List datasets
bq ls --project_id="$GCP_PROJECT" --format=json

# 2. List tables in a dataset
bq ls --project_id="$GCP_PROJECT" "$DATASET" --format=json

# 3. Get table schema (never assume column names)
bq show --schema --format=json "$GCP_PROJECT:$DATASET.$TABLE"

# 4. Table details
bq show --format=json "$GCP_PROJECT:$DATASET.$TABLE"

# 5. Sample data
bq query --use_legacy_sql=false --max_rows=5 "SELECT * FROM \`$GCP_PROJECT.$DATASET.$TABLE\` LIMIT 5"
```

**Phase 1 outputs:**
- Datasets and tables in the project
- Table schemas with column names and types
- Table metadata (size, row count, partitioning)

### Phase 2: Analysis (only after Phase 1)

Only reference datasets, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core BigQuery runner — always use this
bq_query() {
    local query="$1"
    bq query --use_legacy_sql=false --format=json --max_rows="${2:-100}" "$query"
}

# Dry run for cost estimation
bq_dryrun() {
    local query="$1"
    bq query --use_legacy_sql=false --dry_run "$query" 2>&1
}
```

## Anti-Hallucination Rules

- **NEVER reference a dataset or table** without confirming via `bq ls`
- **NEVER reference column names** without seeing them in `bq show --schema`
- **NEVER assume partitioning scheme** — check table metadata
- **NEVER guess project IDs** — always confirm with `gcloud config get project`
- **ALWAYS dry-run expensive queries** to check cost before execution

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, bq show, bq ls, INFORMATION_SCHEMA queries
- **FORBIDDEN**: INSERT, UPDATE, DELETE, DROP, CREATE TABLE, bq rm without explicit user request
- **ALWAYS dry-run first** for queries scanning more than 1GB
- **ALWAYS add `LIMIT`** to exploration queries
- **Use `--max_rows`** to limit bq output
- **Prefer partitioned/clustered scans** — filter on partition column to reduce cost

## Common Operations

### Dataset & Table Overview

```bash
#!/bin/bash
echo "=== Datasets ==="
bq ls --project_id="$GCP_PROJECT" --format=json | jq '.[] | {datasetId: .datasetReference.datasetId, location}'

echo ""
echo "=== Largest Tables ==="
bq_query "SELECT table_schema, table_name, ROUND(size_bytes/1024/1024/1024, 2) as size_gb, row_count, TIMESTAMP_MILLIS(creation_time) as created, TIMESTAMP_MILLIS(last_modified_time) as modified FROM \`$GCP_PROJECT\`.INFORMATION_SCHEMA.TABLE_STORAGE ORDER BY size_bytes DESC LIMIT 20"

echo ""
echo "=== Partitioned Tables ==="
bq_query "SELECT table_catalog, table_schema, table_name, partition_type, partition_expiration_ms FROM \`$GCP_PROJECT\`.INFORMATION_SCHEMA.TABLE_OPTIONS t JOIN \`$GCP_PROJECT\`.INFORMATION_SCHEMA.PARTITIONED_TABLES p USING (table_catalog, table_schema, table_name) LIMIT 20" 2>/dev/null
```

### Job & Cost Analysis

```bash
#!/bin/bash
echo "=== Recent Jobs (last 24h) ==="
bq_query "SELECT job_id, user_email, statement_type, total_bytes_processed, total_slot_ms, creation_time, state FROM \`region-us\`.INFORMATION_SCHEMA.JOBS_BY_PROJECT WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR) ORDER BY total_bytes_processed DESC LIMIT 20"

echo ""
echo "=== Cost by User (last 7 days) ==="
bq_query "SELECT user_email, COUNT(*) as query_count, ROUND(SUM(total_bytes_processed)/1024/1024/1024/1024, 4) as tb_processed, ROUND(SUM(total_bytes_processed)/1024/1024/1024/1024 * 6.25, 2) as estimated_cost_usd FROM \`region-us\`.INFORMATION_SCHEMA.JOBS_BY_PROJECT WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND job_type = 'QUERY' GROUP BY user_email ORDER BY tb_processed DESC LIMIT 20"

echo ""
echo "=== Slot Utilization ==="
bq_query "SELECT TIMESTAMP_TRUNC(period_start, HOUR) as hour, AVG(period_slot_ms / TIMESTAMP_DIFF(period_end, period_start, MILLISECOND)) as avg_slots FROM \`region-us\`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_PROJECT WHERE period_start > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR) GROUP BY hour ORDER BY hour DESC LIMIT 24"
```

### Query Optimization

```bash
#!/bin/bash
echo "=== Expensive Queries (last 24h, >1GB) ==="
bq_query "SELECT job_id, SUBSTR(query, 1, 100) as query_preview, ROUND(total_bytes_processed/1024/1024/1024, 2) as gb_processed, total_slot_ms, TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_sec FROM \`region-us\`.INFORMATION_SCHEMA.JOBS_BY_PROJECT WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR) AND total_bytes_processed > 1073741824 ORDER BY total_bytes_processed DESC LIMIT 15"

echo ""
echo "=== Query Plan Analysis ==="
# Dry run to check bytes scanned
bq_dryrun "SELECT col1, col2 FROM \`$GCP_PROJECT.$DATASET.$TABLE\` WHERE partition_col = '2024-01-01'"
```

### Storage Analysis

```bash
#!/bin/bash
echo "=== Storage by Dataset ==="
bq_query "SELECT table_schema, COUNT(*) as tables, ROUND(SUM(size_bytes)/1024/1024/1024, 2) as total_gb, ROUND(SUM(CASE WHEN storage_tier = 'LONG_TERM' THEN size_bytes ELSE 0 END)/1024/1024/1024, 2) as long_term_gb FROM \`$GCP_PROJECT\`.INFORMATION_SCHEMA.TABLE_STORAGE GROUP BY table_schema ORDER BY total_gb DESC"

echo ""
echo "=== Tables with No Long-term Storage Savings ==="
bq_query "SELECT table_schema, table_name, ROUND(size_bytes/1024/1024/1024, 2) as gb, TIMESTAMP_MILLIS(last_modified_time) as last_modified FROM \`$GCP_PROJECT\`.INFORMATION_SCHEMA.TABLE_STORAGE WHERE last_modified_time > UNIX_MILLIS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)) ORDER BY size_bytes DESC LIMIT 20"
```

## Output Format

Present results as a structured report:
```
Analyzing Bigquery Report
═════════════════════════
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

- **Full table scans**: Queries without partition filters scan entire tables — always filter on partition column
- **SELECT ***: Scanning all columns is expensive — select only needed columns
- **On-demand pricing**: Each TB scanned costs ~$6.25 — always dry-run first
- **Slot contention**: Flat-rate reservations share slots — check slot utilization
- **Streaming buffer**: Recently streamed data may not be in partitions yet — affects partition pruning
- **INFORMATION_SCHEMA region**: Must specify region (e.g., `region-us`) for jobs metadata
- **Legacy SQL**: Always use `--use_legacy_sql=false` — legacy SQL has different syntax and limitations
