---
name: aws-sns-fifo-ordering
description: >
  Amazon SNS FIFO topics for owned accounts: message group ordering, deduplication
  (content-based vs MessageDeduplicationId), FIFO subscriptions to SQS FIFO, throughput
  limits, and fan-out constraints. Use when designing ordered pub/sub, fixing out-of-order
  processing, or migrating standard SNS to FIFO — not for unordered high-throughput
  standard topics alone or unauthorized account access.
---

# AWS SNS FIFO Ordering

## Scope And Authorization

- **In scope:** SNS FIFO topics and subscriber queues/systems in AWS accounts you own or operate.
- **Out of scope:** Publishing to third-party topics; load testing shared environments without approval.
- FIFO has stricter naming, throughput, and subscription constraints — validate consumer capacity.
- Pair consumer code with `code-quality-standards`; SQS multi-tenant fairness → `aws-sqs-fair-queues`.

## When To Use

- Strict per-entity ordering (e.g. per `accountId` event streams).
- Exactly-once-ish publishing via deduplication window (5 minutes).
- SNS FIFO → SQS FIFO fan-out with ordering preserved per message group.
- Debugging duplicate deliveries or out-of-order business side effects.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SQS fair multi-tenant polling | `aws-sqs-fair-queues` |
| Step Functions orchestration | `aws-step-functions-express` |
| Generic backpressure patterns | `backpressure-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Topic name | Must end with `.fifo` |
| Message group | `MessageGroupId` — order guaranteed **within** group only |
| Dedup | `MessageDeduplicationId` or content-based hashing |
| Subscriptions | FIFO topics require FIFO SQS (or compatible endpoints per current AWS rules) |
| Throughput | Per message group and account/region quotas — plan partitioning |
| Standard vs FIFO | Standard: best-effort order, higher fan-out flexibility |

## Workflow

### 1. Confirm scope and success criteria

1. Ordering key (group id strategy), durability, subscribers, max publish TPS, authorization.
2. Success: messages for same group processed in publish order; duplicates suppressed within window.
3. Accept that **cross-group** order is not guaranteed.

### 2. Inventory topics and subscriptions

```bash
aws sts get-caller-identity
aws sns list-topics
aws sns get-topic-attributes --topic-arn "$TOPIC_ARN"
aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN"
```

1. Confirm `FifoTopic=true` and `ContentBasedDeduplication` setting.
2. Verify SQS queues are FIFO (name `.fifo`) and not standard.
3. Check IAM `sns:Publish` conditions and KMS keys if encrypted.

### 3. Baseline ordering requirements

1. Define business ordering key → `MessageGroupId` (avoid single global group — throughput bottleneck).
2. Define dedup key (natural event id vs body hash).
3. Measure consumer concurrency: multiple consumers on same group serialize at SQS FIFO.

### 4. Design and apply FIFO topology

```bash
aws sns create-topic --name orders-events.fifo \
  --attributes FifoTopic=true,ContentBasedDeduplication=false

aws sqs create-queue --queue-name orders-worker.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false

# Subscribe SQS FIFO to SNS FIFO (queue policy must allow SNS)
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sqs --notification-endpoint "$QUEUE_ARN"
```

**Publish pattern:**

```bash
aws sns publish --topic-arn "$TOPIC_ARN" \
  --message '{"orderId":"o-1","state":"PAID"}' \
  --message-group-id "order-o-1" \
  --message-deduplication-id "o-1-PAID-v1"
```

1. Map one logical entity per `MessageGroupId` for strict order.
2. High cardinality groups increase parallelism; single group caps throughput.
3. Filter policies still apply but must respect FIFO subscription rules.
4. Encrypt with CMK when events contain PII; grant subscribers decrypt.

### 5. Verify with evidence

```bash
# Publish ordered sequence to one group, then receive from SQS
for state in CREATED PAID SHIPPED; do
  aws sns publish --topic-arn "$TOPIC_ARN" \
    --message "{\"orderId\":\"o-1\",\"state\":\"$state\"}" \
    --message-group-id "order-o-1" \
    --message-deduplication-id "o-1-$state"
done
aws sqs receive-message --queue-url "$QUEUE_URL" --max-number-of-messages 10 \
  --attribute-names All --message-attribute-names All
```

1. Confirm consumer processes CREATED → PAID → SHIPPED.
2. Republish same `MessageDeduplicationId` within 5 minutes — expect suppress.
3. Publish different groups concurrently — both make progress.

### 6. Observe and harden

1. Metrics: `NumberOfMessagesPublished`, SQS `ApproximateAgeOfOldestMessage`, DLQ depth.
2. Alarms when one hot group backs up (poison message blocking group).
3. DLQ + replay tooling that preserves group id.

### 7. Hand off

1. Document group-id and dedup-id conventions for all publishers.
2. IaC for topic, queues, subscriptions, IAM, KMS.
3. Runbook for stuck FIFO group (visibility timeout, poison message).

## Design Choices

| Choice | Prefer when | Avoid when |
| --- | --- | --- |
| Content-based dedup | Bodies are immutable natural keys | Bodies include timestamps/noise |
| Explicit dedup id | Event IDs from upstream | IDs collide across event types |
| Many groups | Horizontal scale | Need global total order (use single group knowingly) |
| SNS FIFO + SQS FIFO | Ordered fan-out to workers | Need Lambda/email/HTTP as primary FIFO sub without support |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Group ID | Per aggregate (`orderId`) | One group for entire platform |
| Dedup | Stable business event id | Random UUID every retry (duplicates) |
| Consumers | Controlled concurrency per queue | Competing consumers ignoring FIFO semantics |
| Schema | Versioned event envelopes | Breaking body changes without consumers ready |
| Errors | DLQ + group-aware replay | Infinite retry blocking the group |

## Output Checklist

- [ ] Ordering key and dedup strategy documented
- [ ] FIFO topic + FIFO SQS (or supported subs) configured
- [ ] IAM/KMS/policies validated
- [ ] Ordered publish/receive test passed
- [ ] Dedup behavior verified
- [ ] Throughput partitioning reviewed
- [ ] DLQ and poison-message runbook written
- [ ] Metrics/alarms in place
- [ ] `code-quality-standards` applied to publishers/consumers

## Rules

- Ordering is per `MessageGroupId` only — design keys deliberately.
- Do not mix standard SNS/SQS with FIFO expectations.
- Keep PII encrypted and redacted from logs.
- Authorized accounts only; load tests need approval.
- Prefer evidence from receive order over “should be ordered.”
