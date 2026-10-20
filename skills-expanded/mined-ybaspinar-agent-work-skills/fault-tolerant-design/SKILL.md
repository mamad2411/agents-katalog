---
name: fault-tolerant-design
description: Use when designing or reviewing reliability-sensitive software, critical paths, background jobs, queues, database changes, rollout plans, dependency failures, resilience, fault tolerance, failover, or failure modes.
---

# Fault Tolerant Design

Review software so important paths keep working when dependencies, processes, deploys, or infrastructure fail.

Core rule:

> Keep the critical path isolated, redundant where justified, stable under dependency failure, and changed progressively.

Use this for architecture reviews, reliability reviews, background jobs, queues, data pipelines, database changes, rollout plans, external API dependencies, and incident-prone feature paths. Do not use it to add distributed-systems ceremony to low-risk code.

## Principles

| Principle | Review question |
|---|---|
| Isolation | Can this part fail without breaking the critical path? |
| Redundancy | Are important copies isolated, or do they share the same failure domain? |
| Static stability | What last known good state is safe to keep using during dependency failure? |
| Recovery practice | Is the recovery path exercised, idempotent, and boring? |
| Progressive delivery | How is blast radius limited when this change is wrong? |

## Default output

```md
## Critical path
- What must keep working:
- What can degrade or pause:

## Isolation
- Dependencies in the critical path:
- Failure boundaries:
- Cascade risks:
- Shared-fate risks:

## Redundancy
- Copies / retries / alternate paths:
- Isolation between copies:
- Capacity headroom:

## Static stability
- Last known good state:
- Behavior during dependency failure:
- Backpressure / buffering limit:

## Recovery practice
- Failover or recovery path:
- How it is exercised regularly:
- Idempotency / replay safety:

## Progressive delivery
- Rollout order:
- Feature flags / release channels:
- Blast-radius controls:
- Rollback constraints:

## Failure modes
- Non-critical dependency failure:
- Instance/process failure:
- Zone/region/provider-style failure:
- Self-induced deploy/config bug:

## Recommendation
- Required change:
- Optional improvement:
- Risk accepted:
```

Compress the structure for short answers, but keep the critical-path, isolation, static-stability, and rollout decisions explicit.

## Review heuristics

### Isolation

- Remove non-essential dependencies from the request, write, or job critical path.
- Control, admin, analytics, billing, deploy, registry, and config-publishing failures should not break already-running user-facing work.
- Name shared-fate risks: same database, queue, config source, credentials, region, deploy step, or operator.

### Redundancy

- Add copies, retries, or alternate paths only when failure impact justifies complexity.
- Copies are not redundant if they depend on the same bottleneck.
- Retries need limits, backoff, idempotency, and a terminal state such as dead-lettering.

### Static stability

- Prefer last known good config/cache/state over live dependency reads in critical paths.
- State freshness, correctness limits, and safety windows explicitly.
- Use backpressure instead of unbounded queues or memory growth.

### Recovery practice

- Treat untested failover, restore, replay, and rollback as imaginary.
- Design idempotency and replay safety before relying on queues or retries.
- Exercise recovery paths regularly enough that they are routine.

### Progressive delivery

- Ship risky changes from least-critical to most-critical environments.
- Use flags, canaries, release channels, tenant cohorts, queue partitions, or database-by-database rollout when appropriate.
- Rollback must be fast, observable, and state-compatible before a feature flag counts as safety.

## Guardrails

- Do not cargo-cult cloud architecture into small apps.
- Do not add redundancy when removing a dependency is simpler.
- Do not call a system fault tolerant because it retries.
- Do not recommend retry forever, unbounded queues, or silent data loss.
- Do not call copies redundant when they share the same failure domain.
- Do not rely on feature flags if rollback cannot safely handle changed state.
- Do not hide degraded behavior; make stale, paused, or buffered states visible.

## Examples

### External API in a worker

If a worker enriches records through an external API, ingestion should not depend on enrichment when enrichment is optional. Keep the API outside the ingestion critical path. Preserve the last known good enrichment with a freshness timestamp. Use bounded retries, dead-lettering, and idempotent writes so replay is safe.

### Config service in the request path

If every request fetches feature config from a control service, serving traffic depends on the control plane. Move config refresh out of the request path. Serve from a last known good config snapshot with version, age, and safety limits. A control-service outage should block config changes, not existing traffic.

### Global migration rollout

If a database migration and app change are planned for all customers at once, the rollout has excessive shared fate. Require mixed-version compatibility, progressive delivery through dev/canary/low-risk cohorts, blast-radius controls, and a rehearsed rollback or forward-fix path.
