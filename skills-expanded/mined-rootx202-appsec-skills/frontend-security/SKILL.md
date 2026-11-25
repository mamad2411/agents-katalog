---
name: frontend-security
description: Frontend/client-side security auditor covering React, Next.js, Vue, and general SPA/SSR concerns — server components, server actions, middleware, cookies, CSP headers, hydration, and client-side XSS. Use when reviewing a frontend application's client-side and edge-runtime security specifically, for any project.
---

# Frontend Security — Client-Side & Rendering Layer Auditor

A specialized skill for auditing frontend security and the boundary between server and client rendering.

## When to use this
- Any React/Next.js/Vue/SPA project
- Reviewing Server Actions / Server Components / Middleware (Next.js) or equivalents
- Suspected leakage of sensitive data to the client, or CSP/XSS concerns

## Core Checks

### Server vs. Client Boundary
- Make sure sensitive data (secrets, keys, other users' data) is never passed as props from a server-rendered component into a client component without necessity — anything that reaches a client component is visible in the browser bundle/network.
- Environment variables: only variables explicitly intended for the client (e.g. prefixed `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`) should be exposed; check that a real secret wasn't mistakenly given that prefix.

### Server Actions / Server-Side Handlers
- Every server action is effectively an API endpoint — it must contain its own authentication and authorization checks, not rely on being "hidden" in the UI.
- Validate inputs inside the handler itself always, even if client-side validation also exists (the client is never trusted).

### Middleware
- Confirm route-protection middleware (e.g., session checks) actually covers every path it's meant to via the correct matcher/config — check for accidentally unprotected routes.

### Cookies & Security Headers
- Session cookies: `HttpOnly`, `Secure`, `SameSite`
- Baseline security headers present: `Content-Security-Policy`, `X-Frame-Options`/`frame-ancestors`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`
- CSP avoids `unsafe-inline`/`unsafe-eval` unless strictly necessary

### XSS in Component Frameworks
- Any use of `dangerouslySetInnerHTML`/`v-html`/raw DOM injection — content must be sanitized (e.g., DOMPurify) before use
- User-supplied URLs rendered as links (`href={userInput}`) — reject `javascript:` scheme

### CSRF
- Confirm any traditional state-changing endpoint (POST/PUT/DELETE) is protected by a CSRF token or an appropriate SameSite-cookie strategy, especially outside frameworks that provide built-in protection for their own action mechanism.

### Hydration & SSR Data Leakage
- Confirm no per-user personalized data is rendered on a page that could be shared through caching (CDN/edge cache) across different users — a common cross-user data-leak vector in SSR apps.

## Report Format
```
Component/Route: [path]
Issue: [problem]
Severity: Critical/High/Medium/Low
Evidence: [code]
Impact: [impact]
Fix: [suggested change]
```

## Rules
- Never treat client-side validation alone as sufficient — always require a matching server-side check.
- For purely aesthetic/visual concerns (not security), defer to a design skill instead of conflating the two.
