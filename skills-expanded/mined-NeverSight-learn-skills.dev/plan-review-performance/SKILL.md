---
name: plan-review-performance
version: 1.0.0
description: Reviews performance, scaling, caching, database access, and resource usage risks in a plan.
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
  - Bash
---

# Plan Review Performance

Review whether the plan introduces avoidable performance or scaling risk.

## Guardrails

- Focus on performance risks introduced or exposed by the plan.
- Do not optimize without a plausible bottleneck, metric, or user impact.
- Prefer simple query, batching, caching, or pagination fixes over broad rewrites.
- Require a test, benchmark, trace, log, or metric for important claims.

## Evaluate

- N+1 queries and repeated remote calls.
- Missing indexes or inefficient filters.
- Memory growth, streaming, batching, and pagination.
- Cache correctness and invalidation.
- Latency-sensitive user paths.
- Background job retries, queue growth, and idempotency.
- Load spikes, rate limits, and external API quotas.

## Output

Return performance findings ordered by severity with:

- Risk
- Trigger
- User or system impact
- Recommendation
- Test or metric needed
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill plan-review-performance``
