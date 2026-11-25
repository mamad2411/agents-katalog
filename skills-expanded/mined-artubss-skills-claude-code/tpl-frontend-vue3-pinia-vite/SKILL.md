---
name: tpl-frontend-vue3-pinia-vite
description: Template do pack (frontend/05-vue3-pinia-vite.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/05-vue3-pinia-vite.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App Vue]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/05-vue3-pinia-vite.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Vue 3 + TypeScript + Pinia + TanStack Query
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Vue | 3.x |
| Linguagem | TypeScript | 5.x (strict) |
| Bundler | Vite | 6.x |
| State | Pinia (client) + TanStack Query (server) | latest |
| Routing | Vue Router | 4.x |
| Styling | Tailwind CSS | v4 |
| Forms | VeeValidate + Zod | latest |
| HTTP | Axios + vue-query | latest |
| Tests | Vitest + Vue Testing Library | latest |

---

## PROJECT STRUCTURE

```
src/
├── components/
│   ├── ui/             # Design system primitives
│   └── layout/         # Header, Sidebar, Footer
├── composables/        # Equivalente a React hooks — use*.ts
│   ├── useAuth.ts
│   └── useUsers.ts     # TanStack Query hooks
├── features/           # Feature modules (colocated)
│   └── {feature}/
│       ├── components/ # Feature-specific .vue components
│       ├── composables/
│       ├── types.ts
│       └── index.ts
├── pages/              # Page components
├── router/
│   └── index.ts        # Route definitions + guards
├── stores/             # Pinia stores
│   └── {name}.store.ts
├── lib/
│   ├── axios.ts        # Configured instance
│   └── utils.ts
└── types/              # Global types
```

---

## COMPOSITION API — MENTAL MODEL

```vue
<!-- ✅ CORRETO — <script setup> + TypeScript -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUsers } from '@/composables/useUsers';

// Props with TypeScript
interface Props {
  initialFilter?: string;
}
const props = withDefaults(defineProps<Props>(), {
  initialFilter: '',
});

// Emits with TypeScript
const emit = defineEmits<{
  select: [userId: string];
  close: [];
}>();

// Reactive state
const search = ref(props.initialFilter);
const { data: users, isLoading } = useUsers(search);
const filteredCount = computed(() => users.value?.length ?? 0);

function handleSelect(id: string) {
  emit('select', id);
}
</script>

<template>
  <input v-model="search" placeholder="Buscar..." />
  <p v-if="isLoading">Carregando...</p>
  <ul v-else>
    <li v-for="user in users" :key="user.id" @click="handleSelect(user.id)">
      {{ user.name }}
    </li>
  </ul>
  <span>{{ filteredCount }} resultados</span>
</template>
```

**Rules:**
- ALWAYS use `<script setup lang="ts">` — NEVER Options API
- Props: `defineProps<Props>()` with TypeScript interface
- Emits: `defineEmits<Emits>()` with TypeScript
- Extract reusable logic into `composables/use*.ts`

---

## PINIA STORE PATTERN

```typescript
// stores/auth.store.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);

  // Getters (computed)
  const isAuthenticated = computed(() => user.value !== null);
  const isAdmin = computed(() => user.value?.role === 'admin');

  // Actions
  async function login(credentials: { email: string; password: string }) {
    const res = await authApi.login(credentials);
    user.value = res.user;
    token.value = res.token;
  }

  function logout() {
    user.value = null;
    token.value = null;
  }

  return { user, token, isAuthenticated, isAdmin, login, logout };
}, {
  persist: true, // pinia-plugin-persistedstate
});
```

**Rules:**
- Use Composition API syntax (`setup()` function)
- One store per file: `stores/{name}.store.ts`
- `persist: true` only for auth/preferences (not server data)
- NEVER store TanStack Query data in Pinia

---

## COMPOSABLE PATTERN (TanStack Query)

```typescript
// composables/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { computed, type Ref } from 'vue';
import { api } from '@/lib/axios';

const userKeys = {
  all: ['users'] as const,
  list: (search: string) => [...userKeys.all, 'list', search] as const,
  detail: (id: string) => [...userKeys.all, 'detail', id] as const,
};

export function useUsers(search: Ref<string>) {
  return useQuery({
    queryKey: computed(() => userKeys.list(search.value)),
    queryFn: () => api.get('/users', { params: { q: search.value } }).then((r) => r.data),
    staleTime: 5 * 60 * 1000,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: NewUser) => api.post('/users', data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: userKeys.all }),
  });
}
```

**Key difference from React:** Query keys can be `computed()` refs — they re-fetch automatically when the ref changes.

---

## FORM PATTERN (VeeValidate + Zod)

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { z } from 'zod';
import { useCreateUser } from '@/composables/useUsers';

const schema = toTypedSchema(z.object({
  name: z.string().min(2, 'Mínimo 2 caracteres'),
  email: z.string().email('Email inválido'),
}));

const { handleSubmit, defineField, errors } = useForm({ validationSchema: schema });
const [name, nameAttrs] = defineField('name');
const [email, emailAttrs] = defineField('email');

const { mutate, isPending } = useCreateUser();

const onSubmit = handleSubmit((values) => mutate(values));
</script>

<template>
  <form @submit="onSubmit">
    <input v-model="name" v-bind="nameAttrs" />
    <span v-if="errors.name" class="text-red-500">{{ errors.name }}</span>

    <input v-model="email" v-bind="emailAttrs" />
    <span v-if="errors.email" class="text-red-500">{{ errors.email }}</span>

    <button :disabled="isPending">{{ isPending ? 'Salvando...' : 'Criar' }}</button>
  </form>
</template>
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New page | Create page component → add route to `router/index.ts` |
| Auth guard | Navigation guard: `router.beforeEach` + check `useAuthStore` |
| API data | Create composable in `composables/use{Resource}.ts` with vue-query |
| Global state | Pinia store in `stores/{name}.store.ts` |
| Form | VeeValidate + Zod schema → submit calls `useMutation` |
| Reactivity bug | Check `.value` access + `ref` vs `reactive` usage |

---

## TESTING PATTERNS

```typescript
// __tests__/UserCard.test.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query';
import UserCard from '../components/UserCard.vue';

function createWrapper(props = {}) {
  return mount(UserCard, {
    props: { user: { id: '1', name: 'Test', email: 'test@test.com' }, ...props },
    global: {
      plugins: [VueQueryPlugin, { queryClient: new QueryClient() }],
    },
  });
}

describe('UserCard', () => {
  it('renders user name', () => {
    const wrapper = createWrapper();
    expect(wrapper.text()).toContain('Test');
  });

  it('emits select event on click', async () => {
    const wrapper = createWrapper();
    await wrapper.trigger('click');
    expect(wrapper.emitted('select')).toBeTruthy();
  });
});
```

---

## NAMING CONVENTIONS

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Components | PascalCase `.vue` | `UserCard.vue` |
| Composables | `use` prefix `.ts` | `useAuth.ts` |
| Stores | `.store.ts` suffix | `auth.store.ts` |
| Pages | PascalCase `.vue` | `DashboardPage.vue` |
| Types | PascalCase | `User`, `ApiResponse<T>` |

---

## ENV VARS

```env
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=My App
```

## BUILD COMMANDS

```bash
npm run dev          # Vite HMR
npm run build        # tsc + vite build
npm test             # Vitest
npm run lint         # ESLint
npm run preview      # Preview prod build
```

---

## QUALITY GATES

□ `npx tsc --noEmit` — 0 errors
□ `npm test` — all tests pass
□ Vue DevTools — no unexpected re-renders
□ Pinia stores: no state mutations outside actions
□ All async ops show loading state to user
□ All forms validate with VeeValidate + Zod before submit

---

## FORBIDDEN

- NEVER use Options API in new code
- NEVER access `ref` without `.value` in script
- NEVER put server data in Pinia (use TanStack Query)
- NEVER use `this` (Composition API doesn't have `this`)
- NEVER skip TypeScript generics on `defineProps`/`defineEmits`
- NEVER use `v-html` with user-provided content (XSS risk)
