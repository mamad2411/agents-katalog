---
name: tpl-frontend-nextjs-app-router
description: Template do pack (frontend/03-nextjs-app-router.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/03-nextjs-app-router.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/03-nextjs-app-router.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Next.js 15 App Router + TypeScript + Drizzle ORM
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Next.js (App Router) | 15.x |
| Linguagem | TypeScript | 5.x (strict) |
| Database | Neon Postgres + Drizzle ORM | latest |
| Auth | NextAuth.js (Auth.js) | v5 |
| Styling | Tailwind CSS + shadcn/ui | v4 |
| Server State | Server Components + TanStack Query | v5 |
| Forms | Server Actions + Zod | latest |
| Tests | Vitest (unit) + Playwright (e2e) | latest |

---

## APP ROUTER MENTAL MODEL

```
app/
├── (public)/            # Route group — sem auth
│   ├── layout.tsx
│   └── page.tsx
├── (dashboard)/         # Route group — requer auth
│   ├── layout.tsx       # Verifica sessão no Server Component
│   ├── loading.tsx      # Suspense fallback automático
│   ├── error.tsx        # Error boundary automático
│   └── {feature}/
│       ├── page.tsx     # Server Component (busca dados direto)
│       ├── actions.ts   # Server Actions (mutações)
│       └── _components/ # Prefixo _ = privado (não vira rota)
├── api/
│   └── {resource}/
│       └── route.ts     # Route Handler (webhooks, integrations)
└── globals.css
```

**Regra do `_` prefix:** Qualquer pasta/arquivo com `_` é PRIVADO — Next.js não cria rota. Use para colocar componentes específicos de uma rota.

---

## COMPONENT STRATEGY — Server vs Client

```
┌─────────────────────────────────────────────────┐
│ Server Component (DEFAULT — sem "use client")   │
│   ✅ async/await direto                          │
│   ✅ Acesso a DB, env vars, fs                   │
│   ✅ ZERO JavaScript no bundle do client         │
│   ❌ Sem hooks, sem eventos, sem browser APIs    │
├─────────────────────────────────────────────────┤
│ Client Component ("use client" no topo)         │
│   ✅ useState, useEffect, onClick, onSubmit     │
│   ✅ TanStack Query, Zustand, browser APIs      │
│   ❌ Sem acesso direto a DB ou server secrets   │
└─────────────────────────────────────────────────┘

REGRA: Empurre "use client" para as FOLHAS da árvore.
Server Component → renderiza → passa dados via props → Client Component filho
```

### Exemplo: Server Component buscando dados

```typescript
// app/(dashboard)/users/page.tsx — SERVER COMPONENT (default)
import { db } from '@/lib/db';
import { users } from '@/db/schema';
import { UserTable } from './_components/UserTable';

export default async function UsersPage() {
  const allUsers = await db.select().from(users).orderBy(users.createdAt);
  return (
    <div>
      <h1>Usuários</h1>
      <UserTable users={allUsers} />
    </div>
  );
}
```

### Exemplo: Client Component com interação

```typescript
// app/(dashboard)/users/_components/UserTable.tsx
'use client';
import { useState } from 'react';
import type { User } from '@/db/schema';

export function UserTable({ users }: { users: User[] }) {
  const [search, setSearch] = useState('');
  const filtered = users.filter((u) => u.name?.includes(search));
  return (
    <>
      <input value={search} onChange={(e) => setSearch(e.target.value)} />
      <table>{/* ... render filtered */}</table>
    </>
  );
}
```

---

## DATA FETCHING RULES

| Onde | Como | Quando |
|------|------|--------|
| Server Component | `async/await` direto com Drizzle | Dados iniciais da página |
| Client Component | TanStack Query (`useQuery`) | Dados que mudam em tempo real |
| Server Action | `"use server"` + Zod + DB | Formulários, mutações |
| Route Handler | `app/api/*/route.ts` | Webhooks externos, CORS APIs |

---

## SERVER ACTIONS PATTERN (Mutações)

```typescript
// app/(dashboard)/users/actions.ts
'use server';
import { z } from 'zod';
import { db } from '@/lib/db';
import { users } from '@/db/schema';
import { revalidatePath } from 'next/cache';
import { auth } from '@/lib/auth';

const createUserSchema = z.object({
  name: z.string().min(2, 'Nome precisa ter pelo menos 2 caracteres'),
  email: z.string().email('Email inválido'),
  role: z.enum(['admin', 'member']),
});

export async function createUser(formData: FormData) {
  // 1. Auth check
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  // 2. Validate input
  const parsed = createUserSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.flatten() };

  // 3. DB operation
  const [user] = await db.insert(users).values(parsed.data).returning();

  // 4. Revalidate cache
  revalidatePath('/dashboard/users');
  return { data: user };
}

export async function deleteUser(id: string) {
  const session = await auth();
  if (session?.user?.role !== 'admin') throw new Error('Forbidden');

  await db.delete(users).where(eq(users.id, id));
  revalidatePath('/dashboard/users');
}
```

---

## MIDDLEWARE PATTERN (Auth + Redirects)

```typescript
// middleware.ts (raiz do projeto)
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const { pathname } = req.nextUrl;

  // Rotas protegidas
  if (pathname.startsWith('/dashboard') && !req.auth) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Redirect logged user away from login
  if (pathname === '/login' && req.auth) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }
});

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
};
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New feature | Plan Server/Client split → route group folder → page.tsx + actions.ts |
| Hydration error | Find `"use client"` boundary — move event handlers to leaf component |
| Auth on page | middleware.ts matcher + session check in Server Component layout |
| SEO needed | Export `metadata` or `generateMetadata` from page.tsx |
| Mutation with feedback | Server Action → useActionState (React 19) or TanStack useMutation |
| Real-time needed | Route Handler + SSE or external WebSocket |
| Loading state needed | Add `loading.tsx` to route segment (auto-Suspense) |
| Error handling | Add `error.tsx` to route segment (auto-ErrorBoundary) |

---

## DRIZZLE SCHEMA RULES

```typescript
// db/schema/users.ts
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  email: text('email').unique().notNull(),
  name: text('name').notNull(),
  role: text('role', { enum: ['admin', 'member'] }).default('member').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

**Rules:**
- One file per table: `db/schema/{table}.ts`
- Always `createdAt` + `updatedAt`
- Foreign keys declared explicitly
- Index on all columns used in WHERE
- Type exports: `$inferSelect` and `$inferInsert`

---

## METADATA & SEO

```typescript
// app/(public)/blog/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [{ url: post.ogImage }],
    },
  };
}
```

---

## TESTING PATTERNS

```typescript
// __tests__/users/actions.test.ts
import { describe, it, expect, vi } from 'vitest';
import { createUser } from '@/app/(dashboard)/users/actions';

vi.mock('@/lib/auth', () => ({
  auth: vi.fn(() => ({ user: { id: '1', role: 'admin' } })),
}));

vi.mock('@/lib/db', () => ({
  db: { insert: vi.fn().mockReturnThis(), values: vi.fn().mockReturnThis(),
    returning: vi.fn(() => [{ id: '2', name: 'Test', email: 'test@test.com' }]),
  },
}));

describe('createUser', () => {
  it('validates input with Zod', async () => {
    const formData = new FormData();
    formData.set('name', '');
    formData.set('email', 'invalid');
    formData.set('role', 'member');

    const result = await createUser(formData);
    expect(result.error).toBeDefined();
  });
});
```

---

## NAMING CONVENTIONS

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Pages | `page.tsx` (App Router) | `app/(dashboard)/users/page.tsx` |
| Layouts | `layout.tsx` | `app/(dashboard)/layout.tsx` |
| Actions | `actions.ts` | `app/(dashboard)/users/actions.ts` |
| Route Handlers | `route.ts` | `app/api/webhooks/route.ts` |
| Components | PascalCase | `UserCard.tsx` in `_components/` |
| Private folders | `_prefix` | `_components/`, `_hooks/` |
| DB Schema | snake_case | `db/schema/user_profiles.ts` |
| Types | PascalCase | `User`, `ApiResponse<T>` |

---

## ENV VARS

```env
DATABASE_URL=postgresql://...neon.tech/...
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## BUILD COMMANDS

```bash
npm run dev          # Dev server (turbopack)
npm run build        # Production build (tsc + next build)
npm run start        # Start production server
npm test             # Vitest
npm run test:e2e     # Playwright
npm run db:generate  # Drizzle Kit generate migration
npm run db:migrate   # Apply migrations
npm run db:studio    # Drizzle Studio (visual DB browser)
```

---

## QUALITY GATES

Before any PR:
□ `next build` — 0 errors, 0 warnings
□ `npx tsc --noEmit` — 0 errors
□ Lighthouse: Performance > 90, Accessibility > 90
□ All pages have `metadata` or `generateMetadata`
□ No sensitive data in client bundle (`next/bundle-analyzer`)
□ All Server Actions validate with Zod before DB
□ `loading.tsx` exists for all async routes
□ `error.tsx` exists for all critical routes

---

## FORBIDDEN

- NEVER use `pages/api/` (use `app/api/route.ts`)
- NEVER fetch data in Client Component on mount (Server Component or TanStack Query)
- NEVER use `<img>` — always `next/image`
- NEVER import server-only code in Client Components (use `server-only` package)
- NEVER skip `loading.tsx` for routes with async data
- NEVER put DB credentials in `NEXT_PUBLIC_*` env vars
- NEVER use `useEffect` for initial data fetch (Server Component handles it)
- NEVER call Server Actions conditionally in render (call in event handlers)
