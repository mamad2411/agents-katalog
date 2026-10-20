---
name: managing-neptune
description: |
  Use when working with Neptune — neptune.ai experiment tracking and model
  registry management. Covers experiment comparison, model registry, dashboard
  monitoring, run metadata analysis, and artifact management. Use when managing
  ML experiments, comparing model performance, monitoring training progress, or
  auditing Neptune project resources.
connection_type: neptune
preload: false
---

# Neptune.ai Management Skill

Manage and monitor Neptune.ai experiments, model registry, and dashboards.

## MANDATORY: Discovery-First Pattern

**Always list projects and recent runs before querying specific experiments.**

### Phase 1: Discovery

```bash
#!/bin/bash

NEPTUNE_API_TOKEN="${NEPTUNE_API_TOKEN:-}"
NEPTUNE_PROJECT="${NEPTUNE_PROJECT:-}"

neptune_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $NEPTUNE_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.neptune.ai/api/leaderboard/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $NEPTUNE_API_TOKEN" \
            "https://api.neptune.ai/api/leaderboard/v1/${endpoint}"
    fi
}

echo "=== Neptune Project: $NEPTUNE_PROJECT ==="

echo ""
echo "=== Recent Runs ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":15,\"offset\":0},\"sorting\":{\"sortBy\":{\"name\":\"sys/creation_time\"},\"dir\":\"descending\"}}" \
    | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\t\(.attributes[] | select(.name=="sys/state") | .value)\t\(.attributes[] | select(.name=="sys/creation_time") | .value[0:16])"' | column -t

echo ""
echo "=== Run States ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":100,\"offset\":0}}" \
    | jq '[.entries[].attributes[] | select(.name=="sys/state") | .value] | group_by(.) | map({state: .[0], count: length})'
```

## Core Helper Functions

```bash
#!/bin/bash

NEPTUNE_API_TOKEN="${NEPTUNE_API_TOKEN:-}"

# Neptune REST API helper
neptune_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $NEPTUNE_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.neptune.ai/api/leaderboard/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $NEPTUNE_API_TOKEN" \
            "https://api.neptune.ai/api/leaderboard/v1/${endpoint}"
    fi
}

# Neptune CLI wrapper
npt() {
    neptune "$@" 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use REST API with jq filtering for structured output
- Never dump full run attribute trees -- extract key metrics
- Use run short IDs for display, full IDs for API calls

## Common Operations

### Experiment Comparison

```bash
#!/bin/bash
echo "=== Top Runs by Metric ==="
METRIC="${1:-metrics/val_loss}"
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":10,\"offset\":0},\"sorting\":{\"sortBy\":{\"name\":\"${METRIC}\"},\"dir\":\"ascending\"},\"attributeFilters\":[{\"name\":\"sys/state\",\"value\":\"Idle\"}]}" \
    | jq -r '.entries[]? | {
        id: (.attributes[] | select(.name=="sys/id") | .value),
        metric: (.attributes[] | select(.name=="'"$METRIC"'") | .value),
        created: (.attributes[] | select(.name=="sys/creation_time") | .value[0:16])
    }' | head -40

echo ""
echo "=== Failed Runs ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":10,\"offset\":0},\"attributeFilters\":[{\"name\":\"sys/failed\",\"value\":true}]}" \
    | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\t\(.attributes[] | select(.name=="sys/creation_time") | .value[0:16])"' | column -t
```

### Model Registry

```bash
#!/bin/bash
echo "=== Registered Models ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"type\":\"model\",\"pagination\":{\"limit\":20,\"offset\":0}}" \
    | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\t\(.attributes[] | select(.name=="sys/name") | .value // "unnamed")\t\(.attributes[] | select(.name=="sys/creation_time") | .value[0:16])"' | column -t

MODEL_ID="${1:-}"
if [ -n "$MODEL_ID" ]; then
    echo ""
    echo "=== Model Versions: $MODEL_ID ==="
    neptune_api POST "leaderboard/entries" \
        "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"type\":\"modelVersion\",\"pagination\":{\"limit\":10,\"offset\":0},\"attributeFilters\":[{\"name\":\"sys/model_id\",\"value\":\"${MODEL_ID}\"}]}" \
        | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\t\(.attributes[] | select(.name=="sys/stage") | .value // "none")\t\(.attributes[] | select(.name=="sys/creation_time") | .value[0:16])"' | column -t
fi
```

### Dashboard Monitoring

```bash
#!/bin/bash
echo "=== Active Runs (currently training) ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":20,\"offset\":0},\"attributeFilters\":[{\"name\":\"sys/state\",\"value\":\"Active\"}]}" \
    | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\t\(.attributes[] | select(.name=="sys/running_time") | .value // "unknown")\t\(.attributes[] | select(.name=="sys/creation_time") | .value[0:16])"' | column -t

echo ""
echo "=== Resource Usage (recent runs) ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":5,\"offset\":0},\"sorting\":{\"sortBy\":{\"name\":\"sys/creation_time\"},\"dir\":\"descending\"}}" \
    | jq -r '.entries[]? | "\(.attributes[] | select(.name=="sys/id") | .value)\tGPU=\(.attributes[] | select(.name=="monitoring/gpu") | .value // "N/A")\tMem=\(.attributes[] | select(.name=="monitoring/memory") | .value // "N/A")"' | column -t
```

### Run Detail and Metadata

```bash
#!/bin/bash
RUN_ID="${1:?Run ID required}"

echo "=== Run $RUN_ID Details ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":1,\"offset\":0},\"attributeFilters\":[{\"name\":\"sys/id\",\"value\":\"${RUN_ID}\"}]}" \
    | jq '{
        attributes: [.entries[0].attributes[] | {(.name): .value}] | add
    }' | jq 'del(.attributes["sys/trashed"])' | head -40
```

### Tag and Group Analysis

```bash
#!/bin/bash
echo "=== Runs by Tags ==="
neptune_api POST "leaderboard/entries" \
    "{\"projectIdentifier\":\"${NEPTUNE_PROJECT}\",\"pagination\":{\"limit\":100,\"offset\":0}}" \
    | jq '[.entries[].attributes[] | select(.name=="sys/tags") | .value[]?] | group_by(.) | map({tag: .[0], count: length}) | sort_by(-.count)' | head -30
```

## Safety Rules

- **NEVER trash or delete runs** without explicit confirmation -- trashing removes all associated data
- **NEVER change model version stages** without reviewing metrics -- stage transitions affect production serving
- **Always verify project identifier** before bulk operations -- wrong project can affect other teams
- **API token scope**: Tokens may have limited permissions -- verify access level before write operations

## Output Format

Present results as a structured report:
```
Managing Neptune Report
═══════════════════════
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

- **API token expiry**: Neptune API tokens can expire -- regenerate from the Neptune UI if getting 401 errors
- **Run states**: "Active" means currently logging -- do not modify active runs as it may corrupt data
- **Attribute paths**: Neptune uses hierarchical paths (e.g., `metrics/val_loss`) -- incorrect paths return empty results
- **Float series vs single values**: Metrics logged as series need different API calls than single-value attributes
- **Project naming**: Projects use `workspace/project` format -- omitting workspace causes lookup failures
- **Sync mode**: Offline runs need explicit sync -- they do not appear in the UI until `neptune sync` is called
- **Storage limits**: Large artifacts count toward storage quota -- monitor usage to avoid hitting limits
- **Concurrent access**: Multiple processes logging to the same run can cause data corruption
