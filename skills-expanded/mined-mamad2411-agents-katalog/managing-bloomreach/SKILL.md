---
name: managing-bloomreach
description: |
  Use when working with Bloomreach — bloomreach commerce search and
  merchandising platform management including catalog feeds, search
  configuration, autosuggest, category pages, SEO, A/B testing, pixel tracking,
  and recommendation widgets. Covers search relevance, catalog health, widget
  performance, and content personalization metrics.
connection_type: bloomreach
preload: false
---

# Bloomreach Management Skill

Monitor and manage Bloomreach commerce experience and search platform.

## MANDATORY: Discovery-First Pattern

**Always discover account configuration and catalogs before querying search or analytics.**

### Phase 1: Discovery

```bash
#!/bin/bash
BR_API="https://api.connect.bloomreach.com/dataconnect/api/v1"
BR_SEARCH="https://core.dxpapi.com/api/v1/core"
AUTH="Authorization: Bearer ${BLOOMREACH_API_KEY}"
ACCT="${BLOOMREACH_ACCOUNT_ID}"
DOMAIN="${BLOOMREACH_DOMAIN_KEY}"

echo "=== Account Configuration ==="
curl -s -H "$AUTH" "$BR_API/accounts/$ACCT" | \
  jq -r '"Account: \(.account_id)\nDomain: \(.domain_key)\nStatus: \(.status)"' 2>/dev/null || echo "Check via Bloomreach Dashboard"

echo ""
echo "=== Catalog Status ==="
curl -s -H "$AUTH" "$BR_API/accounts/$ACCT/catalogs" | \
  jq -r '.[] | "\(.catalog_name) | Products: \(.product_count) | Last Feed: \(.last_feed_time) | Status: \(.status)"' 2>/dev/null || echo "Check catalog feeds via dashboard"

echo ""
echo "=== Search Health Check ==="
curl -s "$BR_SEARCH/?account_id=$ACCT&auth_key=${BLOOMREACH_AUTH_KEY}&domain_key=$DOMAIN&request_type=search&search_type=keyword&q=test&rows=1&fl=pid,title" | \
  jq -r '"Search API: \(if .response then "OK (\(.response.numFound) results)" else "Error" end)"'

echo ""
echo "=== Autosuggest Health ==="
curl -s "$BR_SEARCH/?account_id=$ACCT&auth_key=${BLOOMREACH_AUTH_KEY}&domain_key=$DOMAIN&request_type=suggest&q=sh&rows=5" | \
  jq -r '"Autosuggest: \(if .response or .suggestionGroups then "OK" else "Error" end)"'

echo ""
echo "=== Widgets ==="
curl -s -H "$AUTH" "$BR_API/accounts/$ACCT/widgets" | \
  jq -r '.[] | "\(.widget_id) | Type: \(.type) | Active: \(.active)"' 2>/dev/null || echo "Check widgets via dashboard"
```

**Phase 1 outputs:** Account config, catalog status, search health, widgets

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Search Performance ==="
curl -s "$BR_SEARCH/?account_id=$ACCT&auth_key=${BLOOMREACH_AUTH_KEY}&domain_key=$DOMAIN&request_type=search&search_type=keyword&q=shoes&rows=5&fl=pid,title,price,thumb_image&stats.field=price" | \
  jq -r '"Results: \(.response.numFound)\nFacets: \(.facet_counts.facet_fields | keys | length)\nPrice Range: \(.stats.stats_fields.price.min // "N/A") - \(.stats.stats_fields.price.max // "N/A")"'

echo ""
echo "=== Category Browse ==="
curl -s "$BR_SEARCH/?account_id=$ACCT&auth_key=${BLOOMREACH_AUTH_KEY}&domain_key=$DOMAIN&request_type=search&search_type=category&q=&rows=1" | \
  jq -r '"Category Browse: \(if .response then "OK (\(.response.numFound) items)" else "Error" end)"'

echo ""
echo "=== Feed History ==="
curl -s -H "$AUTH" "$BR_API/accounts/$ACCT/catalogs/${BLOOMREACH_CATALOG}/feeds" | \
  jq -r '.[:5] | .[] | "\(.feed_id) | Status: \(.status) | Products: \(.product_count) | \(.completed_at)"' 2>/dev/null || echo "Check feed history via dashboard"

echo ""
echo "=== Ranking Rules ==="
curl -s -H "$AUTH" "$BR_API/accounts/$ACCT/ranking-rules" | \
  jq -r '.[] | "\(.name) | Type: \(.type) | Active: \(.active)"' 2>/dev/null || echo "Check ranking rules via dashboard"

echo ""
echo "=== Pixel Tracking Check ==="
curl -s -o /dev/null -w "Pixel Endpoint: %{http_code} (%{time_total}s)\n" \
  "https://p.brsrvr.com/pix.gif?acct_id=$ACCT&test=1"
```

## Output Format

```
BLOOMREACH STATUS
=================
Account: {account_id} ({domain})
Catalog: {products} products | Last Feed: {time} ({status})
Search API: {status}
Autosuggest: {status}
Widgets: {active}/{total}
Ranking Rules: {count}
Pixel Tracking: {status}
Issues: {list_of_warnings}
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

## Common Pitfalls

- **auth_key vs API key**: Search uses auth_key parameter; management uses Bearer token
- **Domain key**: Multi-site setups require correct domain_key per site
- **Catalog feeds**: JSON feed format is strict — validate before submission
- **Pixel tracking**: Required for analytics and personalization — verify implementation
- **SDK version**: Bloomreach has Discovery (search) and Engagement (CDP) — different APIs
