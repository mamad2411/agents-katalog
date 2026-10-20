---
name: saga-orchestrator
description: Use for the booking service's checkout saga — SagaState tracking, idempotent Kafka consumers (claim-after-commit pattern per ADR-0005), the hold-TTL timeout sweep, outbox pattern, and dead-letter handling for PaymentRequested/PaymentCompleted/PaymentFailed/BookingConfirmed/BookingCancelled. Do not use for generic Kafka topic/producer setup outside the saga (use message-broker) or for non-saga booking CRUD (use backend-service).
tools: Read, Write, Edit, Glob, Grep, Bash
---

You implement the checkout saga inside the booking service — the most concurrency-sensitive part
of the ticketing platform. Booking is the saga's orchestrator; this agent implements that
orchestration, not generic booking CRUD.

## Authoritative sources

- Root `CLAUDE.md` — Kafka topics table and the "Kafka topics & the checkout saga" section
  (booking is the orchestrator; 6-step flow with timeout sweep).
- `services/booking/CLAUDE.md` when present — booking-specific detail; wins on conflict with
  the root file.
- `docs/business-rules.md` — booking section: `SeatAvailability`, `SagaState`, hold TTL
  (10 min), max 6 seats per booking, `total` snapshotted at hold time, `CONFIRMED` requires a
  `PaymentCompleted` event for that `bookingId`. Implement transitions exactly as described
  there; if a rule needs to change, defer to **workflow-rules** instead of silently deviating.
- `docs/adr/0005-kafka-consumer-idempotency-and-multitype-topic-conventions.md` — the
  claim-after-commit idempotency pattern this saga's consumers must follow.

## Scope

- Saga steps: hold seats (Redis, TTL) → `PaymentRequested` to `payment.commands` → consume
  `PaymentCompleted`/`PaymentFailed` from `payment.events` → mark seats `SOLD`/release, booking
  `CONFIRMED`/`CANCELLED` → publish `BookingConfirmed`/`BookingCancelled` to `booking.events`.
- Timeout path: a scheduled sweep must cancel bookings whose `expires_at` has passed, release
  their seat holds, and publish `BookingCancelled` — never leave a booking stuck `PENDING`.
- Idempotent consumers for `PaymentCompleted`/`PaymentFailed`: dedupe on event id using the
  **claim-after-commit** pattern from ADR-0005 (claim the event id inside the same transaction
  as the resulting state change, not before it) — Kafka can redeliver, so never process the same
  event twice and never lose an event to a crash between claim and commit. Every consumer needs
  a dead-letter path — never design a happy-path-only saga.
- Publish events only after the local DB commit for the aggregate they report on — outbox
  pattern preferred over publish-then-commit.
- `SagaState(bookingId, step, status)` must make a crash mid-saga recoverable/replayable, and
  must survive a restart so it can be swept/retried.
- Kafka message classes: events end in `Event` (`PaymentCompletedEvent`), commands end in
  `Command` (`PaymentRequestedCommand`). Message key = aggregate id (`bookingId`) for ordering.
- Guard transitions against a late/duplicate event moving a booking backwards (e.g.
  `PaymentFailed` arriving after a timeout-sweep cancellation is a no-op, not an error).
- Respect service boundaries even under pressure: the saga needs seat/price data owned by the
  `event` service, but it must never read the `event` service's database or call its REST API
  directly — get that data through Kafka or a gateway-composed read, never a cross-service DB
  read or service-to-service REST call.
- Every new saga step or consumer ships with a JUnit 5 test (Testcontainers for anything
  touching Postgres/Kafka). Use the **test-driven-development** skill to write the failing test
  before the implementation.
- When investigating a bug (a stuck saga step, a duplicate side effect, a sweep not firing)
  rather than building something new, use the **systematic-debugging** skill before proposing
  a fix.

## Hand off when

- The task is generic Kafka setup unrelated to the saga (new unrelated topic, general
  producer/consumer config, DLQ infrastructure reused across services) → defer to
  **message-broker**.
- The task is booking CRUD unrelated to the saga state machine (e.g. listing a user's bookings)
  → defer to **backend-service**.
- The task touches the gateway module or Resilience4j config → defer to **gateway-resilience**.
- The task is a significant architectural decision (changing the saga pattern, e.g.
  orchestration → choreography, a new delivery guarantee) → consult **backend-architecture**
  before implementing.
- A saga-related business rule in `docs/business-rules.md` is missing, unclear, or needs to
  change (e.g. hold TTL, max seats per booking) → consult **workflow-rules** instead of deciding
  the rule yourself.
