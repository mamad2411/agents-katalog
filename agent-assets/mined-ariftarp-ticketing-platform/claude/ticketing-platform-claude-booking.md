# CLAUDE.md — booking-service

> Loaded when working inside `services/booking/`. See root `CLAUDE.md` for shared conventions and
> `docs/business-rules.md` (section "booking (core)") for the authoritative domain rules.

## What this service owns

The heart of the system: seat *availability* state, time-boxed holds, bookings, and the checkout
**saga** (booking is the orchestrator, per ADR-0001). Port `8083`, database `ticketing_booking`
(role `booking_app`), package root `com.demo.ticketing.booking`.

| Entity            | Owns                                                                 |
|--------------------|-----------------------------------------------------------------------|
| `Booking`          | userId, eventId, `status`, `total`, `createdAt`, `expiresAt`          |
| `BookingItem`      | one held/sold seat of a booking: `seatId`, `price` (snapshot at hold time) |
| `SeatAvailability` | per `(eventId, seatId)` sale state: `AVAILABLE`/`HELD`/`SOLD`         |
| `SagaState`        | per-booking checkout-saga progress (`step`, `status`) for crash recovery |

`Booking.status` lifecycle: `PENDING -> CONFIRMED`, `PENDING -> CANCELLED`, `PENDING -> EXPIRED`
(root `CLAUDE.md`'s enum and `docs/business-rules.md`'s status lifecycle agree — no reconciliation
needed). `SeatAvailability.status` never has a row implying "sold/held" for a seat unless one
exists; an absent row is implicitly `AVAILABLE` (see the future availability endpoint below).

## Phase 7 progress — what's built vs. deliberately deferred

This was a two-pass phase, split across two agents, matching `docs/roadmap.md` Phase 7:

**Pass 1 (`backend-service`, plain CRUD/entity layer):**
- Flyway schema for all four tables (`db/migration/V1__create_bookings_schema.sql`).
- `Booking`/`BookingItem`/`SeatAvailability`/`SagaState` entities + repositories.
- `GET /api/v1/bookings/{id}` and `GET /api/v1/bookings?userId=&status=` (read-only).
- Testcontainers coverage for both endpoints (`BookingControllerTest`) and a Docker-free mapper
  unit test (`BookingMapperTest`).

**Pass 2 (`saga-orchestrator`, this pass — the concurrency-sensitive hold/lock mechanism):**
- `POST /api/v1/bookings/hold` — see "The hold endpoint & Redis lock design" below.
- `SeatHoldLockService` (`infra/redis`) — the Redis distributed lock on `eventId:seatId`, 10-minute
  TTL, `SET key value NX EX 600`.
- `BookingHoldService` (`application`) — orchestrates lock acquisition + the atomic DB write; the
  only code path (besides Phase 8's future saga consumers) allowed to call
  `SeatAvailability.markHeld()`.
- `HoldBookingRequest`/`HoldSeatRequest` DTOs, `SeatUnavailableException` (409),
  `InvalidHoldRequestException` (400), plus `GlobalExceptionHandler` wiring for both and for
  `MethodArgumentNotValidException` (bean validation on the new request DTOs).
- `BookingHoldControllerTest` (happy path, already-`HELD`/`SOLD` seat → 409 with full rollback,
  >6 seats → 400, duplicate `seatId` → 400, empty seat list → 400) and — **the core deliverable of
  this pass** — `SeatHoldConcurrencyTest`, which races two concurrent clients on the same single
  seat across 25 distinct seats per run via a `CountDownLatch` starting gate (not two sequential
  calls) and asserts exactly one `200`/one `409` every time, plus a durable-state check (exactly one
  `HELD` row, one `booking_items` row) per seat. Run independently 4 times during this pass (100
  total race iterations across process/container restarts) with zero flakes.

**Still NOT here — Phase 8, saga wiring (`saga-orchestrator`):**
- `GET /api/v1/bookings/availability?eventId=` — the live-availability read endpoint the frontend
  merges with event's seat-map layout (business-rules.md's "Seat map contract"). Deferred to keep
  this pass scoped to the write-path lock mechanism; the schema/repository support already exists
  (`SeatAvailabilityRepository.findByEventId`).
- `POST /api/v1/bookings/{id}/checkout`, the `payment.events` consumer, `Booking.status` mutations
  to `CONFIRMED`/`CANCELLED`/`EXPIRED`, `SagaState` transitions, the outbox pattern, and the timeout
  sweep that releases expired Redis holds and stale `HELD` rows — see "Known gap: no sweep yet"
  below, this is the most load-bearing thing Phase 8 must land.

Do not treat the absence of these as an oversight if you land here later — check
`docs/roadmap.md` Phase 7/8 and this file's git history before adding them ad hoc.

## The hold endpoint & Redis lock design

`POST /api/v1/bookings/hold` — body `HoldBookingRequest { userId, eventId, seats: [{seatId, price}] }`.
200 with a `BookingResponse` (same shape as the read endpoints) on success; 409 problem+json if any
seat is already locked/held/sold; 400 for more than 6 seats, an empty seat list, or a duplicate
`seatId` in the same request.

**Why the Redis key doubles as both the lock and the hold itself:** `docs/roadmap.md` Phase 7 says
"Redis distributed lock on `eventId:seatId`, 10-minute TTL" — one artifact, not a short-lived mutex
plus a separate long-lived hold marker. `SeatHoldLockService.tryAcquire` does a single atomic
`SET booking:seat-hold:{eventId}:{seatId} {holdToken} NX EX 600` (via
`StringRedisTemplate.opsForValue().setIfAbsent(key, value, ttl)`, which Lettuce sends as one atomic
command). This is what makes the concurrent seat-race path (business-rules.md) resolve to exactly
one winner without any DB round-trip race: the losing request's `SETNX` simply returns `false`, and
`BookingHoldService` rejects it with 409 immediately — no blocking wait, no DB unique-constraint
retry. `release` uses a Lua compare-and-delete script so a caller can never delete a lock it doesn't
own (classic distributed-lock hygiene), used when this request's lock acquisition or DB write fails
partway and everything already acquired must be rolled back.

**Write flow (`BookingHoldService.holdSeats`):**
1. Validate no duplicate `seatId`s in the request (bean validation already rejects empty/>6-seat
   lists via `@NotEmpty`/`@Size(max=6)` on `HoldBookingRequest.seats`).
2. Acquire the Redis lock for every requested seat, fail-fast: the first seat that's already locked
   aborts the loop.
3. If any acquisition failed, release everything acquired so far and throw `SeatUnavailableException`
   (409) — no DB write ever happens for a request that loses the race.
4. If every seat's lock was acquired, run the DB write in one `TransactionTemplate`-wrapped
   transaction (explicit `TransactionTemplate`, not a `@Transactional` method on `this` — avoids the
   Spring self-invocation proxy pitfall of calling an `@Transactional` method from another method on
   the same bean instance): create the `PENDING` `Booking`, snapshot each seat's price onto a
   `BookingItem`, and `SeatAvailability.markHeld()` (or insert a new `HELD` row if none existed).
   This step also re-checks each seat's `SeatAvailability` status as defense in depth — it can never
   race with another concurrent hold on the same seat (the Redis lock already serialized that), but
   it does catch the "stale `HELD` row, expired Redis key" gap described below. Any conflict here
   rolls back the whole transaction (no partial holds) and releases every Redis lock this request
   acquired.
5. On success, the Redis keys are **not** released — they remain live for the full 10-minute TTL as
   the actual seat hold. Phase 8 releases them explicitly on payment failure/timeout, or lets them
   naturally expire once the seat is `SOLD` (Redis TTL expiry after confirmation is harmless since
   `SeatAvailability.SOLD` is what actually gates future holds by then).

**Known gap — no timeout sweep yet (Phase 8):** if a hold's 10-minute Redis TTL elapses before
Phase 8's sweep job exists, the Redis key disappears but the `SeatAvailability` row stays `HELD`
forever (nothing resets it to `AVAILABLE`). A new hold request for that seat would then successfully
acquire the now-free Redis key but get rejected by `BookingHoldService`'s defensive DB check
(seat 4 above) instead of the "should be available again" outcome — a real inconsistency this
phase's tests deliberately do not exercise (their TTL windows never elapse mid-test). This is exactly
`docs/roadmap.md` Phase 8's "hold-expiry edge path"; do not attempt to route around this gap in
Phase 8's DB check without also removing the sweep's necessity — the sweep is what closes it.

**Known gap — price is client-supplied, not fetched from event:** root `CLAUDE.md` requires getting
event-owned data "through Kafka or a gateway-composed read, never a cross-service DB read or
service-to-service REST call," but no Kafka catalog/pricing topic exists (Phase 6-8's topics are
`payment.commands`/`payment.events`/`booking.events` only) and `docs/business-rules.md`'s "Seat map
contract" explicitly forbids a gateway-composed merge endpoint for seat/price data. Since neither
sanctioned channel exists yet, `HoldSeatRequest.price` is accepted as given by the caller (who, per
the Seat map contract, already fetched real prices from `GET /api/v1/events/{eventId}/seats` via the
gateway before calling hold) rather than inventing a forbidden direct REST call to event. This
mirrors this service's existing `userId` JWT-deferral precedent — a documented demo-scope
simplification, not a security decision. **Flagged for `workflow-rules`/`backend-architecture`**: the
real fix is most likely a Kafka-published price-tier snapshot event has to change before this is
production-real (trusting client-supplied price is fine for this interview demo, not for real money).

## Endpoint contract (Phase 7, both passes)

| Endpoint | Returns |
|----------|---------|
| `GET /api/v1/bookings/{id}` | `BookingResponse` — id, userId, eventId, status, total, createdAt, expiresAt, `items[]` (`seatId`, `price`). 404 problem+json if missing. |
| `GET /api/v1/bookings?userId=&eventId=&status=` | `BookingResponse[]` for one user, newest first (`createdAt desc`). `eventId` and `status` are both optional (`status` is one of `PENDING`/`CONFIRMED`/`CANCELLED`/`EXPIRED`); omitted = any event / any status. `userId` is **required** — 400 problem+json if missing. `eventId=&status=PENDING` is the frontend's "resume my in-progress hold on page refresh" query and is guaranteed at most one result (see `BookingHoldService`'s append-not-duplicate invariant: at most one `(userId, eventId, PENDING)` booking exists at a time). |
| `POST /api/v1/bookings/hold` | `BookingResponse` (200) for a new `PENDING` booking with up to 6 held seats; see "The hold endpoint & Redis lock design" above for the 409/400 cases. |

**`userId=me` note:** `docs/roadmap.md` Phase 7 describes the list endpoint's query param as
`?userId=me&status=`, implying the caller resolves "me" to the current user from their JWT.
This service does **not** parse the JWT yet — `userId` is a plain numeric query parameter, exactly
like the `Authorization` header the gateway forwards unchanged (`gateway/CLAUDE.md`: "no `X-User-*`
headers are added"). This mirrors event's Phase 5 precedent of deferring JWT validation
(`services/event/CLAUDE.md`, "Not here (deliberately)") rather than scope-creeping local JWT
validation into a CRUD-only task. Whoever wires the frontend's `userId=me` needs booking to
independently validate the JWT and resolve `sub` -> `userId` first — flag this to `workflow-rules`/
`backend-architecture` before Phase 11 frontend work assumes it already works.

Errors are RFC 7807 `application/problem+json` via `web/GlobalExceptionHandler`.

## Kafka contracts (Phase 6 — already available, wire up producer/consumer in Phase 8)

booking depends on the shared `com.demo.ticketing:messaging` module
(`docs/adr/0003-shared-messaging-module-for-kafka-contracts.md`) for:

- `com.demo.ticketing.messaging.command.PaymentRequestedCommand` — produced to
  `payment.commands` (key = `bookingId`), after the local `SagaState` commit (outbox pattern).
- `com.demo.ticketing.messaging.event.PaymentCompletedEvent` / `PaymentFailedEvent` — consumed
  from `payment.events` (key = `bookingId`).
- `com.demo.ticketing.messaging.event.BookingConfirmedEvent` / `BookingCancelledEvent` —
  produced to `booking.events` (key = `bookingId`). `BookingCancelledEvent.reason` distinguishes
  `"PAYMENT_FAILED"` from `"HOLD_EXPIRED"` (see business-rules.md's "Flagged gaps" — there is no
  distinct `BookingExpired` topic-level event).
- `com.demo.ticketing.messaging.topic.KafkaTopics` — canonical topic name constants; do not
  hardcode topic strings.
- `com.demo.ticketing.messaging.config.KafkaProducerFactorySupport` /
  `KafkaConsumerConfigSupport` / `KafkaJsonSupport` — call these from this service's own
  `@Configuration` class to build `KafkaTemplate`/listener container factory beans.

### DLQ convention
Every `@KafkaListener` here (the `payment.events` consumer) must use a container factory built
via `KafkaConsumerConfigSupport.listenerContainerFactory(...)`, which retries 2 extra times
(fixed 1s backoff) then publishes to `payment.events.DLT`.

### Deferred to Phase 8 (saga)
- `SeatAvailability` mutations to `SOLD`, the `POST /bookings/{id}/checkout` endpoint, and the
  `PaymentRequested` producer — Phase 8, `saga-orchestrator`. (The hold endpoint's `HELD` mutation
  and the Redis lock/hold itself landed in this Phase 7 follow-up pass — see "The hold endpoint &
  Redis lock design" above.)
- The actual `@KafkaListener` for `payment.events`, the timeout sweep job (also responsible for
  releasing the Redis holds/`HELD` rows this pass creates once their TTL elapses — see "Known gap:
  no timeout sweep yet" above), and the idempotency/dedup store keyed on the consumed event's
  `eventId` — Phase 8, `saga-orchestrator`. No Kafka producer/consumer code exists in this service
  yet; this pass only added Redis code.

## Implementation notes / traps

- Package layers: `.domain` (entities), `.application` (+ `.mapper`, `.exception`), `.web` (+
  `.dto`), `.infra` (+ `.redis` — `SeatHoldLockService`), `.config` (currently empty — the Redis
  connection itself is Spring Boot auto-configuration off `spring.data.redis.host/port` in
  `application.yml`, no custom `@Configuration` class was needed; Kafka `@Configuration` classes
  land with Phase 8).
- `BookingMapper` is hand-written (not MapStruct), same rationale as `EventMapper` in the event
  service: the mapping is trivial enough that a hand-written version stays readable and keeps the
  module free of an annotation processor.
- `BookingRepository.findWithItemsById`/`findByUserId...` all use `@EntityGraph(attributePaths =
  "items")` rather than a JPQL `left join fetch ... where :status is null or ...` — event's
  `EventRepository.findForBrowse` documents a real Postgres bind-type trap with nullable-parameter
  `is null` checks; dispatching to two derived-query methods in `BookingService.listBookings`
  sidesteps that class of bug entirely rather than working around it.
- `saga_state.step`/`status` are plain `VARCHAR`, not `CHECK`-constrained enums — deliberately left
  open for `saga-orchestrator` to define the vocabulary (see business-rules.md's "Checkout
  workflow" table for the values it's likely to use: `PAYMENT_REQUESTED`/`CONFIRMED`/`CANCELLED`/
  `EXPIRED` steps, `IN_PROGRESS`/`DONE` statuses).
- `event_id`/`seat_id`/`user_id` columns are **not** foreign keys to another service's tables —
  event and auth own those ids in their own databases (no cross-service DB access, root
  `CLAUDE.md`).
- No Flyway seed data (unlike event's `V2__seed_demo_data.sql`) — booking starts empty by design;
  every test builds its own fixtures.
- `spring.jpa.hibernate.ddl-auto=validate` — Flyway owns the schema and startup fails on drift.
- The Maven parent is a plain aggregator, **not `spring-boot-starter-parent`**, so `-parameters` is
  not on by default (the root pom sets `maven.compiler.parameters`, but name every
  `@RequestParam`/`@PathVariable` explicitly anyway).

## Not here (deliberately)

- **No security/JWT validation** — see the `userId=me` note above and the hold endpoint's price gap
  above. Comes with a dedicated auth pass across services, not scoped to this phase.
- **No timeout sweep** — see "Known gap: no timeout sweep yet" above. Phase 8, `saga-orchestrator`.
- **No Kafka producer/consumer code** — the `messaging` module dependency is wired but no
  `@KafkaListener`/`KafkaTemplate` usage exists yet; see "Kafka contracts" above. This includes the
  `PaymentRequested` publish that would normally follow a successful checkout — this pass only
  builds the pre-saga hold/lock mechanism, not `POST /bookings/{id}/checkout`.
- **No `GET /api/v1/bookings/availability?eventId=`** — see "Still NOT here" above.
- **No OpenTelemetry/JSON logging yet** — cross-cutting stretch phase per `docs/roadmap.md`,
  consistent with the other services.
