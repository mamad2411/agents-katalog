---
name: cors-credentialed-requests
description: >
  Authorized assessment and hardening of credentialed CORS: Access-Control-Allow-Credentials
  with cookies or TLS client certs, forbidden ACAO *, Origin allowlists, null origin, simple
  vs preflight requests, and browser PoC requirements. Use when ACAC is true, credentialed
  cross-origin fetch/XHR, or cookie-authenticated SPA/API origin splits are in scope.
---

# CORS Credentialed Requests

## Scope And Authorization

- **In scope:** APIs and browsers apps you own or have written permission to test for CORS misconfiguration.
- **Out of scope:** Using credentialed CORS bugs on third-party sites without authorization; stealing real user sessions outside agreed PoC accounts.
- Prefer staging with test accounts; use synthetic Origins you control for PoCs.
- Redact cookies, tokens, and `Set-Cookie` values in reports.
- Pair fixes with `code-quality-standards` and CSRF defenses when cookies authenticate state-changing methods.

## When To Use

- `Access-Control-Allow-Credentials: true` appears on API responses.
- SPA on `https://app.example` calls API on `https://api.example` with `credentials: 'include'`.
- Investigating reflected `Access-Control-Allow-Origin` (ACAO) equal to request `Origin`.
- Distinguishing “CORS * without credentials” (often lower impact) from **credentialed** misconfig (high impact).
- Validating that browsers block `ACAO: *` combined with `ACAC: true`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Broad CORS misconfig catalog / checklist | `cors-security-checklist` or `cors-cross-origin-misconfiguration` |
| null Origin specifics | `cors-null-origin-deny` |
| Preflight cache max-age design | `cors-preflight-cache` / `cors-preflight-cache-design` |
| CSRF token design | `csrf-cross-site-request-forgery` |
| COOP / link opener | `cross-origin-opener-policy`, `coop-noopener-links` |
| Implementation quality baseline | `code-quality-standards` |

## Browser rules (credentialed CORS)

| Rule | Correct behavior | Failure mode |
| --- | --- | --- |
| ACAO with credentials | Must be **explicit single origin**, not `*` | Reflecting arbitrary Origin + ACAC true → readable responses with cookies |
| ACAC | `true` only when cookies/client certs needed | Unnecessary ACAC expands impact of any Origin bug |
| Allow-Headers / Methods | Echo only needed values on preflight | `*` or mirror of attacker-supplied ACRH |
| Vary | `Vary: Origin` when ACAO varies | Cache poisoning / wrong ACAO served |
| Cookies | `SameSite`, `Secure`, `Path` still apply | CORS fix alone does not replace CSRF controls |

**Simple vs preflight:** credentialed `GET`/`POST` with “simple” Content-Types may skip preflight; still check actual GET responses for ACAO/ACAC, not only OPTIONS.

## Workflow

### 1. Confirm scope and success criteria

1. List API hosts, SPA origins, auth mode (cookie session vs Bearer in JS).
2. If auth is **Bearer in `Authorization` header only** (no cookies), credentialed CORS impact differs — document that; still test ACAC if present.
3. Success for hardening: allowlist of exact origins; never reflect unvalidated Origin; ACAC only where required; automated regression tests.

### 2. Inventory CORS behavior

```bash
API='https://api.example.local/v1/me'
# Untrusted origin + credentialed probe (authorized target only)
curl -sSI -X GET "$API" \
  -H 'Origin: https://evil.example' \
  -H 'Cookie: session=REDACTED_TEST_COOKIE'

curl -sSI -X OPTIONS "$API" \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET' \
  -H 'Access-Control-Request-Headers: content-type'
```

Record: `ACAO`, `ACAC`, `ACAH`, `ACAM`, `ACAH`/`Access-Control-Expose-Headers`, `Vary`, status code.

### 3. Baseline impact classification

| Observation | Typical severity (context-dependent) |
| --- | --- |
| ACAO reflects evil Origin + ACAC true + cookie auth + sensitive JSON | High — browser PoC can read responses |
| ACAO `*` + ACAC true | Browser blocks; fix still required for correctness |
| ACAO allowlist only first-party + ACAC true | Expected for cookie SPA/API split |
| ACAO reflect without ACAC; no secrets in body | Often low/info unless combined with other issues |
| null Origin accepted with ACAC | See `cors-null-origin-deny` |

### 4. Browser PoC requirements (authorized)

Server headers alone are not a complete demo for credentialed CORS — browsers enforce CORS.

```html
<!-- Host only on an origin you control; use test session cookies -->
<script>
fetch('https://api.example.local/v1/me', {
  method: 'GET',
  credentials: 'include',
  headers: { 'Accept': 'application/json' }
}).then(r => r.text()).then(console.log).catch(console.error);
</script>
```

1. Victim (test account) must be logged into API cookie scope; `SameSite=None; Secure` may be required for true cross-site — note SameSite Lax limitations for PoC.
2. Capture Network tab: request includes cookies; response readable only if ACAO matches page Origin and ACAC true.
3. Do not use real customer sessions.

### 5. Hardening patterns

#### Explicit allowlist (pseudo)

```js
const ALLOW = new Set(['https://app.example.com', 'https://admin.example.com']);
function applyCors(req, res) {
  const origin = req.headers.origin;
  if (origin && ALLOW.has(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Vary', 'Origin');
  }
  // Do not set ACAO at all for disallowed origins
}
```

Avoid:

```js
// BAD: reflects any Origin with credentials
res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
res.setHeader('Access-Control-Allow-Credentials', 'true');
```

Also avoid substring allowlists (`origin.endsWith('example.com')`) that permit `https://example.com.evil.tld` or `https://notexample.com` depending on check — use exact match or parseable origin equality.

### 6. Verify with evidence

```bash
# Disallowed origin: should NOT see ACAO=evil or should omit ACAO
curl -sSI -H 'Origin: https://evil.example' "$API" | rg -i 'access-control|vary'

# Allowed origin
curl -sSI -H 'Origin: https://app.example.com' "$API" | rg -i 'access-control|vary'

# Wildcard + credentials must not be shipped
curl -sSI -H 'Origin: https://app.example.com' "$API" | rg -i 'allow-origin|allow-credentials'
```

Add unit/integration tests that fail if Origin reflection returns for random hosts.

### 7. Observe and hand off

1. Log rejected Origins at debug level only; do not log full cookies.
2. Monitor for sudden allowlist expansions in config PRs.
3. Document interaction with CSRF (`SameSite`, methods, token header that forces preflight).
4. Route null Origin, preflight cache, and general checklist to sibling CORS skills.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| ACAO | Exact allowlist match | Reflect request Origin blindly |
| ACAC | Only for cookie/client-cert APIs | ACAC true on public anonymous CDN |
| Cache | `Vary: Origin` | CDN caches ACAO from first visitor Origin |
| PoC | Controlled origin + test cookie | Claiming critical without browser read proof |
| Allowlist | Parsed origin equality | `contains('example.com')` |
| CSRF | Tokens / SameSite still on | “CORS means no CSRF” |

## Output Checklist

- [ ] Auth mode (cookie vs header) documented
- [ ] OPTIONS and actual method responses captured for evil and allowlisted Origins
- [ ] ACAC necessity justified or removed
- [ ] No ACAO `*` with ACAC true in shipped config
- [ ] Browser PoC or explicit non-applicability (SameSite) noted
- [ ] `Vary: Origin` present when ACAO varies
- [ ] Regression tests for allowlist
- [ ] CSRF interaction reviewed
- [ ] Redacted evidence attached
- [ ] Residual risk (mobile WebViews, old browsers) noted

## Rules

- Authorized targets and test accounts only.
- Prefer fixing reflection bugs over relying on “browsers block *”.
- Credentialed CORS read of sensitive JSON is a confidentiality issue — report with browser evidence when possible.
- Do not disable CORS entirely as a “fix” for SPAs that need cross-origin cookies; use a correct allowlist or same-site deployment.
- Keep focus on **credentialed** request behavior; use sibling skills for null origin, preflight TTL, and full checklists.
