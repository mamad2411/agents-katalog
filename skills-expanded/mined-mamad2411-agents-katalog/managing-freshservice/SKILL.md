---
name: managing-freshservice
description: |
  Use when working with Freshservice — freshservice ITSM platform management
  covering ticket lifecycle, asset management, change requests, release
  management, and CMDB. Use when creating or triaging support tickets, tracking
  IT assets and their relationships, managing change and release workflows, or
  querying the configuration management database for infrastructure
  dependencies.
connection_type: freshservice
preload: false
---

# Freshservice ITSM Management Skill

Manage and analyze Freshservice tickets, assets, changes, releases, and CMDB.

## API Conventions

### Authentication
All API calls use API key as Basic Auth username (password is `X`). Injected automatically.

### Base URL
`https://{{domain}}.freshservice.com/api/v2`

### Core Helper Function

```bash
#!/bin/bash

fs_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "$FRESHSERVICE_API_KEY:X" \
            -H "Content-Type: application/json" \
            "${FRESHSERVICE_URL}/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "$FRESHSERVICE_API_KEY:X" \
            -H "Content-Type: application/json" \
            "${FRESHSERVICE_URL}/api/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Use query parameters for server-side filtering
- Never dump full API responses

## Common Operations

### Ticket Management

```bash
#!/bin/bash
echo "=== Open Tickets by Priority ==="
fs_api GET "/tickets?filter=open&order_by=priority&order_type=desc&per_page=25" \
    | jq -r '.tickets[] | "\(.id)\tP\(.priority)\t\(.status)\t\(.subject[0:60])"' \
    | column -t

echo ""
echo "=== Unassigned Tickets ==="
fs_api GET "/tickets?filter=open&per_page=20" \
    | jq -r '[.tickets[] | select(.responder_id == null)] | .[] | "\(.id)\tP\(.priority)\t\(.created_at[0:16])\t\(.subject[0:50])"' \
    | column -t

echo ""
echo "=== Overdue Tickets ==="
fs_api GET "/tickets?filter=overdue&per_page=15" \
    | jq -r '.tickets[] | "\(.id)\tP\(.priority)\t\(.due_by[0:16])\t\(.subject[0:50])"' \
    | column -t
```

### Asset Management

```bash
#!/bin/bash
echo "=== Asset Inventory Summary ==="
fs_api GET "/assets?per_page=100" \
    | jq -r '[.assets[] | .asset_type_id] | group_by(.) | map({type: .[0], count: length}) | sort_by(.count) | reverse | .[] | "Type \(.type): \(.count) assets"'

echo ""
echo "=== Recently Added Assets ==="
fs_api GET "/assets?order_by=created_at&order_type=desc&per_page=15" \
    | jq -r '.assets[] | "\(.display_id)\t\(.name)\t\(.asset_type_id)\t\(.created_at[0:10])"' \
    | column -t
```

### Change Management

```bash
#!/bin/bash
echo "=== Pending Changes ==="
fs_api GET "/changes?per_page=20" \
    | jq -r '[.changes[] | select(.status == 1 or .status == 2)] | .[] | "\(.id)\t\(.change_type)\t\(.risk)\t\(.subject[0:50])"' \
    | column -t

echo ""
echo "=== Upcoming Planned Changes ==="
fs_api GET "/changes?order_by=planned_start_date&order_type=asc&per_page=15" \
    | jq -r '.changes[] | "\(.id)\t\(.planned_start_date[0:16])\t\(.subject[0:50])"' \
    | column -t
```

### CMDB Operations

```bash
#!/bin/bash
echo "=== CI Types ==="
fs_api GET "/cmdb/ci_types" \
    | jq -r '.ci_types[] | "\(.id)\t\(.name)\t\(.description[0:40] // "-")"' \
    | column -t

echo ""
echo "=== Configuration Items ==="
CI_TYPE_ID="${1:?CI Type ID required}"
fs_api GET "/cmdb/items?ci_type_id=${CI_TYPE_ID}&per_page=25" \
    | jq -r '.items[] | "\(.display_id)\t\(.name)\t\(.ci_type_id)\t\(.state)"' \
    | column -t
```

## Output Format

Present results as a structured report:
```
Managing Freshservice Report
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

- **Priority values**: 1=Low, 2=Medium, 3=High, 4=Urgent — numeric, not string
- **Status values**: 2=Open, 3=Pending, 4=Resolved, 5=Closed — varies by ticket type
- **Rate limits**: 50 requests/min for Sprout, higher for paid tiers — check `X-Ratelimit-Remaining`
- **Pagination**: Max 100 per page — use `page` parameter for pagination
- **Nested includes**: Use `?include=stats,requester` to side-load related data
- **Date format**: ISO 8601 format in UTC
- **Custom fields**: Access via the ticket's custom field names — check field configuration first
