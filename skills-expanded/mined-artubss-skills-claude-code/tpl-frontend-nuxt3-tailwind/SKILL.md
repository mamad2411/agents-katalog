---
name: tpl-frontend-nuxt3-tailwind
description: Template do pack (frontend/11-nuxt3-tailwind.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/11-nuxt3-tailwind.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/11-nuxt3-tailwind.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Nuxt 3 + TypeScript
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Nuxt | 3.x |
| Linguagem | TypeScript | 5.x (strict) |
| State Management | Pinia | 2.x |
| Estilização | Tailwind CSS | v4 |
| Validação | Zod | 3.x |
| Testes unitários | Vitest + @nuxt/test-utils | latest |
| Testes e2e | Playwright | latest |
| ORM (opcional) | Drizzle ORM | latest |
| Deploy | Vercel / Cloudflare Workers / Nitro | — |

---

## PROJECT STRUCTURE

```
├── app.vue                        # Raiz da app — apenas <NuxtLayout> + <NuxtPage>
├── nuxt.config.ts                 # Configuração central
├── server/                        # Nitro server — executado APENAS no servidor
│   ├── api/
│   │   ├── auth/
│   │   │   ├── login.post.ts      # POST /api/auth/login
│   │   │   └── logout.post.ts     # POST /api/auth/logout
│   │   ├── users/
│   │   │   ├── index.get.ts       # GET /api/users
│   │   │   ├── index.post.ts      # POST /api/users
│   │   │   ├── [id].get.ts        # GET /api/users/:id
│   │   │   ├── [id].put.ts        # PUT /api/users/:id
│   │   │   └── [id].delete.ts     # DELETE /api/users/:id
│   ├── middleware/
│   │   └── auth.ts                # Middleware de autenticação nas rotas /api/*
│   ├── plugins/
│   │   └── db.ts                  # Instância DB (Drizzle/Prisma) attached to context
│   └── utils/
│       ├── auth.ts                # Helpers de JWT/session para o servidor
│       └── validate.ts            # Helper para validar com Zod no servidor
├── pages/                         # File-based routing (Vue Router)
│   ├── index.vue
│   ├── login.vue
│   ├── dashboard/
│   │   ├── index.vue
│   │   ├── projects/
│   │   │   ├── index.vue
│   │   │   └── [id].vue
│   │   └── settings.vue
│   └── [...slug].vue              # 404 catch-all
├── layouts/
│   ├── default.vue
│   ├── auth.vue
│   └── dashboard.vue
├── components/
│   ├── ui/                        # Primitivos (Button, Input, Card) — auto-importados
│   └── features/                  # Componentes de domínio — auto-importados
├── composables/                   # useXxx() — auto-importados
│   ├── useAuth.ts
│   ├── useProjects.ts
│   └── usePagination.ts
├── stores/                        # Pinia stores — NÃO auto-importados
│   ├── auth.store.ts
│   └── projects.store.ts
├── utils/                         # Funções puras, SEM side effects
│   ├── formatDate.ts
│   └── currency.ts
├── types/
│   └── index.ts
├── middleware/                    # Route middleware (client + server)
│   ├── auth.global.ts             # .global = executado em toda rota
│   └── role.ts
└── plugins/
    └── pinia.ts
```

---

## AUTO-IMPORTS — REGRAS

Nuxt auto-importa os seguintes:
- `components/` → todos os componentes (incluindo subpastas com prefixo do path)
- `composables/` → `useXxx()` functions
- `utils/` → funções utilitárias
- APIs Vue: `ref`, `computed`, `watch`, etc.
- APIs Nuxt: `useRoute`, `useFetch`, `useRuntimeConfig`, etc.

**O que NÃO é auto-importado:**
- `stores/` — importar explicitamente nos composables/pages
- `server/` — ambiente Nitro separado
- `types/` — apenas types, não tem runtime

```typescript
// ✅ CORRETO — composable auto-importado
// composables/useProjects.ts
export function useProjects() {
  const { data, pending, error, refresh } = useFetch('/api/projects');
  return { projects: data, loading: pending, error, refresh };
}

// Em qualquer .vue — sem import necessário
const { projects, loading } = useProjects();
```

---

## COMPOSABLES VS UTILS — DECISION TABLE

| Situação | Usar | Local | Motivo |
|---------|------|-------|--------|
| Lógica com estado reativo (`ref`, `computed`) | Composable `useXxx()` | `composables/` | Precisa de contexto Vue |
| Função pura sem reatividade | Utility function | `utils/` | Simples, testável, sem overhead |
| Fetch de dados do servidor | Composable + `useFetch`/`useAsyncData` | `composables/` | SSR-aware, deduplicação |
| State global compartilhado | Pinia store | `stores/` | Reatividade + devtools |
| Formatter de data/moeda | Utility | `utils/` | Puro, sem Vue |
| Lógica de formulário | Composable `useForm()` | `composables/` | Precisa de `ref` para erros |

```typescript
// ✅ Utils — sem reatividade
// utils/formatDate.ts
export function formatDate(date: Date, locale = 'pt-BR'): string {
  return new Intl.DateTimeFormat(locale, { dateStyle: 'medium' }).format(date);
}

// ✅ Composable — com reatividade Vue
// composables/usePagination.ts
export function usePagination(totalItems: Ref<number>, perPage = 10) {
  const currentPage = ref(1);
  const totalPages = computed(() => Math.ceil(totalItems.value / perPage));
  const offset = computed(() => (currentPage.value - 1) * perPage);

  function goTo(page: number) {
    currentPage.value = Math.max(1, Math.min(page, totalPages.value));
  }

  return { currentPage, totalPages, offset, goTo };
}
```

---

## SERVER ROUTES (~/server/api)

```typescript
// server/api/users/index.get.ts
import { z } from 'zod';

export default defineEventHandler(async (event) => {
  // Autenticação via middleware (server/middleware/auth.ts)
  const user = event.context.user; // injetado pelo middleware
  if (!user) throw createError({ statusCode: 401, message: 'Não autenticado' });

  const query = getQuery(event);
  const page = Number(query.page) || 1;
  const limit = Number(query.limit) || 20;

  const users = await event.context.db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
    select: { id: true, name: true, email: true, createdAt: true },
  });

  return { users, page, limit };
});

// server/api/users/index.post.ts
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  password: z.string().min(8),
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const result = CreateUserSchema.safeParse(body);

  if (!result.success) {
    throw createError({
      statusCode: 422,
      data: result.error.flatten().fieldErrors,
      message: 'Dados inválidos',
    });
  }

  const user = await event.context.db.user.create({ data: result.data });
  return { user, statusCode: 201 };
});
```

**Regras de Server Routes:**
1. Nomenclatura: `[rota].[método].ts` define automaticamente o HTTP method.
2. Sempre usar `createError({ statusCode, message })` para erros.
3. Sempre validar `body` com Zod antes de usar.
4. Nunca retornar campos sensíveis (senha, tokens internos).
5. Autenticação em `server/middleware/auth.ts` — não repetir em cada handler.

---

## PINIA STORES

```typescript
// stores/auth.store.ts
import { defineStore } from 'pinia';
import type { User } from '~/types';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const loading = ref(false);

  // Getters
  const isAuthenticated = computed(() => user.value !== null);
  const isAdmin = computed(() => user.value?.role === 'admin');

  // Actions
  async function login(email: string, password: string) {
    loading.value = true;
    try {
      const { token, user: loggedUser } = await $fetch('/api/auth/login', {
        method: 'POST',
        body: { email, password },
      });
      user.value = loggedUser;
      useCookie('auth_token').value = token;
      await navigateTo('/dashboard');
    } catch (err) {
      throw err; // re-throw para o componente tratar
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' });
    user.value = null;
    useCookie('auth_token').value = null;
    await navigateTo('/login');
  }

  return { user, loading, isAuthenticated, isAdmin, login, logout };
});
```

**Regras Pinia:**
1. Usar Composition API Store (`defineStore('id', () => {...})`) — não Options Store.
2. Estado inicial sempre com tipos explícitos.
3. Actions assíncronas tratam erros e resetam `loading` no `finally`.
4. Stores NÃO fazem navegação inline — usar `navigateTo()` com cuidado, apenas pós-ação.
5. Nunca persistir dados sensíveis no store (usar cookies HttpOnly no servidor).

---

## NUXT.CONFIG.TS

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },

  typescript: {
    strict: true,
    typeCheck: true,
  },

  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
    '@vueuse/nuxt',
    '@nuxt/test-utils/module',
  ],

  runtimeConfig: {
    // Servidor apenas — nunca exposto ao cliente
    jwtSecret: process.env.JWT_SECRET,
    databaseUrl: process.env.DATABASE_URL,
    // Cliente — prefixo "public"
    public: {
      apiBase: process.env.API_BASE || '/api',
      appName: 'Minha App',
    },
  },

  routeRules: {
    '/dashboard/**': { ssr: false }, // SPA zone — dashboard não precisa de SSR
    '/api/**': { cors: false },
    '/': { prerender: true }, // Landing page pré-renderizada
  },

  nitro: {
    experimental: {
      openAPI: true, // Gera schema OpenAPI das server routes
    },
  },

  app: {
    head: {
      title: 'Minha App',
      htmlAttrs: { lang: 'pt-BR' },
    },
  },
});
```

---

## $FETCH VS USEFETCH VS USEASYNCDATA

| Situação | Usar | Motivo |
|---------|------|--------|
| Fetch em `<script setup>` de page | `useFetch('/api/rota')` | SSR + deduplication automáticos |
| Fetch com query params dinâmicos | `useAsyncData('key', () => $fetch(...))` | Controle total da key |
| Fetch em response a evento (botão) | `$fetch('/api/rota', { method: 'POST' })` | One-shot, não SSR |
| Fetch em server route (servidor→servidor) | `$fetch` ou `ofetch` | Não é hydrated |

```typescript
// Page — SSR aware
const { data: projects, pending, refresh } = await useFetch('/api/projects', {
  query: { page: currentPage },
  watch: [currentPage],
});

// Mutation em resposta a evento
async function deleteProject(id: string) {
  await $fetch(`/api/projects/${id}`, { method: 'DELETE' });
  refresh();
}
```

---

## ROUTING TABLE

| Trigger | Rota | Page/Componente | Middleware | Descrição |
|---------|------|----------------|-----------|-----------|
| Acessa `/` | `/` | `pages/index.vue` | — | Landing (prerendered) |
| Acessa `/login` | `/login` | `pages/login.vue` | `guest` | Redireciona se autenticado |
| Submete login | POST `/api/auth/login` | server route | — | Retorna token + user |
| Acessa `/dashboard` | `/dashboard` | `pages/dashboard/index.vue` | `auth.global` | Requer auth |
| Acessa `/dashboard/projects` | `/dashboard/projects` | `pages/dashboard/projects/index.vue` | `auth.global` | Lista projetos |
| Acessa `/dashboard/projects/:id` | `/dashboard/projects/[id]` | `pages/dashboard/projects/[id].vue` | `auth.global` | Detalhe projeto |
| Cria projeto | POST `/api/projects` | server route | — | Validado com Zod |
| Deleta projeto | DELETE `/api/projects/:id` | server route | — | Verificar ownership |
| 404 | `/*` | `pages/[...slug].vue` | — | Not found |

---

## MIDDLEWARE DE ROTA

```typescript
// middleware/auth.global.ts — executa em TODAS as rotas
export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore();
  const publicRoutes = ['/', '/login', '/register'];

  if (!authStore.isAuthenticated && !publicRoutes.includes(to.path)) {
    return navigateTo('/login');
  }
});
```

---

## TESTES

```typescript
// tests/unit/composables/usePagination.test.ts
import { describe, it, expect } from 'vitest';
import { ref } from 'vue';
import { usePagination } from '~/composables/usePagination';

describe('usePagination', () => {
  it('calcula totalPages corretamente', () => {
    const total = ref(100);
    const { totalPages } = usePagination(total, 10);
    expect(totalPages.value).toBe(10);
  });
});

// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('login com credenciais válidas', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'user@test.com');
  await page.fill('[name=password]', 'password123');
  await page.click('[type=submit]');
  await expect(page).toHaveURL('/dashboard');
});
```

---

## QUALITY GATES

- [ ] `npx nuxi typecheck` — sem erros TypeScript
- [ ] `npx eslint . --max-warnings 0` — sem warnings
- [ ] `npx vitest run` — testes unitários passando
- [ ] `npx playwright test` — testes e2e passando
- [ ] `nuxi build` — build de produção sem erros
- [ ] Toda server route valida input com Zod
- [ ] Nenhuma variável sensível em `runtimeConfig.public`
- [ ] Composables com `useFetch`/`useAsyncData` têm key única
- [ ] Middleware de autenticação aplicado em rotas protegidas
- [ ] Stores não persistem dados sensíveis no cliente
- [ ] Nenhum `console.log` em código de produção
- [ ] `routeRules` configurado para otimização de SSR/SPA/prerender

---

## FORBIDDEN

```
❌ NUNCA importar código de `server/` em `pages/`, `components/`, `composables/`
❌ NUNCA colocar secrets em `runtimeConfig.public` — apenas em `runtimeConfig`
❌ NUNCA usar `localStorage` diretamente — encapsular em composable com check `process.client`
❌ NUNCA fazer fetch no `mounted()` de componentes — usar `useFetch` no `<script setup>`
❌ NUNCA acessar `document` ou `window` fora de `onMounted` ou `process.client` check
❌ NUNCA criar componente sem nomear o arquivo adequadamente (auto-import usa o filename)
❌ NUNCA usar `any` em TypeScript
❌ NUNCA misturar Options API e Composition API no mesmo componente
❌ NUNCA usar `defineComponent` sem `setup()` — projeto é 100% `<script setup>`
❌ NUNCA modificar `node_modules` ou gerar código em `node_modules`
❌ NUNCA commit com variáveis de ambiente hardcoded
```

---

## ENV VARIABLES

```bash
# .env.example
DATABASE_URL="postgresql://user:password@localhost:5432/myapp"
JWT_SECRET="super-secret-min-32-chars"
NUXT_PUBLIC_API_BASE="/api"
NUXT_PUBLIC_APP_NAME="Minha App"
```

---

## COMMANDS

```bash
# Dev
npx nuxi dev

# Typecheck
npx nuxi typecheck

# Build
npx nuxi build
npx nuxi preview

# Generate (static)
npx nuxi generate

# Testes
npx vitest run
npx vitest --ui
npx playwright test
npx playwright test --ui

# Lint
npx eslint . --fix

# Novos componentes / pages
npx nuxi add component ui/MyButton
npx nuxi add page dashboard/settings
npx nuxi add composable useMyFeature
```
