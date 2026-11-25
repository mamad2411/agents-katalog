---
name: security-headers-csp
description: Adds a Content Security Policy and the other protective HTTP headers, starting in report-only mode so nothing breaks before you tighten it.
---

# Security headers and CSP

Roll out in stages. Never enforce a new CSP before you have seen its reports.

## Steps

1. Inventory what the pages load: scripts, styles, fonts, images, frames, fetch and websocket targets, analytics and widgets. Note every inline script and style.
2. Remove inline code where it is cheap. For what remains, use a per-response nonce (`script-src 'nonce-...' 'strict-dynamic'`) or hashes. Do not rely on `'unsafe-inline'` or `'unsafe-eval'` for scripts.
3. Draft the policy: `default-src 'self'`, then explicit `script-src`, `style-src`, `img-src`, `connect-src`, `font-src`, plus `object-src 'none'`, `base-uri 'none'`, `frame-ancestors 'self'` and `form-action 'self'`.
4. Ship it as `Content-Security-Policy-Report-Only` with a `report-to` endpoint or a log of violations. Run through the main user journeys and read the reports. Fix or allow each legitimate source narrowly. Wait for a representative period.
5. Switch to enforcing `Content-Security-Policy` only when reports are clean. Keep a report-only copy of the next stricter version.
6. Add the companions through the framework's middleware or server config:
   - `Strict-Transport-Security: max-age=31536000; includeSubDomains` (add `preload` only after confirming every subdomain serves HTTPS)
   - `X-Content-Type-Options: nosniff`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Permissions-Policy` turning off unused features
7. Test with a header scanner and a browser console check.

## Rules

- Do not paste a policy found online; build it from what the pages actually load.
- Keep policy in one place, in config.

## Report

The policy, the sources allowed and why, where it is set, and the steps remaining to enforce it.
