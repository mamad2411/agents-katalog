---
name: data-fetching
description: React Query + Supabase data fetching patterns for Next.js projects. Covers server-component vs client fetching, mutation strategies, cache updates, and Supabase read-after-write gotchas. Use when writing useMutation hooks, deciding where a fetch belongs, or debugging stale UI after mutations.
---

Apply the following data-fetching patterns to all React Query + Supabase code in this project.

## Stack

- `@tanstack/react-query` — client-side server state, caching, mutations
- `@supabase/ssr` clients — Postgres via HTTP API (browser client in client components, server client in server components / route handlers)

## Server component vs React Query — the decision

| Situation | Fetch with |
| --- | --- |
| Initial page data, read-only render (list page first paint, detail view) | **Server component** — `await createClient()` then query directly; no loading spinner, no client JS |
| Data the user mutates, filters, paginates, or that must refresh without navigation | **React Query** in a client component |
| Both (fast first paint + interactive after) | Server component fetches, passes the result as `initialData` to the client hook |

```tsx
// app/(dashboard)/projects/page.tsx — server component
const supabase = await createClient()
const { data: projects } = await supabase.from('projects').select('*').order('created_at', { ascending: false })
return <ProjectList initialData={projects ?? []} />

// src/features/projects/useProjects.ts — client hook
const useProjects = (initialData: Project[]) =>
  useQuery({
    queryKey: PROJECTS_KEY,
    queryFn: async () => {
      const { data, error } = await supabase.from('projects').select('*').order('created_at', { ascending: false })
      if (error) throw error
      return data
    },
    initialData,
  })
```

Never fetch with `useEffect` + `useState` — that path has no caching, no dedup, no retry, and it always gets rewritten later.

## Mutation strategies

There are two distinct mutation patterns depending on whether you know the final record shape before the API responds.

### Creates — use `onSuccess` only

For inserts, the server assigns the real `id` (UUID). Never use `onMutate` with a temp id — when the real id arrives it causes a key change in React lists, which unmounts and remounts the row and replays any entry animation.

```ts
const useCreateProject = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (input: ProjectInput) => {
      const { data, error } = await supabase.from('projects').insert(input).select().single()
      if (error) throw error
      return data
    },
    onSuccess: (newProject) => {
      queryClient.setQueryData<Project[]>(PROJECTS_KEY, (old) => [newProject, ...(old ?? [])])
    },
    // ❌ do NOT add onSettled: invalidateQueries — see race condition below
  })
}
```

### Updates and deletes — use `onMutate` for optimistic updates

For mutations where you already know the full new state (deletes, field updates, toggles), optimistic updates via `onMutate` are safe because no id changes:

```ts
onMutate: async (id) => {
  await queryClient.cancelQueries({ queryKey: PROJECTS_KEY })
  const previous = queryClient.getQueryData<Project[]>(PROJECTS_KEY)
  queryClient.setQueryData<Project[]>(PROJECTS_KEY, (old) => (old ?? []).filter((p) => p.id !== id))
  return { previous }
},
onError: (_err, _vars, ctx) => {
  if (ctx?.previous) queryClient.setQueryData(PROJECTS_KEY, ctx.previous)
},
onSettled: () => queryClient.invalidateQueries({ queryKey: PROJECTS_KEY }),
```

## Supabase read-after-write race

**Do not call `invalidateQueries` in `onSettled` for create mutations.**

Supabase uses an HTTP API — the `insert` and the subsequent `select` are separate HTTP calls to a connection pool. A `refetch` triggered immediately after an insert can complete before the insert is visible to reads, returning stale data that overwrites the `onSuccess` cache update. The symptom is: new item flashes into view then disappears, only reappearing after a manual refetch (e.g. navigating away and back).

```text
onSuccess → setQueryData([newProject, ...])  ✓ UI updates
onSettled → invalidateQueries → refetch      ✗ Supabase returns old data → cache reverts
```

For creates: `onSuccess` + `setQueryData` is sufficient. Refetch-on-window-focus (React Query's default) provides eventual consistency when the user returns to the tab.

For deletes and updates: `invalidateQueries` in `onSettled` is safe because the mutation completes before `onSettled` fires, and the data was already removed/changed server-side by then.

The same race applies to **server components after a server action**: `revalidatePath()` immediately after an insert can render the stale list. When a page pairs a server action with `revalidatePath`, verify the new row actually appears; if it flickers, return the created row from the action and patch the client cache instead.

## Query client setup (App Router)

One `QueryClient` per browser session, created in state so React strict-mode double-render doesn't duplicate it:

```tsx
// src/components/Providers.tsx
'use client'
const Providers = ({ children }: { children: ReactNode }) => {
  const [queryClient] = useState(
    () => new QueryClient({ defaultOptions: { queries: { staleTime: 30_000 } } }),
  )
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
```

Mount it once in `app/layout.tsx`. A module-level `new QueryClient()` leaks cache between users under SSR — never do it.

## Cache key convention

Use a `const` tuple so TypeScript catches mismatches across hooks, and include the tenant id so switching businesses can never serve another tenant's cached rows:

```ts
const PROJECTS_KEY = ['projects', businessId] as const
```

## Route handlers

`app/api/**/route.ts` is for callers that aren't your React tree: webhooks, cron, third parties. Your own components should query Supabase directly (RLS is the authorization layer) or use server actions — don't build a REST layer in front of Supabase just to fetch your own data. Every route handler zod-parses its input and returns typed JSON.
