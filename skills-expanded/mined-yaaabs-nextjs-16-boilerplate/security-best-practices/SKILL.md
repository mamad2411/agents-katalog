---
name: security-best-practices
description: Security rules for all code in this repo. Use when handling any external input, env vars, auth, API routes, server actions, or dependencies.
---

# Security Best Practices

Every external input is hostile until validated. Every secret leaks unless proven
otherwise. Apply these rules to all code — they are not optional hardening for "later."

## Validate at every boundary with zod

`zod` is installed for exactly this. Validate — don't trust — all of:

- Server action arguments and form data
- Route handler (`route.ts`) request bodies, params, and search params
- Anything read from `localStorage`, cookies, or URL state
- Third-party API responses your code consumes
- Environment variables (parse once at startup in a `src/lib/env.ts` if the app grows)

```ts
const CreatePost = z.object({ title: z.string().min(1).max(200) });
const input = CreatePost.parse(await req.json()); // throws on bad input
```

## Secrets & environment

- Real values go in `.env.local` (git-ignored). Committed template is `.env.example`.
- `NEXT_PUBLIC_` prefix = shipped to every browser. Never prefix a secret with it.
- Never log secrets, tokens, session IDs, or personal data.
- Never hardcode credentials, even "temporarily," even in tests.

## Server/client boundary

- Privileged logic (DB access, API keys, price calculations, permission checks) lives in
  Server Components, server actions, or route handlers only.
- Authorization is checked **on the server for every request** — client-side checks are
  UX, not security. Re-verify session/role inside every server action and route handler,
  not just in layout or UI code.
- Add the `server-only` package import to modules that must never reach the client.

## Output & injection

- Never use `dangerouslySetInnerHTML` with user-influenced content; if unavoidable,
  sanitize with a maintained library first.
- Use parameterized queries / an ORM — never string-build SQL.
- Validate and allowlist URLs before redirecting or fetching them (SSRF).

## Headers & platform

- Baseline security headers are set in `next.config.ts` — keep them when editing config.
- Add a Content-Security-Policy when the app's asset sources stabilize (see SECURITY.md).
- New dependencies: prefer well-maintained, widely-used packages; check `npm audit` after
  adding. Fewer dependencies is itself a security feature.

## When touching auth (future apps built on this template)

- Use a proven library (Auth.js, Clerk, Better Auth...) — never hand-roll sessions,
  password hashing, or token logic.
- Cookies: `httpOnly`, `secure`, `sameSite` — always.
