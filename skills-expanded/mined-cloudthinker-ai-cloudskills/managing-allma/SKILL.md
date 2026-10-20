---
name: managing-allma
description: |
  Use when working with Allma — allma incident management, collaboration
  workflows, post-incident learning, and channel orchestration. Covers incident
  creation via Slack, timeline tracking, stakeholder communication, automated
  workflows, and retrospective analysis. Use when managing active incidents,
  reviewing post-incident learnings, or analyzing incident patterns in Allma.
connection_type: allma
preload: false
---

# Allma Management Skill

Manage and analyze incidents, post-incident reviews, and collaboration workflows in Allma.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $ALLMA_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.allma.io/v1`

### Core Helper Function

```bash
#!/bin/bash

allma_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ALLMA_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.allma.io/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ALLMA_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.allma.io/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Active Incidents

```bash
#!/bin/bash
echo "=== Active Incidents ==="
allma_api GET "/incidents?status=open&limit=25" \
    | jq -r '.incidents[] | "\(.created_at[0:16])\t\(.severity)\t\(.status)\t\(.title[0:60])"' \
    | column -t

echo ""
echo "=== Incident Count by Severity ==="
allma_api GET "/incidents?status=open&limit=100" \
    | jq -r '.incidents[] | .severity' | sort | uniq -c | sort -rn
```

### List Workflows and Templates

```bash
#!/bin/bash
echo "=== Workflows ==="
allma_api GET "/workflows" \
    | jq -r '.workflows[] | "\(.name)\t\(.trigger_type)\t\(.enabled)"' | column -t

echo ""
echo "=== Incident Templates ==="
allma_api GET "/templates" \
    | jq -r '.templates[] | "\(.name)\t\(.severity)\t\(.description[0:50])"' | column -t
```

## Analysis Phase

### Incident Analytics

```bash
#!/bin/bash
echo "=== Resolved Incidents Summary ==="
allma_api GET "/incidents?status=resolved&limit=50" \
    | jq '{
        total: (.incidents | length),
        by_severity: (.incidents | group_by(.severity) | map({(.[0].severity // "unknown"): length}) | add)
    }'

echo ""
echo "=== Pending Action Items ==="
allma_api GET "/action-items?status=open&limit=15" \
    | jq -r '.action_items[] | "\(.priority // "none")\t\(.title[0:60])\t\(.assignee // "unassigned")"' \
    | column -t
```

### Incident Detail

```bash
#!/bin/bash
INCIDENT_ID="${1:?Incident ID required}"

echo "=== Incident Details ==="
allma_api GET "/incidents/${INCIDENT_ID}" \
    | jq '.incident | {id, title, status, severity, created_at, resolved_at, summary: .summary[0:200]}'

echo ""
echo "=== Timeline ==="
allma_api GET "/incidents/${INCIDENT_ID}/timeline?limit=15" \
    | jq -r '.events[] | "\(.created_at[0:16])\t\(.type)\t\(.content[0:60])"' | column -t
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Slack-native**: Allma incidents are tied to Slack channels -- channel context may be needed
- **Workflows**: Automated workflows trigger on incident events -- check trigger conditions
- **Pagination**: Use `limit` and `offset` parameters
- **Rate limits**: Respect API rate limiting headers
- **Action items**: Post-incident action items are tracked separately from incident timeline
