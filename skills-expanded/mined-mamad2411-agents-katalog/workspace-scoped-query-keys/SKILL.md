---
name: workspace-scoped-query-keys
description: Derive React Query keys from a wsId parameter so switching workspace automatically swaps the cache — no manual invalidation, no cross-tenant leakage.
category: architecture
version: 1.0.0
tags: [react-query, multi-tenancy, query-keys, workspace]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Multi-tenant React app using TanStack Query.
- You want workspace switches to "just work" — the right data appears, no manual `qc.invalidateQueries()` calls sprinkled around.

## Steps

1. Define a key factory per domain, parameterized by `wsId`:
   ```ts
   // packages/core/issues/queries.ts
   export const issueKeys = {
     all: (wsId: string) => ["issues", wsId] as const,
     list: (wsId: string, filters: IssueFilters) => ["issues", wsId, "list", filters] as const,
     detail: (wsId: string, id: string) => ["issues", wsId, "detail", id] as const,
   };
   ```
2. Hooks take `wsId` as the workspace identifier. Never reach for `useWorkspaceId()` Context inside the hook (that would tie it to a Provider that may not be mounted yet):
   ```ts
   export function useIssues(wsId: string, filters: IssueFilters) {
     return useQuery({
       queryKey: issueKeys.list(wsId, filters),
       queryFn: () => api.listIssues(wsId, filters),
       enabled: Boolean(wsId),
     });
   }
   ```
3. When the user switches workspaces, the new `wsId` flows through components via the workspace identity singleton → components re-render with new `wsId` → query key changes → React Query fetches fresh data. No explicit invalidation.
4. For mutations, use the same key factory to target invalidations:
   ```ts
   return useMutation({
     mutationFn: (input) => api.createIssue(wsId, input),
     onSettled: () => qc.invalidateQueries({ queryKey: issueKeys.all(wsId) }),
   });
   ```
5. For WS event handlers, read the current wsId from the workspace identity singleton:
   ```ts
   refreshMap.issue = () => {
     const wsId = getCurrentWsId();
     if (wsId) qc.invalidateQueries({ queryKey: issueKeys.all(wsId) });
   };
   ```

## Example

```
User in workspace A:
  qc has: issues/uuid-A/list/{status: todo}
  qc has: issues/uuid-A/detail/abc123

User switches to workspace B → setCurrentWorkspace("b", "uuid-B") → React rerenders:
  New useIssues(wsId: "uuid-B", ...) runs
  Query key changes from ["issues","uuid-A",...] to ["issues","uuid-B",...]
  React Query fetches workspace B's data
  Workspace A's cache entries stay (may get GC'd via gcTime) — no leakage
```

## Caveats

- If a hook has `useWorkspaceId()` in it, it won't work in components that render before the `WorkspaceIdProvider` mounts (sidebar, login screen chrome). Accept `wsId` as a parameter so you can pass `null` during pre-workspace states.
- Don't duplicate server data to Zustand stores — the key structure is what makes switching clean; copying data into stores defeats it.
- `gcTime` (10 min) governs how long stale workspace data lingers; tune it if memory pressure is a concern.
