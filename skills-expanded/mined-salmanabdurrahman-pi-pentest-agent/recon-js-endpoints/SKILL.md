---
name: recon-js-endpoints
description: Endpoint extraction from JavaScript with scope-aware validation — normalize, deduplicate, categorize, and classify API endpoints discovered during JS analysis. Produces structured endpoint inventory for downstream vulnerability validation skills. Every discovered endpoint must pass scope validation before further testing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [endpoint-list, command-log, redacted-evidence, hypothesis-queue]
---

# JavaScript endpoint extraction — normalization, deduplication, and routing

Use this skill after `recon-js-analysis` to transform raw extracted URL patterns into a validated, deduplicated, and categorized endpoint inventory. Raw extraction from JS produces noisy output — relative paths, template literals with variables, duplicate patterns, and out-of-scope URLs. This skill normalizes, deduplicates, scope-validates, and classifies every endpoint so downstream vulnerability skills receive clean, actionable input. Active validation (sending requests to endpoints) requires authorization and scope validation.

## Required inputs

- Raw endpoint list from `recon-js-analysis` or equivalent JS extraction.
- Scope file with in-scope host patterns and out-of-scope exclusions.
- Authorization cache valid for all in-scope hosts.
- Rate limits for active endpoint validation (probing).

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load authorized URL patterns and method restrictions.
3. `pentest_agent_validate_target` for every unique host in the endpoint list.
4. `pentest_agent_check_authorization` before any active endpoint probing.
5. `pentest_agent_build_command` for dry-run argv preview of active probing commands.
6. `pentest_agent_execute_tool` for active probing — rate-limit enforcement.
7. `pentest_agent_append_evidence` with categorized endpoint inventory.

## Workflow

### Phase 1 — normalization

Convert raw extracted URL patterns into a canonical form suitable for deduplication and comparison.

1. **URL normalization rules** for every extracted string:
   - Add scheme if missing: relative paths → `https://<host>/`. If host is unknown, keep as relative and mark as `UNRESOLVED_HOST`.
   - Remove trailing slashes: `/api/users/` → `/api/users` (trailing slashes may indicate different routes in some frameworks — flag and keep both if uncertain).
   - Lowercase the path: `/API/Users` → `/api/users`.
   - Remove fragment identifiers: `/page#section` → `/page`.
   - Sort query parameters alphabetically: `?b=2&a=1` → `?a=1&b=2`.
   - Remove empty query parameters: `?a=&b=2` → `?b=2`.
   - Decode URL-encoded characters where safe: `%20` → space, `%2F` → `/` (but be conservative — some encoded characters are meaningful).
   - Strip common tracking parameters that don't affect routing: `utm_source`, `utm_medium`, `utm_campaign`, `fbclid`, `gclid`, `ref`, `source`.
2. **Host resolution**:
   - If the URL is relative (`/api/users`), associate it with the source JS file's origin host.
   - If the URL is absolute and the host differs from the known target, flag as `EXTERNAL_HOST` and do not probe unless scope includes third-party endpoints.
   - If the URL contains a variable/parameter token (`/api/users/:id`, `/api/users/${userId}`, `/api/users/<id>`), normalize to a parameterized form: `/api/users/{id}`.
3. **Template literal and dynamic URL handling**:
   - Template literals with interpolated variables: extract the static prefix and mark as `PARAMETERIZED`.
   - Concatenated strings: collapse into a single pattern where the concatenation boundary is clear. If unclear, flag for manual review.

### Phase 2 — deduplication

Remove duplicate endpoints and group similar patterns.

1. **Exact deduplication**: `sort -u` on normalized URLs.
2. **Parameterized deduplication**: group endpoints that differ only by parameter values:
   - `/api/users/123` and `/api/users/456` → `/api/users/{id}` (2 instances)
   - If the same parameterized pattern appears 3+ times with different values, mark as `HIGH_CONFIDENCE` — this is a genuine parameterized route.
3. **Method inference**: group endpoints by their likely HTTP method based on context:
   - `fetch()` with no second argument → GET (default)
   - `fetch(url, {method: 'POST', body: ...})` → POST
   - `axios.get(url)` → GET
   - `axios.post(url, data)` → POST
   - `axios.put(url, data)` → PUT
   - `axios.delete(url)` → DELETE
   - `axios.patch(url, data)` → PATCH
   - If method cannot be inferred, mark as `GET` (the safe default for probing) and flag as `UNKNOWN_METHOD`.
4. **Dedup output**: produce a JSON inventory:

```json
[
  {
    "pattern": "/api/v1/users/{id}",
    "method": "GET",
    "instances": 4,
    "sources": ["main.abc123.js:234", "main.abc123.js:891"],
    "host": "api.TARGET.COM",
    "confidence": "high",
    "category": "CRUD"
  }
]
```

### Phase 3 — categorization and classification

Assign each endpoint to a vulnerability-relevant category that determines which downstream skill should test it.

1. **Category taxonomy**:
   | Pattern | Category | Route to skill |
   |---|---|---|
   | `/api/*/login`, `/api/*/auth`, `/api/*/signin` | Authentication | `auth-workflow` |
   | `/api/*/register`, `/api/*/signup` | Registration | `auth-workflow` |
   | `/api/*/reset-password`, `/api/*/forgot` | Password reset | `auth-password-reset` |
   | `/api/*/users/{id}`, `/api/*/profile/{id}` | IDOR candidate | `access-idor` |
   | `/api/*/search?q=`, `/api/*?query=` | Search/query | `vuln-xss`, `vuln-sqli` |
   | `/api/*/upload`, `/api/*/import` | File upload | `vuln-file-upload` |
   | `/api/*/redirect?url=`, `/api/*/goto?target=` | Open redirect | `vuln-open-redirect` |
   | `/api/*/proxy?url=`, `/api/*/fetch?src=` | SSRF candidate | `vuln-ssrf` |
   | `/api/*/download?file=`, `/api/*/view?path=` | Path traversal | `vuln-path-traversal`, `vuln-lfi-rfi` |
   | `/api/*/export`, `/api/*/report` | Data export | `vuln-sensitive-exposure` |
   | `/api/*/admin/*`, `/api/*/manage/*` | Admin/privileged | `access-bfla` |
   | `/graphql` | GraphQL | `enum-graphql` |
   | `/api/*/webhook`, `/api/*/callback` | Webhook/SSRF | `vuln-ssrf` |
   | `/api/*?id=`, `/api/*?user_id=` | ID-based query | `access-idor`, `vuln-sqli`, `vuln-nosql` |
   | `/api/*/invite`, `/api/*/share` | Multi-tenant | `access-tenant-isolation` |
   | `/api/*/checkout`, `/api/*/payment` | Business logic | `business-logic` |
   | `/api/*/batch`, `/api/*/bulk` | Mass assignment | `access-mass-assignment` |

2. **Priority assignment**:
   - **Priority 1** (test first): unauthenticated admin endpoints, direct object references with predictable IDs, file upload/download without extension validation, GraphQL endpoints without query depth limits, open redirect endpoints with `url=` parameter.
   - **Priority 2** (test second): authenticated IDOR candidates, search endpoints without CSRF, password reset with token in URL, batch endpoints with array inputs.
   - **Priority 3** (test last): read-only endpoints, static content, CDN-hosted assets.

3. **Out-of-scope filtering**: remove any endpoint whose host is out-of-scope or whose path matches an out-of-scope pattern. Record count of filtered endpoints.

### Phase 4 — active validation (gated)

Optionally probe discovered endpoints to verify they exist and collect response metadata.

1. **HTTP probing of categorized endpoints** (one request per pattern):
   - Use the most common method for the endpoint (GET by default, POST where clearly indicated).
   - Send a minimal, non-malicious request — no payloads, no fuzzing, no injection attempts.
   - `curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download}" "https://TARGET.COM/api/v1/users"`
   - Record: HTTP status, Content-Type, response size, redirect location (if 3xx), and any error messages in the response body.
2. **403/401 classification**:
   - 401: authentication required but endpoint exists.
   - 403: authorization denied (the endpoint exists and the server acknowledges it, but access is forbidden — more information-leaky than a 404).
   - 404: endpoint does not exist or is hidden.
3. **Do not probe beyond existence verification**: no fuzzing, no parameter tampering, no auth bypass attempts. This phase confirms the endpoint inventory; active validation of vulnerabilities is handled by the routed skills.

## Decision points

- **Endpoint responds with 401 but scope includes authentication testing**: hand off to `auth-workflow` with the endpoint marked as "auth-required, endpoint confirmed."
- **Endpoint responds with 200 and returns data without authentication**: UNVERIFIED — the endpoint may be publicly accessible, or it may have session-based auth not triggered by a single curl. Do not assume it's vulnerable. Flag as `hypothesis-needs-validation`.
- **Endpoint returns 500 with stack trace**: the endpoint is broken AND leaking internal information. Flag as HIGH finding — information disclosure through error messages.
- **Hostname cannot be resolved to a known scope entry**: flag as `UNKNOWN_HOST`. Do not probe. Escalate to operator for scope clarification.
- **Endpoint count exceeds 1,000 after dedup**: the target has a large API surface. Prioritize by category (admin/IDOR/file-upload first). Do not attempt to probe all endpoints — this would exceed reasonable rate limits.

## Prohibited behavior

- Sending any HTTP request to an endpoint whose host is not scope-validated.
- Fuzzing, injection testing, or auth bypass attempts during endpoint validation — this is mapping, not exploitation.
- Probing unauthenticated admin endpoints without explicit scope permission for admin-access testing.
- Sending requests with malicious payloads, even "safe" ones like `' OR 1=1--` — these can trigger WAF/IDS.
- Automating registration, login, or password-reset flows during endpoint validation.

## Stop conditions

- All endpoints return 404 → the JS references endpoints that are not deployed on the live server, or the endpoints require specific headers/sessions not provided. Document and hand off for authenticated testing.
- WAF blocks probes with CAPTCHA or JavaScript challenge → stop, document WAF presence.
- Rate-limited by target (429 responses) → stop, reduce rate, document threshold.
- `pentest_agent_validate_target` rejects the host → stop probing that host.

## Evidence

Produce a structured JSON endpoint inventory with normalization, dedup, categorization, priority, and validation status. Evidence template:

```text
Endpoint extraction for: TARGET.COM
Raw URLs extracted: 1,234 (from 24 JS files)
After normalization: 892
After deduplication: 203 unique endpoint patterns
After scope filtering: 187 in-scope, 16 out-of-scope (filtered)

Category breakdown:
  Authentication: 7 (2 login, 3 register, 2 password-reset)
  IDOR candidate: 34 (/api/users/{id}, /api/orders/{id}, /api/profile/{id})
  Search/query: 12
  File upload: 4
  Open redirect: 3
  SSRF candidate: 5 (/api/proxy, /api/fetch, /api/webhook)
  Path traversal: 8 (/api/download, /api/view, /api/export)
  Admin/privileged: 9 (/api/admin/*, /api/manage/*)
  GraphQL: 1 (/graphql)
  Business logic: 15 (/api/checkout, /api/cart, /api/apply-coupon)
  Mass assignment: 3 (/api/users/batch, /api/orders/bulk)
  Other/read-only: 86

Priority breakdown:
  Priority 1: 23 endpoints (admin, redirect, file upload, proxy, download)
  Priority 2: 78 endpoints (IDOR, search, business-logic)
  Priority 3: 86 endpoints (read-only, static)

Active validation: 187 probed, 89 (200), 34 (401), 23 (403), 18 (404), 12 (500), 11 (timeout)
  [HIGH] /api/admin/users returns 500 with Java stack trace — information disclosure
  [INFO] /api/v2/auth/login returns 200 (v2 API active, v1 may be deprecated)
```

Redact API keys, tokens, session IDs, and any PII from endpoint URLs and response snippets. Redact internal hostnames not in public DNS.

## Report handoff

1. Export the categorized endpoint inventory as structured JSON to `recon-js-endpoints.json`.
2. Hand off Priority 1 endpoints immediately to their respective vulnerability skills.
3. Hand off authenticated endpoints (401 responses) to `auth-workflow` with session-auth instructions.
4. `pentest_agent_record_finding` for: information-disclosure via error messages, exposed admin endpoints, undocumented API versions.
5. Explicitly note: all endpoint probing used minimal non-malicious requests, no injection or fuzzing was performed, all hosts were scope-validated, and out-of-scope endpoints were filtered before probing.
