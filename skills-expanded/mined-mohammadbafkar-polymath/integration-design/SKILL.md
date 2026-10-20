---
name: integration-design
description: Design integration between two services — sync vs async, API gateway / BFF placement, anti-corruption layer, contract + versioning, ports-and-adapters, and backpressure handling.
---

# integration-design

> The contract between two services outlives both implementations. Design the seam — sync or async, who owns the schema, how it evolves — before the first call is wired.

## When to use

- Two services (or a client tier and services) need to talk and you are choosing the integration style.
- A client is making many chatty calls, or an upstream model is leaking into a downstream service.
- A workflow invokes `polymath-architecture:integration-design`.

Not this when: the flow is an asynchronous business process with compensation — that is `event-driven-design`. For the REST resource/verb/status-code details of one endpoint, that is `polymath-backend:api-design-rest`.

## Inputs

- The two parties, what data/operations cross the boundary, and the coupling/latency tolerance.
- Whether either party is legacy or third-party (drives the anti-corruption layer).

## Procedure

1. **Sync vs async**: request/response (REST/gRPC) when the caller needs an answer now and the callee is fast and available; messaging/events when you want temporal decoupling, buffering, or fan-out. State the choice per interaction, not per system.
2. **Place a gateway / BFF** where it earns its keep: an API gateway for cross-cutting concerns (auth, rate-limit, routing) at the edge; a *Backend-for-Frontend* when distinct clients (web/mobile) need tailored aggregation — avoids chatty clients and leaking N services to the UI.
3. **Add an anti-corruption layer** whenever you integrate with a legacy or third-party model: translate at the boundary so their model never becomes your model. This is the ports-and-adapters / hexagonal seam — the domain talks to a port, the adapter speaks their dialect.
4. **Define the contract explicitly**: schema (OpenAPI/protobuf/event schema), ownership (who can change it), and a compatibility rule (additive-only, consumer-driven contracts, or versioned). Breaking changes need a versioning + deprecation path.
5. **Decide error & partial-failure semantics**: timeouts, retries, and what a caller does when the callee is degraded (hand off to `resilience-design` for the parameters).
6. **Handle backpressure** for async edges: bounded queues, consumer lag monitoring, and what happens when the consumer can't keep up (drop, slow the producer, scale out) — never an unbounded buffer.
7. **Minimize coupling**: prefer a narrow, stable contract over a wide one; flag any integration that requires sharing a database.

## Output

- A one-page integration spec: sync/async decision per interaction, gateway/BFF placement, anti-corruption-layer boundaries, the contract (schema + owner + compatibility/versioning rule), error semantics, and the backpressure plan.

## Quality bar

- Each interaction's sync/async choice is justified by need, not habit.
- Every cross-boundary contract names an owner and an evolution rule.
- Integration with legacy/third-party goes through an anti-corruption layer.
- No async edge has an unbounded queue; backpressure behavior is defined.
