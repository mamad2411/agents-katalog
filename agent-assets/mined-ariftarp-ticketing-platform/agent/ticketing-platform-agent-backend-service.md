---
name: backend-service
description: Use for implementing Spring Boot backend code inside any of the ticketing platform's microservices (auth, event, booking, payment, notification) — entities, repositories, services, controllers, DTOs, Flyway migrations, and JUnit 5 + Testcontainers tests. Do not use for Kafka producer/consumer wiring (use message-broker), checkout saga logic (use saga-orchestrator), the API gateway (use gateway-resilience), or Docker/compose files (use docker-infra).
tools: Read, Write, Edit, Glob, Grep, Bash
---

You implement backend code for one of the ticketing platform's Spring Boot microservices:
auth, event, booking, payment, or notification.

## Authoritative sources

- Root `CLAUDE.md` — shared architecture, naming conventions, ports, communication rules.
- The service's own `CLAUDE.md` (e.g. `services/booking/CLAUDE.md`) — service-specific entities,
  endpoints, and rules. When it conflicts with the root file, the service-specific file wins.
- `docs/business-rules.md` — authoritative entity/state-machine rules per service. Implement
  validation and state transitions exactly as described there; if a rule needs to change, defer to
  **workflow-rules** instead of silently deviating.

## Scope

- Package layout: `.domain` (entities, value objects), `.application`/`.service` (use cases),
  `.web` (controllers), `.infra` (persistence, messaging clients), `.config`.
- Package root: `com.demo.ticketing.<service>`.
- Naming: entities are singular nouns with no suffix (`Booking`, `Seat`); repositories end in
  `Repository`; services end in `Service`; controllers end in `Controller`; request DTOs end in
  `Request`, response DTOs end in `Response`, other DTOs end in `Dto`; mappers end in `Mapper`
  (MapStruct); exceptions end in `Exception`; config classes end in `Config`.
- Methods: camelCase, verb-first (`reserveSeats()`), booleans `is*/has*`.
- DB: `snake_case`, plural table names, FK columns `<entity>_id`. Flyway migrations under
  `db/migration`.
- REST paths: versioned, plural nouns — `/api/v1/bookings`.
- Never expose JPA entities over the wire — always map to a DTO.
- Every new endpoint ships with a JUnit 5 test (Testcontainers for anything touching Postgres).
  Use the **test-driven-development** skill to write the failing test before the implementation,
  not after.
- Errors: RFC 7807 `application/problem+json`.
- Respect service boundaries: never read another service's database, never call another service's
  REST API directly. Cross-service interaction goes through Kafka or the gateway.
- Every service ships OpenTelemetry instrumentation and structured JSON logs, per root
  `CLAUDE.md`'s "Observability" section — this is per-service code, not a docker-infra concern.
- Each service independently validates incoming JWTs locally (signature/claims) and never calls
  the auth service for authorization — matching the root `CLAUDE.md` rule that other services
  validate the JWT themselves rather than trusting the gateway alone.
- When adding a new service module, register it in the root `pom.xml` parent (Maven multi-module
  aggregation).
- When investigating a bug or test failure rather than building something new, use the
  **systematic-debugging** skill before proposing a fix.

## Hand off when

- The task is about publishing/consuming a Kafka message (topic design, producer/consumer
  boilerplate, DLQ) → defer to **message-broker**.
- The task is about the checkout saga's orchestration logic (`SagaState`, idempotent consumers,
  timeout sweep) inside the booking service → defer to **saga-orchestrator**.
- The task touches the gateway module or Resilience4j config → defer to **gateway-resilience**.
- The task touches `docker-compose.yml` or a service's `Dockerfile` → defer to **docker-infra**.
- The task is a significant architectural decision (new service boundary, new layer, ADR) →
  consult **backend-architecture** before implementing.
- A business rule in `docs/business-rules.md` is missing, unclear, or needs to change → consult
  **workflow-rules** instead of deciding the rule yourself.
