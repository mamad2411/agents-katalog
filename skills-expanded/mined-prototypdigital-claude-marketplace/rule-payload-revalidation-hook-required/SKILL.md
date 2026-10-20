---
name: payload-revalidation-hook-required
description: Every Payload collection/global read on the front end needs afterChange/afterDelete revalidation hooks gated on context.disableRevalidate — no hook means a cache that silently never busts.
---

# Payload revalidation hook required

In a Payload + Next.js App Router app, cached front-end data only updates when something calls `revalidateTag`/`revalidatePath`. A collection read on the front end with no revalidation hook is a cache that never busts until TTL or redeploy — a silent stale-content bug.

## Rules

- Any collection or global **rendered on the front end** must define `afterChange` **and** `afterDelete` hooks that revalidate the tags/paths its content feeds.
- **Gate on `context.disableRevalidate`** so bulk imports, seeds, and migrations can opt out of cascading revalidation.
- Gate on `_status === 'published'` **only** when the collection has drafts (don't revalidate on every autosave).
- Bust tags through the shared cache-tag source of truth, not hardcoded strings — see the [`payload-cache-revalidation`](https://www.npmjs.com/package/bluetemberg-skills-payload-cache-revalidation) skill for the tag contract and per-locale vs locale-agnostic decision.
- A new front-end collection with no hook should fail review — add the hook in the same change that adds the collection.

## Examples

```ts
// BAD — front-end collection with no revalidation hook: edits never bust the cache until TTL/redeploy
export const Models: CollectionConfig = {
  slug: 'models',
  // no hooks → silent stale content
}

// BAD — hook present but no disableRevalidate gate and a hardcoded tag string (drifts from the fetcher)
const revalidateModel: CollectionAfterChangeHook = ({ doc }) => {
  revalidateTag(`models_${doc.slug}`, 'max') // hardcoded; fires during bulk imports/seeds too
  return doc
}

// GOOD — gated on context, published-only, tag built through the shared cacheTags source of truth
const revalidateModel: CollectionAfterChangeHook = ({ doc, context }) => {
  if (context.disableRevalidate) return doc
  if (doc._status === 'published') revalidateTag(cacheTags.model(doc.slug), 'max')
  return doc
}

export const Models: CollectionConfig = {
  slug: 'models',
  hooks: { afterChange: [revalidateModel], afterDelete: [revalidateModelDelete] },
}
```

## When NOT to apply

- Admin-only collections never read on the front end.
- Always-dynamic routes (`force-dynamic`, no `unstable_cache`) — nothing is cached to bust.
