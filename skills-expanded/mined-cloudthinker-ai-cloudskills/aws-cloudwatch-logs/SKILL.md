---
name: aws-cloudwatch-logs
description: |
  Use when working with Aws Cloudwatch Logs — aWS CloudWatch Logs group
  management, Logs Insights query execution, metric filter analysis, retention
  policy review, and subscription filter management. Covers log group inventory,
  storage cost optimization, query patterns, and cross-account log aggregation.
connection_type: aws
preload: false
---

# AWS CloudWatch Logs Skill

Analyze AWS CloudWatch Logs with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-cloudwatch-logs/` → CloudWatch Logs-specific analysis (log groups, insights, metric filters)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for log_group in $log_groups; do
  get_log_group_details "$log_group" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List log groups with size and retention
list_log_groups() {
  aws logs describe-log-groups \
    --output text \
    --query 'logGroups[].[logGroupName,storedBytes,retentionInDays,metricFilterCount]' | head -50
}

# Get log group details
describe_log_group() {
  local log_group=$1
  aws logs describe-log-groups --log-group-name-prefix "$log_group" \
    --output text \
    --query 'logGroups[0].[logGroupName,storedBytes,retentionInDays,metricFilterCount,kmsKeyId]'
}

# Run CloudWatch Logs Insights query
run_insights_query() {
  local log_group=$1 query=$2 hours=${3:-1}
  local end_time start_time
  end_time=$(date +%s)
  start_time=$((end_time - hours * 3600))

  local query_id
  query_id=$(aws logs start-query \
    --log-group-name "$log_group" \
    --start-time "$start_time" --end-time "$end_time" \
    --query-string "$query" \
    --output text --query 'queryId')

  sleep 3
  aws logs get-query-results --query-id "$query_id" \
    --output text \
    --query 'results[][].[field,value]'
}

# List metric filters for a log group
list_metric_filters() {
  local log_group=$1
  aws logs describe-metric-filters --log-group-name "$log_group" \
    --output text \
    --query 'metricFilters[].[filterName,filterPattern,metricTransformations[0].metricName,metricTransformations[0].metricNamespace]'
}

# List subscription filters
list_subscriptions() {
  local log_group=$1
  aws logs describe-subscription-filters --log-group-name "$log_group" \
    --output text \
    --query 'subscriptionFilters[].[filterName,destinationArn,filterPattern]'
}
```

## Common Operations

### 1. Log Group Inventory with Storage Cost

```bash
#!/bin/bash
export AWS_PAGER=""
aws logs describe-log-groups \
  --output text \
  --query 'logGroups[].[logGroupName,storedBytes,retentionInDays]' \
  | awk '{printf "%s\t%.2f_GB\t%s_days\n", $1, $2/1073741824, ($3=="None"?"NEVER":$3)}' \
  | sort -t$'\t' -k2 -rn | head -20
```

### 2. Log Groups Without Retention (Cost Risk)

```bash
#!/bin/bash
export AWS_PAGER=""
aws logs describe-log-groups \
  --output text \
  --query 'logGroups[?!retentionInDays].[logGroupName,storedBytes]' \
  | awk '{printf "%s\t%.2f_GB\tNO_RETENTION\n", $1, $2/1073741824}' \
  | sort -t$'\t' -k2 -rn | head -20
```

### 3. Logs Insights Error Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
LOG_GROUP=$1
END=$(date +%s)
START=$((END - 86400))
QUERY_ID=$(aws logs start-query \
  --log-group-name "$LOG_GROUP" \
  --start-time "$START" --end-time "$END" \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR|Exception/ | stats count() by bin(1h)' \
  --output text --query 'queryId')
sleep 5
aws logs get-query-results --query-id "$QUERY_ID" \
  --output text \
  --query 'results[][].[field,value]'
```

### 4. Metric Filter Audit

```bash
#!/bin/bash
export AWS_PAGER=""
LOG_GROUPS=$(aws logs describe-log-groups --output text --query 'logGroups[?metricFilterCount>`0`].logGroupName')
for lg in $LOG_GROUPS; do
  aws logs describe-metric-filters --log-group-name "$lg" \
    --output text \
    --query "metricFilters[].[\"$lg\",filterName,filterPattern]" &
done
wait
```

### 5. Subscription Filter Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
LOG_GROUPS=$(aws logs describe-log-groups --output text --query 'logGroups[].logGroupName' | head -50)
for lg in $LOG_GROUPS; do
  aws logs describe-subscription-filters --log-group-name "$lg" \
    --output text \
    --query "subscriptionFilters[].[\"$lg\",filterName,destinationArn]" 2>/dev/null &
done
wait
```

## Anti-Hallucination Rules

1. **storedBytes is compressed size** - CloudWatch Logs reports compressed storage. Actual ingested data is larger. Do not equate stored bytes with ingested bytes.
2. **Retention null = never expire** - A null/None retentionInDays means logs are kept forever. This is the default and a major cost risk.
3. **Insights query is async** - `start-query` returns a query ID. You must poll `get-query-results` until status is "Complete". Allow 3-5 seconds for simple queries.
4. **Insights query limits** - Maximum 20 concurrent queries per account/region. Results limited to 10,000 rows. Queries time out after 60 minutes.
5. **Metric filter pattern syntax** - Metric filter patterns are NOT regex. They use a specific pattern syntax with spaces for AND, quotes for exact match, and brackets for JSON fields.

## Output Format

Present results as a structured report:
```
Aws Cloudwatch Logs Report
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

- **Pagination**: `describe-log-groups` returns max 50 groups per page by default. Use `--limit` and pagination for accounts with many log groups.
- **Log group naming**: Lambda uses `/aws/lambda/`, API Gateway uses `API-Gateway-Execution-Logs_`, ECS uses custom names. Do not assume naming patterns.
- **Cross-account**: CloudWatch Logs can stream to another account via subscription filters. Use `describe-subscription-filters` to detect this.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Insights cost**: CloudWatch Logs Insights charges $0.005 per GB of data scanned. Use time range filters and `limit` to control cost.
