---
name: analyzing-dynamodb
description: |
  Use when working with Dynamodb — amazon DynamoDB table analysis, capacity mode
  evaluation, GSI/LSI usage, item access patterns, and cost optimization.
connection_type: aws
preload: false
---

# DynamoDB Analysis Skill

Analyze and optimize DynamoDB tables with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated table names and attribute errors.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List all tables in the region
aws dynamodb list-tables --output json | jq -r '.TableNames[]'

# 2. Describe target table (schema, capacity, indexes)
aws dynamodb describe-table --table-name "$TABLE_NAME" --output json | jq '{
  TableName: .Table.TableName,
  Status: .Table.TableStatus,
  ItemCount: .Table.ItemCount,
  TableSizeBytes: .Table.TableSizeBytes,
  BillingMode: .Table.BillingModeSummary.BillingMode,
  KeySchema: .Table.KeySchema,
  AttributeDefinitions: .Table.AttributeDefinitions,
  GSICount: (.Table.GlobalSecondaryIndexes | length // 0),
  LSICount: (.Table.LocalSecondaryIndexes | length // 0)
}'

# 3. Sample items to understand actual attribute names
aws dynamodb scan --table-name "$TABLE_NAME" --max-items 5 --output json | jq '.Items[0]'
```

**Phase 1 outputs:**
- List of tables in the account/region
- Table schema with key attributes and billing mode
- Sample items to understand actual attribute names

### Phase 2: Analysis (only after Phase 1)

Only reference tables, attributes, and indexes confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core DynamoDB helper — always use this
ddb_cmd() {
    aws dynamodb "$@" --output json
}

# Describe table helper
ddb_describe() {
    local table="$1"
    ddb_cmd describe-table --table-name "$table"
}

# CloudWatch metric helper for DynamoDB
ddb_metric() {
    local table="$1" metric="$2" stat="${3:-Sum}" period="${4:-300}"
    aws cloudwatch get-metric-statistics \
        --namespace AWS/DynamoDB \
        --metric-name "$metric" \
        --dimensions Name=TableName,Value="$table" \
        --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)" \
        --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
        --period "$period" \
        --statistics "$stat" \
        --output json
}
```

## Anti-Hallucination Rules

- **NEVER reference a table name** without confirming it exists via `list-tables`
- **NEVER reference attribute names** without seeing them in `describe-table` or a sample scan
- **NEVER assume GSI/LSI names** — always get them from `describe-table`
- **NEVER guess capacity units** — always read from table description or CloudWatch metrics
- **NEVER assume billing mode** — confirm on-demand vs provisioned from table description

## Safety Rules

- **READ-ONLY ONLY**: Use only describe-table, list-tables, scan (with --max-items), query, get-item
- **FORBIDDEN**: create-table, delete-table, update-table, put-item, delete-item, batch-write-item without explicit user request
- **ALWAYS add `--max-items`** to scan operations — tables can have billions of items
- **NEVER** run full table scans on production without `--max-items`
- **Use `--select COUNT`** when you only need item counts, not full items

## Common Operations

### Table Health Overview

```bash
#!/bin/bash
echo "=== DynamoDB Tables ==="
TABLES=$(aws dynamodb list-tables --output json | jq -r '.TableNames[]')

for TABLE in $TABLES; do
    INFO=$(ddb_describe "$TABLE" | jq -r '.Table | "\(.TableName)\t\(.TableStatus)\t\(.ItemCount) items\t\((.TableSizeBytes/1024/1024)|round)MB\t\(.BillingModeSummary.BillingMode // "PROVISIONED")"')
    echo "$INFO"
done

echo ""
echo "=== Table Details: $TABLE_NAME ==="
ddb_describe "$TABLE_NAME" | jq '.Table | {
    KeySchema,
    AttributeDefinitions,
    BillingMode: .BillingModeSummary.BillingMode,
    ProvisionedThroughput: (if .BillingModeSummary.BillingMode == "PAY_PER_REQUEST" then "On-Demand" else .ProvisionedThroughput end),
    ItemCount,
    TableSizeMB: ((.TableSizeBytes/1024/1024)|round)
}'
```

### GSI/LSI Analysis

```bash
#!/bin/bash
TABLE_NAME="$1"

echo "=== Global Secondary Indexes ==="
ddb_describe "$TABLE_NAME" | jq -r '.Table.GlobalSecondaryIndexes[]? | "\(.IndexName)\t\(.IndexStatus)\t\(.ItemCount) items\t\(.KeySchema | map(.AttributeName + "=" + .KeyType) | join(","))\tProjection=\(.Projection.ProjectionType)"'

echo ""
echo "=== Local Secondary Indexes ==="
ddb_describe "$TABLE_NAME" | jq -r '.Table.LocalSecondaryIndexes[]? | "\(.IndexName)\t\(.KeySchema | map(.AttributeName + "=" + .KeyType) | join(","))\tProjection=\(.Projection.ProjectionType)"'

echo ""
echo "=== GSI Capacity Utilization ==="
ddb_describe "$TABLE_NAME" | jq -r '.Table.GlobalSecondaryIndexes[]? | select(.ProvisionedThroughput) | "\(.IndexName)\tRCU=\(.ProvisionedThroughput.ReadCapacityUnits)\tWCU=\(.ProvisionedThroughput.WriteCapacityUnits)"'
```

### Capacity & Throttling Analysis

```bash
#!/bin/bash
TABLE_NAME="$1"

echo "=== Consumed Read Capacity ==="
ddb_metric "$TABLE_NAME" "ConsumedReadCapacityUnits" "Sum" 300 | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | "\(.Timestamp)\t\(.Sum)"'

echo ""
echo "=== Consumed Write Capacity ==="
ddb_metric "$TABLE_NAME" "ConsumedWriteCapacityUnits" "Sum" 300 | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | "\(.Timestamp)\t\(.Sum)"'

echo ""
echo "=== Throttled Requests (last 1h) ==="
for METRIC in ReadThrottleEvents WriteThrottleEvents; do
    echo "--- $METRIC ---"
    ddb_metric "$TABLE_NAME" "$METRIC" "Sum" 300 | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | select(.Sum > 0) | "\(.Timestamp)\t\(.Sum)"'
done
```

### Access Pattern Analysis

```bash
#!/bin/bash
TABLE_NAME="$1"

echo "=== Successful Request Latency ==="
ddb_metric "$TABLE_NAME" "SuccessfulRequestLatency" "Average" 60 | jq -r '.Datapoints | sort_by(.Timestamp) | .[-5:][] | "\(.Timestamp)\t\(.Average)ms"'

echo ""
echo "=== System Errors ==="
ddb_metric "$TABLE_NAME" "SystemErrors" "Sum" 300 | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | select(.Sum > 0) | "\(.Timestamp)\t\(.Sum)"'

echo ""
echo "=== User Errors ==="
ddb_metric "$TABLE_NAME" "UserErrors" "Sum" 300 | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | select(.Sum > 0) | "\(.Timestamp)\t\(.Sum)"'
```

### Cost Estimation

```bash
#!/bin/bash
TABLE_NAME="$1"

echo "=== Table Size & Item Count ==="
ddb_describe "$TABLE_NAME" | jq '.Table | {
    TableSizeGB: ((.TableSizeBytes/1024/1024/1024)*100|round/100),
    ItemCount: .ItemCount,
    BillingMode: .BillingModeSummary.BillingMode,
    StorageCostEstimate: "\(((.TableSizeBytes/1024/1024/1024)*0.25)*100|round/100) USD/month (at $0.25/GB)"
}'

echo ""
echo "=== GSI Storage Overhead ==="
ddb_describe "$TABLE_NAME" | jq '[.Table.GlobalSecondaryIndexes[]? | {IndexName, SizeGB: ((.IndexSizeBytes/1024/1024/1024)*100|round/100)}]'
```

## Output Format

Present results as a structured report:
```
Analyzing Dynamodb Report
═════════════════════════
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

- **Scan vs Query**: Scans read every item — always prefer Query with key conditions for production analysis
- **Eventually consistent reads**: Default reads are eventually consistent; specify `--consistent-read` only when needed
- **GSI eventual consistency**: GSI data is always eventually consistent — do not rely on immediate GSI updates
- **Capacity calculation**: 1 RCU = 1 strongly consistent read/s (4KB) or 2 eventually consistent reads/s; 1 WCU = 1 write/s (1KB)
- **Hot partitions**: Adaptive capacity helps but does not eliminate hot key issues — check partition key distribution
- **Item size limit**: 400KB per item — check for items approaching this limit
- **--max-items vs --limit**: `--max-items` limits CLI output (client-side); `--limit` limits DynamoDB scan (server-side and costs less RCU)
