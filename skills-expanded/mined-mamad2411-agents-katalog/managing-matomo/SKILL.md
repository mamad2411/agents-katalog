---
name: managing-matomo
description: |
  Use when working with Matomo — matomo analytics management — monitor site
  traffic, visitor behavior, goals, segments, and reporting. Use when reviewing
  web analytics, inspecting referrer data, checking goal completions, or
  auditing tracking configuration.
connection_type: matomo
preload: false
---

# Managing Matomo

Manage and monitor Matomo web analytics — visitors, pages, referrers, goals, and site configuration.

## Discovery Phase

```bash
#!/bin/bash

MATOMO_API="$MATOMO_URL/index.php"
TOKEN="token_auth=$MATOMO_TOKEN"

echo "=== Sites ==="
curl -s "$MATOMO_API?module=API&method=SitesManager.getAllSites&format=json&$TOKEN" \
  | jq -r '.[] | [.idsite, .name, .main_url, .type] | @tsv' | column -t | head -10

echo ""
echo "=== Goals ==="
curl -s "$MATOMO_API?module=API&method=Goals.getGoals&idSite=$MATOMO_SITE_ID&format=json&$TOKEN" \
  | jq -r '.[] | [.idgoal, .name, .pattern, .revenue] | @tsv' | column -t | head -10

echo ""
echo "=== Segments ==="
curl -s "$MATOMO_API?module=API&method=SegmentEditor.getAll&format=json&$TOKEN" \
  | jq -r '.[] | [.idsegment, .name, .definition] | @tsv' | column -t | head -10

echo ""
echo "=== Tracking Configuration ==="
curl -s "$MATOMO_API?module=API&method=SitesManager.getSiteFromId&idSite=$MATOMO_SITE_ID&format=json&$TOKEN" \
  | jq '{name: .[0].name, timezone: .[0].timezone, currency: .[0].currency, ecommerce: .[0].ecommerce}'
```

## Analysis Phase

```bash
#!/bin/bash

MATOMO_API="$MATOMO_URL/index.php"
TOKEN="token_auth=$MATOMO_TOKEN"
SITE="idSite=$MATOMO_SITE_ID"
PERIOD="period=day&date=last7"

echo "=== Visits Summary (7 days) ==="
curl -s "$MATOMO_API?module=API&method=VisitsSummary.get&$SITE&$PERIOD&format=json&$TOKEN" \
  | jq -r 'to_entries[] | .value | [.nb_visits, .nb_uniq_visitors, .bounce_rate, .avg_time_on_site] | @tsv' | column -t

echo ""
echo "=== Top Pages ==="
curl -s "$MATOMO_API?module=API&method=Actions.getPageUrls&$SITE&period=range&date=last30&format=json&$TOKEN&flat=1&filter_limit=10" \
  | jq -r '.[] | [.label, .nb_visits, .nb_hits, .bounce_rate] | @tsv' | column -t

echo ""
echo "=== Top Referrers ==="
curl -s "$MATOMO_API?module=API&method=Referrers.getWebsites&$SITE&period=range&date=last30&format=json&$TOKEN&filter_limit=10" \
  | jq -r '.[] | [.label, .nb_visits, .nb_actions] | @tsv' | column -t

echo ""
echo "=== Goal Conversions ==="
curl -s "$MATOMO_API?module=API&method=Goals.get&$SITE&period=range&date=last30&format=json&$TOKEN" \
  | jq '{conversions: .nb_conversions, revenue: .revenue, conversion_rate: .conversion_rate}'

echo ""
echo "=== Live Visitors (last 10) ==="
curl -s "$MATOMO_API?module=API&method=Live.getLastVisitsDetails&$SITE&format=json&$TOKEN&filter_limit=5" \
  | jq -r '.[] | [.visitIp, .referrerName // "direct", .actions, .visitDurationPretty, .country] | @tsv' | column -t
```

## Output Format

```
VISITS (7 days)
Visits     Unique Visitors   Bounce Rate   Avg Duration
<n>        <n>               <pct>%        <duration>

TOP PAGES
Page              Visits    Hits    Bounce Rate
<url>             <n>       <n>     <pct>%

TOP REFERRERS
Website           Visits    Actions
<referrer>        <n>       <n>

GOALS (30d)
Conversions:      <n>
Revenue:          <amount>
Conversion Rate:  <pct>%
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

