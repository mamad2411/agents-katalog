---
name: managing-label-studio
description: |
  Use when working with Label Studio — label Studio data labeling platform
  management. Covers project management, annotation tasks, model predictions,
  data export, user management, and labeling configuration. Use when managing
  annotation projects, reviewing labeling progress, importing predictions, or
  exporting labeled datasets.
connection_type: label-studio
preload: false
---

# Label Studio Management Skill

Manage and monitor Label Studio annotation projects, tasks, and labeling workflows.

## MANDATORY: Discovery-First Pattern

**Always list projects and their status before modifying tasks or configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

LS_HOST="${LABEL_STUDIO_HOST:-http://localhost:8080}"
LS_TOKEN="${LABEL_STUDIO_API_KEY:-}"

ls_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Token $LS_TOKEN" \
            -H "Content-Type: application/json" \
            "${LS_HOST}/api/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Token $LS_TOKEN" \
            "${LS_HOST}/api/${endpoint}"
    fi
}

echo "=== Label Studio Version ==="
ls_api GET "version" | jq -r '.'

echo ""
echo "=== Projects ==="
ls_api GET "projects?page_size=20" | jq -r '
    .results[]? | "\(.id)\t\(.title)\ttasks=\(.task_number)\tannotated=\(.num_tasks_with_annotations // 0)\t\(.created_at[0:10])"
' | column -t

echo ""
echo "=== Current User ==="
ls_api GET "current-user/whoami" | jq '{username: .username, email: .email}'
```

## Core Helper Functions

```bash
#!/bin/bash

LS_HOST="${LABEL_STUDIO_HOST:-http://localhost:8080}"
LS_TOKEN="${LABEL_STUDIO_API_KEY:-}"

# Label Studio REST API helper
ls_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Token $LS_TOKEN" \
            -H "Content-Type: application/json" \
            "${LS_HOST}/api/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Token $LS_TOKEN" \
            "${LS_HOST}/api/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use REST API with jq for all queries
- Never dump full task data -- extract annotation summaries
- Use project IDs for API calls, titles for display

## Common Operations

### Project Management

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Project Details ==="
ls_api GET "projects/${PROJECT_ID}" | jq '{
    id: .id,
    title: .title,
    description: .description,
    total_tasks: .task_number,
    annotated: .num_tasks_with_annotations,
    total_annotations: .total_annotations_number,
    total_predictions: .total_predictions_number,
    created: .created_at[0:10],
    label_config_updated: .label_config_updated
}'

echo ""
echo "=== Labeling Progress ==="
TOTAL=$(ls_api GET "projects/${PROJECT_ID}" | jq '.task_number')
ANNOTATED=$(ls_api GET "projects/${PROJECT_ID}" | jq '.num_tasks_with_annotations // 0')
if [ "$TOTAL" -gt 0 ]; then
    PCT=$(echo "scale=1; $ANNOTATED * 100 / $TOTAL" | bc 2>/dev/null || echo "N/A")
    echo "Progress: ${ANNOTATED}/${TOTAL} tasks (${PCT}%)"
fi

echo ""
echo "=== Label Config ==="
ls_api GET "projects/${PROJECT_ID}" | jq -r '.label_config' | head -20
```

### Annotation Task Review

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Task Summary ==="
ls_api GET "tasks?project=${PROJECT_ID}&page_size=20" | jq -r '
    .results[]? | "\(.id)\tannotations=\(.total_annotations)\tpredictions=\(.total_predictions)\tcancelled=\(.cancelled_annotations)\t\(.updated_at[0:16])"
' | column -t

echo ""
echo "=== Unannotated Tasks ==="
ls_api GET "tasks?project=${PROJECT_ID}&page_size=10&filters={\"conjunction\":\"and\",\"items\":[{\"filter\":\"filter:tasks:total_annotations\",\"operator\":\"equal\",\"type\":\"Number\",\"value\":0}]}" \
    | jq -r '.results[]? | "\(.id)\t\(.data | keys | join(","))"' | column -t | head -15

echo ""
echo "=== Annotation Quality (agreement) ==="
ls_api GET "projects/${PROJECT_ID}" | jq '{
    agreement: .agreement,
    overlap: .overlap_cohort_percentage,
    sampling: .sampling
}'
```

### Model Predictions Import

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Existing Predictions ==="
ls_api GET "predictions?project=${PROJECT_ID}&page_size=20" | jq -r '
    .results[]? | "\(.id)\ttask=\(.task)\tscore=\(.score // "N/A")\tmodel=\(.model_version // "unknown")\t\(.created_at[0:16])"
' | column -t | head -15

echo ""
echo "=== Prediction Summary ==="
ls_api GET "projects/${PROJECT_ID}" | jq '{
    total_predictions: .total_predictions_number,
    model_version: .model_version
}'

echo ""
echo "=== ML Backends ==="
ls_api GET "ml?project=${PROJECT_ID}" | jq -r '
    .[]? | "\(.id)\t\(.title // .url)\t\(.state)\t\(.is_interactive)"
' | column -t
```

### Data Export

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"
FORMAT="${2:-JSON}"

echo "=== Available Export Formats ==="
echo "JSON, JSON_MIN, CSV, TSV, CONLL2003, COCO, VOC, YOLO, BRUSH_TO_NUMPY"

echo ""
echo "=== Export Preview (first 5 tasks) ==="
ls_api GET "projects/${PROJECT_ID}/export?exportType=${FORMAT}" \
    | jq '.[0:5] | .[] | {id: .id, annotations_count: (.annotations | length), data_keys: (.data | keys)}' 2>/dev/null | head -30

echo ""
echo "=== Export Stats ==="
ls_api GET "projects/${PROJECT_ID}" | jq '{
    total_tasks: .task_number,
    tasks_with_annotations: .num_tasks_with_annotations,
    total_annotations: .total_annotations_number,
    export_format: "'"$FORMAT"'"
}'
```

### User and Permissions Audit

```bash
#!/bin/bash
echo "=== All Users ==="
ls_api GET "users" | jq -r '
    .[]? | "\(.id)\t\(.username)\t\(.email)\t\(.is_staff // false | if . then "admin" else "user" end)\tactive=\(.is_active)"
' | column -t

PROJECT_ID="${1:-}"
if [ -n "$PROJECT_ID" ]; then
    echo ""
    echo "=== Project Members: $PROJECT_ID ==="
    ls_api GET "projects/${PROJECT_ID}/members" | jq -r '
        .[]? | "\(.user.username)\t\(.user.email)"
    ' | column -t
fi
```

## Safety Rules

- **NEVER delete annotations** without explicit confirmation -- manual labeling effort is expensive and irreversible
- **NEVER modify label configurations** on projects with existing annotations -- this can invalidate all previous labels
- **Always export data before destructive operations** -- create a backup export first
- **Verify prediction model versions** before importing -- overwriting predictions with wrong model loses reference data
- **Check overlap settings** before starting annotation -- modifying overlap mid-project creates inconsistencies

## Output Format

Present results as a structured report:
```
Managing Label Studio Report
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

- **API token vs session**: REST API requires API key (Token auth), not browser session cookies
- **Label config changes**: Changing label config after annotations exist can orphan annotation data -- export first
- **Task data format**: Import data must match the expected schema for the label config -- mismatches cause rendering errors
- **Cloud storage sync**: S3/GCS source storage sync is one-directional -- new files must be re-synced manually
- **Prediction scores**: Prediction scores must be between 0 and 1 -- values outside this range cause import failures
- **Concurrent annotation**: Multiple annotators on the same task without overlap enabled causes conflicts
- **Export pagination**: Large projects may require paginated export -- single export requests can timeout
- **ML backend connectivity**: ML backends must be accessible from Label Studio server -- network issues cause silent prediction failures
