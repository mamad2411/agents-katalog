---
applyTo: "**/*.{tsx,jsx}"
---

# React Coding Standards

## Functional Components Only

- Use typed function declarations or arrow functions — no class components
- Define `interface Props` for every component; export when reusable
- Use `React.FC<Props>` or explicit return types — be consistent per project
- Colocate component, types, styles, and tests in the same directory

## Hooks

- `useState` for local state; `useReducer` for complex state machines
- `useEffect` must always specify dependency arrays — no missing deps
- `useMemo` / `useCallback` only when profiling shows a performance need
- Extract custom hooks for reusable logic: `useAuth()`, `useFetch()`, `useDebounce()`
- Hooks must start with `use` and be called at the top level only

## State Management

- **Server state**: TanStack Query (`useQuery`, `useMutation`) with proper cache keys
- **Client state**: Zustand stores — one per domain concern
- Colocate state as low as possible in the component tree
- Lift state only when siblings need shared access
- Never duplicate server state in client stores

## TypeScript

- Strict mode enabled; no `any` types
- Use discriminated unions for variant types and component states
- Define API response types in `src/types/` and share with API layer
- Use `unknown` over `any` when type is genuinely unknown
- Generic components: `<T,>` syntax for JSX compatibility

## API Integration

- Centralized API client with axios/fetch in `src/api/client.ts`
- TanStack Query for all server state — define query keys in constants
- Optimistic updates via `useMutation` with `onMutate`/`onError`/`onSettled`
- Error boundaries for graceful failure handling

## Component Patterns

- Composition over inheritance — use children, render props, or hooks
- Container/presenter split for complex components
- Keep components under 150 lines; extract hooks for logic
- Use `React.lazy()` + `Suspense` for code splitting
- Memoize expensive renders with `React.memo()` only when profiled

## Testing

- Vitest + React Testing Library
- Test behavior, not implementation — query by role, label, text
- Use `screen.getByRole()` over `getByTestId()` wherever possible
- Mock API calls at the network layer (`msw`) not the module layer
- Test hooks in isolation with `renderHook()`

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API client and endpoint functions
│   ├── assets/        # Static assets
│   ├── components/    # Reusable UI components
│   │   └── ui/        # Base/design-system components
│   ├── hooks/         # Custom React hooks
│   ├── layouts/       # Layout components
│   ├── pages/         # Route-level page components
│   ├── routes/        # React Router config
│   ├── stores/        # Zustand stores
│   ├── types/         # Shared TypeScript types
│   ├── utils/         # Pure helper functions
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```
