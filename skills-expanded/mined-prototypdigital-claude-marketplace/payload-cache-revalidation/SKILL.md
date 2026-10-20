---
name: payload-cache-revalidation
description: Standardizes Next.js + Payload cache revalidation — a cacheTags source of truth, per-locale vs locale-agnostic tags, hooks per cached collection. Use when editing unstable_cache or revalidation hooks.
---

# payload-cache-revalidation

Use this skill whenever you add or change a cached data fetch (`unstable_cache`) or a Payload revalidation hook in a Payload CMS + Next.js App Router project. The goal: the producer (the fetch that sets `tags`) and the consumer (the hook that calls `revalidateTag`) can never drift apart, and a tag's locale scope matches what the page actually renders.

## Triggers

- Adding/editing an `unstable_cache(..., { tags })` call (typically under `app/`, data utilities, or globals).
- Adding/editing a Payload `afterChange` / `afterDelete` revalidation hook in a collection or global.
- Introducing a new Payload collection or global that is read on the front end (it needs a revalidation hook).
- Wiring a relationship field whose related doc is rendered inside an already-cached page or global.

## Required behavior

1. **Single source of truth.** Build every tag string through one shared `cacheTags` helper (a module of small builder functions). Never hardcode a tag string (`` `models_${slug}` ``) in a fetcher or hook — add/extend a `cacheTags` builder and use it on **both** sides. A producer and its consumer must reference the same `cacheTags` entry.

2. **Revalidate directly with `revalidateTag`.** Call `revalidateTag(cacheTags.x(...), 'max')` inside the hook. Prefer a direct call over an HTTP round-trip to a revalidate endpoint — only reach for an endpoint when invalidation must cross a process boundary that doesn't share the cache store.

3. **Per-locale vs locale-agnostic — decide by what the page renders:**
   - A tag is **per-locale** (`x_${slug}_${locale}`) ONLY when the page's entire rendered payload is localized. The fetcher MUST then include `locale` in its `unstable_cache` keyParts, and the hook busts only the edited locale (`req.locale`).
   - A tag is **locale-agnostic** (`x_${slug}`, one tag attached to every per-locale cache entry) when the page renders ANY shared / non-localized field — editing it in one locale changes all locales, so one tag busts them all.
   - If unsure, default to **locale-agnostic** — under-invalidating a shared field is a silent stale-content bug; over-invalidating only costs a rebuild.

4. **Every cached collection needs a revalidation hook.** A collection read on the front end with no `afterChange`/`afterDelete` hook = cache that never busts until TTL/redeploy. Add hooks that bust the collection's tag(s). Gate on `context.disableRevalidate`; gate on `_status === 'published'` only if the collection has drafts. (See the `payload-revalidation-hook-required` rule.)

5. **Embedded relationships bust their parents.** When a related doc is rendered inside a cached parent (page or global), attach the relationship's tag to that parent's cache too, so editing the related doc busts the parent. Verify against ACTUAL usage — only attach where the field is really rendered; asymmetry between collections is usually intentional, not a bug.

6. **Keep the contract test in sync.** If the project has a test asserting the `cacheTags` string contract, update it when you add or change a builder.

## Examples

```ts
// BAD — hardcoded string, drifts from the hook; locale in keyParts but not in tag by accident
unstable_cache(fn, ['models', slug, locale], { tags: [`models_${slug}`] })

// GOOD — built through cacheTags; page renders shared fields, so the tag is locale-agnostic
unstable_cache(fn, ['models', slug, locale], { tags: [cacheTags.model(slug)] })

// GOOD — fully localized page, so per-locale (locale is in keyParts AND the tag)
unstable_cache(fn, ['configurator', slug, locale], { tags: [cacheTags.configurator(slug, locale)] })
```

```ts
// Hook side — same cacheTags entry, direct revalidateTag, correct locale scope
revalidateTag(cacheTags.model(doc.slug), 'max')                        // locale-agnostic: one call
for (const code of locales) revalidateTag(cacheTags.configurator(doc.slug, code), 'max') // per-locale
```

## Completion checklist

- [ ] Tag built via a `cacheTags` builder, never a hardcoded string
- [ ] The same `cacheTags` entry referenced on producer (fetch `tags`) and consumer (hook `revalidateTag`)
- [ ] Locale scope chosen by what the page renders (locale in `unstable_cache` keyParts iff the tag is per-locale)
- [ ] Every front-end-read collection/global has an `afterChange`/`afterDelete` hook gated on `context.disableRevalidate`
- [ ] `cacheTags` contract test updated if a builder changed

## When NOT to use

- The change doesn't touch a cached fetch, a `tags` array, or a revalidation hook.
- Editing admin-only config, labels, or validation with no front-end cache impact.
- Non-cached / always-dynamic routes (`force-dynamic`, no `unstable_cache`).
