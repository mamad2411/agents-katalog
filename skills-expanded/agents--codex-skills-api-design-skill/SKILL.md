---
name: api-design
version: 1.0.0
description: Contract design principles for APIs — resource modeling, error shape, pagination, idempotency keys, and what makes a contract stable to evolve. Load when designing a new API or reviewing one for consumer-friendliness and long-term stability. Do NOT use for versioning an already-published contract or planning a sunset — that is `api-versioning`.
---

# API Design

## Resource/operation modeling

Model around what the consumer actually needs to do, not around internal data structures. A leaky API that mirrors the database schema couples every consumer to internal implementation details that should be free to change.

## Consistency

Consistent naming, casing, pagination style, and error shape across every endpoint in the same API — an inconsistent API forces every consumer to special-case each endpoint.

## Error contract

Errors are part of the contract, not an afterthought: stable error codes/shapes, actionable messages, correct HTTP status semantics (don't return 200 with an error body). A consumer should be able to build reliable error handling without reading source code.

## Pagination and large collections

Never return an unbounded collection. Prefer cursor-based pagination for anything that mutates during iteration; state the page-size default and maximum explicitly.

## Idempotency

For any mutating operation that a client might retry, support an idempotency key so a retried request doesn't duplicate the side effect (see `distributed-systems`).

## Designing for evolution

Prefer additive changes (new optional field, new endpoint) over breaking ones. Never repurpose a field's meaning — add a new one. State the versioning strategy up front (see `api-versioning`) rather than discovering the need for one after the first breaking change is forced.

## Documentation as part of the design

An API isn't done until its contract is written down somewhere a consumer can find without reading the implementation — schema (OpenAPI/GraphQL SDL/protobuf) checked in alongside the code, not maintained separately by hand.
