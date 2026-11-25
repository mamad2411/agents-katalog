---
name: backend-stack-next
description: "The server side of a Next.js app (App Router, Next 15 and 16): route handlers versus server actions, a server-only data access layer, validation, auth checks in every action and handler, caching and revalidation (Cache Components, updateTag, revalidateTag), the Node runtime and proxy.ts, database clients in serverless, environment variables, streaming, after(), rate limits, errors and tests. Read when building the backend of a Next.js project."
---

# Next.js on the server

The generated Next backend: every mutation an `/api` route the app fetches
from itself, `"use server"` functions that trust their arguments, the auth
check only in middleware, a whole database row handed to a client
component, a key in a `NEXT_PUBLIC_` variable, and a new database pool per
request on serverless. The backend rules are in the `backend` skill; pages
and components are the frontend's. These are Next's own server rules.

## 1. Know the version first

- Read `package.json`. Next 16 breaks code written from memory of 15:
  `middleware.ts` is now `proxy.ts`, `cookies()`, `headers()` and `params`
  are async only, `revalidateTag` takes a second argument, caching depends on
  `cacheComponents`, `next lint` is gone, the Edge runtime is deprecated.
- From 16.2 the docs of the installed version ship in
  `node_modules/next/dist/docs/` (the `AGENTS.md` block Next writes points
  there): read the page for the API you use before trusting memory.

## 2. Route handlers or server actions

| Need | Use |
|---|---|
| A mutation from the app's own form or button | server action |
| Data for a page | a server component calling the data access layer, never its own `/api` route |
| Webhooks, mobile or third-party clients, a public API, downloads, a specific status, header or method | route handler |
| Reads from a client component (polling, infinite scroll) | route handler, or data passed down from a server component |

- **Server actions** (`"use server"`) are public HTTP endpoints all the same:
  a POST to the page's route that anyone can send. Validate the input and
  check the user in every one. They run one at a time per client, so they
  are never used for reads, and `Promise.all` over actions does not run them
  in parallel.
- Next checks `Origin` against the host and caps an action's body at 1 MB;
  when a proxy forwards its own host, list the public one in
  `experimental.serverActions.allowedOrigins`, and raise `bodySizeLimit`
  there only for a feature that needs it.
- Several self-hosted instances share one `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`
  (and the same build). After a deploy an old tab may call an action that is
  gone ("Failed to find Server Action"): offer a reload, not a dead end.
- **Route handlers** (`app/api/.../route.ts`) export `GET`, `POST` and so on;
  `RouteContext<"/api/orders/[id]">` types the context, and `params` is a
  promise. `GET` handlers are not cached by default (15 and later).

## 3. A data access layer

- All database and business code lives in a server-only layer
  (`src/server/` or `lib/` with a folder per feature), and each module starts
  with `import "server-only"` (the `server-only` package) so it can never be
  bundled for the browser.
- Server components, actions and route handlers call its functions
  (`getOrders(user)`, `payOrder(user, id)`); they do not hold queries
  themselves. Only this layer imports the database client and the config
  that holds secrets.
- The functions take the current user and check permissions themselves
  (`backend-auth`), so every caller is covered. Middleware (`proxy.ts` in 16)
  can redirect signed-out users, but it is not authorisation.
- Return plain data objects (DTOs) with only the fields the caller may see;
  never pass a whole database row to a client component, where it is
  serialised into the page.
- A client sends an id and its change, never the record: read the rest again
  by id and owner.

```ts
// src/server/auth.ts
import "server-only";
import { cache } from "react";
import { cookies } from "next/headers";

// One lookup per request, however many components and actions ask.
export const getCurrentUser = cache(async (): Promise<User | null> => {
  const token = (await cookies()).get("session")?.value;
  return token ? verifySession(token) : null;
});

// src/server/orders.ts
export async function getOrder(user: User, id: string): Promise<OrderDTO> {
  const order = await db.query.orders.findFirst({ where: eq(orders.id, id) });
  // Someone else's order is "not found": its existence is not revealed.
  if (!order || (order.ownerId !== user.id && user.role !== "admin")) throw new NotFoundError();
  return { id: order.id, status: order.status, totalMinor: order.totalMinor, currency: order.currency };
}
```

## 4. Validation and results

- Parse input with zod (or the project's library) at the top of every action
  and handler: `const parsed = schema.safeParse(Object.fromEntries(formData))`.
- An action returns a typed result the form can show
  (`{ ok: false, errors: { quantity: "too_many" } }` or `{ ok: true, id }`)
  instead of throwing for expected failures; unexpected ones throw and reach
  `error.tsx`.
- A route handler answers with `Response.json(body, { status })` (or
  `NextResponse.json`) and the error format in `backend-errors`, from one
  helper.
- After a mutation, update the cache for what changed (section 5), then
  `redirect` if the flow moves on. `redirect()` and `notFound()` work by
  throwing: never inside a `try` whose `catch` swallows them (or call
  `unstable_rethrow(err)` first in the `catch`).

```ts
"use server";

type State = { ok: boolean; id?: string; errors?: Record<string, string>; message?: string };
const PlaceOrder = z.strictObject({
  productId: z.uuid(),
  quantity: z.coerce.number().int().min(1).max(100),
});

export async function placeOrderAction(_prev: State, formData: FormData): Promise<State> {
  const user = await getCurrentUser();
  if (!user) return { ok: false, message: "sign_in_required" };

  const parsed = PlaceOrder.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { ok: false, errors: Object.fromEntries(parsed.error.issues.map((i) => [i.path.join("."), i.code])) };
  }
  const { id } = await placeOrder(user, parsed.data); // the data layer checks stock and rights
  updateTag(`orders:${user.id}`); // the user sees their own write at once
  redirect(`/orders/${id}`);
}
```

## 5. Caching and revalidation

Check `next.config` for `cacheComponents: true` (16); the models differ.

- **Cache Components**: everything runs at request time unless cached. Cache
  a data function with `"use cache"` plus `cacheLife("hours")` and
  `cacheTag("catalogue")`. A cached scope cannot read `cookies()` or
  `headers()`, even through a helper (the build can pass and the request
  fail): read them outside and pass the values in as arguments, which join
  the cache key. Route segment `dynamic`, `revalidate` and `fetchCache` are
  removed in this mode.
- After a write: `updateTag(tag)` in a server action when the user must see
  their change (read-your-writes); `revalidateTag(tag, "max")` for
  stale-while-revalidate, from actions, route handlers and webhooks
  (`{ expire: 0 }` to expire at once outside an action); `revalidatePath` for
  one route; `refresh()` for uncached data on the current page.
- **Without it** (15, or 16 not opted in): `fetch` is not cached unless
  `cache: "force-cache"`; `unstable_cache` for database reads;
  `export const dynamic = "force-dynamic"` or `revalidate` per route;
  `revalidateTag(tag, "max")` in 16 (one argument in 15).
- Tags per record and per list (`order:${id}`, `orders:${userId}`). Data that
  depends on the user is never cached across users, and route handlers that
  return it send `Cache-Control: private, no-store`.
- The default cache lives in each instance's memory: several self-hosted
  instances need a shared cache handler (`cacheHandlers`, with
  `refreshTags()` for tag invalidation) or they serve different data.

## 6. Runtime, proxy and long work

- Routes run on the Node.js runtime (the default). `runtime = "edge"` is
  deprecated in 16; remove it rather than add it.
- `proxy.ts` (16; `middleware.ts` before, still accepted but deprecated) runs
  before every matched route on Node: redirects, rewrites, headers, a cheap
  signed-out redirect. Give it a `matcher` that excludes `_next/static`,
  `_next/image` and public files. A server action is a POST to its page, so a
  matcher that skips the page skips the action: authorisation lives in the
  data layer.
- `after(() => ...)` from `next/server` runs work once the response is sent
  (a log line, analytics, warming a cache), within the route's
  `export const maxDuration = 30` or the platform's limit. It is not a
  queue: work that must succeed or takes long goes to a job (Inngest,
  Trigger.dev, QStash, or BullMQ on a separate worker: `backend-jobs`).
- Serverless route handlers cannot hold a WebSocket; server-sent events work
  within the duration limit (`backend-realtime`).

## 7. The database client

- One client module (`src/server/db.ts`). With hot reload in development,
  keep it on `globalThis` so every reload does not open a new pool:
  ```ts
  const globalForDb = globalThis as unknown as { db?: Db };
  export const db = globalForDb.db ?? createDb();
  if (process.env.NODE_ENV !== "production") globalForDb.db = db;
  ```
- Drizzle or Prisma, with their migrations (`backend-data`), applied as a
  release step (`drizzle-kit migrate`, `prisma migrate deploy`), never
  `drizzle-kit push` against production. SQLite through `better-sqlite3` or
  libSQL needs the Node.js runtime and a writable disk: fine on a server or
  container, not on serverless platforms, which need a hosted database
  (Turso, Neon, Supabase).
- Serverless multiplies connections by instances: use an HTTP driver
  (`@neondatabase/serverless` with `drizzle-orm/neon-http`), Prisma 7 with a
  driver adapter (`@prisma/adapter-neon`, `@prisma/adapter-pg`) or Prisma
  Accelerate, or a transaction-mode pooler URL with a pool of 1 to 5. On
  Vercel's Fluid compute, `attachDatabasePool(pool)` from `@vercel/functions`
  lets idle clients close before an instance suspends.
- Prisma 7: the `prisma-client` generator with an `output` path, the URL in
  `prisma.config.ts`, `new PrismaClient({ adapter })`, and `.env` not loaded
  by itself.

## 8. Environment variables

- Server secrets without a prefix, read only in server code through the
  config module (`backend-observability`), checked at start with zod or
  `@t3-oss/env-nextjs`. `NEXT_PUBLIC_` variables are compiled into the
  browser bundle: never a key.
- `NEXT_PUBLIC_` values are frozen at `next build`: one image promoted from
  staging to production keeps staging's. A server variable read while a page
  is prerendered is baked in too; read it after `await connection()` to get
  the runtime value.
- `.env*.local` stays out of git; `loadEnvConfig` from `@next/env` loads the
  same files for Vitest and scripts.

## 9. Streams, uploads and rate limits

- Streaming (tokens from a model, progress): a route handler returns
  `new Response(stream, { headers: { "Content-Type": "text/event-stream" } })`
  and stops when `request.signal` aborts (`backend-realtime`).
- Large uploads go from the browser straight to object storage with a
  presigned URL (`backend-files`), not through a 1 MB action body.
- Rate limits on sign-in, sign-up, password reset and anything that sends
  email or costs money, in the action or handler, with a shared store
  (`@upstash/ratelimit` on Redis): an in-memory counter per serverless
  instance limits nothing.

```ts
const signIn = new Ratelimit({ redis: Redis.fromEnv(), limiter: Ratelimit.slidingWindow(5, "1 m") });
const { success, reset } = await signIn.limit(`sign-in:${ip}`);
if (!success) return { ok: false, message: "rate_limited", retryAfter: Math.ceil((reset - Date.now()) / 1000) };
```

## 10. Errors

- An unexpected throw in a page or action renders the nearest `error.tsx` (a
  client component); in production its message is replaced by a generic one
  with a `digest` that matches the server log. `global-error.tsx` covers the
  root layout; `notFound()` renders `not-found.tsx`; `forbidden()` and
  `unauthorized()` need `experimental.authInterrupts`.
- `instrumentation.ts` exports `onRequestError` to report server errors (the
  Sentry SDK provides one) and `register()` for OpenTelemetry
  (`backend-observability`).

## 11. Tests

- The data layer with Vitest against a test database (`backend-testing`).
- Actions and handlers called as functions: `await placeOrderAction(prev,
  formData)`, `await GET(new NextRequest(url), { params: Promise.resolve({ id }) })`,
  with the session helper, `next/cache` and `next/navigation` mocked
  (`redirect` throws, so assert the rejection).
- The `server-only` package throws outside Next: add
  `vi.mock("server-only", () => ({}))` to the Vitest setup file.
- Forms end to end with Playwright against `next build && next start`
  (`testing-e2e`).

## Check it

`next build` type-checks (Next 16 no longer lints: run `eslint .` or
`biome check`); `next typegen` refreshes the route types. The build's route
list marks each route static or dynamic: one that shows user data must be
dynamic. Call route handlers with `curl` against `next start`, since
`next dev` caches differently; test actions and the data layer with Vitest.

## Avoid

`"use server"` functions with no validation or user check; queries written in
page components; a whole row passed to a client component; the auth check
only in middleware or `proxy.ts`; an action used to fetch data; a page
fetching its own `/api` route; `redirect` inside a swallowing `try`;
`cookies()` inside `"use cache"`; user data in a shared cache; a Prisma or
Drizzle client created per request or per reload; SQLite on a serverless
deploy; a secret in a `NEXT_PUBLIC_` variable; long work in `after()`
instead of a queue.
