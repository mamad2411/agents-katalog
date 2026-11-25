---
name: managing-contentful
description: |
  Use when working with Contentful — contentful headless CMS management covering
  space and environment inventory, content type analysis, entry and asset
  monitoring, locale configuration, webhook tracking, API key auditing, and
  usage quota monitoring. Use when reviewing content models, investigating
  publishing issues, monitoring API usage, or auditing space access.
connection_type: contentful
preload: false
---

# Contentful Management Skill

Manage and monitor Contentful spaces, content types, entries, assets, and API usage.

## MANDATORY: Discovery-First Pattern

**Always list spaces and environments before querying specific content types or entries.**

### Phase 1: Discovery

```bash
#!/bin/bash

CF_API="https://api.contentful.com"

cf_api() {
    curl -s -H "Authorization: Bearer $CONTENTFUL_MANAGEMENT_TOKEN" \
         -H "Content-Type: application/json" \
         "${CF_API}/${1}"
}

echo "=== Spaces ==="
cf_api "spaces" | jq -r '
    .items[] |
    "\(.sys.id)\t\(.name)"
' | column -t

echo ""
SPACE_ID="${CONTENTFUL_SPACE_ID}"
echo "=== Environments (Space: $SPACE_ID) ==="
cf_api "spaces/${SPACE_ID}/environments" | jq -r '
    .items[] |
    "\(.sys.id)\t\(.name)\t\(.sys.status.sys.id)"
' | column -t

echo ""
ENV_ID="${CONTENTFUL_ENV:-master}"
echo "=== Content Types ==="
cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/content_types" | jq -r '
    .items[] |
    "\(.sys.id)\t\(.name)\t\(.fields | length) fields\t\(.displayField)"
' | column -t | head -25

echo ""
echo "=== Locales ==="
cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/locales" | jq -r '
    .items[] |
    "\(.code)\t\(.name)\t\(.default)\t\(.fallbackCode // "none")"
' | column -t
```

### Phase 2: Analysis

```bash
#!/bin/bash

SPACE_ID="${CONTENTFUL_SPACE_ID}"
ENV_ID="${CONTENTFUL_ENV:-master}"

echo "=== Entry Counts by Content Type ==="
cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/content_types" | jq -r '.items[].sys.id' | while read ctid; do
    COUNT=$(cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/entries?content_type=${ctid}&limit=0" | jq '.total')
    echo -e "${ctid}\t${COUNT} entries"
done | column -t | head -20

echo ""
echo "=== Draft Entries ==="
cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/entries?sys.publishedAt[exists]=false&limit=10" | jq -r '
    .items[] |
    "\(.sys.contentType.sys.id)\t\(.sys.id)\tDRAFT\t\(.sys.updatedAt[:10])"
' | column -t

echo ""
echo "=== Assets ==="
cf_api "spaces/${SPACE_ID}/environments/${ENV_ID}/assets?limit=1" | jq '{total_assets: .total}'

echo ""
echo "=== Webhooks ==="
cf_api "spaces/${SPACE_ID}/webhooks" | jq -r '
    .items[] |
    "\(.sys.id)\t\(.name)\t\(.active)\t\(.url[:50])"
' | column -t | head -15

echo ""
echo "=== API Keys ==="
cf_api "spaces/${SPACE_ID}/api_keys" | jq -r '
    .items[] |
    "\(.sys.id)\t\(.name)\t\(.environments | length) envs"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `limit=0` to get counts without fetching entries
- Never dump full entry content -- extract sys metadata and field names

## Output Format

Present results as a structured report:
```
Managing Contentful Report
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

- **Environment aliasing**: Master alias can point to different environments -- check alias target
- **Rate limits**: Management API has strict rate limits (7 req/s) -- batch requests carefully
- **Content type changes**: Field deletions require removing content first -- migrations must be ordered
- **Draft vs published**: Entries can be changed but not published -- compare sys.publishedVersion
- **Webhook ordering**: Webhooks do not guarantee delivery order -- use sys.version for consistency
- **API key environments**: Delivery API keys are scoped to specific environments
- **Rich text**: Rich text fields contain embedded entry/asset references -- broken links cause render failures
