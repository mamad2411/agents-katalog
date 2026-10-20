---
name: aws-kinesis-on-demand
description: >
  Amazon Kinesis Data Streams on-demand mode for owned accounts: capacity mode
  selection, scaling behavior, shard-level metrics, cost controls, encryption, and
  consumer design (enhanced fan-out vs shared). Use when operating or migrating
  streams to on-demand — not for flooding streams outside authorization.
---

# AWS Kinesis On-Demand

## Scope And Authorization

- **In scope:** Kinesis Data Streams in AWS accounts you own or operate under authorization.
- **Out of scope:** Write floods or unauthorized consumption of third-party streams.
- On-demand absorbs spikes but can incur surprise cost — set budgets and monitoring.
- Encrypt streams with KMS; restrict IAM for put/get.
- Pair producers/consumers with `code-quality-standards` and `retry-backoff-patterns`.

## When To Use

- Choosing **on-demand** vs **provisioned** shard capacity.
- Migrating mode with `UpdateStreamMode`.
- Handling hot-key / partition key design under on-demand.
- Configuring enhanced fan-out consumers and retention.
- Cost anomaly response after traffic spikes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Kafka/MSK IAM auth | `aws-msk-iam-auth` |
| EventBridge archive/replay | `aws-eventbridge-archive` |
| Lambda event source mapping | `aws-lambda-event-source-mapping` |
| KMS key policies | `aws-kms-key-policy-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mode | Characteristics |
| --- | --- |
| Provisioned | You set shard count; predictable cost; manual/autoscaling apps |
| On-demand | AWS scales write/read throughput; pay for usage; still partition-key aware |
| Limits | Account/stream quotas still apply — request increases if needed |
| Encryption | KMS CMK recommended for sensitive data |
| Retention | 24h default up to extended retention for replay |

## On-Demand vs Provisioned

| Prefer on-demand | Prefer provisioned |
| --- | --- |
| Spiky / unknown traffic | Stable high volume with tuned shards |
| Ops simplicity | Strict cost caps via shard count |
| Fast start | Extreme scale with careful shard planning |

## Workflow

### 1. Confirm scope and success criteria

1. Record stream names, producers, consumers, peak MB/s, data class.
2. Success: no `ProvisionedThroughputExceeded` for expected peaks; p99 producer latency OK; cost within budget; encryption on.
3. Define partition key strategy (avoid single hot key).

### 2. Inventory streams

```bash
aws kinesis list-streams
aws kinesis describe-stream-summary --stream-name "$STREAM"
aws kinesis describe-stream --stream-name "$STREAM" --query "StreamDescription.{Mode:StreamModeDetails,Enc:EncryptionType,Ret:RetentionPeriodHours,Shards:Shards}"
```

1. Note consumers (Lambda, KCL, Firehose, analytics).
2. CloudWatch: `IncomingBytes`, `WriteProvisionedThroughputExceeded`, `ReadProvisionedThroughputExceeded`, `OnDemandStreamCount` metrics as applicable.

### 3. Baseline

1. Peak write bytes/records from last month.
2. Error rates and iterator age for consumers.
3. Current IAM policies for producers.

### 4. Configure on-demand and harden

```bash
aws kinesis update-stream-mode \
  --stream-arn "$STREAM_ARN" \
  --stream-mode-details StreamMode=ON_DEMAND

aws kinesis start-stream-encryption \
  --stream-name "$STREAM" \
  --encryption-type KMS \
  --key-id alias/kinesis-prod
```

**Producer design**

1. Partition keys with high cardinality for even distribution.
2. Batch `PutRecords` with partial failure retry of failed records only.
3. Bound retries; use exponential backoff (`retry-backoff-patterns`).

**Consumer design**

1. Enhanced fan-out for dedicated throughput per consumer when fan-out is high.
2. Lambda ESM: parallelization and bisect on error settings (`aws-lambda-event-source-mapping`).
3. Monitor `GetRecords.IteratorAgeMilliseconds` / consumer lag.

**Cost controls**

1. AWS Budgets on Kinesis.
2. Alarms on IncomingBytes spikes.
3. Lifecycle: delete unused streams; shorten retention if compliance allows.

### 5. Verify with evidence

```bash
aws kinesis describe-stream-summary --stream-name "$STREAM"
# Load test in non-prod approximating peak
# Expect no sustained throughput exceeded for designed load
aws cloudwatch get-metric-statistics --namespace AWS/Kinesis --metric-name IncomingBytes \
  --dimensions Name=StreamName,Value="$STREAM" --start-time ... --end-time ... --period 60 --statistics Sum
```

1. Fail a consumer → iterator age rises → alarm fires.
2. IAM deny test: unauthorized principal cannot PutRecord.
3. Confirm KMS key policy allows stream service use.

### 6. Observe and harden

1. Dashboard: traffic, errors, iterator age, cost.
2. Quarterly mode review (on-demand still optimal?).
3. Access Analyzer / IAM least privilege on stream ARNs.

### 7. Hand off

1. Stream catalog: mode, key strategy, consumers, owners.
2. Runbook for throttling and cost spikes.
3. IaC default encryption and mode.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | high cardinality | single static partition key |
| Mode | on-demand for spikes | provisioned under-scaled, silent loss |
| Crypto | KMS CMK | NONE on sensitive data |
| Consumers | lag alarms | ignore iterator age |
| Cost | budgets + alarms | unlimited surprise bill |
| IAM | stream-scoped | `kinesis:*` on `*` |

## Output Checklist

- [ ] Streams/producers/consumers recorded
- [ ] Mode decision documented
- [ ] Encryption enabled
- [ ] Partition key strategy set
- [ ] Metrics/alarms for throughput, lag, cost
- [ ] Load evidence for expected peaks
- [ ] IAM least privilege applied
- [ ] Consumer failure runbook ready
- [ ] `code-quality-standards` on clients

## Rules

- Owned streams only; do not load-test production without approval.
- Design partition keys deliberately under any mode.
- Monitor cost as a first-class signal for on-demand.
- Encrypt sensitive streams with KMS.
- Focus on on-demand stream ops; Lambda ESM and MSK elsewhere.
