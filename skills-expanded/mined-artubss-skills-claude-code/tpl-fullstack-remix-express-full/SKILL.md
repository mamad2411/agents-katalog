---
name: tpl-fullstack-remix-express-full
description: Template do pack (fullstack/04-remix-express-full.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/04-remix-express-full.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Remix v2 + Express Custom Server + Full Stack

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/04-remix-express-full.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Framework:** Remix v2 (Vite compiler)
- **Server:** Express 5 (custom Remix adapter)
- **Database:** PostgreSQL + Drizzle ORM
- **Sessions:** Redis-backed sessions (connect-redis)
- **File uploads:** AWS S3 (via @aws-sdk/client-s3)
- **Styling:** Tailwind CSS v3
- **Testing:** Vitest (unit/integration), Playwright (E2E)
- **Language:** TypeScript 5.x (strict)

---

## PROJECT STRUCTURE
```
app/
├── root.tsx                  # Remix root, global layout
├── routes/
│   ├── _index.tsx            # Home page
│   ├── _auth.login.tsx       # Login page (login form route)
│   ├── _auth.register.tsx
│   ├── dashboard._index.tsx  # Protected dashboard
│   └── api.upload.tsx        # File upload action
├── components/
│   ├── ui/                   # shadcn-like components
│   └── forms/
├── lib/
│   ├── session.server.ts     # Session helpers
│   ├── auth.server.ts        # getUser, requireUser
│   ├── s3.server.ts          # Upload logic
│   └── db.server.ts          # Drizzle client
└── utils/
    └── invariant.ts
server/
├── index.ts                  # Express entry, mounts Remix
└── middleware/
    ├── rateLimit.ts
    └── logger.ts
public/
vite.config.ts
drizzle.config.ts
```

---

## ARCHITECTURE RULES
1. **All loaders/actions are server-only** — `.server.ts` suffix for any module with secrets/DB; never imported by client bundle.
2. **Sessions stored in Redis** — not cookies (for large session data); cookie holds only session ID.
3. **Progressive enhancement** — forms work without JS; actions handle both JS (fetch) and no-JS (full page) submissions.
4. **Custom Express server owns middleware** — rate limiting, correlation IDs, security headers live in Express, not Remix.
5. **S3 uploads are server-side** — never give clients direct S3 presigned URLs for untrusted uploads; validate first.
6. **No `useEffect` for data fetching** — use Remix `loader`; `useEffect` for non-data side effects only.
7. **Error boundaries in every route** — `export function ErrorBoundary()` handles both expected and unexpected errors.

---

## CUSTOM EXPRESS SERVER + REMIX

```typescript
// server/index.ts
import express       from 'express'
import { createRequestHandler } from '@remix-run/express'
import { createClient }        from 'redis'
import session                 from 'express-session'
import { RedisStore }          from 'connect-redis'
import { rateLimit }           from 'express-rate-limit'
import compression             from 'compression'
import helmet                  from 'helmet'
import morgan                  from 'morgan'

async function bootstrap() {
  const redisClient = createClient({ url: process.env.REDIS_URL })
  await redisClient.connect()

  const app = express()

  app.use(helmet({ contentSecurityPolicy: false }))  // Remix sets its own CSP
  app.use(compression())
  app.use(morgan('combined'))
  app.use(express.json({ limit: '1mb' }))
  app.use(express.static('public', { maxAge: '1h' }))

  app.use(session({
    store:  new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: { secure: process.env.NODE_ENV === 'production', httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 },
  }))

  app.use(rateLimit({ windowMs: 60_000, max: 100 }))

  // Let Remix handle all other routes
  app.all('*', createRequestHandler({ build: await import('../build/server/index.js') }))

  app.listen(process.env.PORT ?? 3000, () => {
    console.log(`Server running on port ${process.env.PORT ?? 3000}`)
  })
}

bootstrap().catch(console.error)
```

---

## SESSION + AUTH HELPERS

```typescript
// app/lib/session.server.ts
import type { Session } from '@remix-run/node'
// Note: session is managed by Express/Redis; we access via request context
export interface SessionData { userId?: string; flash?: string }

// app/lib/auth.server.ts
import { redirect } from '@remix-run/node'
import { db }       from './db.server'
import { users }    from '~/db/schema'
import { eq }       from 'drizzle-orm'

export async function getUser(request: Request): Promise<typeof users.$inferSelect | null> {
  const userId = (request as Request & { session?: SessionData }).session?.userId
  if (!userId) return null
  return db.query.users.findFirst({ where: eq(users.id, userId) }) ?? null
}

export async function requireUser(request: Request) {
  const user = await getUser(request)
  if (!user) throw redirect('/login')
  return user
}

// app/routes/dashboard._index.tsx
import { json, type LoaderFunctionArgs } from '@remix-run/node'
import { useLoaderData } from '@remix-run/react'
import { requireUser } from '~/lib/auth.server'
import { db } from '~/lib/db.server'

export async function loader({ request }: LoaderFunctionArgs) {
  const user  = await requireUser(request)
  const posts = await db.query.posts.findMany({
    where: (p, { eq }) => eq(p.authorId, user.id),
    orderBy: (p, { desc }) => [desc(p.createdAt)],
    limit: 20,
  })
  return json({ user, posts })
}

export default function Dashboard() {
  const { user, posts } = useLoaderData<typeof loader>()
  return (
    <div>
      <h1>Hello, {user.name}</h1>
      <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
    </div>
  )
}

export function ErrorBoundary() {
  return <div className="p-4 text-red-500">Something went wrong loading your dashboard.</div>
}
```

---

## S3 FILE UPLOAD

```typescript
// app/lib/s3.server.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { randomUUID } from 'node:crypto'
import path           from 'node:path'

const s3 = new S3Client({ region: process.env.AWS_REGION! })

export async function uploadToS3(
  file: File,
  prefix = 'uploads/',
): Promise<{ url: string; key: string }> {
  const ext = path.extname(file.name).toLowerCase()
  const key = `${prefix}${randomUUID()}${ext}`

  await s3.send(new PutObjectCommand({
    Bucket:      process.env.S3_BUCKET!,
    Key:         key,
    Body:        Buffer.from(await file.arrayBuffer()),
    ContentType: file.type,
    ACL:         'public-read',
  }))

  return {
    key,
    url: `https://${process.env.S3_BUCKET}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`,
  }
}

// app/routes/api.upload.tsx
import { unstable_parseMultipartFormData, json, type ActionFunctionArgs } from '@remix-run/node'
import { requireUser } from '~/lib/auth.server'
import { uploadToS3 }  from '~/lib/s3.server'

export async function action({ request }: ActionFunctionArgs) {
  const user = await requireUser(request)
  const formData = await unstable_parseMultipartFormData(request, async ({ data, name, filename }) => {
    if (name !== 'file' || !filename) return undefined
    const chunks: Uint8Array[] = []
    for await (const chunk of data) chunks.push(chunk)
    return new File([Buffer.concat(chunks)], filename)
  })
  const file = formData.get('file') as File
  if (!file || file.size > 5 * 1024 * 1024) return json({ error: 'Invalid file' }, 400)
  const { url } = await uploadToS3(file, `users/${user.id}/`)
  return json({ url })
}
```

---

## ROUTING TABLE

| Method | Route | Auth | Action |
|--------|-------|------|--------|
| GET | / | No | Home with loader data |
| GET | /login | No | Login form |
| POST | /login | No | Authenticate, set session |
| GET | /register | No | Register form |
| POST | /register | No | Create user, set session |
| POST | /logout | Yes | Destroy session + redirect |
| GET | /dashboard | Yes | User dashboard |
| GET | /dashboard/posts | Yes | User posts list |
| POST | /dashboard/posts | Yes | Create post action |
| POST | /api/upload | Yes | Upload file to S3 |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] All `.server.ts` never imported in client components (checked by `remix vite:build`)
- [ ] Forms degrade gracefully without JavaScript
- [ ] `playwright test` — E2E login/create post/upload passes
- [ ] `vitest run` — all unit tests pass
- [ ] Session cookie is `httpOnly: true, secure: true` in production
- [ ] S3 file size validated server-side before `PutObjectCommand`
- [ ] Every route has `export function ErrorBoundary()`

---

## FORBIDDEN
- ❌ `fetch('/api/...')` from `useEffect` — use Remix `loader`/`useFetcher`
- ❌ `.server.ts` modules imported in `entry.client.tsx` or UI components
- ❌ `document.cookie` for session storage — Redis-backed sessions only
- ❌ Direct S3 presigned URL given to untrusted input — validate and proxy
- ❌ `unstable_*` APIs in production without understanding breakage risk
- ❌ Large queryStrings over 8kb — use form POST actions
- ❌ Missing error boundaries — unhandled loader errors crash the full page
