---
name: managing-dagster-deep
description: |
  Use when working with Dagster Deep — dagster deep data orchestration
  management covering job and asset inventory, run monitoring, schedule and
  sensor health, partition status, resource configuration, and daemon health
  checks. Use when investigating run failures, analyzing asset materialization,
  monitoring schedule ticks, or auditing Dagster configurations.
connection_type: dagster
preload: false
---

# Dagster Deep Management Skill

Manage and monitor Dagster jobs, assets, schedules, sensors, and infrastructure health.

## MANDATORY: Discovery-First Pattern

**Always list jobs and check daemon health before querying specific runs.**

### Phase 1: Discovery

```bash
#!/bin/bash

DAGSTER_API="${DAGSTER_URL:-http://localhost:3000}/graphql"

dagster_gql() {
    curl -s -H "Content-Type: application/json" \
         ${DAGSTER_API_TOKEN:+-H "Authorization: Bearer $DAGSTER_API_TOKEN"} \
         "${DAGSTER_API}" \
         -d "{\"query\": \"$1\"}"
}

echo "=== Dagster Instance Health ==="
dagster_gql "{ instance { daemonHealth { allDaemonStatuses { daemonType healthy lastHeartbeatTime } } } }" | jq -r '
    .data.instance.daemonHealth.allDaemonStatuses[] |
    "\(.daemonType)\t\(.healthy)\t\(.lastHeartbeatTime)"
' | column -t

echo ""
echo "=== Repositories ==="
dagster_gql "{ repositoriesOrError { ... on RepositoryConnection { nodes { name location { name } } } } }" | jq -r '
    .data.repositoriesOrError.nodes[] |
    "\(.name)\t\(.location.name)"
' | column -t

echo ""
echo "=== Jobs ==="
dagster_gql "{ repositoriesOrError { ... on RepositoryConnection { nodes { name pipelines { name } } } } }" | jq -r '
    .data.repositoriesOrError.nodes[] |
    .name as $repo | .pipelines[] |
    "\($repo)\t\(.name)"
' | column -t | head -30

echo ""
echo "=== Schedules ==="
dagster_gql "{ schedulesOrError { ... on Schedules { results { name scheduleState { status } cronSchedule } } } }" | jq -r '
    .data.schedulesOrError.results[] |
    "\(.name)\t\(.scheduleState.status)\t\(.cronSchedule)"
' | column -t | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Failed Runs (recent) ==="
dagster_gql "{ runsOrError(filter: { statuses: [FAILURE] }, limit: 15) { ... on Runs { results { runId pipelineName status startTime endTime } } } }" | jq -r '
    .data.runsOrError.results[] |
    "\(.runId[:8])\t\(.pipelineName)\t\(.status)\t\(.startTime)"
' | column -t

echo ""
echo "=== Sensors ==="
dagster_gql "{ sensorsOrError { ... on Sensors { results { name sensorState { status } } } } }" | jq -r '
    .data.sensorsOrError.results[] |
    "\(.name)\t\(.sensorState.status)"
' | column -t

echo ""
echo "=== Asset Health ==="
dagster_gql "{ assetsOrError { ... on AssetConnection { nodes { key { path } assetMaterializations(limit: 1) { timestamp } } } } }" | jq -r '
    .data.assetsOrError.nodes[] |
    "\(.key.path | join("/"))\tLast: \(.assetMaterializations[0].timestamp // "never")"
' | column -t | head -20

echo ""
echo "=== Run Queue ==="
dagster_gql "{ runsOrError(filter: { statuses: [QUEUED, STARTING] }, limit: 10) { ... on Runs { results { runId pipelineName status } } } }" | jq -r '
    .data.runsOrError.results[] |
    "\(.runId[:8])\t\(.pipelineName)\t\(.status)"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use status filters on GraphQL queries
- Never dump full run logs or asset metadata -- extract key status fields

## Output Format

Present results as a structured report:
```
Managing Dagster Deep Report
════════════════════════════
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

- **Daemon health**: Scheduler and sensor daemons must be running -- stale heartbeats mean no scheduling
- **Run coordinator**: Run queue limits control concurrency -- queued runs wait for slots
- **Code location errors**: Import errors prevent jobs from loading -- check code location health
- **Partition backfills**: Large backfills can overwhelm the run coordinator
- **Asset freshness**: Stale assets may indicate upstream failures -- trace the dependency graph
- **Sensor cursor**: Sensor cursors track state -- resetting a cursor reprocesses events
- **Resource config**: Missing or invalid resource configurations cause immediate run failures
- **IO managers**: IO manager misconfiguration causes silent data loss between ops
