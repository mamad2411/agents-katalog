---
name: managing-dynatrace
description: |
  Use when working with Dynatrace — dynatrace software intelligence platform for
  full-stack APM, infrastructure monitoring, AIOps, log management, and digital
  experience monitoring. Covers entity discovery, metric querying with DQL,
  problem detection, SLO management, and Davis AI analysis. Use when querying
  Dynatrace metrics, investigating detected problems, analyzing service
  performance, or managing SLOs and alerting profiles.
connection_type: dynatrace
preload: false
---

# Dynatrace Monitoring Skill

Query, analyze, and manage Dynatrace observability data using the Dynatrace API.

## API Overview

Dynatrace uses REST APIs at `https://<ENV_ID>.live.dynatrace.com/api/v2` (SaaS) or `https://<HOST>/e/<ENV_ID>/api/v2` (Managed).

### Core Helper Function

```bash
#!/bin/bash

dt_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${DYNATRACE_URL}/api/v2/${endpoint}" \
            -H "Authorization: Api-Token $DYNATRACE_API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${DYNATRACE_URL}/api/v2/${endpoint}" \
            -H "Authorization: Api-Token $DYNATRACE_API_TOKEN"
    fi
}

dt_metrics() {
    local selector="$1"
    local from="${2:-now-1h}"
    local to="${3:-now}"
    dt_api GET "metrics/query?metricSelector=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${selector}'))")&from=${from}&to=${to}&resolution=Inf"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover entities, metrics, and problems before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Services ==="
dt_api GET "entities?entitySelector=type(SERVICE)&fields=properties.serviceType&pageSize=25" \
    | jq -r '.entities[] | "\(.entityId)\t\(.displayName)\t\(.properties.serviceType // "unknown")"' | head -25

echo ""
echo "=== Hosts ==="
dt_api GET "entities?entitySelector=type(HOST)&fields=properties.osType&pageSize=20" \
    | jq -r '.entities[] | "\(.entityId)\t\(.displayName)\t\(.properties.osType // "unknown")"' | head -20

echo ""
echo "=== Active Problems ==="
dt_api GET "problems?problemSelector=status(OPEN)&pageSize=20" \
    | jq -r '.problems[] | "\(.problemId)\t\(.severityLevel)\t\(.title[0:60])\t\(.impactLevel)"' | head -20

echo ""
echo "=== SLOs ==="
dt_api GET "slo?pageSize=15" | jq -r '.slo[] | "\(.id)\t\(.name)\ttarget:\(.target)%\tstatus:\(.status)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Service Performance (last 1h) ==="
dt_metrics "builtin:service.response.time:avg:names" \
    | jq -r '.result[0].data[] | "\(.dimensions[0])\t\(.values[0] / 1000000 | . * 100 | round / 100)ms"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Service Error Rate ==="
dt_metrics "builtin:service.errors.total.rate:avg:names" \
    | jq -r '.result[0].data[] | "\(.dimensions[0])\t\(.values[0] * 100 | . * 10 | round / 10)%"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Host CPU Usage ==="
dt_metrics "builtin:host.cpu.usage:avg:names" \
    | jq -r '.result[0].data[] | "\(.dimensions[0])\t\(.values[0] | . * 10 | round / 10)%"' | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Open Problems Detail ==="
dt_api GET "problems?problemSelector=status(OPEN)&fields=recentComments,impactedEntities&pageSize=10" \
    | jq -r '.problems[] | "\(.severityLevel)\t\(.title[0:50])\timpacted:\(.impactedEntities | length)"' | head -10

echo ""
echo "=== SLO Error Budget ==="
dt_api GET "slo?pageSize=10&evaluate=true" \
    | jq -r '.slo[] | "\(.name)\ttarget:\(.target)%\tcurrent:\(.evaluatedPercentage // "N/A")%\tbudget:\(.errorBudget // "N/A")%"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `resolution=Inf` for single aggregated values
- Use `entitySelector` for server-side entity filtering
- Metric values: response time is in nanoseconds, divide by 1000000 for ms
- Use `problemSelector=status(OPEN)` to focus on active issues

## Output Format

Present results as a structured report:
```
Managing Dynatrace Report
═════════════════════════
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

