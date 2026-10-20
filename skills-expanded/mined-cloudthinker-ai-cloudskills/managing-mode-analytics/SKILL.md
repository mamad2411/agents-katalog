---
name: managing-mode-analytics
description: |
  Use when working with Mode Analytics — mode Analytics management — monitor
  workspaces, reports, queries, data sources, and scheduled runs. Use when
  reviewing report health, inspecting query performance, auditing data
  connections, or checking scheduled report delivery.
connection_type: mode-analytics
preload: false
---

# Managing Mode Analytics

Manage and monitor Mode Analytics — reports, queries, data sources, and scheduled runs.

## Discovery Phase

```bash
#!/bin/bash

MODE_API="https://app.mode.com/api"
AUTH="-u $MODE_API_TOKEN:$MODE_API_SECRET"

echo "=== Workspace Info ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE" \
  | jq '{name: .name, username: .username, plan: .plan}'

echo ""
echo "=== Data Sources ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/data_sources" \
  | jq -r '._embedded.data_sources[] | [.id, .name, .adapter, .has_expensive_schema_warning] | @tsv' | column -t | head -10

echo ""
echo "=== Spaces ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/spaces" \
  | jq -r '._embedded.spaces[] | [.token, .name, .space_type, .restricted] | @tsv' | column -t | head -10

echo ""
echo "=== Recent Reports ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/reports?order=desc&order_by=updated_at&limit=15" \
  | jq -r '._embedded.reports[] | [.token, .name, .updated_at, .last_run_state] | @tsv' | column -t
```

## Analysis Phase

```bash
#!/bin/bash

MODE_API="https://app.mode.com/api"
AUTH="-u $MODE_API_TOKEN:$MODE_API_SECRET"

echo "=== Report Run History ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/reports/$MODE_REPORT_TOKEN/runs?limit=10" \
  | jq -r '._embedded.report_runs[] | [.token, .state, .created_at, .completed_at] | @tsv' | column -t

echo ""
echo "=== Failed Runs (Recent) ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/report_runs?filter=failed&limit=10" \
  | jq -r '._embedded.report_runs[] | [.report_token, .state, .created_at, .error_message[:60]] | @tsv' | column -t

echo ""
echo "=== Scheduled Reports ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/report_schedules" \
  | jq -r '._embedded.report_schedules[] | [.report_token, .cron, .paused, .last_run_at] | @tsv' | column -t | head -10

echo ""
echo "=== Data Source Health ==="
for DS_ID in $(curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/data_sources" | jq -r '._embedded.data_sources[:5][].id'); do
  DS_NAME=$(curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/data_sources/$DS_ID" | jq -r '.name')
  STATUS=$(curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/data_sources/$DS_ID/status" | jq -r '.status // "unknown"')
  echo "$DS_NAME: $STATUS"
done

echo ""
echo "=== Query Performance (last run) ==="
curl -s $AUTH "$MODE_API/$MODE_WORKSPACE/reports/$MODE_REPORT_TOKEN/runs/latest/queries" \
  | jq -r '._embedded.queries[] | [.name, .state, .raw_rows, (.total_time_in_seconds | tostring) + "s"] | @tsv' | column -t
```

## Output Format

```
WORKSPACE
Name:       <workspace-name>
Plan:       <plan>

DATA SOURCES
ID       Name             Adapter      Warning
<id>     <ds-name>        <adapter>    <bool>

SCHEDULED REPORTS
Report           Cron          Paused   Last Run
<report-token>   <cron>        false    <timestamp>

FAILED RUNS
Report           State    Created         Error
<report-token>   failed   <timestamp>     <message>

QUERY PERFORMANCE
Query Name       State      Rows     Duration
<query-name>     completed  <n>      <seconds>s
```

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

