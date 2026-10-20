---
name: managing-growthbook
description: |
  Use when working with Growthbook — growthBook feature flag management, A/B
  testing, experiment analysis, and data-driven decisions. Covers feature
  definitions, experiment configuration, metric tracking, visual editor
  experiments, and SDK connections. Use when managing feature flags, reviewing
  experiment results, configuring targeting attributes, or analyzing experiment
  metrics in GrowthBook.
connection_type: growthbook
preload: false
---

# GrowthBook Management Skill

Manage and analyze feature flags, experiments, metrics, and data sources in GrowthBook.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $GROWTHBOOK_API_KEY` header. Never hardcode tokens.

### Base URL
`$GROWTHBOOK_URL/api/v1` (cloud: `https://api.growthbook.io/api/v1`, or self-hosted)

### Core Helper Function

```bash
#!/bin/bash

GROWTHBOOK_BASE="${GROWTHBOOK_URL:-https://api.growthbook.io}"

gb_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $GROWTHBOOK_API_KEY" \
            -H "Content-Type: application/json" \
            "${GROWTHBOOK_BASE}/api/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $GROWTHBOOK_API_KEY" \
            -H "Content-Type: application/json" \
            "${GROWTHBOOK_BASE}/api/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Features

```bash
#!/bin/bash
echo "=== Features ==="
gb_api GET "/features?limit=25" \
    | jq -r '.features[] | "\(.valueType)\t\(.id)\t\(.defaultValue)\t\(.environments | keys | join(","))"' \
    | column -t

echo ""
echo "=== Feature Summary ==="
gb_api GET "/features?limit=100" \
    | jq '{total: (.features | length), by_type: (.features | group_by(.valueType) | map({(.[0].valueType): length}) | add), archived: ([.features[] | select(.archived)] | length)}'
```

### List Experiments

```bash
#!/bin/bash
echo "=== Experiments ==="
gb_api GET "/experiments?limit=20" \
    | jq -r '.experiments[] | "\(.status)\t\(.name[0:40])\t\(.variations | length) variations\t\(.phases | length) phases"' \
    | column -t

echo ""
echo "=== Experiment Status Summary ==="
gb_api GET "/experiments?limit=50" \
    | jq -r '.experiments[] | .status' | sort | uniq -c | sort -rn
```

## Analysis Phase

### Experiment Details

```bash
#!/bin/bash
EXPERIMENT_ID="${1:?Experiment ID required}"

echo "=== Experiment Details ==="
gb_api GET "/experiments/${EXPERIMENT_ID}" \
    | jq '.experiment | {id, name, status, hypothesis: .hypothesis[0:100], variations: [.variations[].name], metrics: .metrics, guardrailMetrics: .guardrailMetrics}'

echo ""
echo "=== Results ==="
gb_api GET "/experiments/${EXPERIMENT_ID}/results" \
    | jq -r '.result | .variations[] | "\(.variationId)\t\(.analyses[0].stats.mean // "pending")"' | column -t 2>/dev/null || echo "Results not yet available"
```

### Metrics and Data Sources

```bash
#!/bin/bash
echo "=== Metrics ==="
gb_api GET "/metrics?limit=20" \
    | jq -r '.metrics[] | "\(.type)\t\(.name[0:30])\t\(.datasource[0:20])"' | column -t

echo ""
echo "=== Data Sources ==="
gb_api GET "/data-sources" \
    | jq -r '.dataSources[] | "\(.type)\t\(.name)\t\(.settings.queries | length // 0) queries"' | column -t

echo ""
echo "=== SDK Connections ==="
gb_api GET "/sdk-connections" \
    | jq -r '.connections[] | "\(.name)\t\(.language)\t\(.environment)"' | column -t | head -10
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Self-hosted vs cloud**: Base URL varies -- always use `$GROWTHBOOK_URL` env variable
- **Value types**: `boolean`, `string`, `number`, `json` for feature values
- **Experiment statuses**: `draft`, `running`, `stopped`
- **Statistical engine**: GrowthBook uses Bayesian or Frequentist analysis -- check organization settings
- **Metrics vs guardrails**: Guardrail metrics are monitored but not optimized for
- **Environments**: Features have per-environment rules and enabled state
