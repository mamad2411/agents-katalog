---
name: managing-baserow
description: |
  Use when working with Baserow — baserow open-source database platform
  management covering workspace organization, database and table inventory,
  field configuration analysis, view management, webhook monitoring, and user
  access auditing. Use when reviewing database structures, investigating API
  integration issues, monitoring webhook deliveries, or auditing workspace
  permissions.
connection_type: baserow
preload: false
---

# Baserow Management Skill

Manage and monitor Baserow workspaces, databases, tables, and integrations.

## MANDATORY: Discovery-First Pattern

**Always list workspaces and databases before querying specific tables.**

### Phase 1: Discovery

```bash
#!/bin/bash

BASEROW_API="${BASEROW_URL}/api"

baserow_api() {
    curl -s -H "Authorization: Token $BASEROW_API_TOKEN" \
         -H "Content-Type: application/json" \
         "${BASEROW_API}/${1}"
}

echo "=== Workspaces ==="
baserow_api "workspaces/" | jq -r '
    .[] |
    "\(.id)\t\(.name)\t\(.permissions)"
' | column -t

echo ""
echo "=== Databases ==="
baserow_api "applications/" | jq -r '
    .[] |
    select(.type == "database") |
    "\(.id)\t\(.name)\t\(.workspace.id)\t\(.tables | length) tables"
' | column -t | head -20

echo ""
echo "=== Tables (all databases) ==="
baserow_api "applications/" | jq -r '
    .[] | select(.type == "database") |
    .name as $db | .tables[]? |
    "\($db)\t\(.id)\t\(.name)\t\(.order)"
' | column -t | head -30
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Table Fields Summary ==="
baserow_api "applications/" | jq -r '.[].tables[]?.id' | head -10 | while read tid; do
    baserow_api "database/fields/table/${tid}/" | jq -r --arg tid "$tid" '
        . as $fields | {
            table_id: $tid,
            field_count: ($fields | length),
            link_fields: [$fields[] | select(.type == "link_row")] | length,
            formula_fields: [$fields[] | select(.type == "formula")] | length
        }
    '
done | head -20

echo ""
echo "=== Views ==="
baserow_api "applications/" | jq -r '.[].tables[]?.id' | head -10 | while read tid; do
    baserow_api "database/views/table/${tid}/" | jq -r --arg tid "$tid" '
        .[]? |
        "\($tid)\t\(.id)\t\(.name)\t\(.type)\t\(.public)"
    '
done | column -t | head -20

echo ""
echo "=== Webhooks ==="
baserow_api "applications/" | jq -r '.[].tables[]?.id' | head -10 | while read tid; do
    baserow_api "database/webhooks/table/${tid}/" 2>/dev/null | jq -r --arg tid "$tid" '
        .[]? |
        "\($tid)\t\(.name)\t\(.active)\t\(.events | join(","))"
    '
done | column -t | head -15

echo ""
echo "=== Public Views (security review) ==="
baserow_api "applications/" | jq -r '.[].tables[]?.id' | head -10 | while read tid; do
    baserow_api "database/views/table/${tid}/" | jq -r --arg tid "$tid" '
        .[]? | select(.public == true) |
        "\($tid)\t\(.name)\tPUBLIC\t\(.public_view_has_password)"
    '
done | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Filter by workspace or database
- Never dump full row data -- extract schema and view metadata

## Output Format

Present results as a structured report:
```
Managing Baserow Report
═══════════════════════
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

- **Public views**: Public views expose data without authentication -- audit regularly
- **Link row fields**: Link fields create bidirectional relationships -- deleting one side affects the other
- **Formula dependencies**: Formula fields depend on other fields -- field deletion can break formulas
- **Webhook retries**: Failed webhooks are retried with exponential backoff but eventually dropped
- **Row-level permissions**: Premium feature -- free tier has workspace-level permissions only
- **API rate limits**: Self-hosted has no default rate limiting -- configure reverse proxy limits
