---
name: managing-airflow
description: |
  Use when working with Airflow — apache Airflow workflow orchestration
  management. Covers DAG management, task instance monitoring, executor health,
  pool status, variable management, connection audit, and scheduler diagnostics.
  Use when checking DAG run status, investigating task failures, managing
  Airflow resources, or auditing configurations.
connection_type: airflow
preload: false
---

# Apache Airflow Management Skill

Manage and monitor Apache Airflow DAGs, task instances, and infrastructure via the Airflow REST API.

## MANDATORY: Discovery-First Pattern

**Always list DAGs and their states before querying specific tasks or runs.**

### Phase 1: Discovery

```bash
#!/bin/bash

airflow_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Content-Type: application/json" \
            "${AIRFLOW_BASE_URL}/api/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            "${AIRFLOW_BASE_URL}/api/v1/${endpoint}"
    fi
}

echo "=== Airflow Health ==="
airflow_api GET "health" | jq '{
    metadatabase: .metadatabase.status,
    scheduler: .scheduler.status,
    latest_heartbeat: .scheduler.latest_scheduler_heartbeat
}'

echo ""
echo "=== DAG Summary ==="
airflow_api GET "dags?limit=50&order_by=-last_parsed_time" | jq -r '
    .dags[] | "\(.dag_id)\t\(if .is_paused then "PAUSED" else "ACTIVE" end)\t\(.last_parsed_time // "never")[0:16]"
' | column -t | head -30

echo ""
echo "=== Recent DAG Runs (failed/running) ==="
airflow_api GET "dags/~/dagRuns?limit=20&order_by=-execution_date&state=failed,running" | jq -r '
    .dag_runs[] | "\(.dag_id)\t\(.state)\t\(.execution_date[0:16])\t\(.run_type)"
' | column -t | head -20
```

## Core Helper Functions

```bash
#!/bin/bash

airflow_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Content-Type: application/json" \
            "${AIRFLOW_BASE_URL}/api/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            "${AIRFLOW_BASE_URL}/api/v1/${endpoint}"
    fi
}

# URL-encode a DAG ID (handles special characters)
encode_dag_id() {
    python3 -c "import urllib.parse; print(urllib.parse.quote('$1', safe=''))"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to extract only needed fields from JSON responses
- Never dump full DAG serialization — extract key fields
- Filter by state at the API level using query parameters

## Common Operations

### DAG Run Status Dashboard

```bash
#!/bin/bash
echo "=== DAG Run Summary (last 24h) ==="
airflow_api GET "dags/~/dagRuns?limit=100&order_by=-execution_date&start_date_gte=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)" | jq '
    .dag_runs | group_by(.state) | map({state: .[0].state, count: length}) |
    sort_by(-.count) | .[] | "\(.state): \(.count)"
' -r

echo ""
echo "=== Failed DAG Runs ==="
airflow_api GET "dags/~/dagRuns?limit=20&order_by=-execution_date&state=failed" | jq -r '
    .dag_runs[] | "\(.dag_id)\t\(.execution_date[0:16])\t\(.run_type)\t\(.note // "")"
' | column -t | head -15

echo ""
echo "=== Currently Running ==="
airflow_api GET "dags/~/dagRuns?state=running&order_by=-execution_date" | jq -r '
    .dag_runs[] | "\(.dag_id)\t\(.execution_date[0:16])\t\(.start_date[0:16])"
' | column -t | head -10
```

### Task Instance Analysis

```bash
#!/bin/bash
DAG_ID="${1:?DAG ID required}"
DAG_RUN_ID="${2:?DAG Run ID required}"
ENCODED_DAG=$(encode_dag_id "$DAG_ID")

echo "=== Task Instances for $DAG_ID / $DAG_RUN_ID ==="
airflow_api GET "dags/${ENCODED_DAG}/dagRuns/${DAG_RUN_ID}/taskInstances" | jq -r '
    .task_instances[] |
    "\(.task_id)\t\(.state)\t\(.duration // 0 | floor)s\t\(.try_number)\t\(.operator)"
' | column -t

echo ""
echo "=== Failed Tasks ==="
airflow_api GET "dags/${ENCODED_DAG}/dagRuns/${DAG_RUN_ID}/taskInstances?state=failed" | jq -r '
    .task_instances[] |
    "\(.task_id)\t\(.try_number) tries\t\(.start_date[0:16])\t\(.end_date[0:16])"
' | column -t
```

### Pool and Executor Health

```bash
#!/bin/bash
echo "=== Pool Status ==="
airflow_api GET "pools" | jq -r '
    .pools[] | "\(.name)\tslots=\(.slots)\trunning=\(.running_slots)\tqueued=\(.queued_slots)\topen=\(.open_slots)"
' | column -t

echo ""
echo "=== Pools Near Capacity (>80%) ==="
airflow_api GET "pools" | jq -r '
    .pools[] |
    select(.slots > 0) |
    select((.running_slots / .slots) > 0.8) |
    "WARNING: \(.name) at \((.running_slots / .slots * 100) | floor)% (\(.running_slots)/\(.slots))"
'

echo ""
echo "=== Import Errors ==="
airflow_api GET "importErrors" | jq -r '
    .import_errors[] | "\(.filename)\t\(.timestamp[0:16])\t\(.stack_trace | split("\n") | last)"
' | head -10
```

### Variable and Connection Management

```bash
#!/bin/bash
echo "=== Variables ==="
airflow_api GET "variables?limit=50" | jq -r '
    .variables[] | "\(.key)\t\(.description // "no description")"
' | column -t | head -20

echo ""
echo "=== Connections ==="
airflow_api GET "connections?limit=50" | jq -r '
    .connections[] | "\(.connection_id)\t\(.conn_type)\t\(.host // "N/A")\t\(.port // "N/A")"
' | column -t | head -20

echo ""
echo "=== Connection Types in Use ==="
airflow_api GET "connections?limit=100" | jq -r '
    [.connections[].conn_type] | group_by(.) | map({type: .[0], count: length}) |
    sort_by(-.count) | .[] | "\(.type)\t\(.count)"
' | column -t
```

### DAG Trigger and Management

```bash
#!/bin/bash
DAG_ID="${1:?DAG ID required}"
DRY_RUN="${2:-true}"
ENCODED_DAG=$(encode_dag_id "$DAG_ID")

if [ "$DRY_RUN" = "true" ]; then
    echo "=== DRY RUN: DAG Info for $DAG_ID ==="
    airflow_api GET "dags/${ENCODED_DAG}" | jq '{
        dag_id: .dag_id,
        is_paused: .is_paused,
        schedule_interval: .schedule_interval,
        next_dagrun: .next_dagrun,
        last_parsed: .last_parsed_time,
        file_token: .file_token
    }'
    echo ""
    echo "To trigger, call with dry_run=false"
else
    echo "=== Triggering $DAG_ID ==="
    airflow_api POST "dags/${ENCODED_DAG}/dagRuns" \
        "{\"logical_date\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
        | jq '{dag_run_id: .dag_run_id, state: .state, execution_date: .execution_date}'
fi
```

## Output Format

Present results as a structured report:
```
Managing Airflow Report
═══════════════════════
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

- **DAG ID encoding**: DAG IDs with dots or slashes must be URL-encoded — use `encode_dag_id` helper
- **API versions**: Airflow 2.x uses `/api/v1/`, Airflow 1.x uses experimental API — confirm version first
- **Paused vs active**: Paused DAGs still accept manual triggers but won't run on schedule — check `is_paused`
- **Task retries**: A task may show `success` after multiple retries — check `try_number` to spot flaky tasks
- **Pool exhaustion**: If tasks are stuck in `queued`, check pool slot availability — default pool has 128 slots
- **Scheduler heartbeat**: If `latest_scheduler_heartbeat` is stale (>30s old), scheduler may be down
- **Import errors**: DAGs with Python syntax errors won't appear in the DAG list — always check `/importErrors`
- **Execution date vs start date**: `execution_date` is the logical date (schedule slot), `start_date` is when execution actually began
- **Trigger rules**: Tasks may not run despite upstream success if `trigger_rule` is set to something other than `all_success`
