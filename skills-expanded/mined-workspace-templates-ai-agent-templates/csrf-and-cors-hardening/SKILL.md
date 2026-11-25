---
name: csrf-and-cors-hardening
description: Sets up CORS and CSRF protection that fits how your app authenticates, with cookies or bearer tokens, and removes the wildcard shortcuts.
---

# CSRF and CORS hardening

First decide how the app authenticates. The answer decides everything else.

## Steps

1. Identify the credential: cookie session, bearer token in a header, or both. List the state-changing routes (POST, PUT, PATCH, DELETE) and any GET that changes state.
2. CORS policy:
   - Allowlist exact origins from configuration. Never reflect the request `Origin` without checking it against that list, and never combine `*` with credentials.
   - Set `Access-Control-Allow-Credentials: true` only if cookies must cross origins.
   - Limit methods and headers to what the client uses, set `Vary: Origin`, and cache preflights with `Max-Age`.
3. Cookie sessions need CSRF defence. Layer these:
   - Cookie flags `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict` for sensitive apps).
   - A per-session CSRF token checked on every unsafe method, or the double-submit cookie pattern with a signed value.
   - Verify `Origin` or `Sec-Fetch-Site` on unsafe requests.
4. Bearer-token APIs that never read cookies are not exposed to CSRF. Confirm no route accepts a cookie as a fallback.
5. Make GET handlers safe: no state changes.
6. Add tests: a request from a foreign origin is refused; a POST without the token returns 403; preflight returns only the allowed list.

## Rules

- Do not "fix" a CORS error by widening the policy before you know which origin is calling.
- Use the framework's maintained middleware.

## Report

Auth model found, policy before and after, files changed, tests added.
