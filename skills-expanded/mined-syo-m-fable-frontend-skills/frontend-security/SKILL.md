---
name: frontend-security
description: Frontend security rules — XSS, injection, validation, CSRF, SSRF, CORS, secrets, sessions/JWT, rate limiting, headers, uploads, third-party scripts, prompt injection, dependency hygiene. Use whenever code touches user input, HTML rendering, auth, cookies, URLs, outbound fetch, webhooks, env vars, file uploads, logging, untrusted content fed to an LLM, or new dependencies. 日本語の依頼例:「認証/ログイン実装」「入力フォーム作って」「問い合わせ/お問い合わせフォーム作って」「送信フォーム」「cookie/セッション」「外部APIを叩いて」「webhook受信」「ファイルアップロード」「環境変数」「依存パッケージ追加」「LLMに渡す」。
---

# Frontend Security

Order of defense: don't accept untrusted data → validate at the boundary → encode/sanitize at output → restrict with platform policy (CSP, cookies, headers). Apply all layers, not one. These rules are policy: changing or weakening them requires human security review (see `governance`).

## XSS

- Framework escaping is the default protection — keep it. `dangerouslySetInnerHTML` (React), `set:html` (Astro), `innerHTML`/`insertAdjacentHTML` (DOM) with anything non-static require sanitization with **DOMPurify** at output time, using one shared hardened config — not ad-hoc per-call options. SSR/build-time paths need `isomorphic-dompurify` (DOMPurify requires a DOM). No home-made regex sanitizers, ever.
- URLs are an injection vector: any `href`/`src` from user data → parse with `new URL`, allow only `http:`/`https:` protocols (blocks `javascript:` URLs that escaping does not stop).
- Never build HTML/CSS/JS by string concatenation with user data. No `eval`, `new Function`, string `setTimeout`.
- Don't render raw user input into `<script>` contexts, JSON-LD blocks, or inline event handlers.

## Validation — server-side, schema-first

- Every boundary parses input with zod before use: Server Actions, route handlers, URL/search params, cookies, third-party API responses, webhook payloads (after signature verification — see below).
- Client-side validation is UX only; the server must reject independently.
- Default to closed shapes: `z.strictObject({...})` (zod 4; `.strict()` is the legacy spelling) — unknown keys are **rejected**, blocking mass-assignment (`isAdmin: true` in a profile update). Plain `z.object()` silently strips unknown keys, which also prevents mass-assignment but hides client bugs. Document any exception.
- Bound every user-supplied string with `.max(n)` — unbounded input is a DoS/ReDoS vector.
- Locale-formatted input (decimal comma, native digits): parse to a canonical form first, then validate the canonical value (see `i18n`).
- ReDoS: never execute user-controlled regex; cap input length before any regex; avoid nested quantifiers (`(a+)+`).
- Prototype pollution: never recursively merge user JSON into existing objects; reject `__proto__` / `constructor` / `prototype` keys; prefer `Map` or `Object.create(null)` for user-keyed lookups.
- IDs from the client are claims, not facts: after auth, check the resource belongs to / is permitted for this user (IDOR). Per-resource, in every action/handler — middleware route guards are not enough.
- Authorization model: decide it deliberately (role-based for coarse access, attribute/ownership-based for per-record) and enforce it server-side in one place (a policy helper), not ad-hoc `if (user.role === 'admin')` scattered across handlers. Deny by default.

## Sessions, cookies, JWT

- Session cookies: `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict`), `__Host-` prefix where possible (enforces `Path=/`, no `Domain`). Never store session tokens in `localStorage`.
- Rotate the session ID on login and on privilege change (session fixation).
- JWT, if used: decode ≠ verify — always verify the signature with an `alg` allow-list (reject `none`); check `exp` / `aud` / `iss`; short-lived access tokens + rotated refresh tokens; no PII in claims that reach the client.
- Security-relevant randomness (tokens, nonces, IDs): `crypto.randomUUID()` / `crypto.getRandomValues()` — never `Math.random()`. No hand-rolled crypto; Web Crypto only.

## CSRF & redirects

- Framework protection covers less than you think: Next.js verifies Origin for **Server Actions only**. **Route handlers have no built-in CSRF protection** — every cookie-authenticated state-changing route handler needs explicit Origin/Referer validation or a CSRF token. `SameSite` is defense-in-depth, not sufficient alone (subdomains, legacy clients).
- Mutations are POST-family only; a state-changing GET is a bug regardless of other protections.
- Open redirects: never `redirect(userInput)` raw — allow-list relative paths or known origins. Same rule for OAuth `redirect_uri`; always validate the OAuth `state` parameter.

## Outbound requests — SSRF & webhooks

- Server code fetching a user-supplied or user-influenced URL: allow-list hosts; block private/link-local ranges and cloud metadata endpoints (`169.254.169.254`) — and the IPv6 equivalents (`::1`, `fc00::/7`, `fe80::/10`, IPv4-mapped `::ffff:169.254.169.254`); re-validate after redirects. Constrain `next/image` `remotePatterns` tightly — the image optimizer is a classic SSRF proxy.
- Defeat DNS rebinding / TOCTOU: resolve the host, validate the resolved IP against the deny ranges, then connect to that pinned IP (don't validate a hostname and then let the HTTP client re-resolve it).
- Incoming webhooks: **verify the provider's HMAC signature (constant-time compare) before trusting the payload; reject when the signature header is missing.** Schema validation is not authentication.

## CORS

- Never reflect the request `Origin` while sending `Access-Control-Allow-Credentials: true`; never `*` on authenticated endpoints. Maintain an explicit origin allow-list. "Fixing a CORS error" by widening headers is usually creating a vulnerability — find the legitimate origin instead.

## Rate limiting & auth failures

- Throttle login, signup, password reset, and expensive mutations — per IP and per account.
- Uniform error messages and response timing on login/reset: do not reveal whether an account exists.

## Untrusted content & prompt injection

Relevant whenever the app sends content to an LLM or renders model output (chat, summarization, RAG, agentic features).

- Treat all external content — user input, fetched pages, API/webhook payloads, documents, retrieved chunks — as **data, never instructions**. It may contain text attempting to redirect the model ("ignore previous instructions…"); enclose it in clearly delimited, labeled fields and instruct the model that delimited content is data only.
- The model's output is itself untrusted: never `eval`/render it as HTML/execute it as a tool call without the same validation, sanitization (DOMPurify), and authorization you apply to user input. Tool/function calls the model requests are authorized server-side per the acting user — the model cannot grant itself capability.
- Never put secrets, API keys, or another user's data in a prompt or system message that a response could leak back. Apply least-privilege to any tool the model can invoke; high-impact actions (sending mail, spending, deletes) require explicit human confirmation, not model discretion.
- Server-side LLM keys stay server-side (never `NEXT_PUBLIC_`/`VITE_`); rate-limit and budget-cap LLM endpoints (cost-DoS).

## Secrets, env, logging

- Secrets never appear in: client bundles (`NEXT_PUBLIC_`/`VITE_`/`PUBLIC_` vars are public by definition), repo files, logs, client-bound error messages, or URL query strings (query strings leak via logs and referrers).
- `.env*` in `.gitignore`; commit `.env.example` with placeholders. A secret ever committed = rotate it; deleting the file does not unpublish it. Secrets scanning in CI is mandatory (see `governance`).
- No PII, credentials, or tokens in server logs, analytics events, or error-tracker payloads — configure scrubbing (e.g. Sentry `beforeSend`). Server errors: log details server-side, return a generic message + correlation ID. Stack traces and DB errors never cross the wire.
- Conversely, DO record security events for audit (A09 / ASVS V7): authentication success & failure, authorization denials (IDOR / 403), privilege/role changes, webhook signature-verification failures, password/email changes, and admin actions — each with actor, action, result, source IP, and correlation ID. "Don't log PII" governs the *payload*, not the security-event metadata — silent auth failures are how breaches go undetected. Make these logs tamper-evident and retained per policy.
- Data minimization & retention: collect only what's needed; set a retention window on logs/analytics containing personal data and honor deletion requests — don't keep PII indefinitely "just in case".

## Headers & platform policy

Set and keep (next.config / astro config / hosting headers):

- `Content-Security-Policy`: `script-src` must NOT contain `'unsafe-inline'` (it reopens the main XSS path that framework escaping closes) — use a per-request nonce or hashes, and prefer `'strict-dynamic'`. At minimum: `script-src` without `'unsafe-inline'`/`'unsafe-eval'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, and `frame-ancestors 'none'` (or explicit allow-list) + `X-Frame-Options: DENY` fallback. Roll out via `Content-Security-Policy-Report-Only` first, with reports routed somewhere monitored.
- `Strict-Transport-Security` with a long max-age (understand the commitment before adding `preload`).
- `Cache-Control: no-store` on authenticated/personalized responses — caching a per-user response is a data leak, not a perf win.
- `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cross-Origin-Opener-Policy: same-origin`, `Permissions-Policy` denying unused features.

## Third-party scripts & embeds

- Third-party scripts require approval (see `governance`), exact version pinning, and `integrity` (SRI) when loaded from a CDN; prefer self-hosting. Tag managers that load arbitrary scripts defeat CSP — avoid, or strictly govern what they may inject.
- iframes/embeds: explicit `sandbox` attribute; `postMessage` handlers must check `event.origin` against an allow-list.

## Dependencies

- Before adding: maintenance, downloads, install scripts (`postinstall`), transitive weight, license (see `governance`), and the EXACT package name (typosquatting).
- Dependency confusion: publish private packages under the org scope (`@company/`); pin scope→registry mapping in `.npmrc`; assert registry URLs with `lockfile-lint` in CI.
- Prefer a release cooldown: avoid versions published within the last few days (compromise/worm window). Pin CI actions by commit SHA, not tag.
- Lockfile always committed; CI installs frozen (`npm ci` / `pnpm install --frozen-lockfile` per the repo's package manager), with `--ignore-scripts` where the build allows.
- Audit on every dependency change AND on a weekly schedule; high + critical findings block.

## Uploads & user files

- Validate type by content (magic bytes), not extension; cap size; store outside the web root / in object storage.
- SVG passes image checks but executes scripts: deny or sanitize SVG. Serve user uploads from a separate origin — re-encoding raster images through the framework's image optimizer satisfies this intent; anything served as-is (HTML, SVG, PDF, downloads) must use the separate origin. `Content-Disposition: attachment` for non-image types; correct `Content-Type` + `nosniff`.
- Authorize every download per-request — non-guessable names are defense-in-depth, never the access control. Intentionally-public assets (e.g. avatars) may skip per-request auth as an explicit, documented decision — not a default.
- Never trust client-supplied paths/filenames: path traversal, zip-slip when extracting archives.

## Self-check before shipping boundary code

These are the controls lint can't fully prove (only Semgrep-backstopped in `templates/.semgrep/`). Before finishing any change that touches a boundary, answer each for what you touched — a "no" means fix it, don't ship:

- External input (body / params / cookies / API response / webhook) parsed with a zod schema at the boundary?
- Webhook payload signature verified (constant-time) BEFORE it's trusted?
- Every client-supplied ID authorized for *this* user, per resource (IDOR)?
- Authorization enforced server-side in the one policy helper, deny-by-default — not scattered role checks?
- Outbound fetch to a user-influenced URL: host allow-listed, private/link-local/metadata ranges blocked, AND connected to the pinned resolved IP (DNS-rebinding)?
- No secret / PII / token in the client bundle, logs, analytics, error payloads, or URLs?
- Non-static HTML sanitized (DOMPurify)? No new `dangerouslySetInnerHTML` / `set:html` / `innerHTML` without it?
- Session cookies `HttpOnly` + `Secure` + `SameSite`; cookie-auth state-changing route handlers CSRF-protected?
- Untrusted / model-bound content handled as data, never instructions?
