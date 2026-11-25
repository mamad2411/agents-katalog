---
name: i18n-payload-localized-fields
description: In Payload, set localized:true only on display content; never on slugs, dbNames, relation IDs, or enums. Configure a fallbackLocale so empty translations degrade instead of rendering blank.
---

# Payload localized-field discipline

`localized: true` on the wrong field is expensive to undo: slugs become per-locale (breaking routing and links), relationship IDs fork per locale (breaking joins), and enums fragment. Localize what humans read, nothing that addresses or relates a document.

## Rules

- Localize **display content** only: titles, body/rich text, labels, alt text, SEO copy.
- **Never** set `localized: true` on: `slug`/URL fields, `dbName` values, relationship/upload IDs, enum/`select` values used as logic keys, or fields that feed a unique constraint.
- Set a project-wide `localization.fallbackLocale` (and `fallback: true` on reads) so a missing translation falls back to the default locale instead of rendering empty.
- Keep the collection's `locales` list sourced from the same locale set as next-intl routing — a locale that routes but isn't a Payload locale produces pages with no content.
- A slug that genuinely must differ per locale belongs in a typed next-intl `pathnames` map, not a `localized: true` slug field.

## Examples

```ts
// BAD — slug and a logic-key select are localized: routing forks per locale and
// `status === 'published'` checks break in non-default locales
{ name: 'slug', type: 'text', localized: true, unique: true }
{ name: 'status', type: 'select', options: ['draft', 'published'], localized: true }

// GOOD — only human-readable content is localized; slug and logic keys stay shared
{ name: 'slug', type: 'text', unique: true }                         // shared, addresses the doc
{ name: 'status', type: 'select', options: ['draft', 'published'] } // shared, drives logic
{ name: 'title', type: 'text', localized: true }                     // display content
{ name: 'body', type: 'richText', localized: true }                  // display content

// payload.config.ts — fallback so empty translations degrade, not render blank
localization: { locales: ['en-GB', 'de-DE', 'fr-FR'], defaultLocale: 'en-GB', fallback: true }
```

## Gotchas

- Toggling `localized` on an existing field is a data migration — Payload moves values into/out of the per-locale structure; never flip it casually on populated collections.
- `fallbackLocale` hides missing translations on the front end, so absent content won't surface in QA — track translation coverage separately rather than relying on the fallback to catch gaps.
