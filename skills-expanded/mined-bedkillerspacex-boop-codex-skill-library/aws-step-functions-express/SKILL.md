---
name: aws-step-functions-express
description: >
  AWS Step Functions Express Workflows vs Standard for owned accounts: when to choose
  Express (high-volume, short-duration, at-least-once), execution logging, sync vs async
  start APIs, IAM, and cost/throughput trade-offs. Use when designing event pipelines,
  API backends, or migrating Standard state machines — not for long-running human
  approval workflows that need Standard features.
---

# AWS Step Functions Express Workflows

## Scope And Authorization

- **In scope:** State machines and integrations in AWS accounts you own or operate.
- **Out of scope:** Unauthorized invocation of third-party state machines; load tests without approval.
- Express semantics differ (history, duration, exactly-once) — do not assume Standard behavior.
- Pair application code with `code-quality-standards`; SNS/SQS ordering skills when events are ordered.

## When To Use

- High-throughput, short-lived orchestration (IoT, streaming enrich, API request workflows).
- Choosing Express vs Standard for a new state machine.
- Enabling CloudWatch Logs for Express (no durable execution history like Standard).
- Sync Express (`StartSyncExecution`) for low-latency request/response.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Long-running workflows, wait for callbacks, human approval | Standard Step Functions (same service; not Express) |
| SNS FIFO ordering | `aws-sns-fifo-ordering` |
| Queue fairness | `aws-sqs-fair-queues` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| | Express | Standard |
| --- | --- | --- |
| Duration | Short (minutes max class) | Up to 1 year |
| Rate | Higher event rates | Lower / durable |
| Execution history | Not durable like Standard; use logging | Full history in service |
| Exactly-once | At-least-once | Exactly-once start semantics (per design) |
| Integrations | Optimized for stream/API style | Broader long-running patterns (.wait, activities) |
| Pricing | Per transition / duration model differs | Per state transition |

## Workflow

### 1. Confirm scope and success criteria

1. Max execution time, TPS, need for `.wait`/callback/task tokens, audit history requirements.
2. Success: Express chosen only if constraints fit; logs show executions; idempotent tasks handle retries.
3. If human approval or multi-day saga → Standard.

### 2. Inventory state machines

```bash
aws sts get-caller-identity
aws stepfunctions list-state-machines
aws stepfunctions describe-state-machine --state-machine-arn "$SM_ARN"
# Type: STANDARD | EXPRESS
```

1. Note logging configuration, tracing, and IAM role.
2. List EventBridge/API Gateway/Lambda triggers.

### 3. Baseline requirements vs Express limits

1. Map each step’s max runtime and retry needs.
2. Confirm consumers are idempotent (at-least-once).
3. Decide sync (wait for result) vs async fire-and-forget.

### 4. Implement Express state machine

```bash
aws stepfunctions create-state-machine \
  --name enrich-events-express \
  --type EXPRESS \
  --role-arn "$SFN_ROLE" \
  --definition file://definition.json \
  --logging-configuration level=ALL,includeExecutionData=false,destinations=[{cloudWatchLogsLogGroup:{logGroupArn="$LOG_GROUP_ARN"}}]
```

**Definition tips:**

1. Keep branches tight; avoid patterns requiring long `Wait` for external humans.
2. Use `Retry`/`Catch` with idempotent Lambda/ECS tasks.
3. `includeExecutionData=false` if payloads have PII; log metadata only.
4. X-Ray tracing optional for latency debugging.

**Invoke:**

```bash
# Async
aws stepfunctions start-execution --state-machine-arn "$SM_ARN" --input file://input.json
# Sync Express
aws stepfunctions start-sync-execution --state-machine-arn "$SM_ARN" --input file://input.json
```

1. API Gateway HTTP API can integrate with sync Express for backend workflows.
2. IAM: `states:StartExecution` / `states:StartSyncExecution` scoped to ARN.
3. Payload size limits — offload large blobs to S3 and pass references.

### 5. Verify with evidence

```bash
aws stepfunctions start-sync-execution --state-machine-arn "$SM_ARN" --input '{"ok":true}'
aws logs tail "$LOG_GROUP" --since 30m
# Load nonprod: confirm concurrency and throttling behavior
```

1. Inject task failure → confirm Catch/Retry paths.
2. Duplicate start → confirm downstream idempotency keys.
3. Compare cost estimate vs Standard for expected TPS.

### 6. Observe and harden

1. Alarms: Express execution failures, throttles, log ingestion errors.
2. DLQ/EventBridge archive for failed async triggers.
3. Review IAM of state machine role: least privilege to Lambda/SQS/HTTP endpoints.

### 7. Hand off

1. Document type=EXPRESS decision in ADR (why not Standard).
2. Runbook: read logs (no Standard console history expectation).
3. Version definitions via CI; prevent silent type changes.

## Decision Guide

| Requirement | Choose |
| --- | --- |
| > ~5 minutes durable wait / human tasks | Standard |
| Very high event rate, short work | Express |
| Need full execution history in SFN console | Standard |
| Sync API orchestration | Express sync often fits |
| Callback task token long idle | Standard |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Type choice | Explicit ADR with limits | Express for week-long approvals |
| Idempotency | Business keys on every task | Assume exactly-once Express |
| Logging | Structured, redacted | Execution data with secrets |
| IAM | Resource-scoped invoke | `states:*` on `*` |
| Payloads | S3 pointers for large data | Multi-MB inline JSON |

## Output Checklist

- [ ] Express vs Standard decision documented
- [ ] State machine type EXPRESS verified
- [ ] Logging/tracing configured appropriately
- [ ] IAM roles least privilege
- [ ] Sync/async invoke path tested
- [ ] Idempotency and failure paths evidenced
- [ ] Alarms on failures/throttles
- [ ] PII/secrets excluded from logs/payloads
- [ ] `code-quality-standards` applied to task code/definitions

## Rules

- Do not use Express where Standard semantics are required.
- Design for at-least-once execution.
- Authorized accounts only; control load tests.
- Redact sensitive execution input/output.
- Keep definitions in version control.
