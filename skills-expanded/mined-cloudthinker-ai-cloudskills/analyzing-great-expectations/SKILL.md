---
name: analyzing-great-expectations
description: |
  Use when working with Great Expectations — great Expectations data quality
  framework analysis. Covers expectation suite management, validation result
  review, data docs generation, checkpoint execution, datasource configuration,
  and batch analysis. Use when reviewing data quality results, managing
  expectation suites, investigating validation failures, or auditing data
  quality configurations.
connection_type: great_expectations
preload: false
---

# Great Expectations Analysis Skill

Analyze and manage Great Expectations data quality suites, validations, and checkpoints.

## MANDATORY: Discovery-First Pattern

**Always discover project structure and available suites before querying specific validation results.**

### Phase 1: Discovery

```bash
#!/bin/bash

GE_DIR="${GE_PROJECT_DIR:-.}"

echo "=== Great Expectations Project Structure ==="
ls -la "${GE_DIR}/great_expectations/" 2>/dev/null || echo "No GE directory found at ${GE_DIR}"

echo ""
echo "=== Expectation Suites ==="
ls "${GE_DIR}/great_expectations/expectations/" 2>/dev/null | head -20

echo ""
echo "=== Checkpoints ==="
ls "${GE_DIR}/great_expectations/checkpoints/" 2>/dev/null | head -20

echo ""
echo "=== Datasources (from config) ==="
python3 -c "
import yaml
with open('${GE_DIR}/great_expectations/great_expectations.yml') as f:
    config = yaml.safe_load(f)
for name, ds in config.get('datasources', {}).items():
    print(f'{name}\t{ds.get(\"class_name\", \"?\")}\t{ds.get(\"execution_engine\", {}).get(\"class_name\", \"?\")}')
" 2>/dev/null | column -t

echo ""
echo "=== Validation Results (recent) ==="
ls -lt "${GE_DIR}/great_expectations/uncommitted/validations/" 2>/dev/null | head -10
```

## Core Helper Functions

```bash
#!/bin/bash

GE_DIR="${GE_PROJECT_DIR:-.}"
GE_BASE="${GE_DIR}/great_expectations"

# Run GE CLI command
ge_cmd() {
    cd "${GE_DIR}" && great_expectations "$@" 2>/dev/null
}

# Parse validation result JSON
ge_parse_validation() {
    local result_file="$1"
    jq '{
        suite: .meta.expectation_suite_name,
        success: .success,
        evaluated: (.results | length),
        passed: ([.results[] | select(.success == true)] | length),
        failed: ([.results[] | select(.success == false)] | length),
        run_time: .meta.run_id.run_time
    }' "$result_file"
}

# List all expectation suites
ge_list_suites() {
    find "${GE_BASE}/expectations" -name "*.json" -type f 2>/dev/null | \
        sed "s|${GE_BASE}/expectations/||;s|\.json$||;s|/|.|g"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Parse JSON validation results with jq — never dump full expectation configs
- Summarize pass/fail counts, not individual expectation details

## Common Operations

### Expectation Suite Analysis

```bash
#!/bin/bash
echo "=== All Expectation Suites ==="
ge_list_suites | while read suite; do
    SUITE_FILE="${GE_BASE}/expectations/$(echo $suite | tr '.' '/').json"
    COUNT=$(jq '.expectations | length' "$SUITE_FILE" 2>/dev/null || echo 0)
    echo -e "${suite}\t${COUNT} expectations"
done | column -t

echo ""
echo "=== Suite Detail ==="
SUITE="${1:-}"
if [ -n "$SUITE" ]; then
    SUITE_FILE="${GE_BASE}/expectations/$(echo $SUITE | tr '.' '/').json"
    jq -r '.expectations[] | "\(.expectation_type)\t\(.kwargs | to_entries | map("\(.key)=\(.value)") | join(", ") | .[0:60])"' \
        "$SUITE_FILE" | column -t | head -20
fi
```

### Validation Results Review

```bash
#!/bin/bash
echo "=== Recent Validation Results ==="
find "${GE_BASE}/uncommitted/validations" -name "*.json" -type f 2>/dev/null | \
    sort -r | head -10 | while read vfile; do
    jq -r '"Suite: \(.meta.expectation_suite_name)\tSuccess: \(.success)\tPassed: \([.results[] | select(.success)] | length)/\(.results | length)\tTime: \(.meta.run_id.run_time[0:16] // "?")"' "$vfile" 2>/dev/null
done | column -t

echo ""
echo "=== Failed Validations ==="
find "${GE_BASE}/uncommitted/validations" -name "*.json" -type f 2>/dev/null | \
    sort -r | head -20 | while read vfile; do
    FAILED=$(jq 'select(.success == false) | .meta.expectation_suite_name' "$vfile" 2>/dev/null)
    if [ -n "$FAILED" ]; then
        jq -r '"\(.meta.expectation_suite_name)\t\(.meta.run_id.run_time[0:16] // "?")\t\([.results[] | select(.success == false)] | length) failed"' "$vfile"
    fi
done | column -t
```

### Failed Expectation Details

```bash
#!/bin/bash
VALIDATION_FILE="${1:?Validation result file path required}"

echo "=== Validation Summary ==="
ge_parse_validation "$VALIDATION_FILE"

echo ""
echo "=== Failed Expectations ==="
jq -r '
    .results[] | select(.success == false) |
    "\(.expectation_config.expectation_type)\t\(.expectation_config.kwargs.column // "table-level")\tObserved: \(.result.observed_value // "N/A")"
' "$VALIDATION_FILE" | column -t | head -20

echo ""
echo "=== Unexpected Values (sample) ==="
jq -r '
    .results[] | select(.success == false) |
    select(.result.partial_unexpected_list != null) |
    "\(.expectation_config.kwargs.column): \(.result.partial_unexpected_list[:5] | join(", "))"
' "$VALIDATION_FILE" | head -10
```

### Checkpoint Execution

```bash
#!/bin/bash
CHECKPOINT="${1:?Checkpoint name required}"
DRY_RUN="${2:-true}"

if [ "$DRY_RUN" = "true" ]; then
    echo "=== Checkpoint Config: $CHECKPOINT ==="
    CKPT_FILE="${GE_BASE}/checkpoints/${CHECKPOINT}.yml"
    python3 -c "
import yaml
with open('${CKPT_FILE}') as f:
    config = yaml.safe_load(f)
print(f'Class: {config.get(\"class_name\", \"?\")}')
for vc in config.get('validations', []):
    print(f'  Suite: {vc.get(\"expectation_suite_name\", \"?\")}\tBatch: {vc.get(\"batch_request\", {}).get(\"datasource_name\", \"?\")}')
" 2>/dev/null
    echo ""
    echo "To execute, call with dry_run=false"
else
    echo "=== Running Checkpoint: $CHECKPOINT ==="
    cd "${GE_DIR}" && great_expectations checkpoint run "$CHECKPOINT" 2>&1 | tail -20
fi
```

### Data Docs and Documentation

```bash
#!/bin/bash
echo "=== Data Docs Sites ==="
python3 -c "
import yaml
with open('${GE_BASE}/great_expectations.yml') as f:
    config = yaml.safe_load(f)
for name, site in config.get('data_docs_sites', {}).items():
    store = site.get('store_backend', {})
    print(f'{name}\t{store.get(\"class_name\", \"?\")}\t{store.get(\"base_directory\", store.get(\"bucket\", \"?\"))}')
" 2>/dev/null | column -t

echo ""
echo "=== Build Data Docs ==="
echo "Run: great_expectations docs build --no-view"

echo ""
echo "=== Expectation Coverage ==="
ge_list_suites | while read suite; do
    SUITE_FILE="${GE_BASE}/expectations/$(echo $suite | tr '.' '/').json"
    TYPES=$(jq -r '[.expectations[].expectation_type] | unique | join(", ")' "$SUITE_FILE" 2>/dev/null)
    echo -e "${suite}\t${TYPES}"
done | column -t | head -15
```

## Output Format

Present results as a structured report:
```
Analyzing Great Expectations Report
═══════════════════════════════════
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

- **Project root**: GE expects to be run from the project root containing `great_expectations/` directory
- **Suite naming**: Suite names use dots as separators that map to directory structure — `my_suite.orders` maps to `expectations/my_suite/orders.json`
- **Validation storage**: Results in `uncommitted/validations/` are gitignored by default — use a configured validations store for persistence
- **Config versions**: GE has had major config format changes (v2 vs v3) — check `config_version` in `great_expectations.yml`
- **Batch request**: V3 API uses batch requests with datasource/data_connector/data_asset — all three must match
- **Runtime vs stored**: Expectations can be created at runtime (not persisted) — only suites saved to disk appear in file listing
- **Checkpoint vs suite**: Checkpoints orchestrate validation runs against specific data batches — suites define the rules only
- **Data docs staleness**: Data docs are static HTML and must be rebuilt after new validations — they don't auto-update
- **Cloud vs OSS**: Great Expectations Cloud has its own API — OSS relies on file-based configuration and CLI
