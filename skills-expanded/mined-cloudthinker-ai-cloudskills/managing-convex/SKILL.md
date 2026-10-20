---
name: managing-convex
description: |
  Use when working with Convex — convex backend platform management covering
  project inventory, table schemas, function deployments, scheduled job status,
  index configuration, environment variable auditing, and usage metrics. Use for
  comprehensive Convex project health and resource optimization.
connection_type: convex
preload: false
---

# Convex Management

Analyze Convex projects, tables, functions, scheduled jobs, and deployment health.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${CONVEX_DEPLOY_KEY}"
DEPLOY_URL="${CONVEX_URL}"
AUTH=(-H "Authorization: Convex ${TOKEN}" -H "Content-Type: application/json")

echo "=== Deployment Info ==="
curl -s "${DEPLOY_URL}/api/get_deployment_info" "${AUTH[@]}" \
  | jq -r '"Project: \(.projectSlug)\tTeam: \(.teamSlug)\tStatus: \(.deploymentState)"' \
  | column -t

echo ""
echo "=== Tables ==="
curl -s "${DEPLOY_URL}/api/list_tables" "${AUTH[@]}" \
  | jq -r '.[] | "\(.name)\t\(.documentCount // "N/A") docs\t\(.sizeBytes // "N/A") bytes"' \
  | column -t | head -20

echo ""
echo "=== Functions ==="
curl -s "${DEPLOY_URL}/api/list_functions" "${AUTH[@]}" \
  | jq -r '.[] | "\(.name)\t\(.type)\t\(.visibility)"' \
  | column -t | head -30

echo ""
echo "=== Indexes ==="
curl -s "${DEPLOY_URL}/api/list_indexes" "${AUTH[@]}" \
  | jq -r '.[] | "\(.table)\t\(.name)\t\(.fields | join(","))\t\(.status)"' \
  | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${CONVEX_DEPLOY_KEY}"
DEPLOY_URL="${CONVEX_URL}"
AUTH=(-H "Authorization: Convex ${TOKEN}" -H "Content-Type: application/json")

echo "=== Scheduled Jobs ==="
curl -s "${DEPLOY_URL}/api/list_scheduled_jobs" "${AUTH[@]}" \
  | jq -r '.[] | "\(.name)\t\(.state)\t\(.scheduledTime)\t\(.completedTime // \"pending\")"' \
  | column -t | head -20

echo ""
echo "=== Cron Jobs ==="
curl -s "${DEPLOY_URL}/api/list_cron_jobs" "${AUTH[@]}" \
  | jq -r '.[] | "\(.name)\t\(.schedule)\t\(.lastRun // \"never\")\t\(.nextRun)"' \
  | column -t | head -10

echo ""
echo "=== Environment Variables (names only) ==="
curl -s "${DEPLOY_URL}/api/list_environment_variables" "${AUTH[@]}" \
  | jq -r '.[].name' | while read -r name; do echo "  ${name}"; done

echo ""
echo "=== Usage Metrics ==="
curl -s "${DEPLOY_URL}/api/usage" "${AUTH[@]}" \
  | jq '{function_calls: .functionCalls, database_bandwidth: .databaseBandwidth, storage_bandwidth: .storageBandwidth, action_compute: .actionCompute}' 2>/dev/null

echo ""
echo "=== Recent Deployments ==="
curl -s "${DEPLOY_URL}/api/list_deployments" "${AUTH[@]}" \
  | jq -r '.[:5][] | "\(.id[0:8])\t\(.status)\t\(.startTime)\t\(.endTime // \"in-progress\")"' \
  | column -t | head -10
```

## Output Format

```
CONVEX ANALYSIS
=================
Table            Documents    Size       Indexes   Functions
──────────────────────────────────────────────────────────────
users            5,240        12MB       3         8 (query/mutation)
messages         124,500      89MB       5         12 (query/mutation/action)
sessions         2,100        3MB        2         4 (query/mutation)

Functions: 24 total (10 queries, 8 mutations, 6 actions)
Cron Jobs: 3 active | Scheduled: 2 pending
Env Vars: 8 configured | Deployments: 5 recent (all successful)
```

## Safety Rules

- **Read-only**: Only use list/get API endpoints
- **Never run mutations**, delete tables, or modify indexes without confirmation
- **Environment variables**: Never output values, only names
- **Deploy keys**: Never expose deploy key values in output

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

