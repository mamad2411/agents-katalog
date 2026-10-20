---
name: managing-circleci
description: |
  Use when working with Circleci — circleCI pipeline and workflow management.
  Covers pipeline status, workflow analysis, job logs, credit usage monitoring,
  orb management, and project configuration. Use when checking CI status,
  investigating build failures, analyzing credit consumption, or managing
  CircleCI orbs.
connection_type: circleci
preload: false
---

# CircleCI Management Skill

Manage and monitor CircleCI pipelines, workflows, and credit usage.

## Core Helper Functions

```bash
#!/bin/bash

# CircleCI API v2 helper
circleci_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Circle-Token: ${CIRCLECI_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://circleci.com/api/v2/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Circle-Token: ${CIRCLECI_TOKEN}" \
            "https://circleci.com/api/v2/${endpoint}"
    fi
}

# Project slug helper (gh/org/repo or bb/org/repo)
project_slug() {
    echo "${1:?VCS type required}/${2:?org required}/${3:?repo required}"
}
```

## MANDATORY: Discovery-First Pattern

**Always list projects and pipelines before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Current User ==="
circleci_api GET "me" | jq '{login: .login, name: .name, id: .id}'

echo ""
echo "=== Recent Pipelines (org) ==="
circleci_api GET "pipeline?org-slug=gh/${CIRCLECI_ORG}&mine=false" | jq -r '
    .items[:15][] |
    "\(.project_slug)\t#\(.number)\t\(.state)\t\(.created_at[0:16])"
' | column -t

echo ""
echo "=== My Recent Pipelines ==="
circleci_api GET "pipeline?org-slug=gh/${CIRCLECI_ORG}&mine=true" | jq -r '
    .items[:10][] |
    "\(.project_slug)\t#\(.number)\t\(.state)\t\(.trigger.type)"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `jq` to filter API responses — CircleCI returns paginated results
- Never dump full job logs — tail relevant sections

## Common Operations

### Pipeline & Workflow Status

```bash
#!/bin/bash
PROJECT_SLUG="${1:?Project slug required (e.g. gh/org/repo)}"

echo "=== Recent Pipelines ==="
circleci_api GET "project/${PROJECT_SLUG}/pipeline?branch=main" | jq -r '
    .items[:10][] |
    "\(#\(.number))\t\(.state)\t\(.trigger.type)\t\(.created_at[0:16])"
' | column -t

echo ""
echo "=== Latest Pipeline Workflows ==="
PIPELINE_ID=$(circleci_api GET "project/${PROJECT_SLUG}/pipeline?branch=main" | jq -r '.items[0].id')
circleci_api GET "pipeline/${PIPELINE_ID}/workflow" | jq -r '
    .items[] |
    "\(.name)\t\(.status)\t\(.created_at[0:16])\tduration=\(if .stopped_at then (((.stopped_at | fromdateiso8601) - (.created_at | fromdateiso8601)) | floor) else "running" end)s"
' | column -t
```

### Workflow Job Analysis

```bash
#!/bin/bash
WORKFLOW_ID="${1:?Workflow ID required}"

echo "=== Workflow Jobs ==="
circleci_api GET "workflow/${WORKFLOW_ID}/job" | jq -r '
    .items[] |
    "\(.name)\t\(.status)\t\(.job_number // "pending")\t\(.started_at[0:16] // "queued")"
' | column -t

echo ""
echo "=== Failed Jobs Detail ==="
circleci_api GET "workflow/${WORKFLOW_ID}/job" | jq -r '
    .items[] | select(.status == "failed") |
    "\(.name)\tjob_number=\(.job_number)\ttype=\(.type)"
'
```

### Job Log Retrieval

```bash
#!/bin/bash
PROJECT_SLUG="${1:?Project slug required}"
JOB_NUMBER="${2:?Job number required}"

echo "=== Job Steps ==="
circleci_api GET "project/${PROJECT_SLUG}/job/${JOB_NUMBER}" | jq -r '
    .steps[] | .actions[] |
    "\(.step)\t\(.name)\t\(.status)\t\(.run_time_millis // 0 | . / 1000 | floor)s"
' | column -t

echo ""
echo "=== Failed Step Output ==="
circleci_api GET "project/${PROJECT_SLUG}/job/${JOB_NUMBER}" | jq -r '
    .steps[] | .actions[] | select(.status == "failed") |
    "Step: \(.name)\nOutput URL: \(.output_url)"
'
```

### Credit Usage Analysis

```bash
#!/bin/bash
echo "=== Credit Usage Summary (last 30 days) ==="
# Insights API for credit consumption
circleci_api GET "insights/gh/${CIRCLECI_ORG}/summary?reporting-window=last-30-days" | jq '{
    total_credits_used: .org_data.metrics.total_credits_used,
    total_runs: .org_data.metrics.total_runs,
    success_rate: (.org_data.metrics.success_rate * 100 | floor),
    throughput: .org_data.metrics.throughput
}'

echo ""
echo "=== Top Credit-Consuming Projects ==="
circleci_api GET "insights/gh/${CIRCLECI_ORG}/summary?reporting-window=last-30-days" | jq -r '
    .org_project_data | sort_by(-.metrics.total_credits_used) | .[:10][] |
    "\(.project_name)\tcredits=\(.metrics.total_credits_used | floor)\truns=\(.metrics.total_runs)\tsuccess=\(.metrics.success_rate * 100 | floor)%"
' | column -t

echo ""
echo "=== Workflow Credit Breakdown ==="
circleci_api GET "insights/gh/${CIRCLECI_ORG}/${PROJECT}/workflows?reporting-window=last-30-days" | jq -r '
    .items | sort_by(-.metrics.total_credits_used) | .[:10][] |
    "\(.name)\tcredits=\(.metrics.total_credits_used | floor)\tmedian_duration=\(.metrics.duration_metrics.median | floor)s"
' | column -t
```

### Orb Management

```bash
#!/bin/bash
echo "=== Organization Orbs ==="
circleci_api GET "orb?owner-slug=gh/${CIRCLECI_ORG}&mine=true" | jq -r '
    .items[] | "\(.name)\tv\(.versions[0].version // "none")\t\(.statistics.last_30_day_build_count // 0) builds/30d"
' | column -t

echo ""
echo "=== Orb Details ==="
ORB_NAME="${1:-circleci/node}"
circleci_api GET "orb/${ORB_NAME}" | jq '{
    name: .name,
    latest_version: .versions[0].version,
    created_at: .created_at,
    description: .description
}'
```

### Rerun and Cancel Operations

```bash
#!/bin/bash
WORKFLOW_ID="${1:?Workflow ID required}"
ACTION="${2:-status}"  # status, rerun-failed, cancel

case "$ACTION" in
    "status")
        circleci_api GET "workflow/${WORKFLOW_ID}" | jq '{id, name, status, created_at, stopped_at}'
        ;;
    "rerun-failed")
        echo "=== Rerunning failed jobs in workflow ==="
        circleci_api POST "workflow/${WORKFLOW_ID}/rerun" '{"from_failed": true}' | jq .
        ;;
    "cancel")
        echo "=== Canceling workflow ==="
        circleci_api POST "workflow/${WORKFLOW_ID}/cancel" | jq .
        ;;
esac
```

## Anti-Hallucination Rules
- NEVER guess project slugs — always use the format `gh/org/repo` or `bb/org/repo`
- NEVER fabricate workflow or pipeline IDs — always discover via API
- NEVER assume orb availability — verify orb exists before referencing
- CircleCI API v2 uses UUIDs for workflows and pipelines, not sequential numbers

## Safety Rules
- NEVER trigger pipelines without explicit user confirmation
- NEVER cancel running workflows without user approval
- Credit usage queries are read-only and safe to run
- Rerunning workflows consumes credits — warn user before rerun

## Output Format

Present results as a structured report:
```
Managing Circleci Report
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
- **API versions**: v1.1 and v2 coexist — most management tasks use v2, some legacy endpoints use v1.1
- **Project slug format**: Must be `{vcs}/{org}/{repo}` — GitHub is `gh/`, Bitbucket is `bb/`
- **Pagination**: API responses are paginated — use `page-token` from response for next page
- **Credit classes**: Different resource classes consume credits at different rates (Docker vs machine vs macOS)
- **Contexts vs env vars**: Organization contexts share secrets across projects — project env vars are project-scoped
- **Config validation**: Use `circleci config validate` locally before pushing — syntax errors block pipeline creation
