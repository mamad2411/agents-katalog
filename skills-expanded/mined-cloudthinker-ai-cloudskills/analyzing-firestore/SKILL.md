---
name: analyzing-firestore
description: |
  Use when working with Firestore — google Cloud Firestore collection analysis,
  index management, security rules review, usage metrics, and query
  optimization.
connection_type: gcp
preload: false
---

# Firestore Analysis Skill

Analyze and optimize Firestore databases with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated collection/field names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List Firestore databases
gcloud firestore databases list --project="$GCP_PROJECT"

# 2. List root collections
gcloud firestore indexes composite list --project="$GCP_PROJECT" --database="$DB_NAME" 2>/dev/null

# 3. List collection groups (via REST API)
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://firestore.googleapis.com/v1/projects/$GCP_PROJECT/databases/$DB_NAME/collectionGroups"

# 4. Sample documents from a collection
gcloud firestore export gs://"$BUCKET"/sample --collection-ids="my_collection" --project="$GCP_PROJECT" 2>/dev/null

# OR via REST API for direct document read
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://firestore.googleapis.com/v1/projects/$GCP_PROJECT/databases/(default)/documents/my_collection?pageSize=5"
```

**Phase 1 outputs:**
- Firestore databases and their modes (Native/Datastore)
- Root collections
- Sample documents to understand actual field names

### Phase 2: Analysis (only after Phase 1)

Only reference collections, documents, and fields confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Firestore REST API helper — always use this
firestore_api() {
    local path="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
        -H "Authorization: Bearer $(gcloud auth print-access-token)" \
        -H "Content-Type: application/json" \
        "https://firestore.googleapis.com/v1/projects/${GCP_PROJECT}/databases/${FIRESTORE_DB:-(default)}/$path"
}

# gcloud Firestore helper
firestore_cmd() {
    gcloud firestore "$@" --project="${GCP_PROJECT}" --database="${FIRESTORE_DB:-(default)}"
}
```

## Anti-Hallucination Rules

- **NEVER reference a collection** without confirming it exists via API discovery
- **NEVER reference field names** without seeing them in sample documents
- **NEVER assume document IDs** — always list documents first
- **NEVER guess index configurations** — always check composite indexes
- **NEVER assume database mode** — check if Native or Datastore mode

## Safety Rules

- **READ-ONLY ONLY**: Use only GET requests, gcloud list/describe commands
- **FORBIDDEN**: POST/PATCH/DELETE to documents, `gcloud firestore delete`, index creation without explicit user request
- **ALWAYS use `pageSize`** parameter to limit document reads
- **Monitor read costs** — each document read is billed
- **Use field masks** to read only necessary fields and reduce read costs

## Common Operations

### Database Overview

```bash
#!/bin/bash
echo "=== Firestore Databases ==="
gcloud firestore databases list --project="$GCP_PROJECT" --format="table(name,type,locationId,deleteProtectionState)"

echo ""
echo "=== Composite Indexes ==="
firestore_cmd indexes composite list --format="table(name,queryScope,state,fields)"

echo ""
echo "=== Field Indexes ==="
firestore_cmd indexes fields list --format="table(name,indexConfig)" 2>/dev/null
```

### Collection Analysis

```bash
#!/bin/bash
COLLECTION="${1:-my_collection}"

echo "=== Sample Documents from $COLLECTION ==="
firestore_api "documents/$COLLECTION?pageSize=5" | jq '.documents[]? | {name: .name, fields: (.fields | keys), createTime, updateTime}'

echo ""
echo "=== Document Count (sampled) ==="
firestore_api "documents/$COLLECTION?pageSize=1&mask.fieldPaths=__name__" | jq '.documents | length'
```

### Security Rules Review

```bash
#!/bin/bash
echo "=== Current Security Rules ==="
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "https://firestore.googleapis.com/v1/projects/$GCP_PROJECT/databases/(default)/documents:runQuery" \
    -X POST -d '{}' 2>/dev/null

# Download rules via Firebase CLI if available
firebase firestore:get-rules --project="$GCP_PROJECT" 2>/dev/null || echo "Firebase CLI not available"
```

### Usage Metrics

```bash
#!/bin/bash
echo "=== Firestore Read/Write Metrics (last 1h) ==="
gcloud monitoring time-series list \
    --project="$GCP_PROJECT" \
    --filter='metric.type="firestore.googleapis.com/document/read_count"' \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format="table(metric.labels,points.value)"

echo ""
echo "=== Active Connections ==="
gcloud monitoring time-series list \
    --project="$GCP_PROJECT" \
    --filter='metric.type="firestore.googleapis.com/network/active_connections"' \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format="table(points.value)" 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Analyzing Firestore Report
══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Billing on reads**: Every document read (including list operations) is billed — use field masks and page limits
- **No COUNT without reading**: Firestore lacks native count — counting requires reading all documents (use aggregation queries in newer versions)
- **Composite index limits**: Maximum 200 composite indexes per database — plan indexes carefully
- **Subcollection queries**: Collection group queries require composite indexes — check before querying across subcollections
- **Document size limit**: 1MB per document — check for documents approaching this limit
- **Security rules**: Open rules (`allow read, write: if true`) are a security risk — always review
