---
name: managing-aws-dynamodb-deep
description: |
  Use when working with Aws Dynamodb Deep — aWS DynamoDB deep-dive management
  covering table configurations, capacity analysis, GSI/LSI health, auto-scaling
  policies, streams, backups, contributor insights, and TTL settings. Use when
  performing deep analysis of DynamoDB tables, optimizing capacity and
  throughput, debugging throttling, or auditing table configurations beyond
  basic inventory.
connection_type: aws
preload: false
---

# AWS DynamoDB Deep-Dive Skill

Deep analysis of DynamoDB tables, capacity planning, index health, and operational metrics.

## MANDATORY: Discovery-First Pattern

**Always list tables and get basic descriptions before deep-diving.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== DynamoDB Tables ==="
TABLES=$(aws dynamodb list-tables --output text --query 'TableNames[]')
echo "$TABLES" | tr '\t' '\n'

echo ""
echo "=== Table Summary ==="
for table in $TABLES; do
  aws dynamodb describe-table --table-name "$table" --output text \
    --query "Table.[TableName,TableStatus,BillingModeSummary.BillingMode,ItemCount,TableSizeBytes,GlobalSecondaryIndexes[].IndexName|join(',',@)]" &
done
wait

echo ""
echo "=== Auto-Scaling Targets ==="
aws application-autoscaling describe-scalable-targets --service-namespace dynamodb --output text \
  --query 'ScalableTargets[].[ResourceId,ScalableDimension,MinCapacity,MaxCapacity]' 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
START_TIME=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")

echo "=== Throttle Events (7d) ==="
for table in $(aws dynamodb list-tables --output text --query 'TableNames[]'); do
  {
    read_throttle=$(aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name ReadThrottleEvents \
      --dimensions Name=TableName,Value="$table" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    write_throttle=$(aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name WriteThrottleEvents \
      --dimensions Name=TableName,Value="$table" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tReadThrottles:%s\tWriteThrottles:%s\n" "$table" "${read_throttle:-0}" "${write_throttle:-0}"
  } &
done
wait

echo ""
echo "=== Consumed vs Provisioned Capacity ==="
for table in $(aws dynamodb list-tables --output text --query 'TableNames[]'); do
  {
    consumed_read=$(aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name ConsumedReadCapacityUnits \
      --dimensions Name=TableName,Value="$table" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    consumed_write=$(aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name ConsumedWriteCapacityUnits \
      --dimensions Name=TableName,Value="$table" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    printf "%s\tAvgReadCU:%.1f\tAvgWriteCU:%.1f\n" "$table" "${consumed_read:-0}" "${consumed_write:-0}"
  } &
done
wait

echo ""
echo "=== GSI Status ==="
for table in $(aws dynamodb list-tables --output text --query 'TableNames[]'); do
  aws dynamodb describe-table --table-name "$table" --output text \
    --query "Table.GlobalSecondaryIndexes[].[\"$table\",IndexName,IndexStatus,ItemCount,Projection.ProjectionType]" 2>/dev/null &
done
wait

echo ""
echo "=== Streams & TTL ==="
for table in $(aws dynamodb list-tables --output text --query 'TableNames[]'); do
  {
    stream=$(aws dynamodb describe-table --table-name "$table" --output text \
      --query 'Table.StreamSpecification.StreamEnabled')
    ttl=$(aws dynamodb describe-time-to-live --table-name "$table" --output text \
      --query 'TimeToLiveDescription.TimeToLiveStatus')
    printf "%s\tStream:%s\tTTL:%s\n" "$table" "${stream:-disabled}" "${ttl:-DISABLED}"
  } &
done
wait

echo ""
echo "=== Backups ==="
aws dynamodb list-backups --output text \
  --query 'BackupSummaries[].[TableName,BackupName,BackupStatus,BackupCreationDateTime,BackupType]' | head -10

echo ""
echo "=== Contributor Insights ==="
for table in $(aws dynamodb list-tables --output text --query 'TableNames[]'); do
  aws dynamodb describe-contributor-insights --table-name "$table" --output text \
    --query "[TableName,ContributorInsightsStatus]" 2>/dev/null &
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: TableName, Metric, Value
- Aggregate capacity metrics as averages over the period
- Never dump full table items -- show metadata and metrics only

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

- **Billing mode**: PAY_PER_REQUEST vs PROVISIONED -- capacity metrics differ significantly
- **GSI throttling**: GSIs have independent capacity -- throttled GSIs can cause table-level write throttling
- **Hot partitions**: Use Contributor Insights to identify hot partition keys
- **On-demand scaling**: On-demand tables can throttle if traffic exceeds 2x previous peak within 30 minutes
- **Auto-scaling delay**: Auto-scaling reacts to CloudWatch alarms with ~5 minute delay -- not instant
- **Item size**: Max 400KB per item -- check `AverageItemSize` from table description
- **Stream retention**: DynamoDB Streams retain data for 24 hours only -- process events promptly
- **Backup types**: AWS_BACKUP (managed by AWS Backup), SYSTEM (continuous backups), USER (on-demand)
