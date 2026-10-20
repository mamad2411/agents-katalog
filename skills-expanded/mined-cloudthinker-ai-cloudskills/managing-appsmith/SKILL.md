---
name: managing-appsmith
description: |
  Use when working with Appsmith — appsmith low-code platform management
  covering application inventory, workspace organization, datasource health,
  page and widget analysis, and user access auditing. Use when reviewing
  internal tool configurations, investigating datasource connectivity,
  monitoring application deployments, or auditing workspace permissions.
connection_type: appsmith
preload: false
---

# Appsmith Management Skill

Manage and monitor Appsmith applications, workspaces, datasources, and deployments.

## MANDATORY: Discovery-First Pattern

**Always list workspaces and applications before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

APPSMITH_API="${APPSMITH_URL}/api/v1"

appsmith_api() {
    curl -s -H "Authorization: Bearer $APPSMITH_API_KEY" \
         -H "Content-Type: application/json" \
         "${APPSMITH_API}/${1}"
}

echo "=== Workspaces ==="
appsmith_api "workspaces" | jq -r '
    .data[] |
    "\(.id)\t\(.name)\t\(.userPermissions | length) perms"
' | column -t

echo ""
echo "=== Applications ==="
appsmith_api "applications" | jq -r '
    .data[] |
    "\(.id)\t\(.name)\t\(.workspaceId)\t\(.isPublic // false)"
' | column -t | head -30

echo ""
echo "=== Datasources ==="
appsmith_api "datasources" | jq -r '
    .data[] |
    "\(.id)\t\(.name)\t\(.pluginName)\t\(.isValid)"
' | column -t | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Invalid Datasources ==="
appsmith_api "datasources" | jq -r '
    .data[] |
    select(.isValid == false) |
    "\(.id)\t\(.name)\t\(.pluginName)\tINVALID\t\(.invalids | join("; "))"
' | column -t

echo ""
echo "=== Application Pages ==="
appsmith_api "applications" | jq -r '.data[].id' | head -10 | while read aid; do
    appsmith_api "pages?applicationId=${aid}" | jq -r --arg aid "$aid" '
        .data[]? |
        "\($aid)\t\(.id)\t\(.name)\t\(.isDefault)"
    '
done | column -t | head -20

echo ""
echo "=== App Summary ==="
appsmith_api "applications" | jq '{
    total_apps: (.data | length),
    public_apps: [.data[] | select(.isPublic == true)] | length,
    private_apps: [.data[] | select(.isPublic != true)] | length
}'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Filter applications by workspace
- Never dump full page/widget DSL -- extract page names and widget counts

## Output Format

Present results as a structured report:
```
Managing Appsmith Report
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

- **Datasource validity**: Invalid datasources prevent queries from running -- fix credentials or connection strings
- **Git sync**: Applications with Git sync can have merge conflicts -- check sync status
- **Environment configs**: Datasource configs differ between environments -- verify the correct env
- **Widget bindings**: Broken JS bindings in widgets cause runtime errors -- not visible via API
- **Deploy vs edit**: Published app differs from edit mode -- ensure latest changes are deployed
