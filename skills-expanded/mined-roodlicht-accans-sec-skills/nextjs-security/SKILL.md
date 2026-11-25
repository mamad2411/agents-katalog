---
name: nextjs-security
description: Next.js security review — middleware auth-bypass patterns (CVE-2025-29927), Server Actions auth/CSRF, Server/Client Component boundary and SSR data leaks, auth.js (NextAuth) config, route handlers as API, Image Optimization SSRF, security headers via middleware.
---

# Next.js Security

## When to use

This skill is the Next.js-specific layer on top of `secure-coding` and `api-security`. Next.js has gone through several architectural shifts in recent years (Pages Router, App Router, Server Actions, middleware evolution), and the security implications shift with them. It is also used by teams that do not have a sharp line between front-end and back-end — and that is exactly where bugs live.

Triggers on:

- A question like "review our Next.js app", "CVE-2025-29927 impact", "make Server Actions safe", "auth.js/NextAuth config review", "middleware auth", "SSR is leaking data into the client bundle", "image optimization SSRF".
- Presence of `next.config.js`/`.mjs`/`.ts`, `middleware.ts` in the project root, an `app/` directory with `page.tsx` and `layout.tsx`, `pages/` (older router), `"use server"` or `"use client"` directives, NextAuth/auth.js config.
- A PR that touches middleware, adds Server Actions, converts API routes to Server Actions, or changes auth.js config.
- Next.js version bumps, especially around security releases.
- Handoff from `security-review` or `api-security` when Next.js is in the stack.

### When NOT (handoff)

- General JS/TS secure-coding → `secure-coding`.
- OWASP API Top 10 as a conceptual framework → `api-security`. Here for the Next.js implementation.
- SAST tooling (eslint-plugin-security, Semgrep `p/javascript`) → `sast-orchestrator`.
- Dep vulns in `package.json` / `package-lock.json` → `cve-triage`.
- Vercel/Netlify deploy config and edge-network policies → `iac-security` where possible, otherwise platform-specific docs.
- Secrets in `.env.local` or Vercel env vars → `secrets-scanner`.

## Approach

Seven phases. Phase 1 (middleware and auth-bypass) is the heart — that is where the CVE-2025-29927-class bug sat and where architectural misconceptions cause problems most often.

### 1. Middleware and auth-bypass

Next.js middleware runs before every matching request and is often used for authentication gates and redirects. That is precisely why it is an attack surface.

- **CVE-2025-29927** (`[verify against https://nextjs.org/blog]` and [https://github.com/vercel/next.js/security/advisories](https://github.com/vercel/next.js/security/advisories)): An internal header that Next.js used for infinite-loop detection could be set externally, causing middleware to be skipped. Effect: middleware-based auth could be bypassed. Patched in 14.2.25, 15.2.3. Reviewer impact questions:
  - Are you running a version ≥ fix?
  - Was middleware your only auth layer for affected paths? If yes: anyone who could have gained access during the exposure window is an audit target.
  - Are there defense-in-depth auth checks at page or Server-Action level? If "no", this is a pattern-level fix, not just a version bump.

- **More general middleware pattern**: middleware is not a safe place for **only** auth. Defense-in-depth: also check auth in the page/route-handler/Server-Action. Middleware for redirects and header enforcement, not as the sole gate.

- **Open redirects via middleware**: `return NextResponse.redirect(new URL(request.nextUrl.searchParams.get('next') ?? '/', request.url))` — if `next` is not validated, this is an open redirect. Allowlist destinations.

- **Matchers**: `export const config = { matcher: '/admin/:path*' }` — a too-narrow matcher does not protect what you thought it protected. Verify all sensitive paths are matched.

### 2. Server Actions: auth and CSRF

Server Actions (`"use server"`) are RPC endpoints called from a Client Component but executing as server code. They share security concerns with API routes, plus a few of their own.

- **Authentication in the Action itself**, not only in the caller. An attacker can call your action hard-coded, bypassing your UI guard.
  ```ts
  'use server';
  export async function deletePost(id: string) {
    const session = await auth();         // do not skip
    if (!session) throw new Error('unauth');
    const post = await db.post.findUnique({ where: { id } });
    if (post.authorId !== session.user.id) throw new Error('forbidden'); // IDOR fix
    await db.post.delete({ where: { id } });
  }
  ```
- **Input validation**: Server Actions receive a `FormData` or directly-called args. Validate with zod/valibot/yup. Trust nothing that comes from the client.
- **CSRF**: Next.js protects Server Actions by default via same-origin checks and an action ID issued only by the server. Cross-origin POST to an action fails. But: that protection leans on the `Origin` and `Host` headers. Custom proxy setups can break this; verify Next.js' CSRF guard is still active behind your proxy.
- **Rate-limiting**: Next.js has no built-in rate limiter. Use Upstash/Redis/edge-config on the action path, or place auth-sensitive Actions behind a gateway that does rate-limiting.

### 3. Server/Client Component boundary and SSR data leaks

The App Router introduced Server Components and Client Components. The boundary is meaningful at runtime: what is in a Server Component does not end up in the client bundle, what is in a Client Component does.

- **`"use client"` boundary**: data passed as props into a Client Component lands in the client bundle or in the hydration payload. So: no secrets, no internal IDs, no `password_hash`, no other user's data that happened to come along in your query, no feature flags that competitors should not see.
- **`process.env` in Client Components**: only `NEXT_PUBLIC_*` vars are available. Anything else reads as `undefined`. That is the right default; but an accidentally renamed `NEXT_PUBLIC_API_KEY` leaks into the production bundle. Grep for `NEXT_PUBLIC_` and confirm everything explicitly belongs in public.
- **Hydration mismatch as a leak source**: if server and client see different data (e.g. an admin flag), the hydrating client can show data in dev tools that it should not. Server-rendered state contains what you send.
- **Route handler (`app/api/.../route.ts`)** for Pages Router's API routes: treat as any other API endpoint (see `api-security`). Auth in the handler, not only in the UI.

### 4. auth.js (NextAuth) and session model

auth.js (rebranded from NextAuth v5) is the de facto auth library for Next.js.

- **Session strategy**: `database` or `jwt`. JWT strategy stuffs all session data into an encrypted JWT cookie — fast reads, no server-side invalidation. Database strategy has invalidation but requires a DB hit per request. The choice is a trade-off; the JWT default is reasonable for small apps, database for anything where logout really must invalidate.
- **`AUTH_SECRET`** must be cryptographically random (`openssl rand -base64 32`), in vault or env var, different per environment. See `secrets-scanner`.
- **Providers**: OAuth providers (Google, GitHub, etc.) use PKCE by default in auth.js v5. OK. Watch out for the Custom Credentials provider: you write the `authorize` function yourself, all credential validation is your responsibility. Verify password hashing (argon2id via the `argon2` package or bcrypt), and timing-safe comparison.
- **Callback-URL allowlist**: `pages.signIn` etc. explicit. No dynamic redirect URL from a `callbackUrl` query param without an allowlist check.
- **Session-cookie flags**: auth.js sets `HttpOnly`, `Secure` (in prod), `SameSite=Lax` by default. Do not override unless necessary.

### 5. Image Optimization, file uploads, other SSRF vectors

- **`next/image` with external sources**: `remotePatterns` in `next.config.js` is the allowlist for where Next.js may fetch images. A wildcard hostname is effectively an image-proxy SSRF: someone loads `/_next/image?url=<internal-URL>` and uses your server to reach internal endpoints. Scope `remotePatterns` to your exact CDN/bucket domain.
  Canonical example of this class: `[verify against CVE database and Next.js advisories — multiple image-proxy related CVEs have appeared]`.
- **File uploads via Server Actions**: `FormData` with `File` — validate server-side on content type, size, magic bytes. Client `File.type` is spoofable. Store outside `public/` to prevent path traversal.
- **Fetch in Server Components to user URLs**: classic SSRF (see `api-security` phase 5). Block private IP ranges, DNS-rebinding protection.
- **`next/headers` cookies/headers access**: only in Server Components and Server Actions, not in Client Components. Well-guarded by default.

### 6. Security headers via middleware or next.config

Headers are configured in `next.config.js` `headers()` or in middleware.

```js
// next.config.mjs
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'Content-Security-Policy', value: "default-src 'self'; script-src 'self' 'nonce-<nonce>'; ..." },
];

export default {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};
```

- **CSP** with a nonce is recommended; Next.js documents the nonce pattern via middleware. Avoid `'unsafe-inline'` and `'unsafe-eval'` where possible — they largely null out CSP's XSS protection.
- **HSTS** with `preload` only if you are on the HSTS preload list or want to be. `max-age` at least 1 year for preload eligibility.
- Headers via middleware are more dynamic (per route) but heavier.

### 7. Misc and verification-loop

- **`dangerouslySetInnerHTML`** — React equivalent of `|safe`. Only on sanitized content, never directly on user input. Use `DOMPurify` or `sanitize-html` for user-generated HTML.
- **`eval`, `new Function`, dynamic `import(userString)`** — RCE vectors, never on user input.
- **`revalidatePath` / `revalidateTag`** from Server Actions — if the path parameter comes from user input, someone can manipulate your cache. Allowlist the paths.
- **`noindex` on non-production** via middleware or `robots.txt`, to keep staging out of Google by accident.

Verification-loop: Layer 1 (next.config, middleware, layout/page auth checks, Server Actions all walked through?), assumptions ("auth.js works by default" only if you have seen the actual config). Layer 2 (CVE-2025-29927 with fix versions checked against nextjs.org advisories, auth.js v5 API names correct, no invented Next.js version ranges in fix claims).

## Output

```
Next.js security review — <app>
Next.js: <x.y.z> | Router: <App | Pages | mixed>
auth.js / NextAuth: <version, provider list>

Middleware:
  Present:               <yes/no>
  Auth via middleware:   <only layer | part of defense-in-depth>
  Matchers:              <scope>
  CVE-2025-29927 patched:<yes/no>
  Open redirects:        <list>

Server Actions (App Router):
  Number of actions:     N
  Auth check per action: <yes for all | gaps on ...>
  Input validation:      <zod/valibot/... | none>
  Rate-limited:          <yes/no>

Server/Client boundary:
  NEXT_PUBLIC_* exposure: <list, review>
  Secrets in Client props:<grep for password/token/key>
  Hydration leaks:        <visible in dev tools?>

auth.js:
  AUTH_SECRET source:    <vault/env>
  Session strategy:      <jwt | database>
  Providers:             <OAuth + PKCE | credentials + hashing scheme>
  Callback-URL allowlist:<yes/no>

next/image:
  remotePatterns scope:  <specific | wildcard — FINDING>

Security headers:
  HSTS:                  <on + preload>
  CSP:                   <nonce/hash | unsafe-inline — FINDING>
  Frame-Options:         <DENY/SAMEORIGIN>

Version check:
  Latest security release: <date>
  cve-triage handoff:      <N deps with vulns>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- Next.js Security — [https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy](https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy) and broader [https://nextjs.org/docs](https://nextjs.org/docs).
- Next.js Security Advisories — [https://github.com/vercel/next.js/security/advisories](https://github.com/vercel/next.js/security/advisories). Primary CVE source.
- Server Actions docs — [https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations).
- auth.js (NextAuth v5) — [https://authjs.dev/](https://authjs.dev/).
- React Security — [https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html](https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html) for `dangerouslySetInnerHTML`.
- OWASP Top 10 2021 — [https://owasp.org/Top10/](https://owasp.org/Top10/).
- CSP Reference — [https://content-security-policy.com/](https://content-security-policy.com/). Useful CSP builder plus per-directive explanation.
- MDN Headers (HSTS, X-Frame-Options, etc.) — [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers). Primary header reference.

## Categories

- appsec
