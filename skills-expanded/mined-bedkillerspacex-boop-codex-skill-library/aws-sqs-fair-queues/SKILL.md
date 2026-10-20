---
name: aws-sqs-fair-queues
description: >
  Amazon SQS fair queues for owned multi-tenant workloads: mitigating noisy-neighbor
  tenants, message group fairness when receiving, monitoring per-group backlog, and
  designing tenant keys. Use when high-volume tenants starve others on shared queues
  or when enabling fair queue behavior — not for basic unordered queue setup alone or
  unauthorized access to third-party accounts.
---

# AWS SQS Fair Queues

## Scope And Authorization

- **In scope:** SQS queues in AWS accounts you own where multi-tenant or multi-key fairness matters.
- **Out of scope:** Disrupting shared queues outside your authorization; extracting tenant data without need.
- Fair queues complement FIFO message groups and standard queue designs — confirm regional feature availability.
- Pair with `aws-sns-fifo-ordering` for ordered pub/sub and `backpressure-patterns` for consumer overload.
- Use `code-quality-standards` for worker code.

## When To Use

- Multi-tenant SaaS workers share one queue; large tenants create head-of-line blocking.
- FIFO queues where a hot `MessageGroupId` dominates receives.
- Need fairer polling so quiet tenants still get throughput.
- Designing tenant partition keys and DLQ strategies with fairness in mind.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SNS FIFO ordering / dedup | `aws-sns-fifo-ordering` |
| Express vs Standard Step Functions | `aws-step-functions-express` |
| General backpressure / load shedding | `backpressure-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Noisy neighbor | One tenant’s volume delays others on shared consumer fleet |
| Fairness | Receive attempts distribute more evenly across groups/tenants when fair queues enabled |
| Group key | Usually tenant id or `MessageGroupId` (FIFO) |
| Still needed | Per-tenant rate limits, quotas, DLQ, autoscaling — fairness is not a quota system |
| Tooling | SQS console/CLI attributes, CloudWatch queue metrics, worker instrumentation |

## Workflow

### 1. Confirm scope and success criteria

1. Tenancy model, queue type (standard/FIFO), consumer concurrency, SLA for small tenants.
2. Success: under synthetic hot-tenant load, cold tenants still process within SLO.
3. Measure baseline: p99 age for quiet vs hot tenant messages.

### 2. Inventory queues and consumer topology

```bash
aws sts get-caller-identity
aws sqs list-queues
aws sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-names All
aws sqs list-queue-tags --queue-url "$QUEUE_URL"
```

1. Identify whether producers set tenant id in group id / message attributes.
2. Map Lambda event source mapping vs ECS/K8s workers (concurrency, batch size).
3. Note DLQ redrive policy and max receive count.

### 3. Baseline noisy-neighbor evidence

1. Load test (authorized): publish 95% traffic as tenant A, 5% as B/C.
2. Record processing lag per tenant attribute.
3. Capture CloudWatch: `ApproximateAgeOfOldestMessage`, `NumberOfMessagesReceived`, worker CPU.

### 4. Enable fairness and design keys

```bash
# Enable fair queue behavior via queue attributes when supported in your account/region.
# Attribute names can evolve — verify with current AWS docs / Console before prod.
aws sqs set-queue-attributes --queue-url "$QUEUE_URL" --attributes file://fair-queue-attrs.json
aws sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-names All
```

**Producer conventions:**

1. FIFO: set `MessageGroupId` to tenant (or tenant+shard) — never one global group.
2. Standard: include `tenant_id` message attribute; consider separate queues for enterprise tiers if fairness insufficient.
3. Shard hot tenants: `tenantId#shardN` to increase parallelism without drowning others.

**Consumer conventions:**

1. Short visibility timeout relative to p99 processing; heartbeat extend for long jobs.
2. Idempotent handlers — fairness changes delivery interleaving.
3. Per-tenant concurrency caps in application when one tenant still dominates CPU after fair receive.

### 5. Verify with evidence

```bash
# Synthetic publish (illustrative loop — run only in lab/nonprod)
# Publish mixed tenants, then observe receive distribution and age metrics
aws cloudwatch get-metric-statistics --namespace AWS/SQS \
  --metric-name ApproximateAgeOfOldestMessage \
  --dimensions Name=QueueName,Value=my-workers.fifo \
  --start-time 2026-07-01T00:00:00Z --end-time 2026-07-01T01:00:00Z \
  --period 60 --statistics Maximum
```

1. Compare quiet-tenant latency before/after fair queue enablement.
2. Confirm poison messages still move to DLQ without permanent global stall (FIFO group awareness).
3. Validate IAM still least privilege (`sqs:ReceiveMessage` on intended queues only).

### 6. Observe and harden

1. Dashboards: queue age, DLQ depth, per-tenant processing counters (app metrics).
2. Alarms: age SLO breach; DLQ > 0; consumer error rate.
3. Review hot tenants for dedicated queues or throttled ingress API.

### 7. Hand off

1. Document tenant key + sharding policy for all producers.
2. Runbook: disable/adjust fairness only with capacity review.
3. Cost note: more even work may change autoscaling patterns.

## Fairness Design Matrix

| Pattern | When | Trade-off |
| --- | --- | --- |
| Shared queue + fair receive | Many small tenants | Hot tenants still share CPU after receive |
| Shard groups | Very hot tenants | More complexity in keys |
| Dedicated premium queues | Enterprise isolation | Ops overhead |
| API ingress quotas | Prevent queue flood | Needs gateway enforcement |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | Stable tenant/group ids | Random group per message (kills FIFO order) |
| Testing | Multi-tenant synthetic load | Only happy-path single tenant tests |
| Isolation | Fairness + app quotas | “Fair queue means no rate limits needed” |
| FIFO poison | Group-aware DLQ handling | One bad message blocks understanding of fairness |
| Metrics | Per-tenant latency | Only global TPS |

## Output Checklist

- [ ] Multi-tenant pain evidenced with metrics
- [ ] Queue type and group/tenant key design documented
- [ ] Fair queue settings applied (feature-verified for region)
- [ ] Before/after quiet-tenant latency compared
- [ ] Consumer idempotency and visibility timeout reviewed
- [ ] DLQ/redrive validated under mixed load
- [ ] Alarms and per-tenant metrics planned
- [ ] Producer conventions published
- [ ] `code-quality-standards` applied to workers

## Rules

- Authorized load testing only.
- Fairness does not replace authz, quotas, or encryption.
- Preserve FIFO ordering keys when sharding.
- Do not log full message bodies with PII.
- Prefer measured tenant SLOs over assumed fairness.
