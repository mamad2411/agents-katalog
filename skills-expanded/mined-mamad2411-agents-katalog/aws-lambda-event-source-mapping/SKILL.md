---
name: aws-lambda-event-source-mapping
description: >
  AWS Lambda event source mappings (ESM) for owned accounts: SQS, Kinesis, DynamoDB
  Streams, Kafka configurations, batching, partial batch failure, starting positions,
  scaling, and IAM. Use when wiring stream/queue consumers to Lambda — not for
  unauthorized invocation of functions you do not own.
---

# AWS Lambda Event Source Mapping

## Scope And Authorization

- **In scope:** Lambda functions and event sources in AWS accounts you operate under authorization.
- **Out of scope:** Creating mappings that drain third-party queues/streams without authority.
- Bad ESM settings cause data loss, poison-pill loops, or cost spikes — change with care.
- Ensure function IAM can read the source and write DLQs.
- Pair with `aws-lambda-least-privilege` and `retry-backoff-patterns`.

## When To Use

- Creating/updating ESM for SQS, Kinesis, DynamoDB Streams, MSK/self-managed Kafka.
- Tuning `BatchSize`, `MaximumBatchingWindowInSeconds`, parallelization.
- Implementing `ReportBatchItemFailures` for partial success.
- Setting `BisectOnFunctionError`, retry attempts, destinations on failure.
- Debugging lag, iterator age, or stuck shards.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Function IAM role design | `aws-lambda-least-privilege` |
| SnapStart cold start | `aws-lambda-snapstart` |
| Kinesis on-demand capacity | `aws-kinesis-on-demand` |
| MSK IAM auth | `aws-msk-iam-auth` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Source | Key ESM knobs |
| --- | --- |
| SQS | batch size, batching window, scaling concurrency, partial failures |
| Kinesis / DDB Streams | starting position, parallelization factor, bisect, max retry, age |
| MSK / Kafka | topics, consumer group, auth, VPC |
| Common | enabled/disabled, filters, function response types |

## Partial Batch Failure (SQS / Streams)

```json
{
  "batchItemFailures": [
    { "itemIdentifier": "message-id-or-sequence" }
  ]
}
```

Function must report failures correctly or entire batch retries.

## Workflow

### 1. Confirm scope and success criteria

1. Record function, source ARN, throughput, ordering needs, idempotency.
2. Success: lag within SLO; poison messages to DLQ; no unbounded retries; IAM least privilege.
3. Define whether ordering per partition/group must be preserved.

### 2. Inventory mappings

```bash
aws lambda list-event-source-mappings --function-name "$FN"
aws lambda get-event-source-mapping --uuid "$UUID"
aws sqs get-queue-attributes --queue-url "$URL" --attribute-names All
aws kinesis describe-stream-summary --stream-name "$STREAM"
```

1. Note `State` (Enabled/Disabled/problems).
2. Check DLQ configuration on queue or on ESM/failure destination.
3. Review filter criteria JSON.

### 3. Baseline

1. Metrics: `IteratorAge`, `ApproximateAgeOfOldestMessage`, `NumberOfMessagesSent`, function errors, throttles.
2. Sample payload size for batch sizing.
3. Current reserved concurrency on function (can starve ESM).

### 4. Configure ESM safely

**SQS example:**

```bash
aws lambda create-event-source-mapping \
  --function-name order-worker \
  --event-source-arn arn:aws:sqs:REGION:ACCT:orders \
  --batch-size 10 \
  --maximum-batching-window-in-seconds 5 \
  --function-response-types ReportBatchItemFailures
```

**Kinesis example:**

```bash
aws lambda create-event-source-mapping \
  --function-name stream-worker \
  --event-source-arn arn:aws:kinesis:REGION:ACCT:stream/orders \
  --starting-position LATEST \
  --batch-size 100 \
  --parallelization-factor 2 \
  --bisect-batch-on-function-error \
  --maximum-retry-attempts 3 \
  --destination-config '{"OnFailure":{"Destination":"arn:aws:sqs:REGION:ACCT:orders-dlq"}}'
```

**Hardening**

1. Idempotent handlers (at-least-once delivery).
2. Timeouts: function timeout > processing time for max batch.
3. Filter criteria to drop noise early.
4. For SQS: visibility timeout ≥ function timeout × retries budget.
5. Disable ESM before dangerous deploys; re-enable after.
6. Kafka: secure auth and VPC config; restrict topics.

### 5. Verify with evidence

```bash
aws lambda get-event-source-mapping --uuid "$UUID"
# Send test messages; confirm invocations and success metrics
# Force handler error on one record → only that record retries / DLQ
```

1. Lag metrics stable under load test.
2. Reserved concurrency: ESM does not get hard-stuck at zero concurrency.
3. IAM AccessDenied does not appear in function logs for source reads.

### 6. Observe and harden

1. Alarms: iterator age / oldest message age, ESM failure states, DLQ depth.
2. Dashboards per stream/queue consumer.
3. Review batch size after payload growth.

### 7. Hand off

1. Document source → function → DLQ map.
2. Runbook: disable ESM, drain, replay from DLQ/archive.
3. Code standards for batch failure reporting.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Failures | partial batch + DLQ | infinite whole-batch retry |
| Timeout | aligned with visibility/batch | 3s timeout, 10k records |
| Idempotency | keys on event id | double side effects OK? |
| Concurrency | understood reserved limits | reserved 0 on consumer fn |
| Start position | intentional TRIM/LATEST | accidental reprocess entire stream in prod |
| Filters | drop junk early | process everything then ignore |

## Output Checklist

- [ ] Source/function/SLO recorded
- [ ] ESM settings inventory complete
- [ ] Batching/retry/DLQ configured
- [ ] Partial failure support implemented if used
- [ ] Timeouts/visibility aligned
- [ ] IAM permissions verified
- [ ] Lag and error alarms set
- [ ] Test evidence for success and poison pill
- [ ] Runbook for disable/replay
- [ ] `aws-lambda-least-privilege` applied

## Rules

- Owned event sources only.
- Assume at-least-once delivery; design idempotency.
- Never ignore DLQ and iterator age.
- Align timeouts, batch sizes, and concurrency deliberately.
- Focus on ESM behavior; function IAM and SnapStart in neighbor skills.
