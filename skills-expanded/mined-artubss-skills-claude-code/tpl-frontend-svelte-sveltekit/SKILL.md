---
name: tpl-frontend-svelte-sveltekit
description: Template do pack (frontend/06-svelte-sveltekit.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/06-svelte-sveltekit.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/06-svelte-sveltekit.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — SvelteKit + TypeScript + Drizzle ORM
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | SvelteKit | 2.x |
| Linguagem | TypeScript | 5.x (strict) |
| Database | PlanetScale / Turso + Drizzle ORM | latest |
| Styling | Tailwind CSS | v4 |
| Forms | Superforms + Zod | latest |
| State | Svelte stores (built-in) | - |
| Tests | Vitest + Playwright | latest |

---

## SVELTEKIT MENTAL MODEL

```
src/
├── lib/
│   ├── server/          # NUNCA exposto ao cliente (import $lib/server/*)
│   │   ├── db/          # Drizzle config + queries
│   │   │   ├── index.ts # DB connection
│   │   │   └── schema.ts
│   │   └── auth.ts      # Session validation
│   ├── components/      # Componentes .svelte reutilizáveis
│   │   ├── ui/          # Primitivos: Button, Input, Card
│   │   └── layout/      # Header, Sidebar, Footer
│   ├── stores/          # Svelte writable/derived stores
│   └── utils.ts         # Helpers puros
├── routes/
│   ├── +layout.svelte   # Root layout (nav, providers)
│   ├── +layout.server.ts # Root load (session, user)
│   ├── (public)/        # Route group sem auth
│   │   └── +page.svelte
│   ├── (app)/           # Route group com auth
│   │   ├── +layout.server.ts  # Auth guard
│   │   └── dashboard/
│   │       ├── +page.svelte
│   │       ├── +page.server.ts
│   │       └── +error.svelte
│   └── api/             # API routes (+server.ts)
└── hooks.server.ts      # Middleware global (auth, logging)
```

**Key insight:** `$lib/server/` imports are BLOCKED from client code by SvelteKit. Anything in `lib/server/` is guaranteed server-only — no accidental leaks.

---

## DATA FETCHING RULES

| Arquivo | Tipo | Uso |
|---------|------|-----|
| `+page.server.ts` | Server-only load | DB queries, auth checks, secrets |
| `+page.ts` | Universal load | API calls, public data |
| `+server.ts` | API route | Webhooks, external integrations |
| Form Actions | Server-only mutation | CRUD operations via forms |

**Rule:** Prefer `+page.server.ts` over `+page.ts` unless you need the load to run on client navigation too.

---

## LOAD FUNCTION PATTERN

```typescript
// routes/(app)/users/+page.server.ts
import { db } from '$lib/server/db';
import { users } from '$lib/server/db/schema';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.user) throw error(401, 'Unauthorized');

  const allUsers = await db.select().from(users).orderBy(users.createdAt);

  return {
    users: allUsers,
    meta: { title: 'Usuários', count: allUsers.length },
  };
};

// In +page.svelte:
// <script lang="ts">
//   export let data;  // Typed automatically from load return
//   // data.users, data.meta — fully typed!
// </script>
```

---

## FORM ACTIONS + SUPERFORMS PATTERN

```typescript
// routes/(app)/users/new/schema.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(2, 'Nome mínimo 2 caracteres'),
  email: z.string().email('Email inválido'),
  role: z.enum(['admin', 'member']),
});

// routes/(app)/users/new/+page.server.ts
import { superValidate, fail } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { createUserSchema } from './schema';

export const load = async () => {
  const form = await superValidate(zod(createUserSchema));
  return { form };
};

export const actions = {
  default: async ({ request }) => {
    const form = await superValidate(request, zod(createUserSchema));
    if (!form.valid) return fail(400, { form });

    await db.insert(users).values(form.data);
    return { form };
  },
};
```

```svelte
<!-- routes/(app)/users/new/+page.svelte -->
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  export let data;

  const { form, errors, enhance, delayed } = superForm(data.form);
</script>

<form method="POST" use:enhance>
  <input name="name" bind:value={$form.name} />
  {#if $errors.name}<span class="text-red-500">{$errors.name}</span>{/if}

  <input name="email" bind:value={$form.email} />
  {#if $errors.email}<span class="text-red-500">{$errors.email}</span>{/if}

  <button disabled={$delayed}>
    {$delayed ? 'Salvando...' : 'Criar Usuário'}
  </button>
</form>
```

---

## HOOKS (Global Middleware)

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { validateSession } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  // Auth: attach user to locals
  const sessionId = event.cookies.get('session');
  if (sessionId) {
    event.locals.user = await validateSession(sessionId);
  }

  return resolve(event);
};
```

---

## SVELTE STORES PATTERN

```typescript
// lib/stores/theme.ts
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

function createThemeStore() {
  const { subscribe, set, update } = writable<'light' | 'dark'>(
    browser ? (localStorage.getItem('theme') as 'light' | 'dark') ?? 'light' : 'light'
  );

  return {
    subscribe,
    toggle: () => update((t) => {
      const next = t === 'light' ? 'dark' : 'light';
      if (browser) localStorage.setItem('theme', next);
      return next;
    }),
    set,
  };
}

export const theme = createThemeStore();

// Derived store example
export const isDark = derived(theme, ($t) => $t === 'dark');
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New page | `routes/{path}/+page.svelte` + `+page.server.ts` |
| New form | Zod schema → Superforms → Form Action in `+page.server.ts` |
| Auth check | `locals.user` in load function → `error(401)` if missing |
| Auth guard group | Create `(app)/+layout.server.ts` that checks `locals.user` |
| Real-time data | Svelte writable store + SSE via `+server.ts` |
| API endpoint | `routes/api/{path}/+server.ts` → export `GET`, `POST`, etc. |
| Global middleware | `hooks.server.ts` → `handle` function |
| Shared state | Create store in `lib/stores/{name}.ts` |

---

## TESTING PATTERNS

```typescript
// tests/users.test.ts
import { describe, it, expect } from 'vitest';
import { createUserSchema } from '$lib/schemas/user';

describe('createUserSchema', () => {
  it('rejects empty name', () => {
    const result = createUserSchema.safeParse({ name: '', email: 'a@b.com', role: 'member' });
    expect(result.success).toBe(false);
  });

  it('accepts valid data', () => {
    const result = createUserSchema.safeParse({
      name: 'Test User',
      email: 'test@example.com',
      role: 'admin',
    });
    expect(result.success).toBe(true);
  });
});
```

---

## NAMING CONVENTIONS

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Pages | `+page.svelte` | `routes/dashboard/+page.svelte` |
| Server Load | `+page.server.ts` | `routes/dashboard/+page.server.ts` |
| Layouts | `+layout.svelte` | `routes/(app)/+layout.svelte` |
| API Routes | `+server.ts` | `routes/api/users/+server.ts` |
| Components | PascalCase `.svelte` | `lib/components/UserCard.svelte` |
| Stores | camelCase `.ts` | `lib/stores/theme.ts` |
| Server-only | `$lib/server/*` | `$lib/server/db/index.ts` |

---

## ENV VARS

```env
DATABASE_URL=libsql://...turso.io
DATABASE_AUTH_TOKEN=...
SESSION_SECRET=...
PUBLIC_APP_URL=http://localhost:5173
```

## BUILD COMMANDS

```bash
npm run dev          # Dev server with HMR
npm run build        # Production build
npm run preview      # Preview production locally
npx svelte-check     # TypeScript + Svelte diagnostics
npm test             # Vitest
npm run test:e2e     # Playwright
```

---

## QUALITY GATES

□ `npx svelte-check` — 0 errors
□ `npm test` — all pass
□ All form actions validate with Zod via Superforms
□ No sensitive data in `+page.ts` (use `+page.server.ts`)
□ CSP headers configured in `svelte.config.js`
□ `hooks.server.ts` handles auth globally
□ All DB imports from `$lib/server/` (never `$lib/`)

---

## FORBIDDEN

- NEVER import from `$lib/server/` in client code (SvelteKit blocks it but don't try)
- NEVER use `+page.ts` for sensitive data (use `+page.server.ts`)
- NEVER skip Zod validation in form actions
- NEVER access `document`/`window` without `browser` check from `$app/environment`
- NEVER use inline `<style>` when Tailwind classes exist
- NEVER put DB connection strings in `PUBLIC_` env vars
