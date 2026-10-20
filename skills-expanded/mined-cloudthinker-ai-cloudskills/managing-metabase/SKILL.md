---
name: managing-metabase
description: |
  Use when working with Metabase — metabase BI platform management. Covers
  question and dashboard analysis, database connection management,
  pulse/subscription monitoring, collection organization, query performance, and
  user activity tracking. Use when analyzing dashboards, investigating query
  issues, managing database connections, or auditing Metabase usage.
connection_type: metabase
preload: false
---

# Metabase Management Skill

Manage and analyze Metabase questions, dashboards, database connections, and user activity via the Metabase API.

## MANDATORY: Discovery-First Pattern

**Always discover databases and collections before querying specific questions or dashboards.**

### Phase 1: Discovery

```bash
#!/bin/bash

metabase_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "X-Metabase-Session: ${METABASE_SESSION_TOKEN}" \
            -H "Content-Type: application/json" \
            "${METABASE_URL}/api/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "X-Metabase-Session: ${METABASE_SESSION_TOKEN}" \
            "${METABASE_URL}/api/${endpoint}"
    fi
}

echo "=== Databases ==="
metabase_api GET "database" | jq -r '
    .data[] | "\(.id)\t\(.name)\t\(.engine)\t\(if .is_sample then "SAMPLE" else "CUSTOM" end)"
' | column -t

echo ""
echo "=== Collections ==="
metabase_api GET "collection" | jq -r '
    .[] | select(.personal_owner_id == null) | "\(.id)\t\(.name)\t\(.location // "/")"
' | column -t | head -20

echo ""
echo "=== Recent Activity ==="
metabase_api GET "activity?limit=15" | jq -r '
    .[] | "\(.timestamp[0:16])\t\(.topic)\t\(.user?.common_name // "system")\t\(.model_id // "")"
' | column -t | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

metabase_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "X-Metabase-Session: ${METABASE_SESSION_TOKEN}" \
            -H "Content-Type: application/json" \
            "${METABASE_URL}/api/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "X-Metabase-Session: ${METABASE_SESSION_TOKEN}" \
            "${METABASE_URL}/api/${endpoint}"
    fi
}

# Authenticate and get session token if needed
metabase_login() {
    curl -s -X POST \
        -H "Content-Type: application/json" \
        "${METABASE_URL}/api/session" \
        -d "{\"username\": \"${METABASE_USER}\", \"password\": \"${METABASE_PASS}\"}" | jq -r '.id'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to extract key fields — never dump full question/dashboard definitions
- Filter collections to exclude personal folders unless specifically needed

## Common Operations

### Question (Saved Query) Management

```bash
#!/bin/bash
echo "=== Questions Summary ==="
metabase_api GET "card" | jq '
    {
        total: length,
        native_queries: [.[] | select(.dataset_query.type == "native")] | length,
        gui_queries: [.[] | select(.dataset_query.type == "query")] | length,
        archived: [.[] | select(.archived == true)] | length
    }'

echo ""
echo "=== Most Viewed Questions ==="
metabase_api GET "card" | jq -r '
    sort_by(-.view_count) | .[:15][] |
    "\(.id)\t\(.name[0:40])\t\(.view_count) views\t\(.database_id)\t\(.collection?.name // "root")"
' | column -t

echo ""
echo "=== Questions with Errors ==="
metabase_api GET "card" | jq -r '
    .[] | select(.last_query_start != null and .cache_invalidated_at != null) |
    select(.query_average_duration > 30000) |
    "\(.id)\t\(.name[0:40])\t\(.query_average_duration / 1000 | floor)s avg"
' | column -t | head -10
```

### Dashboard Analysis

```bash
#!/bin/bash
DASHBOARD_ID="${1:?Dashboard ID required}"

echo "=== Dashboard Details ==="
metabase_api GET "dashboard/${DASHBOARD_ID}" | jq '{
    id: .id,
    name: .name,
    collection: .collection?.name,
    cards: (.dashcards | length),
    parameters: (.parameters | length),
    last_edit: .updated_at
}'

echo ""
echo "=== Dashboard Cards ==="
metabase_api GET "dashboard/${DASHBOARD_ID}" | jq -r '
    .dashcards[] | "\(.id)\t\(.card?.name // "text/heading")\t\(.card?.display // "N/A")\tsize=\(.size_x)x\(.size_y)"
' | column -t | head -20

echo ""
echo "=== Dashboard Parameters ==="
metabase_api GET "dashboard/${DASHBOARD_ID}" | jq -r '
    .parameters[] | "\(.name)\t\(.type)\t\(.default // "no default")"
' | column -t
```

### Database Connection Health

```bash
#!/bin/bash
echo "=== Database Connection Status ==="
metabase_api GET "database" | jq -r '
    .data[] | "\(.id)\t\(.name)\t\(.engine)\t\(.details.host // "N/A")\t\(.details.port // "N/A")"
' | column -t

echo ""
echo "=== Sync Status ==="
metabase_api GET "database" | jq -r '
    .data[] | "\(.name)\tinitial_sync=\(.initial_sync_status)\tmetadata_sync=\(.metadata_sync_schedule // "auto")"
' | column -t

echo ""
echo "=== Database Tables ==="
DB_ID="${1:-}"
if [ -n "$DB_ID" ]; then
    metabase_api GET "database/${DB_ID}/metadata" | jq -r '
        .tables[] | select(.active == true) | "\(.schema // "public")\t\(.name)\t\(.rows // "?")\t\(.entity_type // "?")"
    ' | column -t | head -20
fi
```

### Pulse and Subscription Management

```bash
#!/bin/bash
echo "=== Active Pulses ==="
metabase_api GET "pulse" | jq -r '
    .[] | select(.archived == false) | "\(.id)\t\(.name)\t\(.channels[0]?.channel_type // "?")\t\(.cards | length) cards"
' | column -t | head -15

echo ""
echo "=== Pulse Schedules ==="
metabase_api GET "pulse" | jq -r '
    .[] | select(.archived == false) |
    "\(.name)\t\(.channels[0]?.schedule_type // "?")\t\(.channels[0]?.schedule_hour // "?")\t\(.channels[0]?.recipients | length // 0) recipients"
' | column -t | head -15

echo ""
echo "=== Dashboard Subscriptions ==="
DASHBOARD_ID="${1:-}"
if [ -n "$DASHBOARD_ID" ]; then
    metabase_api GET "dashboard/${DASHBOARD_ID}/subscriptions" | jq -r '
        .[] | "\(.id)\t\(.channels[0]?.channel_type // "?")\t\(.channels[0]?.schedule_type // "?")"
    ' | column -t
fi
```

### User Activity and Audit

```bash
#!/bin/bash
echo "=== Active Users ==="
metabase_api GET "user?status=active&limit=20" | jq -r '
    .data[] | "\(.id)\t\(.common_name)\t\(.email)\t\(.last_login[0:10] // "never")\t\(if .is_superuser then "ADMIN" else "USER" end)"
' | column -t | head -20

echo ""
echo "=== Recent Query Executions ==="
metabase_api GET "dataset" 2>/dev/null
metabase_api GET "activity?limit=20" | jq -r '
    .[] | select(.topic | test("query|card")) |
    "\(.timestamp[0:16])\t\(.topic)\t\(.user?.common_name // "?")\t\(.details?.name // .model_id // "?")"
' | column -t | head -15
```

## Output Format

Present results as a structured report:
```
Managing Metabase Report
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

- **Session tokens**: Metabase sessions expire (default 14 days) — re-authenticate via `POST /api/session` if getting 401
- **Card vs Question**: In the API, "card" is the internal name for what the UI calls a "question" or "saved question"
- **Native vs GUI queries**: `dataset_query.type` is "native" for SQL or "query" for GUI builder — native queries bypass Metabase's query builder
- **Collection permissions**: Collections have group-based permissions — API results depend on the session user's access
- **Database sync**: Metabase syncs database metadata periodically — new tables may not appear until sync completes
- **Query duration**: `query_average_duration` is in milliseconds, not seconds — divide by 1000
- **Pulse deprecation**: Pulses are being replaced by Dashboard Subscriptions in newer versions — check both
- **Embedding**: Embedded questions/dashboards use signed JWTs — different auth flow than API tokens
- **Caching**: Metabase caches query results — stale results may be from cache, configurable per-database
