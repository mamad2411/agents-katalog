# CLAUDE.md — gateway

> Loaded when working inside `gateway/`. See root `CLAUDE.md` for shared conventions.

Spring Cloud Gateway (WebFlux) on port **8080**. The only inbound door to the platform: the
frontend talks to `http://localhost:8080` and never to a service directly.

## What this module owns

1. **Routing** — path → owning service, nothing else.
2. **Edge JWT validation** — reject unauthenticated/invalid tokens before they cost a service a
   thread.
3. **Resilience4j** — circuit breaker + timeout on every sync route, retry on safe methods, plus a
   503 fallback.
4. **RFC 7807 error shape** for everything the gateway itself answers (401/403/503).

## What must never live here

No business logic, no persistence, no Kafka, no DTO/domain model, no cross-service composition.
The gateway routes each request to the **one** service that owns it; it is not a place to join two
services' data, and it never proxies service-to-service calls (those go over Kafka — root
`CLAUDE.md`, "Communication rules"). If a task needs the gateway to *decide* something about
bookings, seats or payments, that task belongs in a service.

## Route table

| Path                | Method(s) | Target                        | Auth     | Phase |
|---------------------|-----------|-------------------------------|----------|-------|
| `/api/v1/auth/**`   | any       | `${services.auth.uri}` (8081)  | **open** | 3/4   |
| `GET /api/v1/events/**` | GET   | `${services.event.uri}` (8082) | **open** | 5/7 |
| `POST /api/v1/events/**` | POST | `${services.event.uri}` (8082) | JWT + `ADMIN` role | 14 |
| `PUT /api/v1/events/{eventId}` | PUT | `${services.event.uri}` (8082) | JWT + `ADMIN` role | 14 |
| `DELETE /api/v1/events/{eventId}` | DELETE | `${services.event.uri}` (8082) | JWT + `ADMIN` role | 14 |
| `POST /api/v1/venues/**` | POST | `${services.event.uri}` (8082) | JWT + `ADMIN` role | 14 |
| `GET /api/v1/admin/**` | GET   | `${services.event.uri}` (8082) | JWT + `ADMIN` role | 14 |
| `/api/v1/bookings/**` | any     | `${services.booking.uri}` (8083) | JWT required | 7 |
| `/actuator/health`  | GET       | gateway itself                | open     | 4     |
| `/fallback/{service}` | any     | gateway itself (internal forward) | open | 4     |
| everything else     | any       | —                             | JWT required | — |

Not yet routed:

- **payment** (8084) and **notification** (8085) — **never**. They have no inbound REST; they are
  Kafka-only. Do not add a route for them.

`GET /api/v1/events/**` is public because event's catalog reads need no login
(`services/event/CLAUDE.md`: "No security/JWT. The catalog reads are public."). Phase 14 added
admin write endpoints under the same `/api/v1/events/**` prefix (`POST /events`,
`POST /events/{id}/seat-categories`, and later `PUT /events/{eventId}` /
`DELETE /events/{eventId}` for the admin edit/delete screen) plus a brand-new `POST /api/v1/venues`
— all routed to the same `${services.event.uri}` target (event owns venues too) and gated to the
`ADMIN` role in `SecurityConfig` (`.pathMatchers(HttpMethod.POST, ...).hasRole("ADMIN")`,
`.pathMatchers(HttpMethod.PUT, EVENTS_PATH).hasRole("ADMIN")`,
`.pathMatchers(HttpMethod.DELETE, EVENTS_PATH).hasRole("ADMIN")`, each declared *before* the
`GET`-only public rule so none of them is short-circuited — see the ordering comment in
`SecurityConfig`). The `roles` JWT claim is mapped to `ROLE_*` `GrantedAuthority`s by a
`JwtAuthenticationConverter` in `GatewayJwtConfig`. `services/event/CLAUDE.md` still says "No
security/JWT" for the service itself — these endpoints deliberately have **no** local JWT/role
validation at all and trust the gateway to reject non-ADMIN callers before the request ever
arrives (the same deferral precedent `booking` uses for its own JWT-avoidance elsewhere). That
makes the gateway's `ADMIN` check the only enforcement of "Only ADMIN may create/update venues and
events" (`docs/business-rules.md`) for these endpoints — do not weaken it.

Phase 14 also added `GET /api/v1/admin/events`, a separate prefix routed to the same
`${services.event.uri}` target, for the admin screen's table of events across **all** statuses
(the public `GET /api/v1/events` stays ON_SALE-only and unchanged). It is gated to the `ADMIN`
role the same way (`.pathMatchers(HttpMethod.GET, ADMIN_EVENTS_PATH).hasRole("ADMIN")`). Since
`/api/v1/admin/**` doesn't overlap any existing public-path prefix, its declaration order in
`authorizeExchange` is not load-bearing the way the `POST` rules' order is — it just needs to stay
before `.anyExchange().authenticated()`.

Paths are forwarded **verbatim** (no `StripPrefix`): services map their controllers at the full
`/api/v1/<resource>` path.

### Adding a route (Phases 5/7)

1. Add `services.<name>.uri` to `application.yml` (env-var indirection + localhost default).
2. Add the route with the same two filters, using a `CircuitBreaker` name of `<name>CircuitBreaker`
   and `fallbackUri: forward:/fallback/<name>`.
3. Add `resilience4j.circuitbreaker.instances.<name>CircuitBreaker.baseConfig: default` and the
   matching `resilience4j.timelimiter.instances.<name>CircuitBreaker` entry.
4. Nothing else — `FallbackController` is generic over `{service}` and the route is protected by
   default (deny-by-default in `SecurityConfig`).

## JWT validation contract

- **Algorithm: HS512**, symmetric, shared secret with the auth service — see
  `docs/adr/0002-hmac-shared-secret-jwt-validation.md` for why HMAC instead of RS256/JWKS.
- **Secret:** env var `TICKETING_JWT_SECRET` (same name and same demo default in
  `gateway/src/main/resources/application.yml` as in `services/auth/src/main/resources/application.yml`).
- Auth signs with jjwt's `signWith(key)`, which picks the algorithm from the key length; the
  64-character demo secret is 512 bits, hence HS512. **If the secret's length ever changes, update
  `security.jwt.mac-algorithm` too** — the decoder is pinned to exactly one algorithm on purpose, so
  a mismatch shows up as blanket 401s.
- **Claims:** `sub` (userId), `email`, `roles`, plus `iat`/`exp`. Validated: signature, `exp`, `nbf`
  (Spring's default 60s clock skew). No `iss`/`aud` — auth does not set them; add an issuer check
  here first if a second issuer ever appears.
- **Identity propagation:** the incoming `Authorization` header is forwarded downstream unchanged
  and **no** `X-User-*` headers are added. Downstream services validate the same token themselves
  (root `CLAUDE.md`) — a trusted header from the gateway would make them depend on the gateway for
  authorization, which is exactly what we do not want.
- Public paths are listed in `SecurityConfig.PUBLIC_PATHS`, plus one explicit
  `HttpMethod.GET`-scoped `permitAll()` for `/api/v1/events/**` (kept out of the plain string array
  on purpose — see below); everything else is `authenticated()`.
- Role-based rules (`hasRole("ADMIN")`) arrived with the admin routes in Phase 14: `POST` on
  `/api/v1/events/**` and `/api/v1/venues/**` requires the `ADMIN` role, and so do `PUT`/`DELETE`
  on `/api/v1/events/**` (added for the admin edit/delete-event screen). These `pathMatchers` calls
  are declared **before** the `GET`-only public rule and before `PUBLIC_PATHS`' `permitAll()` in
  `authorizeExchange` — Spring Security evaluates rules in declaration order and stops at the first
  match, so a path-based `permitAll()` on `/api/v1/events/**` would otherwise short-circuit before
  the role check ever runs (and any new HTTP method on `/api/v1/events/**` without its own explicit
  rule here silently falls through to `anyExchange().authenticated()` — any logged-in user, not
  just admins — so every new admin-only method on this prefix needs its own `pathMatchers` line).
  The 403 handler for `hasRole` failures is wired and tested (`ProblemDetailAccessDeniedHandler`).

## Resilience4j

Both templates live under `configs.default` in `application.yml`, and each route's instances
inherit them via `baseConfig: default`. **The Resilience4j instance name must equal the
`CircuitBreaker` filter's `name` arg** — that is how Spring Cloud CircuitBreaker looks the
configuration up.

| Config                                    | Meaning                                                                 |
|-------------------------------------------|-------------------------------------------------------------------------|
| `resilience4j.circuitbreaker.configs.default` | 20-call count window, opens at 50% failures (min 10 calls) or 50% slow calls (>2s), stays open 10s, then 3 half-open probes. |
| `resilience4j.timelimiter.configs.default`    | 3s budget for one client request, **retries included**.             |
| `instances.authCircuitBreaker`            | The auth route's breaker + time limiter.                                |
| `instances.bookingCircuitBreaker`         | The booking route's breaker + time limiter.                             |
| `instances.eventCircuitBreaker`           | The event route's breaker + time limiter.                               |
| `instances.venueCircuitBreaker`           | The venue route's breaker + time limiter (Phase 14).                    |
| `instances.adminEventCircuitBreaker`      | The admin-events route's breaker + time limiter (Phase 14).             |

Filter order inside a route is declaration order, and it is deliberate:

- **CircuitBreaker first (outer)** — one client request counts once in the breaker window, and the
  3s time limiter bounds the whole attempt rather than each retry.
- **Retry second (inner)**, `methods: GET` only. POSTs (`/auth/register`, `/auth/login`) are never
  retried: a 5xx may mean the write already happened, and Spring Cloud Gateway replays a request
  without re-buffering its body unless a `CacheRequestBody` filter is added — a retried POST could
  reach the service with an empty body. The breaker + fallback already cover "the service is down".

Breaker open, time limiter fired, or connection refused → internal forward to
`/fallback/{service}` → **503 `application/problem+json`**. The client never sees a Netty/connect
error.

## Error contract

Everything the gateway answers itself is `application/problem+json` with `status`, `title`,
`detail` and `instance` (the caller's original path):

| Situation                              | Status | Produced by                              |
|----------------------------------------|--------|------------------------------------------|
| No/invalid/expired/wrong-signature JWT | 401    | `ProblemDetailAuthenticationEntryPoint`  |
| Authenticated but not allowed          | 403    | `ProblemDetailAccessDeniedHandler`       |
| Downstream down/slow/breaker open      | 503    | `FallbackController`                     |

Spring Security's reactive handlers run before any `@RestControllerAdvice`, which is why these are
explicit handlers writing the body via `ProblemDetailResponseWriter` rather than an exception
handler. Downstream error bodies (e.g. auth's 401 for bad credentials) pass through untouched.

## Tests

`gateway/src/test/java/com/demo/ticketing/gateway/` — **no Docker, no Testcontainers**, and it must
stay that way: the "downstream service" is an `okhttp3.mockwebserver.MockWebServer` on a random port
wired in through `@DynamicPropertySource` overriding `services.auth.uri`.

- `AuthRouteSecurityTest` — auth route open, header forwarded unchanged, 401 problem+json for
  missing/garbage/expired/wrong-secret/wrong-algorithm tokens, valid token passes the edge.
- `AuthRouteResilienceTest` — slow downstream → 503 fallback; GET retried on 5xx; POST not retried.
- `BookingRouteTest` — booking route protected (401 without a token, downstream never hit), valid
  token forwards path/query/`Authorization` header verbatim, `POST /bookings/hold` not retried on
  5xx, `GET` retried — same pattern as the auth tests, against `services.booking.uri`.
- `EventRouteTest` — event route public for `GET` (no token needed to reach it), path/query
  forwarded verbatim, `Authorization` header forwarded unchanged when present with no invented
  identity headers, `GET` retried on 5xx — plus (Phase 14) `POST /events`,
  `POST /events/{id}/seat-categories`, `PUT /events/{eventId}` and `DELETE /events/{eventId}`: 401
  with no token, 403 with a `USER`-role token, forwarded verbatim with an `ADMIN`-role token —
  against `services.event.uri`.
- `VenueRouteTest` (Phase 14) — same three-case pattern (401/403/forwarded) for
  `POST /api/v1/venues` against `services.event.uri` (venues and events share the event service).
- `AdminEventRouteTest` (Phase 14) — same three-case pattern (401/403/forwarded verbatim
  including query params) for `GET /api/v1/admin/events` against `services.event.uri`.
- `DownstreamUnavailableTest` — unreachable service → 503 fallback, breaker opens.
- `ProblemDetailHandlersTest` — the 401/403 bodies themselves.
- `TestJwt` mints tokens with the same secret/claims auth issues, so tests never need auth running;
  `validAdmin()` mints one with `roles: ["ADMIN"]` for the Phase 14 role-gated routes.

Keep resilience tests deterministic: override the timeouts/window sizes per test class with
`@SpringBootTest(properties = ...)`, never `Thread.sleep`.
