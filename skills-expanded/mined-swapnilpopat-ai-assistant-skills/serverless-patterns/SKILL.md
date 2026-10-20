---
name: serverless-patterns
description: Apply event-driven, function-based, and managed-runtime patterns (Lambda, Azure Functions, Cloud Run/Functions, Cloudflare Workers) — including idempotency, fan-out, orchestration, cold-start, and cost control. Use when designing event-driven systems or replacing always-on compute with managed runtimes.
---

# Serverless Patterns

Serverless wins when the workload is spiky, event-driven, or stateless — and loses when you fight the platform. Pick the runtime per concern (function vs container vs edge), make every handler idempotent, and own the cost curve before traffic does.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Functions | AWS Lambda (SnapStart, ARM64), Azure Functions Flex, Google Cloud Functions Gen 2 |
| Container-on-demand | AWS Lambda container images, Cloud Run, Azure Container Apps, Cloudflare Containers |
| Edge runtimes | Cloudflare Workers, Vercel Edge, Deno Deploy |
| Orchestration | AWS Step Functions, Azure Durable Functions, GCP Workflows, Temporal Cloud |
| Event bus | EventBridge, Azure Event Grid, GCP Eventarc, Cloudflare Queues |
| Streaming | Kinesis / MSK, Event Hubs, Pub/Sub, Confluent Cloud |
| API front | API Gateway HTTP / Function URLs, APIM, API Gateway, Cloudflare |
| IaC | SST v3, Serverless Framework v4, AWS SAM, Terraform, Pulumi |
| Observability | OpenTelemetry Lambda layer, ADOT collector, native APM |
| Spec | CloudEvents 1.0, AsyncAPI 3.0 |

## When to Use
- Spiky or unpredictable traffic (idle cost matters).
- Event-driven processing (S3/Blob/GCS uploads, queue messages, webhooks).
- Glue between SaaS systems.
- Per-tenant isolation cheaply.
- Background workflows with branching/retries.

## Don't Use When
- Sustained high RPS with stable load — containers are cheaper.
- Long-running (> 15 min) synchronous work — use orchestration or containers.
- Latency budget < 50 ms with cold starts on the hot path.
- Heavy local state, large in-memory caches, or GPU workloads.

## Prerequisites
- Event sources / queues already provisioned or planned.
- Idempotency strategy chosen (request-id store, conditional writes).
- Tracing wired so async hops aren't black boxes.

## Inputs the Agent Should Gather
- Trigger types (HTTP, queue, event, schedule, stream).
- p99 latency budget and cold-start tolerance.
- Peak RPS, sustained RPS, and burst factor.
- Payload size distribution.
- Downstream limits (DB connections, third-party rate limits).

## Instructions

### 1. Pick the runtime per workload

| Pattern | Best fit | Why |
| --- | --- | --- |
| Sync API < 30s, spiky | Lambda + API GW HTTP, or Cloud Run | Scale-to-zero, per-request billing |
| Sync API, sustained, large image | Cloud Run / Container Apps | Cheaper than Lambda at high RPS |
| Global low-latency read | Cloudflare Workers + KV/D1 | Sub-50ms cold start near user |
| Background per-event | Lambda + SQS/EventBridge / Functions + Service Bus | Built-in retry, DLQ |
| Long workflow (> 15 min) | Step Functions / Durable / Temporal | Stateful, retries, replay |
| Stream processing | Lambda + Kinesis (parallelization factor) / Functions + Event Hubs | Managed scaling per shard |
| Scheduled batch | EventBridge Scheduler / Functions Timer / Cloud Scheduler | No cron host to maintain |

### 2. Design every handler idempotent
```python
# AWS Lambda + DynamoDB conditional write idempotency
import boto3, json, os, hashlib
from botocore.exceptions import ClientError

ddb = boto3.client("dynamodb")
TABLE = os.environ["IDEMPOTENCY_TABLE"]

def handler(event, _ctx):
    key = event["headers"].get("Idempotency-Key") or hashlib.sha256(
        json.dumps(event["body"], sort_keys=True).encode()
    ).hexdigest()
    try:
        ddb.put_item(
            TableName=TABLE,
            Item={"pk": {"S": key}, "ttl": {"N": str(int(_ctx.get_remaining_time_in_millis()/1000) + 86400)}},
            ConditionExpression="attribute_not_exists(pk)",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"statusCode": 200, "body": '{"status":"duplicate"}'}
        raise
    # … perform side effect exactly once …
    return {"statusCode": 200, "body": '{"status":"ok"}'}
```
Or use AWS Powertools / Azure Durable entity / Temporal — don't roll your own twice.

### 3. Cold-start mitigation, in order of cost-efficiency
1. Choose ARM64 / smaller deps / lighter language (Go, Rust, Node).
2. Strip the deployment artifact; lazy-load heavy SDKs.
3. Move init outside the handler; reuse SDK clients.
4. Lambda SnapStart (Java/.NET/Python), Functions premium plan only when justified.
5. Provisioned concurrency / Min instances *only* on the hot path with measured impact.

### 4. Fan-out and back-pressure
```
HTTP ─> API GW ─> Lambda (validate) ─> SNS / EventBridge ─> [SQS-A → Lambda-A]
                                                            [SQS-B → Lambda-B]
                                                            [SQS-C → Lambda-C]
```
- Each consumer has its own queue + DLQ.
- Set per-consumer concurrency so one slow downstream can't starve others.
- Reserved/maximum concurrency on producers prevents downstream meltdown.

### 5. Orchestrate, don't chain
For multi-step workflows use Step Functions / Durable Functions / Temporal — not function-calls-function.
- Visible state machine.
- Built-in retry with backoff per step.
- Replay/inspect failed runs.
- Sagas via compensation steps.

```json
// Step Functions Standard: order saga
{
  "StartAt": "ReserveInventory",
  "States": {
    "ReserveInventory": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "reserveInventory", "Payload.$": "$" },
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "Fail" }],
      "Next": "ChargeCard" },
    "ChargeCard": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "chargeCard", "Payload.$": "$" },
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "ReleaseInventory" }],
      "Next": "Done" },
    "ReleaseInventory": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "releaseInventory", "Payload.$": "$" },
      "Next": "Fail" },
    "Done": { "Type": "Succeed" },
    "Fail": { "Type": "Fail" }
  }
}
```

### 6. Cost guardrails
- Set per-function concurrency cap (prevent runaway loops billing six figures).
- Alarm on invocations + duration anomaly.
- Use ARM64 (~20% cheaper on Lambda).
- Tier storage on event payloads; pass S3 references not blobs (Claim Check).
- Compare break-even monthly vs Cloud Run / Container Apps at sustained load.

### 7. Observability
- Enable OpenTelemetry tracing on every function; propagate W3C `traceparent` through async hops via message attributes.
- Structured JSON logs with request id, idempotency key, tenant id.
- Single dashboard per workflow, not per function.

## Common Pitfalls

| Pitfall | Why it bites | Fix |
| --- | --- | --- |
| Non-idempotent handlers + at-least-once delivery | Double-charges, duplicate emails | Idempotency key + conditional write |
| Synchronous fan-out via SDK calls | Cascading timeouts, cold-start chains | Async via queue/event bus |
| Provisioned concurrency everywhere | Pays for idle, defeats serverless | Apply only on measured hot paths |
| DB connection storms | Each cold function opens a new conn | RDS Proxy / Hyperdrive / connection pool service |
| 15-minute Lambda workflows | Hits hard limit mid-run | Step Functions / Durable / Temporal |
| Logs only, no traces | Async failures are invisible | OTel + traceparent propagation |
| No DLQ | Lost events on persistent failure | DLQ + alert + replay tool |
| One mega-function | Slow cold start, unclear ownership | One function per responsibility |

## Output Format
1. Per-trigger runtime decision with rationale.
2. Idempotency mechanism (storage + key strategy).
3. Concurrency and DLQ configuration.
4. Workflow diagram if multi-step (Step Functions / Durable / Temporal definition).
5. Observability wiring (trace exporter, log schema, dashboard).
6. Cost estimate at p50 / peak load + break-even vs container alternative.

## Abort Criteria
- Sustained load makes container PaaS materially cheaper — switch.
- Sync latency budget can't absorb cold start and warm-pool cost is unaffordable.
- No idempotency strategy possible (e.g., side effect to non-idempotent legacy) — wrap with orchestrator + manual review.

## Related Skills
- `../cloud-solution-architect/SKILL.md` — pattern catalog
- `../../architect/architecture-patterns/` — event-driven, CQRS, saga
- `../../architect/quality-attributes/slo-error-budgets/SKILL.md`
- `../../engineer/api-development/` — API design

## Authoritative References
- AWS Lambda Operator Guide; AWS Powertools (Python/TypeScript/Java/.NET)
- AWS Serverless Lens (Well-Architected)
- Azure Functions best practices; Durable Functions docs
- Google Cloud Run + Cloud Functions Gen 2 docs
- Cloudflare Workers + Queues + Durable Objects docs
- CloudEvents 1.0, AsyncAPI 3.0
- Temporal documentation
