---
name: optimistic-updates
description: >-
  Use when implementing optimistic UI for mutations: instant likes, inline edits,
  toggles, delete-then-undo, or any action that should feel instant before the
  server confirms. Not for read-only views or critical writes that must wait for
  server confirmation (payments, auth).
---

# Optimistic updates

Apply the change in the UI **before** the server confirms, then reconcile.

## When to use

| Good fit | Bad fit |
|----------|---------|
| Likes, reactions, follow toggles | Payments, refunds |
| Inline rename, status toggle | Account deletion |
| Delete with undo toast | Auth state changes |
| Reorder lists | Anything requiring fresh server state to be correct |

## SWR pattern

```ts
async function toggleLike(post: Post) {
  const key = ["post", post.id] as const;
  const next = { ...post, liked: !post.liked, like_count: post.like_count + (post.liked ? -1 : 1) };

  await mutate(
    key,
    async () => {
      await api.toggleLike(post.id);
      return next;
    },
    { optimisticData: next, rollbackOnError: true, revalidate: false },
  );
}
```

## TanStack Query pattern

```ts
const m = useMutation({
  mutationFn: api.toggleLike,
  onMutate: async (post) => {
    await qc.cancelQueries({ queryKey: ["post", post.id] });
    const prev = qc.getQueryData<Post>(["post", post.id]);
    qc.setQueryData(["post", post.id], (p?: Post) =>
      p ? { ...p, liked: !p.liked } : p,
    );
    return { prev };
  },
  onError: (_e, post, ctx) => {
    if (ctx?.prev) qc.setQueryData(["post", post.id], ctx.prev);
  },
  onSettled: (_d, _e, post) => {
    qc.invalidateQueries({ queryKey: ["post", post.id] });
  },
});
```

## Delete with undo

1. Optimistically remove the row from the list.
2. Show a Sonner toast: "Project deleted — Undo" for 5 s.
3. On Undo: cancel the pending delete.
4. After timeout: actually call the delete API.

This avoids confirmation dialogs for low-risk deletes.

## Rules

- **Always rollback** on error and surface a toast.
- Disable the trigger only if the user must wait (rare for optimistic flows).
- Reconcile by refetching once on settled — the optimistic value can drift (denormalized counts, server-side timestamps).
- Don't optimistically commit work that has visible side effects elsewhere (charges, emails sent).

## Avoid

- Optimistic update without rollback — UI lies on failure.
- Optimistic for payments or anything irreversible.
- Forgetting to update **all** affected cache keys (list + detail).
