---
name: payload-field-builder-pattern
description: Share Payload fields through builder functions that accept { overrides } and deep-merge onto a base config — never copy-paste field definitions.
---

# Payload field-builder pattern

Reusable fields (links, media frames, pricing, SEO groups) live behind **builder functions**, not duplicated inline. This keeps a field's shape defined once and adjustable at each call site.

Why: copy-pasted field definitions drift apart — a fix or `dbName` change lands in one copy and not the others, producing inconsistent schemas and migrations.

## Rules

- A shared field is exported as a **function** (`link()`, `productFrame()`, `titleFrame()`) that returns a `Field` (or `Field[]`), not a bare object.
- The builder accepts an **`{ overrides }`** argument and merges it onto the base with `deepMerge(base, overrides)` so callers can tweak `label`, `admin`, `required`, `name`, etc. without forking the field.
- Keep the base config inside the builder; never copy a field's full definition into a collection just to change one prop — pass an override instead.
- When a builder sets `dbName`, follow [`payload-dbname-snake-case`](payload-dbname-snake-case).
- Builders compose: a higher-level builder may call lower-level ones and merge their results.

## Examples

```ts
// BAD — the link field copy-pasted and hand-edited in every collection
{ name: 'cta', type: 'group', fields: [ /* 30 lines duplicated */ ] }

// GOOD — one builder, overridden per call site
export const link = ({ overrides = {} }: { overrides?: Partial<GroupField> } = {}): Field =>
  deepMerge(
    { name: 'link', type: 'group', dbName: 'link', fields: [ /* base */ ] },
    overrides,
  )

// call site
link({ overrides: { name: 'cta', label: 'Call to action' } })
```

## When NOT to apply

- A genuinely one-off field used in a single place with no reuse.
- Generated fields produced by a plugin (don't wrap plugin output in a builder).
