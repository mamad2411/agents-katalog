---
name: design-aws-pattern
description: Pick the right AWS primitive for a workload — compute (Lambda/ECS/EKS/EC2), storage (S3/EFS/FSx), database (RDS/Aurora/DynamoDB) with cost + ops + scale tradeoffs.
---

# design-aws-pattern

> Given a workload sketch, produce a primitive choice with the *why*, not just the *what*. Output: chosen primitive, two runner-ups, and the conditions that would flip the choice.

## When to use

- A PRD says "deploy on AWS" without naming services.
- A workload is on the wrong primitive (Lambda timing out, ECS overprovisioned) and you want to know what to migrate to.
- A spike needs a "scratch this on AWS" plan.

## Procedure

1. **Characterize the workload.** Ask explicitly:
   - **Compute** — invocation pattern (request/sec, peak vs idle), max latency budget, longest task duration, stateful vs stateless.
   - **Storage** — data shape (objects vs filesystem vs block), access pattern (read-heavy / write-heavy / mixed), throughput, single-writer vs concurrent.
   - **Database** — query shape (point lookup vs aggregation), consistency, multi-region, transactional.
2. **Compute decision tree.**
   - `latency < 100ms` AND `idle most of the time` AND `stateless` AND `task < 15min` → **Lambda**.
   - Long tasks or steady RPS or websockets → **ECS Fargate** (serverless containers) for moderate scale; **EKS** when you need cluster-level controls (mesh, multi-tenancy, GPU).
   - Long-running stateful or licensed software → **EC2** with auto-scaling group.
3. **Storage decision tree.**
   - Object / blob (versioned, append-only-ish) → **S3** (with Intelligent-Tiering for unknown access patterns).
   - POSIX filesystem multi-attached → **EFS** (high latency, low throughput) or **FSx** (NetApp/Lustre/Windows; high throughput, paid).
   - Block storage single-attached → **EBS**.
4. **Database decision tree.**
   - Relational, < 64TB, predictable load → **RDS** (Postgres / MySQL).
   - Relational, very high throughput, serverless-ish → **Aurora** (Postgres-compatible).
   - KV / document, single-digit ms point lookup, scale-out → **DynamoDB**.
   - Wide-column / time-series → **Timestream** or **Keyspaces**.
5. **Networking.** Public-facing → ALB or API Gateway. Internal-only → PrivateLink + internal NLB. Cross-account → VPC Peering / Transit Gateway.
6. **Cost shape.** Per primitive, name the *cost driver*: Lambda = invocations + GB-s; ECS = vCPU-hour × always-on; RDS = instance + storage + IOPS; DynamoDB = on-demand vs provisioned.
7. **Ops shape.** Patch cadence, scaling levers, observability defaults (Lambda gets CloudWatch logs free; ECS needs explicit log driver; EKS adds CNI + cluster autoscaler complexity).
8. **Flip conditions.** State the metric thresholds where you'd revisit. "Lambda chosen because RPS < 200 and p99 < 100ms; revisit at 1k+ RPS or when cold starts exceed 200ms."

## Output

```text
design-aws-pattern: refund-async-writes

Workload: bursty, stateless, ~500ms task, JSON in/out via queue.

Compute:
  Chosen:    AWS Lambda (Python 3.12, 512MB).
  Why:       bursty + stateless + idle 70% of the day; sub-15-min tasks.
  Runner-up: ECS Fargate (if cold starts > 200ms become a problem).
  Flip when: sustained > 500 RPS for > 30 min (then ECS provisioned).

Queue:
  Chosen:    SQS standard with 14d retention + DLQ.
  Why:       Lambda native integration; backpressure for free.

Database:
  Chosen:    DynamoDB on-demand with single PK (refund_id) + GSI (status, created_at).
  Why:       point-lookup + recent-by-status queries; no relational joins required.
  Flip when: cross-entity transactions appear → RDS Postgres.

Networking:
  Lambda → VPC for DB access (NAT $$). If DB is DynamoDB, no VPC needed.

Cost driver: Lambda GB-s + DynamoDB on-demand read/write units. ~$300/mo at 500 RPS estimated.

Ops shape:
  Logs: CloudWatch out of the box.
  Tracing: X-Ray via SDK.
  Errors: DLQ + CloudWatch alarm on age-of-oldest-message.
```

## Quality bar

- Workload characterized in measurable terms (RPS, latency budget, task duration).
- Chosen primitive justified, not asserted.
- Runner-up named (the path back if assumptions break).
- Flip conditions are quantitative.

## Anti-patterns to avoid

- "Lambda for everything." Long tasks, websockets, or steady-state RPS cost more on Lambda than ECS.
- "EKS by default." Add the operational tax only when cluster-level controls are needed.
- DynamoDB without modeling access patterns first. Schema-less ≠ access-pattern-less.
- Picking based on "the team knows X". Tenancy is real; weight it, but don't ignore fit.
