---
name: managing-elastic-siem
description: |
  Use when working with Elastic Siem — elastic Security SIEM detection
  management, alert triage, rule configuration, and threat hunting. Covers
  security alerts, detection rules, timeline investigations, endpoint events,
  and case management. Use when investigating security alerts, reviewing
  detection rule health, analyzing threat patterns, or managing Elastic Security
  configurations.
connection_type: elastic-siem
preload: false
---

# Elastic Security SIEM Management Skill

Manage and analyze Elastic Security alerts, detection rules, cases, and threat hunting queries.

## API Conventions

### Authentication
All API calls use `Authorization: ApiKey $ELASTIC_API_KEY` -- injected automatically. Never hardcode tokens.

### Base URL
`https://$ELASTIC_HOST:9200` (Elasticsearch) and `https://$KIBANA_HOST:5601` (Kibana Security API)

### Core Helper Function

```bash
#!/bin/bash

elastic_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: ApiKey $ELASTIC_API_KEY" \
            -H "Content-Type: application/json" \
            -H "kbn-xsrf: true" \
            "${KIBANA_HOST}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: ApiKey $ELASTIC_API_KEY" \
            -H "Content-Type: application/json" \
            -H "kbn-xsrf: true" \
            "${KIBANA_HOST}${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Always filter by relevant time range to avoid huge response sets
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Open Alerts Summary ==="
elastic_api POST "/api/detection_engine/signals/search" \
    '{"query":{"bool":{"filter":[{"term":{"signal.status":"open"}}]}},"size":0,"aggs":{"by_severity":{"terms":{"field":"signal.rule.severity"}}}}' \
    | jq '{total_open: .hits.total.value, by_severity: [.aggregations.by_severity.buckets[] | {severity: .key, count: .doc_count}]}'

echo ""
echo "=== Detection Rules ==="
elastic_api GET "/api/detection_engine/rules/_find?per_page=1" \
    | jq '"Total rules: \(.total), Page: \(.page)"' -r

echo ""
echo "=== Active Cases ==="
elastic_api GET "/api/cases/_find?status=open&perPage=1" \
    | jq '"Open cases: \(.total)"' -r
```

## Analysis Phase

### Alert Triage

```bash
#!/bin/bash
echo "=== Critical/High Open Alerts (last 7 days) ==="
elastic_api POST "/api/detection_engine/signals/search" \
    '{"query":{"bool":{"filter":[{"term":{"signal.status":"open"}},{"range":{"@timestamp":{"gte":"now-7d"}}},{"terms":{"signal.rule.severity":["critical","high"]}}]}},"size":20,"sort":[{"@timestamp":"desc"}]}' \
    | jq -r '.hits.hits[]._source | "\(.["@timestamp"][0:16])\t\(.signal.rule.severity)\t\(.signal.rule.name[0:50])\t\(.host.name // "N/A")"' \
    | column -t

echo ""
echo "=== Alerts by Rule ==="
elastic_api POST "/api/detection_engine/signals/search" \
    '{"query":{"bool":{"filter":[{"term":{"signal.status":"open"}}]}},"size":0,"aggs":{"by_rule":{"terms":{"field":"signal.rule.name","size":10}}}}' \
    | jq -r '.aggregations.by_rule.buckets[] | "\(.doc_count)\t\(.key[0:60])"' | column -t
```

### Detection Rules Health

```bash
#!/bin/bash
echo "=== Rules by Status ==="
for status in enabled disabled; do
    COUNT=$(elastic_api GET "/api/detection_engine/rules/_find?filter=alert.attributes.enabled:${status}&per_page=1" | jq '.total')
    echo "$status: $COUNT"
done

echo ""
echo "=== Failed Rules ==="
elastic_api GET "/api/detection_engine/rules/_find?filter=alert.attributes.executionStatus.status:error&per_page=20" \
    | jq -r '.data[] | "\(.name[0:40])\t\(.execution_summary.last_execution.status)\t\(.execution_summary.last_execution.message[0:50])"' \
    | column -t | head -15
```

### Case Management

```bash
#!/bin/bash
echo "=== Open Cases ==="
elastic_api GET "/api/cases/_find?status=open&perPage=20&sortField=createdAt&sortOrder=desc" \
    | jq -r '.cases[] | "\(.created_at[0:16])\t\(.severity)\t\(.status)\t\(.title[0:50])\t\(.totalAlerts) alerts"' \
    | column -t

echo ""
echo "=== Cases by Assignee ==="
elastic_api GET "/api/cases/_find?perPage=100&status=open" \
    | jq -r '[.cases[] | .assignees[0].uid // "unassigned"] | group_by(.) | map({assignee: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.assignee): \(.count)"' | head -10
```

## Output Format

Present results as a structured report:
```
Managing Elastic Siem Report
════════════════════════════
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

- **kbn-xsrf header**: Required for all Kibana API POST/PUT/DELETE requests
- **Signal vs alert**: Older versions use `signal`, newer use `alert` -- check your version
- **Detection engine API path**: Changed between versions -- verify `/api/detection_engine/` vs `/api/alerting/`
- **Pagination**: Use `per_page` and `page` params -- default page size is 20
- **ECS fields**: Elastic Common Schema field names differ from raw log fields
