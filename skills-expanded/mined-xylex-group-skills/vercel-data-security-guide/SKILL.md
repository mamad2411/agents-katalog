---
name: vercel-data-security-guide
description: >
  Apply Next.js App Router data-security best practices for RSC, Data Access Layers,
  DTOs, server-only modules, React taint, and Server Actions (authn/authz, input
  validation, return minimization, CSRF origins). Use when reviewing or implementing
  data fetching, mutations, secret handling, IDOR prevention, client prop exposure,
  or "use server"/"use client" security; when the user runs /vercel-data-security-guide
  or mentions Next.js data security, RSC data leaks, or Server Action security.
---

# Vercel / Next.js Data Security Guide

Source of truth (Next.js 16 App Router): https://nextjs.org/docs/app/guides/data-security

React Server Components change **where** data is accessed. Treat security as a
server-boundary problem: authorize before read/write, minimize what crosses to
the client, never trust client input.

When uncertain about API details, re-fetch the current guide rather than relying
on memory. Related docs: authentication, CSP, forms, server-actions.

## When to load this skill

- Implementing or refactoring data fetching in App Router
- Writing or reviewing `"use server"` actions / `"use client"` props
- Auditing authorization, IDOR, secrets, or env exposure
- Choosing HTTP API vs DAL vs component-level queries
- Configuring taint, `server-only`, or `serverActions.allowedOrigins`

## Operating modes

Pick one mode per request:

| Mode | Goal |
|------|------|
| **Implement** | Add/change features using a single consistent data-access approach |
| **Review / audit** | Walk the checklist in [references/audit-checklist.md](references/audit-checklist.md) |
| **Fix leak** | Stop private fields, env, or DB rows from reaching the client |

Always prefer **retrieval** of current Next.js docs over pre-trained assumptions
for config keys (`experimental.taint`, `serverActions`, etc.).

## Core model

1. **Server Components** may touch secrets, DB, internal APIs.
2. **Client Components** must be treated like browser code — even when prerendered.
3. **Server Actions** are public POST endpoints. UI auth checks do **not** protect them.
4. Prefer **one** data-fetching approach per codebase; do not mix styles casually.

## Choose a data-fetching approach

| Approach | Use when | Security rule |
|----------|----------|---------------|
| **External HTTP APIs** | Large/existing apps, separate backend teams | Zero Trust — call APIs with explicit auth; no special RSC privilege |
| **Data Access Layer (DAL)** | New projects / greenfield | `server-only` library; authorize inside DAL; return minimal DTOs |
| **Component-level queries** | Prototypes only | Sanitize before any client prop; easy to over-expose |

**Default for new work:** DAL + DTOs.

DAL requirements:

- `import 'server-only'`
- Authn + authz at the boundary
- Return only fields the UI needs (API minimization)
- Prefer `cache()` for request-scoped identity helpers so secrets are not threaded through component trees
- Prefer classes for identity objects to reduce accidental full-object serialization
- Only DAL should read secret `process.env` values (not `NEXT_PUBLIC_*`)

Condensed patterns: [references/patterns.md](references/patterns.md).

## Reading data — hard rules

1. **Never pass raw DB rows** into Client Components.
2. Define **narrow prop types** on client UI (only fields needed for render).
3. Mark privileged modules with **`server-only`** so client imports fail the build.
4. Optional defense-in-depth: enable **React taint** (`experimental.taint`) and taint
   sensitive objects/values — still filter in the DAL first.
5. Env: only `NEXT_PUBLIC_*` is client-visible; everything else stays server.
6. Functions/classes are blocked from Client Components by default — do not work around that.

## Mutating data — hard rules

1. Use **Server Actions** (`'use server'`) for mutations — not render side-effects.
2. Treat every exported action as **directly callable via POST**.
3. Inside every action (or delegated DAL function):
   - **Validate** input (forms, params, headers, searchParams)
   - **Re-authenticate** (session/token) — page-level `auth()` is not enough
   - **Authorize** resource ownership / role (prevent IDOR)
   - **Return** only UI-needed fields (never full records by default)
4. Prefer thin actions that call a **`server-only` DAL** for DB + authz.
5. Rate-limit expensive actions (email, writes, external APIs).
6. Closures capture encrypted snapshots — do not rely on encryption alone for secrets.
7. Self-host multi-instance: set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` (base64 AES key).
8. Proxies / multi-domain: configure `serverActions.allowedOrigins` when Origin ≠ Host.
9. No mutations during render (cookie deletes, cache revalidation, DB writes in page body).

Built-in Next.js mitigations (not a substitute for authz):

- Encrypted non-deterministic action IDs (rebuilt periodically; cache ≤ ~14 days)
- Dead-code elimination of unused actions
- Actions only via POST; Origin vs Host (or X-Forwarded-Host) check

## Implementation workflow

1. **Identify the boundary** — which code is RSC, client, action, route handler, proxy.
2. **Pick approach** — HTTP / DAL / prototype component query (one style).
3. **Implement reads** — authorize → query → DTO → pass DTO to UI only.
4. **Implement writes** — validate → authn → authz → mutate → minimal return → revalidate.
5. **Gate secrets** — `server-only`, no secret env outside DAL, no broad client props.
6. **Verify** — see checklist below; run typecheck/lint; smoke the action as a bare POST mentally.

## Review / audit workflow

Use [references/audit-checklist.md](references/audit-checklist.md). Report findings with:

- File + symbol
- Failure mode (e.g. IDOR, over-fetch to client, unvalidated param)
- Severity
- Concrete fix (DTO shape, authz check, `server-only` move)

Priority surfaces:

1. `"use server"` files and inline server actions in forms
2. `"use client"` prop types fed from Server Components
3. Dynamic segments `app/**/[param]/**` and `searchParams`
4. `proxy.ts` / middleware and `route.ts` handlers
5. Direct `process.env` / DB client imports outside a DAL

## Anti-patterns (flag immediately)

| Anti-pattern | Why |
|--------------|-----|
| `return <Client user={dbRow} />` | Full row serializes to client |
| Broad client props (`user: User` with secrets) | Encourages over-sharing |
| Trusting `searchParams.isAdmin` | Client-controlled |
| Page `auth()` only; no check inside action | Action is a separate entry point |
| Action deletes by id without ownership check | IDOR |
| Returning full ORM update result to client | Internal fields leak |
| Mutation in render (`cookies().delete` in Page) | Side-effects / wrong method |
| DB/env imports in shared or client modules | Environment poisoning |
| Mixing HTTP Zero Trust + ad-hoc RSC SQL | Inconsistent audit surface |

## Config snippets (verify against current docs)

```js
// next.config — taint (defense in depth)
module.exports = {
  experimental: {
    taint: true,
  },
}
```

```js
// next.config — allowed origins for reverse proxies (shape may move out of experimental)
module.exports = {
  experimental: {
    serverActions: {
      allowedOrigins: ["my-proxy.com", "*.my-proxy.com"],
    },
  },
}
```

```bash
# Self-host multi-instance encryption key
openssl rand -base64 32
# NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=<value>
```

## Related topics

- Authentication: https://nextjs.org/docs/app/guides/authentication
- Content Security Policy: https://nextjs.org/docs/app/guides/content-security-policy
- Forms: https://nextjs.org/docs/app/guides/forms
- Server Actions: https://nextjs.org/docs/app/guides/server-actions
- Security blog: https://nextjs.org/blog/security-nextjs-server-components-actions

## Principles

- **Authorize at the data boundary**, not only at the page UI.
- **Minimize DTOs** — never “pass the row and sort it out later.”
- **Assume actions are public POST APIs.**
- **One data-access style** per codebase when possible.
- **Defense in depth:** DAL filters first; taint/`server-only` as backup.
