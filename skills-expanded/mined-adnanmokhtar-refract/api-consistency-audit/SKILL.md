---
name: api-consistency-audit
description: API surface consistency audit — 22 drift fingerprints across endpoints, covering response envelope shape, error contract, pagination, resource-path and field naming, idempotency keys, auth/rate-limit/security headers, conditional requests (ETag/If-Match), batch contract, log and metric naming, timeout-retry policy, and OpenAPI coverage. Used by /polish on backend-* stacks; 16 fingerprints emit a closure verb from a closed 15-verb vocabulary, 6 emit a routed observation with no verb. Every finding carries <path:line> evidence. Behaviour-preserving — envelope unification and naming changes ship through the deprecation flow, never a blind rewrite. NOT for adding endpoints (/add-endpoint), fixing functional bugs (/fix-bug), or non-backend stacks (halts).
kind: skill
pack: backend
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: api-consistency-audit

## Premise

**Resolve `$ROOTS` first, and print it in the report.** Set it as an array — `ROOTS=(apps/api/src apps/web/src)` — and every probe expands it as `"${ROOTS[@]}"`: a space-joined string does not word-split in zsh (the macOS default shell), so `rg` searches one path that does not exist, prints an IO error to stderr and exits 2 — which reads as zero hits. Every probe below reads `$ROOTS` — set it once to this project's real code roots. A probe over a directory that does not exist returns zero hits, and zero hits reads as CLEAN, which is a false negative rather than a pass. Record any root with no equivalent here as `n-a (<reason>)` on the scope line before the first finding.

Detect drift across the project's API surface so /polish can unify it. The skill operates on the deployed contract (OpenAPI spec, route table, controller signatures, response builders) and the project's conventions (`_extracted-idioms.md § API conventions` or `ai/api-conventions.md`).

**Every finding cites `<method path>` + `<file:line>` + the canonical convention it diverges from + a closure verb.** A drift claim without the cited endpoint and the canonical it violates is not a finding — it is a vibe. The canonical always comes from the project's declared conventions, never invented (see Halt conditions). This skill is the API-half of /polish (the frontend half is the design-token / a11y / motion suite).

## Adapt to the codebase

Drift is measured against the project's OWN primitive — detect and mirror it before clustering, so a fix routes through the mechanism the codebase already uses (never a second one):

| Framework | Response envelope / error contract | Rate-limit binding | ETag / conditional | Pagination |
|---|---|---|---|---|
| **NestJS** | interceptor + `HttpException` filter | `@Throttle` / `ThrottlerGuard` | interceptor / `res.setHeader` | `nestjs-paginate` / repo keyset |
| **Django/DRF** | renderer + `exception_handler` | DRF throttle classes | conditional views / `ETag` mixin | `CursorPagination` |
| **FastAPI** | response model + exception handler | `slowapi` / middleware | manual `ETag` / `If-None-Match` | keyset / `fastapi-pagination` |
| **Spring** | `@ControllerAdvice` + `ProblemDetail` | bucket4j / gateway filter | `ResponseEntity` ETag / `ShallowEtagHeaderFilter` | `Pageable` / `ScrollPosition` |
| **Express** | response helper + error middleware | `express-rate-limit` | manual ETag | keyset helper |
| **Rails** | `render` + `rescue_from` | `rack-attack` | `fresh_when` / `stale?` | `pagy` |
| **Laravel** | Resource + Handler | `throttle` middleware | `setEtag` / `SetCacheHeaders` | `cursorPaginate` |

Where the project ships `_extracted-idioms.md § API conventions`, that file is the oracle for which shape is canonical; the framework table only tells the detector WHERE to look.

## When to run

- Dispatched by `/polish` on `backend-*` stacks.
- No command wrapper ships for this skill; invoke via `/polish --diagnose-only --stack=backend` (writes the artifact, no fixes) or run the skill directly.
- NOT for adding new endpoints (use `/add-endpoint`) or fixing functional bugs (use `/fix-bug`).

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Codebase root | Orchestrator | YES |
| `PROJECT_KIND` (must be `backend-*`) | `_extracted-codebase.md § Gold standards` | YES |
| API conventions | `_extracted-idioms.md § API conventions` OR `ai/api-conventions.md` | YES (without it, the canonical envelope/naming/etc. is unknown — halt) |
| OpenAPI spec | `<openapi.json>` / `<swagger.yaml>` (auto-detected) | NO (skip openapi-coverage detector if missing; warn) |
| Endpoint registry | Auto-detected from controllers / route table | YES |
| Scope filter (optional) | Caller flag | NO (default: all endpoints) |

## Outputs (precise contract)

A finding-draft array — one row per detected drift fingerprint. Each row:

```yaml
class: api-consistency
subclass: <one of: response-envelope-drift | error-contract-drift |
                   naming-convention-drift | pagination-drift | versioning-drift |
                   auth-header-drift | idempotency-key-missing |
                   rate-limit-header-drift | rate-limit-enforcement-missing |
                   etag-conditional-drift | optimistic-concurrency-missing |
                   batch-endpoint-contract-drift | field-selection-drift |
                   resource-naming-drift |
                   security-header-drift | log-field-drift |
                   metric-name-drift | trace-span-drift |
                   timeout-policy-drift | retry-policy-drift |
                   openapi-coverage-gap | example-coverage-gap>
endpoint: <method + path, e.g., "POST /orders">
file: <controller-or-handler-path:line>
canonical: <what the project's convention says — the envelope shape / naming / etc.>
divergence: <what this endpoint does differently>
closure_verb: <one of the 15 verbs below — OMIT THIS KEY ENTIRELY on a routed observation>
routed_to: <present INSTEAD of closure_verb on the 6 routed observations: the command,
            pattern, or pack that owns the fix>
risk: low | medium | high
```

**The closure-verb vocabulary is closed at 15, and `/polish`'s validator enforces it.** `scripts/validate-polish-artifacts.sh` reads every `closure_verb:` line in `ai/polish/ledger.md` and `ai/polish/_api-decisions.md` and rejects the whole artifact if any value falls outside `API_CONSISTENCY_VERBS`. A detector that wants a sixteenth verb does not get one; it either reuses an existing verb (because the *act* is the same) or it emits `routed_to:` and no verb at all. Inventing a verb does not produce a richer finding — it produces a rejected run.

| Vocabulary (15) |
|---|
| `unify-envelope` · `unify-error-contract` · `unify-naming` · `unify-pagination` · `unify-versioning` · `unify-auth-header` · `add-idempotency-key` · `unify-rate-limit-headers` · `unify-log-fields` · `unify-metric-names` · `unify-trace-spans` · `unify-timeout-policy` · `unify-retry-policy` · `add-openapi-doc` · `add-endpoint-example` |

## The 22 fingerprints — 16 closure-verb detectors + 6 routed observations

The split is not bookkeeping, it is the scope line. This skill audits **consistency**: it finds a surface where sibling endpoints disagree and it names the canonical they should converge on. Six of the fingerprints below are not that. Wiring a limiter, adding ETag revalidation, introducing an `If-Match` precondition, and returning per-item batch statuses are *additive capability* — the endpoint is missing a thing, not diverging from a thing. Field-selection and security-header uniformity are owned end-to-end by another pattern or pack, so their correctness criterion lives somewhere this skill cannot read. Those six still earn their place, because a consistency sweep is exactly when you notice them; but they route to the owner instead of closing here, and they emit **no** `closure_verb:` line. (They previously emitted six invented verbs that `validate-polish-artifacts.sh` rejects outright — a whole `/polish` run discarded because a detector wanted vocabulary it does not own.)

### 1. response-envelope-drift

**Fingerprint**: endpoints return different top-level shapes for the same conceptual response.

Common shapes the project might pick as canonical (one of):
- `{ data, meta, errors }` (JSON:API-ish)
- `{ data, pagination }` (Atlassian-ish)
- bare resource (no envelope at all — also valid IF consistent)

Drift: mixing them. Example: `GET /orders` returns `{ data: [...], meta: {...} }` but `GET /customers` returns `[...]` directly.

**Detection**: parse OpenAPI response schemas OR static-analyse controller return types. Cluster by shape. Anything not in the dominant cluster is drift.

**Closure verb**: `unify-envelope` — wrap responses in the canonical shape. Ships through additive flow first (add wrapped variant alongside; deprecate bare; remove in next major).

### 2. error-contract-drift

**Fingerprint**: 4xx/5xx responses have different shapes across endpoints.

Common canonical shapes:
- RFC 9457 (obsoletes RFC 7807, 2023) Problem Details — `{ type, title, status, detail, instance, errors? }` served as `application/problem+json`. The `type` is a stable, dereferenceable URI per error class (e.g. `https://errors.acme.com/insufficient-funds`), NOT the human-readable `title`.
- `{ error, code, message, details? }`
- `{ message, code }`

Drift: some endpoints return `{ error: "msg" }`, others `{ message: "msg" }`, others throw raw stack traces in the body.

**Detection**: cluster 4xx/5xx body schemas by shape. When the canonical is Problem Details, the fingerprint is BOTH the body keys AND the `Content-Type` — an endpoint that returns the right keys but `application/json` (not `application/problem+json`), or uses `type` as a free-text title rather than a stable URI, is drift. Flag any error path emitting a raw stack trace / framework default body.

**Closure verb**: `unify-error-contract`.

### 3. naming-convention-drift

**Fingerprint**: response/request field names mix `camelCase` and `snake_case` across endpoints (or `PascalCase` etc.).

**Detection**: extract every field name from request/response schemas; classify case style. If the mix isn't 100% one style, drift.

**Closure verb**: `unify-naming` — picks the project's canonical case (from `_extracted-idioms.md`) and renames others. Ships with serializer mapping for breaking-change protection.

### 3b. resource-naming-drift

**Fingerprint**: the *path* — not the field names of #3 — is inconsistent across the surface. A collection that is singular where its siblings are plural (`/order` beside `/customers`), a segment in a different case style (`/shippingAddresses` beside `/shipping-addresses`), or an action encoded as a path segment (`POST /orders/42/cancelOrder`) where siblings use the method or a `:verb` custom method.

**Detection**: extract every path from the route registry. Split on `/`; classify each non-parameter segment by (a) number (singular/plural) and (b) case style. Cluster; anything outside the dominant cluster is drift. Separately, grep segments against a verb list (`get`, `create`, `update`, `delete`, `cancel`, `send`, `fetch`, `do`) — a verb in a path segment that is not preceded by `:` is drift regardless of the cluster. Emits e.g. `POST /order/{id}/cancelOrder` at `src/orders/orders.controller.ts:88` — singular collection **and** verb-in-path, while `POST /customers/{id}:deactivate` at `src/customers/customer.controller.ts:52` is plural + custom-method form.

**Detection (pointer)**: the naming contract itself (plural nouns, kebab-case segments, verb-free paths, the sanctioned `POST /v1/{resource}:verb` escape hatch) is OWNED by `ai/patterns/api-contract.md` § Resource naming and URL structure — point there, do not restate the rules. This detector asserts only that the surface disagrees with itself and with the declared canonical.

**Detection (runnable)**: five of the checks are mechanical; run them, don't eyeball the route table. `routes.txt` is one `METHOD /path  file:line` per line, produced by step 2 of the Procedure (or by the framework's own route-list command, wired in `references/<framework>.md`).

```bash
# 0. paths only; route params normalised to {id}; /api and /vN prefixes stripped so depth is honest.
#    Normalise ONLY `/:param` (colon-style route params) — a bare `:` rule eats the `{id}:verb`
#    custom-method form and turns every legitimate custom method into a phantom finding.
awk '{print $2}' routes.txt \
  | sed -E 's/\{[^}]*\}/{id}/g; s#/:[A-Za-z_][A-Za-z0-9_]*#/{id}#g; s#^/(api/)?(v[0-9]+/)?#/#' \
  | sort -u > paths.txt

# 1. verb encoded in a path segment. The verb must be the whole segment (`/delete`) or be followed
#    by a separator or capital (`/cancel-order`, `/cancelOrder`) — a bare prefix match flags
#    `/addresses` as the verb "add", `/settings` as "set", `/updates` as "update". The `:verb`
#    custom-method form is exempt by construction: its verb follows a colon, never a slash.
grep -nE '/(get|list|create|new|add|update|edit|set|delete|remove|destroy|cancel|send|fetch|do|run|process|handle|perform)((-|_|[A-Z])[A-Za-z0-9_-]*)?(/|$)' paths.txt

# 2a. segments that fail Zalando #129's published regex  ^[a-z][a-z\-0-9]*$
grep -oE '(^|/)[A-Za-z][A-Za-z0-9_-]*' paths.txt | tr -d '/' | sort -u | grep -vE '^[a-z][a-z0-9-]*$'

# 2b. which style actually dominates. Run this FIRST — a surface that is uniformly snake or camel
#     has a canonical that is not kebab, and 2a's output is then the wrong list to act on.
grep -oE '(^|/)[A-Za-z][A-Za-z0-9_-]*' paths.txt | tr -d '/' | sort -u \
  | awk '/_/{s++;next} /[A-Z]/{c++;next} /-/{k++;next} {p++} END{print "kebab:",k+0,"single-word:",p+0,"snake:",s+0,"camel/Pascal:",c+0}'

# 3. nesting deeper than 3 sub-resource levels (Zalando #147). The first named segment is the
#    top-level collection, so 4 named segments == 3 levels of nesting; flag 5 or more.
awk -F/ '{n=0; for(i=1;i<=NF;i++) if($i!="" && $i!="{id}") n++; if(n>4) print n" levels: "$0}' paths.txt

# 4. a collection segment repeating inside one path (AIP-122 uniqueness) — always a real bug
awk -F/ '{delete seen; for(i=1;i<=NF;i++) if($i!="" && $i!="{id}"){ if($i in seen){print "repeat: "$0; break} seen[$i]=1 }}' paths.txt

# 5. empty or trailing path segments (Zalando #136) — usually a route-builder concatenation bug
grep -nE '//|.+/$' paths.txt
```

Each hit is still a *candidate*, not a finding: re-attach `METHOD` + `file:line` from `routes.txt` and name the sibling endpoint it contradicts before it is emittable.

**What grep cannot decide** — state these limits in the finding rather than pretending the script settled them:

- **Singular vs plural.** There is no check above for it, deliberately. No regex knows that `/media`, `/series`, `/info`, `/analytics`, `/staff` are correctly not-`s`-suffixed while `/order` beside `/customers` is drift — that is AIP-122's "moose" case (`ai/patterns/api-contract.md` § The plural rule has a real exception). Trailing-`s` clustering false-positives on every mass noun in the domain, and a domain is mostly mass nouns. Emit plural drift as a candidate paired with the contradicting sibling; a human confirms.
- **Whether a segment is a verb or a noun.** `/orders/42/transfer`, `/documents/7/review` — a transfer and a review are also things. Check 1's word list catches only the unambiguous ones; a domain noun that is also a verb needs a reader.
- **Whether nesting is wrong or merely deep.** Check 3 counts segments. It cannot tell a genuinely contained sub-resource from a lazily-nested independent one; the deciding question ("can this id be resolved without the parent's id?") is answered by the schema, not the path.
- **What the canonical is.** 2a measures the surface against Zalando's regex; 2b measures it against itself. Neither knows what the project chose. That comes from `api-conventions.md` — and this skill halts without it rather than guessing.

**Retrofit rule — do not skip it.** When the declared canonical disagrees with the textbook, **the canonical wins and the textbook-correct endpoint is the outlier.** A detector that pushes a consistently singular surface toward plural is not finding drift, it is manufacturing it, and it spends a breaking path rename to do so. `ai/patterns/api-contract.md` § Retrofitting owns the argument (new endpoints match the declared canonical; convention changes happen only as a versioning event, whole-surface, or get closed in an ADR); this detector obeys it. The two exceptions that get fixed regardless of the canonical are a verb path whose method contradicts it (`GET /orders/42/delete` — GET is safe, so prefetchers and crawlers may fire it) and a segment leaking PII or an enumerable id (`/users/{email}`). Those are defects and route out as such; casing is not.

**Closure verb**: `unify-naming` — the same verb as #3, deliberately. The *act* is identical (pick the project's canonical, rename the outliers, ship through the deprecation flow); only the surface differs. A path rename is a breaking change even though no field moved, so `risk: high` applies whenever the route is public.

### 4. pagination-drift

**Fingerprint**: list endpoints use different pagination styles:
- `?cursor=<opaque>` (cursor-based)
- `?page=<n>&limit=<n>` (offset/limit)
- `?offset=<n>&limit=<n>` (raw offset)
- `?after=<id>` / `?before=<id>` (keyset)

Drift: mixing. The project's `api-conventions.md` should declare ONE canonical style.

**Closure verb**: `unify-pagination`.

### 5. versioning-drift

**Fingerprint**: endpoints prefixed `/v1/` and `/v2/` coexisting without documented deprecation OR with overlapping responsibility (same conceptual operation in both).

**Detection**: route table; flag mixed prefixes; cross-check `_extracted-idioms.md § Deprecations`.

**Closure verb**: `unify-versioning` (declares which is canonical; surfaces the deprecation plan for the other).

### 6. auth-header-drift

**Fingerprint**: some endpoints expect `Authorization: Bearer <token>`, others `X-API-Key: <key>`, others a custom header. Mixed within the same API.

**Closure verb**: `unify-auth-header`.

### 7. idempotency-key-missing

**Fingerprint**: write endpoints (POST/PUT/PATCH/DELETE) don't accept an `Idempotency-Key` header where the project's convention requires it. Especially critical for payment/order creation.

**Detection**: per-method scan; cross-check `api-conventions.md § Idempotency` (if the project requires it).

**Closure verb**: `add-idempotency-key`.

### 8. rate-limit-header-drift

**Fingerprint**: rate-limited endpoints advertise their quota inconsistently — some emit quota fields, others emit none; or the field family itself differs across the surface (`X-Rate-Limit-*` vs `X-RateLimit-*` vs the draft's `RateLimit` / `RateLimit-Policy`). The canonical form and the legacy-triple transition rule are owned by `ai/patterns/rate-limiting.md`; this detector asserts only that the surface must pick ONE family and use it everywhere, and that `Retry-After` — the one field here with an RFC behind it — is present on every `429`.

**Closure verb**: `unify-rate-limit-headers`.

### 8b. rate-limit-enforcement-missing

**Fingerprint**: sibling to `rate-limit-header-drift` (#8) — that one checks header NAMING; this one checks whether a limiter is WIRED AT ALL. A mutating (`POST`/`PUT`/`PATCH`/`DELETE`) or expensive-read endpoint (search, export, report, fan-out, fuzzy/`LIKE` query) has NO limiter middleware/decorator on its path while sibling endpoints do.

**Detection**: per route, look for an inbound limiter binding — middleware in the chain (`rateLimit(...)`, `@Throttle`, `throttle:`, `RateLimiterMiddleware`, gateway/Kong/Envoy `rate-limit` plugin) OR a decorator/guard. Cluster routes that HAVE one; any mutating/expensive route NOT in that cluster (and not explicitly exempted in `api-conventions.md § Rate limiting`) is drift. Emits e.g. `POST /reports/export` at `src/reports/reports.controller.ts:88` — no limiter, while `POST /orders` at `src/orders/orders.controller.ts:41` carries `@Throttle({ default: { limit: 20, ttl: 60000 } })`.

**Detection (always-on hook)**: an unlimited mutating endpoint is also a server-side resilience gap, not just a uniformity gap — flag it even when NO sibling has a limiter (the cluster is empty). The enforcement SHAPE (429 + `Retry-After` + unprefixed `RateLimit-*` headers, per-tenant buckets over a shared store, FAIL-OPEN vs FAIL-CLOSED on store outage, 503 admission control) is OWNED by `ai/patterns/rate-limiting.md` — point there; do NOT re-specify the algorithm here. 429 = RFC 6585; `Retry-After` = RFC 9110 §10.2.3; the `RateLimit` / `RateLimit-Policy` quota fields = IETF `draft-ietf-httpapi-ratelimit-headers` — still an Internet-Draft, whose HTTPDIR early review of `-10` came back "Not ready", so cite it as a direction of travel and never as a settled contract.

**Routed observation — no closure verb.** Wiring a limiter that was never there is additive capability, not drift unification. `routed_to: /add-endpoint § production floor (ENF-1) + ai/patterns/rate-limiting.md` — that pattern owns the enforcement shape, and `/add-endpoint`'s floor is where a missing limiter becomes a blocking row. Report the endpoint, the empty cluster, and stop.

### 8c. etag-conditional-drift

**Fingerprint**: a cacheable `GET` (single-resource read, or a list with a stable representation) returns no `ETag` (and no `Last-Modified`) while sibling reads do — so clients can't revalidate. Conversely, an endpoint emits an `ETag` but ignores `If-None-Match`, never returning `304 Not Modified`.

**Detection**: per `GET` route, check the response builder for an `ETag`/`Last-Modified` header and the handler for `If-None-Match` short-circuit logic. Cluster reads that revalidate; cacheable siblings outside the cluster are drift. Emits e.g. `GET /orders/:id` at `src/orders/orders.controller.ts:120` — no `ETag`, while `GET /customers/:id` at `src/customers/customer.controller.ts:96` sets `res.setHeader('ETag', weakEtag(body))` and returns `304` on match.

**Detection (pointer)**: the revalidation contract (strong vs weak ETag, `If-None-Match` → `304`, RFC 9110 obsoletes RFC 7232) is OWNED by `ai/patterns/conditional-requests.md` — point there for the exact handling.

**Routed observation — no closure verb.** `routed_to: ai/patterns/conditional-requests.md` (strong vs weak ETag, `If-None-Match` → `304`, RFC 9110). Adding revalidation to a read that never had it is a capability change with cache-correctness consequences; it belongs behind that pattern's rules, not a sweep verb.

### 8d. optimistic-concurrency-missing

**Fingerprint**: a write endpoint (`PUT`/`PATCH`/`DELETE`) targets a resource whose model carries a concurrency token — a `version` / `row_version` / `etag` / `updated_at` column — but the handler accepts NO `If-Match` precondition, so concurrent writers silently last-write-wins (lost update).

**Detection**: cross-reference the route's target model (from the ORM entity / migration) for a version/`updated_at` column against the handler's request parsing for `If-Match`. A write with the column but no precondition check is drift; bonus-flag handlers that don't return `412 Precondition Failed` on mismatch or `428 Precondition Required` when the project mandates the header. Emits e.g. `PATCH /documents/:id` at `src/documents/document.controller.ts:64` — model `Document` has `version` (`migrations/0007_documents.sql:12`) but no `If-Match` read.

**Detection (pointer)**: the over-HTTP optimistic-concurrency contract (`If-Match` → `412`, `428 Precondition Required`, RFC 9110) is OWNED by `ai/patterns/conditional-requests.md`. The DB-side stored-version replay / compare-and-swap belongs to the distributed-systems pack (`stored-idempotency-replay`) — point there, do not duplicate.

**Routed observation — no closure verb.** `routed_to: ai/patterns/conditional-requests.md` (`If-Match` → `412`, `428 Precondition Required`). Introducing a precondition changes the endpoint's contract for every existing client — it needs the deprecation flow that pattern prescribes, not a unification commit.

### 8e. batch-endpoint-contract-drift

**Fingerprint**: a route accepts an ARRAY body (bulk create/update/delete) but returns a single scalar status for the whole batch — `200`/`204` with no per-item result — so a caller can't tell WHICH items succeeded and which failed. Partial failure is invisible.

**Detection**: per route, detect array-shaped request bodies (OpenAPI `type: array`, or handler iterating the parsed body). Check the response schema for a sibling per-item status array (e.g. `{ results: [{ id, status, error? }, ...] }`) and/or a `207 Multi-Status`-style envelope. A batch route returning a bare scalar is drift. Emits e.g. `POST /orders/bulk` at `src/orders/orders.controller.ts:152` — accepts `Order[]`, returns `201` with no `results[]`, while `POST /invoices/bulk` at `src/invoices/invoices.controller.ts:71` returns `{ results: [{ index, id, status }] }`.

**Routed observation — no closure verb.** `routed_to: ai/patterns/api-contract.md § Bulk / batch endpoints (API-3)` — that section owns the all-or-nothing vs best-effort decision, the `207 Multi-Status` shape, and the per-item `results[]` row format. Which semantic the endpoint should have is a contract decision, not something a consistency sweep gets to pick.

### 8f. field-selection-drift

**Fingerprint** (opt-in — fires ONLY if `api-conventions.md § Field selection` declares a `?fields=` / `?expand=` / sparse-fieldset convention): some list/detail endpoints honour `?fields=`/`?expand=` (sparse fieldsets / relation expansion) while sibling endpoints silently ignore the param and return the full representation.

**Detection**: skip entirely unless the convention is declared. When declared, per read route check the handler for parsing of the declared param (projection / expansion logic). Cluster endpoints that honour it; sibling reads of comparable resources that ignore it are drift. Emits e.g. `GET /customers` at `src/customers/customer.controller.ts:40` honours `?fields=`, but `GET /orders` at `src/orders/orders.controller.ts:33` ignores it and returns all columns.

**Detection (pointer)**: the underlying `SELECT *` / over-fetch at the data layer is OWNED by the database pack — point there; this detector only flags the HTTP-surface UNIFORMITY of the param contract.

**Routed observation — no closure verb.** `routed_to: ai/patterns/api-contract.md § Field selection / expansion (API-5)`. That section already declares field selection an **opt-in capability with one project-wide convention** — so an endpoint ignoring `?fields=` is either a gap against a declared convention (fix it there, under that section's allow-list and N+1 rules) or evidence the convention was never declared (in which case the detector should not have fired). Neither outcome is a rename.

### 8g. security-header-drift

**Fingerprint** (low weight — presence-UNIFORMITY only): some response paths set baseline security headers (`X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `X-Frame-Options` / CSP) while others omit them, so the header set is inconsistent across the surface.

**Detection**: sample response headers across route groups (global middleware vs per-route overrides that strip/skip the security middleware). Flag groups whose responses lack a header that the majority of paths set. This detector asserts ONLY uniformity of presence — it does NOT define which headers are required, their values, or threat coverage. The security-header POLICY (which headers, correct values, HSTS max-age/preload, CSP shape) is OWNED by the security pack (`security-headers`) — point there.

**Routed observation — no closure verb.** `routed_to: security pack § security-headers`. This detector deliberately asserts *nothing* about which headers are required or what their values should be — it cannot close a finding whose correctness criterion lives in another pack. Report the non-uniform route group and hand over.

### 9. log-field-drift

**Fingerprint**: structured logs use different field names for the same concept across endpoints.

Common drifts:
- `userId` vs `user_id` vs `uid`
- `orderId` vs `order_id` vs `oid`
- `requestId` vs `req_id` vs `correlation_id` vs `trace_id`

**Detection**: scan all `log.info(...)` / `logger.warn(...)` / similar calls; extract structured fields; classify by concept; flag drift.

**Closure verb**: `unify-log-fields` — applies the project's canonical name from `_extracted-idioms.md § Logging`.

### 10. metric-name-drift

**Fingerprint**: counters / histograms / gauges named inconsistently for similar concepts.

Common drifts:
- `orders.created` vs `OrderCreated` vs `order_created_total` vs `orders_created`
- Different unit suffixes (`_ms` vs `_seconds` vs none)

**Detection**: scan metric registration; classify by concept; flag drift.

**Closure verb**: `unify-metric-names`.

### 11. trace-span-drift

**Fingerprint**: tracing spans for similar operations have different names / attributes.

Common drifts:
- `db.query` vs `database.fetch` vs `repo.read`
- Some spans tagged with `db.statement`, others not.

**Closure verb**: `unify-trace-spans`.

### 12. timeout-policy-drift

**Fingerprint**: per-endpoint or per-client timeout values differ across call sites in the same tier without a documented reason. Some 30s, some 5s, some absent.

**Detection (runnable)**: harvest every timeout literal with its call site, then cluster. The clustering is the detector; a list of timeouts is not a finding.

```bash
# 1. Harvest. Cover the three shapes: client-construction options, per-call options, and
#    server/middleware config. Extend the pattern list from `references/<framework>.md` — this
#    grep is stack-shaped, and a stack whose primitive is absent here scans clean for the
#    wrong reason. Searched over "${ROOTS[@]}" (a guessed `src/ config/` exits 2 on a monorepo
#    and the cluster comes back empty); X keeps test doubles out of the cluster.
X=(-g '!**/*.{spec,test}.*' -g '!**/{test,tests,__tests__,__mocks__}/**')
rg -n --no-heading \
  -e '\btimeout\s*[:=]\s*[0-9_]+' \
  -e '\b(timeoutMs|requestTimeout|connectTimeout|readTimeout|socketTimeout|deadline)\s*[:=]' \
  -e 'AbortSignal\.timeout\(\s*[0-9_]+' \
  -e 'WithTimeout\(\s*[a-z]+,\s*[0-9]+' \
  "${X[@]}" "${ROOTS[@]}" | sort -t: -k1,1 > timeouts.txt

# 2. Cluster by value. A surface with one or two values has a canonical; a surface with nine
#    has drift. The count is what makes this emittable, not any single row. Strip the
#    `path:line:` prefix and keep only the number after the timeout key — a bare
#    `grep -oE '[0-9_]+'` over the rows clusters line numbers.
sed -E 's/^[^:]+:[0-9]+://' timeouts.txt \
  | grep -oE '([Tt]imeout[A-Za-z]*|deadline)[[:space:]]*([:=]|\()[[:space:]]*([a-z]+,[[:space:]]*)?[0-9_]+' \
  | grep -oE '[0-9_]+$' | tr -d '_' | sort -n | uniq -c | sort -rn
```

**Unit ambiguity is the footgun, and it is not cosmetic.** `timeout: 30` means 30 **seconds** in some clients and 30 **milliseconds** in others; the same integer in two files can be a 1000× difference. Resolve the unit from each library's own docs before comparing two numbers, and if a value's unit cannot be resolved, it does not enter the cluster — it is reported as `unit unresolved` at its `<file:line>`. Two "different" timeouts that are the same duration are a phantom finding; two identical integers that differ by three orders of magnitude are the real one, and a naive cluster reports exactly backwards on both.

**Per-tier drift is correct, not drift.** A 30s export and a 2s lookup are supposed to differ. Cluster **within** a tier (same downstream, same interactivity class) and emit only when siblings in one tier disagree. The finding must name the tier and the sibling it contradicts.

**A missing timeout outranks an inconsistent one.** A call site with *no* timeout is unbounded — it is not the low end of the distribution, it is a different defect (a hung upstream pins a worker until the process is restarted). Report it first, separately, and never fold it into the "inconsistent values" count.

**Closure verb**: `unify-timeout-policy`. A call site with no timeout at all routes to `distributed-systems` (bulkhead / deadline propagation) rather than closing here — this skill unifies values that exist, it does not introduce resilience the surface never had.

### 13. retry-policy-drift

**Fingerprint**: retry counts, backoff shape, or jitter differ across call sites hitting comparable dependencies, with no documented reason.

**Detection (runnable)**:

```bash
# Retry configuration, wherever the stack puts it.
rg -n --no-heading \
  -e '\b(retries|maxRetries|max_attempts|maxAttempts|retryCount|attempts)\s*[:=]\s*[0-9]+' \
  -e '\b(backoff|retryDelay|retry_backoff|initialInterval)\s*[:=]' \
  -e '\b(retry|Retry|with_retry|@Retryable|retryWhen|p-retry|tenacity|backoff\.on_exception)\b' \
  "${X[@]}" "${ROOTS[@]}" > retries.txt

# Which files make outbound calls: the CLIENT imports and calls, never the word `http` (which
# matches every HttpException / HttpStatus import). If the project wraps its client in one
# outbound kernel, add the wrapper's import as one more -e — the retry policy then lives there.
rg -l \
  -e "(from|require\()\s*['\"](axios|undici|got|node-fetch|ky|ofetch|@nestjs/axios)['\"]" \
  -e '\bfetch\(' -e '\bHttpService\b' -e '\bHttpClient\b' \
  -e '^\s*(import|from)\s+(requests|httpx|aiohttp|urllib3)\b' -e '"net/http"' \
  -e '@grpc/grpc-js|grpc\.(insecure_channel|Dial)' \
  "${X[@]}" "${ROOTS[@]}" | sort > callers.txt
awk -F: '{print $1}' retries.txt | sort -u > has-retry.txt
comm -23 callers.txt has-retry.txt          # outbound callers with NO retry policy
```

**The dangerous finding here is not inconsistency — it is a retry on a non-idempotent write.** A `POST` retried after a timeout may have succeeded upstream; the retry duplicates the side effect, and the caller cannot tell. Before reporting any retry row as merely inconsistent, check the method and the idempotency key: a retry on a `POST` with no `Idempotency-Key` is a correctness defect that outranks every drift row in this file, and it routes to `add-idempotency-key` (verb 7) rather than to `unify-retry-policy`. **When the distributed-systems pack is installed**, retry *eligibility* is its `retry-deadline-scan` §5 — a retry on a non-idempotent call, a library default that retries any method on a network error (axios-retry's default condition retried one POST 4× after a socket reset, measured in the backend research lab), a provider idempotency key minted per attempt: hand the row there as `→ distributed-systems retry-deadline-scan §5` and keep only the drift here. Without that pack, report it here under verb 7 at its `<file:line>`, marked `owner absent`.

**Retry without jitter is a synchronised herd.** Identical backoff across N callers reconverges them onto the same recovery instant, which is how a recovering dependency gets knocked over a second time. Flag a backoff config with no jitter parameter even when every call site agrees — this is the one row where *consistency itself* is the defect, and a cluster-based detector reports it as clean.

**Retry budgets compose multiplicatively.** Three layers each retrying 3× is 27 requests for one logical call, and each layer looks reasonable on its own. When the harvest shows retry configured at more than one layer of the same path, report the product, not the individual counts.

**Closure verb**: `unify-retry-policy`. The retry *mechanism* (circuit breaker, budget, deadline propagation) is owned by the distributed-systems pack; this detector unifies what the surface already declares and hands the rest over.

### 14. openapi-coverage-gap

**Fingerprint**: an endpoint exists in the route table but isn't in the OpenAPI spec.

**Detection**: route registry minus OpenAPI paths.

**Closure verb**: `add-openapi-doc`.

### 15. example-coverage-gap

**Fingerprint**: endpoint is in OpenAPI but has no `examples` for request/response. (Or a single trivial example that doesn't reflect real-world payloads.)

**Closure verb**: `add-endpoint-example`.

## Procedure (step-by-step)

1. **Pre-flight**:
   - `PROJECT_KIND` matches `backend-*`. Halt otherwise (this skill is backend-only).
   - `_extracted-idioms.md § API conventions` OR `ai/api-conventions.md` exists. Halt if missing — without canonical conventions, drift is undefined.
   - OpenAPI spec discoverable (warn-only if missing; openapi-coverage detector skips).
2. **Build endpoint registry** — walk controllers / route table; emit one row per `{method, path, file, line}`.
3. **For each fingerprint** (1–15 + 3b, plus routed siblings 8b–8g above):
   - Apply the detector's fingerprint procedure across the registry.
   - Emit findings. A closure-verb detector emits `closure_verb:` with a value from the 15-verb table; a routed observation emits `routed_to:` and **no `closure_verb:` key at all**. Writing a verb outside the vocabulary does not degrade gracefully — `validate-polish-artifacts.sh` fails the entire artifact, so the run that took an hour produces nothing.
4. **Cross-cutting check** — if a finding's closure verb would break a public contract (rename a response field; change envelope shape), flag `risk: high` and require ADR.
5. **Write artifact** — `ai/polish/_api-decisions.md` with all findings grouped by subclass.

## Hard rules

- **Behaviour-preserving** — closure verbs that rename / unify ship via deprecation flow (additive change first, deprecation header, removal in next major). Blind rewrites are forbidden — they break clients.
- **Per-endpoint commit** — one finding = one commit (except for naming-convention-drift sweeps where a single mass-rename commit is acceptable when wired through serializer mapping).
- **OpenAPI must stay in sync** — every code change updates the spec in the same commit.
- **Contract tests must stay green** — if the project has them.
- **No detector invents new conventions** — the canonical shape always comes from `_extracted-idioms.md § API conventions`. If that file says nothing about envelope/naming/etc., the detector skips with WARN.
- **No detector invents a closure verb.** The vocabulary is the 15 in the table above and it is enforced by a script, not by convention. Reuse the verb whose *act* matches, or emit `routed_to:` instead. Extending the vocabulary is a coordinated change to `scripts/validate-polish-artifacts.sh` **and** `commands/polish.md` — not something a detector does unilaterally.

## False positives / gotchas

- **A single consistent shape is not drift.** A bare-resource envelope (no wrapper) used *everywhere* is valid — flag only the *mix*. Same for pagination style, auth header, naming case: uniformity is the goal, not a specific choice.
- **Tier-scoped variation is legitimate.** Different timeouts/retries *across* service tiers (public vs internal vs batch) are fine; only *within-tier* divergence with no documented reason is drift.
- **Opt-in detectors stay silent unless declared.** `field-selection-drift` fires only if `api-conventions.md § Field selection` declares a `?fields=`/`?expand=` convention; don't invent one.
- **`noindex`-style intentional exemptions** — an endpoint explicitly exempted in `api-conventions.md` (e.g. a health check with no rate limit, an internal admin route with offset pagination) is not drift; honour the declared exemption.
- **Ownership pointers, not re-specification** — the six routed observations (8b–8g) flag *uniformity* and nothing more; the algorithm, contract, or policy is owned by the named pattern or the security/database/observability pack. Do not emit a fix that re-specifies the owned shape, and do not attach a closure verb to one — a finding this skill cannot close is a finding it must hand over.
- **A path rename is a breaking change** — `resource-naming-drift` (3b) reuses `unify-naming`, but a public route rename is `risk: high` and takes the same dual-route-then-sunset flow as a field rename. Renaming a path "because it's just a string" breaks every stored link, bookmark, and integration runbook.
- **The custom-method verb is camelCase on purpose.** `POST /shipping-addresses/42:markPrimary` in an otherwise kebab-case surface is not case drift — AIP-136 requires camelCase after the colon, so the island is correct under either casing doctrine. Check 2a above cannot see it (the verb follows a `:`, not a `/`); a hand-written case detector that flags it has a bug.

## Halt conditions

- **`api-conventions.md` / `_extracted-idioms.md § API conventions` missing** → halt; the canonical is undefined. Surface "/setup-project --refine to declare API conventions first". No detector invents a convention.
- **Conflicting conventions** (`api-conventions.md` says snake_case but `_extracted-idioms.md` says camelCase) → halt; surface the conflict for user resolution rather than picking one.
- **`PROJECT_KIND` is not `backend-*`** → halt (this skill is backend-only).
- **A finding lacks its cited `<method path>` + `<file:line>` + the canonical it diverges from** → not emittable; re-derive or drop it.
- **High-risk closure** (would break a public contract — rename a field, change the envelope) → flag `risk: high`, halt *that* finding, surface the ADR template; the rest continue.
- **OpenAPI spec missing** → warn (not halt); skip the openapi-coverage + example-coverage detectors only.

## References

- `_extracted-idioms.md § API conventions` (project-specific oracle).
- `ai/api-conventions.md` (alternative location).
- `align-discipline.md` — closed-vocabulary closure-verb discipline.
- `polish` command — dispatches this skill on backend stacks.
- `ai/patterns/rate-limiting.md` — server-side inbound limit + load shedding (429 + `Retry-After` + `RateLimit-*` headers; per-tenant buckets; shared store; FAIL-OPEN/CLOSED; 503 admission control). Owner of the enforcement shape that routed observation 8b hands off to.
- `ai/patterns/conditional-requests.md` — `ETag`/`If-None-Match` → `304` (read revalidation) + `If-Match` → `412` / `428` (optimistic concurrency over HTTP); RFC 9110. Owner of routed observations 8c + 8d.
- `ai/patterns/response-streaming.md` — NDJSON/SSE/chunked for unbounded results; mid-stream terminal error sentinel; backpressure; disconnect cancellation; RFC 9112. Consider when a list/export route would otherwise return an unbounded body.
- `ai/patterns/async-job-offload.md` — `202 Accepted` + `Location` + status URL; job-status state machine; idempotent submit; result TTL. Consider for the expensive endpoints surfaced by 8b instead of holding a synchronous connection.
