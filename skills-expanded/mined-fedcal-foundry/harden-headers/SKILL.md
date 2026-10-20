---
name: harden-headers
description: Set HTTP security headers and cookie flags correctly - a Content-Security-Policy without unsafe-inline including the nonce or hash migration path, HSTS, COOP/COEP/CORP, Referrer-Policy, Permissions-Policy, and SameSite/__Host- cookies - and roll CSP out in report-only mode, read the violation reports, and only then enforce. Use when adding security headers, when a review flags a missing or weak header, or when a CSP has been stuck in report-only or weakened with unsafe-inline.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
model: sonnet
effort: medium
user-invocable: true
argument-hint: "<app path or URL> [--audit] [--rollout]"
metadata:
  foundry.vertical: dev
  foundry.io: "app config -> header policy + report-only rollout plan + tests"
license: Apache-2.0
---

# Harden HTTP response headers and cookies

Headers are cheap, verifiable and permanently regress-able. This skill produces a policy,
a rollout that will not break the application, and tests that fail when a header changes.

Standards: OWASP ASVS 5.0 V3 Web Frontend Security · W3C Content Security Policy Level 3 ·
RFC 6797 (HSTS) · RFC 6265 and the `rfc6265bis` work for `SameSite` and cookie prefixes
(still an Internet-Draft — verify its status before citing it as an RFC) · W3C
Referrer Policy · W3C Permissions Policy · HTML standard (COOP) and Fetch standard
(COEP/CORP) · W3C Fetch Metadata Request Headers · W3C Reporting API ·
CWE-1021, CWE-693, CWE-614, CWE-1004, CWE-1275, CWE-319.

Headers are defence in depth. A CSP does not fix an XSS sink and HSTS does not fix a mixed
-content bug. Fix the primary defect; add these so the next one is contained.

## Step 0 — Audit what is actually sent

Measure before changing. The effective headers are what the *last* proxy sends, not what
the application code sets.

```bash
curl -sSI https://app.example.com/ | sed -n '1,40p'
curl -sSI https://app.example.com/api/health
curl -sS -D- -o /dev/null https://app.example.com/login   # login page often differs
```

Check at least: the landing page, an authenticated page, an API route, a static asset, an
error page (4xx/5xx often bypass the middleware) and a redirect response. Record the
current value of every header in the table below, then find where each is set:

```bash
rg -n 'Content-Security-Policy|Strict-Transport-Security|X-Frame-Options|Referrer-Policy|Permissions-Policy|Cross-Origin-|X-Content-Type-Options|SameSite|Set-Cookie'
rg -n 'helmet|SecurityHeaders|headersSecurityConfig|add_header|Header always set|response.headers'
```

Two failure modes to catch here: headers set in the application *and* the proxy, with the
proxy winning; and headers absent on error responses because the middleware runs after the
handler.

## Target policy

| Header | Target value | Why | Standard |
|---|---|---|---|
| `Content-Security-Policy` | see below — nonce-based, no `unsafe-inline` for scripts | contains injected script | CSP L3; ASVS 5.0 V3 |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` (add `preload` only with intent) | forces HTTPS after first visit | RFC 6797; CWE-319 |
| `X-Content-Type-Options` | `nosniff` | stops MIME confusion on uploads and JSON | Fetch standard |
| `Referrer-Policy` | `strict-origin-when-cross-origin`, or `no-referrer` for sensitive apps | stops URL leakage of ids and tokens | W3C Referrer Policy |
| `Permissions-Policy` | deny everything unused: `camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()` | shrinks the API surface of the page and of embedded frames | W3C Permissions Policy |
| `Cross-Origin-Opener-Policy` | `same-origin` | severs the opener relationship; a prerequisite for cross-origin isolation | HTML standard |
| `Cross-Origin-Embedder-Policy` | `require-corp` or `credentialless` — **only if you need cross-origin isolation** | required for `SharedArrayBuffer` / precise timers | Fetch standard |
| `Cross-Origin-Resource-Policy` | `same-origin` for private resources, `cross-origin` for a public CDN asset | stops other origins embedding your resources | Fetch standard |
| `X-Frame-Options` | `DENY` — legacy only; `frame-ancestors` supersedes it | clickjacking (CWE-1021) | superseded by CSP L3 |
| `Cache-Control` | `no-store` on authenticated responses | keeps private data out of shared and browser caches | RFC 9111 |
| `X-XSS-Protection` | omit it, or `0` | the legacy auditor is removed from current browsers and its filter introduced bugs | — |

`Strict-Transport-Security` warnings: `includeSubDomains` applies to every subdomain
including ones you do not control operationally; inventory them first. `preload` is
effectively irreversible on a human timescale — removal from the preload list takes months
to propagate. Do not add `preload` to a domain that still serves anything over HTTP.

`Cross-Origin-Embedder-Policy: require-corp` breaks every cross-origin resource that does
not opt in with CORP or CORS. Do not enable it as generic hardening; enable it only when a
feature requires cross-origin isolation, and roll it out with
`Cross-Origin-Embedder-Policy-Report-Only` first.

## Content-Security-Policy

### Target

```
default-src 'self';
script-src 'self' 'nonce-{RANDOM}' 'strict-dynamic';
style-src 'self' 'nonce-{RANDOM}';
img-src 'self' data:;
font-src 'self';
connect-src 'self' https://api.example.com;
frame-ancestors 'none';
form-action 'self';
base-uri 'none';
object-src 'none';
require-trusted-types-for 'script';
report-uri /csp-report;
report-to csp-endpoint;
```

Notes that matter:

- **`'unsafe-inline'` in `script-src` disables the main benefit of CSP.** A policy that
  keeps it is a hardening gesture, not a control. Removing it is the whole job; the rest of
  the header is easy.
- **`'strict-dynamic'`** lets a nonce-trusted script load further scripts, which is what
  makes bundlers and module loaders workable. When present, host allow-lists in `script-src`
  are ignored by supporting browsers — keep `'self'` and a host list only as a fallback for
  older ones, and know they are inert where `'strict-dynamic'` is honoured.
- **`base-uri 'none'`** and **`object-src 'none'`** are cheap and close well-known bypasses;
  omitting them is a common reason a nonce-based policy is still bypassable.
- **`frame-ancestors`** replaces `X-Frame-Options` and is the value that actually applies
  where both are present.
- **Host allow-lists are weak.** Any allowed host serving a JSONP endpoint, a user-content
  path, or an outdated framework bundle re-opens the policy. Prefer nonces over host lists.
- **`report-uri` is deprecated but still the most widely honoured**; send both `report-uri`
  and `report-to` with a `Reporting-Endpoints` header during the transition, and verify what
  your browser population actually delivers rather than assuming.
- **Trusted Types** (`require-trusted-types-for 'script'`) is the strongest available
  control against DOM XSS, but is not universally supported — deploy it report-only first
  and keep a fallback. Check current support rather than trusting any support claim here.

### Migration path away from `unsafe-inline`

Detailed procedure in `references/csp-rollout.md`. In short:

1. **Inventory inline code.** Find every inline `<script>`, inline `<style>`, `on*=`
   attribute, `javascript:` URL, `eval`/`new Function`, and `innerHTML` sink:
   ```bash
   rg -n '<script(?![^>]*src=)|on(click|load|error|submit|change)=|javascript:' --glob '*.html' --glob '*.jsx' --glob '*.tsx' --glob '*.vue'
   rg -n 'eval\(|new Function\(|innerHTML|outerHTML|insertAdjacentHTML|document\.write'
   ```
2. **Choose nonce or hash per artifact.** Nonce for anything server-rendered (needs a fresh
   CSPRNG value per response and a template that can inject it). Hash for a fixed set of
   inline scripts in a static build (no per-request work, but every edit changes the hash —
   generate it in the build, never by hand).
3. **Externalise what cannot take a nonce.** Inline event-handler attributes (`onclick=`)
   cannot carry a nonce at all: move them to `addEventListener` in an external file. This is
   usually the bulk of the migration work.
4. **Bootstrap data**: replace inline `window.__DATA__ = {...}` with
   `<script type="application/json" id="data">` read via `textContent`, or a nonced script.
5. **Third-party tags** (analytics, tag managers, chat widgets) are where the migration
   dies. A tag manager that injects arbitrary inline script is incompatible with a strict
   CSP by design. Decide explicitly: nonce-propagate if the vendor supports it, isolate the
   tag in a sandboxed iframe on a separate origin, or drop it. Record the decision.
6. **Styles last.** `style-src 'unsafe-inline'` is a materially smaller risk than the script
   equivalent; if the CSS-in-JS library cannot take a nonce, keep it temporarily, note it as
   an accepted gap with a date, and do not let it block removing `unsafe-inline` from
   `script-src`.

The nonce must be a fresh CSPRNG value per response (CWE-330 if not), at least 128 bits,
and never cached. A page cached by a CDN with its nonce is a policy that no longer applies.

### Report-only rollout

Never enforce a new CSP directly. Sequence:

1. Ship `Content-Security-Policy-Report-Only` with the *target* policy and a report
   endpoint. Change nothing else.
2. Collect for at least one full business cycle — a week minimum, longer if there are
   weekly or monthly batch pages. Cover the whole application, not just the landing page.
3. Triage reports (see `references/reading-csp-reports.md`): separate genuine application
   violations from browser-extension noise, which is the majority of raw report volume and
   which you must filter out or the signal is unusable.
4. Fix the application violations. Re-measure until the report rate for first-party sources
   is stable and near zero.
5. Enforce, keeping the report endpoint live. Keep a second, stricter policy in report-only
   alongside the enforced one — that is how you ratchet without risk.
6. Add a test asserting the exact enforced header so a future middleware change cannot
   silently weaken it.

Both headers can be sent at once: one enforced policy plus one report-only policy is the
standard ratchet pattern.

## Cookies

| Attribute | Value | Consequence of omitting |
|---|---|---|
| `Secure` | always | cookie sent over plaintext (CWE-614, CWE-319) |
| `HttpOnly` | on session and token cookies | script can read the session (CWE-1004) |
| `SameSite` | `Lax` default; `Strict` for high-value; `None` **only** with `Secure` and a real cross-site need | CSRF exposure (CWE-1275, CWE-352) |
| `Path` | `/` with the `__Host-` prefix | scope creep |
| `Domain` | omit — omitting it makes the cookie host-only | a subdomain, including one you do not control, can read it |
| Prefix | `__Host-` for session cookies | no protection against a subdomain overwriting the cookie |
| Lifetime | session cookie or a short `Max-Age`, with server-side expiry too | client-side expiry is decoration (CWE-613) |

`__Host-` requires `Secure`, `Path=/` and **no** `Domain`, and forbids a subdomain from
setting it. It is the strongest binding available for a session cookie and costs nothing.
`__Secure-` is the weaker fallback where a `Domain` is genuinely required.

`SameSite=Lax` does not protect against a same-site attacker (any subdomain, any origin with
a shared registrable domain). It is not a substitute for CSRF tokens on high-value
state-changing operations. Where available, check `Sec-Fetch-Site` as an additional signal.

## Where to set them

One place, applied to every response including errors and redirects. In order of preference:
application middleware (travels with the app, testable in the test suite) → reverse
proxy/ingress → CDN. Setting the same header at two layers is the most common cause of a
policy that is correct in code and wrong in production. Detect duplicates:

```bash
curl -sSI https://app.example.com/ | grep -ci 'content-security-policy'
```

Anything above 1 for an enforced policy is a defect.

## Verification and regression protection

- Automated test asserting the **exact** header string on: an anonymous page, an
  authenticated page, an API route, a 404 and a 500. Assert equality, not presence.
- A cookie test asserting `Secure; HttpOnly; SameSite` and the `__Host-` prefix on the
  session cookie.
- Evaluate the CSP with a policy evaluator (for example Google's CSP Evaluator) and record
  the residual weaknesses rather than deleting the report.
- Add a check to CI so the headers are part of the build contract, not a one-off change.

Commands and test skeletons per stack: `references/verify-headers.md`.

## Exit criteria

- [ ] Every header in the target table has a decided value — set, or explicitly declined
      with a reason (COEP in particular).
- [ ] CSP contains no `unsafe-inline` and no `unsafe-eval` in `script-src`, or the exception
      is recorded with an owner and a date.
- [ ] CSP includes `object-src 'none'`, `base-uri 'none'`, `frame-ancestors` and
      `form-action`.
- [ ] Nonces are per-response, CSPRNG-generated, and not cached by any layer.
- [ ] Report-only ran for at least one full business cycle with extension noise filtered and
      first-party violations driven to a stable near-zero rate before enforcement.
- [ ] Exactly one enforced CSP header is present in the production response.
- [ ] Session cookies carry `__Host-`, `Secure`, `HttpOnly` and an explicit `SameSite`.
- [ ] Header assertions exist in CI for anonymous, authenticated, API, 404 and 500 responses.
- [ ] HSTS `preload` added only after confirming no subdomain requires plaintext HTTP.

## What this skill deliberately does not cover

- **XSS remediation itself.** Headers contain the consequence; the sink still needs fixing.
  Use the `security-review` skill.
- **CORS configuration.** A different problem with an overlapping vocabulary — see
  `security-review` class 13.
- **TLS configuration**: cipher suites, certificate management, OCSP. Ops vertical.
- **WAF rules, bot management and rate limiting.**
- **Browser support matrices.** Support changes; verify against current data rather than
  trusting any table, including this one.
- **Subresource Integrity, `Clear-Site-Data`, `Network Error Logging` and email-domain
  headers**, which are worthwhile but out of scope here.

## Degradation

- No live URL: audit from configuration only, and state that the effective headers were not
  observed. Proxy and CDN layers can override everything you found.
- No report endpoint available: use a hosted collector or log the report body server-side;
  do not skip report-only. Enforcing an unmeasured CSP breaks production.
- Static site with no server: set headers at the CDN/host, use hashes rather than nonces,
  and generate the hashes in the build.
- `superpowers` present: use `superpowers:verification-before-completion` before declaring
  the rollout done — "the header is in the config" is not the same as "the header is in the
  response".

## References

- `references/csp-rollout.md` — full report-only rollout, nonce plumbing per stack, and the
  third-party-tag decision.
- `references/reading-csp-reports.md` — report payload fields, filtering extension noise,
  triage rules, and when to enforce.
- `references/header-reference.md` — per-header syntax, values and pitfalls.
- `references/verify-headers.md` — curl checks and test skeletons per stack.
