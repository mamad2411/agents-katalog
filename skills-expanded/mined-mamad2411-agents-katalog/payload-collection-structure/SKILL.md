---
name: payload-collection-structure
description: Public Payload 3 collections follow a consistent shape — tracking fields, Content/SEO tabs, drafts with scheduled publish, and a slug field.
---

# Payload collection structure

Give every public-facing collection (rendered on the front end) the same skeleton. Targets Payload 3 (Next-native, Lexical, Drizzle/Postgres).

Why: divergent shapes force editors and consuming code to special-case each collection, and a missing piece (versions, tracking fields, revalidation) ships as a latent data-loss or stale-content bug.

## Rules

- **Tracking fields:** include `createdBy` / `updatedBy` (relationship to users, populated via hooks) and a `publishedAt` date. Don't hand-roll these per collection — share them via a field builder ([`payload-field-builder-pattern`](payload-field-builder-pattern)).
- **Tabs:** organise fields into a **Content** tab and an **SEO** tab (the latter from the SEO plugin) rather than a flat field list.
- **Versions + drafts:** enable `versions: { drafts: { schedulePublish: true }, maxPerDoc: 50 }` for editorial collections so content can be drafted, scheduled, and rolled back without unbounded row growth.
- **Slug:** use the shared `slugField()` builder for the URL identifier — consistent validation, formatting, and `dbName`.
- **Revalidation:** any collection read on the front end needs revalidation hooks — see [`payload-revalidation-hook-required`](payload-revalidation-hook-required).

## Examples

```ts
// BAD — flat field list, no tabs, hand-rolled slug, no versions, no revalidation hooks
export const Pages: CollectionConfig = {
  slug: 'pages',
  fields: [
    { name: 'slug', type: 'text' }, // duplicated validation/format per collection
    { name: 'title', type: 'text' },
    { name: 'metaTitle', type: 'text' }, // SEO mixed into content, no tab grouping
  ],
  // no versions/drafts, no createdBy/updatedBy/publishedAt, no afterChange/afterDelete → stale cache
}

// GOOD — shared builders, Content/SEO tabs, drafts + scheduled publish, revalidation hooks
export const Pages: CollectionConfig = {
  slug: 'pages',
  access: { read: anyone, update: or(superAdminAccess, marketEditorAccess) },
  versions: { drafts: { schedulePublish: true }, maxPerDoc: 50 },
  fields: [
    ...slugField(),
    { type: 'tabs', tabs: [
      { label: 'Content', fields: [ /* ... */ ] },
      { label: 'SEO', fields: [ /* seo plugin fields */ ] },
    ] },
    ...trackingFields(), // createdBy / updatedBy / publishedAt
  ],
  hooks: { afterChange: [revalidatePage], afterDelete: [revalidatePage] },
}
```

## When NOT to apply

- Internal / admin-only collections never rendered on the front end (no SEO tab, no revalidation, drafts optional).
- Join/relationship-only collections with no editorial content.
