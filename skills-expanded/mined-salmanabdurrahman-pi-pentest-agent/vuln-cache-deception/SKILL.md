---
name: vuln-cache-deception
description: Web cache deception validation — test CDN/cache storage of authenticated responses via extension tricks, path manipulation, and delimiter injection without accessing other users' cached data.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Web cache deception — authenticated-content caching validation

Use this skill to test whether a CDN, reverse proxy, or application cache stores authenticated responses under cacheable URLs, then serves them to unauthenticated requesters. Focus on extension tricks, path delimiters, and cache-key analysis. Test only with tester-owned authenticated sessions — never access cached responses belonging to other users.

## Required inputs

- Written scope naming the target origin, CDN/proxy layer (if known), authorized test accounts, and explicit permission to test cache behavior on authenticated endpoints.
- A valid authenticated session (cookie or token) for a tester-owned test account. The session must access at least one authenticated page that returns user-specific content (profile, dashboard, settings, orders).
- Valid authorization cache for the target. Separate permission required if testing cache deception across tenant boundaries or on admin endpoints.
- Known CDN/provider (Cloudflare, Fastly, Akamai, CloudFront, Varnish, Nginx cache) if disclosed by the target.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — cache infrastructure fingerprinting

Identify the caching layer and its default behavior:
1. Request a known static resource (`/favicon.ico`, `/robots.txt`, `/style.css`).
2. Inspect response headers: `Cache-Control`, `Age`, `X-Cache`, `CF-Cache-Status`, `X-Varnish`, `Surrogate-Control`, `X-Served-By`.
3. Request the same static resource again and compare `Age` and cache-status headers.
4. Request the homepage without authentication and note cache headers.
5. Request an authenticated page (`/account`, `/profile`, `/dashboard`) with the test session and note cache headers — pay attention to `Cache-Control: private`, `no-store`, or `Vary: Cookie`.

Record baseline: which cache status values appear (HIT/MISS/EXPIRED/HIT-FOR-PASS), cache TTL on static assets, and whether authenticated pages already carry `private`/`no-store`.

### Phase 2 — sensitive endpoint inventory

Identify endpoints that return user-specific content and should never be publicly cached:
- `/account`, `/account/settings`, `/account/billing`;
- `/profile`, `/profile/edit`;
- `/dashboard`;
- `/orders`, `/orders/123`;
- `/api/me`, `/api/user`, `/api/account`;
- `/admin` (only if scope permits);
- `/inbox`, `/messages`;
- any endpoint that returns the authenticated user's name, email, or identifiers in the response body.

For each endpoint, record: URL, whether it returns user-specific content (yes/no), and current cache headers from the authenticated response.

### Phase 3 — deception URL construction

For each sensitive endpoint, construct deception URLs using extension and delimiter tricks:

```text
Origin: https://TARGET/account

Deception variants:
/account.css          — static extension appended
/account.js           — alternative static extension
/account.png          — image extension
/account.ico          — icon extension
/account.svg          — vector extension
/account.woff2        — font extension
/account/nonexistent.css  — extra path segment with static extension
/account;.css         — path-parameter delimiter (semicolon)
/account%3B.css       — URL-encoded semicolon
/account%00.css       — null byte (legacy bypass)
/account%0A.css       — newline injection
```

Rules:
- Never construct deception URLs for endpoints you cannot access authenticated.
- Never include another user's identifier or session in the deception URL.
- Test one variant per endpoint per cycle to avoid cache pollution.

### Phase 4 — authenticated priming and unauthenticated retrieval

For each deception URL:
1. **Prime**: request the deception URL with the test session cookie. Record the response status, `X-Cache` header, and `Age` header.
2. **Wait**: pause for 5-10 seconds (or the observed cache TTL if known).
3. **Retrieve**: request the same deception URL without any authentication cookie or token.
4. **Compare**: does the unauthenticated response contain the test user's content (name, email, account data)?

If the unauthenticated response contains user-specific content → cache deception confirmed. The cache stored an authenticated response under a URL that appears static and served it without authentication.

### Phase 5 — cache-key analysis

When deception succeeds, analyze what the cache key includes:
1. Vary the `Accept-Language` header — does it change the cached response?
2. Vary the `User-Agent` header — does it change the cached response?
3. Add custom headers (`X-Forwarded-Host`, `X-Original-URL`) — do they affect cache behavior?
4. Test whether the `Vary` response header lists `Cookie` — if not, the CDN ignores cookies in the cache key by design.
5. Document the root cause: the cache treats `<endpoint>.css` as a static resource, does not include the session cookie in the cache key, and the origin does not set `Cache-Control: private` on the authenticated response.

## Decision points

- **Stop at first confirmed deception**: one clean unauthenticated retrieval of authenticated content is sufficient proof. Do not enumerate all possible deception variants.
- **Downgrade when origin sets proper headers**: if all authenticated endpoints carry `Cache-Control: private` or `no-store`, the origin is correctly configured — document negative result.
- **Escalate on PII exposure**: if the cached response contains email, physical address, payment info, or government ID → critical finding.
- **Refuse cache poisoning crossover**: cache deception (reading cached data) is distinct from cache poisoning (injecting malicious data into cache). Do not pivot to poisoning without separate scope and authorization.

## Prohibited behavior

- Accessing cached responses belonging to other users, even if discoverable.
- Cache poisoning: injecting malicious headers, responses, or payloads into the cache.
- Cache busting or purging without explicit CDN provider authorization.
- Testing deception on endpoints that process payments, delete accounts, or modify sensitive state.
- Storing raw authenticated response bodies containing PII or tokens.

## Stop conditions

- Unauthenticated retrieval of authenticated content → finding confirmed, stop testing that endpoint class.
- All tested endpoints correctly serve `Cache-Control: private` → negative result, stop.
- CDN returns `Cache-Control: no-store, private` on all deception URLs → protected, stop.
- Rate limiting, CDN block, or detection-team contact.

## Evidence — deception matrix

For each tested endpoint, record:

```text
Endpoint: <URL>
Authenticated content: <yes | no (only generic UI)>
Deception URL: <constructed URL with extension/delimiter>
Primed with session: <yes> | response status: <200 | 30x | 40x>
Cache status after prime: <HIT | MISS | EXPIRED>
Unauthenticated retrieval status: <200 | 30x | 40x>
Unauthenticated body contains test-user content: <yes | no>
Content exposed: <username | email | order ID | ... | none>
Cache-key analysis: <Vary: Cookie absent | Cache-Control missing | CDN rule mismatch>
Impact: <none | auth content cached | PII cached>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an endpoint × deception-variant matrix. Include both positive and negative results. Never store: raw response bodies containing PII, session tokens, or other users' data.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, deception URL, content exposed, CVSS estimate (5.3–7.5 depending on PII exposure), and remediation guidance.
2. Reference the deception matrix.
3. Recommend: `Cache-Control: private, no-store` on all authenticated responses, `Vary: Cookie` to include session in cache key, CDN rule to bypass cache for authenticated paths, URL normalization to reject unexpected extensions on dynamic endpoints, and cache-deception tests in CI.
