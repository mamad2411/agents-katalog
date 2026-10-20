---
name: gcp-firestore-deep
description: |
  Use when working with Gcp Firestore Deep — google Cloud Firestore document and
  collection analysis, index management, security rules review, usage
  monitoring, and performance diagnostics via gcloud CLI.
connection_type: gcp
preload: false
---

# Firestore Skill

Manage and analyze Google Cloud Firestore using `gcloud firestore` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume database names, collection names, or index configurations.

```bash
# Discover Firestore databases
gcloud firestore databases list --format=json \
  | jq '[.[] | {name: .name, type: .type, locationId: .locationId, concurrencyMode: .concurrencyMode, appEngineIntegrationMode: .appEngineIntegrationMode, deleteProtectionState: .deleteProtectionState}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for db in $(gcloud firestore databases list --format="value(name)" | xargs -I{} basename {}); do
  {
    gcloud firestore indexes composite list --database="$db" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# List composite indexes
list_composite_indexes() {
  local db="${1:-(default)}"
  gcloud firestore indexes composite list --database="$db" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, collection: .collectionGroup, state: .state, fields: [.fields[] | {path: .fieldPath, order: .order // .arrayConfig}]}]'
}

# List field indexes (overrides)
list_field_overrides() {
  local db="${1:-(default)}"
  gcloud firestore indexes fields list --database="$db" --format=json \
    | jq '[.[] | select(.indexConfig.indexes) | {field: .name, indexes: .indexConfig.indexes}]'
}

# Export database
export_database() {
  local db="$1" bucket="$2"
  gcloud firestore export "gs://$bucket" --database="$db" --format=json
}

# Get database usage metrics
get_firestore_metrics() {
  local project="$1"
  gcloud monitoring time-series list \
    --filter="metric.type=starts_with(\"firestore.googleapis.com/\")" \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format=json --limit=100
}
```

## Common Operations

### 1. Database Overview

```bash
# List databases and their configuration
gcloud firestore databases list --format=json \
  | jq '[.[] | {name: .name | split("/") | last, type: .type, location: .locationId, concurrencyMode: .concurrencyMode, pointInTimeRecovery: .pointInTimeRecoveryEnablement, deleteProtection: .deleteProtectionState}]'
```

### 2. Index Management

```bash
# Composite indexes with build status
list_composite_indexes "(default)"

# Find indexes that are still building
gcloud firestore indexes composite list --database="(default)" --format=json \
  | jq '[.[] | select(.state != "READY") | {collection: .collectionGroup, state: .state, fields: [.fields[] | .fieldPath]}]'

# Field-level index overrides
list_field_overrides "(default)"
```

### 3. Collection Analysis

```bash
# Document count and storage metrics
gcloud monitoring time-series list \
  --filter="metric.type=\"firestore.googleapis.com/document/count\"" \
  --interval-start-time="$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Read/write operation metrics
gcloud monitoring time-series list \
  --filter="metric.type=\"firestore.googleapis.com/api/request_count\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json
```

### 4. Security Rules Review

```bash
# Get current security rules (requires Firebase CLI or REST API)
# Using REST API via gcloud
PROJECT=$(gcloud config get-value project)
gcloud rest firestore.projects.databases.documents --method=GET \
  "https://firestore.googleapis.com/v1/projects/$PROJECT/databases/(default)/documents" 2>/dev/null

# Check rules release history
gcloud firestore databases describe --database="(default)" --format=json
```

### 5. Usage and Performance Monitoring

```bash
# Active connections
gcloud monitoring time-series list \
  --filter="metric.type=\"firestore.googleapis.com/network/active_connections\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Snapshot listeners
gcloud monitoring time-series list \
  --filter="metric.type=\"firestore.googleapis.com/network/snapshot_listeners\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Rule evaluation metrics
gcloud monitoring time-series list \
  --filter="metric.type=\"firestore.googleapis.com/rules/evaluation_count\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json
```

## Output Format

Present results as a structured report:
```
Gcp Firestore Deep Report
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

## Common Pitfalls

1. **Database naming**: The default database is named `(default)` with parentheses. Always quote it in commands to avoid shell interpretation.
2. **Index build time**: Composite index creation can take minutes to hours depending on data volume. Check `state` field before querying with new indexes.
3. **Hot spots**: Sequential document IDs (timestamps, auto-increment) cause write hot spots. Check for monotonically increasing key patterns.
4. **Read-after-write**: In multi-region databases, strong consistency is only guaranteed within a single document. Cross-document reads may see stale data.
5. **Cost model**: Firestore charges per document read/write/delete, not per query. A query returning 1000 documents costs 1000 read operations.
