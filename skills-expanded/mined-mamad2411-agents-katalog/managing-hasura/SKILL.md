---
name: managing-hasura
description: |
  Use when working with Hasura — hasura GraphQL Engine management - metadata
  inspection, remote schema configuration, event trigger management, action
  definitions, and permission analysis. Use when managing Hasura-based APIs,
  configuring data sources, analyzing event delivery, or troubleshooting
  permission issues.
connection_type: hasura
preload: false
---

# Hasura Management Skill

Manage Hasura GraphQL Engine metadata, remote schemas, event triggers, actions, and permissions.

## Core Helper Functions

```bash
#!/bin/bash

# Hasura endpoint configuration
HASURA_ENDPOINT="${HASURA_ENDPOINT:-http://localhost:8080}"
HASURA_ADMIN_SECRET="${HASURA_ADMIN_SECRET:-}"

# Hasura Metadata API wrapper
hasura_metadata() {
    local payload="$1"
    curl -s -X POST "${HASURA_ENDPOINT}/v1/metadata" \
        -H "Content-Type: application/json" \
        -H "X-Hasura-Admin-Secret: ${HASURA_ADMIN_SECRET}" \
        -d "$payload" | jq '.'
}

# Hasura Schema API wrapper
hasura_schema() {
    local payload="$1"
    curl -s -X POST "${HASURA_ENDPOINT}/v2/query" \
        -H "Content-Type: application/json" \
        -H "X-Hasura-Admin-Secret: ${HASURA_ADMIN_SECRET}" \
        -d "$payload" | jq '.'
}

# Health check
hasura_health() {
    curl -s "${HASURA_ENDPOINT}/healthz"
}
```

## MANDATORY: Discovery-First Pattern

**Always check Hasura health and inspect metadata before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Hasura Health ==="
hasura_health
echo ""

echo "=== Server Version ==="
curl -s "${HASURA_ENDPOINT}/v1/version" | jq '.'

echo ""
echo "=== Metadata Export Summary ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '{
    version: .version,
    sources: [.sources[] | {name, kind, tables_count: (.tables | length)}],
    remote_schemas: [(.remote_schemas // [])[] | .name],
    actions: [(.actions // [])[] | .name],
    custom_types: (.custom_types // {} | keys),
    cron_triggers: [(.cron_triggers // [])[] | .name],
    rest_endpoints: [(.rest_endpoints // [])[] | .name]
}'

echo ""
echo "=== Data Sources ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[.sources[] | {name, kind, tables: [.tables[] | .table.name]}]'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Export metadata and filter with jq; never dump full metadata
- Summarize permission rules rather than listing every column

## Common Operations

### Metadata Management

```bash
#!/bin/bash

echo "=== Tracked Tables ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[.sources[] | {
    source: .name,
    tables: [.tables[] | {
        name: .table.name,
        schema: (.table.schema // "public"),
        relationships: ((.array_relationships // []) + (.object_relationships // []) | length),
        permissions: {
            select: (.select_permissions // [] | length),
            insert: (.insert_permissions // [] | length),
            update: (.update_permissions // [] | length),
            delete: (.delete_permissions // [] | length)
        }
    }]
}]'

echo ""
echo "=== Relationships ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[.sources[].tables[] | {
    table: .table.name,
    object_rels: [(.object_relationships // [])[] | .name],
    array_rels: [(.array_relationships // [])[] | .name]
}] | map(select((.object_rels | length > 0) or (.array_rels | length > 0)))'

echo ""
echo "=== Metadata Inconsistencies ==="
hasura_metadata '{"type": "get_inconsistent_metadata", "args": {}}' | jq '{
    is_consistent: .is_consistent,
    inconsistent_objects: [(.inconsistent_objects // [])[] | {type, reason: .reason, definition: .definition}]
}'
```

### Remote Schema Management

```bash
#!/bin/bash

echo "=== Remote Schemas ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[(.remote_schemas // [])[] | {
    name,
    url: .definition.url,
    timeout_seconds: .definition.timeout_seconds,
    forward_client_headers: .definition.forward_client_headers,
    customization: (.definition.customization // "none")
}]'

echo ""
echo "=== Remote Schema Permissions ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[(.remote_schemas // [])[] | {
    name,
    permissions: [(.permissions // [])[] | {role: .role, allowed_types: (.definition.schema // "custom" | length)}]
}]'
```

### Event Trigger Management

```bash
#!/bin/bash

echo "=== Event Triggers ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[.sources[].tables[] | select(.event_triggers) | .event_triggers[] | {
    name,
    table: .definition,
    webhook: .webhook,
    operations: [if .insert then "INSERT" else empty end, if .update then "UPDATE" else empty end, if .delete then "DELETE" else empty end],
    retry_conf: .retry_conf,
    headers_count: (.headers // [] | length)
}]'

echo ""
echo "=== Event Delivery Status ==="
hasura_schema '{"type": "run_sql", "args": {"sql": "SELECT trigger_name, status, count(*) as count FROM hdb_catalog.event_log GROUP BY trigger_name, status ORDER BY trigger_name, status", "source": "default"}}' 2>/dev/null \
    | jq '.result' || echo "Cannot query event log directly"

echo ""
echo "=== Pending Events ==="
hasura_schema '{"type": "run_sql", "args": {"sql": "SELECT trigger_name, count(*) FROM hdb_catalog.event_log WHERE delivered = false AND error = false AND archived = false GROUP BY trigger_name", "source": "default"}}' 2>/dev/null \
    | jq '.result' || echo "Cannot query pending events directly"

echo ""
echo "=== Cron Triggers ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[(.cron_triggers // [])[] | {name, webhook, schedule: .schedule, include_in_metadata: .include_in_metadata, retry_conf: .retry_conf}]'
```

### Action Management

```bash
#!/bin/bash

echo "=== Actions ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[(.actions // [])[] | {
    name,
    kind: .definition.kind,
    handler: .definition.handler,
    type: .definition.type,
    forward_client_headers: .definition.forward_client_headers,
    permissions: [(.permissions // [])[] | .role],
    timeout: .definition.timeout
}]'

echo ""
echo "=== Custom Types ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '{
    input_objects: [(.custom_types.input_objects // [])[] | .name],
    objects: [(.custom_types.objects // [])[] | .name],
    scalars: [(.custom_types.scalars // [])[] | .name],
    enums: [(.custom_types.enums // [])[] | .name]
}'

echo ""
echo "=== REST Endpoints ==="
hasura_metadata '{"type": "export_metadata", "args": {}}' | jq '[(.rest_endpoints // [])[] | {name, url, methods: .methods, definition: .definition.query.query_name}]'
```

## Safety Rules
- **Read-only by default**: Only use `export_metadata`, `get_inconsistent_metadata`, and read queries
- **Never apply** metadata changes without explicit user confirmation
- **Never drop** tracked tables or remove data sources without confirmation
- **Never expose** admin secrets, webhook URLs with embedded credentials, or database connection strings
- **Test metadata changes**: Use `replace_metadata` with `allow_inconsistent_metadata: true` to dry-run changes

## Output Format

Present results as a structured report:
```
Managing Hasura Report
══════════════════════
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
- **Metadata inconsistencies**: Adding tables that reference missing foreign keys causes inconsistent state; always check after changes
- **Event trigger backlog**: Undelivered events accumulate in `hdb_catalog.event_log`; monitor and clean up regularly
- **Permission column sets**: Forgetting to include new columns in select permissions means roles cannot see new data
- **Remote schema conflicts**: Naming collisions between remote schema types and local types cause build failures
- **Migration ordering**: Hasura migrations must be applied in order; out-of-order migrations cause metadata conflicts
