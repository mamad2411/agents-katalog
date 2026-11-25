---
name: security
description: Security rules for any web project (Next.js, Nuxt, SvelteKit, Remix, Vite SPA, Express, Django, Laravel, Rails, Supabase, Firebase). Use whenever a task touches auth, sessions, JWT, permissions, admin routes, the database, an API route or server action, payments, webhooks, file uploads, outbound requests, secrets, env vars, logs, headers, CORS, cloud storage or deployment config, and before any production release.
---

# Security

Apply the items relevant to the task. At the end, one line: items checked, items left. If a request forces you to break a rule, say so instead of doing it. Before a release, also run `audit.md` in this skill's folder.

The browser is enemy territory. Anything checked only in the frontend is not checked.

## 1. Secrets

- No secret in client code, in the repo or in its history. Environment variables, read server-side only.
- Public-by-design prefixes: `NEXT_PUBLIC_`, `VITE_`, `PUBLIC_`, `NUXT_PUBLIC_`, `EXPO_PUBLIC_`, `REACT_APP_`. Never a secret behind them.
- Client side, only keys meant to be public (Supabase anon key, Firebase web config, Stripe publishable key). `service_role`, Stripe secret keys, DB connection strings and third-party API keys never leave the server.
- `.env*` in `.gitignore`, except an up-to-date `.env.example` with no real values. The web server never serves `.env`, `.git/` or config files.
- Secrets generated with a CSPRNG, at least 32 bytes. Never `secret`, `changeme`, a word, or a value copied from a tutorial.
- A secret that reached git, a log, a ticket or a chat is compromised: rotate it. Deleting the commit is not enough.
- Separate secrets for dev, preview and production.

## 2. Authentication

- Use the framework's or provider's auth before writing your own.
- Passwords hashed with argon2id or bcrypt. No homemade hashing, no MD5, no bare SHA.
- Password policy: at least 8 characters, long passphrases allowed, checked against known breached passwords when possible. No forced composition rules.
- MFA available, and required for admin accounts.
- No default credentials anywhere: no `admin/admin`, no seed or test accounts in production, default passwords of DB, CMS and dashboards changed.
- Same response whether the account exists or not, on login, signup and reset (no enumeration).
- OAuth: `state` parameter checked, PKCE, redirect URIs on an exact allowlist.

## 3. Password reset and email verification

- Token random, at least 32 bytes, stored hashed, single-use, expiring in under an hour.
- Token invalidated after use, and every reset token invalidated after a password change.
- All sessions revoked after a password reset or change.
- Reset links built from a configured base URL, never from the request's `Host` header.
- Rate limited per account and per IP.

## 4. Sessions and JWT

- Session cookies `httpOnly`, `Secure`, `SameSite=Lax` or `Strict`, scoped to the right domain and path.
- New session ID on login and on privilege change. Idle and absolute expiry. Logout invalidates server-side.
- No session token or JWT in `localStorage`.
- JWT: secret from env and strong (see 1), algorithm pinned on verification (reject `none` and unexpected algorithms), `exp`, `iss` and `aud` checked, short-lived access token, refresh token rotated and revocable.
- A JWT payload is readable by anyone: no sensitive data in it. Never trust a decoded token that wasn't verified.

## 5. Authorization

- Every route, server action, API handler, RPC and GraphQL resolver checks auth and permission server-side. Hiding a button or a route protects nothing.
- Next.js: a Server Action is a public endpoint, check the user inside it. Middleware alone is not enough.
- Supabase server-side: `getUser()` or `getClaims()`, never `getSession()` alone to decide access.
- IDOR / BOLA: every access to a resource checks it belongs to the user or that they have the right. Changing an ID in the URL, body, query or a nested route gives access to nothing. List endpoints filter by owner or tenant server-side.
- Multi-tenant: every query is scoped by tenant, enforced in the DB (RLS) or in one shared helper, never remembered per query.
- Mass assignment: never pass the request body straight to the ORM. Allowlist writable fields. `role`, `isAdmin`, `userId`, `tenantId`, `price`, `status` are never writable by the client.
- Roles read server-side, never from a value sent by the client.
- Admin routes and panels: role checked server-side on every request, MFA, ideally a separate path or subdomain with stricter rate limits. A secret URL is not protection.

## 6. Database and storage permissions

- Least-privileged DB user for the app. No superuser. The database is not reachable from the internet, or only through an allowlist.
- Supabase / Postgres: RLS enabled on every table, one policy per operation, tested with two different users. RLS without policy blocks everything, `using (true)` protects nothing. `security definer` functions and views bypass RLS: avoid, or justify and restrict.
- Firebase: no `allow read, write: if true` and no test-mode rules in production. Rules tested with the emulator.
- MongoDB, Redis, Elasticsearch: authentication on, never exposed publicly.
- Storage buckets (S3, R2, GCS, Supabase Storage, Firebase Storage): private by default, no public listing, access through signed URLs or storage policies.
- Versioned migrations. Never edit an applied one.

## 7. Input, injection and output

- All input validated server-side with a schema (Zod, Valibot, Pydantic, Laravel validation, etc.): type, length, format, range. Client validation is for comfort only.
- SQL injection: parameterized queries or ORM. Never string concatenation, including in an ORM's raw SQL and in `ORDER BY` or column names (allowlist those).
- NoSQL injection: reject objects where a string is expected (`{"$gt": ""}`), strip `$` operators from input, no `$where` or server-side JS.
- No `eval`, `new Function`, or shell command built from user input. No user input in file paths without normalization and an allowlist (path traversal).
- Lists and search: pagination with a max page size. GraphQL: depth and complexity limits, introspection off in production.

## 8. XSS

- Let the framework escape. No `dangerouslySetInnerHTML`, `v-html`, `{@html}`, `innerHTML` or `|safe` on user content.
- Rich text or Markdown from users: sanitize with DOMPurify or an equivalent allowlist sanitizer, server-side or right before render.
- User-supplied URLs in `href` or `src`: allow `http`, `https` and `mailto` only. Block `javascript:` and `data:`.
- No user data inlined into a `<script>` block without JSON-safe escaping.
- Content-Security-Policy set, without `unsafe-inline` for scripts when the stack allows (nonces or hashes).

## 9. CSRF and CORS

- Cookie-based auth: CSRF protection on every state-changing request (framework token, or `SameSite` plus Origin check). No state change on GET.
- CORS: explicit allowlist of origins. Never `*` with credentials, never reflecting the request's Origin blindly.

## 10. File uploads

- Max size enforced server-side, format allowlist, type checked on file content (magic bytes), not only extension or declared MIME.
- Images re-encoded server-side when possible. SVG and HTML uploads refused, or served as downloads: they can carry XSS.
- Filename regenerated server-side. Stored outside the web root or in a private bucket, served with `Content-Disposition: attachment` or from a separate domain.
- Per-user quota.

## 11. SSRF and outbound requests

- Outbound request to a URL supplied by a user: domain allowlist. Otherwise, block private and link-local ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`, `::1`, `fc00::/7`), resolve DNS before checking, and don't follow redirects blindly.
- Timeout on every outbound request.
- Post-login and post-action redirects: internal paths only (open redirect).

## 12. Payments

- Prices, totals, discounts and currency computed server-side from product IDs and quantities. Never trust an amount, price or coupon value sent by the client.
- Coupons and promo codes validated server-side, with usage limits.
- Order fulfilled only on the provider's verified webhook (for Stripe, `checkout.session.completed` or `payment_intent.succeeded`), never on the success page redirect.
- Webhook handling idempotent: the same event received twice applies once.
- Quantities bounded, negative values rejected.

## 13. Webhooks

- Signature verified on the raw body before any processing. Timestamp checked to block replays.
- Idempotent handling, keyed on the event ID.

## 14. Errors, logs and debug tools

- Production errors: a generic message to the client. Stack traces, SQL errors and file paths only in server logs.
- Debug mode off in production: `DEBUG=False` (Django), `APP_DEBUG=false` (Laravel), no Werkzeug debugger, no framework dev overlay.
- No debug, test, seed or reset endpoints in production. GraphQL playground, Swagger UI, Adminer, phpMyAdmin, Supabase Studio, Prisma Studio and similar never publicly exposed.
- Source maps not public in production: disabled, or uploaded privately to the error tracker and not deployed.
- Logs: no passwords, tokens, API keys, full card numbers or unneeded personal data. Log files and log dashboards not publicly accessible.

## 15. Rate limiting

- Every public endpoint is rate limited per IP and per user. Stricter on login, signup, reset, code sending, search, uploads, contact forms and anything that costs money (email, SMS, AI).
- Return `429` with `Retry-After`.

## 16. Transport and headers

- HTTPS enforced, HSTS.
- `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `frame-ancestors 'none'` or `'self'`, `Permissions-Policy`.
- No `X-Powered-By` or version banners.
- Third-party scripts kept to a minimum, self-hosted or loaded with Subresource Integrity, and listed in the CSP. Every tag manager and widget is a script with full access to the page.
- Transactional email: SPF, DKIM and DMARC set on the sending domain, so nobody can send mail as you and yours doesn't land in spam.

## 17. Cloud and deployment

- IAM and API keys scoped to the minimum: read-only where enough, one key per service.
- Preview deployments protected, and never connected to the production database with write access.
- Production and development in separate projects (Supabase, Firebase, cloud accounts).
- Billing alerts on every cloud and API provider.

## 18. Apps that call an LLM

- Model output is untrusted input: escape it, validate it, never execute it.
- No secrets or other users' data in prompts.
- Tools the model can call run with the user's permissions, checked server-side.
- Max tokens per request and a per-user quota.

## 19. Dependencies

- Lockfile committed. Audit (`npm audit`, `pnpm audit`, `pip-audit`, `composer audit`) before shipping. Report high and critical issues.
- Verify a package's exact name and maintenance before adding it.
