---
name: workspace-aware-zustand-persist
description: Zustand persist storage that auto-namespaces keys by workspace slug, with microtask-deferred rehydration on workspace switch.
category: architecture
version: 1.0.0
tags: [zustand, persist, workspace, multi-tenancy, storage]
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

- Zustand stores persisting to localStorage in a multi-workspace app.
- Each workspace should have its own view filters, drafts, recent items — not a shared pool.
- You must guarantee that switching workspaces does not leak state from the previous one.

## Steps

1. Paired module-level singletons for the current workspace identity:
   ```ts
   let _currentSlug: string | null = null;
   let _currentWsId: string | null = null;
   const _rehydrateFns: Array<() => void> = [];
   ```
2. Setter that is idempotent on equal slug and defers side effects to a microtask:
   ```ts
   export function setCurrentWorkspace(slug: string | null, wsId: string | null) {
     if (_currentSlug === slug) { _currentWsId = wsId; return; }
     _currentSlug = slug; _currentWsId = wsId;
     queueMicrotask(() => {
       for (const fn of _rehydrateFns) fn();
     });
   }
   ```
   Why microtask: zustand persist rehydrate internally calls setState, which React 19 forbids during render. Deferring to a microtask sidesteps the warning.
3. Storage adapter that namespaces every key with the current slug:
   ```ts
   export function createWorkspaceAwareStorage(adapter: StorageAdapter): StateStorage {
     const resolve = (key: string) => (_currentSlug ? `${key}:${_currentSlug}` : key);
     return {
       getItem:    (k) => adapter.getItem(resolve(k)),
       setItem:    (k, v) => adapter.setItem(resolve(k), v),
       removeItem: (k) => adapter.removeItem(resolve(k)),
     };
   }
   ```
4. Every workspace-scoped store uses this storage AND registers for rehydration:
   ```ts
   export const useIssuesViewStore = create<IssuesViewState>()(
     persist(
       (set) => ({ /* ... */ }),
       {
         name: "myapp_issues_view",
         storage: createJSONStorage(() => createWorkspaceAwareStorage(defaultStorage)),
       },
     ),
   );
   registerForWorkspaceRehydration(() => useIssuesViewStore.persist.rehydrate());
   ```
5. Maintain a global list of workspace-scoped storage keys for cleanup on workspace delete / logout:
   ```ts
   const WORKSPACE_SCOPED_KEYS = [
     "myapp_issues_view", "myapp_issue_draft", "myapp_navigation", // ...
   ];
   export function clearWorkspaceStorage(adapter: StorageAdapter, slug: string) {
     for (const key of WORKSPACE_SCOPED_KEYS) adapter.removeItem(`${key}:${slug}`);
   }
   ```

## Example

User has stores for issue draft, view filters, recent issues in workspace `my-team`. On switch to `other-team`:
- `setCurrentWorkspace("other-team", "uuid-2")` fires.
- Every registered store's persist rehydrate runs on next microtask.
- Reads now go to `myapp_issue_draft:other-team`, totally independent from `my-team`'s drafts.

## Caveats

- Forgetting to register a store for rehydration is the single biggest bug source — the storage namespaces correctly on write, but on workspace switch the in-memory state still reflects the previous slug until something triggers a read. Prefer a single registration helper and document it loudly.
- Never persist ephemeral UI state (modal open, transient selection) — only things worth preserving across restarts.
- Don't persist server data; it belongs in the Query cache.
