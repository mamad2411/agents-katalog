---
name: gcp-pubsub-exactly-once
description: >
  Google Cloud Pub/Sub exactly-once delivery for pull subscriptions: enablement,
  ack deadlines, idempotent handlers, ordering keys interaction, dead-letter topics,
  and verification of duplicate suppression. Use for owned GCP messaging workloads —
  not a guarantee of end-to-end exactly-once without idempotent consumers.
---

# GCP Pub/Sub Exactly-Once Delivery

## Scope And Authorization

- **In scope:** Owned projects; authorized messaging architecture changes.
- **Out of scope:** Flooding third-party topics/subscriptions; unauthorized publish.
- Exactly-once delivery is a **subscription feature** with API and regional constraints;
  application-level idempotency is still required for true end-to-end once processing.
- Validate in non-prod with load that includes retries and restarts.
- Redact message payloads that contain PII or secrets from logs and tickets.
- Pair consumer code with `code-quality-standards`.

## When To Use

- Designing or migrating pull subscribers that cannot tolerate duplicate side effects
  (charges, inventory decrements) without heavy dedupe stores.
- Enabling `enableExactlyOnceDelivery` on new or existing subscriptions.
- Debugging “duplicate messages” vs “at-least-once redelivery after ack timeout”.
- Setting ack deadlines, flow control, and dead-letter policies correctly with EOD.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Baseline GCP IAM for Pub/Sub | `gcp-iam-basics` |
| Retry/backoff in clients | `retry-backoff-patterns` |
| General observability | `observability-metrics-tracing` |
| Kafka / other brokers | broker-specific skills |
| Push subscription OIDC auth | API/auth skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| At-least-once | Default Pub/Sub delivery; duplicates possible |
| Exactly-once delivery (EOD) | Pub/Sub ensures a message is not redelivered to a subscriber after successful ack, within product guarantees for **pull** (and documented surfaces) |
| Ack | Subscriber confirms processing; with EOD, ack is strongly consistent for that subscription |
| Ack deadline | Time to ack before redelivery consideration |
| Ordering key | Ordered delivery per key; interacts with concurrency |
| Dead-letter topic (DLT) | After max delivery attempts, forward poison messages |
| Idempotency key | Application dedupe (message_id, business id) still best practice |

### What EOD does not mean

- Does **not** mean only one publisher attempt ever existed.
- Does **not** automatically make multi-step DB + external API side effects atomic —
  use transactions / outbox / idempotent writes.
- Does **not** remove need to handle failed processing before ack (nack / deadline).
- Feature availability and guarantees depend on subscription type, region, and client
  library support — confirm current Google docs for your runtime.

## Workflow

### 1. Confirm requirements

1. Record topic, subscription, region, consumer runtime, peak backlog, authorization.
2. Decide: side effects must be single-apply → EOD + idempotent handler.
3. Confirm **pull** (or supported) path; redesign if you only have unsupported push patterns.
4. Success metrics: duplicate side-effect rate → 0 under restarts; ack latency SLOs held.

### 2. Inventory current subscriptions

```bash
gcloud pubsub topics list --project=PROJECT_ID
gcloud pubsub subscriptions list --project=PROJECT_ID

gcloud pubsub subscriptions describe SUBSCRIPTION_ID --project=PROJECT_ID
# Look for: enableExactlyOnceDelivery, ackDeadlineSeconds, deadLetterPolicy,
# messageRetentionDuration, enableMessageOrdering, filter, retryPolicy
```

Capture baseline: duplicate processing incidents, redelivery rate, nack patterns.

### 3. Design consumer contract

1. **Ack only after** durable commit of side effects (or transactional outbox).
2. Store processed `message_id` (and business key) for defense in depth.
3. On failure: nack or let deadline expire; do not ack.
4. Bound concurrency; with ordering keys, respect per-key ordering constraints.
5. Configure DLT for poison messages after N attempts.

### 4. Enable exactly-once delivery

```bash
# New subscription with EOD
gcloud pubsub subscriptions create SUBSCRIPTION_ID \
  --topic=TOPIC_ID \
  --project=PROJECT_ID \
  --enable-exactly-once-delivery \
  --ack-deadline=60 \
  --message-retention-duration=7d

# Update existing (expect reconfiguration constraints / recreated sub if required)
gcloud pubsub subscriptions update SUBSCRIPTION_ID \
  --project=PROJECT_ID \
  --enable-exactly-once-delivery
```

Dead-letter example:

```bash
gcloud pubsub subscriptions update SUBSCRIPTION_ID \
  --project=PROJECT_ID \
  --dead-letter-topic=DLT_TOPIC \
  --max-delivery-attempts=10
```

IAM: subscriber SA needs `roles/pubsub.subscriber`; publisher to DLT needs publish on DLT.

### 5. Client library usage notes

```text
# Pseudocode — use current google-cloud-pubsub client for your language
# 1) Receive with flow control max_messages / max_bytes
# 2) Process (DB upsert by message_id)
# 3) Ack only on success; with EOD, use ack APIs that surface ack response errors
# 4) On ack failure, treat as uncertain — rely on idempotent process on redelivery
```

1. Upgrade client libraries to versions that support EOD ack semantics.
2. Handle ack response errors explicitly (retry ack; do not assume silence = success).
3. Align ack deadline with p99 processing time + safety margin; extend deadline if supported.

### 6. Verify with evidence

| Test | Method | Expect |
| --- | --- | --- |
| Happy path | Publish N unique msgs | N side effects |
| Restart mid-process | Kill worker after process before ack | ≤1 side effect with EOD+idempotency |
| Slow handler | Processing > deadline without extend | Controlled redelivery; idempotent |
| Poison message | Always fail | Lands in DLT after max attempts |
| Duplicate publish | Same business payload twice | Two message_ids → app policy decides |

```bash
# Publish test messages
gcloud pubsub topics publish TOPIC_ID --message='{"order_id":"o-1"}' --project=PROJECT_ID

# Inspect subscription metrics in Cloud Monitoring:
# ack_message_count, nack_message_count, oldest_unacked_message_age, dead_letter_message_count
```

### 7. Operate and harden

- Alert on: oldest unacked age, DLT rate, ack failure rate, subscriber lag.
- Capacity: EOD may change throughput characteristics; load-test before prod cutover.
- Document that **exactly-once delivery ≠ exactly-once business transaction** without
  careful handler design.
- Review IAM on topic, subscription, and DLT annually.

## Configuration table

| Setting | Guidance |
| --- | --- |
| `enableExactlyOnceDelivery` | true for pull subscribers that need strong ack |
| `ackDeadlineSeconds` | ≥ p99 process time; avoid huge values that delay redelivery |
| Ordering | Enable only if required; lowers parallelism |
| Retention | Long enough for debugging; cost vs recoverability |
| Filter | Server-side filter reduces noise; test filter changes |
| Retry policy | Minimum backoff for transient errors |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Ack timing | After durable commit | Ack then process |
| Duplicates | EOD + idempotent upsert | EOD alone, non-idempotent charge API |
| Dead letter | Monitored DLT + replay runbook | Infinite redelivery storm |
| Libraries | Current client + ack error handling | Ancient library ignoring EOD |
| IAM | Least-privilege subscriber SA | Editor on project for “simplicity” |

## Output Checklist

- [ ] Topic/subscription/region/authorization recorded
- [ ] Requirement for EOD vs at-least-once documented
- [ ] Subscription settings exported before change
- [ ] EOD enabled with compatible client version
- [ ] Ack deadline and flow control sized
- [ ] DLT configured and monitored
- [ ] Idempotent handler implemented and tested
- [ ] Restart and deadline tests show no double side effects
- [ ] Metrics/alerts for lag, nack, DLT
- [ ] `code-quality-standards` applied to consumer code

## Rules

- Owned projects only; do not load-test shared third-party topics.
- Never log full payloads with secrets; redact.
- Prefer idempotent consumers even when EOD is on.
- Do not claim “exactly-once system” without end-to-end design review.
- Keep focus on Pub/Sub EOD; route IAM and generic retry patterns to sibling skills.
