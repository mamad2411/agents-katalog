---
name: managing-buildkite
description: |
  Use when working with Buildkite — buildkite CI/CD pipeline and agent
  management. Covers build pipeline status, agent pool health, artifact
  management, build annotations, and cluster queue monitoring. Use when checking
  build status, investigating failures, managing agents, or reviewing pipeline
  configurations.
connection_type: buildkite
preload: false
---

# Buildkite Management Skill

Manage and monitor Buildkite build pipelines, agents, and artifacts.

## Core Helper Functions

```bash
#!/bin/bash

# Buildkite REST API helper
buildkite_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BUILDKITE_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://api.buildkite.com/v2/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${BUILDKITE_TOKEN}" \
            "https://api.buildkite.com/v2/${endpoint}"
    fi
}

# GraphQL API helper for complex queries
buildkite_graphql() {
    local query="$1"
    curl -s -X POST \
        -H "Authorization: Bearer ${BUILDKITE_TOKEN}" \
        -H "Content-Type: application/json" \
        "https://graphql.buildkite.com/v1" \
        -d "{\"query\": \"$query\"}"
}
```

## MANDATORY: Discovery-First Pattern

**Always list pipelines and agents before querying specific builds.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Organization Info ==="
buildkite_api GET "organizations/${BK_ORG}" | jq '{name: .name, slug: .slug, pipelines_count: .pipelines_count, agents_count: .agents_count}'

echo ""
echo "=== Pipelines ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines?per_page=20" | jq -r '
    .[] | "\(.slug)\t\(.running_builds_count) running\t\(.scheduled_builds_count) queued\t\(.visibility)"
' | column -t

echo ""
echo "=== Agent Summary ==="
buildkite_api GET "organizations/${BK_ORG}/agents?per_page=30" | jq -r '
    .[] | "\(.name)\t\(.connection_state)\t\(.hostname)\tqueue=\(.metadata // [] | map(select(startswith("queue="))) | .[0] // "default")"
' | column -t | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `per_page` for pagination — default is 30, max is 100
- Never dump full build logs — use annotation or step-level retrieval

## Common Operations

### Build Pipeline Dashboard

```bash
#!/bin/bash
PIPELINE="${1:?Pipeline slug required}"

echo "=== Recent Builds ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds?per_page=15" | jq -r '
    .[] | "\(#\(.number))\t\(.state)\t\(.branch)\t\(.created_at[0:16])\t\(.creator.name // "api")"
' | column -t

echo ""
echo "=== Build State Summary ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds?per_page=50" | jq '{
    total: length,
    passed: [.[] | select(.state == "passed")] | length,
    failed: [.[] | select(.state == "failed")] | length,
    running: [.[] | select(.state == "running")] | length,
    canceled: [.[] | select(.state == "canceled")] | length,
    blocked: [.[] | select(.state == "blocked")] | length
}'
```

### Build Job Analysis

```bash
#!/bin/bash
PIPELINE="${1:?Pipeline slug required}"
BUILD_NUMBER="${2:?Build number required}"

echo "=== Build Jobs ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}" | jq -r '
    .jobs[] | select(.type == "script") |
    "\(.name // .command[0:40])\t\(.state)\t\(.agent.name // "unassigned")\t\(.started_at[0:16] // "pending")"
' | column -t

echo ""
echo "=== Failed Jobs ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}" | jq -r '
    .jobs[] | select(.state == "failed") |
    "Job: \(.name // .command[0:50])\nExit: \(.exit_status)\nAgent: \(.agent.name // "unknown")\n---"
'

echo ""
echo "=== Failed Job Log (tail) ==="
FAILED_JOB_ID=$(buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}" | jq -r '.jobs[] | select(.state == "failed") | .id' | head -1)
if [ -n "$FAILED_JOB_ID" ]; then
    buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}/jobs/${FAILED_JOB_ID}/log" | jq -r '.content' | tail -50
fi
```

### Agent Pool Management

```bash
#!/bin/bash
echo "=== All Agents ==="
buildkite_api GET "organizations/${BK_ORG}/agents?per_page=50" | jq -r '
    .[] | "\(.name)\t\(.connection_state)\t\(.ip_address)\t\(.hostname)\tversion=\(.version)\tjob=\(.job.id // "idle")"
' | column -t

echo ""
echo "=== Agents by Queue ==="
buildkite_api GET "organizations/${BK_ORG}/agents?per_page=100" | jq -r '
    group_by(.metadata // [] | map(select(startswith("queue="))) | .[0] // "default") |
    .[] | "\(.[0].metadata // [] | map(select(startswith("queue="))) | .[0] // "default")\t\(length) agents\t\([.[] | select(.connection_state == "connected")] | length) connected"
' | column -t

echo ""
echo "=== Disconnected Agents ==="
buildkite_api GET "organizations/${BK_ORG}/agents?per_page=50" | jq -r '
    .[] | select(.connection_state != "connected") |
    "\(.name)\t\(.connection_state)\tlast_seen=\(.lost_at[0:16] // "unknown")"
' | column -t
```

### Artifact Management

```bash
#!/bin/bash
PIPELINE="${1:?Pipeline slug required}"
BUILD_NUMBER="${2:?Build number required}"

echo "=== Build Artifacts ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}/artifacts" | jq -r '
    .[] | "\(.filename)\tsize=\(.file_size / 1024 | floor)KB\t\(.state)\tjob=\(.job_id[0:8])"
' | column -t

echo ""
echo "=== Download URL ==="
ARTIFACT_ID="${3:-}"
if [ -n "$ARTIFACT_ID" ]; then
    buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}/artifacts/${ARTIFACT_ID}/download" | jq '.url'
fi
```

### Build Annotations

```bash
#!/bin/bash
PIPELINE="${1:?Pipeline slug required}"
BUILD_NUMBER="${2:?Build number required}"

echo "=== Build Annotations ==="
buildkite_api GET "organizations/${BK_ORG}/pipelines/${PIPELINE}/builds/${BUILD_NUMBER}/annotations" | jq -r '
    .[] | "\(.context)\t\(.style)\t\(.body_html[0:80])"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess pipeline slugs — always discover via API first
- NEVER fabricate build numbers — query pipeline builds to find actual numbers
- NEVER assume agent queues — list agents to see available metadata/queues
- Agent metadata format varies — always inspect before filtering

## Safety Rules
- NEVER trigger builds without explicit user confirmation
- NEVER stop agents or cancel builds without user approval
- NEVER unblock builds without confirming the block step purpose
- Build logs may contain sensitive output — warn before displaying

## Output Format

Present results as a structured report:
```
Managing Buildkite Report
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
- **Build states**: `scheduled`, `running`, `passed`, `failed`, `blocked`, `canceled`, `canceling`, `skipping`, `not_run`
- **Block steps**: Builds in `blocked` state require manual unblock — they are intentional gates
- **Agent metadata**: Queue assignment uses metadata tags (e.g., `queue=deploy`) not a dedicated field
- **GraphQL vs REST**: Some features (pipeline metrics, cluster queues) are only available via GraphQL API
- **Webhook tokens**: Different from API tokens — webhook tokens validate incoming webhooks
- **Dynamic pipelines**: `buildkite-agent pipeline upload` can modify pipeline at runtime — YAML may not reflect actual steps
