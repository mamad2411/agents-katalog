---
name: express-api
description: Express API conventions, as an alternative to Next.js route handlers for projects with a separate API server. Covers middleware order, the auth→validate→handle route pattern, service layer boundaries, a singleton DB client, and integration testing against a real running server. Use when the project has a standalone Express app (server.ts / app.ts) rather than app/api routes.
---

Apply the following conventions to standalone Express API projects. Check for an `app.ts`/`server.ts` with `express()` before applying this — if routes live under Next.js's `app/api/`, use route-handler conventions instead.

## Middleware order is load-bearing

Express runs middleware in registration order, and several of these have a *correctness* dependency on being before or after another — not just style:

```ts
// app.ts
import 'dotenv/config'; // or Doppler-injected env — must be first
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import cookieParser from 'cookie-parser';

initTelemetry(); // Sentry/OTel init — before anything that could throw

assertRequiredEnvVars(['DATABASE_URL', 'STRIPE_SECRET_KEY', 'SESSION_SECRET']); // fail fast

const app = express();

app.use(cors({ origin: ALLOWED_ORIGINS, credentials: true }));
app.use(helmet());
app.use(compression());

// Raw-body webhook routes MUST be mounted BEFORE the json body parser.
// Stripe (and most webhook senders) verify a signature over the exact raw
// bytes; once express.json() has parsed and re-serialized the body, the
// signature no longer matches the bytes you'd re-stringify.
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), stripeWebhookHandler);

app.use(express.json());
app.use(cookieParser());
app.use(requestLogger);

app.use(sessionMiddleware);

app.use('/api', apiRouter);

app.use(notFoundHandler); // 404 — after all routes
app.use(errorHandler); // error middleware — last, 4 args
```

The order that matters most: **env/secrets → telemetry init → CORS → helmet → compression → raw-body webhook routes → `express.json()` → cookie parser → request logging → env-var assertions/session/auth → routes → 404 → error handler.** Moving the webhook route after `express.json()` is the single most common way to silently break webhook signature verification — it still 200s in local testing with a mocked signature and only fails against the real provider.

## Route handler pattern

Every route: auth middleware → schema-driven validation middleware → handler. The handler is wrapped so a thrown/rejected error reaches Express's error middleware instead of hanging the request:

```ts
router.post(
  '/projects',
  requireAuth,
  validateRequest({ body: createProjectSchema }),
  async (req, res, next) => {
    try {
      const project = await projectService.create(req.auth.userId, req.body);
      res.status(201).json(project);
    } catch (err) {
      next(err); // never let an async handler throw unhandled
    }
  },
);
```

An `async` route handler that throws does **not** automatically reach Express's error handler (true for Express 4; Express 5 changes this, but don't rely on the major version without checking `package.json`) — the `try/catch` + `next(err)` is the safety net either way, and it's cheap enough to always write.

## Service layer — routes never touch the ORM directly

Route handlers call services; services own the database client and business logic. This keeps handlers testable without a DB and keeps the persistence layer swappable:

```ts
// services/projectService.ts
export const projectService = {
  create: async (userId: string, input: CreateProjectInput) => {
    return prisma.project.create({ data: { ...input, ownerId: userId } });
  },
  listForUser: async (userId: string) => {
    return prisma.project.findMany({ where: { ownerId: userId } });
  },
};
```

If a route imports `prisma` (or any ORM/DB client) directly, that's a signal the logic belongs in a service instead.

## One DB client instance, not one per module

Instantiate the client once and import the singleton everywhere — never `new PrismaClient()` (or equivalent) inside a route file or service module:

```ts
// lib/db.ts
export const prisma = new PrismaClient();
```

Multiple instances each open their own connection pool; under serverless or hot-reload dev servers this exhausts DB connections fast. Every service imports `{ prisma } from '../lib/db'`.

## Integration testing: a managed test server, not a mocked app

Rather than mocking Express internals, boot the real app against a real (ephemeral or dedicated test) database, wait for it to be healthy, then run the test suite against the live server over HTTP. This catches middleware-order bugs, real serialization, and real DB constraints that an in-process mock would hide:

```ts
// test/managedServer.ts
export const startTestServer = async () => {
  process.env.DATABASE_URL = TEST_DATABASE_URL;
  const server = app.listen(0); // ephemeral port
  const port = (server.address() as AddressInfo).port;

  await waitOn({ resources: [`http://localhost:${port}/health`], timeout: 15_000 });

  return { server, baseUrl: `http://localhost:${port}` };
};

export const stopTestServer = (server: Server) => new Promise((resolve) => server.close(resolve));
```

```ts
// projects.integration.test.ts
let ctx: Awaited<ReturnType<typeof startTestServer>>;
beforeAll(async () => (ctx = await startTestServer()));
afterAll(() => stopTestServer(ctx.server));

it('creates a project', async () => {
  const res = await fetch(`${ctx.baseUrl}/api/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${testToken}` },
    body: JSON.stringify({ name: 'Test' }),
  });
  expect(res.status).toBe(201);
});
```

Reserve this for the handful of flows worth exercising end-to-end (auth, payments, anything crossing multiple services); unit-test individual services and validation schemas in isolation for everything else — booting the full server per test file is slower than mocking, by design, in exchange for realism.
