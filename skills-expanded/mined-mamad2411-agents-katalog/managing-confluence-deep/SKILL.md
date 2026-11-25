---
name: managing-confluence-deep
description: |
  Use when working with Confluence Deep — deep Confluence management covering
  spaces, pages, content analytics, permissions, and workspace health. Use when
  performing deep audits of Confluence usage, analyzing content freshness,
  reviewing space permissions, or assessing documentation coverage across an
  Atlassian Confluence instance.
connection_type: atlassian
preload: false
---

# Managing Confluence (Deep)

Deep Confluence workspace analysis covering content health, permissions, and usage patterns via the Confluence REST API.

## Discovery Phase

```bash
#!/bin/bash
CONFLUENCE_BASE="$CONFLUENCE_URL/wiki/api/v2"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_URL/wiki/rest/api/user/current" \
  | jq '{accountId, displayName, email}'

echo ""
echo "=== Spaces Overview ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_BASE/spaces?limit=30" \
  | jq -r '.results[] | "\(.id)\t\(.key)\t\(.name[0:30])\t\(.type)\t\(.status)"' | column -t

echo ""
echo "=== Recently Modified Pages ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_URL/wiki/rest/api/content?type=page&orderby=lastmodified%20desc&limit=15&expand=version,space" \
  | jq -r '.results[] | "\(.space.key)\t\(.title[0:40])\t\(.version.when[0:10])\t\(.version.by.displayName)"' | column -t

echo ""
echo "=== Content Counts by Space ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_URL/wiki/rest/api/content?type=page&limit=0" \
  | jq '{total_pages: .size}'
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_URL/wiki/rest/api/content?type=blogpost&limit=0" \
  | jq '{total_blogposts: .size}'
```

## Analysis Phase

```bash
#!/bin/bash
CONFLUENCE_BASE="$CONFLUENCE_URL/wiki/rest/api"
SPACE_KEY="${1:?Space key required}"

echo "=== Space Details ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_BASE/space/$SPACE_KEY?expand=description.plain,homepage" \
  | jq '{key, name, type, status, description: .description.plain.value[0:100], homepage: .homepage.title}'

echo ""
echo "=== Pages in Space (by last modified) ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_BASE/content?spaceKey=$SPACE_KEY&type=page&orderby=lastmodified%20desc&limit=20&expand=version" \
  | jq -r '.results[] | "\(.title[0:40])\t\(.version.when[0:10])\t\(.version.number) revisions\t\(.version.by.displayName)"' | column -t

echo ""
echo "=== Stale Pages (no update in 90+ days) ==="
CUTOFF=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d "-90 days" +%Y-%m-%d)
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_BASE/content?spaceKey=$SPACE_KEY&type=page&limit=50&expand=version" \
  | jq -r --arg cutoff "$CUTOFF" \
    '.results[] | select(.version.when[0:10] < $cutoff) | "\(.title[0:40])\t\(.version.when[0:10])\tSTALE"' \
  | column -t | head -15

echo ""
echo "=== Space Permissions ==="
curl -s -H "Authorization: Bearer $ATLASSIAN_TOKEN" \
  "$CONFLUENCE_BASE/space/$SPACE_KEY?expand=permissions" \
  | jq '[.permissions[] | {operation: .operation.operation, target: .operation.targetType, subjects: (.subjects // {} | keys)}] | unique_by(.operation) | .[:10]'
```

## Output Format

```
CONFLUENCE DEEP HEALTH
Instance:       [url]
Total Spaces:   [count] (global: [n], personal: [n])
Total Pages:    [count]
Total Blogs:    [count]

SPACE HEALTH REPORT: [SPACE_KEY]
Pages:          [count]
Stale Pages:    [count] (90+ days without update)
Avg Revisions:  [avg]
Top Contributor:[name]

CONTENT FRESHNESS
Updated <7d:    [count]
Updated <30d:   [count]
Updated <90d:   [count]
Stale (90d+):   [count]
```

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

