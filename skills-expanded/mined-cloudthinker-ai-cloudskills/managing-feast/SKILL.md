---
name: managing-feast
description: |
  Use when working with Feast — feast feature store management. Covers feature
  store configuration, entity management, feature views, materialization, online
  serving, and data source inspection. Use when managing ML feature pipelines,
  materializing features, querying online/offline stores, or debugging feature
  retrieval issues.
connection_type: feast
preload: false
---

# Feast Management Skill

Manage and monitor Feast feature store entities, feature views, and materialization.

## MANDATORY: Discovery-First Pattern

**Always inspect the feature store registry before modifying features or running materialization.**

### Phase 1: Discovery

```bash
#!/bin/bash

FEAST_REPO="${FEAST_REPO_PATH:-.}"

echo "=== Feast Version ==="
feast version 2>/dev/null

echo ""
echo "=== Feature Store Config ==="
cat "${FEAST_REPO}/feature_store.yaml" 2>/dev/null | head -20

echo ""
echo "=== Entities ==="
feast -c "$FEAST_REPO" entities list 2>/dev/null | head -15

echo ""
echo "=== Feature Views ==="
feast -c "$FEAST_REPO" feature-views list 2>/dev/null | head -15

echo ""
echo "=== Data Sources ==="
feast -c "$FEAST_REPO" data-sources list 2>/dev/null | head -15

echo ""
echo "=== On-Demand Feature Views ==="
feast -c "$FEAST_REPO" on-demand-feature-views list 2>/dev/null | head -10
```

## Core Helper Functions

```bash
#!/bin/bash

FEAST_REPO="${FEAST_REPO_PATH:-.}"

# Feast CLI wrapper
feast_cmd() {
    feast -c "$FEAST_REPO" "$@" 2>/dev/null
}

# Feast registry API (if using Feast server)
feast_api() {
    local endpoint="$1"
    curl -s "${FEAST_SERVER_URL:-http://localhost:6566}/${endpoint}"
}

# Check materialization status
feast_materialize_status() {
    feast_cmd feature-views list | while read -r fv; do
        echo "$fv: $(feast_cmd feature-views describe "$fv" 2>/dev/null | grep -i 'materialization' | head -1)"
    done
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use Feast CLI for registry operations
- Use REST API or Python SDK output for serving queries
- Never dump full feature view definitions -- extract key fields

## Common Operations

### Entity Management

```bash
#!/bin/bash
echo "=== All Entities ==="
feast_cmd entities list

ENTITY="${1:-}"
if [ -n "$ENTITY" ]; then
    echo ""
    echo "=== Entity Details: $ENTITY ==="
    feast_cmd entities describe "$ENTITY"
fi
```

### Feature View Inspection

```bash
#!/bin/bash
echo "=== Feature Views ==="
feast_cmd feature-views list

FV_NAME="${1:-}"
if [ -n "$FV_NAME" ]; then
    echo ""
    echo "=== Feature View Details: $FV_NAME ==="
    feast_cmd feature-views describe "$FV_NAME"
fi

echo ""
echo "=== Feature Services ==="
feast_cmd feature-services list 2>/dev/null | head -10
```

### Materialization

```bash
#!/bin/bash
START_DATE="${1:?Start date required (YYYY-MM-DD)}"
END_DATE="${2:?End date required (YYYY-MM-DD)}"
DRY_RUN="${3:-true}"

echo "=== Materialization Plan ==="
echo "Date range: $START_DATE to $END_DATE"
echo ""
echo "Feature views to materialize:"
feast_cmd feature-views list 2>/dev/null

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo "DRY RUN: Would materialize features from $START_DATE to $END_DATE"
    echo "To execute, call with dry_run=false"
else
    echo ""
    echo "=== Running Materialization ==="
    feast_cmd materialize "$START_DATE" "$END_DATE" 2>&1 | tail -20
fi
```

### Online Serving Test

```bash
#!/bin/bash
FEATURE_SERVICE="${1:?Feature service name required}"

echo "=== Feature Service: $FEATURE_SERVICE ==="
feast_cmd feature-services describe "$FEATURE_SERVICE" 2>/dev/null

echo ""
echo "=== Online Store Status ==="
# Check if online store is accessible
ONLINE_STORE_TYPE=$(grep 'type:' "${FEAST_REPO}/feature_store.yaml" 2>/dev/null | grep -A1 'online_store' | tail -1 | awk '{print $2}')
echo "Online store type: ${ONLINE_STORE_TYPE:-unknown}"

echo ""
echo "=== Sample Online Fetch ==="
echo "Use feast_cmd get-online-features or the Python SDK to fetch features:"
echo "  from feast import FeatureStore"
echo "  store = FeatureStore('${FEAST_REPO}')"
echo "  features = store.get_online_features("
echo "      features=['${FEATURE_SERVICE}:feature_name'],"
echo "      entity_rows=[{'entity_id': 'value'}]"
echo "  ).to_dict()"
```

### Registry and Data Source Audit

```bash
#!/bin/bash
echo "=== Registry Summary ==="
echo "Entities:"
feast_cmd entities list 2>/dev/null | wc -l | xargs -I{} echo "  {} entities"
echo "Feature Views:"
feast_cmd feature-views list 2>/dev/null | wc -l | xargs -I{} echo "  {} feature views"
echo "Data Sources:"
feast_cmd data-sources list 2>/dev/null | wc -l | xargs -I{} echo "  {} data sources"

echo ""
echo "=== Data Sources ==="
feast_cmd data-sources list

echo ""
echo "=== Feature Store Config ==="
cat "${FEAST_REPO}/feature_store.yaml" 2>/dev/null | head -30
```

## Safety Rules

- **NEVER delete feature views** with active consumers -- downstream models depend on feature availability
- **NEVER run materialization** without verifying date ranges -- overlapping materializations can cause data inconsistencies
- **Always apply registry changes** (`feast apply`) before materialization -- unapplied definitions are not materialized
- **Check online store capacity** before large materializations -- Redis/DynamoDB may need scaling
- **Verify data source freshness** before materializing -- stale sources produce outdated features

## Output Format

Present results as a structured report:
```
Managing Feast Report
═════════════════════
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

- **Registry sync**: Multiple Feast instances sharing a registry must use a centralized registry (SQL, GCS, S3) -- local file registries cause conflicts
- **Materialization gaps**: Incremental materialization requires contiguous date ranges -- gaps cause missing features in online serving
- **TTL expiration**: Features with TTL set will expire from the online store -- ensure materialization runs frequently enough
- **Entity key types**: Entity key types must match between feature views and retrieval requests -- type mismatches cause silent null returns
- **Offline vs online schemas**: Feature data types must be consistent between offline and online stores -- schema drift causes serving errors
- **Feast apply order**: Dependencies matter -- entities must be registered before feature views that reference them
- **Point-in-time joins**: Offline retrieval uses point-in-time correct joins -- incorrect event timestamps cause feature leakage
- **Provider compatibility**: Not all features are available in all providers (GCP, AWS, local) -- check provider documentation
