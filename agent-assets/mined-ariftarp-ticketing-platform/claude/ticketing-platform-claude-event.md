# CLAUDE.md — event-service

> Loaded when working inside `services/event/`. See root `CLAUDE.md` for shared conventions and
> `docs/business-rules.md` (section "event (catalog)") for the authoritative domain rules.

## What this service owns

The **read-heavy catalog**: venues, events, price tiers, and the venue's **static seat map**.
Port `8082`, database `ticketing_event`, package root `com.demo.ticketing.event`.

| Entity         | Owns                                                              |
|----------------|-------------------------------------------------------------------|
| `Venue`        | name, address, city                                               |
| `Event`        | venue, title, description, `startsAt`, `status`                   |
| `SeatCategory` | a price tier for **one event**: name, price, and the venue section it prices |
| `Seat`         | a physical seat of a **venue** (section, row, number) — not of an event |

`Event.status` lifecycle: `DRAFT → ON_SALE → SOLD_OUT` or `DRAFT → ON_SALE → CLOSED`. Only an
`ON_SALE` event with `startsAt` in the future is bookable (surfaced as `bookable` on the detail
response so the UI doesn't re-derive it).

## The one rule that matters most (ADR-0001)

**event never knows whether a seat is available, held, or sold.** That state belongs to the
booking service (`seat_availability` + Redis holds). Concretely:

- No table in this service's schema may gain a sold/held/available column.
- `SeatDto` / `SeatMapResponse` must never gain an availability field —
  `SeatDtoContractTest` fails the build if they do.
- event never calls booking, and booking never reads this database. The seat-selection screen
  fetches layout here and availability from booking, and merges them **client-side by `seatId`**
  (`docs/business-rules.md` → "Seat map contract"). Do not add a server-side composed endpoint.

## Endpoint contract

| Endpoint | Returns |
|----------|---------|
| `GET /api/v1/events` | `EventSummaryResponse[]` — id, title, venueName, city, startsAt, status, `fromPrice` (lowest tier). **Only `ON_SALE` events.** Optional filters `?city=&q=&from=&to=`; `city` is exact/case-insensitive, `q` is a case-insensitive title contains, `from`/`to` are ISO-8601 instants bounding `startsAt`. |
| `GET /api/v1/events/{eventId}` | `EventResponse` — detail + venue + price tiers (highest price first) + `bookable`. Any status (a direct link to a `SOLD_OUT`/`CLOSED` event must still render). 404 problem+json if missing. |
| `GET /api/v1/events/{eventId}/seats` | `SeatMapResponse` — `{eventId, venueId, seats[]}` where each seat is `{seatId, section, row, number, seatCategory{id,name,price}}`. **Layout only, no availability.** 404 problem+json if missing. |
| `GET /api/v1/admin/events` | `EventSummaryResponse[]` — same shape and same optional `?city=&q=&from=&to=` filters as `GET /api/v1/events`, but **every status** (`DRAFT`/`ON_SALE`/`SOLD_OUT`/`CLOSED`), for the admin events table. Distinct path prefix on purpose: the gateway gates `/api/v1/admin/**` on `hasRole("ADMIN")` by path, so this service adds no local JWT/role check (see "Not here (deliberately)"). |
| `PUT /api/v1/events/{eventId}` | `EventResponse` — edits an existing event for the admin event-management screen. Gateway-gated `ADMIN`-only (`SecurityConfig.pathMatchers(HttpMethod.PUT, EVENTS_PATH)`), same as the `POST` endpoints below; this service does no local JWT/role check either (see "Not here (deliberately)"). 404 problem+json if missing. |
| `DELETE /api/v1/events/{eventId}` | `204 No Content` — deletes an event for the admin event-management screen. Same gateway-only `ADMIN` gate as `PUT` above. 404 problem+json if missing. |

No paging yet: the demo catalog is a handful of events, and a paging envelope is a response-contract
decision better made when the list actually needs it (roadmap Phase 11/14).

Errors are RFC 7807 `application/problem+json` via `web/GlobalExceptionHandler`.

## Modeling decision to know about

`business-rules.md` defines `SeatCategory` as `(id, eventId, name, price)` but does not say **how a
seat gets its tier for an event**. This service resolves it by **section**: `seat_categories` carries
a `section`, and every `Seat` in that venue section is sold at that tier for that event
(`UNIQUE (event_id, section)` + `UNIQUE (event_id, name)` enforce one tier per section per event).
Consequences:

- Seats in a section the event does not price are **omitted** from the seat map — an event may use
  only part of a venue (see the seeded `Retro Fest`, which prices section B only).
- If a tier ever needs to span several sections, promote `section` to a `seat_category_sections`
  child table instead of duplicating tier rows — and get `workflow-rules` to ratify the rule first.

## Implementation notes / traps

- Package layers: `.domain` (entities), `.application` (+ `.mapper`, `.exception`), `.web` (+ `.dto`),
  `.infra` (repositories), `.config`.
- `EventMapper` is hand-written, not MapStruct: the only real logic is the section→tier join, and it
  is worth reading and unit-testing directly (`EventMapperTest`, no Docker needed).
- DB column names: `seats.row_label` and `seats.seat_number` — `row` is a reserved word in SQL/HQL.
- Datasource authenticates as the least-privilege **`event_app`** role, never the `ticketing`
  superuser (Phase 2 review finding).
- The Maven parent is a plain aggregator, **not `spring-boot-starter-parent`**, so `-parameters` is
  not on by default (the root pom now sets `maven.compiler.parameters`). Name every
  `@RequestParam`/`@PathVariable` explicitly anyway — without it, requests fail at runtime with a 500
  "parameter name information not available".
- Optional filters in JPQL are bind-type minefields on Postgres: never wrap a nullable parameter in
  `lower()` (`function lower(bytea) does not exist`) and never test a nullable timestamp parameter
  with `:p is null` (`could not determine data type of parameter`). `EventService` pre-lowercases
  strings and substitutes open bounds for missing dates; see `EventRepository.findForBrowse`.
- `spring.jpa.hibernate.ddl-auto=validate` — Flyway owns the schema and startup fails on drift.

## Not here (deliberately)

- **No security/JWT.** The catalog reads are public. Admin endpoints (`POST /venues`, `POST
  /events`, `POST /events/{id}/seat-categories`, `PUT /events/{eventId}`,
  `DELETE /events/{eventId}`, `GET /admin/events`, roadmap Phase 14) rely entirely on the gateway's
  path-based `ADMIN` role gate — this service does no local JWT/role validation of its own.
- **No Kafka.** event neither produces nor consumes; it is not part of the checkout saga.
- **No OpenTelemetry/JSON logging yet** — cross-cutting stretch phase per `docs/roadmap.md`,
  consistent with the other services.
