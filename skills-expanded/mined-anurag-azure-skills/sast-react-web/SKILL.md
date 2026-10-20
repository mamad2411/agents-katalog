---
name: "sast-react-web"
description: "Static security testing for React web apps: XSS, secrets, CSP, dependency and auth hygiene. Use when reviewing React web security."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# SAST — React Web

- **XSS:** never `dangerouslySetInnerHTML` without sanitization (DOMPurify); no `eval`/`new Function`.
- **Secrets:** only `VITE_`-prefixed public config in the bundle; real secrets stay server-side.
- **CSP/headers:** ship a Content-Security-Policy; avoid inline scripts; `Referrer-Policy`, `X-Content-Type-Options`.
- **Auth:** tokens in httpOnly cookies where possible; if in memory, clear on logout; CSRF protection for cookie auth.
- **Transport:** HTTPS only; validate redirect targets.
- **Dependencies:** `npm audit` clean of high/critical; pinned versions.
