---
name: analyzing-influxdb
description: |
  Use when working with Influxdb — influxDB bucket management, Flux query
  analysis, task management, retention policies, and performance monitoring.
connection_type: influxdb
preload: false
---

# InfluxDB Analysis Skill

Analyze and optimize InfluxDB instances with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated bucket/measurement names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List organizations (InfluxDB 2.x)
influx org list

# 2. List buckets
influx bucket list

# 3. List measurements in a bucket
influx query 'import "influxdata/influxdb/schema"
schema.measurements(bucket: "my_bucket")'

# 4. List field keys for a measurement
influx query 'import "influxdata/influxdb/schema"
schema.measurementFieldKeys(bucket: "my_bucket", measurement: "my_measurement")'

# 5. List tag keys
influx query 'import "influxdata/influxdb/schema"
schema.measurementTagKeys(bucket: "my_bucket", measurement: "my_measurement")'

# 6. Sample data
influx query 'from(bucket: "my_bucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "my_measurement")
  |> limit(n: 5)'
```

**Phase 1 outputs:**
- Organizations and buckets
- Measurements with field and tag keys
- Sample data to confirm schema

### Phase 2: Analysis (only after Phase 1)

Only reference buckets, measurements, fields, and tags confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Flux query runner — always use this
influx_query() {
    local query="$1"
    influx query --org "${INFLUX_ORG}" "$query"
}

# InfluxDB API helper
influx_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Token ${INFLUX_TOKEN}" \
        "http://${INFLUX_HOST:-localhost}:8086$endpoint"
}

# InfluxQL (1.x compat)
influx_v1() {
    local query="$1"
    curl -s -G "http://${INFLUX_HOST:-localhost}:8086/query" \
        --data-urlencode "q=$query" \
        -H "Authorization: Token ${INFLUX_TOKEN}"
}
```

## Anti-Hallucination Rules

- **NEVER reference a bucket** without confirming via `influx bucket list`
- **NEVER reference measurement names** without discovering via `schema.measurements()`
- **NEVER assume field or tag keys** — always check via schema functions
- **NEVER guess retention periods** — check bucket configuration
- **NEVER assume task names** — list tasks first

## Safety Rules

- **READ-ONLY ONLY**: Use only `from()`, `schema.*`, `influx query`, API GET endpoints
- **FORBIDDEN**: `to()`, `influx delete`, `influx bucket delete`, `influx write` without explicit user request
- **ALWAYS bound queries with `range()`** — unbounded queries scan all data
- **Use short time ranges** for initial exploration, then expand
- **Limit output** with `|> limit(n: 100)` on exploration queries

## Common Operations

### Bucket Overview

```bash
#!/bin/bash
echo "=== Buckets ==="
influx bucket list --json | jq '.[] | {name, id, retentionPeriod: (.retentionRules[0].everySeconds // 0 | . / 86400 | tostring + " days"), orgID}'

echo ""
echo "=== Measurements per Bucket ==="
for BUCKET in $(influx bucket list --json | jq -r '.[].name' | grep -v _); do
    echo "--- $BUCKET ---"
    influx_query "import \"influxdata/influxdb/schema\"
    schema.measurements(bucket: \"$BUCKET\")" 2>/dev/null
done
```

### Task Management

```bash
#!/bin/bash
echo "=== Tasks ==="
influx task list --json | jq '.[] | {name, id, status, every, lastRunStatus: .latestCompleted}'

echo ""
echo "=== Task Run History ==="
TASK_ID="${1:-}"
if [ -n "$TASK_ID" ]; then
    influx task run list --task-id "$TASK_ID" --json | jq '.[] | {runID: .id, status, scheduledFor, startedAt, finishedAt}'
fi

echo ""
echo "=== Failed Tasks ==="
influx task list --json | jq '[.[] | select(.latestCompleted != null)] | .[] | {name, status}'
```

### Query Performance Analysis

```bash
#!/bin/bash
BUCKET="${1:-my_bucket}"

echo "=== Cardinality Check ==="
influx_query "import \"influxdata/influxdb\"
influxdb.cardinality(bucket: \"$BUCKET\", start: -24h)"

echo ""
echo "=== Series Count by Measurement ==="
influx_query "import \"influxdata/influxdb/schema\"
schema.measurements(bucket: \"$BUCKET\")
  |> limit(n: 20)"

echo ""
echo "=== Tag Value Cardinality ==="
influx_query "import \"influxdata/influxdb/schema\"
schema.measurementTagValues(bucket: \"$BUCKET\", measurement: \"my_measurement\", tag: \"host\")
  |> count()"
```

### Retention & Storage

```bash
#!/bin/bash
echo "=== Bucket Retention Policies ==="
influx bucket list --json | jq '.[] | {name, retentionSeconds: .retentionRules[0].everySeconds, retentionDays: ((.retentionRules[0].everySeconds // 0) / 86400)}'

echo ""
echo "=== Storage Stats (API) ==="
influx_api "/api/v2/orgs/${INFLUX_ORG_ID}/usage" 2>/dev/null || echo "Usage API not available"

echo ""
echo "=== Shard Info (if available) ==="
influx_v1 "SHOW SHARDS" 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Analyzing Influxdb Report
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

- **Unbounded range**: Queries without `range()` scan entire bucket history — always specify start time
- **High cardinality**: Too many unique tag values causes memory issues — check cardinality before querying
- **Tags vs fields**: Tags are indexed (fast to filter), fields are not — do not store high-cardinality data as tags
- **Task scheduling**: Tasks have minimum interval of 1s in OSS, 1m in Cloud — check limits
- **Schema-on-write**: InfluxDB does not enforce schema — inconsistent field types cause query errors
- **Downsampling**: Use continuous queries or tasks for downsampling — querying raw high-resolution data is expensive
