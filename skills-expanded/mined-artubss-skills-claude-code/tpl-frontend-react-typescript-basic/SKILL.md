---
name: tpl-frontend-react-typescript-basic
description: Template do pack (frontend/01-react-typescript-basic.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/01-react-typescript-basic.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App React]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/01-react-typescript-basic.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — React 19 + TypeScript + Vite
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | React | 19.x |
| Linguagem | TypeScript | 5.x (strict) |
| Bundler | Vite | 6.x |
| Estilização | Tailwind CSS | v4 |
| Server State | TanStack Query | v5 |
| Client State | Zustand | 5.x |
| Forms | React Hook Form + Zod | latest |
| Routing | React Router | v7 |
| Testes | Vitest + Testing Library + Playwright | latest |

---

## PROJECT STRUCTURE

```
src/
├── components/           # UI reutilizável (botões, inputs, modals)
│   ├── ui/               # Primitivos: Button, Input, Modal, Card
│   └── layout/           # Header, Sidebar, Footer, PageLayout
├── features/             # Módulos de feature (cada feature = pasta isolada)
│   └── {feature}/
│       ├── components/   # Componentes específicos da feature
│       ├── hooks/        # Hooks específicos (ex: useUsers.ts)
│       ├── api.ts        # TanStack Query hooks + API calls
│       ├── types.ts      # Tipos locais da feature
│       └── index.ts      # Re-export público
├── hooks/                # Hooks globais compartilhados
├── lib/
│   ├── api-client.ts     # Axios/fetch configurado com interceptors
│   ├── query-client.ts   # TanStack QueryClient config
│   └── utils.ts          # Helpers puros
├── pages/                # Páginas (React Router v7)
├── stores/               # Zustand stores
└── types/                # Tipos globais + generics
```

**Regra de colocation:** tudo de uma feature vive junto. Se deletar a pasta, a feature inteira desaparece sem side effects.

---

## MENTAL MODEL — Feature Module Pattern

### Criando uma nova feature

```typescript
// src/features/projects/types.ts
export interface Project {
  id: string;
  name: string;
  status: 'active' | 'archived';
  createdAt: string;
}

// src/features/projects/api.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { Project } from './types';

export const projectKeys = {
  all: ['projects'] as const,
  list: (filters: Record<string, unknown>) => [...projectKeys.all, 'list', filters] as const,
  detail: (id: string) => [...projectKeys.all, 'detail', id] as const,
};

export function useProjects(filters = {}) {
  return useQuery({
    queryKey: projectKeys.list(filters),
    queryFn: () => apiClient.get<Project[]>('/projects', { params: filters }),
  });
}

export function useCreateProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Omit<Project, 'id' | 'createdAt'>) =>
      apiClient.post<Project>('/projects', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: projectKeys.all });
    },
  });
}
```

### Form com Zod + React Hook Form

```typescript
// src/features/projects/components/CreateProjectForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateProject } from '../api';

const createProjectSchema = z.object({
  name: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  status: z.enum(['active', 'archived']),
});

type FormData = z.infer<typeof createProjectSchema>;

export function CreateProjectForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(createProjectSchema),
  });
  const createProject = useCreateProject();

  const onSubmit = (data: FormData) => createProject.mutate(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} placeholder="Nome do projeto" />
      {errors.name && <p className="text-red-500 text-sm">{errors.name.message}</p>}
      <button type="submit" disabled={createProject.isPending}>
        {createProject.isPending ? 'Criando...' : 'Criar Projeto'}
      </button>
    </form>
  );
}
```

---

## COMPONENT RULES

- Functional components only — NEVER class components
- NEVER put API calls directly in components — use TanStack Query hooks
- All forms: React Hook Form + Zod resolver (schema FIRST, then form)
- Extract repeated UI into `/components/ui/`, business logic into hooks
- Props interface on same file, prefixed with component name: `ButtonProps`
- Use `React.ComponentPropsWithoutRef<'element'>` para props de HTML nativo

```typescript
// ✅ CORRETO — componente com tipos explícitos
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
}

export function UserCard({ user, onEdit }: UserCardProps) { /* ... */ }

// ❌ ERRADO — props inline, sem tipos
export function UserCard(props: any) { /* ... */ }
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New page needed | Create `pages/FeaturePage.tsx` → add to router → create feature folder |
| New form | Create Zod schema FIRST → RHF form → submit handler → success/error states |
| API integration | Create `features/{name}/api.ts` → define query keys → add TanStack Query hook |
| Global state needed | Create Zustand store in `stores/{name}.store.ts` → NEVER for server state |
| Component library need | Check shadcn/ui FIRST → if not there, build with Tailwind |
| Performance issue | React DevTools Profiler → flame graph → memo/useCallback only if measured slow |
| Auth flow needed | Store token in httpOnly cookie → interceptor in api-client → redirect on 401 |
| Error boundary needed | Create `ErrorBoundary.tsx` → wrap route/feature → log to monitoring |

---

## STATE MANAGEMENT DECISION TREE

```
Dado vem do servidor? ─── SIM → TanStack Query (useQuery / useMutation)
         │
         NÃO
         │
Múltiplos componentes usam? ─── SIM → Zustand store
         │
         NÃO
         │
É estado de UI local? ─── SIM → useState / useReducer
         │
         NÃO
         │
É tema/locale/auth? ─── SIM → Context (wrap App)
```

**NUNCA** use Context para dados que TanStack Query pode cachear.
**NUNCA** use Zustand para dados que vêm de API — use TanStack Query.

---

## ZUSTAND STORE PATTERN

```typescript
// src/stores/ui.store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      sidebarOpen: true,
      theme: 'light',
      toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'ui-store' }
  )
);

// Uso: const sidebarOpen = useUIStore((s) => s.sidebarOpen);
// SEMPRE use selectors — NUNCA useUIStore() sem selector (re-render total)
```

---

## TESTING PATTERNS

```typescript
// src/features/projects/__tests__/ProjectList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { ProjectList } from '../components/ProjectList';

const server = setupServer(
  http.get('/api/projects', () =>
    HttpResponse.json([{ id: '1', name: 'Test', status: 'active' }])
  ),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

test('renders project list from API', async () => {
  renderWithProviders(<ProjectList />);
  await waitFor(() => {
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

---

## QUALITY GATES

Before any PR:
□ `npx tsc --noEmit` — 0 errors
□ `npm test` — all tests pass
□ `npm run lint` — 0 errors
□ No `any` without comment explaining why
□ Loading and error states for all async operations
□ Mobile responsive (375px minimum)
□ No hardcoded strings (use i18n or constants)
□ Every TanStack Query has error handling (isError / error boundary)

---

## FORBIDDEN

- NEVER use `any` without documented reason
- NEVER inline styles (use Tailwind classes)
- NEVER use `useEffect` for data fetching (use TanStack Query)
- NEVER mutate state directly (Zustand's immer if needed)
- NEVER hardcode API URLs — use `VITE_API_URL` env var
- NEVER call API directly in component body
- NEVER use `useCallback`/`useMemo` without measuring performance first
- NEVER use Redux/MobX — TanStack Query + Zustand cover everything

---

## NAMING CONVENTIONS

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | camelCase + `use` | `useUserProfile.ts` |
| Stores | camelCase + `.store.ts` | `user.store.ts` |
| API files | camelCase + `api.ts` | `features/users/api.ts` |
| Types | PascalCase | `UserProfile`, `ApiResponse<T>` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` in `lib/constants.ts` |
| Tests | `__tests__/Name.test.tsx` | `__tests__/UserCard.test.tsx` |

---

## ENV VARS

```env
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=My App
VITE_SENTRY_DSN=               # Error monitoring (optional)
```

## BUILD COMMANDS

```bash
npm run dev          # Start dev server (Vite HMR)
npm run build        # Production build (tsc + vite build)
npm run test         # Run Vitest
npm run test:e2e     # Run Playwright
npm run lint         # ESLint + TypeScript check
npm run preview      # Preview production build locally
```

## COMMON RECIPES

### Protected Route
```typescript
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: user, isLoading } = useCurrentUser();
  if (isLoading) return <Spinner />;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}
```

### Optimistic Update
```typescript
useMutation({
  mutationFn: updateProject,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: projectKeys.detail(id) });
    const previous = queryClient.getQueryData(projectKeys.detail(id));
    queryClient.setQueryData(projectKeys.detail(id), newData);
    return { previous };
  },
  onError: (_err, _new, context) => {
    queryClient.setQueryData(projectKeys.detail(id), context?.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: projectKeys.detail(id) });
  },
});
```
