---
name: wp-rest-api-performance-and-observability
description: Reviews WordPress REST API query bounds, payloads, caching, CORS, rate-limit integration, logging, latency, and failure visibility. Use for performance work or production diagnostics.
license: MIT
compatibility: "General WordPress REST API guidance; checked against WordPress 7.0.1 documentation."
---

# WordPress REST API Performance and Observability

## Use this skill when

- An endpoint or headless client is slow.
- Collections or embedded responses are large.
- Adding caches, a CDN, CORS, or rate limiting.
- Investigating timeouts, error spikes, or external dependency failures.
- Designing privacy-safe API logs and metrics.

## Approach

1. Reproduce with exact route, method, authentication context, parameters, and environment.
2. Measure latency, query count, payload size, memory, cache state, and external calls.
3. Bound database and remote work.
4. Reduce fields and embedding.
5. Define cache scope, keys, invalidation, and private-response rules.
6. Review CORS and credential behavior as security policy.
7. Integrate with project-owned rate limiting rather than inventing an in-plugin global limiter.
8. Add redacted route-level metrics, traces, and error classification.
9. Verify changes with cold/warm and authorized/anonymous tests.

## Workflow

Use [rest-api-performance-workflow.md](workflows/rest-api-performance-workflow.md).

## Resources

- [caching-cors-and-rate-limit-guidance.md](resources/caching-cors-and-rate-limit-guidance.md)
- [observability-and-privacy-checklist.md](resources/observability-and-privacy-checklist.md)

## Output

Return:

- Reproduction evidence.
- Bottleneck classification.
- Proposed change and cache/security implications.
- Before/after measurements.
- Observability additions.
- Rollback and regression tests.
