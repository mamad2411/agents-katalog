---
name: resilience-flow-control
description: "Use when thinking through, reviewing, changing, or verifying resilience and flow controls: caches, invalidation, rate limits, quotas, external integrations, retries, timeouts, circuit breakers, bulkheads, degradation, backpressure, or admission control. For queue delivery use async-messaging; for transactional effects use transactions-consistency; for whole-system capacity use system-architecture-harness."
---

# Think Through Resilience & Flow Control

## Overview

Production guidance for surviving load and dependency failure. Each reference paper captures the mechanics that separate resilient systems from hopeful ones: retry storms, synchronized expiry, thundering herds, timeouts that compose incorrectly, circuit breakers without fallbacks, and rate limits that fail open exactly when they matter.

**Core principle:** Every dependency fails, every cache goes stale, and every retry amplifies load. Controls must have explicit semantics (window, scope, fail-open/closed) and the system must stay bounded while capacity is unavailable.

## Domain Law

```text
NO RESILIENCE OR FLOW-CONTROL CHANGE WITHOUT:
1. the minimum required primary paper(s) for the control selected from the context table;
2. the failure being defended against named (timeout, overload, staleness,
   provider outage) before choosing a mechanism;
3. "Existing-codebase checks" run when changing existing controls;
4. every applicable MUST mapped to a bounded decision, a test that
   injects the failure, or a documented exception.
```

## When to Use

Use this skill when thinking through, reviewing, changing, or verifying:

- caches: placement, TTL, eviction, invalidation, warming, negative caching, stampede protection;
- distributed cache coordination and hot-key handling;
- rate limiting by IP/user/tenant/endpoint, window algorithms, distributed limiting, fail-open/closed policy;
- quotas: soft/hard limits, reservation, reset windows, overage;
- external integrations: provider contracts, outages, degradation, replacement risk;
- retries: classification, caps, budgets, exponential backoff with jitter, honoring provider pushback;
- timeouts: per-hop and end-to-end deadlines, cancellation propagation;
- circuit breakers: trip thresholds, half-open probing, fallback behavior;
- bulkheads and concurrency limits;
- graceful degradation and load shedding;
- backpressure and admission control for queues and workers.

## When Not to Use

- Queue/job/event delivery semantics: use `async-messaging`.
- Transaction, lock, and consistency internals: use `transactions-consistency` (023, 103).
- Auth throttling policy ownership: `auth-access` (004) defines the goal; this skill supplies the mechanism.
- Whole-system overload and capacity architecture: use `system-architecture-harness`.

## Select the Operating Mode

| Mode | Use when | Required result |
|---|---|---|
| **Think** | The safe decision is not settled | requirements, constraints, invariants, risks, alternatives, decision, and validation path |
| **Review** | An artifact, repository, diff, or operating state already exists | evidence separated from assumptions, prioritized findings, and blockers |
| **Change** | Decisions are approved and repository changes are requested | the smallest safe change, compatibility notes, and verification still required |
| **Verify** | A claim needs proof | tests or measurements run, observed evidence, and residual risks |

If the user names a mode, use it. Otherwise infer the mode from intent and state the inference in one sentence. For a combined request, run **Think → Review → Change → Verify** and preserve the trace between phases. Think may stop with a decision; Review may stop with findings. Change must not claim completion before Verify. Verify must never turn a planned or unavailable check into evidence.

## Required Context Loading

| Situation | Papers |
|---|---|
| Cache-aside/read-through/write-through, TTL, stampede, hot keys | [037 Caching](references/papers/037-caching.md) |
| Cache coordination across instances | [131 Distributed Cache Coordination](references/papers/131-distributed-cache-coordination.md) |
| Limit algorithms, scopes, distributed state, fail policy | [038 Rate Limiting](references/papers/038-rate-limiting.md) |
| Quota reservation, soft/hard limits, reset | [039 Quotas](references/papers/039-quotas.md) |
| Provider contracts, outages, degraded modes, exit risk | [051 External Integrations](references/papers/051-external-integrations.md) |
| Retry classification, caps, budgets, jitter | [052 Retry Engineering](references/papers/052-retry-engineering.md) |
| Deadline budgeting, timeout composition, cancellation | [053 Timeout Engineering](references/papers/053-timeout-engineering.md) |
| Breaker states, thresholds, fallbacks | [054 Circuit Breakers](references/papers/054-circuit-breakers.md) |
| Degradation modes, bulkheads, containment | [055 Resilience](references/papers/055-resilience.md) |
| Queue/worker backpressure, shedding, admission control | [104 Backpressure](references/papers/104-backpressure.md) |

Load context in stages:

1. For the minimum required primary paper(s), read the executive engineering summary, pre-implementation questions, and the applicable normative requirements, failure modes, and verification checks needed to establish the obligations.
2. Then read only the named request-specific sections needed to decide or verify this control; record those section names in the output.
3. Treat every other owner paper or section as optional depth. Load it only when the request, a newly discovered dependency, risk, or unresolved evidence gap requires it; promote that depth to required when it becomes necessary.

Never load every paper in this skill by default.

## Workflow

Use the domain workflow as shared gates, then branch by the selected mode:

- **Think:** answer the questions and stop with a reasoned decision and validation path; do not edit by default.
- **Review:** inspect the available artifact or repository and stop with evidence-backed findings; do not claim changes.
- **Change:** apply only approved decisions, then continue to Verify before claiming completion.
- **Verify:** run the relevant checks, report observed results, and label every unavailable or unrun check.

1. Name the failure being defended against and the user journey it protects; select primary papers (a third-party checkout call touches 051 + 053 + 052 + 054).
2. Apply the staged loading contract above; do not turn a touched boundary into a full read of every owner paper.
3. Answer the paper's pre-implementation questions; label autonomous assumptions and their impact.
4. For existing controls, trace one logical operation across client, proxy, service, SDK, and worker layers; inventory every deadline, timeout, retry, queue, admission gate, and concurrency limit, and observe what happens when the dependency is down.
5. Define one end-to-end deadline and retry budget for the logical operation; allocate smaller per-hop/per-attempt budgets from remaining time, propagate cancellation, name the retry owner at each boundary, and calculate maximum call amplification across the full path.
6. Define bounded admission, queue, and concurrency per constrained resource; state what is rejected or shed when full, the explicit unavailable or degraded behavior, and its correctness, authorization, and recovery guarantees.
7. Convert each MUST/SHOULD/AVOID/NEVER into bounded decisions with explicit semantics (window, scope, thresholds, fail-open/closed) and failure-injection tests.
8. Apply the active mode: stop at a control decision in Think; stop at findings in Review; make the smallest approved safe change in Change; run outage, deadline-exhaustion, stacked-retry, saturation, shedding, and degradation checks in Verify.
9. Before completion, re-scan the normative lists and stop if any rule lacks a decision, test, or documented exception.

## Companion Skills and Standalone Safety

| Type | When | Companion | Missing companion behavior |
|---|---|---|---|
| **Required** | Retries can duplicate or ambiguously complete state changes | `transactions-consistency` | Require idempotent effects and status or reconciliation paths. |
| **Recommended** | Queue depth, worker concurrency, or backlog behavior is central | `async-messaging` | State required bounds and label delivery depth missing. |
| **Recommended** | Outage, overload, latency, or stampede claims need proof | `quality-release` | Define exact drills and label them unrun. |
| **Handoff** | Capacity or overload changes whole-system topology | `system-architecture-harness` | Limit the local control decision and identify architecture depth missing. |

If a companion is unavailable, complete only the safe local flow-control decision, name the missing depth, and recommend the exact technical ID or relevant installation group. Never claim unavailable material was read or weaken resource bounds, deadlines, retry budgets, or idempotency requirements.

## Output Contract

The selected mode is authoritative. Include only applicable fields below; a planned check is a validation path, not verification evidence.

Scale the output to the active mode: Think returns control semantics and bounds; Review returns findings; Change returns the repository-aware change plus pending proof; Verify returns observed failure and overload evidence with unrun checks labeled. A combined flow preserves all four phases.

1. **Papers consulted** — numbers and the sections relied on.
2. **Logical-operation budget** — each defended failure with one end-to-end deadline/retry budget, per-hop/per-attempt allocation from remaining time, cancellation propagation, retry owner, maximum call amplification, and ambiguous-outcome handling.
3. **Assumptions and unanswered questions** — labeled, with their design impact.
4. **Rule-to-decision map** — each applicable MUST/SHOULD → control parameters, enforcement point, and failure-injection test.
5. **Flow-control contract and failure modes** — admission, queue, and concurrency bounds; explicit reject, shed, unavailable, or degraded behavior; retry storms, stampedes, synchronized expiry, provider outage, and backlog saturation.
6. **Verification evidence** — outage, deadline-exhaustion, multi-layer retry amplification, saturation, shedding, and degradation-mode checks.

## Stop Conditions

Stop and revise when any of these appears:

- code is written before the defended failure is named;
- a logical operation lacks one end-to-end deadline/retry budget with per-hop/per-attempt allocations from remaining time and propagated cancellation;
- retries are independently stacked, or retry ownership and maximum call amplification are not explicit and bounded;
- a retry without a cap, deadline, backoff with jitter, and idempotent effects;
- a remote call without a timeout, or timeouts that do not compose into an end-to-end deadline;
- a circuit breaker with no fallback or degraded mode behind it;
- a cache with no named source of truth, TTL/invalidation policy, stampede protection, or loss behavior;
- cache treated as authoritative state with no rebuild path;
- a rate limiter with no stated fail-open/fail-closed decision or distributed-awareness analysis;
- quotas enforced only client-side or without reservation for concurrent use;
- synchronized expiry or lockstep refresh with no jitter;
- admission, concurrency, queue depth, or fan-out is unbounded or defended only by autoscaling;
- saturation has no explicit reject, shed, unavailable, or safe degraded behavior;
- degradation that silently changes correctness or authorization semantics;
- any resilience MUST downgraded to a TODO without a documented exception.

## References

Ten production papers under `references/papers/`: 037 Caching, 038 Rate Limiting, 039 Quotas, 051 External Integrations, 052 Retry Engineering, 053 Timeout Engineering, 054 Circuit Breakers, 055 Resilience, 104 Backpressure, 131 Distributed Cache Coordination. Cross-domain pointers inside the papers name the sibling skill to activate.

Worked example: [caching, stampede defense, and rate limiting for a hot endpoint](examples/worked-example-hot-endpoint-protection.md).
