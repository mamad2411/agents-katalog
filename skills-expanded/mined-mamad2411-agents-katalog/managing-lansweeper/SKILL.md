---
name: managing-lansweeper
description: |
  Use when working with Lansweeper — lansweeper IT asset discovery and inventory
  management covering network scanning, hardware and software inventory,
  compliance reporting, and vulnerability assessment. Use when discovering
  devices across the network, auditing installed software and patch levels,
  generating compliance reports for IT assets, or identifying unauthorized or
  unmanaged devices on the network.
connection_type: lansweeper
preload: false
---

# Lansweeper IT Asset Discovery & Inventory Skill

Manage and analyze Lansweeper asset discovery, inventory, and compliance.

## API Conventions

### Authentication
All API calls use personal access token or OAuth2 — injected automatically.

### Base URL
`https://api.lansweeper.com/api/v2`

### Core Helper Function

```bash
#!/bin/bash

ls_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
            -H "Content-Type: application/json" \
            "${LANSWEEPER_URL:-https://api.lansweeper.com}/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
            -H "Content-Type: application/json" \
            "${LANSWEEPER_URL:-https://api.lansweeper.com}/api/v2${endpoint}"
    fi
}
```

## Common Operations

### Asset Discovery

```bash
#!/bin/bash
echo "=== GraphQL: Asset Summary by Type ==="
curl -s -X POST \
    -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.lansweeper.com/api/v2/graphql" \
    -d '{
        "query": "query { site { id name assetResources(pagination: {limit: 50, page: 1}, fields: [\"assetBasicInfo.name\", \"assetBasicInfo.type\", \"assetBasicInfo.ipAddress\", \"assetBasicInfo.lastSeen\"]) { total items { url key fields { value } } } } }"
    }' | jq -r '.data.site.assetResources | "Total assets: \(.total)"'
```

### Hardware Inventory

```bash
#!/bin/bash
echo "=== Hardware Inventory ==="
curl -s -X POST \
    -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.lansweeper.com/api/v2/graphql" \
    -d '{
        "query": "query { site { assetResources(fields: [\"assetBasicInfo.name\", \"assetBasicInfo.type\", \"assetBasicInfo.manufacturer\", \"assetBasicInfo.model\", \"assetBasicInfo.lastSeen\"], pagination: {limit: 25}, filters: {conjunction: AND, conditions: [{path: \"assetBasicInfo.type\", operator: EQUAL, value: \"Windows\"}]}) { total items { key fields { value } } } } }"
    }' | jq -r '.data.site.assetResources.items[:25] | .[] | [.fields[].value] | join("\t")' | column -t
```

### Software Inventory

```bash
#!/bin/bash
echo "=== Installed Software Across Assets ==="
curl -s -X POST \
    -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.lansweeper.com/api/v2/graphql" \
    -d '{
        "query": "query { site { assetResources(fields: [\"assetBasicInfo.name\", \"softwares.name\", \"softwares.version\"], pagination: {limit: 25}) { total items { key fields { value } } } } }"
    }' | jq -r '.data.site.assetResources.items[:20] | .[] | [.fields[].value] | join("\t")' | column -t
```

### Compliance Reporting

```bash
#!/bin/bash
echo "=== Assets Not Seen in 30 Days ==="
THRESHOLD=$(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)
curl -s -X POST \
    -H "Authorization: Bearer $LANSWEEPER_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.lansweeper.com/api/v2/graphql" \
    -d "{
        \"query\": \"query { site { assetResources(fields: [\\\"assetBasicInfo.name\\\", \\\"assetBasicInfo.type\\\", \\\"assetBasicInfo.lastSeen\\\"], pagination: {limit: 25}, filters: {conjunction: AND, conditions: [{path: \\\"assetBasicInfo.lastSeen\\\", operator: LESS_THAN, value: \\\"${THRESHOLD}\\\"}]}) { total items { key fields { value } } } } }\"
    }" | jq -r '.data.site.assetResources | "Stale assets: \(.total)"'
```

## Output Format

Present results as a structured report:
```
Managing Lansweeper Report
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

- **GraphQL API**: Lansweeper Cloud uses GraphQL — not REST — construct queries carefully
- **Field paths**: Use dot-separated field paths like `assetBasicInfo.name`, `softwares.name`
- **Pagination**: Use `pagination: {limit: N, page: N}` — check `total` in response
- **Site context**: Queries run against a specific site — multi-site deployments need site selection
- **Filter operators**: Available operators include `EQUAL`, `NOT_EQUAL`, `CONTAINS`, `LESS_THAN`, `GREATER_THAN`
- **Rate limits**: Cloud API has rate limits — check response headers
- **Scan freshness**: `lastSeen` indicates last successful scan — stale data means the asset may be offline
