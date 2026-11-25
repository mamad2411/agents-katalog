---
name: managing-ivanti
description: |
  Use when working with Ivanti — ivanti Neurons for ITSM covering service
  request management, IT asset management, workflow automation, and self-service
  portal configuration. Use when creating and routing service requests, tracking
  IT hardware and software assets, configuring automated workflows for common IT
  tasks, or managing the employee self-service portal and service catalog.
connection_type: ivanti
preload: false
---

# Ivanti Neurons ITSM Management Skill

Manage and analyze Ivanti service requests, assets, and automation workflows.

## API Conventions

### Authentication
All API calls use API key or OAuth token — injected automatically via header.

### Base URL
`https://{{tenant}}.ivanticloud.com/api/odata`

### Core Helper Function

```bash
#!/bin/bash

ivanti_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: rest_api_key=$IVANTI_API_KEY" \
            -H "Content-Type: application/json" \
            "${IVANTI_URL}/api/odata${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: rest_api_key=$IVANTI_API_KEY" \
            -H "Content-Type: application/json" \
            "${IVANTI_URL}/api/odata${endpoint}"
    fi
}
```

## Common Operations

### Service Request Management

```bash
#!/bin/bash
echo "=== Open Service Requests ==="
ivanti_api GET "/businessobject/incidents?\$filter=Status ne 'Closed'&\$orderby=Priority asc&\$top=25&\$select=IncidentNumber,Subject,Priority,Status,Owner,CreatedDateTime" \
    | jq -r '.value[] | "\(.IncidentNumber)\t\(.Priority)\t\(.Status)\t\(.Subject[0:60])"' \
    | column -t

echo ""
echo "=== Requests by Category ==="
ivanti_api GET "/businessobject/incidents?\$filter=Status ne 'Closed'&\$top=200&\$select=Category" \
    | jq -r '[.value[].Category] | group_by(.) | map({category: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.category // "Uncategorized"): \(.count)"'
```

### Asset Management

```bash
#!/bin/bash
echo "=== IT Assets Summary ==="
ivanti_api GET "/businessobject/CI?\$top=200&\$select=AssetType,Status,Name" \
    | jq -r '[.value[].AssetType] | group_by(.) | map({type: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.type): \(.count)"'

echo ""
echo "=== Recently Added Assets ==="
ivanti_api GET "/businessobject/CI?\$orderby=CreatedDateTime desc&\$top=15&\$select=Name,AssetType,Status,Owner,CreatedDateTime" \
    | jq -r '.value[] | "\(.Name)\t\(.AssetType)\t\(.Status)\t\(.CreatedDateTime[0:10])"' \
    | column -t
```

### Workflow Automation

```bash
#!/bin/bash
echo "=== Active Workflows ==="
ivanti_api GET "/businessobject/Frs_WorkflowInstance?\$filter=Status eq 'Active'&\$top=20&\$select=WorkflowName,Status,CreatedDateTime,BusinessObjectId" \
    | jq -r '.value[] | "\(.WorkflowName)\t\(.Status)\t\(.CreatedDateTime[0:16])"' \
    | column -t

echo ""
echo "=== Failed Workflows (last 7 days) ==="
SINCE=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
ivanti_api GET "/businessobject/Frs_WorkflowInstance?\$filter=Status eq 'Failed' and CreatedDateTime ge ${SINCE}&\$top=15" \
    | jq -r '.value[] | "\(.WorkflowName)\t\(.CreatedDateTime[0:16])\t\(.ErrorMessage[0:40] // "-")"' \
    | column -t
```

## Output Format

Present results as a structured report:
```
Managing Ivanti Report
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

- **OData syntax**: Uses OData v4 query syntax — `$filter`, `$orderby`, `$top`, `$select`, `$expand`
- **Business object names**: Object names are case-sensitive — use exact names from schema
- **API key format**: Header format is `Authorization: rest_api_key=XXXXX` — not Bearer token
- **Rate limits**: Cloud tenants have configurable rate limits — check response headers
- **Pagination**: Use `$skip` and `$top` for pagination — default page size may vary
- **Relationships**: Use `$expand` to include related objects in a single query
- **Date filtering**: Use ISO 8601 format with OData comparison operators (`ge`, `le`, `eq`)
