---
name: managing-apache-airflow-deep
description: |
  Use when working with Apache Airflow Deep — apache Airflow deep management
  covering DAG inventory, task instance monitoring, scheduler health, executor
  status, pool and variable management, connection auditing, and SLA miss
  tracking. Use when investigating DAG failures, analyzing task duration trends,
  monitoring scheduler performance, or auditing Airflow configurations.
connection_type: airflow
preload: false
---

# Apache Airflow Deep Management Skill

Manage and monitor Apache Airflow DAGs, task instances, scheduler, and infrastructure health.

## MANDATORY: Discovery-First Pattern

**Always list DAGs and check scheduler health before querying specific task instances.**

### Phase 1: Discovery

```bash
#!/bin/bash

AIRFLOW_API="${AIRFLOW_BASE_URL}/api/v1"

airflow_api() {
    curl -s -u "$AIRFLOW_USERNAME:$AIRFLOW_PASSWORD" \
         -H "Content-Type: application/json" \
         "${AIRFLOW_API}/${1}"
}

echo "=== Airflow Health ==="
airflow_api "health" | jq '{
    metadatabase: .metadatabase.status,
    scheduler: .scheduler.status,
    scheduler_heartbeat: .scheduler.latest_scheduler_heartbeat
}'

echo ""
echo "=== DAGs Summary ==="
airflow_api "dags?limit=50" | jq -r '
    .dags[] |
    "\(.dag_id)\t\(.is_paused)\t\(.schedule_interval // "None")\t\(.owners | join(","))"
' | column -t | head -30

echo ""
echo "=== Pools ==="
airflow_api "pools" | jq -r '
    .pools[] |
    "\(.name)\t\(.slots)\tqueued=\(.queued_slots)\trunning=\(.running_slots)\topen=\(.open_slots)"
' | column -t
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Failed DAG Runs (last 24h) ==="
YESTERDAY=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)
airflow_api "dags/~/dagRuns?start_date_gte=${YESTERDAY}&state=failed&limit=20" | jq -r '
    .dag_runs[] |
    "\(.dag_id)\t\(.dag_run_id)\t\(.state)\t\(.end_date // "running")"
' | column -t | head -20

echo ""
echo "=== Failed Task Instances (last 24h) ==="
airflow_api "dags/~/dagRuns/~/taskInstances?start_date_gte=${YESTERDAY}&state=failed&limit=20" | jq -r '
    .task_instances[] |
    "\(.dag_id)\t\(.task_id)\t\(.state)\t\(.try_number) tries\t\(.duration // 0)s"
' | column -t | head -20

echo ""
echo "=== SLA Misses ==="
airflow_api "dags/~/dagRuns/~/taskInstances?state=sla_miss&limit=10" 2>/dev/null | jq -r '
    .task_instances[]? |
    "\(.dag_id)\t\(.task_id)\t\(.execution_date)"
' | column -t

echo ""
echo "=== Variables (names only) ==="
airflow_api "variables?limit=50" | jq -r '.variables[].key' | head -20

echo ""
echo "=== Connections Summary ==="
airflow_api "connections?limit=50" | jq -r '
    .connections[] |
    "\(.connection_id)\t\(.conn_type)\t\(.host // "n/a")"
' | column -t | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use date filters to scope DAG runs and task instances
- Never dump full DAG source code or XCom values -- extract key metadata

## Output Format

Present results as a structured report:
```
Managing Apache Airflow Deep Report
═══════════════════════════════════
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

- **Scheduler lag**: If scheduler heartbeat is stale, tasks will not be scheduled -- check scheduler process
- **Pool exhaustion**: All pool slots occupied means tasks queue indefinitely -- monitor open_slots
- **Zombie tasks**: Tasks marked running but scheduler lost contact -- check for zombie detection in logs
- **DAG parsing errors**: Import errors prevent DAGs from loading -- check import_errors endpoint
- **XCom size**: Large XCom values degrade database performance -- monitor XCom table size
- **Executor capacity**: Celery/Kubernetes executor has worker limits -- check worker availability
- **Database connections**: Metadata DB connection pool exhaustion causes widespread failures
- **Catchup**: DAGs with catchup=True can spawn hundreds of backfill runs when unpaused
