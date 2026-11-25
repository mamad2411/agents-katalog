---
name: managing-optimizely
description: |
  Use when working with Optimizely — optimizely feature experimentation, flag
  management, audience targeting, event tracking, and results analysis. Covers
  feature flag configuration, experiment design, rollout management, audience
  rules, and statistical results. Use when managing feature flags, reviewing
  experiment results, configuring audiences, or analyzing conversion metrics in
  Optimizely.
connection_type: optimizely
preload: false
---

# Optimizely Management Skill

Manage and analyze feature flags, experiments, audiences, and results in Optimizely.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $OPTIMIZELY_API_KEY` header (personal access token). Never hardcode tokens.

### Base URL
`https://api.optimizely.com/v2`

### Core Helper Function

```bash
#!/bin/bash

opt_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $OPTIMIZELY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.optimizely.com/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $OPTIMIZELY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.optimizely.com/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Projects and Flags

```bash
#!/bin/bash
echo "=== Projects ==="
opt_api GET "/projects?per_page=25" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.platform)\t\(.status)"' | column -t

echo ""
PROJECT_ID="${1:?Project ID required}"
echo "=== Feature Flags ==="
opt_api GET "/features?project_id=${PROJECT_ID}&per_page=25" \
    | jq -r '.[] | "\(.id)\t\(.key)\t\(.archived)"' | column -t
```

### List Experiments

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Experiments ==="
opt_api GET "/experiments?project_id=${PROJECT_ID}&per_page=20" \
    | jq -r '.[] | "\(.status)\t\(.name[0:40])\t\(.type)\t\(.variations | length) variations"' | column -t

echo ""
echo "=== Experiment Status Summary ==="
opt_api GET "/experiments?project_id=${PROJECT_ID}&per_page=100" \
    | jq -r '.[] | .status' | sort | uniq -c | sort -rn
```

## Analysis Phase

### Experiment Results

```bash
#!/bin/bash
EXPERIMENT_ID="${1:?Experiment ID required}"

echo "=== Experiment Details ==="
opt_api GET "/experiments/${EXPERIMENT_ID}" \
    | jq '{name, status, type, key, variations: [.variations[] | {key, name, weight}], metrics: [.metrics[].event_id]}'

echo ""
echo "=== Results ==="
opt_api GET "/experiments/${EXPERIMENT_ID}/results" \
    | jq -r '.metrics[0:5][] | "\(.name[0:30])\t\(.results | to_entries[] | "\(.key): \(.value.lift.value // "pending")")"' \
    | column -t 2>/dev/null || echo "Results not yet available"
```

### Audiences and Events

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Audiences ==="
opt_api GET "/audiences?project_id=${PROJECT_ID}&per_page=20" \
    | jq -r '.[] | "\(.id)\t\(.name[0:40])\t\(.conditions | length // 0) conditions"' | column -t

echo ""
echo "=== Events ==="
opt_api GET "/events?project_id=${PROJECT_ID}&per_page=20" \
    | jq -r '.[] | "\(.key)\t\(.name[0:40])\t\(.event_type)"' | column -t

echo ""
echo "=== Environments ==="
opt_api GET "/environments?project_id=${PROJECT_ID}" \
    | jq -r '.[] | "\(.key)\t\(.name)\t\(.is_primary)"' | column -t
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
- **Experiment types**: `a/b`, `feature`, `multiarmed_bandit` -- type determines available features
- **Experiment statuses**: `not_started`, `running`, `paused`, `concluded`, `archived`
- **Traffic allocation**: Variations have weights that must sum to 10000 (basis points)
- **Feature vs experiment**: Features are flags; experiments test variations of features
- **Environments**: Feature flags can be toggled per environment
- **Pagination**: Use `per_page` and `page` parameters, max 100 per page
- **Rate limits**: 50 requests per second for REST API
