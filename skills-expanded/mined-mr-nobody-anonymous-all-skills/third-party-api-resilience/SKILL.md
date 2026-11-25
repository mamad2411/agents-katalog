---
name: third-party-api-resilience
description: "Harden integrations with external APIs: timeouts, retry budgets, circuit breaking, rate-limit awareness, caching and graceful degradation."
type: procedural
category: integration
domain: integration
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - third party api timeout
  - retry storm
  - circuit breaker design
  - rate limit handling
  - external api degradation
keywords:
  - resilience
  - timeout
  - retry
  - circuit-breaker
  - rate-limit
  - backoff
source: custom
enabled: true
---

# Third-Party API Resilience

## Purpose

Harden integrations with external APIs: timeouts, retry budgets, circuit breaking, rate-limit awareness, caching and graceful degradation.

## When to Use

- A dependency's latency or outages cascade into your service.
- You must respect a provider's rate limits without dropping user requests.
- Failures need explicit degradation instead of hanging requests.

## When NOT to Use

- The dependency is internal and in-process with no network hop.
- You control both ends and can use a durable queue instead of retries.
- The failure is a bug in your own code rather than an availability problem.

## Capabilities

- Set layered timeouts (connect, read, total) below the caller's deadline.
- Retry only idempotent operations with jittered exponential backoff.
- Break circuits on sustained failure and recover gradually with probes.
- Degrade to cached or partial results with visible status.

## Inputs

- The provider's documented rate limits, quotas and status page.
- The caller's deadline budget and the acceptable degradation behaviour.
- Observed error rates and latency percentiles.

## Workflow

1. Map the call graph and assign each hop a deadline smaller than its caller's.
2. Classify errors: retryable transport faults versus deterministic 4xx failures.
3. Add a circuit breaker with a defined open/half-open policy.
4. Cache stable responses with explicit invalidation.
5. Add idempotency keys for writes and test with fault injection.

## Tools

- HTTP client with retry support
- circuit-breaker library
- feature flags for degradation

## Examples

- `curl -sS -m 2 https://api.example/health`
- `allskills explain integration.third-party-api-resilience --query "retry storm"`
- `allskills route "external API keeps timing out"`

## Safety

- Retrying non-idempotent writes duplicates payments and orders; require keys.
- Retries without jitter synchronize clients into a thundering herd.
- Never log full provider error payloads; they may contain secrets or PII.

## Source

All-Skills canonical library (`skills/integration/third-party-api-resilience`). First-party skill, maintained in this repository.

## Notes

- Retry budgets bound total extra load; unbounded retries turn an incident into an outage.
- Timeouts should shrink as you go deeper into the call chain, not grow.
- Pairs with: `integration/webhook-delivery-design`, `observability/slo-sli`.
