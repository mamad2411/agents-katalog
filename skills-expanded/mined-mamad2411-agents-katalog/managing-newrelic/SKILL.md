---
name: managing-newrelic
description: |
  Use when working with Newrelic — new Relic observability platform for APM,
  infrastructure monitoring, log management, synthetic monitoring, and alerting.
  Covers NRQL query building, application performance analysis, error
  investigation, alert policy management, and dashboard overview. Use when
  querying New Relic metrics, investigating application errors, analyzing
  service performance, or managing alert conditions.
connection_type: newrelic
preload: false
---

# New Relic Monitoring Skill

Query, analyze, and manage New Relic observability data using NerdGraph (GraphQL API) and NRQL.

## API Overview

New Relic uses **NerdGraph** — a GraphQL API at `https://api.newrelic.com/graphql`.

### Core Helper Function

```bash
#!/bin/bash

nr_gql() {
    local query="$1"
    curl -s -X POST "https://api.newrelic.com/graphql" \
        -H "Api-Key: $NEW_RELIC_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"query\": $(echo "$query" | jq -Rs .)}"
}

# NRQL query shortcut
nr_nrql() {
    local nrql="$1"
    local account_id="${NEW_RELIC_ACCOUNT_ID}"
    nr_gql "{
        actor {
            account(id: ${account_id}) {
                nrql(query: $(echo "$nrql" | jq -Rs .)) {
                    results
                }
            }
        }
    }" | jq -r '.data.actor.account.nrql.results'
}
```

## MANDATORY: Discovery-First Pattern

**Always discover account IDs, applications, and entity GUIDs before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
nr_gql '{
    actor {
        accounts { id name }
        user { name email }
    }
}' | jq -r '.data.actor | "User: \(.user.name) (\(.user.email))\n" + (.accounts | .[] | "Account: \(.id) - \(.name)")' | head -10

echo ""
echo "=== Monitored Applications (APM) ==="
nr_nrql "SELECT uniques(appName) FROM Transaction SINCE 1 day ago LIMIT 50" \
    | jq -r '.[].member' | head -20

echo ""
echo "=== Infrastructure Hosts ==="
nr_nrql "SELECT uniques(hostname) FROM SystemSample SINCE 1 hour ago LIMIT 30" \
    | jq -r '.[].member' | head -20

echo ""
echo "=== Alert Policies ==="
nr_gql "{
    actor {
        account(id: ${NEW_RELIC_ACCOUNT_ID}) {
            alerts {
                policiesSearch {
                    policies { id name incidentPreference }
                }
            }
        }
    }
}" | jq -r '.data.actor.account.alerts.policiesSearch.policies[] | "\(.id)\t\(.name)\t\(.incidentPreference)"' | column -t | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — always use `LIMIT` in NRQL queries
- Use `FACET` for grouping instead of fetching raw events
- Use `TIMESERIES` only when trends are specifically needed

## NRQL Cheat Sheet

```sql
-- APM: Error rate by app
SELECT percentage(count(*), WHERE error.message IS NOT NULL) AS error_rate
FROM Transaction
WHERE appName = 'your-app'
SINCE 1 hour ago FACET appName LIMIT 10

-- APM: P95 latency
SELECT percentile(duration, 95) AS p95_sec
FROM Transaction
SINCE 1 hour ago FACET appName LIMIT 10

-- Infrastructure: CPU usage
SELECT average(cpuPercent) AS avg_cpu
FROM SystemSample
SINCE 1 hour ago FACET hostname LIMIT 20

-- Logs: Error count
SELECT count(*) FROM Log
WHERE level = 'error'
SINCE 1 hour ago FACET service.name LIMIT 10

-- Browser: Page load time
SELECT average(duration) FROM PageView
SINCE 1 hour ago FACET pageUrl LIMIT 10
```

## Common Operations

### APM Performance Dashboard

```bash
#!/bin/bash
APP="${1:-}"
SINCE="${2:-1 hour ago}"

APP_FILTER=""
[ -n "$APP" ] && APP_FILTER="WHERE appName = '${APP}'"

echo "=== Application Performance ==="
{
    nr_nrql "SELECT average(duration)*1000 AS avg_ms, percentile(duration, 95)*1000 AS p95_ms, count(*) AS requests FROM Transaction ${APP_FILTER} SINCE ${SINCE} FACET appName LIMIT 15" &
    nr_nrql "SELECT percentage(count(*), WHERE error.message IS NOT NULL) AS error_rate FROM Transaction ${APP_FILTER} SINCE ${SINCE} FACET appName LIMIT 15" &
}
wait

echo ""
echo "=== Slowest Transactions ==="
nr_nrql "SELECT average(duration)*1000 AS avg_ms, count(*) AS calls FROM Transaction ${APP_FILTER} SINCE ${SINCE} FACET name LIMIT 15" \
    | jq -r '.[] | "\(.avg_ms | . * 10 | round / 10)ms\t\(.calls)\t\(.name[0:60])"' | sort -rn | column -t | head -15

echo ""
echo "=== Top Errors ==="
nr_nrql "SELECT count(*) AS count FROM TransactionError ${APP_FILTER} SINCE ${SINCE} FACET error.class, error.message LIMIT 10" \
    | jq -r '.[] | "\(.count)\t\(.["error.class"] // "Unknown")\t\(.["error.message"][0:60] // "")"' | sort -rn | column -t | head -10
```

### Infrastructure Monitoring

```bash
#!/bin/bash
echo "=== Host CPU (top 15) ==="
nr_nrql "SELECT average(cpuPercent) AS avg_cpu, max(cpuPercent) AS max_cpu FROM SystemSample SINCE 1 hour ago FACET hostname LIMIT 15" \
    | jq -r '.[] | "\(.hostname)\tavg:\(.avg_cpu | . * 10 | round / 10)%\tmax:\(.max_cpu | . * 10 | round / 10)%"' \
    | sort -t: -k2 -rn | column -t

echo ""
echo "=== Memory Usage (top 15) ==="
nr_nrql "SELECT average(memoryUsedPercent) AS mem_pct FROM SystemSample SINCE 1 hour ago FACET hostname LIMIT 15" \
    | jq -r '.[] | "\(.hostname)\t\(.mem_pct | . * 10 | round / 10)%"' | sort -t$'\t' -k2 -rn | column -t

echo ""
echo "=== Disk Usage (>80%) ==="
nr_nrql "SELECT average(diskUsedPercent) AS disk_pct FROM StorageSample WHERE diskUsedPercent > 80 SINCE 1 hour ago FACET hostname, mountPoint LIMIT 15" \
    | jq -r '.[] | "\(.hostname)\t\(.mountPoint)\t\(.disk_pct | . * 10 | round / 10)%"' | column -t

echo ""
echo "=== Network Throughput ==="
nr_nrql "SELECT sum(receiveBytesPerSecond)/1024/1024 AS rx_mbps, sum(transmitBytesPerSecond)/1024/1024 AS tx_mbps FROM NetworkSample SINCE 1 hour ago FACET hostname LIMIT 10" \
    | jq -r '.[] | "\(.hostname)\tRX:\(.rx_mbps | . * 10 | round / 10)MB/s\tTX:\(.tx_mbps | . * 10 | round / 10)MB/s"' | column -t
```

### Alert & Incident Review

```bash
#!/bin/bash
echo "=== Open Violations ==="
nr_gql "{
    actor {
        account(id: ${NEW_RELIC_ACCOUNT_ID}) {
            alerts {
                violations(cursor: \"\") {
                    violations {
                        id duration label
                        condition { name }
                        policy { name }
                        entity { name }
                        openedAt
                    }
                }
            }
        }
    }
}" | jq -r '.data.actor.account.alerts.violations.violations[] | "\(.openedAt[0:16])\t\(.policy.name)\t\(.condition.name)\t\(.entity.name)"' \
    | column -t | head -20

echo ""
echo "=== Alert Conditions ==="
nr_gql "{
    actor {
        account(id: ${NEW_RELIC_ACCOUNT_ID}) {
            alerts {
                nrqlConditionsSearch {
                    nrqlConditions { id name enabled signal { fillOption } }
                }
            }
        }
    }
}" | jq -r '.data.actor.account.alerts.nrqlConditionsSearch.nrqlConditions[] | "\(.enabled)\t\(.name)"' \
    | sort | column -t | head -20
```

### Log Analysis

```bash
#!/bin/bash
SERVICE="${1:-}"
SINCE="${2:-1 hour ago}"

SERVICE_FILTER=""
[ -n "$SERVICE" ] && SERVICE_FILTER="WHERE service.name = '${SERVICE}'"

echo "=== Log Volume by Level ==="
nr_nrql "SELECT count(*) FROM Log ${SERVICE_FILTER} SINCE ${SINCE} FACET level LIMIT 10" \
    | jq -r '.[] | "\(.level // "unknown")\t\(.count)"' | sort -t$'\t' -k2 -rn | column -t

echo ""
echo "=== Recent Errors ==="
nr_nrql "SELECT message, timestamp FROM Log WHERE level = 'error' ${SERVICE:+AND service.name = '$SERVICE'} SINCE ${SINCE} LIMIT 20" \
    | jq -r '.[] | "\(.timestamp // "")\t\(.message[0:80] // "")"' | sort -r | column -t | head -15
```

### Service Map / Dependencies

```bash
#!/bin/bash
APP="${1:?App name required}"

echo "=== External Calls by Service ==="
nr_nrql "SELECT count(*), average(duration)*1000 AS avg_ms FROM Span WHERE appName = '${APP}' AND span.kind = 'client' SINCE 1 hour ago FACET db.system, peer.hostname LIMIT 15" \
    | jq -r '.[] | "\(.["db.system"] // .["peer.hostname"] // "unknown")\tcalls:\(.count)\tavg:\(.avg_ms | . * 10 | round / 10)ms"' | column -t

echo ""
echo "=== Database Query Performance ==="
nr_nrql "SELECT count(*), average(duration)*1000 AS avg_ms FROM Span WHERE appName = '${APP}' AND db.statement IS NOT NULL SINCE 1 hour ago FACET db.operation, db.collection LIMIT 10" \
    | jq -r '.[] | "\(.["db.operation"])\t\(.["db.collection"] // "N/A")\tcalls:\(.count)\tavg:\(.avg_ms | . * 10 | round / 10)ms"' | column -t | head -10
```

## Output Format

Present results as a structured report:
```
Managing Newrelic Report
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

- **Account ID is required**: NerdGraph queries always need `account(id: <id>)` — discover in Phase 1
- **NRQL `SINCE` format**: Use human-readable like `1 hour ago`, `3 days ago`, or absolute ISO dates
- **`LIMIT` is required**: NRQL defaults to 10 results — always explicitly set `LIMIT` up to 2000
- **Event type case sensitivity**: `Transaction`, `SystemSample`, `Log` are case-sensitive — NRQL uses them exactly as named
- **`TIMESERIES` adds rows**: Using `TIMESERIES` with long time windows can return hundreds of data points — avoid unless trending is needed
- **Span vs Transaction**: `Span` is distributed tracing data; `Transaction` is APM data — different granularity
- **EU vs US data center**: EU accounts use `api.eu.newrelic.com/graphql` — check region if getting auth errors
- **Rate limits**: NerdGraph has rate limits of 60 requests/min per API key — add `sleep 0.5` between batch calls
- **Data age**: NRQL queries data up to 90 days for paid accounts; some event types retain less
