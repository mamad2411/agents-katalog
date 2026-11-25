---
name: kb-api
description: Portable API patterns for Next.js 16+ App Router — Server Actions vs Route Handlers decision, `ActionResult<T>` discriminated-union contract, HTTP status conventions, Zod `safeParse` at the boundary, async `params`, and `revalidatePath` success-only rule. Invoke when writing or reviewing server actions / route handlers without kit wrappers, or choosing between action vs route. For kit-shipped wrappers → `sk-api`.
last-verified: 2026-04-23
---

# kb-api — Portable Server Actions & Route Handler Patterns

> Stack: Next.js 16+ App Router + Zod.
> **Portable** — these patterns work in any Next.js project, with or without the Starter Kit.
>
> **Pair:** [`sk-api`](../sk-api/SKILL.md) — kit-shipped wrappers (`withAuth`, `withSelf`, `ActionError`, `ActionResult` implementation, `@/lib/logger`, inline-Response convention, `canHardDeleteUser`, humanId retry).
> **Orchestrator for CRUD:** [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md) — end-to-end CRUD module generation.
> Related: [`kb-db`](../kb-db/SKILL.md) / [`sk-db`](../sk-db/SKILL.md) for DB patterns · [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) for mocking in action tests · [`kb-security`](../kb-security/SKILL.md) / [`sk-security`](../sk-security/SKILL.md) for auth + RBAC.

---

## 1. Server Actions vs Route Handlers — decision matrix

| Use Server Action       | Use Route Handler                      |
| ----------------------- | -------------------------------------- |
| Mutations from UI forms | Webhooks (Stripe, Resend, etc.)        |
| Progressive enhancement | External / mobile / SSE clients        |
| Needs `revalidatePath`  | REST contract required                 |
| Type-safe end-to-end    | Third-party integrations / public auth |

> **Default to Server Actions.** Reach for a route handler only when something external calls it or the response isn't page-revalidation (health, SSE, uploads, NextAuth callbacks, invite flow, webhooks).

---

## 2. The `ActionResult<T>` return contract (pattern, not implementation)

The discriminated-union pattern is portable — adopt it in any Server Action codebase, not only this repo:

```ts
export type ActionResult<T = void> = { data: T; error?: never } | { error: string; data?: never };
```

Consumers branch on `result.error`:

```tsx
const result = await createUser(input);
if (result.error) {
  toast.error(result.error);
  return;
}
// result.data is typed here
```

**Why the union matters:**

- Type-narrowing in the consumer is automatic — no `if (!result.data)` ambiguity.
- Errors carry a string ready for `toast` / inline UI. Internal stack traces never reach the client.
- Works identically with FormData (progressive enhancement) and plain-object calls.

> The kit pairs this with a typed `ActionError` class whose message is the only thing surfaced to the user. Without the kit, you can achieve the same by catching in a thin wrapper and returning `{ error: err.message }` only for a whitelisted error class. See [`sk-api`](../sk-api/SKILL.md) for the kit implementation.

---

## 2.1 CRUD Server Action signatures (portable)

Every CRUD module exposes five actions with stable shapes. Use these signatures regardless of kit adoption — they compose cleanly with or without a wrapper helper. Orchestrator for full scaffold: [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md).

```ts
// Read (list) — no input; scoped by caller's role via guard
export async function getEntities(): Promise<ActionResult<Entity[]>>;

// Read (single) — string id; returns null when not found
export async function getEntityById(id: string): Promise<ActionResult<Entity | null>>;

// Create — unknown input, parsed once at boundary
export async function createEntity(input: unknown): Promise<ActionResult<{ id: string }>>;

// Update — id + partial payload; returns nothing on success
export async function updateEntity(id: string, input: unknown): Promise<ActionResult>;

// Delete — soft delete (sets deletedAt/deletedBy); hard delete is an opt-in exception
export async function deleteEntity(id: string): Promise<ActionResult>;
```

**Semantics (portable rules):**

| Action          | Auth                        | Semantics                                                         |
| --------------- | --------------------------- | ----------------------------------------------------------------- |
| `getEntities`   | guard (`list` capability)   | Filter soft-deleted; order deterministically (created_at, id)     |
| `getEntityById` | guard (`read` capability)   | `null` for missing — callers render 404; never throw for "absent" |
| `createEntity`  | guard (`create` capability) | Zod parse → uniqueness checks → insert → revalidate on success    |
| `updateEntity`  | guard (`update` capability) | Load target → guard (self/role) → Zod parse → update → revalidate |
| `deleteEntity`  | guard (`delete` capability) | Soft delete by default; cascading effects go in the same tx       |

> These are **signatures**, not kit helpers. Inside each action you can compose an auth guard + `safeParse` + `revalidatePath` directly, or delegate to a wrapper (the kit's `withAuth` does exactly that — see [`sk-api`](../sk-api/SKILL.md)).

---

## 2.2 Auth guard — abstract pattern (no kit helpers)

A portable CRUD server action has four phases in order: **auth → permission → validate → mutate → revalidate**. Below is the raw pattern; a kit wrapper collapses it to one call, but the semantics are identical.

```ts
'use server';

import { getSession, requirePermission } from '@/lib/auth';
import { revalidatePath } from 'next/cache';
import { createSchema } from './validations';
import type { ActionResult } from './types';

export async function createEntity(input: unknown): Promise<ActionResult<{ id: string }>> {
  try {
    // 1. Auth — session must exist
    const session = await getSession();
    if (!session?.user?.id) return { error: 'Unauthorized' };

    // 2. Permission — capability check against role
    requirePermission(session.user.role, 'entities', 'create');

    // 3. Validate — parse ONCE at the boundary
    const parsed = createSchema.safeParse(input);
    if (!parsed.success) return { error: 'Invalid input' };

    // 4. Mutate — trust parsed.data, do not re-parse
    const id = await insertEntity(parsed.data, session.user.id);

    // 5. Revalidate — success path ONLY (see §2.4)
    revalidatePath('/entities');

    return { data: { id } };
  } catch (err) {
    // Only whitelist user-facing error classes; log the rest, return generic
    if (err instanceof Error && err.name === 'UserFacingError') return { error: err.message };
    // logger.error({ err, scope: 'createEntity' });
    return { error: 'Something went wrong' };
  }
}
```

**Guard rules:**

- The **auth guard precedes everything** — no DB read, no Zod parse, no side effect before the session is verified.
- **Permission check is separate from auth** — a logged-in user without the capability gets `403`-equivalent behavior (not `401`).
- **Never re-check auth inside the handler body** — the guard at the top is the single source of truth for that request.
- **Self-service actions** (user edits own data) skip the permission step but still require auth. Do not pass `userId` as input — read it from the session.

> Kit-shipped equivalent: `withAuth({ resource, action, schema, revalidate }, input, handler)` compresses steps 1-5 into a single call. See [`sk-api`](../sk-api/SKILL.md) §1.

---

## 2.3 Zod at the boundary — parse once, trust after

**The rule:** parse input **exactly once**, at the action / route boundary. After `safeParse` succeeds, `parsed.data` is a fully-typed value you trust through the rest of the call stack. Do not re-parse inside helpers, DB layer, or downstream services.

```ts
// ❌ Double parsing — smell: unclear ownership of validation
export async function updateEntity(id: string, input: unknown) {
  const a = schema.safeParse(input);
  if (!a.success) return { error: 'Invalid' };
  await repo.update(id, schema.parse(a.data)); // parsed again — why?
}

// ✅ Parse once, pass typed data
export async function updateEntity(id: string, input: unknown) {
  const parsed = schema.safeParse(input);
  if (!parsed.success) return { error: 'Invalid input' };
  await repo.update(id, parsed.data); // repo.update signature takes the inferred type
}
```

**Why this matters:**

- Double parsing masks unclear trust boundaries — if you feel the need to re-parse, the real problem is that your internal function accepts `unknown`. Fix the internal type, not the parse count.
- Parsing is not free. In hot paths (SSE streams, high-traffic routes) a stray second parse adds latency.
- Schema drift hides here. Two parses with "similar" schemas diverge silently; one parse has one source of truth.

**Boundaries where you MUST parse:**

- Server action input (`input: unknown`)
- Route handler body (`await req.json()`)
- Route handler params / search params (even typed ones — they arrive as strings)
- Form data from Server Components (`formData.get('x')` is always `FormDataEntryValue | null`)
- External webhook payloads (Stripe / Resend / etc.)

**Boundaries where you MUST NOT parse:**

- Internal function calls that already received typed data
- DB query results (typed by the ORM — Drizzle `$inferSelect` in this stack)
- Session user (already typed by NextAuth callbacks)

---

## 2.4 `revalidatePath` — success-only, never on failure

```ts
// ❌ Unconditional — revalidates even on validation failure
revalidatePath('/entities');
return parsed.success ? { data } : { error };

// ✅ Only after a real mutation succeeds
const result = await doMutation();
revalidatePath('/entities'); // only reached on success path
return { data: result };
```

**Rules:**

- Revalidate **after** the mutation commits, not before. Errors thrown mid-mutation must not trigger revalidation — the cache is still correct.
- Revalidate **only the affected paths**. For CRUD: the list page and the specific detail page (`/entities/[id]` if editing in place).
- Prefer `revalidateTag` when multiple paths share a tagged cache boundary (detail + list from same count query). `revalidatePath` is fine for simple 1-2 path cases.
- **Read-only actions (`getX`) never revalidate.** If you feel the urge to revalidate after a read, the real bug is stale cache on the mutation path.

---

## 3. Input validation — Zod `safeParse` at the boundary

Regardless of wrapper, validate at **every** boundary: action input, route body, route params, form data. Never trust input, never `any`-type it.

```ts
// Route handler — explicit parse
const body = await req.json();
const result = schema.safeParse(body);
if (!result.success) {
  return Response.json(
    { error: 'Invalid request body', details: result.error.flatten() },
    { status: 400 }
  );
}
// result.data is typed
```

```ts
// Server action — parse once, trust after
export async function createUser(input: unknown) {
  const parsed = schema.safeParse(input);
  if (!parsed.success) throw new Error('Invalid input'); // or framework-specific user-facing error
  // parsed.data is typed — do NOT parse again downstream
}
```

> Parse exactly once per request. Double-parsing is a code smell that signals unclear ownership of validation.

---

## 4. Next.js 16+ — async `params` and `searchParams`

In Next.js 16+, dynamic route `params` and `searchParams` are **Promises**. This is the single most common source of silent bugs when upgrading from 15.x.

```ts
// Route handler
export async function GET(_req: Request, { params }: { params: Promise<{ userId: string }> }) {
  const { userId } = paramsSchema.parse(await params);
  // …
}

// Server Component
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const { id } = await params;
  const sp = await searchParams;
  // …
}
```

> Forgetting `await` yields a Promise where a string is expected, which Zod parses to an error — but in TypeScript it silently compiles unless the type is explicit. Always type `params` as `Promise<…>`.

---

## 5. Response conventions — HTTP status code + body shape

Portable table. Use exactly these pairings in route handlers regardless of project:

| Situation           | Status | Body                                                        |
| ------------------- | ------ | ----------------------------------------------------------- |
| GET / PATCH OK      | 200    | `Response.json(data)`                                       |
| POST created        | 201    | `Response.json(data, { status: 201 })`                      |
| DELETE OK (no body) | 204    | `new Response(null, { status: 204 })`                       |
| Zod failure         | 400    | `{ error, message, details: error.flatten() }`              |
| Auth failure        | 401    | `{ error: 'Unauthorized' }`                                 |
| Permission failure  | 403    | `{ error: 'Forbidden', message }`                           |
| Not found           | 404    | `{ error: 'not_found', message }`                           |
| Degraded (health)   | 503    | `{ status: 'degraded', … }`                                 |
| Server error        | 500    | `{ error: 'Internal server error' }` + structured log entry |

**Rules:**

- Always pass `{ status: NNN }` — `Response.json({ error })` without status defaults to 200 with an error shape, which is worse than any honest status.
- Keep error codes stable — clients depend on them. Changing `user_exists` to `user_already_exists` breaks callers.
- Never put a stack trace in the response. Log it server-side, return a generic message.

---

## 6. Anti-patterns (framework-level, portable)

| ❌                                                         | ✅                                                                         |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| `any` on body / params                                     | Zod `safeParse` at the boundary                                            |
| Returning `{ error: '…' }` from a route without status     | Always pass `{ status: NNN }`                                              |
| `console.log` for production observability                 | Structured logger (per-project choice — `pino`, `winston`, kit's `logger`) |
| Stack traces leaked to the client                          | Generic user message + structured server log                               |
| Forgetting `await` on `params` / `searchParams` (Next 16+) | Type as `Promise<…>` and `await` before use                                |
| Zod-parsing the same input twice                           | Parse once at the boundary; trust `data` downstream                        |
| Double-purposing `'use server'` files with helpers         | Helpers in a non-`'use server'` file                                       |
| Treating `400` and `422` interchangeably                   | `400` for malformed / unparseable; `422` for parseable-but-invalid         |

---

## 7. Portable checklist

**Server Action:**

- [ ] `'use server'` at file top (never mixed with non-action exports)
- [ ] Return shape is a discriminated union (`{ data }` | `{ error }`)
- [ ] Auth guard precedes DB reads, Zod parse, and side effects
- [ ] Permission check is separate from auth (capability, not identity)
- [ ] Input validated with Zod exactly once, at the boundary (never re-parse downstream)
- [ ] User-facing errors are strings; internal details go to logs
- [ ] `revalidatePath` / `revalidateTag` called ONLY on success path
- [ ] Read-only actions (`getX`) never revalidate
- [ ] CRUD module exposes `getEntities` / `getEntityById` / `createEntity` / `updateEntity` / `deleteEntity` with stable shapes (§2.1)

**Route Handler:**

- [ ] `safeParse` for body AND params (`await params` in Next.js 16+)
- [ ] Explicit `{ status: NNN }` on every response
- [ ] Errors logged with context (scope, route, error)
- [ ] Auth check present for private endpoints
- [ ] Failure body shape: `{ error, message, details? }`

---

_Cross-reference: [`sk-api`](../sk-api/SKILL.md) — kit-shipped helpers. [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md) — CRUD orchestration. [`sk-features-index`](../sk-features-index/SKILL.md) — kit feature catalog. [`kb-db`](../kb-db/SKILL.md) / [`sk-db`](../sk-db/SKILL.md) — DB patterns. [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) / [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) — mocking patterns in action tests. [`kb-security`](../kb-security/SKILL.md) / [`sk-security`](../sk-security/SKILL.md) — NextAuth config and RBAC design._
