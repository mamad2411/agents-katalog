---
name: managing-hyperproof
description: |
  Use when working with Hyperproof — hyperproof compliance operations platform
  for managing controls, evidence, risks, and audit workflows across multiple
  frameworks. Covers control testing, evidence automation, task management, risk
  register, and audit preparation. Use when reviewing control compliance,
  tracking evidence collection, managing compliance tasks, assessing
  organizational risk, or coordinating audit activities.
connection_type: hyperproof
preload: false
---

# Hyperproof Management Skill

Manage and analyze Hyperproof controls, evidence, tasks, risks, and audit workflows.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $HYPERPROOF_ACCESS_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://api.hyperproof.app/v1`

### Core Helper Function

```bash
#!/bin/bash

hp_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $HYPERPROOF_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.hyperproof.app/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $HYPERPROOF_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.hyperproof.app/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Programs ==="
hp_api GET "/programs" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.framework)"' | column -t | head -10

echo ""
echo "=== Controls Summary ==="
hp_api GET "/controls?pageSize=1" \
    | jq '"Total controls: \(.totalCount // (.data | length))"' -r

echo ""
echo "=== Task Summary ==="
hp_api GET "/tasks?pageSize=1&status=open" \
    | jq '"Open tasks: \(.totalCount // (.data | length))"' -r
```

## Analysis Phase

### Control Status

```bash
#!/bin/bash
PROGRAM_ID="${1:-}"

echo "=== Controls by Health ==="
ENDPOINT="/controls?pageSize=200"
[ -n "$PROGRAM_ID" ] && ENDPOINT="/programs/${PROGRAM_ID}/controls?pageSize=200"

CONTROLS=$(hp_api GET "$ENDPOINT")
echo "$CONTROLS" | jq '{
    total: (.data | length),
    healthy: ([.data[] | select(.healthStatus == "healthy")] | length),
    at_risk: ([.data[] | select(.healthStatus == "at_risk")] | length),
    unhealthy: ([.data[] | select(.healthStatus == "unhealthy")] | length),
    not_assessed: ([.data[] | select(.healthStatus == "not_assessed")] | length)
}'

echo ""
echo "=== Unhealthy Controls ==="
echo "$CONTROLS" | jq -r '.data[] | select(.healthStatus == "unhealthy" or .healthStatus == "at_risk") | "\(.healthStatus)\t\(.identifier)\t\(.name[0:45])\towner:\(.owner[0:20] // "Unassigned")"' \
    | column -t | head -15
```

### Evidence Management

```bash
#!/bin/bash
echo "=== Evidence Collection Status ==="
hp_api GET "/proofs?pageSize=200" \
    | jq '{
        total: (.data | length),
        current: ([.data[] | select(.status == "current")] | length),
        expiring_soon: ([.data[] | select(.status == "expiring_soon")] | length),
        expired: ([.data[] | select(.status == "expired")] | length),
        missing: ([.data[] | select(.status == "missing")] | length)
    }'

echo ""
echo "=== Expired/Missing Evidence ==="
hp_api GET "/proofs?pageSize=50&status=expired,missing" \
    | jq -r '.data[] | "\(.status)\t\(.name[0:35])\tcontrol:\(.controlIdentifier)\tdue:\(.dueDate[0:10] // "N/A")"' \
    | column -t | head -15
```

### Task Tracking

```bash
#!/bin/bash
echo "=== Open Tasks by Priority ==="
hp_api GET "/tasks?pageSize=100&status=open" \
    | jq -r '[.data[].priority] | group_by(.) | map({priority: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.priority): \(.count)"'

echo ""
echo "=== Overdue Tasks ==="
hp_api GET "/tasks?pageSize=50&status=open&overdue=true" \
    | jq -r '.data[] | "\(.priority)\t\(.name[0:40])\tassignee:\(.assignee[0:20] // "Unassigned")\tdue:\(.dueDate[0:10])"' \
    | column -t | head -15
```

### Risk Register

```bash
#!/bin/bash
echo "=== Risk Summary ==="
hp_api GET "/risks?pageSize=100" \
    | jq '{
        total: (.data | length),
        by_level: ([.data[].riskLevel] | group_by(.) | map({level: .[0], count: length}))
    }'

echo ""
echo "=== High/Critical Risks ==="
hp_api GET "/risks?pageSize=50&riskLevel=high,critical" \
    | jq -r '.data[] | "\(.riskLevel)\t\(.name[0:40])\tstatus:\(.treatmentStatus)\towner:\(.owner[0:20] // "Unassigned")"' \
    | column -t | head -15
```

## Output Format

Present results as a structured report:
```
Managing Hyperproof Report
══════════════════════════
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

- **Program scoping**: Most queries can be scoped to a program -- include program ID for framework-specific views
- **Health vs status**: Controls have `healthStatus` (automated) and manual assessment status
- **Pagination**: Use `pageSize` and `page` -- check `totalCount` in response
- **Rate limits**: Check response headers for rate limiting
- **Proof vs evidence**: Hyperproof uses "proofs" terminology for evidence artifacts
- **OAuth2 tokens**: Access tokens expire -- refresh via OAuth2 token endpoint
