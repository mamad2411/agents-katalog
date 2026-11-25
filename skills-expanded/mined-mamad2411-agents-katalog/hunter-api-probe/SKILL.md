---
name: hunter-api-probe
description: >-
  Drive an HTTP/API surface to hunt deviations and capture every exchange.
  Load when the target is an endpoint, route, or API and you must send real
  requests, not read the handler source. Specifies contract conformance against
  OpenAPI/schema, status-code correctness, error-shape consistency, the
  authorisation matrix (every endpoint x every role including unauthenticated),
  idempotency, pagination, rate-limit behaviour, input-boundary and injection
  probes, and response-time distribution capture. Defines the captured-exchange
  artifact format. Use to probe an endpoint, check a contract, test authz,
  fuzz inputs, or capture HTTP evidence for a Sign or Trail.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hunter API Probe

Assumes `hunter-doctrine` is loaded. An API deviation you cannot reproduce with
a real request/response pair is not a Find. Reading the handler tells you what
should happen; this skill records what does. Every claim carries the captured
exchange — "I observed a 500" is not evidence; the exchange is.

## Inputs

- Base URL and the surface map of endpoints (from `hunter-recon` if available;
  otherwise the OpenAPI/schema, or a crawl of the route table).
- The contract, when one exists: OpenAPI/Swagger, JSON Schema, a typed client,
  or acceptance criteria. Its presence sets `hunt_mode = conformance`; its
  absence sets `hunt_mode = defect` (universal correctness only).
- Credentials **per role**, provided by the operator. Never fabricate tokens.

## The captured-exchange artifact

Every request Hunter sends is written whole. This is the addressable evidence
unit for every API Sign and Trail. Store under
`run/<hunt-id>/api/<endpoint-slug>/<seq>.json`:

```json
{
  "exchange_id": "api/session/003",
  "at": "2026-08-07T14:02:11Z",
  "request": {
    "method": "POST",
    "url": "https://target/api/session",
    "headers": { "content-type": "application/json",
                 "authorization": "Bearer <redacted:role=editor>" },
    "body": { "email": "a@b.co", "password": "<redacted>" }
  },
  "response": {
    "status": 500,
    "headers": { "content-type": "text/html" },
    "body_bytes": 1284,
    "body_excerpt": "<pre>TypeError: cannot read property...",
    "elapsed_ms": 812
  },
  "role": "editor",
  "expectation": { "authority": "spec:openapi.yaml#/paths/~1session/post",
                   "expected_status": 200, "expected_shape": "SessionToken" }
}
```

Redact secret header/body values to `<redacted>` but record that they were sent
and which role they belonged to. The exchange must be complete: method, URL,
headers, body, status, response headers, timing. A partial exchange is a Sign at
best.

## Probe classes

Run these against every endpoint on the surface map. Each produces Signs.

### 1. Contract conformance (conformance mode)

For every endpoint with a schema entry, validate the live response against the
declared schema: status set, required fields, types, enums, formats, nullable
rules. Quote the violated schema line verbatim as the authority. A response that
returns 200 with a field the schema declares required-and-absent is a deviation
even though the status is "fine".

### 2. Status-code correctness

Map the observed status against the correct one for the input:
- Valid input → 2xx; malformed body → 400; missing/invalid auth → 401;
  authenticated-but-forbidden → 403; unknown resource → 404; wrong method → 405;
  conflicting state → 409; valid-but-unprocessable → 422.
A 200 wrapping an error body, or a 500 where a 400 belongs, is a Sign — the
status code is a contract with every client and cache.

### 3. Error-shape consistency

Collect the error body of every non-2xx response across all endpoints. They must
share one shape (same envelope, same field names, same content-type). A mix of
JSON `{error}`, HTML stack traces, and bare strings is a deviation: it breaks
every client's error handling and often leaks internals. A raw stack trace in a
response body is CRITICAL — it is an information-disclosure Find.

### 4. Authorisation matrix — the highest-yield class

**This is the probe class that finds the most and is almost always under-
covered.** Build the full matrix: **every endpoint × every role, including
unauthenticated and a low-privilege role.** Do not sample it.

For each cell, send an otherwise-valid request carrying that role's credential
(or none) and record the status:

```
                 unauth   viewer   editor   admin
GET  /users        401      200      200     200
POST /users        401      403      403     200
GET  /users/:id    401      200*     200     200     * own record only?
DELETE /users/:id  401      403      403     200
```

Flag every cell where a lower role reaches data or an action it must not:

- unauth or viewer receiving 2xx on a privileged endpoint → auth-bypass Find
- 403 vs 404 leakage: a 403 on a resource that should read as 404 to this role
  discloses existence — record it
- IDOR: authenticate as role A, request role B's object by id; a 2xx is a Find
- horizontal escalation: same-role access to another tenant's data

The matrix's denominator (endpoints × roles) is your authz coverage fraction.
Any unfilled cell is **dark**, never assumed safe.

### 5. Idempotency

For methods that declare idempotency (GET, PUT, DELETE) or accept an
`Idempotency-Key`, send the identical request twice and diff the effect. A
second DELETE that 500s, a PUT that double-applies, or a keyed POST that charges
twice is a Sign. Capture both exchanges.

### 6. Pagination

Walk a paginated collection end to end. Probe: does `limit`/`offset` or the
cursor honour bounds; do pages overlap or drop records at boundaries; does the
total count match the walked count; does an out-of-range page 500 or return junk;
is ordering stable across pages. Record the walked count vs declared total.

### 7. Rate-limit behaviour

Send a burst past the declared limit (only against an authorised target). Verify:
429 (not 500) on breach, a `Retry-After` or reset header present and accurate,
the limiter recovers after the window, and it does not lock out unrelated
clients. Absence of any limit on an auth or write endpoint is itself a Sign.

### 8. Input-boundary and injection probes

Per parameter, send: empty, max-length + 1, wrong type, negative/zero, unicode
and emoji, and injection markers appropriate to the backend (SQL: `' OR '1'='1`;
NoSQL: `{"$gt":""}`; command: `; id`; template: `${7*7}`; path: `../../etc`).
A probe is a Find only when a response **proves** injection (data returned that
should not be, an evaluated expression, a stack trace revealing the query) — not
when the input is merely accepted. Only probe systems you are authorised to
test.

### 9. Response-time distribution

Per endpoint, send **≥5** requests and capture the full distribution
(min/median/p95/max), never a single number. A single timing is not evidence of
a performance deviation. Record the distribution; hand outliers with a stated
threshold to `hunter-repro`.

## Outputs

Per endpoint, a Sign record referencing its captured exchanges:

```json
{
  "sign_id": "sign/1a7b",
  "surface": "GET /api/users/:id",
  "observed": "viewer role reads another user's record (IDOR)",
  "raw_steps": [
    "auth as viewer (user 12)",
    "GET /api/users/99 -> 200 with user 99 PII"
  ],
  "authority": "implicit",
  "artifacts": ["api/users/007.json", "api/users/008.json"],
  "probe_class": "authz-matrix",
  "role": "viewer"
}
```

Plus a per-surface coverage line as a real fraction, and the authz matrix as an
artifact with dark cells named:
`api coverage: 34/40 endpoints probed · authz 152/160 cells · 8 dark`.

## Handoff

- Confirmed Signs → `hunter-repro` for 2-of-2 and the Trail; `min_steps` become
  a curl/HTTP script the fixer can replay.
- Coverage fractions + the authz matrix → the report coverage map (§12 §2).
- Contract citations carry `spec:<file>#<pointer>` so the report names the
  authority verbatim.

## Never

- **NEVER** fabricate a token or bypass a control you were not asked to test.
- **NEVER** sample the authz matrix; every endpoint × every role or the missing
  cells are dark.
- **NEVER** call an input-injection probe a Find without a response proving the
  injection.
- **NEVER** report a performance deviation from a single timing; capture ≥5.
- **NEVER** run bursts, writes, or injection against an unauthorised target.
