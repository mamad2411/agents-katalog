---
name: endpoint-test-method
description: Hit a running dev endpoint via curl and verify status + response shape + required headers (auth, tenant) field-by-field against the DTO. Use AFTER any controller, DTO, guard, pipe or interceptor edit to prove the route works end-to-end, or when a frontend reports an unexpected shape and you need ground truth. NOT when no dev server is running (it refuses to auto-start), NOT against staging/prod hosts, and NOT for static contract diffing — that is api-snapshot.
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# endpoint-test-method

## Premise

Find real bugs, not hand-waves. Every assertion cites the controller/DTO `<file:line>` and the actual response body produced. "Returned 200, looks fine" is not verification — phantom-success (200 with wrong shape) is the most common regression here. Field-by-field diff against the response DTO is mandatory; key-set comparison alone is insufficient. Cross-tenant 200 is a real bug, never "dev mode".

A run that skips any of the 5 mandatory cases (golden, invalid body, no auth, wrong tenant, idempotency) is incomplete.

Make an HTTP request to a local endpoint, then verify the status, headers, and response body match what the controller + DTO declared.

**Ownership inside the endpoint-test-method triad.** This skill owns the *mechanism*: the curl invocations, the assertions, and the field-by-field diff. The `endpoint-tester` agent owns *case selection and the verdict*. The `/endpoint-test` command owns *argument resolution and escalation routing*. Each of the three states its cases once; when you need to know what a call actually asserts, it is here.

## When to use

- After editing a controller method (handler, decorators, route).
- After changing an input or response DTO.
- After a guard / interceptor / pipe change that affects the route.
- When suspecting a regression — quick sanity check before blaming the frontend.

## Prerequisites

- Dev server running on a known port. **Resolve the port from the project, never from a convention** — read the dev script in `package.json` / `Procfile` / compose file, or `CLAUDE.md`, and confirm with `lsof -i :<port>` or the `start:dev` log. A repo with several deployable apps has one port per app; enumerate them from the same source rather than assuming a pairing. Testing the right route against the wrong app's port produces a `404` that reads like a missing endpoint and a `200` that reads like a pass.
- Auth credentials in `.env.local` / `.env.dev` — NEVER use `*PROD*` credentials or `*.prod.env`.
- `curl` and `jq` available.

## Safety invariants

- ONLY target `localhost`, `127.0.0.1`, `::1`, or a tunnel the user explicitly named in this session (`*.ngrok.io`, `*.trycloudflare.com`, `*.loca.lt`).
- Refuse on any other host unless the user confirms in writing with the URL.
- Print every curl so the user can replay.

## Procedure

1. Read the controller — method, path, required headers, body shape, response shape.
2. Read the input DTO — derive the **minimal valid payload** (required fields + valid types).
3. Read the response DTO — note every field that should appear.
4. Resolve base URL from `CLAUDE.md` / `ai/stack.md`. If absent, ask the user; do not guess.
5. Source credentials from `.env.local`, `.env.dev`, or `.env.example`.
6. Execute 5 cases minimum:

   **1. Golden path** (valid auth, valid body)
   ```bash
   curl -sS -X POST "http://localhost:4000/api/v1/orders" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $DEV_JWT" \
     -H "X-Tenant-Id: dev-tenant" \
     -d '{"customerId":"u_1","items":[{"sku":"A1","qty":2}]}' \
     -w "\n---\nstatus=%{http_code}\ntime=%{time_total}s\n" | tee /tmp/r1.json
   ```
   Assert: status matches documented success (201/200/204), body field-by-field matches response DTO, correlation-id header (if declared), `time_total` within SLO.

   **2. Invalid body** — drop a required field; expect the project's declared validation-failure status (`422 Unprocessable Content` for a well-formed body that fails semantic validation; `400` only for a body that could not be parsed at all — see `ai/patterns/error-handling.md` § Status mapping) carrying the project's field-error rows, each naming the offending field with a stable machine code.
   **3. No auth** — omit `Authorization`; expect 401 (or 403 for public-but-rate-limited).
   **4. Wrong tenant** — header that doesn't own the resource; expect 404 (preferred) or 403. A 200 here is a cross-tenant leak (file as security finding).
   **5. Idempotency** (mutating endpoints with `Idempotency-Key`) — two POSTs with the same key; second returns same body, no duplicate side effects.

7. Field-by-field shape diff vs response DTO:
   ```bash
   jq -r 'keys_unsorted|join(",")' /tmp/r1.json
   ```
   Compare the key set against the DTO file.

## Conditional cases (run when the endpoint's contract declares the capability)

These are not optional in the sense of "nice to have" — each one runs **iff** the endpoint claims the corresponding capability, and skipping a case for a capability the endpoint does claim is the same incompleteness as skipping one of the mandatory five. Cite the declaration (`<file:line>` of the decorator, the OpenAPI row, the middleware) that put the case in scope.

**Rate limit** — if a limiter is bound to the route.
```bash
for i in $(seq 1 "$((LIMIT + 1))"); do
  curl -sS -o /dev/null -D - -X GET "$BASE/api/v1/orders" \
    -H "Authorization: Bearer $DEV_JWT" \
    -w "status=%{http_code}\n" | grep -iE '^(status|retry-after|ratelimit)'
done
```
Assert on the `(LIMIT+1)`-th call: status `429`, **`Retry-After` present** (this is the one field with an RFC behind it — RFC 9110 §10.2.3), and a quota field present. The quota field family is the project's choice per `ai/patterns/rate-limiting.md` — the draft's `RateLimit` / `RateLimit-Policy`, the draft-05 `RateLimit-Limit`/`-Remaining`/`-Reset` triple, or both during migration. Assert the family the project declared; do **not** assert a family the project never adopted, and do not treat the absence of the legacy triple as a failure on a project that emits the two-field form.

**Conditional requests** — if the read emits `ETag` or `Last-Modified`.
```bash
ETAG=$(curl -sS -D - -o /dev/null "$BASE/api/v1/orders/$ID" -H "Authorization: Bearer $DEV_JWT" \
       | awk 'tolower($1)=="etag:"{print $2}' | tr -d '\r')
curl -sS -o /dev/null -w "revalidate=%{http_code}\n" "$BASE/api/v1/orders/$ID" \
     -H "Authorization: Bearer $DEV_JWT" -H "If-None-Match: $ETAG"
```
Assert `304` with an empty body. An endpoint that sets `ETag` and still returns `200` on a matching `If-None-Match` has a header that costs bytes and buys nothing. If the resource carries a version column and the write path declares `If-Match`, repeat with a stale validator and assert `412`.

**Async / `202` hand-off** — if the write offloads to a job.
```bash
LOC=$(curl -sS -D - -o /dev/null -X POST "$BASE/api/v1/exports" -H "Authorization: Bearer $DEV_JWT" \
      -d '{}' | awk 'tolower($1)=="location:"{print $2}' | tr -d '\r')
curl -sS "$BASE$LOC" -H "Authorization: Bearer $DEV_JWT"
```
Assert `202`, a `Location` header, and that following it returns a job-status document whose state is one of the declared values. A `202` with no `Location` is a promise with no way to collect on it.

**Streaming** — if the response is NDJSON / SSE / chunked. Assert the `Content-Type` matches the declared transport and that the stream carries a terminal marker (success sentinel or error record) rather than just ending. See `ai/patterns/response-streaming.md`; note that a streaming route is exempt from the envelope diff, so the terminal-marker assertion is the only completeness check it gets.

**Pagination** — `?limit=10&cursor=...` returns at most 10 items plus a next cursor; the next cursor actually advances (page 2 ≠ page 1).

**Filters / sorts** — each declared param demonstrably changes the result set. A param that is accepted and ignored is worse than a `400`.

**Soft-delete** — a deleted record returns `404` on read while the row still carries `deleted_at`.

## Output

```
## /api/v1/orders [POST]   base=http://localhost:4000 (SAFE — localhost)

| # | Case                | Status | Assertion                       | Result |
|---|---------------------|--------|---------------------------------|--------|
| 1 | Golden path         | 201    | DTO shape match                 | PASS   |
| 2 | Missing `items`     | 422    | fieldErrors[].field == 'items'  | PASS   |
| 3 | No auth             | 401    | WWW-Authenticate header         | PASS   |
| 4 | Wrong tenant        | 404    | no resource in body             | PASS   |
| 5 | Idempotency replay  | 201    | same body both calls            | FAIL — different createdAt timestamps

Bugs surfaced:
  - case 5: idempotency not honored; missing IdempotencyService.getOrSet wrap.
  - case 1: response DTO declares correlationId but response omits it.

Curl commands:
  <each executed curl preserved for replay>
```

## False positives / gotchas

- **Phantom success** — 200 with wrong shape. Always diff response keys against DTO field-by-field.
- **Too-permissive dev auth** — local server may skip tenant guards that prod enforces. Cross-tenant 200 is a real bug, not "dev mode".
- **Stale server** — code edited but server not restarted. Look for the new line of code in the log; absent = restart needed.
- **Dynamic fields** (`createdAt`, `id`, `correlationId`) differ between calls — exclude when comparing shapes, not values.
- **A capability asserted that the project never adopted.** The mirror of phantom success: failing an endpoint for not emitting a header family, a cursor style, or a validator the project's conventions never declared. Assert the declared contract, not the one you would have designed.
- Don't start the server yourself (side effects). Print the dev command and stop if it isn't running.

## Related

- **Runnable primitive.** endpoint-test-method is the executable curl primitive that the `@endpoint-tester` agent orchestrates — the agent adds case selection, reporting, and verdict discipline; this skill is the hit-and-assert mechanism it drives.
- `.claude/skills/log-tail-method/SKILL.md` — follow a failing case (500, phantom success) into the structured logs by its correlation id.
- `.claude/skills/debug-tenant/SKILL.md` — escalate a cross-tenant 200 (case 4) into the full tenant-leak playbook.
- `.claude/skills/api-snapshot/SKILL.md` — the static-contract counterpart: snapshot guards the *declared* OpenAPI shape, endpoint-test-method guards the *running* response.
- `ai/patterns/api-contract.md` — the response-DTO / envelope shape each field-by-field assertion diffs against.
- `ai/patterns/error-handling.md` — the error-envelope + status mapping cases 2–4 expect.

## Halt conditions

- Halt on hand-waves: every PASS must cite the case number + status code + DTO `<file:line>` it diffed against.
- Halt if any of the 5 mandatory cases (golden / invalid body / no auth / wrong tenant / idempotency) was silently skipped.
- Halt if a conditional case was skipped for a capability the endpoint **does** declare — cite the declaration that put it in scope, or state why it is out of scope. "Probably fine" is not a scope decision.
- Halt if a 200 response was accepted without field-by-field diff against the response DTO — phantom success is the classic miss.
- Halt if the target host is not localhost / 127.0.0.1 / a session-named tunnel — refuse to fire requests at unverified hosts.
