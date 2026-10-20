---
name: managing-blameless
description: |
  Use when working with Blameless — blameless incident management, SLO tracking,
  retrospectives, and reliability insights. Covers incident lifecycle, blameless
  retrospective facilitation, follow-up tracking, reliability scorecards, and
  incident type categorization. Use when managing active incidents, conducting
  retrospectives, tracking SLO compliance, or analyzing reliability trends in
  Blameless.
connection_type: blameless
preload: false
---

# Blameless Management Skill

Manage and analyze incidents, retrospectives, SLOs, and reliability insights in Blameless.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $BLAMELESS_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.blameless.com/api/v1`

### Core Helper Function

```bash
#!/bin/bash

bl_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $BLAMELESS_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.blameless.com/api/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $BLAMELESS_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.blameless.com/api/v1${endpoint}"
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
bl_api GET "/incidents?status=active&limit=25" \
    | jq -r '.incidents[] | "\(.created_at[0:16])\t\(.severity)\t\(.status)\t\(.title[0:60])"' \
    | column -t

echo ""
echo "=== Incident Types ==="
bl_api GET "/incident-types" \
    | jq -r '.incident_types[] | "\(.name)\t\(.description[0:50])"' | column -t
```

### List SLOs

```bash
#!/bin/bash
echo "=== SLO Overview ==="
bl_api GET "/slos?limit=25" \
    | jq -r '.slos[] | "\(.name)\t\(.target)%\t\(.current_value)%\t\(.status)"' \
    | column -t

echo ""
echo "=== SLOs At Risk ==="
bl_api GET "/slos?limit=50" \
    | jq -r '.slos[] | select(.current_value < .target) | "\(.name)\ttarget:\(.target)%\tcurrent:\(.current_value)%"' | column -t
```

## Analysis Phase

### Retrospective Summary

```bash
#!/bin/bash
echo "=== Recent Retrospectives ==="
bl_api GET "/retrospectives?limit=15&sort=-created_at" \
    | jq -r '.retrospectives[] | "\(.created_at[0:16])\t\(.incident.title[0:40])\t\(.status)"' \
    | column -t

echo ""
echo "=== Pending Follow-ups ==="
bl_api GET "/follow-ups?status=open&limit=15" \
    | jq -r '.follow_ups[] | "\(.priority // "none")\t\(.title[0:60])\t\(.assignee.name // "unassigned")"' \
    | column -t
```

### Incident Detail

```bash
#!/bin/bash
INCIDENT_ID="${1:?Incident ID required}"

echo "=== Incident Details ==="
bl_api GET "/incidents/${INCIDENT_ID}" \
    | jq '.incident | {id, title, status, severity, type: .incident_type.name, created_at, resolved_at, summary: .summary[0:200]}'

echo ""
echo "=== Timeline ==="
bl_api GET "/incidents/${INCIDENT_ID}/events?limit=15" \
    | jq -r '.events[] | "\(.created_at[0:16])\t\(.event_type)\t\(.description[0:60])"' | column -t
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
- **Retrospective workflow**: Retrospectives go through stages (draft, in-review, published)
- **SLO windows**: SLOs use rolling or calendar windows -- check window type before comparing
- **Follow-ups vs tasks**: Follow-ups are post-incident commitments tracked separately from incident tasks
- **Rate limits**: Respect API rate limiting headers
- **Pagination**: Use `limit` and `offset` parameters
