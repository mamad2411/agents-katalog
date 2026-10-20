---
name: gcp-cloud-spanner
description: |
  Use when working with Gcp Cloud Spanner — google Cloud Spanner instance
  management, query statistics analysis, hot spot detection, schema analysis,
  and performance diagnostics via gcloud CLI.
connection_type: gcp
preload: false
---

# Cloud Spanner Skill

Manage and analyze Google Cloud Spanner using `gcloud spanner` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume instance names, database names, or table names.

```bash
# Discover Spanner instances
gcloud spanner instances list --format=json \
  | jq '[.[] | {name: .name | split("/") | last, displayName: .displayName, config: .config | split("/") | last, nodeCount: .nodeCount, processingUnits: .processingUnits, state: .state}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for instance in $(gcloud spanner instances list --format="value(name)" | xargs -I{} basename {}); do
  {
    gcloud spanner databases list --instance="$instance" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# List databases in an instance
list_databases() {
  local instance="$1"
  gcloud spanner databases list --instance="$instance" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, state: .state, versionRetentionPeriod: .versionRetentionPeriod, earliestVersionTime: .earliestVersionTime, encryptionConfig: .encryptionConfig, databaseDialect: .databaseDialect}]'
}

# Get database DDL (schema)
get_schema() {
  local instance="$1" database="$2"
  gcloud spanner databases ddl describe --instance="$instance" --database="$database" --format=json
}

# Execute a read-only query
query_spanner() {
  local instance="$1" database="$2" sql="$3"
  gcloud spanner databases execute-sql "$database" --instance="$instance" --sql="$sql" --format=json
}

# Get instance metrics
get_instance_metrics() {
  local instance="$1"
  gcloud monitoring time-series list \
    --filter="metric.type=starts_with(\"spanner.googleapis.com/\") AND resource.labels.instance_id=\"$instance\"" \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format=json --limit=50
}
```

## Common Operations

### 1. Instance and Database Overview

```bash
instances=$(gcloud spanner instances list --format="value(name)" | xargs -I{} basename {})
for inst in $instances; do
  {
    echo "=== Instance: $inst ==="
    gcloud spanner instances describe "$inst" --format=json \
      | jq '{name: .name | split("/") | last, config: .config | split("/") | last, processingUnits: .processingUnits, nodeCount: .nodeCount, state: .state}'
    list_databases "$inst"
  } &
done
wait
```

### 2. Query Statistics

```bash
# Top queries by CPU usage (from SPANNER_SYS)
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT text, execution_count, avg_latency_seconds, avg_cpu_seconds
  FROM SPANNER_SYS.QUERY_STATS_TOP_MINUTE
  ORDER BY avg_cpu_seconds DESC
  LIMIT 10"

# Query statistics over the last hour
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT text, execution_count, avg_latency_seconds, avg_rows_scanned, avg_cpu_seconds
  FROM SPANNER_SYS.QUERY_STATS_TOP_HOUR
  ORDER BY execution_count DESC
  LIMIT 10"
```

### 3. Hot Spot Detection

```bash
# Read/write statistics by table
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT t.TABLE_NAME, t.ROW_COUNT, t.BYTES
  FROM INFORMATION_SCHEMA.TABLE_STATISTICS AS t
  ORDER BY t.BYTES DESC"

# Lock statistics (detect contention)
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT ROW_RANGE_START_KEY, LOCK_WAIT_SECONDS, SAMPLE_LOCK_REQUESTS
  FROM SPANNER_SYS.LOCK_STATS_TOP_MINUTE
  ORDER BY LOCK_WAIT_SECONDS DESC
  LIMIT 10"

# Transaction statistics
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT FPRINT, READ_COLUMNS, WRITE_CONSTRUCTIVE_COLUMNS, AVG_COMMIT_LATENCY_SECONDS, AVG_TOTAL_LATENCY_SECONDS
  FROM SPANNER_SYS.TXN_STATS_TOP_MINUTE
  ORDER BY AVG_TOTAL_LATENCY_SECONDS DESC
  LIMIT 10"
```

### 4. Schema Analysis

```bash
# Get full schema DDL
get_schema "$INSTANCE" "$DATABASE"

# Table and index information
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT TABLE_NAME, COLUMN_NAME, SPANNER_TYPE, IS_NULLABLE, ORDINAL_POSITION
  FROM INFORMATION_SCHEMA.COLUMNS
  ORDER BY TABLE_NAME, ORDINAL_POSITION"

# Index usage
query_spanner "$INSTANCE" "$DATABASE" "
  SELECT TABLE_NAME, INDEX_NAME, INDEX_TYPE, IS_UNIQUE, IS_NULL_FILTERED
  FROM INFORMATION_SCHEMA.INDEXES
  ORDER BY TABLE_NAME"
```

### 5. Performance Monitoring

```bash
# CPU utilization
gcloud monitoring time-series list \
  --filter="metric.type=\"spanner.googleapis.com/instance/cpu/utilization\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Storage usage
gcloud monitoring time-series list \
  --filter="metric.type=\"spanner.googleapis.com/instance/storage/used_bytes\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Operation latencies
gcloud monitoring time-series list \
  --filter="metric.type=\"spanner.googleapis.com/api/request_latencies\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json
```

## Output Format

Present results as a structured report:
```
Gcp Cloud Spanner Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

1. **Sequential primary keys**: Monotonically increasing keys (timestamps, auto-increment) cause hot spots. Use UUIDs or bit-reversed sequences.
2. **Node count vs processing units**: 1 node = 1000 processing units. Scaling by processing units gives finer granularity (minimum 100 PU for regional, 300 PU for multi-region).
3. **Interleaved tables**: Interleaved tables co-locate parent and child rows for performance. Deleting a parent row cascades to children if `ON DELETE CASCADE` is set.
4. **SPANNER_SYS tables**: System statistics tables are available only for queries from `gcloud spanner databases execute-sql`, not from client libraries without explicit configuration.
5. **Stale reads**: Use `--read-timestamp` or `--exact-staleness` for stale reads that reduce lock contention. Fresh reads (default) require locks.
