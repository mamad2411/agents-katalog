---
name: tpl-fullstack-react-express-monolith
description: Template do pack (fullstack/06-react-express-monolith.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/06-react-express-monolith.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: React 19 + Express 5 Monorepo (SPA + API)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/06-react-express-monolith.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Frontend:** React 19 + TypeScript + Vite 6
- **Backend:** Express 5 + TypeScript + Node.js 22
- **Database:** PostgreSQL + Drizzle ORM
- **Auth:** Passport.js + JWT (httpOnly cookie)
- **Monorepo:** pnpm workspaces (shared types package)
- **Testing:** Vitest (unit + API), Playwright (E2E)
- **Language:** TypeScript 5.x (strict) throughout

---

## PROJECT STRUCTURE
```
packages/
└── shared/                      # Shared types (no runtime deps)
    ├── src/
    │   └── types.ts
    └── package.json

apps/
├── client/                      # Vite SPA
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/                 # Typed fetch client
│   │   │   └── client.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── usePosts.ts
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   └── Dashboard.tsx
│   │   └── components/
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
└── server/                      # Express API
    ├── src/
    │   ├── index.ts
    │   ├── db/
    │   │   ├── index.ts
    │   │   └── schema.ts
    │   ├── routes/
    │   │   ├── auth.ts
    │   │   ├── users.ts
    │   │   └── posts.ts
    │   ├── middleware/
    │   │   ├── authenticate.ts
    │   │   └── validate.ts
    │   └── services/
    │       └── authService.ts
    ├── tests/
    └── package.json

pnpm-workspace.yaml
```

---

## ARCHITECTURE RULES
1. **Shared types package** — `@repo/shared` only types; `apps/client` and `apps/server` both depend on it; zero circular deps.
2. **Cookie-based JWT** — store access token in `httpOnly + secure + sameSite=strict` cookie; never `localStorage`.
3. **CORS locked to origin** — `app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }))` — never `'*'` with credentials.
4. **Vite proxy in dev** — `vite.config.ts` proxies `/api` to Express to avoid CORS issues in development.
5. **Express serves SPA in production** — `app.use(express.static('client/dist'))` + fallback `*` returns `index.html`.
6. **Typed API client** — frontend uses a generated typed `apiClient` (not raw fetch) that automatically attaches credentials.
7. **Drizzle schema = shared contract** — infer types from Drizzle schema for DB models; map to shared DTO types in service layer.

---

## SHARED TYPES

```typescript
// packages/shared/src/types.ts
export interface User {
  id:        string
  email:     string
  name:      string
  role:      'user' | 'admin'
  createdAt: string
}

export interface Post {
  id:        string
  title:     string
  body:      string
  published: boolean
  authorId:  string
  author:    Pick<User, 'id' | 'name'>
  createdAt: string
}

export interface ApiResponse<T>  { data: T }
export interface ApiError        { error: string; details?: Record<string, string[]> }
export type     ApiResult<T>     = ApiResponse<T> | ApiError
```

---

## VITE PROXY + PRODUCTION SERVE

```typescript
// apps/client/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path  from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '~': path.resolve(__dirname, 'src') } },
  server: {
    proxy: {
      '/api': {
        target:       'http://localhost:3001',
        changeOrigin: true,
        cookieDomainRewrite: 'localhost',
      },
    },
  },
})

// apps/server/src/index.ts (production SPA serving)
import express from 'express'
import path    from 'node:path'

const app = express()

// ... middleware, routes ...

if (process.env.NODE_ENV === 'production') {
  const clientDist = path.resolve(__dirname, '../../client/dist')
  app.use(express.static(clientDist))
  app.get('*', (_req, res) => res.sendFile(path.join(clientDist, 'index.html')))
}
```

---

## AUTH FLOW (Cookie JWT)

```typescript
// apps/server/src/routes/auth.ts
import express            from 'express'
import bcrypt             from 'bcryptjs'
import jwt                from 'jsonwebtoken'
import { z }              from 'zod'
import { db }             from '../db'
import { users }          from '../db/schema'
import { eq }             from 'drizzle-orm'
import type { User }      from '@repo/shared'

const router  = express.Router()
const COOKIE  = 'auth_token'

const loginSchema = z.object({ email: z.string().email(), password: z.string().min(8) })

router.post('/login', async (req, res) => {
  const parsed = loginSchema.safeParse(req.body)
  if (!parsed.success) return res.status(400).json({ error: 'Invalid input', details: parsed.error.flatten().fieldErrors })

  const user = await db.select().from(users).where(eq(users.email, parsed.data.email)).get()
  if (!user || !await bcrypt.compare(parsed.data.password, user.hashedPassword)) {
    return res.status(401).json({ error: 'Invalid credentials' })
  }

  const token = jwt.sign({ sub: user.id, role: user.role }, process.env.JWT_SECRET!, { expiresIn: '7d' })
  res.cookie(COOKIE, token, {
    httpOnly: true, secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict', maxAge: 7 * 24 * 60 * 60 * 1000,
  })
  const { hashedPassword: _, ...safeUser } = user
  return res.json({ data: safeUser })
})

router.post('/logout', (_req, res) => {
  res.clearCookie(COOKIE)
  res.json({ data: { ok: true } })
})

// apps/server/src/middleware/authenticate.ts
import jwt   from 'jsonwebtoken'
import type { Request, Response, NextFunction } from 'express'

export function authenticate(req: Request, res: Response, next: NextFunction): void {
  const token = req.cookies?.auth_token
  if (!token) { res.status(401).json({ error: 'Unauthorized' }); return }
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as { sub: string; role: string }
    req.userId = payload.sub
    req.userRole = payload.role
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}
declare global { namespace Express { interface Request { userId: string; userRole: string } } }
```

---

## TYPED API CLIENT (Frontend)

```typescript
// apps/client/src/api/client.ts
import type { ApiResult, User, Post } from '@repo/shared'

const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  const json = await res.json() as ApiResult<T>
  if ('error' in json) throw new Error(json.error)
  return json.data
}

export const apiClient = {
  auth: {
    login:   (email: string, password: string) => request<User>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
    logout:  () => request<{ ok: boolean }>('/auth/logout', { method: 'POST' }),
    me:      () => request<User>('/auth/me'),
  },
  posts: {
    list:    () => request<Post[]>('/posts'),
    create:  (data: Pick<Post, 'title' | 'body'>) => request<Post>('/posts', { method: 'POST', body: JSON.stringify(data) }),
    delete:  (id: string) => request<{ ok: boolean }>(`/posts/${id}`, { method: 'DELETE' }),
  },
}
```

---

## ROUTING TABLE

| Method | Path | Auth | Action |
|--------|------|------|--------|
| POST | /api/auth/login | No | Set cookie JWT |
| POST | /api/auth/logout | No | Clear cookie |
| GET | /api/auth/me | Yes | Current user |
| GET | /api/users | Yes (admin) | List users |
| GET | /api/posts | No | Public posts |
| POST | /api/posts | Yes | Create post |
| GET | /api/posts/:id | No | Single post |
| PUT | /api/posts/:id | Yes (owner) | Update post |
| DELETE | /api/posts/:id | Yes (owner) | Delete post |
| GET | * | No | Serve `index.html` (prod) |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors (both client and server)
- [ ] `vitest run` — all tests pass
- [ ] `playwright test` — login + CRUD E2E passes
- [ ] CORS `origin` is specific URL, not `'*'`
- [ ] Auth cookie is `httpOnly: true, secure: true` in production
- [ ] `npm run build` produces `client/dist/` and `server/dist/`
- [ ] All API responses typed via `ApiResponse<T>` wrapper
- [ ] `@repo/shared` has zero runtime dependencies

---

## FORBIDDEN
- ❌ `localStorage.setItem('token', ...)` — httpOnly cookies only
- ❌ `Access-Control-Allow-Origin: *` with `credentials: true`
- ❌ Direct `import` of server modules in client code
- ❌ `res.json(error)` without proper status code
- ❌ Password comparison with `===` — always `bcrypt.compare`
- ❌ Raw `fetch` in React components — use `apiClient`
- ❌ `any` type on `req.body` — always parse with Zod
- ❌ Serving SPA fallback before API routes in Express
