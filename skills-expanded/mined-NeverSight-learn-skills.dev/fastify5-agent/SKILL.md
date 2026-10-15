---
name: fastify5-agent-skill
description: >
  Production Fastify 5 (TypeScript) patterns: schema validation, plugins, typed routes,
  error handling, security hardening, logging, testing with inject, and graceful shutdown.
  Use this skill whenever the user is building a Node.js/TypeScript API with Fastify,
  setting up route validation with Zod or TypeBox, creating Fastify plugins, adding
  security middleware (Helmet, CORS, rate limiting), writing tests using Fastify's inject
  method, or configuring graceful shutdown. Also trigger when the user asks about Fastify
  vs Express, Zod vs TypeBox type providers, or any Fastify plugin architecture question.
---

# Fastify 5 Production Patterns (TypeScript)

Fastify 5 is schema-first and type-safe by design. Key changes from v4:
- `reply.send()` is deprecated — `return` values from route handlers instead
- Full async/await throughout (no callback-style plugin registration)
- TypeBox v0.31+ required for the TypeBox type provider
- Stricter TypeScript types throughout

---

## Quick Start

### Minimal server

✅ **Correct: basic server with typed response**

```ts
import Fastify from "fastify";

const app = Fastify({ logger: true });

app.get("/health", async () => ({ status: "ok" as const }));

await app.listen({ host: "0.0.0.0", port: 3000 });
```

❌ **Wrong: start server without awaiting listen**

```ts
app.listen({ port: 3000 });
console.log("started"); // races startup and hides bind failures
```

---

## Dependencies & tsconfig

```bash
npm install fastify @fastify/helmet @fastify/cors @fastify/rate-limit fastify-plugin
npm install -D typescript @types/node vitest
# Choose one type provider:
npm install @fastify/type-provider-typebox @sinclair/typebox
# OR
npm install fastify-type-provider-zod zod
```

**tsconfig.json** (minimum):
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist"
  }
}
```

---

## Schema Validation + Type Providers

Fastify validates requests/responses via JSON schema. Use a type provider so runtime validation and static types stay in sync — no duplicate type definitions needed.

### Zod provider (recommended for full-stack TypeScript)

✅ **Correct: Zod schema drives validation + types**

```ts
import Fastify from "fastify";
import { z } from "zod";
import {
  ZodTypeProvider,
  serializerCompiler,
  validatorCompiler,
} from "fastify-type-provider-zod";

const app = Fastify({ logger: true });

// Required: register Zod compilers before using the type provider
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

const typedApp = app.withTypeProvider<ZodTypeProvider>();

const QuerySchema = z.object({ q: z.string().min(1) });

typedApp.get(
  "/search",
  { schema: { querystring: QuerySchema } },
  async (req) => {
    return { q: req.query.q }; // req.query is typed as { q: string }
  },
);

await app.listen({ port: 3000 });
```

❌ **Wrong: forget to set validator/serializer compilers**

```ts
// This compiles but validation silently does nothing at runtime
const app = Fastify().withTypeProvider<ZodTypeProvider>();
```

### TypeBox provider (recommended for OpenAPI + performance)

TypeBox schemas are plain JSON Schema at runtime — zero transformation overhead.

✅ **Correct: TypeBox schema**

```ts
import Fastify from "fastify";
import { Type } from "@sinclair/typebox";
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";

const app = Fastify({ logger: true }).withTypeProvider<TypeBoxTypeProvider>();

const Params = Type.Object({ id: Type.String({ minLength: 1 }) });
const Reply = Type.Object({ id: Type.String() });

app.get(
  "/users/:id",
  { schema: { params: Params, response: { 200: Reply } } },
  async (req) => ({ id: req.params.id }),
);

await app.listen({ port: 3000 });
```

---

## Plugin Architecture

Plugins create isolated scopes — decorators, hooks, and routes inside a plugin don't leak out. This is the primary tool for keeping codebases organised.

✅ **Correct: typed route plugin**

```ts
import type { FastifyPluginAsync } from "fastify";
import { Type } from "@sinclair/typebox";
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";

const Params = Type.Object({ id: Type.String() });

export const usersRoutes: FastifyPluginAsync = async (app) => {
  const typed = app.withTypeProvider<TypeBoxTypeProvider>();

  typed.get("/", async () => [{ id: "1" }]);
  typed.get(
    "/:id",
    { schema: { params: Params } },
    async (req) => ({ id: req.params.id }),
  );
};
```

❌ **Wrong: cast params with `as any` to dodge types**

```ts
app.get("/:id", async (req) => ({ id: (req.params as any).id }));
```

✅ **Correct: register with a prefix**

```ts
app.register(usersRoutes, { prefix: "/api/v1/users" });
```

Use `fastify-plugin` (`fp`) when a plugin's decorators must be visible to the parent scope — e.g. a database plugin that decorates `app.db`:

```ts
// src/plugins/db.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

declare module "fastify" {
  interface FastifyInstance {
    db: DatabaseClient;
  }
}

const dbPlugin: FastifyPluginAsync = async (app) => {
  const client = await connectToDatabase();
  app.decorate("db", client);
  app.addHook("onClose", async () => { await client.disconnect(); });
};

export default fp(dbPlugin, { name: "db" });
```

**Rule of thumb**: wrap infrastructure plugins (db, auth, config) with `fp`; keep route plugins as plain `FastifyPluginAsync` so they stay encapsulated.

---

## Error Handling

Centralize unexpected failures and return a stable error shape. Log the real error server-side; send a safe message to the client.

✅ **Correct: setErrorHandler with validation awareness**

```ts
app.setErrorHandler((err, req, reply) => {
  // Fastify marks validation errors with err.validation
  if (err.validation) {
    return reply.status(400).send({
      error: "validation_error",
      message: err.message,
    });
  }

  req.log.error({ err }, "request failed");
  reply.status(err.statusCode ?? 500).send({ error: "internal" });
});
```

For domain errors, define typed classes and check them in the handler:

```ts
export class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} ${id} not found`);
    this.name = "NotFoundError";
  }
}

// In setErrorHandler:
if (err instanceof NotFoundError) {
  return reply.status(404).send({ error: err.message });
}
```

Route handlers can simply throw — Fastify catches and routes to the error handler:

```ts
async (request) => {
  const user = await db.findUser(request.params.id);
  if (!user) throw new NotFoundError("User", request.params.id);
  return user;
}
```

---

## Security Hardening

Add standard security plugins and enforce payload limits early in the plugin registration order.

✅ **Correct: Helmet + CORS + rate limiting**

```ts
import helmet from "@fastify/helmet";
import cors from "@fastify/cors";
import rateLimit from "@fastify/rate-limit";

await app.register(helmet);
await app.register(cors, { origin: false });
await app.register(rateLimit, { max: 100, timeWindow: "1 minute" });
```

**Per-route rate limit override:**

```ts
{
  schema: { ... },
  config: { rateLimit: { max: 5, timeWindow: "1 minute" } }
}
```

**CORS with environment-driven origins:**

```ts
await app.register(cors, {
  origin: process.env.ALLOWED_ORIGINS?.split(",") ?? false,
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true,
});
```

---

## Logging

Fastify uses Pino. Always log context via `request.log` inside handlers — it automatically includes `reqId`.

```ts
async (request) => {
  request.log.info({ userId: request.params.id }, "Fetching user");
  return db.findUser(request.params.id);
}
```

**Redact sensitive fields** in the Fastify config:

```ts
const app = Fastify({
  logger: {
    level: process.env.LOG_LEVEL ?? "info",
    redact: ["req.headers.authorization", "req.body.password"],
    ...(process.env.NODE_ENV === "development" && {
      transport: { target: "pino-pretty" },
    }),
  },
});
```

---

## Graceful Shutdown

Close the HTTP server and downstream clients (DB pools, message queues) on SIGINT/SIGTERM.

✅ **Correct: close on signals**

```ts
const close = async (signal: string) => {
  app.log.info({ signal }, "shutting down");
  await app.close();
  process.exit(0);
};

process.on("SIGINT", () => void close("SIGINT"));
process.on("SIGTERM", () => void close("SIGTERM"));
```

Full server entrypoint with factory function (keeps app.ts testable):

```ts
// src/app.ts
export async function buildApp() {
  const app = Fastify({ logger: true });
  await app.register(securityPlugins);
  await app.register(userRoutes, { prefix: "/api/users" });
  return app;
}

// src/server.ts
const app = await buildApp();

process.on("SIGINT", () => void close("SIGINT"));
process.on("SIGTERM", () => void close("SIGTERM"));

try {
  await app.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
} catch (err) {
  app.log.error(err);
  process.exit(1);
}
```

---

## Testing (Fastify inject)

Test routes in-memory without binding a port. Create a fresh Fastify instance per test for isolation.

✅ **Correct: inject request**

```ts
import Fastify from "fastify";
import { describe, it, expect } from "vitest";
import { usersRoutes } from "../src/routes/users.js";

describe("users", () => {
  it("returns a user by id", async () => {
    const app = Fastify();
    await app.register(usersRoutes, { prefix: "/users" });

    const res = await app.inject({ method: "GET", url: "/users/1" });
    expect(res.statusCode).toBe(200);
    expect(res.json()).toHaveProperty("id", "1");
  });

  it("rejects missing required fields", async () => {
    const app = Fastify();
    await app.register(usersRoutes, { prefix: "/users" });

    const res = await app.inject({
      method: "POST",
      url: "/users",
      payload: { name: "" },
    });
    expect(res.statusCode).toBe(400);
  });
});
```

For tests that span the full app (auth, security headers, etc.), use the `buildApp` factory:

```ts
import { buildApp } from "../src/app.js";

const app = await buildApp();
const res = await app.inject({
  method: "GET",
  url: "/protected",
  headers: { authorization: "Bearer test-token" },
});
await app.close();
```

---

## Decision Trees

### Fastify vs Express

- Prefer **Fastify** for schema-based validation, predictable plugin encapsulation, and high throughput.
- Prefer **Express** for minimal middleware stacks and maximal ecosystem familiarity.

### Zod vs TypeBox

- Prefer **Zod** when the codebase already standardizes on Zod (forms, tRPC, shared validation).
- Prefer **TypeBox** for auto-generated OpenAPI specs and performance-critical validation.

---

## Anti-Patterns to Avoid

- **Skipping request validation.** Always validate at boundaries with schemas — never trust raw input.
- **Dumping everything in `server.ts`.** Isolate routes and dependencies into separate plugins.
- **Leaking raw error objects to clients.** Return stable error shapes; log full details server-side.
- **Using `as any` to silence type errors.** Use a type provider or typed schemas instead.
- **Not awaiting `app.listen()`.** This races startup and silently hides bind failures.
- **Forgetting Zod compilers.** Call `setValidatorCompiler` / `setSerializerCompiler` before `withTypeProvider` — skipping them means validation silently does nothing at runtime.

---

## Resources

- [Fastify docs](https://www.fastify.io/)
- [fastify-type-provider-zod](https://github.com/turkerdev/fastify-type-provider-zod)
- [@fastify/type-provider-typebox](https://github.com/fastify/fastify-type-provider-typebox)
