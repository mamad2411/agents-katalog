---
id: "backend.distributed-systems"
name: "Backend Architecture & Distributed Systems"
version: "1.2.0"
domain: "backend"
description: "Design and implement resilient, scalable backend architectures, strict API contracts, idempotent operations, and distributed failure tolerance with maximum efficiency."
triggers:
  - "Designing API contracts (REST, OpenAPI, tRPC, gRPC)"
  - "Implementing authentication, authorization, or middleware pipelines"
  - "Designing distributed asynchronous workflows, message queues, or event processing"
  - "Handling idempotency, rate limiting, circuit breaking, or retry policies"
prerequisites:
  - "architecture.system-design"
  - "security.secure-development"
risk_profile: "high"
---

# Backend Architecture & Distributed Systems

## Overview
This skill embodies the rigor of a Principal Distributed Systems Architect. It guides AI agents in authoring rock-solid backend services, bulletproof API boundaries, and resilient asynchronous pipelines that withstand partial network failures, traffic spikes, and distributed state divergence.

## 🎯 Token Conservation & High-Yield Heuristics
1. **Schema-First Specification**: Always define request/response schemas (Zod, Pydantic, OpenAPI) first. Clean contract schemas reduce ambiguity and eliminate hundreds of lines of speculative validation code.
2. **Standardized Error Envelopes**: Use RFC 7807 (Problem Details for HTTP APIs) or unified error envelopes (`{ success: false, error: { code, message, details } }`). Do not improvise random error formats.
3. **Deterministic DTOs**: Never pass raw database entities (ORM models) through public API endpoints. Map them through explicit Data Transfer Objects (DTOs).

## 📐 Core Engineering Directives

### 1. API Contract & Boundary Defense
- **Explicit Input Validation**: Validate every payload at the perimeter before it touches business logic. Reject unknown properties (`strip` or `strict` schemas) to prevent mass-assignment vulnerabilities.
- **HTTP Semantics & Status Codes**: Use precise status codes: `200 OK` (success with body), `201 Created` (resource created with `Location` header), `204 No Content`, `400 Bad Request`, `401 Unauthorized` (unauthenticated), `403 Forbidden` (authenticated without permission), `404 Not Found`, `409 Conflict`, `422 Unprocessable Content`, `429 Too Many Requests`, `500 Internal Server Error`.
- **Pagination & Query Limits**: All collection endpoints must enforce default and maximum limits (e.g. `limit <= 100`). Never return unbounded arrays from database queries.

### 2. Distributed Resilience & Concurrency
- **Idempotency Keys**: All mutating POST/PUT requests involving payments, orders, or state changes must accept an `Idempotency-Key` header stored in an atomic cache (Redis / DB lock) with TTL.
- **Circuit Breakers & Timeouts**: Every outgoing network call to external APIs, databases, or microservices must have:
  - Explicit connection and socket timeouts (e.g. $2\text{s}$ connect, $5\text{s}$ read).
  - Exponential backoff with full jitter for retries ($T = \min(M, B \times 2^{\text{attempt}}) \pm \text{jitter}$).
  - Circuit breakers (tripping on $> 50\%$ failure rate over a rolling window).
- **Transactional Outbox Pattern**: Never publish messages to an external broker (Kafka, RabbitMQ, SQS) directly inside a database transaction. Write events to an `outbox` database table within the same ACID transaction, then asynchronously dispatch to the broker to guarantee at-least-once delivery without dual-write corruption.

### 3. Caching & State Management
- **Cache-Aside with Dogpile Defense**: When using Redis/Memcached, guard against cache stampedes using mutual exclusion locks, probabilistic early expiration (XFetch), or background cache refreshing.
- **Deterministic Cache Keys**: Format cache keys hierarchically: `domain:entity:id:version` (e.g. `user:profile:usr_123:v2`).

### 4. Observability & Context Propagation
- **Distributed Tracing**: Propagate `traceparent` (W3C Trace Context) and `x-request-id` across all internal calls and log entries.
- **Structured JSON Logging**: Emit logs as machine-parseable JSON containing `timestamp`, `level`, `trace_id`, `span_id`, `service`, `message`, and contextual metadata. Never log raw plaintext strings or passwords/tokens.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Backend Reality | Mandatory Action |
|---|---|---|
| *"I'll return the full database user object in the API response."* | Leaks password hashes, salt, internal timestamps, and PII to consumers. | Map through an explicit output DTO omitting all sensitive fields. |
| *"I don't need a timeout on this HTTP call; it will finish fast."* | External services stall, exhaust server connection pools, and trigger cascade outages. | Attach strict cancellation tokens and timeout headers to all network operations. |
| *"I'll do the retry immediately in a while loop."* | Creates thundering herd effects and DDoS attacks against recovering dependencies. | Implement exponential backoff with full jitter and a max retry ceiling (e.g. 3 attempts). |
| *"A simple try-catch block returning status 500 for everything is fine."* | Hides actionable client errors, obscures root cause, and breaks client error recovery. | Categorize into domain error classes (Validation, NotFound, Unauthorized, Conflict, System). |

## ✅ Backend Verification Checklist
- [ ] All endpoint inputs validated with strict schemas before execution.
- [ ] Explicit timeouts and retry limits configured on all outgoing network calls.
- [ ] Mutating state actions support idempotency keys.
- [ ] Zero unhandled promise rejections or uncaught exceptions.
- [ ] RFC 7807 structured error responses returned for all error conditions.

