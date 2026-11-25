---
name: api-design-review
description: Runs a structured, evidence-based review of API contract design and cross-endpoint consistency across REST, GraphQL, and gRPC surfaces — resource/endpoint naming and HTTP verb correctness, status-code correctness, request/response shape and envelope consistency, error-response format, pagination and filtering conventions, idempotency, versioning strategy, backward compatibility, and documentation/spec-vs-code drift (OpenAPI/Swagger, GraphQL SDL, .proto), plus GraphQL-specific checks (N+1-shaped resolver design, @deprecated usage, query depth/complexity limiting) and gRPC-specific checks (proto field-number stability, proto3 optional/wrappers, service/method naming). This is a design/contract-consistency review, not an authentication/access-control security review (use cybersecurity-check for that) and not a latency/throughput performance review (use performance-audit for that). Use this whenever the user asks for an "API design review", "API review", "API-Design prüfen", "API-Design-Review", "REST API check", "REST-API prüfen", "REST-Konventionen prüfen", "API-Konsistenzprüfung", "API consistency check", "API contract review", "API-Vertragsprüfung", "OpenAPI review", "Swagger review", "OpenAPI-Spec prüfen", "GraphQL schema review", "GraphQL-Schema prüfen", "gRPC review", "proto review", ".proto prüfen", "API style guide check", "endpoint naming review", "Endpunkt-Namenskonvention prüfen", "sind unsere Endpunkte konsistent", "HTTP-Methoden korrekt verwendet", "REST best practices check", "Statuscode-Konsistenz prüfen", "status code check", "Fehlerformat prüfen", "error response consistency", "Pagination-Konventionen prüfen", "pagination consistency check", "Idempotenz prüfen", "idempotency check", "idempotency key check", "API-Versionierung prüfen", "API versioning review", "breaking change check", "Breaking-Change-Check", "backward compatibility check", "Abwärtskompatibilität prüfen", "Schema-Drift prüfen", "spec vs. code drift", "N+1 im GraphQL-Schema", "DataLoader check", "query depth limiting", "query complexity limiting", "proto field number stability", "Feldnummern-Stabilität", "proto3 optional check", or asks about any specific item this covers (plural vs. singular resource names, kebab vs. camel vs. snake case in URLs, GET used for a state-changing action, cursor vs. offset pagination, envelope consistency, ISO 8601 date format consistency, null vs. omitted fields, deprecation process for old API versions) — even if they only name one or two of these and not "API design review" explicitly.
---

# API Design Review

A structured, evidence-based review of an API's **contract design and cross-endpoint
consistency** — REST, GraphQL, gRPC, or a mix of these — for backend developers and architects
designing or reviewing a public or internal API surface. It investigates actual route/resolver/proto
definitions and any spec files, and reports one table the user can act on.

**Scope boundary — read this before starting.** This skill checks whether an API's *contract* is
well-designed and internally consistent: naming, HTTP semantics, status codes, error shapes,
pagination, idempotency, versioning, compatibility, and spec accuracy. It explicitly does **not**
cover:
- **Authentication/authorization/injection/access control** — that's `cybersecurity-check` (its
  S1, S11, S12, S19 items in particular). If an endpoint's auth looks off during this review, note
  it in one line and point to that skill rather than assessing it here.
- **Latency, throughput, N+1 query performance impact, caching strategy** — that's
  `performance-audit`. This skill flags the *design pattern* that predicts an N+1 problem (e.g. a
  GraphQL resolver with no batching) as a design smell, but does not measure or size its actual
  performance impact — that's the other skill's job.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer: an actual route/handler
  file and line, an actual resolver or `.proto` definition, an actual example request/response
  captured from code or the spec, an actual git log entry. Never write "the API looks RESTful,"
  "naming seems consistent," or "error handling looks fine" as a standalone claim — quote the
  endpoints/fields you compared and what you found.
- **This is a design/contract-consistency review, not a security or performance review.** Say the
  scope boundary above once, up front, in the report, and honor it per-row — don't let an auth or
  latency observation quietly turn into a ❌ in this table; note it as an aside pointing to the
  sibling skill instead.
- **Don't invent scope you can't check, and don't silently drop scope either.** If the project has
  no public API at all, is GraphQL-only (so REST-specific checks don't apply), or has no `.proto`
  files, mark the relevant rows `➖ N/A` with a one-line reason ("no public API in this project,"
  "GraphQL-only — REST verb/status-code checks don't apply," "no gRPC services found"). Every
  check in the applicable section(s) gets a row; none are quietly skipped just because the project
  only uses one of the three styles.
- **Be genuinely thorough.** Consistency findings are only convincing when you've actually compared
  endpoints against each other — don't sample two endpoints and extrapolate to "the whole API is
  consistent." Walk the full route/resolver/proto list before concluding a check passes.

## Workflow

1. **Identify the API style(s) in use.** REST, GraphQL, gRPC, or a mix (e.g. a public REST API plus
   an internal gRPC service-to-service layer). This determines which sections below apply — mark
   the inapplicable ones `➖ N/A` up front rather than skipping them silently.
2. **Locate the actual contract definitions**, not just documentation:
   - REST: route/controller files, an OpenAPI/Swagger spec (`openapi.yaml`/`.json`, `swagger.json`,
     annotations in code that generate one).
   - GraphQL: the SDL schema file(s) (`schema.graphql`, `.gql`) or code-first schema definition,
     and the resolver implementations.
   - gRPC: `.proto` files and their generated/handwritten service implementations.
   Note whether a spec file exists at all for each style found — its absence is itself a finding
   under Documentation accuracy below, not a reason to skip that section.
3. **Work through the checklist(s)** below that match the style(s) found — universal checks apply
   regardless of style; REST/GraphQL/gRPC-specific checks are labeled as such and get `➖ N/A` rows
   for styles not present.
4. **Report as one table**, ❌ findings first within each area, followed by the prioritized punch
   list and needs-review list.

## Resource & endpoint naming (REST)

**API1 — Resource naming and casing consistency.** Collections should use plural nouns
(`/users`, not `/user`), and casing should be consistent across every endpoint — pick one of
kebab-case (`/order-items`), camelCase (`/orderItems`), or snake_case (`/order_items`) and check
every route uses it, not a mix. List every distinct casing/pluralization style actually found
across the route list; more than one style in the same API is the finding, not any one style being
"wrong." Also check nesting depth is applied consistently for structurally similar relationships
(if `/users/{id}/orders` is nested one level, a sibling relationship shouldn't jump to
`/orders/{orderId}/items/{itemId}/details` levels of nesting without an established reason).

**API2 — HTTP verbs mapped correctly to operations.** For every endpoint, confirm the verb matches
what it actually does:
- `GET` must be read-only and safe/idempotent — no endpoint that creates, mutates, or deletes state
  should use `GET` (a common violation: `GET /users/{id}/send-reset-email` or
  `GET /orders/{id}/cancel`).
- `POST` for creation or non-idempotent actions; flag any `POST` endpoint that's actually a pure
  read (some APIs misuse `POST` to pass a large query body — that's legitimate for search-with-body
  endpoints, but say so explicitly rather than flagging it blind).
- `PUT` should mean full resource replacement (client sends the complete representation); `PATCH`
  should mean partial update. Flag a `PUT` that only updates a subset of fields without documenting
  that as the actual contract, and a `PATCH` that's actually implemented as a full replace under a
  different name.
- `DELETE` for removal. Flag any state-changing action hidden behind a `GET` or a same-verb
  endpoint that behaves differently depending on a body flag.

## Status code correctness (REST)

**API3 — Status codes used correctly and consistently.** Check across all endpoints (not just one)
that:
- Success paths return an appropriate 2xx (`200` for a read/update with a body, `201` for
  creation with the created resource, `202` for accepted-but-async, `204` for a no-content success
  like a bare `DELETE`) rather than every endpoint returning a blanket `200` regardless of outcome.
- The API does not bury errors in a `200` response body (e.g. `{"status": "error", "message": ...}`
  with an HTTP `200`) — this forces every client to parse the body just to know if the call
  succeeded, defeating HTTP semantics and any middleware/monitoring that keys off status codes.
- `400` (malformed/unparseable request), `404` (resource doesn't exist), `422` (well-formed request
  that fails business/validation rules), and `409` (conflict — e.g. a duplicate unique key, a
  version/optimistic-concurrency mismatch) are used distinctly and consistently for their
  respective cases across endpoints, not interchangeably (e.g. one endpoint returning `400` for a
  validation failure while another returns `422` for the same category of problem).

## Request/response shape consistency

**API4 — Envelope consistency.** Check whether responses are wrapped in a consistent envelope
(e.g. `{"data": ..., "meta": ...}`) across *every* endpoint, or consistently unwrapped (the
resource returned directly as the response body) across every endpoint. Either choice is fine; the
finding is when some endpoints return a bare object/array and others wrap the same kind of payload
in an envelope — that inconsistency is what breaks a generic client-side response parser.

**API5 — Field naming, casing, and date/time format consistency.** Compare field names across
different endpoints/resources for the same or similar-meaning fields (`createdAt` vs. `created_at`
vs. `created_date` used in different endpoints; `userId` vs. `user_id` vs. `uid`). Separately check
every date/time field uses one consistent format — ISO 8601 (`2026-08-31T14:00:00Z`) is the
common target — rather than a mix of ISO 8601, Unix timestamps, and locale-formatted strings across
different endpoints.

**API6 — Null vs. omitted-field handling.** Check whether the API has a consistent rule for
representing "no value": always include the field with `null`, or always omit it entirely, applied
the same way across endpoints. A field that's `null` in one endpoint's response and simply absent
for the equivalent case in another endpoint is a real client-side parsing hazard (a client
distinguishing "field missing" from "field explicitly null" will behave differently depending on
which endpoint it's calling for no principled reason).

## Error response format

**API7 — A single consistent error shape across all endpoints.** Locate error responses from
several different endpoints/error paths (validation failure, not-found, server error, auth
failure — note that only the *shape* is in scope here, not the auth logic itself) and compare their
JSON structure. A well-designed API returns one consistent shape everywhere — typically a machine-
readable error code, a human-readable message, and optionally a list of field-level validation
details — so a client can write one error-handling path instead of one per endpoint. Flag: ad hoc
per-endpoint error shapes (one returns `{"error": "..."}`, another returns
`{"message": "...", "code": ...}`, another returns a raw stack trace or framework default error
page), and any endpoint that omits a stable machine-readable error code, forcing clients to match
on the human-readable message string.

## Pagination & filtering conventions

**API8 — Consistent pagination style across list endpoints.** Check whether every list/collection
endpoint uses the same pagination approach — cursor-based (`?cursor=...`) or offset-based
(`?page=`/`?offset=`&`?limit=`) — consistently. Consistency matters more than which style is
chosen; flag it when some list endpoints use one style and others use the other with no documented
reason (e.g. cursor-based only for a specific high-write-volume collection where offset pagination
would produce skipped/duplicated results — that's a legitimate, callable-out exception, not an
inconsistency).

**API9 — Consistent filter/sort query-parameter naming.** Compare filter and sort parameter names
across list endpoints (`?sort=`, `?sortBy=`, `?order_by=` used interchangeably for the same concept
in different endpoints; `?filter[status]=` vs. `?status=` vs. `?status_eq=` for equivalent
filtering). Flag inconsistent naming for functionally equivalent query parameters.

**API10 — Enforced maximum page size.** Check that list endpoints reject or cap an excessively
large `limit`/`page_size` request rather than allowing an unbounded page size that returns the
entire collection in one response — this is a design/contract concern (an undocumented or
unenforced cap is a contract gap a client can't safely rely on), not a performance-sizing exercise.

## Idempotency

**API11 — Naturally-idempotent operations are actually implemented idempotently.** `PUT` and
`DELETE` are expected by HTTP semantics to be idempotent (calling twice has the same effect as
calling once). Verify this in the handler code: does a repeated `PUT` with the same body produce
the same end state (rather than, say, appending to a list field each call)? Does a repeated
`DELETE` of an already-deleted resource return a clean idempotent result (`204`/`404` treated as
success-equivalent by the client contract) rather than erroring differently on the second call in a
way that breaks retry logic?

**API12 — Idempotency-key mechanism for retryable creation.** For `POST` endpoints that create a
resource with real-world consequences if duplicated (payment, order, charge creation) and that a
client might retry after a timeout/network failure, check for an idempotency-key mechanism
(client-supplied key, e.g. an `Idempotency-Key` header, that the server uses to detect and
deduplicate a retried request rather than creating the resource twice). No such endpoints in this
API → `➖ N/A`, state what you checked.

## Versioning strategy

**API13 — Explicit, consistently-applied versioning approach with a deprecation process.** Check
whether the API has a defined versioning strategy — URL path (`/v1/...`), a custom header, or
content-negotiation (`Accept: application/vnd.api+json;version=2`) — and that it's applied the same
way across every endpoint rather than some endpoints being versioned and others not. Separately
check for a documented deprecation process (a `Deprecation`/`Sunset` header, a changelog, a
migration guide) for retiring old versions or fields, rather than versions/fields disappearing
without notice. No versioning scheme at all is a real, reportable finding for any API with external
consumers — don't treat "no version in the URL" as automatically fine without checking whether
there's some other mechanism in its place.

## Backward compatibility

**API14 — Additive vs. breaking changes to already-consumed endpoints.** For endpoints likely to
have existing consumers (anything not brand-new in this change), check recent git history on the
route/resolver/proto file: `git log -p --follow <file>` for the last several changes. A field
rename, type change, removed field, or removed endpoint without a corresponding version bump is a
breaking change shipped silently — flag it specifically, citing the commit. Adding a new optional
field, or a new endpoint, is compatible and not a finding. If git history shows no evidence either
way (too new, or history unavailable), say so rather than asserting compatibility you didn't check.

## Documentation accuracy

**API15 — Spec-to-code drift.** If an OpenAPI/Swagger spec, GraphQL SDL schema, or `.proto` file
exists, spot-check a representative sample of it against the actual route/resolver/service
implementation: a field documented in the spec that no longer exists in code, a field returned by
code that's absent from the spec, a documented required field that the handler treats as optional
or vice versa, an endpoint/method present in one but not the other. Call out explicitly that a
stale spec is often worse than no spec, since it actively misleads integrators who trust it over
reading the code. No spec file exists at all for a style in use → that absence is itself the
finding (recommend one), not an automatic `➖ N/A`.

## GraphQL-specific

**API16 — N+1-shaped resolver design (design smell, not a performance measurement).** For resolvers
that fetch a related/nested field per parent item (e.g. a `posts` field resolving each post's
`author` individually), check whether a batching mechanism (DataLoader or equivalent) is used.
Flag the *absence* of the pattern as a design-level finding — "this resolver has no batching layer,
so it will issue one query per parent item" — without measuring or sizing the actual runtime
impact; a full performance analysis of query cost belongs to `performance-audit`.

**API17 — Field/type deprecation via `@deprecated`.** Check that fields or types being phased out
use the schema's `@deprecated(reason: "...")` directive (with a reason pointing consumers to the
replacement) rather than being silently removed or left undocumented as obsolete. A removed field
with no deprecation history in the schema/changelog is a breaking-change finding (overlaps with
API14 — cite both).

**API18 — Query complexity/depth limiting.** Check for middleware or schema-level configuration
that limits query depth or computed complexity/cost (e.g. `graphql-depth-limit`, a cost-analysis
plugin, a max-depth validation rule) so a single client query can't request unboundedly nested data
in one call. No such limiting configured at all is a reportable design gap, not an automatic
`➖ N/A` — GraphQL's flexible querying is exactly what makes this a design-level control, distinct
from rate limiting (a security/abuse-prevention concern owned by `cybersecurity-check`).

## gRPC-specific

**API19 — Proto field-number stability.** Check `.proto` files (and their git history for evidence
of past field removals) for reused field numbers: a removed field's number must never be assigned
to a new field, since old binary-encoded messages/clients still reference that number on the wire
and reusing it silently corrupts data for anyone not yet upgraded. Confirm removed fields are
marked `reserved <number>` (and ideally `reserved "<old_name>"`) rather than the number simply being
free for reuse.

**API20 — proto3 optional/wrappers used where unset-vs-default matters.** For fields where
distinguishing "not set by the client" from "explicitly set to the zero value" is semantically
meaningful (e.g. a boolean flag, a numeric field where `0` is a valid value distinct from "not
provided"), check the field uses `optional` (proto3 presence tracking) or a wrapper type
(`google.protobuf.BoolValue`, `Int32Value`, etc.) rather than a bare scalar, which cannot represent
that distinction at all on the wire.

**API21 — Consistent service/method naming.** Check that service and RPC method names follow one
consistent convention across all `.proto` files (e.g. `VerbNoun` method names like `GetUser`,
`ListOrders`, `CreateInvoice` — not a mix of `UserGet`, `FetchOrders`, and `invoice_create` in
different services), matching the naming style already established elsewhere in the same API
surface.

## Output format

Start with 2-4 sentences: which API style(s) were found (REST/GraphQL/gRPC/mix), which spec/schema
files and route/resolver/proto sources were actually inspected, anything that couldn't be checked
(no git history available for a compatibility check, no spec file to compare against), and the
scope-boundary caveat — this is a contract-design review, not a security or performance review.

Then ALWAYS use this exact table — one row per check, per API style where a check applies to more
than one style present, none omitted:

| # | Check | Bereich/Area | Status | Befund/Evidence | Empfehlung/Recommendation |
|---|---|---|---|---|---|
| 1 | ... | Naming/Status Codes/Shape/Errors/Pagination/Idempotency/Versioning/Compatibility/Docs/GraphQL/gRPC | ✅/❌/⚠️/➖ | file:line, endpoint/field names compared, or command output | only if not ✅ |

(Match the table's actual language to the conversation's language — column names above are
illustrative. Keep "Befund"/"Evidence" concrete: the actual endpoints/fields you compared, a
file:line, a git log excerpt, or "not found — searched X, Y, Z.")

Status legend:
- ✅ Pass — checked across the relevant endpoints/fields and found consistent/correct
- ❌ Fail — checked, and a concrete inconsistency or contract problem was found
- ⚠️ Needs manual/human review — a judgment call code alone can't resolve (e.g. whether a
  cursor-vs-offset split is an intentional documented exception, whether a breaking-looking change
  was actually communicated to consumers out-of-band)
- ➖ N/A — this check's API style isn't present in the project (e.g. no GraphQL schema, no `.proto`
  files, no public API at all) — state why in one clause

End with a **prioritized punch list**: every ❌, ordered by how disruptive the inconsistency is to
API consumers (breaking-change and error-shape/status-code problems generally first, cosmetic
naming drift last), each with the one-line fix. Follow it with a **needs-review list**: every ⚠️,
since those need a human decision rather than a code change.
