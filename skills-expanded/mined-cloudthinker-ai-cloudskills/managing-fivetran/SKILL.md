---
name: managing-fivetran
description: |
  Use when working with Fivetran — fivetran data integration connector
  management. Covers connector status monitoring, sync operations, schema drift
  detection, usage metrics, destination management, and transformation
  scheduling. Use when checking connector sync status, investigating sync
  failures, managing schema configurations, or analyzing Fivetran usage.
connection_type: fivetran
preload: false
---

# Fivetran Management Skill

Manage and monitor Fivetran connectors, sync operations, and data pipeline health via the Fivetran API.

## MANDATORY: Discovery-First Pattern

**Always list groups and connectors before querying specific sync details.**

### Phase 1: Discovery

```bash
#!/bin/bash

fivetran_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Basic ${FIVETRAN_API_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.fivetran.com/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Basic ${FIVETRAN_API_KEY}" \
            "https://api.fivetran.com/v1/${endpoint}"
    fi
}

echo "=== Groups (Destinations) ==="
fivetran_api GET "groups" | jq -r '
    .data.items[] | "\(.id)\t\(.name)\t\(.created_at[0:10])"
' | column -t

echo ""
echo "=== All Connectors ==="
fivetran_api GET "groups" | jq -r '.data.items[].id' | while read gid; do
    fivetran_api GET "groups/${gid}/connectors" | jq -r --arg gid "$gid" '
        .data.items[]? | "\(.id)\t\(.service)\t\(.schema)\t\(.status.sync_state)\t\(.status.update_state)"
    '
done | column -t | head -30
```

## Core Helper Functions

```bash
#!/bin/bash

fivetran_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Basic ${FIVETRAN_API_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.fivetran.com/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Basic ${FIVETRAN_API_KEY}" \
            "https://api.fivetran.com/v1/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to filter connector details — never dump full schema configs
- Filter by sync state or connector status at display level

## Common Operations

### Connector Health Dashboard

```bash
#!/bin/bash
echo "=== Connector Status Summary ==="
fivetran_api GET "groups" | jq -r '.data.items[].id' | while read gid; do
    fivetran_api GET "groups/${gid}/connectors"
done | jq -s '
    [.[].data.items[]?] |
    {
        total: length,
        connected: [.[] | select(.status.sync_state == "scheduled")] | length,
        syncing: [.[] | select(.status.sync_state == "syncing")] | length,
        broken: [.[] | select(.status.setup_state == "broken")] | length,
        paused: [.[] | select(.paused == true)] | length
    }'

echo ""
echo "=== Broken / Error Connectors ==="
fivetran_api GET "groups" | jq -r '.data.items[].id' | while read gid; do
    fivetran_api GET "groups/${gid}/connectors" | jq -r '
        .data.items[]? |
        select(.status.setup_state == "broken" or (.status.tasks[]?.code? // "" | test("error"))) |
        "\(.id)\t\(.service)\t\(.schema)\t\(.status.tasks[0]?.message? // "unknown error")"
    '
done | column -t | head -15
```

### Sync Status and History

```bash
#!/bin/bash
CONNECTOR_ID="${1:?Connector ID required}"

echo "=== Connector Details ==="
fivetran_api GET "connectors/${CONNECTOR_ID}" | jq '{
    id: .data.id,
    service: .data.service,
    schema: .data.schema,
    sync_state: .data.status.sync_state,
    update_state: .data.status.update_state,
    paused: .data.paused,
    sync_frequency: .data.sync_frequency,
    succeeded_at: .data.succeeded_at,
    failed_at: .data.failed_at
}'

echo ""
echo "=== Recent Sync Logs ==="
fivetran_api GET "connectors/${CONNECTOR_ID}/logs?limit=10" | jq -r '
    .data.items[]? | "\(.created_at[0:16])\t\(.event)\t\(.message[0:80] // "")"
' | head -15
```

### Schema Drift Detection

```bash
#!/bin/bash
CONNECTOR_ID="${1:?Connector ID required}"

echo "=== Schema Configuration ==="
fivetran_api GET "connectors/${CONNECTOR_ID}/schemas" | jq -r '
    .data.schemas | to_entries[] |
    .key as $schema |
    .value.tables | to_entries[] |
    "\($schema).\(.key)\t\(.value.enabled)\t\(.value.sync_mode // "default")"
' | column -t | head -30

echo ""
echo "=== Disabled Tables ==="
fivetran_api GET "connectors/${CONNECTOR_ID}/schemas" | jq -r '
    .data.schemas | to_entries[] |
    .key as $schema |
    .value.tables | to_entries[] |
    select(.value.enabled == false) |
    "\($schema).\(.key)"
' | head -15

echo ""
echo "=== Column-Level Changes ==="
fivetran_api GET "connectors/${CONNECTOR_ID}/schemas" | jq -r '
    .data.schemas | to_entries[] |
    .key as $schema |
    .value.tables | to_entries[] |
    .key as $table |
    .value.columns? | to_entries[]? |
    select(.value.enabled == false) |
    "\($schema).\($table).\(.key)\tDISABLED"
' | head -15
```

### Usage Metrics

```bash
#!/bin/bash
echo "=== Monthly Active Rows (MAR) by Connector ==="
fivetran_api GET "groups" | jq -r '.data.items[].id' | while read gid; do
    fivetran_api GET "groups/${gid}/connectors" | jq -r '
        .data.items[]? | "\(.id)\t\(.service)\t\(.schema)\t\(.daily_sync_frequency // "N/A")"
    '
done | column -t | head -20

echo ""
echo "=== Usage by Group ==="
fivetran_api GET "groups" | jq -r '
    .data.items[] | "\(.id)\t\(.name)"
' | while IFS=$'\t' read gid gname; do
    COUNT=$(fivetran_api GET "groups/${gid}/connectors" | jq '.data.items | length')
    echo -e "${gname}\t${COUNT} connectors"
done | column -t
```

### Connector Management

```bash
#!/bin/bash
CONNECTOR_ID="${1:?Connector ID required}"
ACTION="${2:?Action required: pause|unpause|sync}"

case "$ACTION" in
    pause)
        echo "=== Pausing Connector $CONNECTOR_ID ==="
        fivetran_api PATCH "connectors/${CONNECTOR_ID}" '{"paused": true}' | jq '{
            id: .data.id, paused: .data.paused, status: .code
        }'
        ;;
    unpause)
        echo "=== Unpausing Connector $CONNECTOR_ID ==="
        fivetran_api PATCH "connectors/${CONNECTOR_ID}" '{"paused": false}' | jq '{
            id: .data.id, paused: .data.paused, status: .code
        }'
        ;;
    sync)
        echo "=== Triggering Sync for $CONNECTOR_ID ==="
        fivetran_api POST "connectors/${CONNECTOR_ID}/force" | jq '{
            code: .code, message: .message
        }'
        ;;
    *)
        echo "Unknown action: $ACTION (use pause, unpause, or sync)"
        ;;
esac
```

## Output Format

Present results as a structured report:
```
Managing Fivetran Report
════════════════════════
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

- **API auth**: Fivetran uses Basic auth with base64-encoded `api_key:api_secret` — ensure `FIVETRAN_API_KEY` is pre-encoded
- **Sync states**: `scheduled` means idle/waiting, `syncing` means active — `scheduled` does NOT mean it hasn't synced yet
- **Setup state**: `broken` means the connector cannot sync — check `.status.tasks` for specific error messages
- **Schema changes**: New tables/columns from source are auto-added but may be disabled by schema change handling policy
- **Force sync**: Triggering a force sync doesn't guarantee immediate start — it queues based on available slots
- **Sync frequency**: Measured in minutes — `60` means hourly, `1440` means daily
- **Historical syncs**: Initial sync can take much longer than incremental — check `succeeded_at` vs connector creation date
- **Group = Destination**: In Fivetran, a "group" maps to one warehouse destination — connectors are children of groups
- **Rate limits**: API rate limit is 100 requests/minute per API key — batch requests where possible
