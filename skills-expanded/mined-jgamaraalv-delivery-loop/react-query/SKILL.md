---
name: react-query
description: Guidelines for using React Query for data fetching, caching, and server state synchronization in React applications
---

## Core Principles

- Use React Query for all data fetching and caching
- Leverage React Query's built-in state management instead of `useState` for server data
- Use React Context and `useReducer` for managing client-side global state
- Avoid excessive API calls through proper caching strategies
- Always handle loading states and errors properly

## Topics by Concern

| Concern                     | Reference                        |
| --------------------------- | -------------------------------- |
| Client setup & file layout  | `references/setup.md`            |
| Reading data                | `references/queries.md`          |
| Writing data                | `references/mutations.md`        |
| Server vs. client state     | `references/state-management.md` |
| Caching speed & re-renders  | `references/performance.md`      |
| Failure handling & recovery | `references/error-handling.md`   |

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/setup.md` — feature-based project structure plus the one-time `QueryClient`/`QueryClientProvider` configuration (staleTime, cacheTime, retry, DevTools) · read when scaffolding React Query in a project or tuning client defaults.
- `references/queries.md` — query hooks: basic typed query, service-thrown user-friendly errors, dependent (`enabled`) queries, paginated (`keepPreviousData`) queries, and `useInfiniteQuery` · read when fetching/reading any server data.
- `references/mutations.md` — mutation hooks: basic mutation with cache invalidation, and the four-callback optimistic-update pattern (`onMutate`/`onError`/`onSettled`) · read when creating, updating, or deleting server data.
- `references/state-management.md` — the server-state vs. client-state split, integrating React Query alongside Context/Reducer or Zustand · read when deciding where a piece of state lives or wiring React Query into existing global state.
- `references/performance.md` — structured query-key factories, `select` for selective subscriptions, and prefetching on user intent · read when invalidation is imprecise, components re-render too often, or navigation feels slow.
- `references/error-handling.md` — global `QueryClient` `onError` defaults and `QueryErrorResetBoundary` + error boundaries with retry · read when standardizing error behavior or adding render-time error recovery.

## Key Conventions

1. Use React Query DevTools to inspect cache and track query status
2. Group react-query hooks within feature-specific directories (feature-based organization)
3. Always handle errors properly with user-friendly messages and retry options
4. Fetch only required data - use API parameters to reduce data transfer
5. Avoid deeply nesting queries - flatten when possible for better performance
6. Use local state for component-specific data, global state for shared data
7. Leverage React Query's built-in caching and state management capabilities

## Anti-Patterns to Avoid

- Do not use `useEffect` for data fetching
- Do not store server data in `useState`
- Do not forget loading and error state handling
- Do not create queries without proper cache invalidation strategies
- Do not skip the `enabled` option for conditional queries
- Do not ignore TypeScript types for query responses
