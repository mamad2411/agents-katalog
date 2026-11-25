---
name: managing-google-analytics
description: |
  Use when working with Google Analytics — google Analytics 4 management —
  monitor property configuration, event streams, user metrics, conversions, and
  audience data. Use when reviewing traffic trends, inspecting event setup,
  auditing conversion goals, or analyzing user acquisition.
connection_type: google-analytics
preload: false
---

# Managing Google Analytics

Manage and monitor Google Analytics 4 — properties, data streams, events, conversions, and user metrics.

## Discovery Phase

```bash
#!/bin/bash

GA_API="https://analyticsadmin.googleapis.com/v1beta"
GA_DATA="https://analyticsdata.googleapis.com/v1beta"
AUTH="Authorization: Bearer $(gcloud auth print-access-token)"

echo "=== Account Summary ==="
curl -s -H "$AUTH" "$GA_API/accountSummaries" \
  | jq -r '.accountSummaries[] | .propertySummaries[] | [.property, .displayName] | @tsv' | column -t | head -10

echo ""
echo "=== Property Details ==="
curl -s -H "$AUTH" "$GA_API/properties/$GA_PROPERTY_ID" \
  | jq '{displayName: .displayName, timeZone: .timeZone, currencyCode: .currencyCode, industryCategory: .industryCategory}'

echo ""
echo "=== Data Streams ==="
curl -s -H "$AUTH" "$GA_API/properties/$GA_PROPERTY_ID/dataStreams" \
  | jq -r '.dataStreams[] | [.name, .type, .displayName, .webStreamData.defaultUri // .androidAppStreamData.packageName // "N/A"] | @tsv' | column -t | head -10

echo ""
echo "=== Conversion Events ==="
curl -s -H "$AUTH" "$GA_API/properties/$GA_PROPERTY_ID/conversionEvents" \
  | jq -r '.conversionEvents[] | [.eventName, .createTime, .deletable] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

GA_DATA="https://analyticsdata.googleapis.com/v1beta"
AUTH="Authorization: Bearer $(gcloud auth print-access-token)"

echo "=== Active Users & Sessions (7 days) ==="
curl -s -H "$AUTH" -X POST "$GA_DATA/properties/$GA_PROPERTY_ID:runReport" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "date"}],
    "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
    "orderBys": [{"dimension": {"dimensionName": "date"}}]
  }' | jq -r '.rows[] | [.dimensionValues[0].value, .metricValues[0].value, .metricValues[1].value, .metricValues[2].value] | @tsv' | column -t

echo ""
echo "=== Top Pages (30 days) ==="
curl -s -H "$AUTH" -X POST "$GA_DATA/properties/$GA_PROPERTY_ID:runReport" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "pagePath"}],
    "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
    "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": true}],
    "limit": 10
  }' | jq -r '.rows[] | [.dimensionValues[0].value, .metricValues[0].value, .metricValues[1].value] | @tsv' | column -t

echo ""
echo "=== Traffic Sources ==="
curl -s -H "$AUTH" -X POST "$GA_DATA/properties/$GA_PROPERTY_ID:runReport" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "sessionSource"}],
    "metrics": [{"name": "sessions"}, {"name": "activeUsers"}, {"name": "bounceRate"}],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}],
    "limit": 10
  }' | jq -r '.rows[] | [.dimensionValues[0].value, .metricValues[0].value, .metricValues[1].value, .metricValues[2].value] | @tsv' | column -t

echo ""
echo "=== Realtime ==="
curl -s -H "$AUTH" -X POST "$GA_DATA/properties/$GA_PROPERTY_ID:runRealtimeReport" \
  -H "Content-Type: application/json" \
  -d '{"metrics": [{"name": "activeUsers"}]}' \
  | jq '{activeUsersNow: .rows[0].metricValues[0].value}'
```

## Output Format

```
PROPERTY
Name:       <property-name>
Timezone:   <timezone>
Currency:   <currency>

DAILY METRICS (7d)
Date          Users    Sessions   Pageviews
<date>        <n>      <n>        <n>

TOP PAGES (30d)
Page Path            Pageviews   Users
<path>               <n>         <n>

TRAFFIC SOURCES (30d)
Source               Sessions   Users    Bounce Rate
<source>             <n>        <n>      <pct>

REALTIME
Active Users Now:    <n>
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

