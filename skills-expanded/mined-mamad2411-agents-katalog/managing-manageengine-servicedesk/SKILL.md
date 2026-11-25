---
name: managing-manageengine-servicedesk
description: |
  Use when working with Manageengine Servicedesk — manageEngine ServiceDesk Plus
  management covering incident handling, IT asset tracking, CMDB configuration,
  and reporting. Use when creating and managing incidents with SLA tracking,
  cataloging hardware and software assets, building CMDB relationships between
  configuration items, or generating operational performance reports.
connection_type: manageengine-servicedesk
preload: false
---

# ManageEngine ServiceDesk Plus Management Skill

Manage and analyze ManageEngine ServiceDesk Plus incidents, assets, and CMDB.

## API Conventions

### Authentication
All API calls use technician API key — injected as query parameter or header.

### Base URL
`https://{{server}}/api/v3`

### Core Helper Function

```bash
#!/bin/bash

me_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "authtoken: $MANAGEENGINE_API_KEY" \
            -H "Content-Type: application/json" \
            "${MANAGEENGINE_URL}/api/v3${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "authtoken: $MANAGEENGINE_API_KEY" \
            -H "Content-Type: application/json" \
            "${MANAGEENGINE_URL}/api/v3${endpoint}"
    fi
}
```

## Common Operations

### Incident Management

```bash
#!/bin/bash
echo "=== Open Requests ==="
me_api GET "/requests?list_info={\"row_count\":25,\"sort_field\":\"priority\",\"sort_order\":\"asc\",\"search_criteria\":{\"field\":\"status.name\",\"condition\":\"is not\",\"value\":\"Closed\"}}" \
    | jq -r '.requests[] | "\(.id)\t\(.priority.name)\t\(.status.name)\t\(.subject[0:60])"' \
    | column -t

echo ""
echo "=== Overdue Requests ==="
me_api GET "/requests?list_info={\"row_count\":15,\"search_criteria\":{\"field\":\"is_overdue\",\"condition\":\"is\",\"value\":true}}" \
    | jq -r '.requests[] | "\(.id)\t\(.priority.name)\t\(.due_by_time)\t\(.subject[0:50])"' \
    | column -t
```

### Asset Management

```bash
#!/bin/bash
echo "=== Asset Summary ==="
me_api GET "/assets?list_info={\"row_count\":100}" \
    | jq -r '[.assets[].product_type.name] | group_by(.) | map({type: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.type): \(.count)"'

echo ""
echo "=== Assets by State ==="
me_api GET "/assets?list_info={\"row_count\":100}" \
    | jq -r '[.assets[].asset_state] | group_by(.) | map({state: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.state): \(.count)"'
```

### CMDB Operations

```bash
#!/bin/bash
echo "=== CI Types ==="
me_api GET "/cmdb/ci_types" \
    | jq -r '.ci_types[] | "\(.id)\t\(.name)\t\(.ci_count // 0) CIs"' \
    | column -t

echo ""
echo "=== Configuration Items ==="
CI_TYPE_ID="${1:?CI Type ID required}"
me_api GET "/cmdb/ci_types/${CI_TYPE_ID}/cis?list_info={\"row_count\":25}" \
    | jq -r '.cis[] | "\(.id)\t\(.name)\t\(.ci_state // "-")"' \
    | column -t
```

## Output Format

Present results as a structured report:
```
Managing Manageengine Servicedesk Report
════════════════════════════════════════
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

- **list_info parameter**: Filtering and pagination use JSON-encoded `list_info` query parameter
- **Search criteria**: Nested JSON structure with `field`, `condition`, `value` — multiple criteria use `logical_operator`
- **Auth header**: Uses `authtoken` header (not `Authorization`) — format varies between cloud and on-premise
- **Rate limits**: Cloud edition enforces rate limits — check documentation for current limits
- **API versions**: v3 is current — v1 endpoints still work but may lack features
- **Date format**: Epoch milliseconds in responses — provide human-readable dates in search criteria
- **Pagination**: Use `row_count` and `start_index` in `list_info` JSON parameter
