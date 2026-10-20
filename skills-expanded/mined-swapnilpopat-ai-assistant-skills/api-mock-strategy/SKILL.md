---
name: api-mock-strategy
description: Choose between stubs, mocks, fakes, virtual services, and contract-driven mocks (WireMock 3, Microcks, Mockoon, Prism, MSW 2) to enable parallel development without false confidence. Use when designing test isolation or shifting integration testing left.
source: self
date_added: 2026-04-30
---

# API Mock Strategy

Mocks decouple teams and speed up tests, but they lie if not anchored to a contract. Pick the right kind of double for each layer.

## Stack Baseline (2026)

| Need | Tool |
| --- | --- |
| HTTP record/replay & stubs | WireMock 3, Mockoon, hoverfly |
| Spec-driven mocks | Prism (OpenAPI), Microcks (OpenAPI/AsyncAPI/gRPC) |
| Browser-side mocks | MSW 2 (Service Worker + Node) |
| Contract-as-mock | Pact stub server, Spring Cloud Contract |
| Async/event mocks | Microcks, Karapace mock |

## Test Double Taxonomy (Meszaros)

- **Dummy** — passed but unused.
- **Stub** — canned answers, no verification.
- **Spy** — stub that records calls.
- **Mock** — pre-programmed expectations, fails on mismatch.
- **Fake** — working but lightweight implementation (e.g., in-memory DB).

Pick the lightest double that proves the case. Prefer **fakes for state**, **stubs for queries**, **contract mocks for cross-service**.

## Decision Matrix

| Test layer | Recommended double | Why |
| --- | --- | --- |
| Unit (own code) | Stubs/fakes via DI | Fast, no I/O |
| Component (own service + DB) | Real DB via Testcontainers; stub external HTTP with WireMock | Realistic but isolated |
| Contract (between services) | Pact / Spring Cloud Contract stub | Verifies both sides agree |
| E2E in non-prod | Microcks for unstable downstreams; real for stable | Reduces flakiness |
| Browser dev/test | MSW | No network, deterministic |

## Anti-Pattern: The Mock-All Trap

Mocking everything turns tests into "the code does what I told the mocks to say." Counter:

- Always pair internal mocks with **at least one** real-integration test per dependency.
- Source mock responses from the real spec (Prism/Microcks) or recorded prod responses (with PII scrubbed).
- Run **provider verification** (Pact) on every consumer-published contract.

## WireMock 3 Snippet

```java
stubFor(post("/orders")
  .withRequestBody(matchingJsonPath("$.idempotencyKey"))
  .willReturn(jsonResponse(Map.of("id", "${random.uuid}"), 201)
    .withFixedDelay(120)));
```

## MSW 2 Snippet (browser test)

```ts
import { http, HttpResponse } from 'msw';
export const handlers = [
  http.get('/api/users/:id', ({ params }) =>
    HttpResponse.json({ id: params.id, name: 'Ada' })),
];
```

## Lifecycle & Governance

- Mocks live next to the spec; CI verifies mock conformance to spec on every change.
- Tag each mock with owner, expiry, and "pin to spec version".
- Periodically replay recorded prod traffic against mocks (shadow) to detect drift.

## Common Pitfalls

| Pitfall | Avoidance |
| --- | --- |
| Mocks drift from real API | Generate from OpenAPI/AsyncAPI; verify contracts |
| Hidden coupling on stub URLs | Centralize base URL config |
| Mocks return 200 for everything | Always model error/timeouts |
| Snapshot fixtures rot | Refresh from staging weekly with diff alert |
| MSW shipped to production | Tree-shake; guard with env check |

## References

- WireMock — https://wiremock.org/
- Microcks — https://microcks.io/
- Prism — https://stoplight.io/open-source/prism
- MSW — https://mswjs.io/
- Pact stub server — https://docs.pact.io/
- Meszaros, "xUnit Test Patterns"
