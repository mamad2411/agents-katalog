---
name: structural-operating
description: Use when shipping, releasing, ramping, operating, monitoring, rolling back, running migrations, handling on-call readiness, or designing production runbooks.
---

# Structural Operating

A release should make the safe move obvious and the irreversible move hard to take by accident.

Core rule:

> Ship so a mistake is cheap to undo, promote only on signals, and leave the 2am operator a runbook instead of an improvisation exercise.

## Default output

```md
## Rollout shape
- Flag/canary/ramp:
- Promotion signal:
- Rollback/backout:
- Irreversible approval:

## Runtime containment
- Degraded tiers:
- Retry/deadline/breaker:
- Load shedding / quotas:
- Shutdown/drain:

## Ownership
- Owner:
- Runbook:
- Artefacts with expiry:
```

## Operating checks

- Ship reversibly when blast radius justifies it: flags, canaries, cohorts, expand/contract, shadow traffic.
- Promote on evidence from canary/control metrics, not calendar time or hunch.
- Separate the decision to release from the act; dry-run plans and require four-eyes for irreversible/wide steps.
- Degrade in tiers and rehearse the path before relying on it.
- Bound load you create: deadlines, capped retries, exponential backoff, jitter, breakers, explicit 503/backpressure.
- Finish in-flight work before exit: stop accepting, drain within a deadline, flush, ack only durable work.
- Give every flag, cache, quota, migration, dashboard, and runbook one owner and expiry/review date.
- Ensure known failures have runbook actions; novel failures have named owners.

## Red flags

- Rollback requires a new build while the release is burning.
- Ramp advances because “it has been an hour”.
- Retry policy has no cap, jitter, deadline, or breaker.
- Graceful shutdown waits forever or drops accepted work.
- Alert, flag, or migration has no owner or sunset.
