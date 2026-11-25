---
name: api-integration
description: "REST/GraphQL integration: rate limiting, exponential backoff, circuit breakers, webhook handling, and HMAC signature verification"
category: integration
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/integration/api-integration/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Enterprise API Integration

## Scope
Engineering resilient, secure integrations with external third-party APIs and microservices across REST, GraphQL, and event-driven webhooks.

## Resilience & Security Patterns
- **Resilience Patterns**:
  - Exponential Backoff with Full Jitter: $t = \operatorname{random}(0, \min(M, B \cdot 2^{\text{attempt}}))$.
  - Circuit Breaker Pattern: Closed $\to$ Open (after $N$ consecutive failures) $\to$ Half-Open (trial requests).
- **Webhook Security**: Verifying HMAC-SHA256 signatures on incoming webhook payloads using shared secrets to prevent forgery.
- **Idempotency Keys**: Including unique client-generated UUIDs (`Idempotency-Key` header) to safely retry mutating operations.

## Tools & Standards
- **Software**: Postman, Insomnia, Polly (.NET), tenacity (Python).
