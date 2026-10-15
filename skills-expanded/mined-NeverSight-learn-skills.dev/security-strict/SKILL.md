---
name: security-strict
description: Use this skill when adding or reviewing code that touches auth, tenancy, input validation, webhooks, secrets, caching, or user-provided content (strict security rules).
---

# Security Skill (Strict)

Use this skill for **any** change that could affect confidentiality, integrity, or availability. This is intentionally strict: if a pattern can plausibly cause cross-tenant leakage or unsafe exposure, treat it as a blocker.

This skill fits typical modern web app stacks, for example:

- Next.js App Router (server-first)
- An auth provider (solo or multi-tenant)
- Drizzle ORM + Postgres
- Optional locale routing (`/{locale}/...`)

## Non‑negotiables (stop-the-line rules)

### 1) Tenant isolation is mandatory

- **Derive workspace from the session**, never from client input.
- Every DB query/mutation touching tenant data **must** include `workspace_id` filtering.

References:

- Tenant/workspace derivation: your server-side tenant guard module
- Tenant query patterns: drizzle-tenant-queries skill

### 2) All mutations must be Server Actions (internal)

- Prefer Server Actions for internal CRUD.
- Route Handlers are only for **external** traffic (webhooks, PDF export, third-party callbacks).

References:

- Server Actions conventions: nextjs-server-actions skill

### 3) Validate all inputs at boundaries

- Validate/parse at module boundaries (Server Actions, Route Handlers, webhook handlers).
- Prefer Zod; reject unknown keys.
- Never trust strings that look like IDs (UUIDs) unless validated.

References:

- Zod patterns: zod-v4 skill
- Action result union (don’t throw raw errors across RSC): your shared action result union type

When returning errors from server code, prefer stable `AppErrorCode` values from `@/lib/errors/codes` (use `AppError.*` constants instead of hardcoded strings).

### 4) Never leak sensitive data

- Do not log secrets, tokens, cookies, raw webhook bodies, or PII beyond what’s needed.
- Do not return raw errors to the client. Map to safe messages.
- Avoid exposing internal identifiers; prefer UUIDs for public routes.

### 5) Avoid caching private data incorrectly

- Assume tenant data is **private**.
- Don’t accidentally cache tenant-scoped responses in shared caches.
  - For `fetch`, use `{ cache: "no-store" }` when in doubt.
  - For read helpers, `cache()` memoizes _per request_; it is not a cross-user cache, but still ensure inputs include `workspaceId`.

#### Secure performance (cost without leaks)

- Prefer performance wins that don’t weaken isolation: request-level `cache()`, query parallelization, and removing N+1.
- If you add instrumentation (query timing/logging), never log PII, raw payloads, headers, cookies, or tokens.
- Any cross-request caching must have workspace-scoped keys/tags; otherwise treat it as a security bug.

## Required security checklist (apply to every PR touching app logic)

### Auth + tenancy checklist

- [ ] All protected routes/actions derive workspace via `requireWorkspaceCached()` / `requireWorkspace()`.
- [ ] No use of client-provided `workspaceId` (or equivalent) in any server code.
- [ ] Every query/update/delete includes `workspaceId` in `where`.
- [ ] For updates/deletes: guard by both entity id AND `workspaceId`.
- [ ] Cross-tenant join safety: scope both sides when joining tenant-scoped tables.

### Input validation checklist

- [ ] Use Zod (or equivalent) at boundaries; use `safeParse`.
- [ ] Reject unknown keys (strict object schemas).
- [ ] Normalize and trim user inputs where appropriate.
- [ ] Validate emails/URLs/UUIDs with explicit schemas.
- [ ] For money/time: enforce integer cents + ISO currency; time in UTC.

### Output safety checklist

- [ ] No `dangerouslySetInnerHTML` for user content.
- [ ] Do not render raw user-provided HTML/Markdown without a proven sanitizer.
- [ ] For URLs (redirects, links): allowlist internal paths or validate same-origin.

### Secrets + environment checklist

- [ ] Secrets are read only on the server (`process.env.*`), never sent to client.
- [ ] Never add `NEXT_PUBLIC_*` for secrets.
- [ ] Do not add debug endpoints exposing environment, config, headers, or DB info.

### Webhooks & external endpoints checklist

- [ ] Verify signatures (do not process events without verification).
- [ ] On verification failure: return 400.
- [ ] On transient internal failure: return 500 to trigger retries.
- [ ] Treat payload fields as untrusted even after signature verification.

Reference implementation:

- Webhook verification: your webhook handler route (auth provider / billing / external callbacks)

### Dependency + supply-chain checklist

- [ ] Prefer existing dependencies; avoid adding new ones without a clear need.
- [ ] No `eval`, `new Function`, dynamic `require` of untrusted paths.
- [ ] Avoid unmaintained packages; confirm minimal attack surface.

## Secure implementation patterns

### Pattern: safe Server Action (tenant-safe + strict input)

- Use `requireWorkspaceCached()` to derive `{ workspace, userId }`.
- Zod-validate input.
- Mutate with `workspace.id` in the `where` clause.
- Return `ActionResult` union.

Pseudo-shape (not copy/paste):

- `"use server"`
- `const { workspace } = await requireWorkspaceCached();`
- `const parsed = Schema.safeParse(input);`
- `if (!parsed.success) return { status: "error", ... }`
- `await db.update(table).set(...).where(and(eq(table.id, id), eq(table.workspaceId, workspace.id)))`

### Pattern: safe Route Handler (webhook)

- Force dynamic if needed: `export const dynamic = "force-dynamic"`.
- Verify signature **before** doing anything.
- Return 500 on internal failure so the provider retries.

See: `app/api/clerk/webhook/route.ts`.

### Pattern: tenant isolation test mindset

If you add new tenant-scoped entities or modify query helpers, also add/extend an isolation test.

Reference:

- `scripts/test-client-isolation.ts`

## Red flags (treat as security bugs)

- Any DB operation without `workspace_id` filter.
- Any endpoint that accepts `workspaceId` from the client.
- Using `findFirst({ where: eq(table.id, id) })` for tenant-scoped tables.
- Returning raw DB rows containing PII (emails, tax IDs) without necessity.
- Logging request bodies for webhooks or form submissions.
- Caching tenant data with shared tags that could be used across users.
- Redirects built from `searchParams.get("next")` without validation.

## Edge cases you must handle

- **Cross-tenant entity IDs**: a valid UUID is still untrusted; always scope by workspace.
- **Webhook replay**: signature verification helps; consider idempotency when adding webhook side-effects.
- **Partial failures**: if a multi-step mutation can partially succeed, use transactions.
- **Locale in URLs**: avoid open-redirect patterns when switching locales; only allow known locales.

## Verification before shipping

- Run lint + typecheck.
- Run tenant isolation checks when you touch DB access patterns.

Suggested commands (use project runbooks):

- bun-workflow skill (if your project uses Bun)
- Your tenant isolation checks/tests (if present; often require `DATABASE_URL`)

## Repository anchors

- Tenancy/workspace: your tenant guard module
- DB schema: your schema module(s)
- Server actions: your actions/mutations layer
- Webhook handler: your webhook handler route
- Validation helpers: your validation helpers (if present)
