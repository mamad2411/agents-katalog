---
name: "fastify"
description: "Fastify REST API: schema-first validation, plugin architecture, hooks lifecycle, TypeScript, Pino logging, JWT auth, Swagger, and production patterns for high-throughput Node.js services"
---

# Fastify Skill

## When to activate
- Building a REST API with Fastify
- Migrating an Express service to Fastify for performance gains
- Adding schema validation, JWT auth, or Swagger docs to a Fastify app
- Setting up the plugin/encapsulation model for a modular Fastify service
- Writing tests with `fastify.inject()` (no live HTTP server)
- Any task where the user references `fastify`, `@fastify/*`, or `fastify-plugin`

## When NOT to use
- Edge deployments — use the hono skill (Cloudflare Workers, Deno Deploy)
- Full-stack framework with SSR — use the nextjs or remix skill
- The user explicitly wants Express middleware ecosystem compatibility

## Instructions

### Project setup and structure

```
Set up a production-ready Fastify project with TypeScript.

Language: TypeScript
Database: [PostgreSQL / MongoDB / none]
Auth: [JWT / none]
Swagger: [yes / no]

Directory structure:
src/
  app.ts            ← Fastify instance + plugin registration (no listen here)
  server.ts         ← entry point (listen + graceful shutdown)
  plugins/
    sensible.ts     ← @fastify/sensible for standard HTTP errors
    jwt.ts          ← fastify-jwt plugin (scoped auth decorator)
    swagger.ts      ← @fastify/swagger + @fastify/swagger-ui
  routes/
    index.ts        ← route aggregator
    users/
      index.ts      ← users route definitions with JSON Schema
      schema.ts     ← TypeBox schemas for request/response
  hooks/
    auth.ts         ← onRequest hook for JWT verification
  types/
    index.ts        ← module augmentation for fastify decorators

// src/app.ts
import Fastify from 'fastify'
import sensible from '@fastify/sensible'
import cors from '@fastify/cors'
import { jwtPlugin } from './plugins/jwt'
import { swaggerPlugin } from './plugins/swagger'
import { usersRoutes } from './routes/users'

export function buildApp(opts = {}) {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL ?? 'info',
      // Pino redact — never log secrets
      redact: ['req.headers.authorization', 'body.password'],
    },
    ajv: {
      customOptions: { removeAdditional: 'all', coerceTypes: true },
    },
    ...opts,
  })

  // Core plugins
  app.register(sensible)
  app.register(cors, { origin: process.env.ALLOWED_ORIGINS?.split(',') ?? [] })

  // Auth + docs
  app.register(jwtPlugin)
  app.register(swaggerPlugin)

  // Health check — outside auth scope
  app.get('/health', { schema: { hide: true } }, async () => ({ status: 'ok' }))

  // Versioned routes
  app.register(usersRoutes, { prefix: '/api/v1/users' })

  return app
}

// src/server.ts
import { buildApp } from './app'

const app = buildApp()
const PORT = Number(process.env.PORT ?? 3000)

const start = async () => {
  try {
    await app.listen({ port: PORT, host: '0.0.0.0' })
  } catch (err) {
    app.log.error(err)
    process.exit(1)
  }
}

// Graceful shutdown
const stop = async () => {
  await app.close()
  process.exit(0)
}

process.on('SIGTERM', stop)
process.on('SIGINT', stop)

start()
```

### Schema-first validation with TypeBox

```
Add TypeBox schemas for [resource] routes. TypeBox generates both the
TypeScript type and the JSON Schema for Fastify AJV in one declaration.

// src/routes/users/schema.ts
import { Type, Static } from '@sinclair/typebox'

export const UserSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  role: Type.Union([Type.Literal('admin'), Type.Literal('user')]),
  createdAt: Type.String({ format: 'date-time' }),
})

export const CreateUserBody = Type.Object({
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  password: Type.String({ minLength: 8 }),
})

export const UpdateUserBody = Type.Partial(
  Type.Pick(CreateUserBody, ['name', 'email'])
)

export const UserParams = Type.Object({
  id: Type.String({ format: 'uuid' }),
})

export const UserListQuery = Type.Object({
  page: Type.Optional(Type.Integer({ minimum: 1, default: 1 })),
  limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 100, default: 20 })),
})

// Inferred TypeScript types — no duplication
export type User = Static<typeof UserSchema>
export type CreateUserBody = Static<typeof CreateUserBody>
export type UpdateUserBody = Static<typeof UpdateUserBody>
export type UserParams = Static<typeof UserParams>
export type UserListQuery = Static<typeof UserListQuery>

// src/routes/users/index.ts
import { FastifyPluginAsync } from 'fastify'
import {
  UserSchema, CreateUserBody, UpdateUserBody, UserParams, UserListQuery,
} from './schema'
import { Type } from '@sinclair/typebox'

export const usersRoutes: FastifyPluginAsync = async (app) => {
  // GET /users — public or protected depending on onRequest hook below
  app.get<{ Querystring: UserListQuery }>('/', {
    schema: {
      querystring: UserListQuery,
      response: {
        200: Type.Object({
          users: Type.Array(UserSchema),
          total: Type.Integer(),
          page: Type.Integer(),
        }),
      },
      tags: ['Users'],
    },
  }, async (req) => {
    const { page = 1, limit = 20 } = req.query
    // fetch from DB
    return { users: [], total: 0, page }
  })

  app.post<{ Body: CreateUserBody }>('/', {
    schema: {
      body: CreateUserBody,
      response: { 201: UserSchema },
      tags: ['Users'],
    },
  }, async (req, reply) => {
    // create user
    const user = { id: crypto.randomUUID(), ...req.body, role: 'user', createdAt: new Date().toISOString() }
    return reply.code(201).send(user)
  })

  app.get<{ Params: UserParams }>('/:id', {
    schema: { params: UserParams, response: { 200: UserSchema }, tags: ['Users'] },
  }, async (req, reply) => {
    const user = null // await db.findById(req.params.id)
    if (!user) throw reply.notFound(`User ${req.params.id} not found`)
    return user
  })

  app.patch<{ Params: UserParams; Body: UpdateUserBody }>('/:id', {
    schema: { params: UserParams, body: UpdateUserBody, response: { 200: UserSchema }, tags: ['Users'] },
  }, async (req, reply) => {
    const user = null // await db.updateById(req.params.id, req.body)
    if (!user) throw reply.notFound(`User ${req.params.id} not found`)
    return user
  })

  app.delete<{ Params: UserParams }>('/:id', {
    schema: { params: UserParams, response: { 204: Type.Null() }, tags: ['Users'] },
  }, async (req, reply) => {
    // await db.deleteById(req.params.id)
    return reply.code(204).send()
  })
}
```

### Plugin architecture and encapsulation

```
Explain and implement the Fastify plugin encapsulation model.

Key rule: plugins registered with fastify-plugin() SHARE their decorators and
hooks with the parent scope. Plugins registered without it are ENCAPSULATED
(isolated — decorators not visible outside).

Use fastify-plugin when: you're adding decorators, setting hooks, or registering
shared infrastructure (db, jwt, redis) that sibling routes need.
Omit it when: you're registering route sub-groups that should be isolated.

// src/plugins/jwt.ts — shared auth plugin (uses fastify-plugin)
import fp from 'fastify-plugin'
import fjwt from '@fastify/jwt'
import { FastifyPluginAsync, FastifyRequest } from 'fastify'

const jwtPlugin: FastifyPluginAsync = async (app) => {
  app.register(fjwt, { secret: process.env.JWT_SECRET! })

  // Decorate request with an auth method routes can call
  app.decorate('authenticate', async (req: FastifyRequest) => {
    await req.jwtVerify()
  })
}

export default fp(jwtPlugin, { name: 'jwt' })

// src/types/index.ts — augment Fastify types so TypeScript knows about decorators
import { FastifyRequest } from 'fastify'
declare module 'fastify' {
  interface FastifyInstance {
    authenticate: (req: FastifyRequest) => Promise<void>
  }
}
declare module '@fastify/jwt' {
  interface FastifyJWT {
    payload: { sub: string; role: string; email: string }
    user: { sub: string; role: string; email: string }
  }
}

// Usage in a protected route scope (encapsulated — onRequest only fires here)
app.register(async (protectedScope) => {
  protectedScope.addHook('onRequest', app.authenticate)

  protectedScope.get('/me', async (req) => {
    return req.user  // typed: { sub, role, email }
  })
})
```

### Hooks lifecycle

```
Add Fastify hooks for [cross-cutting concern: logging / auth / rate limiting / transform].

Hook order:
  onRequest → preParsing → preValidation → preHandler → handler → preSerialization → onSend → onResponse
  onError fires on any uncaught error in the above chain.

// onRequest — runs before body parsing. Ideal for auth.
app.addHook('onRequest', async (req, reply) => {
  const token = req.headers.authorization?.slice(7)
  if (!token) throw reply.unauthorized('Bearer token required')
  req.user = app.jwt.verify(token)
})

// preHandler — body is parsed and validated. Ideal for business-logic guards.
app.addHook('preHandler', async (req, reply) => {
  if (req.user.role !== 'admin' && req.method !== 'GET') {
    throw reply.forbidden('Write access requires admin role')
  }
})

// onSend — transform or inspect the serialized response payload.
app.addHook('onSend', async (req, reply, payload) => {
  reply.header('X-Request-Id', req.id)
  return payload  // must return payload (or a modified version)
})

// onError — global error normalization.
app.addHook('onError', async (req, reply, error) => {
  req.log.error({ err: error, userId: req.user?.sub }, 'request error')
  // Don't mutate reply here — onError is for side effects only
})

// Scoped hook — applies only to routes in this plugin block
app.register(async (scope) => {
  scope.addHook('preHandler', rateLimitHook)
  scope.post('/login', loginHandler)
  scope.post('/register', registerHandler)
})
```

### Testing with fastify.inject()

```
Write tests for [route or feature] using fastify.inject() — no HTTP server needed.

// test/users.test.ts
import { test, beforeEach, afterEach } from 'node:test'
import assert from 'node:assert/strict'
import { buildApp } from '../src/app'

let app: ReturnType<typeof buildApp>

beforeEach(async () => {
  app = buildApp({ logger: false })  // silence logs in tests
  await app.ready()
})

afterEach(async () => {
  await app.close()
})

test('GET /api/v1/users — returns 200 with pagination', async () => {
  const res = await app.inject({
    method: 'GET',
    url: '/api/v1/users?page=1&limit=5',
    headers: { authorization: `Bearer ${validToken}` },
  })

  assert.equal(res.statusCode, 200)
  const body = res.json()
  assert.ok(Array.isArray(body.users))
  assert.equal(body.page, 1)
})

test('POST /api/v1/users — validates body, returns 400 on missing email', async () => {
  const res = await app.inject({
    method: 'POST',
    url: '/api/v1/users',
    payload: { name: 'Alice' },  // missing email and password
  })

  assert.equal(res.statusCode, 400)
  const body = res.json()
  assert.equal(body.error, 'Bad Request')
})

test('GET /api/v1/users/:id — returns 404 for unknown id', async () => {
  const res = await app.inject({
    method: 'GET',
    url: '/api/v1/users/00000000-0000-0000-0000-000000000000',
    headers: { authorization: `Bearer ${validToken}` },
  })

  assert.equal(res.statusCode, 404)
})

// Generate a signed JWT for testing
const validToken = app.jwt.sign({ sub: 'test-user', role: 'user', email: 'test@example.com' })
```

### Swagger documentation

```
Add Swagger UI to a Fastify app.

// src/plugins/swagger.ts
import fp from 'fastify-plugin'
import swagger from '@fastify/swagger'
import swaggerUi from '@fastify/swagger-ui'

export default fp(async (app) => {
  await app.register(swagger, {
    openapi: {
      info: { title: 'My API', version: '1.0.0' },
      components: {
        securitySchemes: {
          bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' },
        },
      },
      security: [{ bearerAuth: [] }],
    },
  })

  await app.register(swaggerUi, {
    routePrefix: '/docs',
    uiConfig: { deepLinking: true },
    staticCSP: true,
  })
})

// In routes, add tags and operationId for grouping in the UI
app.get('/users', {
  schema: {
    tags: ['Users'],
    operationId: 'listUsers',
    summary: 'List all users',
    description: 'Returns paginated users. Requires admin role.',
  },
}, handler)

// Access Swagger JSON: GET /docs/json
// Swagger UI:          GET /docs
```

## Example

**User:** I have an Express API doing ~8k req/s on a 4-core machine. I want to move to Fastify but keep the same route structure and Zod validation I already have.

**Migration plan:**

1. Replace the Express app shell:

```typescript
// Before (Express)
import express from 'express'
const app = express()
app.use(express.json())

// After (Fastify — built-in JSON parsing, ~2-3x faster serialization)
import Fastify from 'fastify'
const app = Fastify({ logger: true })
```

2. Replace Zod schemas with TypeBox (Fastify's native AJV integration is faster than Zod for request validation; TypeBox gives you TypeScript types for free):

```typescript
// Before (Zod)
const createUserSchema = z.object({ name: z.string().min(1), email: z.string().email() })

// After (TypeBox — validates at AJV speed, still typed)
const CreateUserBody = Type.Object({
  name: Type.String({ minLength: 1 }),
  email: Type.String({ format: 'email' }),
})
```

3. Convert routes — Fastify route schema replaces validation middleware:

```typescript
// Before (Express + validate middleware)
router.post('/', validate(createUserSchema), async (req, res) => {
  res.status(201).json(await createUser(req.body))
})

// After (Fastify — schema in route options, no middleware needed)
app.post<{ Body: CreateUserBody }>('/users', {
  schema: { body: CreateUserBody, response: { 201: UserSchema } },
}, async (req, reply) => {
  return reply.code(201).send(await createUser(req.body))
})
```

4. Replace middleware chains with hooks (scoped to protected routes only):

```typescript
app.register(async (protected) => {
  protected.addHook('onRequest', app.authenticate)
  protected.register(usersRoutes, { prefix: '/users' })
  protected.register(ordersRoutes, { prefix: '/orders' })
})
```

5. Test without spinning up a server:

```bash
npm run test  # fastify.inject() — zero port binding, full request lifecycle
```

Expected result: 16-20k req/s on the same 4-core machine, structured JSON logs via Pino, and full Swagger docs at `/docs`.
