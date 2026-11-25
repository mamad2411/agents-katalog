---
name: backend-cache
description: "Design cache keys, invalidation, expiration, and fallback. Use for cache correctness and measured caching changes; db-query fixes the underlying query semantics."
---

# backend-cache

Design cache keys, invalidation, expiration, and fallback.

## Choose this workflow

Use for cache correctness and measured caching changes; db-query fixes the underlying query semantics.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan caching behavior when requested; apply for requested implementation using resolved freshness, identity and failure semantics.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Key design, invalidation, expiry, stampedes, and fallback; implementation on request.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Map the source of truth, consumers, authorization scope and every invalidation path. Define the key as an unambiguous identity tuple including relevant tenant, user, filters and representation version; distinguish a cached empty/falsey value from a miss.
2. Specify separate absent, in-flight, successful and failed states. Define whether concurrent callers share work, when the freshness clock starts, the exact expiry boundary and zero-TTL behavior. Choose these from product requirements, not a convenient implementation default.
3. If asynchronous work is shared, assign cancellation ownership: a caller may stop waiting without cancelling shared work needed by other callers. Handle already-aborted callers, synchronous fetch errors, asynchronous rejection and listener cleanup on every terminal path.
4. If invalidation can race with an asynchronous fill, associate each fill with its current entry or generation. Invalidation must detach obsolete work so its late success or failure cannot overwrite or remove a newer entry. Decide explicitly whether existing waiters still receive the detached result.
5. Verify identity isolation, falsey hits, coalescing, expiry, failure/retry, per-caller cancellation and reversed completion after invalidation using a controlled clock and deferred work. Measure hit rate or latency only with an actual representative workload.

## Technical method

- **Inspect:** Inspect key dimensions, tenant scope, validity, empty-value handling, source failures and shared-fill ownership.
- **Method:** Use identity-aware keys and generation checks on replacement/deletion; separate a waiter's cancellation from shared fill lifetime.
- **Avoid misdiagnosis:** Old completion can resurrect invalidated data; treating zero or an empty list as a miss changes semantics.
- **Check the result:** Test cross-tenant keys, zero TTL, empty values, invalidate-during-fill, late rejection and one canceled waiter with another still active.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When an authorization change can outlive a cached response:** Invalidate or version the relevant identity boundary; a long TTL cannot substitute for access control.
- **When multiple consumers share an in-flight fill:** Separate waiter lifetimes from fill ownership. Test cancelling one waiter while another completes, and an old rejection arriving during a newer fill.

## Deliver and verify

- Key and state/lifetime contract, chosen invalidation and cancellation ownership, implementation when requested, and independent isolation/race/failure evidence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A cancelled or obsolete caller cannot poison another consumer or a newer fill; failures are recoverable according to the stated cache policy. Key collisions and valid falsey values do not cause cross-identity reuse or extra fetches.

## Stop and recover

- Do not treat caching as a fix for incorrect queries. No production flush or shared-cache changes without explicit scope.

## Example requests

- **Normal (plan):** Plan tenant-safe cache keys and invalidation for invoice summaries.
- **Edge (apply):** Fix cached dashboard data leaking between accounts with identical filters.
- **Blocked (inspect):** Inspect cache logic without flushing production or assuming current hit-rate data.
