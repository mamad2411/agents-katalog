---
name: managing-mlflow
description: |
  Use when working with Mlflow — mLflow experiment tracking and model registry
  management. Covers experiment tracking, run comparison, model registry,
  artifact management, model serving, and metric analysis. Use when managing ML
  experiments, comparing model runs, promoting models through stages, or
  debugging MLflow tracking issues.
connection_type: mlflow
preload: false
---

# MLflow Management Skill

Manage and monitor MLflow experiments, model registry, and artifact tracking.

## MANDATORY: Discovery-First Pattern

**Always list experiments and registered models before querying specific runs.**

### Phase 1: Discovery

```bash
#!/bin/bash

MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-http://localhost:5000}"

mlflow_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Content-Type: application/json" \
            "${MLFLOW_TRACKING_URI}/api/2.0/mlflow/${endpoint}" -d "$data"
    else
        curl -s -X "$method" "${MLFLOW_TRACKING_URI}/api/2.0/mlflow/${endpoint}"
    fi
}

echo "=== MLflow Experiments ==="
mlflow_api GET "experiments/search" | jq -r '
    .experiments[] | "\(.experiment_id)\t\(.name)\t\(.lifecycle_stage)\t\(.creation_time // 0 | . / 1000 | strftime("%Y-%m-%d"))"
' | column -t | head -20

echo ""
echo "=== Registered Models ==="
mlflow_api GET "registered-models/search" | jq -r '
    .registered_models[]? | "\(.name)\t\(.latest_versions | length) versions\t\(.creation_timestamp // 0 | . / 1000 | strftime("%Y-%m-%d"))"
' | column -t | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-http://localhost:5000}"

# MLflow REST API helper
mlflow_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Content-Type: application/json" \
            "${MLFLOW_TRACKING_URI}/api/2.0/mlflow/${endpoint}" -d "$data"
    else
        curl -s -X "$method" "${MLFLOW_TRACKING_URI}/api/2.0/mlflow/${endpoint}"
    fi
}

# Search runs with filter
mlflow_search_runs() {
    local experiment_id="$1"
    local filter="${2:-}"
    local max_results="${3:-20}"
    mlflow_api POST "runs/search" "{\"experiment_ids\":[\"${experiment_id}\"],\"filter\":\"${filter}\",\"max_results\":${max_results},\"order_by\":[\"metrics.val_loss ASC\"]}"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use REST API with jq filtering for all queries
- Never dump full run details -- extract key metrics and parameters
- Convert timestamps from milliseconds to human-readable dates

## Common Operations

### Experiment Runs and Comparison

```bash
#!/bin/bash
EXPERIMENT_ID="${1:?Experiment ID required}"

echo "=== Recent Runs in Experiment $EXPERIMENT_ID ==="
mlflow_api POST "runs/search" \
    "{\"experiment_ids\":[\"${EXPERIMENT_ID}\"],\"max_results\":15,\"order_by\":[\"attribute.start_time DESC\"]}" \
    | jq -r '.runs[]? | "\(.info.run_id[0:8])\t\(.info.status)\t\(.data.params // [] | map("\(.key)=\(.value)") | join(",") | .[0:40])\t\(.data.metrics // [] | map("\(.key)=\(.value)") | join(",") | .[0:40])"' | column -t

echo ""
echo "=== Best Runs by Metric ==="
mlflow_api POST "runs/search" \
    "{\"experiment_ids\":[\"${EXPERIMENT_ID}\"],\"max_results\":5,\"order_by\":[\"metrics.val_loss ASC\"],\"filter\":\"status = 'FINISHED'\"}" \
    | jq -r '.runs[]? | "\(.info.run_id[0:8])\tval_loss=\(.data.metrics[]? | select(.key=="val_loss") | .value)\taccuracy=\(.data.metrics[]? | select(.key=="accuracy") | .value)"' | column -t
```

### Run Detail and Artifacts

```bash
#!/bin/bash
RUN_ID="${1:?Run ID required}"

echo "=== Run Details ==="
mlflow_api GET "runs/get?run_id=${RUN_ID}" | jq '{
    run_id: .run.info.run_id,
    status: .run.info.status,
    start_time: (.run.info.start_time / 1000 | strftime("%Y-%m-%d %H:%M:%S")),
    end_time: (.run.info.end_time // 0 | if . > 0 then . / 1000 | strftime("%Y-%m-%d %H:%M:%S") else "running" end),
    experiment_id: .run.info.experiment_id,
    parameters: (.run.data.params | map({(.key): .value}) | add),
    metrics: (.run.data.metrics | map({(.key): .value}) | add)
}'

echo ""
echo "=== Artifacts ==="
mlflow_api GET "artifacts/list?run_id=${RUN_ID}" | jq -r '
    .files[]? | "\(if .is_dir then "DIR " else "FILE" end)\t\(.path)\t\(.file_size // "-")"
' | column -t | head -20
```

### Model Registry Management

```bash
#!/bin/bash
MODEL_NAME="${1:?Model name required}"

echo "=== Model: $MODEL_NAME ==="
mlflow_api GET "registered-models/get?name=${MODEL_NAME}" | jq '{
    name: .registered_model.name,
    description: .registered_model.description,
    tags: .registered_model.tags,
    versions: [.registered_model.latest_versions[]? | {
        version: .version,
        stage: .current_stage,
        status: .status,
        run_id: .run_id[0:8],
        source: .source,
        created: (.creation_timestamp / 1000 | strftime("%Y-%m-%d"))
    }]
}'

echo ""
echo "=== All Versions ==="
mlflow_api GET "model-versions/search?filter=name%3D%27${MODEL_NAME}%27&max_results=10&order_by=version_number+DESC" \
    | jq -r '.model_versions[]? | "\(.version)\t\(.current_stage)\t\(.status)\t\(.run_id[0:8])\t\(.creation_timestamp // 0 | . / 1000 | strftime("%Y-%m-%d"))"' | column -t
```

### Model Stage Transitions

```bash
#!/bin/bash
MODEL_NAME="${1:?Model name required}"
VERSION="${2:?Version number required}"
TARGET_STAGE="${3:-Staging}"
DRY_RUN="${4:-true}"

echo "=== Current State ==="
mlflow_api GET "model-versions/get?name=${MODEL_NAME}&version=${VERSION}" | jq '{
    name: .model_version.name,
    version: .model_version.version,
    current_stage: .model_version.current_stage,
    status: .model_version.status
}'

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo "DRY RUN: Would transition $MODEL_NAME v$VERSION to $TARGET_STAGE"
    echo "To execute, call with dry_run=false"
else
    echo ""
    echo "=== Transitioning to $TARGET_STAGE ==="
    mlflow_api POST "model-versions/transition-stage" \
        "{\"name\":\"${MODEL_NAME}\",\"version\":\"${VERSION}\",\"stage\":\"${TARGET_STAGE}\",\"archive_existing_versions\":false}" \
        | jq '{name: .model_version.name, version: .model_version.version, new_stage: .model_version.current_stage}'
fi
```

### Metric History and Comparison

```bash
#!/bin/bash
RUN_ID="${1:?Run ID required}"
METRIC_KEY="${2:-loss}"

echo "=== Metric History: $METRIC_KEY ==="
mlflow_api GET "metrics/get-history?run_id=${RUN_ID}&metric_key=${METRIC_KEY}" \
    | jq -r '.metrics[]? | "\(.step)\t\(.value)\t\(.timestamp // 0 | . / 1000 | strftime("%H:%M:%S"))"' \
    | column -t | head -30
```

## Safety Rules

- **NEVER delete experiments or runs** without explicit confirmation -- data loss is permanent
- **NEVER transition models to Production** without reviewing validation metrics
- **Always use `archive_existing_versions: false`** unless explicitly replacing a production model
- **Check downstream dependencies** before archiving model versions -- other services may reference specific versions
- **Back up the tracking database** before any bulk operations

## Output Format

Present results as a structured report:
```
Managing Mlflow Report
══════════════════════
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

- **Tracking URI**: Ensure MLFLOW_TRACKING_URI is set correctly -- defaults to local `./mlruns` directory
- **Run ID format**: Run IDs are UUIDs -- partial matching requires searching, not direct lookup
- **Stage transitions**: Only one model version can be in Production per model name (with `archive_existing=true`)
- **Artifact storage**: Artifacts are stored separately from metadata -- S3/GCS permissions required for artifact access
- **Nested runs**: Parent-child run relationships are tracked via tags -- use `mlflow.parentRunId` tag to find children
- **Metric step conflicts**: Logging the same metric at the same step overwrites -- use unique step numbers
- **Model serving**: MLflow Models need compatible environments -- check `conda.yaml` or `requirements.txt` in model artifacts
- **Database migrations**: MLflow schema changes require `mlflow db upgrade` -- backup database before upgrading
