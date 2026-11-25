---
name: tpl-frontend-react-ts-zustand-query
description: Template do pack (frontend/02-react-ts-zustand-query.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/02-react-ts-zustand-query.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App React]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/02-react-ts-zustand-query.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — React 19 + TypeScript + Zustand + TanStack Query (Enterprise Pattern)
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | React | 19.x |
| Linguagem | TypeScript | 5.x (strict) |
| Bundler | Vite | 6.x |
| Styling | Tailwind CSS + shadcn/ui | v4 |
| Server State | TanStack Query | v5 |
| Client State | Zustand + immer middleware | v5 |
| Forms | React Hook Form + Zod | latest |
| HTTP | Axios (configured instance) | latest |
| Tests | Vitest + Testing Library | latest |

---

## PROJECT STRUCTURE
```
src/
├── components/ui/       # shadcn/ui components (CLI-generated)
├── components/shared/   # Custom reusable components
├── features/
│   └── {feature}/
│       ├── components/  # Feature-specific components
│       ├── hooks/       # useQuery/useMutation wrappers
│       ├── store.ts     # Zustand slice (client state only)
│       ├── api.ts       # Axios + TanStack Query keys
│       ├── types.ts     # Feature-local types
│       └── index.ts     # Public re-exports
├── lib/
│   ├── axios.ts         # Instance with interceptors
│   ├── query-client.ts  # QueryClient singleton
│   └── utils.ts         # cn() + pure helpers
├── stores/              # Global Zustand stores
└── types/               # Global types + API response types
```

---

## MENTAL MODEL — State Split

```
Server State (TanStack Query)     Client State (Zustand)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ━━━━━━━━━━━━━━━━━━━━━━━━━
✅ API responses                  ✅ UI state (sidebar, modals)
✅ Cached entities                ✅ Theme/locale preferences
✅ Pagination state               ✅ Wizard/stepper progress
✅ Background refetching          ✅ Temporary form drafts
✅ Optimistic mutations           ✅ Notification queue

NEVER: Server data in Zustand
NEVER: UI toggles in TanStack Query
```

---

## ZUSTAND RULES

```typescript
// stores/ui.store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface UIState {
  sidebarOpen: boolean;
  notifications: Notification[];
  toggleSidebar: () => void;
  addNotification: (n: Notification) => void;
  dismissNotification: (id: string) => void;
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      immer((set) => ({
        sidebarOpen: true,
        notifications: [],
        toggleSidebar: () => set((s) => { s.sidebarOpen = !s.sidebarOpen; }),
        addNotification: (n) => set((s) => { s.notifications.push(n); }),
        dismissNotification: (id) => set((s) => {
          s.notifications = s.notifications.filter((n) => n.id !== id);
        }),
      })),
      { name: 'ui-store' }
    ),
    { name: 'UIStore' }
  )
);

// ✅ CORRETO — selector específico (re-render mínimo)
const sidebarOpen = useUIStore((s) => s.sidebarOpen);

// ❌ ERRADO — sem selector (re-render em QUALQUER mudança)
const store = useUIStore();
```

**Rules:**
- Each store in separate file: `stores/{name}.store.ts`
- Use `immer` for complex state (nested objects/arrays)
- Expose only needed data — use selectors to prevent re-renders
- Use `persist` middleware when state should survive page refresh
- NEVER store derived data (compute with selectors or `useMemo`)

---

## TANSTACK QUERY RULES

```typescript
// features/users/api.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/axios';

// Query key factory — consistent invalidation
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Record<string, unknown>) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

export function useUsers(filters = {}) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => api.get('/users', { params: filters }).then((r) => r.data),
    staleTime: 5 * 60 * 1000, // 5 min cache
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => api.get(`/users/${id}`).then((r) => r.data),
    enabled: !!id, // Don't fetch until id is available
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/users/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}
```

**Rules:**
- Query keys as factory with `as const`
- Mutations ALWAYS invalidate related queries on success
- All queries have explicit `staleTime` (don't rely on default)
- Optimistic updates for actions that feel slow (toggles, likes)
- `enabled` option for conditional queries

---

## AXIOS INTERCEPTORS

```typescript
// lib/axios.ts
import axios from 'axios';
import { useAuthStore } from '@/stores/auth.store';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Auth token injection
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Token refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      try {
        await useAuthStore.getState().refreshToken();
        return api(error.config);
      } catch {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New async data | TanStack Query hook in `features/{name}/api.ts` with query key factory |
| Cross-feature state | Zustand store in `stores/{name}.store.ts` |
| Complex form | Zod schema → RHF → submit calls `useMutation` |
| Performance re-renders | Check: store selectors too broad? Missing `staleTime`? |
| Cache invalidation | `queryClient.invalidateQueries({ queryKey: keys.lists() })` |
| Optimistic update | `useMutation` with `onMutate`, `onError`, `onSettled` |
| Auth integration | Interceptor in `lib/axios.ts` + `auth.store.ts` |

---

## TESTING PATTERNS

```typescript
// features/users/__tests__/useUsers.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { useUsers } from '../api';

const server = setupServer(
  http.get('/api/users', () => HttpResponse.json([{ id: '1', name: 'Test' }])),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function wrapper({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}

test('fetches users', async () => {
  const { result } = renderHook(() => useUsers(), { wrapper });
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data).toHaveLength(1);
});
```

---

## NAMING CONVENTIONS

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | `use` prefix | `useUserProfile.ts` |
| Stores | `.store.ts` suffix | `ui.store.ts` |
| API files | `api.ts` per feature | `features/users/api.ts` |
| Query keys | `{entity}Keys` factory | `userKeys.list(filters)` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` |

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
□ `npm test -- --coverage` — coverage > 70%
□ No Zustand subscriptions without selectors
□ All TanStack Query mutations show loading state
□ All error responses handled with user-facing feedback
□ Skeleton loaders (not spinners) for all list/table loads

---

## FORBIDDEN

- NEVER share state via props drilling (>2 levels → store)
- NEVER `queryClient.invalidateQueries` without specific queryKey
- NEVER `useEffect` to sync two pieces of state (derive instead)
- NEVER store derived data in Zustand (compute in selectors)
- NEVER use `any` without documented reason
- NEVER use Context for data that TanStack Query handles
