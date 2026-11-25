---
name: managing-gitlab-ci
description: |
  Use when working with Gitlab Ci — gitLab CI/CD pipeline and runner management.
  Covers pipeline status, job logs, runner administration, artifact management,
  environment deployments, and merge request pipelines. Use when checking CI
  status, investigating job failures, managing runners, or auditing deployment
  history.
connection_type: gitlab
preload: false
---

# GitLab CI Management Skill

Manage and monitor GitLab CI/CD pipelines, runners, and artifacts.

## Core Helper Functions

```bash
#!/bin/bash

# GitLab API helper
gitlab_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
            -H "Content-Type: application/json" \
            "${GITLAB_URL:-https://gitlab.com}/api/v4/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
            "${GITLAB_URL:-https://gitlab.com}/api/v4/${endpoint}"
    fi
}

# URL-encode project path
gitlab_project() {
    echo "${1}" | sed 's/\//%2F/g'
}
```

## MANDATORY: Discovery-First Pattern

**Always list projects and pipelines before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID or URL-encoded path required}"

echo "=== Project Info ==="
gitlab_api GET "projects/${PROJECT_ID}" | jq '{id: .id, name: .name, default_branch: .default_branch, web_url: .web_url}'

echo ""
echo "=== Recent Pipelines ==="
gitlab_api GET "projects/${PROJECT_ID}/pipelines?per_page=15" | jq -r '
    .[] | "\(.id)\t\(.status)\t\(.ref)\t\(.source)\t\(.created_at[0:16])"
' | column -t

echo ""
echo "=== Runners (project) ==="
gitlab_api GET "projects/${PROJECT_ID}/runners" | jq -r '
    .[] | "\(.id)\t\(.description)\t\(.status)\t\(.runner_type)\t\(.active)"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `per_page` parameter to limit results
- Never dump full job traces — extract relevant sections

## Common Operations

### Pipeline Status Dashboard

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Pipeline Summary (last 50) ==="
gitlab_api GET "projects/${PROJECT_ID}/pipelines?per_page=50" | jq '{
    total: length,
    success: [.[] | select(.status == "success")] | length,
    failed: [.[] | select(.status == "failed")] | length,
    running: [.[] | select(.status == "running")] | length,
    pending: [.[] | select(.status == "pending")] | length,
    canceled: [.[] | select(.status == "canceled")] | length
}'

echo ""
echo "=== Failed Pipelines ==="
gitlab_api GET "projects/${PROJECT_ID}/pipelines?status=failed&per_page=10" | jq -r '
    .[] | "\(.id)\t\(.ref)\t\(.source)\t\(.created_at[0:16])\t\(.web_url)"
' | column -t
```

### Job Log Analysis

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"
PIPELINE_ID="${2:?Pipeline ID required}"

echo "=== Pipeline Jobs ==="
gitlab_api GET "projects/${PROJECT_ID}/pipelines/${PIPELINE_ID}/jobs?per_page=50" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.stage)\t\(.status)\t\(.duration // 0 | floor)s"
' | column -t

echo ""
echo "=== Failed Job Logs (tail) ==="
FAILED_JOB=$(gitlab_api GET "projects/${PROJECT_ID}/pipelines/${PIPELINE_ID}/jobs" | jq '[.[] | select(.status == "failed")][0].id')
if [ "$FAILED_JOB" != "null" ] && [ -n "$FAILED_JOB" ]; then
    gitlab_api GET "projects/${PROJECT_ID}/jobs/${FAILED_JOB}/trace" | tail -60
fi
```

### Runner Management

```bash
#!/bin/bash
echo "=== All Runners (admin) ==="
gitlab_api GET "runners/all?per_page=30" | jq -r '
    .[] | "\(.id)\t\(.description)\t\(.status)\t\(.runner_type)\t\(.platform // "unknown")\ttags=\(.tag_list | join(","))"
' | column -t

echo ""
echo "=== Offline Runners ==="
gitlab_api GET "runners/all?status=offline&per_page=20" | jq -r '
    .[] | "\(.id)\t\(.description)\t\(.contacted_at[0:16])\t\(.runner_type)"
' | column -t

echo ""
echo "=== Runner Jobs (active) ==="
RUNNER_ID="${1:?Runner ID required}"
gitlab_api GET "runners/${RUNNER_ID}/jobs?status=running" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.project.name)\t\(.pipeline.id)"
' | column -t
```

### Artifact Management

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Recent Job Artifacts ==="
gitlab_api GET "projects/${PROJECT_ID}/jobs?per_page=20" | jq -r '
    .[] | select(.artifacts != []) |
    "\(.id)\t\(.name)\t\(.artifacts | map(.size) | add // 0 | . / 1024 | floor)KB\t\(.artifacts_expire_at[0:10] // "no-expiry")"
' | column -t

echo ""
echo "=== Download Artifact ==="
JOB_ID="${2:?Job ID required}"
echo "URL: ${GITLAB_URL:-https://gitlab.com}/api/v4/projects/${PROJECT_ID}/jobs/${JOB_ID}/artifacts"
echo "Use: gitlab_api GET 'projects/${PROJECT_ID}/jobs/${JOB_ID}/artifacts' > artifacts.zip"
```

### Environment & Deployment Status

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Environments ==="
gitlab_api GET "projects/${PROJECT_ID}/environments?per_page=20" | jq -r '
    .[] | "\(.name)\t\(.state)\t\(.last_deployment.status // "never")\t\(.last_deployment.created_at[0:16] // "n/a")"
' | column -t

echo ""
echo "=== Recent Deployments ==="
gitlab_api GET "projects/${PROJECT_ID}/deployments?per_page=10&order_by=created_at&sort=desc" | jq -r '
    .[] | "\(.id)\t\(.environment)\t\(.status)\t\(.ref)\t\(.created_at[0:16])"
' | column -t
```

### Merge Request Pipelines

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Open MR Pipelines ==="
gitlab_api GET "projects/${PROJECT_ID}/merge_requests?state=opened&per_page=15" | jq -r '
    .[] | select(.pipeline != null) |
    "MR!\(.iid)\t\(.title[0:40])\tpipeline=\(.pipeline.status)\t\(.pipeline.web_url)"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess project IDs — discover via API or use URL-encoded path
- NEVER fabricate pipeline or job IDs — always query first
- NEVER assume runner tags — list runners to see available tags
- Project paths must be URL-encoded (e.g., `group%2Fsubgroup%2Fproject`)

## Safety Rules
- NEVER retry or cancel pipelines without user confirmation
- NEVER delete environments or runners without explicit approval
- NEVER expose CI/CD variable values — use masked/protected variables
- Job traces may contain secrets — warn user before displaying raw logs

## Output Format

Present results as a structured report:
```
Managing Gitlab Ci Report
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
- **Project ID vs path**: API accepts numeric ID or URL-encoded path — numeric is safer
- **Pipeline sources**: `push`, `merge_request_event`, `schedule`, `api`, `trigger` — filter by source when investigating
- **Runner scopes**: Instance, group, and project runners have different visibility — check the right scope
- **Job artifacts expiry**: Artifacts expire based on CI config — `expire_in: 1 week` is common
- **Protected branches**: CI variables marked `protected` only available on protected branch pipelines
- **DAG vs stage ordering**: `needs:` keyword creates DAG — jobs may not follow stage order
- **Detached pipelines**: MR pipelines run detached from branch — they have different merge ref behavior
