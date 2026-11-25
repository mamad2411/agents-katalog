---
name: backend-stack-node
description: "A Node.js API in TypeScript: the Node version, strict ESM setup, Hono, Fastify, Express or NestJS, validation with zod, problem-details errors, config at start, Drizzle, Prisma or Kysely, pino with request ids, graceful shutdown, the event loop with worker threads and streams, outbound timeouts, BullMQ jobs, OpenTelemetry, tests with Vitest. Read when building or changing a Node.js backend."
---

# Node.js with TypeScript

The generated Node API: Express 4 with `any` bodies, a `try/catch` in every
handler answering `res.status(500).send(err.message)`, `process.env` read in
twenty files, `console.log`, a database client per request, a CPU-heavy loop
that stalls every other request, and no shutdown, so each deploy drops
requests. The backend rules are in the `backend` skill; these are Node's own.

## 1. Setup

- Node: the active LTS for a new service, 24 in 2026 (22 is maintained until
  April 2027, 20 is end of life, 26 becomes LTS in October 2026); never an
  odd-numbered release in production. The same major in `package.json`
  `engines`, `.nvmrc` and the Docker base image.
- TypeScript with `strict` on, ES modules (`"type": "module"`). The
  project's package manager (pnpm, npm, yarn, bun), one lock file.
- `tsconfig.json`: `"module": "nodenext"`, `"target": "es2024"`, `"strict"`,
  `"noUncheckedIndexedAccess"`, `"verbatimModuleSyntax"`, `"outDir": "dist"`
  and `"types": ["node"]` (a recent `tsc --init` writes `"types": []`,
  which hides Node's globals). Relative imports end in `.js`.
- Development with `tsx watch src/index.ts`; production runs the compiled
  output (`tsc` or `tsup` to `dist/`), not `ts-node` or tsx. Node 22.18+ and
  24 also run TypeScript directly (`node src/index.ts`) when it is erasable
  only (`erasableSyntaxOnly`: no enums, namespaces or constructor parameter
  properties) with `.ts` import paths: good for scripts; compile the service.
- `node --env-file-if-exists=.env` loads a local `.env` (Node 22.9+) without
  dotenv; production gets real variables from the platform.

Framework: the project's; for a new API, by this table.

| Framework | Choose it when |
|---|---|
| Hono | a new API of any size: web-standard `Request` and `Response`, typed routes, runs on Node, Bun, Deno and Workers |
| Fastify | plugins, schema-validated routes and response serialisation, pino built in |
| Express 5 | the project already uses Express; v5 sends rejected promises to the error handler (v4 needs a wrapper) |
| NestJS | a large team that wants modules, dependency injection and decorators, and accepts the ceremony |

## 2. Layout

```
src/
  index.ts          start: config, app, server, shutdown
  app.ts            the app and its routes, exported for tests
  config.ts         env parsed with zod
  instrumentation.ts  OpenTelemetry, loaded before everything (section 11)
  worker.ts         the job worker's own entry point
  lib/              db, logger, errors
  orders/
    routes.ts       HTTP: parse, call the service, respond
    service.ts      rules and transactions
    repository.ts   queries
    schemas.ts      zod schemas and the types inferred from them
    orders.test.ts
```

## 3. Config at start

`config.ts` parses `process.env` with a zod schema (`z.coerce.number()` for
ports, `z.url()` for URLs, no default for secrets); on failure it prints the
variable names, never the values, and exits `1` (`backend-observability`).
Nothing else reads `process.env`.

## 4. Validation and errors

- zod schemas at the edge (`@hono/zod-validator`; for Fastify,
  `fastify-type-provider-zod` with `setValidatorCompiler(validatorCompiler)`
  and response schemas that drop undeclared fields; `schema.parse` in
  Express), with `z.infer` for the types, shared with a TypeScript client
  when there is one.
- `z.coerce` for query strings and path parameters, `z.strictObject()` (zod
  4; `.strict()` in 3) or copying fields to refuse extra keys (`backend-api`).
- An `AppError` class with a `code` and a status, thrown from services; one
  error handler (`app.onError` in Hono, `setErrorHandler` in Fastify, the
  final middleware in Express, an exception filter in NestJS) maps it, zod
  errors and the unexpected into the format in `backend-errors`. No
  `try/catch` around each handler.

```ts
export class AppError extends Error { // plain fields: erasable, works with type stripping
  readonly status: number; readonly code: string; readonly errors: FieldError[];
  constructor(status: number, code: string, errors: FieldError[] = []) {
    super(code); this.status = status; this.code = code; this.errors = errors;
  }
}
// ["lines", 0, "quantity"] -> "lines[0].quantity"
const fieldPath = (path: PropertyKey[]) => path.reduce<string>((acc, p) =>
  typeof p === "number" ? `${acc}[${p}]` : acc ? `${acc}.${String(p)}` : String(p), "");
export const fromZod = (error: z.core.$ZodError) =>
  new AppError(400, "validation_failed", error.issues.flatMap((i) =>
    i.code === "unrecognized_keys"
      ? i.keys.map((k) => ({ field: fieldPath([...i.path, k]), code: "unknown_field" }))
      : [{ field: fieldPath(i.path), code: i.code }]));

app.post("/orders",
  zValidator("json", PlaceOrder, (r) => { if (!r.success) throw fromZod(r.error); }),
  async (c) => {
    const order = await orders.place(c.get("user"), c.req.valid("json"));
    return c.json(order, 201, { Location: `/orders/${order.id}` });
  });

app.onError((err, c) => {
  const e = err instanceof AppError ? err
    : err instanceof HTTPException ? new AppError(err.status, "http_error") // e.g. 413 from bodyLimit
    : new AppError(500, "internal");
  const requestId = c.get("requestId");
  if (e.status >= 500) logger.error({ err, requestId }, "request failed"); // the one log line
  const body = { type: `https://example.com/errors/${e.code.replaceAll("_", "-")}`, status: e.status,
    code: e.code, ...(e.errors.length && { errors: e.errors }), ...(e.status >= 500 && { requestId }) };
  return c.body(JSON.stringify(body), e.status as ContentfulStatusCode,
    { "Content-Type": "application/problem+json" });
});
```

## 5. Data

- Drizzle (SQL-shaped and light, `drizzle-kit` migrations), Prisma
  (schema-first; Prisma 7 needs a driver adapter such as `@prisma/adapter-pg`
  and a `prisma.config.ts`) or Kysely (a typed query builder, types from
  `kysely-codegen`): the project's choice, one client from `lib/db.ts`;
  `backend-data` for the rest.
- Inside `db.transaction(async (tx) => ...)` every query uses `tx`; one
  written against `db` runs outside the transaction and is not rolled back.
- node-postgres returns `bigint` and `numeric` columns as strings: Drizzle's
  `bigint({ mode: "number" })` only while values stay under 2^53; money as
  integer minor units. Times as `timestamp({ withTimezone: true })`.
- One `pg.Pool` per process (`max: 10`, `connectionTimeoutMillis: 5_000` so
  a starved pool fails fast), sized against the database's limit across all
  instances. Migrations: `drizzle-kit generate` then `migrate`, or `prisma
  migrate deploy` at release; `drizzle-kit push` only on a scratch database.

```ts
// Race-free: the check and the write are one statement; 0 rows means not enough stock.
const rows = await tx.update(products)
  .set({ stock: sql`${products.stock} - ${qty}` })
  .where(and(eq(products.id, productId), gte(products.stock, qty)))
  .returning({ id: products.id });
if (rows.length === 0) throw new AppError(409, "out_of_stock");
```

## 6. Logging

- pino as the logger (Fastify's built-in one, or `hono-pino`), with a
  request id and a child logger per request; `pino-pretty` only in
  development. Hono's `requestId()` (`hono/request-id`) reuses a valid
  incoming `X-Request-Id` and returns it; Fastify 5 ignores incoming ids
  unless `requestIdHeader` is set, and generates them with `genReqId`.
- `AsyncLocalStorage` puts the id on every line written during the request,
  with no logger passed around; `redact` keeps secrets out:

```ts
export const requestContext = new AsyncLocalStorage<{ requestId: string; userId?: string }>();
export const logger = pino({
  level: config.LOG_LEVEL,
  mixin: () => requestContext.getStore() ?? {},
  redact: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token"],
});
app.use(async (c, next) => {
  const started = performance.now();
  await requestContext.run({ requestId: c.get("requestId") }, next);
  logger.info({ method: c.req.method, route: c.req.routePath, status: c.res.status,
    ms: Math.round(performance.now() - started) }, "request");
});
```

## 7. Shutdown

```ts
import { setTimeout as sleep } from "node:timers/promises";

const server = serve({
  fetch: app.fetch,
  port: config.PORT,
  // Longer than the load balancer's idle timeout (60s on an AWS ALB), or it sees 502s.
  serverOptions: { keepAliveTimeout: 65_000, headersTimeout: 66_000 },
});
async function shutdown(signal: string) {
  logger.info({ signal }, "shutting down");
  ready = false;                                   // /readyz answers 503
  setTimeout(() => process.exit(1), 20_000).unref(); // the hard limit
  await sleep(5_000);                               // let the load balancer notice
  server.close(async () => {                        // in-flight requests finish first
    await worker?.close(); await sdk.shutdown(); await pool.end();
    process.exit(0);
  });
}
for (const signal of ["SIGINT", "SIGTERM"]) process.once(signal, () => void shutdown(signal));
```

- `server.close()` stops accepting, and since Node 19 closes idle keep-alive
  connections too. `headersTimeout` must not exceed `requestTimeout` (default
  300 seconds; Node refuses to start otherwise), and `requestTimeout` limits
  receiving the request, not the handler's time. Fastify: `await app.close()`
  answers `503` meanwhile; its `keepAliveTimeout` is already 72 seconds.
- And `process.on("unhandledRejection")` logs and exits, so a bug is not left
  running in a broken state. Run as `node dist/index.js` in exec form, not
  through `npm start`: an npm or shell parent may not pass `SIGTERM` on.

## 8. The event loop

- One thread runs every request's JavaScript: 100 ms of CPU in one handler
  delays every request waiting behind it. Watch the p99 of
  `monitorEventLoopDelay()`; above about 100 ms something blocks.
- No `*Sync` calls (`readFileSync`, `pbkdf2Sync`, `gzipSync`) in handlers;
  password hashing through the async API of `argon2` or `bcrypt`.
- CPU-bound work (a report, parsing a big file) in worker threads through a
  Piscina pool (`maxThreads` about the cores minus one, `pool.run(data, {
  signal })`), or in a job.
- The libuv pool (file system, `dns.lookup`, crypto, zlib) has 4 threads by
  default; `UV_THREADPOOL_SIZE=8` to 16 for crypto- or file-heavy services.
- Large payloads as streams, never buffered: `pipeline()` from
  `node:stream/promises`, a database cursor streamed out as CSV, uploads
  sent straight to object storage (`backend-files`). Body limits before
  parsing: Hono `bodyLimit({ maxSize: 1024 * 1024 })`, Fastify's `bodyLimit`
  (1 MiB by default), `express.json({ limit: "1mb" })` (100 kB by default).

## 9. Outbound calls

- `fetch` with a deadline, joined to the request's own signal so the call
  stops when the client leaves: `signal: AbortSignal.any([c.req.raw.signal,
  AbortSignal.timeout(5_000)])`. `TimeoutError` and `AbortError` are
  different failures (`backend-errors`). One client module per provider,
  retries only for idempotent calls (`backend-integrations`).

## 10. Jobs

- BullMQ on Redis, the worker in its own process (`src/worker.ts`) scaled
  apart from the API; pg-boss or graphile-worker when PostgreSQL is all there
  is (`backend-jobs`). Its connection needs `maxRetriesPerRequest: null`,
  Redis runs with `maxmemory-policy noeviction`, and job ids never hold `:`.

```ts
const connection = new Redis(config.REDIS_URL, { maxRetriesPerRequest: null });
export const emails = new Queue<{ orderId: string }>("emails", {
  connection,
  defaultJobOptions: { attempts: 5, backoff: { type: "exponential", delay: 1_000 },
    removeOnComplete: { count: 1_000 }, removeOnFail: { age: 7 * 24 * 3600 } },
});
// A second add with the same id is ignored while the first is stored.
await emails.add("receipt", { orderId }, { jobId: `receipt-${orderId}` });
```

## 11. OpenTelemetry

`src/instrumentation.ts` starts `NodeSDK` with the auto-instrumentations and
registers the ESM loader hook; run `node --import ./dist/instrumentation.js
dist/index.js` (code in `backend-observability`). Route names come from
`@hono/otel` or `@fastify/otel`; Express and pg are covered by the defaults.

## 12. Tests

Vitest; the app exported from `app.ts` and called without a port
(`app.request("/orders")` in Hono, `app.inject()` in Fastify, supertest for
Express); a real database per `backend-testing`; MSW for other services.
A validation test sends several faults at once and asserts the whole
`errors` list (`lines[0].quantity` `too_small`, `role` `unknown_field`), not
only the `400`.

## Check it

`tsc --noEmit`, the linter (ESLint or Biome), the tests, then start it and
call the endpoints with `curl`: a bad body gives a `400` listing every field,
a 2 MB body a `413`, and `kill -TERM` during a slow request lets it finish
and exits `0`. `npm audit --omit=dev` (or `pnpm audit --prod`) for known
vulnerabilities.

## Avoid

`any` for request bodies; a `try/catch` in every handler; `process.env` read
outside `config.ts`; `console.log` as the logger; `ts-node` in production;
Express 4 async handlers without error handling; a floating promise for work
that must finish; queries on `db` inside a transaction; `*Sync` calls or CPU
loops in handlers; `fetch` without a timeout; a server with no shutdown
handler; `npm start` as the container command; BullMQ job ids with `:`.
