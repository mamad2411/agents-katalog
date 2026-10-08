---
name: ecs-runtime-debug-playbook
description: Debug AWS ECS or Fargate deployments where CI or workflow status does not match live behavior, especially when an old task definition keeps serving traffic, a new task exits during startup, health checks are false-green, Alembic or schema state may be inconsistent with physical tables, or AWS profile or region confusion blocks diagnosis. Use when tracing deploy failures across workflows, ECS services, one-off tasks, CloudWatch logs, database state, and public smoke checks.
---

# ECS Runtime Debug Playbook

Use this skill to debug deploy incidents by proving each layer in order instead of trusting workflow output.

Read [references/playbook.md](references/playbook.md) when you need the full checklist, failure-pattern inventory, example commands, or validation expectations.

## Workflow

### 1. Pin the investigation scope

- Record the expected release SHA, task definition revision, cluster, service, AWS profile, and region before inspecting anything.
- Export `AWS_DEFAULT_PROFILE`, `AWS_REGION`, and `AWS_DEFAULT_REGION` explicitly for every command path that touches live infrastructure.
- Treat relative labels like "latest deploy" or "the new backend" as unsafe until they are tied to exact ARNs, workflow run IDs, or commit SHAs.

### 2. Compare the workflow claim to live ECS state

- Inspect the ECS service first. Do not assume a green workflow means the intended revision is actually serving traffic.
- Check service `taskDefinition`, service `desiredCount` and `runningCount`, the PRIMARY deployment revision, and whether any older deployments still have running or pending tasks.
- If the intended task definition is not the only active deployment serving the full desired count, treat rollout as incomplete even if CI reported success.

### 3. Collect crash evidence before changing anything

- Inspect the stopped task for the intended revision.
- Read the CloudWatch log stream for the startup failure.
- Identify the first concrete runtime fault, not just the top-level deploy symptom.

### 4. Verify runtime invariants inside the real runtime

- Prefer one-off inspection tasks that run inside the same image and task definition as the failing service.
- For database-backed services, compare revision metadata to physical schema state. Do not trust Alembic head alone.
- If a health endpoint says healthy but the runtime crashes on startup, assume the readiness contract is incomplete until proven otherwise.

### 5. Repair the smallest trustworthy layer

- If live data may be mutated, create a snapshot first.
- If revision metadata is ahead of the physical schema, rewind or restamp only to the last revision you can prove is real, then replay migrations forward.
- If the failure is a false-green deploy gate, fix the rollout waiter or readiness logic in code so the same incident cannot pass again.
- Prefer repairing the contract and the live state together: one without the other leaves recurrence risk.

### 6. Prove recovery with live checks

- Re-run the migration or repair path and confirm the expected revision and required runtime objects now exist.
- Wait until the exact expected task definition is the sole active serving deployment.
- Run public or load-balancer-level smoke checks against the live system, not only internal health checks.

### 7. Write the incident record

- Record the root cause, contradictory signals, live repair sequence, guardrails added, and validation performed.
- Make the record specific enough that another agent can repeat the investigation without rediscovering the path.

## Guardrails

- Prefer exact resource identifiers over inferred names.
- Prefer one-off runtime inspection over local speculation.
- Prefer physical schema checks over metadata-only checks.
- Prefer explicit rollout success criteria over provider waiters whose semantics you have not verified.
- Stop before risky live mutation if you do not have a snapshot or rollback path.
