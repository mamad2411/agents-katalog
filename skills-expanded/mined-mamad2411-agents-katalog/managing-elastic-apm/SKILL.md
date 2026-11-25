---
name: managing-elastic-apm
description: |
  Use when working with Elastic Apm — elastic APM application performance
  monitoring for distributed tracing, error tracking, metrics collection, and
  service map visualization within the Elastic Stack. Covers service discovery,
  transaction analysis, error investigation, span analysis, and agent
  configuration. Use when investigating application performance, analyzing
  distributed traces, reviewing error patterns, or managing APM agent
  configurations.
connection_type: elastic-apm
preload: false
---

# Elastic APM Monitoring Skill

Query, analyze, and manage Elastic APM data using the Elasticsearch and Kibana APIs.

## API Overview

Elastic APM data is stored in Elasticsearch and queried via `https://<ES_HOST>:9200` or Kibana APM API at `https://<KIBANA_HOST>/api/apm`.

### Core Helper Function

```bash
#!/bin/bash

es_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${ELASTICSEARCH_URL}/${endpoint}" \
            -H "Authorization: ApiKey $ELASTIC_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${ELASTICSEARCH_URL}/${endpoint}" \
            -H "Authorization: ApiKey $ELASTIC_API_KEY"
    fi
}

kibana_apm() {
    local endpoint="$1"
    curl -s "${KIBANA_URL}/api/apm/${endpoint}" \
        -H "Authorization: ApiKey $ELASTIC_API_KEY" \
        -H "kbn-xsrf: true"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover services, environments, and APM indices before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== APM Services ==="
kibana_apm "services?start=$(date -d '1 hour ago' -Iseconds)&end=$(date -Iseconds)" \
    | jq -r '.items[] | "\(.serviceName)\t\(.agentName)\t\(.environment // "unknown")"' | head -20

echo ""
echo "=== APM Indices ==="
es_api GET "_cat/indices/apm-*?h=index,docs.count,store.size&s=index" | head -15

echo ""
echo "=== Environments ==="
kibana_apm "environments?start=$(date -d '1 hour ago' -Iseconds)&end=$(date -Iseconds)" \
    | jq -r '.environments[]' | head -10

echo ""
echo "=== Agent Configurations ==="
kibana_apm "settings/agent-configuration" \
    | jq -r '.configurations[] | "\(.service.name)\t\(.service.environment // "all")\t\(.settings | keys | join(","))"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
SERVICE="${1:-}"
RANGE_START=$(date -d '1 hour ago' -Iseconds)
RANGE_END=$(date -Iseconds)

echo "=== Transaction Performance ==="
kibana_apm "services/${SERVICE}/transactions/groups/main_statistics?start=${RANGE_START}&end=${RANGE_END}&transactionType=request&latencyAggregationType=p95" \
    | jq -r '.transactionGroups[] | "\(.name[0:50])\tp95:\(.latency / 1000 | . * 10 | round / 10)ms\tthroughput:\(.throughput | . * 10 | round / 10)/min\terror:\(.errorRate * 100 | . * 10 | round / 10)%"' | head -15

echo ""
echo "=== Error Groups ==="
kibana_apm "services/${SERVICE}/errors/groups/main_statistics?start=${RANGE_START}&end=${RANGE_END}" \
    | jq -r '.errorGroups[] | "\(.name[0:50])\toccurrences:\(.occurrences)\tlast:\(.lastSeen[0:19])"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Service Dependencies ==="
kibana_apm "services/${SERVICE}/dependencies?start=${RANGE_START}&end=${RANGE_END}" \
    | jq -r '.serviceDependencies[] | "\(.name)\tlatency:\(.latency.value / 1000 | . * 10 | round / 10)ms\tthroughput:\(.throughput.value | . * 10 | round / 10)/min"' | head -10

echo ""
echo "=== Infrastructure Metrics ==="
kibana_apm "services/${SERVICE}/infrastructure?start=${RANGE_START}&end=${RANGE_END}" \
    | jq -r '.currentPeriod[] | "\(.name)\tcpu:\(.cpu // "N/A")\tmem:\(.memory // "N/A")"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use time range parameters and Kibana APM aggregation endpoints
- Latency values are in microseconds from Kibana APM API — divide by 1000 for ms
- Use `transactionType` filter (request, page-load, etc.) to narrow results
- Prefer Kibana APM endpoints over raw Elasticsearch queries for pre-aggregated data

## Output Format

Present results as a structured report:
```
Managing Elastic Apm Report
═══════════════════════════
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

