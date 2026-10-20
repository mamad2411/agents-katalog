---
name: "hono"
description: "Hono framework: build ultra-fast REST APIs and middleware for Cloudflare Workers, Bun, Deno, and Node.js — routing, validation with Zod, RPC client, and edge deployment patterns"
---

# Hono Skill

## When to activate
- Building a new API with Hono on Cloudflare Workers, Bun, or Node.js
- Migrating an Express API to Hono for edge deployment
- Setting up Zod validation with Hono's validator middleware
- Using Hono RPC for type-safe client/server communication
- Implementing middleware (auth, CORS, rate limiting) in Hono

## When NOT to use
- Next.js API routes — use the nextjs skill
- Full-featured backend with heavy ORM integration — Hono works but Express/Fastify have more ecosystem
- Large monolith with complex middleware chains — consider NestJS

## Instructions

### Project setup

```
Set up a Hono project for [target runtime].

Runtime: [Cloudflare Workers / Bun / Node.js / Deno / Vercel Edge]
Features: [routing / validation / auth / CORS / RPC]

Cloudflare Workers setup:
npm create cloudflare@latest my-api -- --template hono
cd my-api && npm install

Directory structure:
src/
  index.ts        ← entry point
  routes/
    users.ts      ← route handlers
    auth.ts
  middleware/
    auth.ts       ← custom middleware
  types.ts        ← shared types
wrangler.toml     ← Cloudflare config
package.json

Basic Hono app (src/index.ts):
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { usersRoute } from './routes/users'

const app = new Hono()

// Global middleware
app.use('*', logger())
app.use('/api/*', cors({
  origin: ['https://yourapp.com'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
}))

// Routes
app.route('/api/users', usersRoute)

// Health check
app.get('/health', (c) => c.json({ status: 'ok' }))

// 404 handler
app.notFound((c) => c.json({ error: 'Not found' }, 404))

// Error handler
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: 'Internal server error' }, 500)
})

export default app

Generate the setup for my target runtime.
```

### Routing and handlers

```
Build Hono routes for [resource].

Resource: [users / orders / products / etc.]
Methods: [GET list / GET by ID / POST / PUT / DELETE]
Auth: [required / optional / none]

Route file (src/routes/users.ts):
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const usersRoute = new Hono()

// Schemas
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).default('user'),
})

const updateUserSchema = createUserSchema.partial()

// List users
usersRoute.get('/', async (c) => {
  const { page = '1', limit = '20' } = c.req.query()
  // ... fetch from DB
  return c.json({ users: [], page: Number(page), total: 0 })
})

// Get single user
usersRoute.get('/:id', async (c) => {
  const id = c.req.param('id')
  // ... fetch from DB
  const user = null // replace with DB call
  if (!user) return c.json({ error: 'User not found' }, 404)
  return c.json(user)
})

// Create user
usersRoute.post(
  '/',
  zValidator('json', createUserSchema),
  async (c) => {
    const body = c.req.valid('json')  // typed and validated
    // ... save to DB
    return c.json({ id: 'new-id', ...body }, 201)
  }
)

// Update user
usersRoute.patch(
  '/:id',
  zValidator('json', updateUserSchema),
  async (c) => {
    const id = c.req.param('id')
    const body = c.req.valid('json')
    // ... update in DB
    return c.json({ id, ...body })
  }
)

// Delete user
usersRoute.delete('/:id', async (c) => {
  const id = c.req.param('id')
  // ... delete from DB
  return c.body(null, 204)
})

export { usersRoute }

Generate routes for my resource with validation.
```

### Middleware patterns

```
Implement [middleware type] for Hono.

Middleware type: [auth / rate limiting / request logging / caching / API key]

JWT authentication middleware:
import { createMiddleware } from 'hono/factory'
import { verify } from 'hono/jwt'

type Env = {
  Variables: {
    userId: string
    userRole: string
  }
}

export const authMiddleware = createMiddleware<Env>(async (c, next) => {
  const auth = c.req.header('Authorization')
  if (!auth?.startsWith('Bearer ')) {
    return c.json({ error: 'Unauthorized' }, 401)
  }
  
  const token = auth.split(' ')[1]
  try {
    const payload = await verify(token, c.env.JWT_SECRET)
    c.set('userId', payload.sub as string)
    c.set('userRole', payload.role as string)
    await next()
  } catch {
    return c.json({ error: 'Invalid token' }, 401)
  }
})

// Apply to specific routes:
usersRoute.use('*', authMiddleware)
// Or specific route:
usersRoute.post('/', authMiddleware, handler)

// Access in handler:
usersRoute.get('/me', authMiddleware, (c) => {
  const userId = c.get('userId')  // typed
  return c.json({ userId })
})

Rate limiting middleware (using KV on Cloudflare Workers):
export const rateLimiter = (limit: number, windowMs: number) =>
  createMiddleware(async (c, next) => {
    const ip = c.req.header('CF-Connecting-IP') ?? 'unknown'
    const key = `rate:${ip}`
    const count = Number(await c.env.KV.get(key) ?? 0)
    
    if (count >= limit) {
      return c.json({ error: 'Too many requests' }, 429)
    }
    
    await c.env.KV.put(key, String(count + 1), {
      expirationTtl: Math.ceil(windowMs / 1000),
    })
    
    await next()
  })

// Apply:
app.use('/api/auth/*', rateLimiter(5, 60_000))  // 5 req/min on auth

Generate the middleware for my use case.
```

### Hono RPC (type-safe client)

```
Set up Hono RPC for type-safe client-server communication.

Use case: [Next.js frontend calling Hono API / full-stack monorepo]

Server (define typed routes):
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

const routes = app
  .get('/api/posts', (c) => {
    return c.json({ posts: [] as Post[] })
  })
  .post(
    '/api/posts',
    zValidator('json', z.object({ title: z.string(), body: z.string() })),
    (c) => {
      const { title, body } = c.req.valid('json')
      return c.json({ id: '1', title, body }, 201)
    }
  )

export type AppType = typeof routes
export default app

Client (Next.js or any frontend):
import { hc } from 'hono/client'
import type { AppType } from '../api'  // import the server type

const client = hc<AppType>('http://localhost:3000')

// Fully typed — no manual types needed:
const res = await client.api.posts.$get()
const { posts } = await res.json()  // TypeScript knows the shape

const newPost = await client.api.posts.$post({
  json: { title: 'Hello', body: 'World' }  // TypeScript validates this
})
const post = await newPost.json()  // TypeScript knows the response shape

Generate the RPC setup for my project structure.
```

### Cloudflare Workers deployment

```
Deploy Hono to Cloudflare Workers.

Project: [name]
Bindings needed: [KV / D1 / R2 / AI / none]

wrangler.toml:
name = "my-api"
main = "src/index.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]

# KV namespace
[[kv_namespaces]]
binding = "KV"
id = "your-kv-namespace-id"

# D1 database
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-d1-id"

# R2 bucket
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# Environment variables (secrets via: wrangler secret put JWT_SECRET)
[vars]
ENVIRONMENT = "production"

Type-safe env bindings:
type Bindings = {
  JWT_SECRET: string
  KV: KVNamespace
  DB: D1Database
  BUCKET: R2Bucket
  ENVIRONMENT: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/users', async (c) => {
  const { results } = await c.env.DB.prepare(
    'SELECT * FROM users LIMIT 20'
  ).all()
  return c.json(results)
})

Deploy commands:
wrangler deploy          # deploy to production
wrangler dev             # local development with live reload
wrangler d1 execute DB --local --file ./schema.sql  # init local D1
wrangler secret put JWT_SECRET  # set a secret

Generate the wrangler config for my bindings.
```

## Example

**User:** Building a REST API for a SaaS product. Cloudflare Workers + D1 database + JWT auth. How do I set up Hono with the full stack?

**Claude's setup:**

```typescript
// src/index.ts
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { authMiddleware } from './middleware/auth'
import { usersRoute } from './routes/users'

type Bindings = {
  DB: D1Database
  JWT_SECRET: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.use('*', logger())
app.use('/api/*', cors({ origin: 'https://yourapp.com' }))

// Public routes
app.post('/api/auth/login', async (c) => {
  const { email, password } = await c.req.json()
  // verify credentials against c.env.DB
  // return JWT signed with c.env.JWT_SECRET
  return c.json({ token: 'jwt...' })
})

// Protected routes
app.route('/api/users', usersRoute)

export default app
```

```toml
# wrangler.toml
name = "my-saas-api"
main = "src/index.ts"
compatibility_date = "2024-11-01"

[[d1_databases]]
binding = "DB"
database_name = "saas-db"
database_id = "..."
```

**Performance:** Hono on Workers cold-starts in ~1ms vs 100-300ms for a container. At Cloudflare's edge (300+ locations), your API is always within ~20ms of any user globally. Perfect for a SaaS product with international users.

---
