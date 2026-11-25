---
name: managing-moogsoft
description: |
  Use when working with Moogsoft — moogsoft AI-driven incident management
  covering intelligent alert detection, noise reduction, correlation engine
  tuning, situation management, workflow automation, and performance analytics.
  Use when configuring Moogsoft correlation algorithms, analyzing alert noise
  reduction effectiveness, managing situations, or reviewing AI-driven incident
  detection patterns.
connection_type: moogsoft
preload: false
---

# Moogsoft AI Incident Management Skill

Manage Moogsoft AI-driven alert detection, noise reduction, correlation, and situation management.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer XXXXXX` header — injected automatically. Never hardcode tokens.

### Base URL
`https://INSTANCE.moogsoft.ai/api`

### Core Helper Function

```bash
#!/bin/bash

ms_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $MOOGSOFT_API_KEY" \
            -H "Content-Type: application/json" \
            "https://${MOOGSOFT_INSTANCE}.moogsoft.ai/api${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $MOOGSOFT_API_KEY" \
            "https://${MOOGSOFT_INSTANCE}.moogsoft.ai/api${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target ≤50 lines per script output

## Alert Management

### Get Active Alerts
```bash
ms_api GET "/v1/alerts?status=open&limit=50&sort=-createdAt" | jq '[.[] | {
  id, description, severity, source,
  class, service, createdAt,
  dedupCount, situationId
}]'
```

### Get Alert Statistics
```bash
ms_api GET "/v1/alerts/stats?period=24h" | jq '{
  totalAlerts: .total,
  deduplicated: .deduplicated,
  noiseReductionPercent: .noiseReduction,
  bySeverity: .bySeverity,
  topSources: [.bySource[:5]]
}'
```

## Situation Management

### List Active Situations
```bash
ms_api GET "/v1/situations?status=open&limit=25" | jq '[.[] | {
  id, description, severity, status,
  alertCount, createdAt,
  owner, services: [.services[]]
}]'
```

### Get Situation Details
```bash
ms_api GET "/v1/situations/SITUATION_ID" | jq '{
  description, severity, status,
  alertCount, createdAt, lastUpdated,
  alerts: [.alerts[] | {id, description, severity, source}],
  suggestedActions: .suggestions
}'
```

## Correlation Engine

### Get Correlation Definitions
```bash
ms_api GET "/v1/correlation-definitions" | jq '[.[] | {
  id, name, type, enabled,
  algorithm, parameters
}]'
```

### Review Noise Reduction Metrics
```bash
ms_api GET "/v1/metrics/noise-reduction?period=7d" | jq '{
  period: "7 days",
  totalIncoming: .totalAlerts,
  afterDedup: .afterDeduplication,
  afterCorrelation: .afterCorrelation,
  reductionPercent: .overallReduction,
  trend: .dailyTrend
}'
```

## Workflow Automation

### List Workflows
```bash
ms_api GET "/v1/workflows" | jq '[.[] | {id, name, enabled, trigger, actions: [.actions[] | .type]}]'
```

## Common Tasks

1. **Monitor noise reduction** — track deduplication and correlation effectiveness
2. **Tune correlation algorithms** — adjust time windows, similarity thresholds, and clustering
3. **Manage situations** — review, merge, or split correlated incident groups
4. **Analyze alert patterns** — identify noisy sources and flapping alerts
5. **Configure workflows** — automate situation assignment, notification, and enrichment

## Output Format

Present results as a structured report:
```
Managing Moogsoft Report
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

