---
name: enum-headers-cookies
description: HTTP response header and cookie security audit across all in-scope endpoints. Covers security header presence, server information leakage, cookie attribute analysis, cache-control directives, and client-side security policy enforcement. Passive-first header collection with active probing for cookie behavior classification.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, header-audit, cookie-attribute-matrix, info-leakage-report]
---

# Enum headers and cookies

Use this skill to audit HTTP response headers and cookie attributes across every in-scope endpoint. Response headers define the server's security posture: they tell the browser how to handle content, framing, caching, and cross-origin requests. Cookies carry session state; their attributes define the attack surface for session hijacking, fixation, and cross-site request forgery. This skill systematically collects, classifies, and reports on both, flagging missing protections, information leakage, and misconfigurations.

## Required inputs

- Validated target list with all in-scope endpoints (home page, login, API paths, static assets, error pages, redirect targets).
- Scope file defining allowed testing methods and rate limits.
- Authorization cache valid for all in-scope hosts.
- Session tokens at multiple privilege levels, if available, for cookie-attribute comparison across tiers.
- Known cookie names from documentation or prior recon for targeted analysis.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every endpoint before contact.
3. Use `pentest_agent_check_authorization` before any request that includes session cookies or targets authenticated endpoints.
4. Use `pentest_agent_build_command` for dry-run preview when using catalog tools for bulk header capture or cookie analysis.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for header audit tables, cookie matrices, and information-leakage reports.

## Workflow

### Phase 1 — Baseline header collection

Collect response headers from every in-scope endpoint, varying method and authentication state.

- For each endpoint, send a GET request and capture all response headers. Record the endpoint URL, HTTP status code, and the full header set.
- For endpoints that accept POST, send a POST request with a benign body and capture headers. POST responses often differ from GET responses in caching and security headers.
- For authenticated endpoints, send requests both without authentication and with each available privilege tier. Authentication state commonly changes the server response headers.
- For error pages (404, 500), trigger and capture headers. Error responses frequently omit security headers that normal responses include.
- For redirect targets, capture the intermediate 301/302 response headers, not just the final destination headers. Redirect responses define HSTS upgrade behavior and cookie Domain scoping.

### Phase 2 — Security header audit

Audit each endpoint for the presence and correctness of security headers.

- Check for `Strict-Transport-Security` (HSTS). Required on all HTTPS endpoints. Flag if `max-age` is less than 31536000 (one year), if `includeSubDomains` is absent on the apex domain, or if `preload` is missing on production sites. Flag if the header is absent entirely on any HTTPS response.
- Check for `X-Content-Type-Options: nosniff`. Required on all endpoints serving user-controlled content or uploads. Flag if absent.
- Check for `X-Frame-Options` or `Content-Security-Policy` with `frame-ancestors` directive. Required on any page that should not be embedded in iframes. Flag if both are absent on authenticated pages.
- Check for `Referrer-Policy`. Flag if absent or set to `unsafe-url` (leaks full URL to cross-origin requests).
- Check for `Permissions-Policy` (formerly `Feature-Policy`). Flag if absent on pages using camera, microphone, geolocation, or other sensitive browser features.
- Check for `Cross-Origin-Resource-Policy`, `Cross-Origin-Opener-Policy`, and `Cross-Origin-Embedder-Policy`. Required for applications handling cross-origin isolation. Flag if absent when the application uses `SharedArrayBuffer` or other isolation-requiring features.
- Check for `Cache-Control` directives on authenticated responses. Authenticated pages must not be cached by intermediate proxies. Flag if `public` or missing `private`/`no-store` on responses containing session data.
- Produce a per-endpoint header audit table: endpoint, status code, each security header present/absent/value, and risk flag.

### Phase 3 — Information leakage header detection

Identify response headers that reveal technology stack, versions, or internal infrastructure.

- Check for `Server` header. Flag if it reveals specific software and version (e.g., `Apache/2.4.41 (Ubuntu)`) rather than a generic value. Versioned server banners inform attackers of known-vulnerable versions.
- Check for `X-Powered-By` header. Flag if present; it reveals the backend language or framework (e.g., `PHP/7.4.33`, `Express`, `ASP.NET`).
- Check for `X-AspNet-Version`, `X-AspNetMvc-Version`, `X-Generator`, `X-Drupal-Cache`, `X-Drupal-Dynamic-Cache`, `X-Joomla-Cache`, and other CMS-specific version headers.
- Check for `Via` header revealing internal proxy chains, load balancers, or CDN configurations.
- Check for `X-Backend-Server`, `X-Served-By`, `X-Cache`, `X-Cache-Hits`, `CF-Cache-Status`, and similar infrastructure headers that expose internal architecture.
- Check for `X-Debug-Token`, `X-Debug-Token-Link`, `X-Debug-Token-Link`, `X-Symfony-Cache` (debug headers accidentally left in production).
- Check for `X-Request-ID`, `X-Trace-ID`, `X-Amzn-Trace-Id` on error responses. Trace IDs can be used to correlate requests across internal systems.
- Produce an information-leakage report: header, value, endpoint, and recommended remediation.

### Phase 4 — Cookie inventory and attribute audit

Collect all cookies and audit their security attributes.

- For each endpoint, record every `Set-Cookie` header. Parse each cookie into: name, value prefix (redacted), Domain, Path, Expires/Max-Age, Secure, HttpOnly, SameSite, and any custom attributes.
- Audit each cookie against best practices:
  - `Secure`: must be set on all cookies. Flag any cookie served over HTTPS without the Secure flag.
  - `HttpOnly`: must be set on session cookies and any cookie not accessed by JavaScript. Flag session cookies without HttpOnly.
  - `SameSite`: must be `Lax` or `Strict`. Flag `None` without `Secure` (browsers will reject this). Flag absent SameSite (defaults to `Lax` in modern browsers but `None` in older ones).
  - `Domain`: flag cookies scoped to a parent domain when a more specific domain would suffice. A cookie on `.example.com` is accessible to every subdomain, increasing lateral-movement risk.
  - `Path`: flag cookies scoped to `/` when a more specific path would suffice. Overly broad Path scoping exposes cookies to paths that do not need them.
  - `Expires` / `Max-Age`: flag session cookies with excessively long lifetimes. A session cookie valid for 30 days increases the window for session hijacking. Flag persistent cookies without an expiration (they become session cookies, which is usually acceptable).
- Check for cookie name prefixes: `__Secure-` (must be set with Secure flag, from a secure origin) and `__Host-` (must be set with Secure flag, from a secure origin, with Path=/ and no Domain attribute). Flag cookies using these prefixes incorrectly.
- Check for known sensitive cookie names: `session`, `sess`, `auth`, `token`, `jwt`, `refresh`, `csrf`, `xsrf`. These cookies require all security attributes set correctly.

### Phase 5 — Cookie behavior across authentication states

Understand how cookies change across privilege tiers.

- Authenticate at each available privilege tier and capture the full cookie set.
- Compare cookies across tiers. Do admin sessions use the same cookie name as user sessions? Can a user cookie be replaced with an admin cookie? Document cookie-name differences.
- Test whether cookies are invalidated on logout. Send a request with the pre-logout cookie after logging out. Flag if the cookie remains valid.
- Test whether cookies are invalidated on password change or privilege change. Flag if old session cookies remain valid after credential rotation.
- Test concurrent session behavior: authenticate twice with the same account. Does the first session remain valid? If yes, the application allows session duplication.
- Document cookie lifecycles in the evidence record.

### Phase 6 — Cache-control and CDN header audit

Headers controlling caching and CDN behavior affect data leakage and availability.

- Check `Cache-Control` header on every endpoint. Authenticated responses must be `private, no-cache, no-store, must-revalidate` or equivalent.
- Check for `Pragma: no-cache` and `Expires: 0` on authenticated responses as backward-compatible cache-busting.
- Check for `Vary` header. If an endpoint serves different content based on `Authorization`, `Cookie`, or `Accept-Encoding`, the `Vary` header should list those headers so caches do not serve cross-user responses.
- Check for `Age` header indicating a cached response was served. If an authenticated response has an `Age` > 0, the CDN or proxy may be caching authenticated content.
- Check for `Surrogate-Control`, `Surrogate-Key`, `CDN-Cache-Control`, and CDN-specific purge headers that reveal CDN configuration.
- Flag any caching of authenticated content as a data-leakage risk.

## Decision points

- Endpoint coverage: if the target has thousands of endpoints, test every distinct path prefix and a representative sample of dynamic endpoints. Do not test every permutation.
- Cookie attribute severity: prioritize session cookies without Secure/HttpOnly/SameSite over tracking cookies with the same gaps.
- Information leakage: Server and X-Powered-By headers are low severity individually but can combine with other findings to enable targeted attacks. Always report them but classify severity based on whether specific versions are exposed.
- Caching: authenticated responses without cache-control headers are always at least medium severity due to shared-proxy and browser-cache risks.

## Prohibited behavior

No cookie manipulation to test for privilege escalation (that is vulnerability validation, not enumeration). No session hijacking, session fixation, or session replay testing. No extraction of cookie values for offline cracking. No testing against out-of-scope endpoints. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on an endpoint when all headers and cookies are collected and audited. Stop if the target rate-limits header requests. Stop if the authorization cache expires. Stop if headers indicate the application is behind an outage page or maintenance mode.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- Per-endpoint header audit table with risk flags.
- Information-leakage report with leaked headers and versions.
- Cookie inventory with full attribute audit.
- Cookie-behavior lifecycle documentation.
- Cache-control audit and CDN header analysis.

Never store raw cookie values, session tokens, CSRF tokens, or response bodies containing user data. Redact cookie values to a prefix-only representation (e.g., `session=abc123...`). Never store credentials, PII, or full Set-Cookie header values in reports.

## Report handoff

Record findings via `pentest_agent_record_finding` for: missing HSTS on HTTPS endpoints (high), missing Secure/HttpOnly/SameSite on session cookies (high), Server header with version (low), X-Powered-By header (low), debug headers in production (medium), missing security headers on authenticated pages (medium), authenticated responses with public cache-control (medium), session cookies valid after logout (high), and broad Domain scoping on sensitive cookies (medium). Render the final report with `pentest_agent_render_report`.
