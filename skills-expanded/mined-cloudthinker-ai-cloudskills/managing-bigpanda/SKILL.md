---
name: managing-bigpanda
description: |
  Use when working with Bigpanda — bigPanda AIOps platform management covering
  event correlation, root cause analysis, incident management, alert enrichment,
  topology-based correlation, environment management, and analytics. Use when
  configuring BigPanda correlation patterns, investigating correlated incidents,
  tuning noise reduction, or analyzing alert topology and root cause indicators.
connection_type: bigpanda
preload: false
---

# BigPanda AIOps Management Skill

Manage BigPanda event correlation, root cause analysis, incident management, and alert enrichment.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer XXXXXX` header — injected automatically. Never hardcode tokens.

### Base URL
`https://api.bigpanda.io`

### Core Helper Function

```bash
#!/bin/bash

bp_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $BIGPANDA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.bigpanda.io${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $BIGPANDA_API_TOKEN" \
            "https://api.bigpanda.io${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target ≤50 lines per script output

## Incident Management

### Get Active Incidents
```bash
bp_api GET "/resources/v2.0/incidents?status=active&sort=-startedAt&limit=25" | jq '[.items[] | {
  id, title, status, severity,
  startedAt, alertCount,
  assignee, environment
}]'
```

### Get Incident Details with Correlated Alerts
```bash
bp_api GET "/resources/v2.0/incidents/INCIDENT_ID/alerts" | jq '[.items[] | {
  alertId, status, severity,
  host, check, description,
  source_system, timestamp
}]'
```

## Correlation and Root Cause

### Get Correlation Patterns
```bash
bp_api GET "/resources/v2.0/correlation-patterns" | jq '[.items[] | {
  id, name, active,
  correlationType,
  conditions
}]'
```

### Review Root Cause Analysis
```bash
bp_api GET "/resources/v2.0/incidents/INCIDENT_ID/rca" | jq '{
  rootCause: .rootCause,
  confidence: .confidence,
  relatedChanges: [.changes[] | {type, description, timestamp}],
  topology: .topologyPath
}'
```

## Alert Enrichment

### Get Enrichment Tags
```bash
bp_api GET "/resources/v2.0/enrichment/tags" | jq '[.items[] | {name, type, source, active}]'
```

### Create Enrichment Mapping
```bash
bp_api POST "/resources/v2.0/enrichment/tags" '{
  "name": "service_tier",
  "type": "mapping",
  "source": "host",
  "active": true,
  "mapping": {"web-prod-*": "tier-1", "api-prod-*": "tier-1", "batch-*": "tier-3"}
}'
```

## Environment Management

### List Environments
```bash
bp_api GET "/resources/v2.0/environments" | jq '[.items[] | {id, name, alertCount, incidentCount}]'
```

## Analytics

### Get Incident Analytics
```bash
bp_api GET "/resources/v2.0/analytics/incidents?period=30d" | jq '{
  totalIncidents: .total,
  mttr: .meanTimeToResolve,
  noiseReduction: .noiseReductionPercentage,
  topSources: [.bySource[] | {source: .name, count: .value}][:5]
}'
```

## Common Tasks

1. **Review correlated incidents** — understand how BigPanda groups related alerts
2. **Tune correlation patterns** — adjust topology and tag-based correlation rules
3. **Analyze root cause** — review RCA recommendations and associated change events
4. **Optimize enrichment** — add metadata tags for better alert context and routing
5. **Monitor noise reduction** — track correlation efficiency and alert-to-incident ratios

## Output Format

Present results as a structured report:
```
Managing Bigpanda Report
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

