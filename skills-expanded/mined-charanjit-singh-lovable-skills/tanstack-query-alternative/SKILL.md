---
name: tanstack-query-alternative
description: >-
  Use when adding or refactoring data fetching with TanStack Query (React Query)
  in Lovable projects: useQuery, useMutation, query keys, cache invalidation,
  Supabase fetchers. This is the default data layer for Lovable. Not for forms
  validation alone or one-off fetches outside a hook.
---

# TanStack Query patterns (default for Lovable)

TanStack Query is Lovable's default data-fetching library. Use it for **every** server-state read and write. Reach for `useEffect` + `fetch` only when no cache is desired (e.g. one-shot edge POSTs without revalidation).

Pair with:

- [`tanstack-mutations-and-invalidation`](../tanstack-mutations-and-invalidation/) — write paths
- [`tanstack-infinite-queries`](../tanstack-infinite-queries/) — pagination and infinite scroll
- [`tanstack-prefetch-and-hydration`](../tanstack-prefetch-and-hydration/) — route prefetching, SSR hydration

For SWR-first projects, use [`typed-api-hooks-forms`](../typed-api-hooks-forms/) instead. **Pick one library per app — never mix.**

---

## File layout

```
src/
  lib/
    supabase.ts
    query-client.ts        # QueryClient + defaults
  types/
    database.ts            # generated Supabase types
  api/
    users.ts               # pure fetchers (no React)
    projects.ts
  hooks/
    queries/
      useUser.ts
      useProjects.ts
    mutations/
      useCreateProject.ts
      useDeleteProject.ts
```

Rules:

- **Fetchers in `api/`** — async, typed, throw on error.
- **Hooks in `hooks/queries/`** — only `useQuery` wiring; no JSX, no business logic.
- **Mutations in `hooks/mutations/`** — `useMutation` + invalidation policy.
- Never call `supabase.from(...)` inside a component.

---

## QueryClient defaults

```ts
// src/lib/query-client.ts
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,            // 30s — tune per resource
      gcTime: 5 * 60 * 1000,        // 5m
      refetchOnWindowFocus: false,  // Lovable apps usually don't need it
      retry: (failureCount, err) => {
        if (isHttpStatus(err, [401, 403, 404])) return false;
        return failureCount < 2;
      },
    },
    mutations: {
      retry: false,
    },
  },
});
```

Wrap the app **once**:

```tsx
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

Add `ReactQueryDevtools` in dev for cache inspection.

---

## Query keys — factory pattern

Centralize keys so invalidation can't drift:

```ts
// src/hooks/queries/keys.ts
export const userKeys = {
  all: ["users"] as const,
  detail: (id: string) => [...userKeys.all, "detail", id] as const,
};

export const projectKeys = {
  all: ["projects"] as const,
  list: (filters: { status?: string; orgId?: string }) =>
    [...projectKeys.all, "list", filters] as const,
  detail: (id: string) => [...projectKeys.all, "detail", id] as const,
};
```

Rules:

- Tuple keys, broadest segment first (`["projects", "list", ...]`).
- Filter objects are fine — TanStack hashes them deterministically. But keep filter shapes stable.
- Don't sprinkle ad-hoc strings (`"user-" + id`); always go through the factory.

---

## Typed query hook

```ts
// src/api/users.ts
import type { Database } from "@/types/database";
type User = Database["public"]["Tables"]["users"]["Row"];

export async function fetchUser(id: string): Promise<User | null> {
  const { data, error } = await supabase
    .from("users")
    .select("*")
    .eq("id", id)
    .maybeSingle();
  if (error) throw error;
  return data;
}
```

```ts
// src/hooks/queries/useUser.ts
import { useQuery } from "@tanstack/react-query";
import { fetchUser } from "@/api/users";
import { userKeys } from "./keys";

export function useUser(id: string | null | undefined) {
  return useQuery({
    queryKey: id ? userKeys.detail(id) : userKeys.detail("none"),
    queryFn: () => fetchUser(id!),
    enabled: !!id,
  });
}
```

The hook returns the full `UseQueryResult` — components destructure `{ data, isLoading, error, refetch }` directly. Do not invent custom return shapes that lose generics.

---

## Deduping — same key = one request

Three components calling `useUser(id)` with the same `id` share one network request and one cache entry. Get this for free by **using the key factory everywhere**.

When several UI surfaces need the **same Supabase graph** on a screen, write **one query** with a joined select, not three:

```ts
// api/posts.ts
export async function fetchPostDetail(postId: string) {
  const { data, error } = await supabase
    .from("posts")
    .select(`
      *,
      author:users!posts_author_id_fkey ( id, display_name, avatar_url ),
      comments ( id, body, created_at, author:users ( id, display_name ) )
    `)
    .eq("id", postId)
    .single();
  if (error) throw error;
  return data;
}

// hooks/queries/usePostDetail.ts
export function usePostDetail(postId: string | undefined) {
  return useQuery({
    queryKey: postKeys.detail(postId ?? "none"),
    queryFn: () => fetchPostDetail(postId!),
    enabled: !!postId,
  });
}
```

Strategy matrix:

| Situation | Approach |
|-----------|----------|
| Same entity, many components | One hook + shared key |
| Same table, different filters | One hook, distinct keys per filter |
| List + detail with overlap | List hook for list; detail hook with richer `select` |
| Many components need full graph | Single joined fetcher + one hook |

---

## Loading and error UX

- `isLoading` (first load) vs `isFetching` (background refetch) — only show skeletons on `isLoading`.
- `isError`: show retry calling `refetch()`.
- Pair with [`error-states-and-empty-ui`](../error-states-and-empty-ui/).

---

## Mutations (overview — see deep dive)

```ts
const m = useMutation({
  mutationFn: api.createProject,
  onSuccess: () => qc.invalidateQueries({ queryKey: projectKeys.all }),
});
```

Optimistic UI, complex invalidation, and rollback: see [`tanstack-mutations-and-invalidation`](../tanstack-mutations-and-invalidation/) and [`optimistic-updates`](../optimistic-updates/).

---

## Avoid

- `useEffect` + `fetch` for server state.
- Inline Supabase calls in components.
- Mixing SWR and TanStack Query in one project.
- Ad-hoc string keys outside the factory.
- Wrapping `useQuery` in a custom shape that hides `isFetching`, `dataUpdatedAt`, or `error`.
- `refetchOnWindowFocus: true` on heavy queries (kills cost when users tab back).

## Checklist

- [ ] Single `QueryClient` at the app root with sane defaults.
- [ ] Key factories per resource, used everywhere.
- [ ] Typed fetchers in `api/`; hooks in `hooks/queries`.
- [ ] One joined query per screen instead of N parallel ones.
- [ ] DevTools mounted in dev for cache inspection.
