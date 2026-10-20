---
name: optimistic-mutation-pattern
description: Standard React Query optimistic-update pattern with snapshot/restore on failure and onSettled invalidation — for CRUD mutations in realtime apps.
category: architecture
version: 1.0.0
tags: [react-query, optimistic, mutations, ux, patterns]
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

- CRUD on a Linear-style product (status change, priority, assignee, title edit).
- Server roundtrip is 100-300ms and you don't want the UI to stall.
- Your query keys are workspace-scoped and the cache is your single source of truth.

## Steps

1. `onMutate`: snapshot the current cache, apply the optimistic update, return the snapshot as context.
   ```ts
   onMutate: async (variables) => {
     await qc.cancelQueries({ queryKey: issueKeys.all(wsId) });
     const previous = qc.getQueryData(issueKeys.list(wsId, filters));
     qc.setQueryData(issueKeys.list(wsId, filters), (old) =>
       old?.map(issue => issue.id === variables.id ? { ...issue, ...variables.patch } : issue)
     );
     return { previous };
   },
   ```
2. `mutationFn`: actual server call, as usual.
3. `onError`: restore from snapshot in context.
   ```ts
   onError: (err, variables, context) => {
     if (context?.previous) {
       qc.setQueryData(issueKeys.list(wsId, filters), context.previous);
     }
   },
   ```
4. `onSettled`: invalidate so the final state reconciles with server truth.
   ```ts
   onSettled: () => qc.invalidateQueries({ queryKey: issueKeys.all(wsId) }),
   ```
5. For list mutations (create, delete), use the same pattern but splice the list instead of patching an item.

## Example

Change issue status:
```ts
const mutation = useMutation({
  mutationFn: ({ id, status }) => api.updateIssue(wsId, id, { status }),
  onMutate: async ({ id, status }) => {
    await qc.cancelQueries({ queryKey: issueKeys.all(wsId) });
    const previous = qc.getQueryData<Issue[]>(issueKeys.list(wsId, filters));
    qc.setQueryData<Issue[]>(issueKeys.list(wsId, filters), old =>
      old?.map(i => i.id === id ? { ...i, status } : i) ?? []
    );
    return { previous };
  },
  onError: (_err, _vars, ctx) => {
    if (ctx?.previous) qc.setQueryData(issueKeys.list(wsId, filters), ctx.previous);
  },
  onSettled: () => qc.invalidateQueries({ queryKey: issueKeys.all(wsId) }),
});

<Button onClick={() => mutation.mutate({ id: issue.id, status: "done" })}>Mark Done</Button>
```

## Caveats

- `cancelQueries` is important — it prevents an in-flight query from overwriting your optimistic value with stale server data.
- If multiple mutations on the same key fire back-to-back, `onMutate` sees the current cache (already optimistically updated by the earlier mutation) — usually what you want.
- Don't skip `onSettled` invalidation. The optimistic value might be wrong (server-side validation rejected the change); the invalidation is your self-healing step.
- For mutations that affect relationships (assignee changes affecting counts), invalidate all related keys — e.g. both `issueKeys.all(wsId)` and `memberKeys.workload(wsId, memberId)`.
