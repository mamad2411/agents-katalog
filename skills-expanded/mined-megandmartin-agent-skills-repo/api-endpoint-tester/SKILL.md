---
name: api-endpoint-tester
description: curl-based smoke tests for any API — auth enforcement, happy path, error cases, and latency — reported in a pass/fail results table. Use when the user says "test my API", "check the endpoints", "does auth actually work", "smoke test the backend", or shipped/changed API routes. Don't use for chasing one known bug to its root cause — use bug-triage-protocol.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, API, Testing, curl]
    related_skills: [vercel-deploy-check, bug-triage-protocol, supabase-migration-writer, env-secrets-hygiene]
---

# API Endpoint Tester

Systematic smoke tests with nothing but curl and python3. For every endpoint, four questions get an evidence-backed answer: does it reject strangers (auth), does it work when used right (happy path), does it fail politely when used wrong (errors), and is it fast enough (latency)? The most important test is the one vibe-built apps skip: **the request that should be rejected.**

## When to Use

- New or changed API routes need a confidence check before/after deploy.
- User suspects an endpoint is unprotected ("can anyone call this?").
- Building the results table for a launch checklist or PR.
- **Not for:** isolating a known bug — use `bug-triage-protocol`. Not for whole-site deploy verification — use `vercel-deploy-check`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Status + latency, one line | `curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" "$BASE/api/items"` |
| Unauthenticated probe | `curl -si "$BASE/api/items" \| head -1` (expect 401/403, NOT 200) |
| Authenticated GET | `curl -s "$BASE/api/items" -H "Authorization: Bearer $TOKEN"` |
| POST happy path | `curl -si -X POST "$BASE/api/items" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name":"test"}'` |
| Malformed-body probe | `curl -si -X POST "$BASE/api/items" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name":'` (expect 400, not 500) |
| Pretty-print JSON | append `\| python3 -m json.tool` (or `\| jq .`) |
| Latency, 5 runs | `for i in 1 2 3 4 5; do curl -s -o /dev/null -w "%{time_total}\n" "$BASE/api/items"; done` |

## Procedure

1. **Precheck** — `command -v curl python3`. Set `BASE` (prefer a preview/staging URL; confirm explicitly with the user before running POST/DELETE tests against production data). Get a real `$TOKEN` (browser devtools → Network → copy the Authorization header from a logged-in request). Export both as env vars — never paste tokens into files or the transcript.
2. **Inventory** — list endpoints to test: from the code (`grep -rE "app\.(get|post|put|delete)|export async function (GET|POST|PUT|DELETE)" --include="*.ts" -l api/ app/api/ src/ 2>/dev/null`), the router directory listing, or the user. For each: method, path, auth required?, sample valid body.
3. **Auth pass (first, always)** — hit every protected endpoint with no token, then with garbage (`-H "Authorization: Bearer nonsense"`). Expect 401/403 both times. A 200 with real data here is a **critical finding — report it immediately**, before finishing the sweep. Where multi-user data exists, also try user A's token against user B's resource id — expect 403/404.
4. **Happy path** — one valid call per endpoint with `$TOKEN` and a valid body. Expect 2xx and a sane JSON shape (spot-check fields via `python3 -m json.tool`). For POSTs, use obviously-test data (`"name":"smoke-test-<date>"`) and note created ids for cleanup.
5. **Error cases** — per write endpoint: malformed JSON (expect 400), missing required field (expect 400 with a useful message), nonexistent id (expect 404). Any 500 on bad input is a fail — servers should never crash on user input.
6. **Latency** — 5 runs per key endpoint (first run is cold start; report it separately). Bar: median under 1s for simple reads; over 3s is a fail worth a `bug-triage-protocol` follow-up.
7. **Cleanup + deliver** — delete test rows you created (confirm with the user before any DELETE call). Fill the results table; every FAIL gets the exact repro command so the fix loop starts instantly.

## Output Template

```
## API Smoke Test — <base url> — <date>
Token user: <role/email>   Environment: preview | production (confirmed)

| Endpoint | Test | Expected | Got | Latency (median) | Result |
|---|---|---|---|---|---|
| GET /api/items | no token | 401 | 401 | — | PASS |
| GET /api/items | valid token | 200, array | 200 | 0.31s | PASS |
| GET /api/items/:id | other user's id | 404 | 200 ⚠️ | — | FAIL (data leak) |
| POST /api/items | malformed JSON | 400 | 500 | — | FAIL |

Summary: 7 PASS / 2 FAIL
Critical: GET /api/items/:id returns other users' data — fix before anything else (see supabase-migration-writer for RLS).
Repro for each FAIL: <exact curl command>
Cleanup: test rows <ids> deleted ✅
```

## Pitfalls

- **Testing only with a valid token** — the sweep proves the API works but not that it's protected; the unauthenticated probe is the security test. Recovery: auth pass runs first and covers every endpoint, every time.
- **Expired token mid-sweep** — everything starts returning 401 and looks like mass failure. Recovery: when a previously-passing endpoint flips to 401, re-grab a fresh token and re-run from the first failure, not from scratch.
- **Cold start read as slow API** — first request 4s, rest 0.3s. Recovery: always run 5 and report median + cold separately; judge on the median.
- **Smoke-testing writes against production** — test rows in real users' views. Recovery: prefer preview; on prod, only obviously-labeled test data, record every created id, delete them (with confirm) before reporting done.
- **JSON "looks fine" but shape is wrong** — 200 with `{"items": null}` still breaks the frontend. Recovery: assert the shape, e.g. `curl -s ... | python3 -c "import json,sys; d=json.load(sys.stdin); assert isinstance(d['items'], list); print('shape ok')"`.

## Verification

- [ ] Every protected endpoint probed with no token AND a garbage token (401/403 both)
- [ ] Cross-user access attempted where multi-user data exists
- [ ] Every write endpoint probed with malformed input; zero 500s
- [ ] Latency reported as median-of-5 with cold start noted
- [ ] Every FAIL row includes its exact repro command
- [ ] Test data cleaned up (user confirmed the deletes); no tokens echoed into the transcript
