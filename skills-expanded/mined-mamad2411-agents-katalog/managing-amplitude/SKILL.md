---
name: managing-amplitude
description: |
  Use when working with Amplitude — amplitude analytics management — monitor
  event ingestion, user activity, chart dashboards, cohorts, and data taxonomy.
  Use when reviewing event volumes, inspecting user funnels, auditing taxonomy
  health, or debugging ingestion issues.
connection_type: amplitude
preload: false
---

# Managing Amplitude

Manage and monitor Amplitude product analytics — event ingestion, taxonomy, cohorts, and dashboards.

## Discovery Phase

```bash
#!/bin/bash

AMP_API="https://amplitude.com/api/2"
AUTH="-u $AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY"

echo "=== Event Taxonomy ==="
curl -s $AUTH "$AMP_API/taxonomy/event" \
  | jq -r '.data[:20][] | [.event_type, .category // "uncategorized", .description // ""] | @tsv' | column -t

echo ""
echo "=== User Properties ==="
curl -s $AUTH "$AMP_API/taxonomy/user-property" \
  | jq -r '.data[:15][] | [.user_property, .type // "unknown"] | @tsv' | column -t

echo ""
echo "=== Cohorts ==="
curl -s $AUTH "$AMP_API/cohorts" \
  | jq -r '.cohorts[:10][] | [.id, .name, .size, .lastComputed] | @tsv' | column -t

echo ""
echo "=== Charts / Dashboards ==="
curl -s $AUTH "$AMP_API/charts" \
  | jq -r '.charts[:10][] | [.id, .name, .chartType, .lastModified] | @tsv' | column -t
```

## Analysis Phase

```bash
#!/bin/bash

AMP_API="https://amplitude.com/api/2"
AUTH="-u $AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY"
TODAY=$(date -u +%Y%m%d)
WEEK_AGO=$(date -u -v-7d +%Y%m%d 2>/dev/null || date -u -d '7 days ago' +%Y%m%d)

echo "=== Active Users (7 days) ==="
curl -s $AUTH "$AMP_API/users/active?start=$WEEK_AGO&end=$TODAY" \
  | jq -r '.data[] | [.date, .count] | @tsv' | column -t

echo ""
echo "=== Event Volume by Type (24h) ==="
curl -s $AUTH "$AMP_API/events/segmentation?e=%7B%22event_type%22%3A%22_all%22%7D&start=$WEEK_AGO&end=$TODAY&m=totals" \
  | jq -r '.data.series' | head -20

echo ""
echo "=== Event Volume Summary ==="
curl -s $AUTH "$AMP_API/events/list" \
  | jq -r '.data[:15][] | [.event_type, .totals.last_7_days // 0] | @tsv' \
  | sort -t$'\t' -k2 -rn | column -t

echo ""
echo "=== Revenue Metrics (7 days) ==="
curl -s $AUTH "$AMP_API/revenue/metrics?start=$WEEK_AGO&end=$TODAY" \
  | jq '{revenue: .data.revenue, arppu: .data.arppu, paying_users: .data.payingUsers}' 2>/dev/null
```

## Output Format

```
TAXONOMY
Event Type           Category         Description
<event-type>         <category>       <description>

ACTIVE USERS (7d)
Date          Count
<date>        <n>

EVENT VOLUME (Top Events)
Event Type           Last 7 Days
<event-type>         <count>

COHORTS
ID       Name            Size      Last Computed
<id>     <cohort-name>   <size>    <timestamp>
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

