---
name: managing-incident-io
description: |
  Use when working with Incident Io — incident.io incident lifecycle management,
  severity tracking, custom fields, status pages, post-incident reviews, and
  role assignments. Covers incident creation, escalation, follow-up tracking,
  and analytics. Use when investigating active incidents, reviewing
  post-mortems, analyzing incident trends, or managing incident workflows in
  incident.io.
connection_type: incident-io
preload: false
---

# incident.io Management Skill

Manage and analyze incidents, post-incident reviews, and workflows in incident.io.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $INCIDENT_IO_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.incident.io/v2`

### Core Helper Function

```bash
#!/bin/bash

iio_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $INCIDENT_IO_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.incident.io/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $INCIDENT_IO_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.incident.io/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Always filter by relevant time range to avoid huge response sets
- Never dump full API responses

## Discovery Phase

### List Active Incidents

```bash
#!/bin/bash
echo "=== Active Incidents ==="
iio_api GET "/incidents?page_size=25&status_category[one_of]=active" \
    | jq -r '.incidents[] | "\(.created_at[0:16])\t\(.severity.name)\t\(.status.name)\t\(.name[0:60])"' \
    | column -t

echo ""
echo "=== Incident Count by Severity ==="
iio_api GET "/incidents?page_size=100&status_category[one_of]=active" \
    | jq -r '.incidents[] | .severity.name' | sort | uniq -c | sort -rn
```

### List Incident Types and Severities

```bash
#!/bin/bash
echo "=== Severities ==="
iio_api GET "/severities" | jq -r '.severities[] | "\(.rank)\t\(.name)\t\(.description[0:60])"' | column -t

echo ""
echo "=== Incident Roles ==="
iio_api GET "/incident_roles" | jq -r '.incident_roles[] | "\(.role_type)\t\(.name)\t\(.required)"' | column -t

echo ""
echo "=== Custom Fields ==="
iio_api GET "/custom_fields" | jq -r '.custom_fields[] | "\(.field_type)\t\(.name)"' | column -t | head -15
```

## Analysis Phase

### Incident Analytics

```bash
#!/bin/bash
echo "=== Closed Incidents (last 30 days) ==="
iio_api GET "/incidents?page_size=100&status_category[one_of]=closed" \
    | jq '{
        total: (.incidents | length),
        by_severity: (.incidents | group_by(.severity.name) | map({(.[0].severity.name): length}) | add),
        avg_duration_hrs: (.incidents | map(select(.closed_at != null) | ((.closed_at | fromdateiso8601) - (.created_at | fromdateiso8601)) / 3600) | if length > 0 then add / length | . * 10 | round / 10 else 0 end)
    }'

echo ""
echo "=== Follow-ups Pending ==="
iio_api GET "/follow_ups?incident_mode=real&status=outstanding" \
    | jq -r '.follow_ups[0:15][] | "\(.priority.name // "none")\t\(.title[0:60])\t\(.assignee.name // "unassigned")"' \
    | column -t
```

### Incident Detail

```bash
#!/bin/bash
INCIDENT_ID="${1:?Incident ID required}"

echo "=== Incident Details ==="
iio_api GET "/incidents/${INCIDENT_ID}" \
    | jq '.incident | {id, name, status: .status.name, severity: .severity.name, created_at, closed_at, summary: .summary[0:200]}'

echo ""
echo "=== Incident Updates ==="
iio_api GET "/incident_updates?incident_id=${INCIDENT_ID}" \
    | jq -r '.incident_updates[0:10][] | "\(.created_at[0:16])\t\(.updater.name)\t\(.message[0:80])"' | column -t
```

## Output Format
- Always use tab-separated columns with `column -t` for tables
- Limit lists to 15-25 items with `head`
- Use `jq` to extract only relevant fields
- Show counts and summaries before detailed listings

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
- **Pagination**: Use `page_size` parameter, max 250 per page
- **Status categories**: Use `active`, `closed`, `paused` for filtering by lifecycle stage
- **API v2 only**: Always use `/v2` prefix -- v1 endpoints are deprecated
- **Rate limits**: 1000 requests per minute -- stagger parallel calls if needed
- **Follow-ups vs actions**: Follow-ups are post-incident tasks; actions are in-incident steps
