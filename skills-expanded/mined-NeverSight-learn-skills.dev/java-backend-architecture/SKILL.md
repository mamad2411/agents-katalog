---
name: java-backend-architecture
description: Design high-throughput Java backend systems with clear module boundaries, reactive I/O, resiliency, and production-grade observability.
version: 0.1.0
triggers:
  - java
  - spring boot
  - webflux
  - architecture
  - backend
  - sse
  - scalability
---

# Java Backend Architecture

Use this skill when building or reviewing Java backend services.

## Principles

- Prefer clear boundaries: `api`, `application`, `domain`, `infra`
- Keep hot paths non-blocking when targeting large numbers of concurrent streams
- Separate provider adapters from transport adapters
- Make rate limits, auth, and tenant boundaries explicit
- Design for observability from the start

## For high-concurrency streaming systems

- Prefer Spring WebFlux or Netty-based transport over thread-per-request models
- Avoid blocking JDBC on the streaming path; use R2DBC or isolate blocking work on dedicated pools
- Keep response chunks small and predictable
- Cap context size and message history early
- Put per-tenant quotas and circuit breakers at the edge

## Delivery checklist

- REST + SSE endpoints separated cleanly
- Auth and API keys in middleware/filter layer
- Skill resolution in a dedicated module
- LLM provider abstraction behind an interface
- Redis for session memory, rate limiting, and fan-out state
- Micrometer + Prometheus for p95/p99, active streams, tokens/sec
- k6 or Gatling benchmark before production rollout
