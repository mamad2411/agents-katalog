---
name: serverless-patterns
version: 1.0.0
min_mindforge_version: 10.1.1
status: stable
triggers: serverless pattern, cold start mitigation, function composition, event trigger lambda, stateless function, serverless state management, lambda architecture, function timeout, serverless cost model, ephemeral compute, serverless scaling, function orchestration
compose: cost-estimation
---

# Skill — Serverless Patterns

## When this skill activates
Any task involving serverless function design, cold start optimization,
function composition, event-driven architectures using FaaS platforms,
or cost modeling for serverless workloads.

## Mandatory actions when this skill is active

### Before writing any code
1. Identify the trigger type (HTTP, queue, schedule, storage event, stream).
2. Determine state requirements and where state will live (DynamoDB, Redis, S3).
3. Estimate invocation volume and duration for cost projection.
4. Decide composition pattern (Step Functions vs choreography vs direct invoke).

### During implementation
- Keep functions focused (single responsibility).
- Externalize all state (no reliance on local filesystem or memory between invocations).
- Implement idempotency keys for retry-safe operations.
- Set appropriate timeout values (not max — just enough + buffer).
- Use structured logging with correlation IDs for distributed tracing.
- Checkpoint long-running work before timeout boundary.

### After implementation
- Verify cold start latency meets SLA requirements.
- Confirm cost model aligns with budget (invocations × duration × memory).
- Test retry and failure scenarios end-to-end.
- Monitor concurrency limits and throttling metrics.

## Cold Start Mitigation

### Techniques
1. **Provisioned concurrency** — Pre-warm N instances (cost trade-off).
2. **Bundle optimization** — Smaller deployment = faster init.
3. **Avoid VPC** — VPC attachment adds 5-10s cold start (only if DB needed).
4. **Lazy initialization** — Defer heavy setup until first request needs it.
5. **Connection pooling** — Use RDS Proxy or connection pool service.
6. **Language choice** — Go/Rust cold start < Python < Java/Node.

### When cold start matters
- Synchronous user-facing APIs (matters a lot).
- Async queue processors (usually doesn't matter).
- Scheduled jobs (doesn't matter at all).

## Composition Patterns

### Step Functions (Orchestration)
- Central coordinator manages workflow state.
- Built-in retry, catch, timeout per step.
- Visual debugging of execution history.
- Best for: complex workflows, human approval steps, long-running processes.

### Choreography (Event-Driven)
- Each function emits events, others react.
- No single point of failure.
- Harder to debug end-to-end.
- Best for: loosely coupled, independent scaling per step.

### Fan-Out / Fan-In
- Dispatch N parallel tasks → aggregate results.
- Use SQS/SNS for fan-out, DynamoDB for aggregation.
- Handle partial failures gracefully.

## State Management

| State Type | Solution | Use When |
|-----------|----------|----------|
| Session state | DynamoDB / Redis | Auth tokens, cart |
| Workflow state | Step Functions | Multi-step processes |
| Cache | ElastiCache / DAX | Repeated reads |
| File state | S3 | Large objects |
| Event state | Event carried | Pass between functions |

## Cost Model

```
Monthly cost = (invocations × $0.20/1M) + (GB-seconds × $0.0000166667)
```

### Cost comparison triggers
- If >1M invocations/hour sustained → consider containers.
- If function runs >15min → containers or batch.
- If always-on with predictable load → containers cheaper.
- If spiky/unpredictable → serverless wins on cost.

## Trigger Patterns

| Trigger | Pattern | Key Concern |
|---------|---------|-------------|
| HTTP (API Gateway) | Request/response | Cold start latency |
| SQS | Queue consumer | Batch size, visibility timeout |
| Schedule (cron) | Periodic job | Idempotency on overlap |
| S3 event | File processor | Duplicate events possible |
| DynamoDB stream | Change capture | Ordering guarantees |
| Kinesis | Stream processor | Shard iterator, checkpointing |

## Timeout Strategy
- Set timeout = expected p99 duration + 20% buffer.
- Checkpoint work before 80% of timeout.
- Implement dead-letter queues for timed-out invocations.
- Never set timeout to maximum "just in case."

## Self-check
- [ ] Function is idempotent (safe to retry).
- [ ] State externalized (no local filesystem reliance).
- [ ] Timeout set appropriately (not max).
- [ ] Cold start measured and within SLA.
- [ ] Cost model validated against expected traffic.
- [ ] Dead-letter queue configured for failures.
- [ ] Correlation IDs propagated for tracing.
