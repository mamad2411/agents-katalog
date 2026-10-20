# CLAUDE.md — Event Ticketing Platform (monorepo)

> Root memory for Claude Code. Loaded at the start of every session from the repo root.
> Per-service specifics live in each service's own `CLAUDE.md` (loaded lazily when you touch that folder).
> Keep this file lean: shared architecture, contracts, and rules only. Details go in the per-service files.

## What this project is

An event ticketing platform (browse events → pick seats → pay → get tickets) built as a
microservices system. Purpose: an interview showcase built ~80% with AI, so **every decision
must be explainable**. Prefer clarity and correctness over cleverness.

## Tech stack (do not swap without noting it in an ADR)

- **Backend:** Java 21, Spring Boot 3.x, **Maven** (multi-module), Spring Cloud Gateway
- **Resilience:** Resilience4j on the gateway (circuit breaker + timeout + retry on sync routes)
- **Messaging:** **Apache Kafka** (async events + orchestration saga)
- **Data:** PostgreSQL — **one database per service**, no shared schema
- **Caching / locks:** Redis (seat holds with TTL, distributed locks)
- **Frontend:** Next.js (App Router, TypeScript), **pnpm**
- **Local infra:** Docker Compose (Postgres, Kafka, Redis, all services, frontend)
- **Tests:** backend JUnit 5 + Testcontainers (integration); frontend **Vitest** (unit) + **Playwright** (E2E)
- **Observability:** OpenTelemetry instrumentation → **Elastic (Elasticsearch + Kibana)** for logs & traces
  (no separate tracing UI). Structured JSON logs everywhere.

## Repo layout (monorepo, single git root)

```
ticketing-platform/
├── CLAUDE.md                  ← this file (shared context)
├── docker-compose.yml         ← full local stack
├── pom.xml                    ← Maven parent (aggregates the service modules)
├── docs/
│   └── adr/                   ← Architecture Decision Records (one file per decision)
├── gateway/                   ← Spring Cloud Gateway (edge, JWT validation, routing, Resilience4j)
├── services/
│   ├── auth/         + CLAUDE.md   ← users, registration, login, JWT issuing
│   ├── event/        + CLAUDE.md   ← catalog: venues, events, seat map, price tiers
│   ├── booking/      + CLAUDE.md   ← seat availability + holds, bookings, SAGA orchestrator
│   ├── payment/      + CLAUDE.md   ← mock payment provider
│   └── notification/ + CLAUDE.md   ← consumes events, "sends" mail/SMS (mock)
└── frontend/         + CLAUDE.md   ← Next.js app
```

Add a service's `CLAUDE.md` only when you start real work in that folder — don't stub them all up front.

## Service responsibilities & bounded contexts

- **auth** — identity only. Issues JWTs. Other services validate the JWT; they never call auth for authz.
- **event** — read-heavy catalog. Owns the *static* seat map (venue layout, sections, rows, seats)
  and pricing. Does **not** track whether a seat is sold — that lives in booking.
- **booking** — the heart of the system. Owns seat *availability state* per event, holds (Redis, TTL),
  bookings, and runs the checkout **saga**. This is where the interesting concurrency lives.
- **payment** — mock. Consumes a payment command, "processes", emits success/failure. No real PSP.
- **notification** — pure consumer. Reacts to events, writes a notification log. No inbound REST.

> Decision (record as ADR-001): seat availability lives in **booking**, not event, so seat mutation
> stays inside one service and we avoid distributed writes to seat state. event stays a clean catalog.

## Communication rules

- **Sync (REST via gateway):** client-facing reads/commands. JSON. One OpenAPI spec per service.
  The gateway wraps sync routes with Resilience4j (breaker + timeout + retry).
- **Async (Kafka):** all cross-service workflow. Services never call each other's REST directly and
  **never touch another service's database**. If you need another service's data at write time,
  go through an event or a gateway-composed read.
- Errors: RFC 7807 `application/problem+json`.

## Kafka topics & the checkout saga

Topics (JSON payloads; message **key = aggregate id**, e.g. `bookingId`, for ordering):

| Topic                  | Producer      | Consumer      | Events                                   |
|------------------------|---------------|---------------|------------------------------------------|
| `payment.commands`     | booking       | payment       | `PaymentRequested`                       |
| `payment.events`       | payment       | booking       | `PaymentCompleted`, `PaymentFailed`      |
| `booking.events`       | booking       | notification  | `BookingConfirmed`, `BookingCancelled`   |

**Saga = orchestration, booking is the orchestrator:**

1. User selects seats → booking creates a `PENDING` booking and places **seat holds in Redis with a TTL**
   (e.g. 10 min), setting `expires_at`.
2. Checkout → booking publishes `PaymentRequested` → `payment.commands`.
3. payment (mock) publishes `PaymentCompleted` **or** `PaymentFailed` → `payment.events`.
4. booking consumes the result:
   - **Completed** → mark seats `SOLD`, booking `CONFIRMED`, issue ticket, publish `BookingConfirmed`.
   - **Failed** → release holds, booking `CANCELLED`, publish `BookingCancelled`.
5. **Timeout** → if the hold TTL expires before payment, a scheduled sweep cancels the booking,
   releases seats, publishes `BookingCancelled`.
6. notification consumes `booking.events` and logs a "sent" notification.

**Non-negotiables for events:** consumers must be **idempotent** (dedupe on event id — messages can
redeliver), publish only after the local DB commit (outbox pattern preferred), and every consumer
needs a dead-letter path. Don't design a happy-path-only saga.

## Data model (summary — full DDL in each service's CLAUDE.md)

- **auth:** `users(id, email, password_hash, created_at)`, `roles`, `user_roles`
- **event:** `venues`, `events(venue_id, title, starts_at, status)`, `seat_categories(event_id, name, price)`, `seats(venue_id, section, row, number)`
- **booking:** `bookings(user_id, event_id, status, total, created_at, expires_at)`,
  `booking_items(booking_id, seat_id, price)`, `seat_availability(event_id, seat_id, status)`,
  `saga_state(booking_id, step, status)` — holds themselves live in Redis, not Postgres
- **payment:** `payments(booking_id, amount, status, provider_ref, created_at)`
- **notification:** `notifications(type, recipient, channel, status, payload, created_at)`

## Conventions — general

- Package root: `com.demo.ticketing.<service>` (e.g. `com.demo.ticketing.booking`).
- Layer entities and DTOs separately; never expose JPA entities over the wire.
- One Spring Boot app per service module; Flyway for migrations (`db/migration`).
- Ports: gateway `8080`, auth `8081`, event `8082`, booking `8083`, payment `8084`,
  notification `8085`, frontend `3000`, Postgres `5432`, Kafka `9092`, Redis `6379`.
- Frontend talks **only** to the gateway (`http://localhost:8080`), never to services directly.
- A new endpoint or consumer ships with tests.
- Git: feature branches, Conventional Commits (`feat:`, `fix:`, `refactor:` …).
- Code identifiers are **English**; comments may be English or Turkish but stay consistent per file.

## Naming conventions — backend (Java / Spring)

- **Package layers:** `.domain` (entities, value objects), `.application` / `.service` (use cases),
  `.web` (controllers), `.infra` (persistence, messaging, clients), `.config`.
- **Entities (JPA):** singular domain noun, **no suffix** — `Booking`, `Seat`, `Payment`.
- **Repositories:** `*Repository` — `BookingRepository`.
- **Services:** `*Service` — `BookingService`. Saga orchestrator: `*Saga` or `*Orchestrator`.
- **Controllers:** `*Controller` — `BookingController`.
- **DTOs:**
  - request payloads end with **`Request`** — `CreateBookingRequest`.
  - response payloads end with **`Response`** — `BookingResponse`.
  - other/internal DTOs end with **`Dto`** — `SeatDto`.
- **Mappers:** `*Mapper` — `BookingMapper` (MapStruct).
- **Kafka messages:** events end with **`Event`** (`PaymentCompletedEvent`), commands with
  **`Command`** (`PaymentRequestedCommand`).
- **Enums:** singular PascalCase — `BookingStatus { PENDING, CONFIRMED, CANCELLED, EXPIRED }`.
- **Exceptions:** `*Exception` — `SeatUnavailableException`.
- **Config classes:** `*Config` — `KafkaConfig`.
- **Methods:** camelCase, verb-first — `reserveSeats()`, `confirmBooking()`; booleans `is*/has*`
  (`isSeatAvailable()`). Avoid non-English names (no `denemeFonk()` → use `example()`/a real verb).
- **Constants:** `UPPER_SNAKE_CASE`.
- **DB:** `snake_case`, **plural tables** (`bookings`), FK `<entity>_id` (`event_id`).
- **REST paths:** versioned, plural nouns — `/api/v1/bookings`, `/api/v1/events/{eventId}/seats`.
- **Kafka topics:** `dot.case` — `payment.commands`.

## Naming conventions — frontend (Next.js / TypeScript)

- **Components:** PascalCase file + export — `SeatMap.tsx`, `EventCard.tsx`.
- **Hooks:** `use` + camelCase — `useSeatSelection.ts`, `useCountdown.ts`.
- **Non-component modules** (utils, api clients): camelCase file — `bookingApi.ts`, `formatPrice.ts`.
- **Types / interfaces:** PascalCase; mirror the API — `BookingResponse`, `CreateBookingRequest`;
  other shapes end with `Dto` to match the backend.
- **API client functions:** camelCase, verb-first — `fetchEvents()`, `createBooking()`, `holdSeats()`.
- **Routes:** App Router file conventions — `app/events/[eventId]/page.tsx`, `app/checkout/page.tsx`.
- **Booleans:** `is*/has*` — `isSeatHeld`.
- **Constants:** `UPPER_SNAKE_CASE`. **Env vars:** client-exposed ones are `NEXT_PUBLIC_*`.
- **Styling:** Tailwind utility-first; component-scoped CSS as `*.module.css` only when needed.

## How Claude Code should work here

- Respect service boundaries: no shared DB, no cross-service DB reads, no service-to-service REST.
- When adding a service, mirror the standard module structure and add its `CLAUDE.md`.
- Keep business logic out of the gateway — it only routes, validates JWTs, and applies Resilience4j.
- Before implementing a workflow that spans services, model it as Kafka events first.
- When you make a notable design decision, write a short ADR in `docs/adr/`.
- Prefer the smallest change that works; don't pull in new frameworks or libraries silently.

## Scope for the demo

Build the **vertical slice** end to end first: register/login → browse an event → hold seats →
pay (mock) → confirmed booking + notification, with the full saga and timeout path working.
Depth of one complete flow beats breadth of half-built services.
