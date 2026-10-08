---
name: sh-kb-csrf
description: "Knowledge base for finding Cross-Site Request Forgery - state-changing requests that rely only on ambient credentials (cookies) with no anti-CSRF token or SameSite protection. Use when hunting CSRF. CWE-352, OWASP A01:2021-Broken Access Control."
---

# Cross-Site Request Forgery (CSRF) - Hunter Knowledge Base

A logged-in victim's browser is tricked into sending a state-changing request; the app trusts the ambient
cookie and performs the action as the victim. Requires cookie-based auth and a missing anti-CSRF control.

## Preconditions to confirm first
1. The endpoint performs a **state change** (create/update/delete/transfer/settings).
2. Auth is via **ambient credentials** (session cookie / HTTP Basic), not a per-request header token that
   JS must attach (`Authorization: Bearer`) - pure Bearer-in-header APIs are generally not CSRF-able.
3. There is **no** effective anti-CSRF defense on that route.

## Sinks / patterns (grep targets)
State-changing route handlers (`POST`/`PUT`/`PATCH`/`DELETE`, or `GET` that mutates) that:
- lack CSRF middleware/decorator, or explicitly disable it: `csrf_exempt`, `@csrf.exempt`,
  `skip_before_action :verify_authenticity_token`, `csrf: false`, Spring `.csrf().disable()`,
  Express without `csurf`, `SameSite=None`/absent on the session cookie.
- Grep: `csrf_exempt|verify_authenticity_token|csrf().disable|csurf|SameSite|@csrf`.

## Detection recipe
1. From `codebase-map.json`, list state-changing endpoints and their auth mechanism.
2. Check the global CSRF posture: is protection enabled framework-wide? Then find per-route exemptions.
3. Check cookie flags: `SameSite=Lax/Strict` blocks most cross-site POSTs; `SameSite=None` re-opens it.
4. Confirm the endpoint doesn't already require a non-ambient token or a custom header (which forces a
   preflight and blocks simple cross-site requests).

## Payloads / PoC
- Auto-submitting form: an HTML page with `<form action="https://target/settings" method="POST">` and
  hidden inputs, plus `<script>document.forms[0].submit()</script>`; victim visiting it triggers the action.
- For JSON endpoints that accept `text/plain` or don't check content-type: a form with
  `enctype="text/plain"` crafting a JSON-ish body.
- GET-based state change: `<img src="https://target/delete?id=5">`.
- PoC = the victim, while logged in, loads the attacker page and the state change occurs.

## False-positive filters
- Anti-CSRF token required and validated (synchronizer token, double-submit cookie) on the route.
- `SameSite=Lax` (default in modern browsers) or `Strict` on the session cookie - mitigates most CSRF;
  note residual risk for top-level GET navigations under Lax.
- Auth is a header token the browser won't auto-attach cross-site (Bearer), not a cookie.
- Endpoint requires a custom header (forces CORS preflight) and CORS is not permissive.

## CWE / OWASP / severity
CWE-352. OWASP A01:2021. Severity by action impact: account/email/password change or money transfer ->
**high**; low-value toggles -> medium/low.

## Chaining hints
CSRF + `xss` (steal token then forge) ; CSRF to change email/password -> account takeover; CSRF to add an
attacker OAuth/app -> persistence; often combined with `access-control` to hit privileged actions.

## Mitigation
Enable framework CSRF protection on all state-changing routes (don't blanket-exempt); require a
synchronizer or double-submit token; set session cookies `SameSite=Lax`/`Strict` + `Secure`; prefer
non-ambient auth for APIs; require a custom header for JSON APIs and lock down CORS.
