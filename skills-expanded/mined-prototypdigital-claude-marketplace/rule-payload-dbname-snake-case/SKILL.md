---
name: payload-dbname-snake-case
description: Custom Payload `dbName` overrides must be snake_case — lowercase letters, digits, underscores only.
---

# Payload `dbName` snake_case

`dbName` controls the underlying Postgres column or table identifier. Keep every custom `dbName` snake_case so database identifiers stay consistent and predictable.

## Rules

- Write `dbName` as **snake_case only** — lowercase letters, digits, and underscores. No hyphens, camelCase, PascalCase, or spaces.
- When deriving `dbName` from a camelCase `name`, lowercase each word and join with `_` (`linkType` → `link_type`, `bgGradientColors` → `bg_gradient_colors`).
- Convert any kebab-case draft (`link-type`) to snake_case (`link_type`) before committing it.
- Keep it short — Postgres identifiers cap at 63 characters; abbreviate long group names (`pay_opts`, not `payment_options_configuration`).
- Never set a `dbName` containing `-`. If the field `name` is itself kebab-style, rename the `name` first, then derive `dbName`.

This is a mechanical, code-checkable invariant — best enforced by a lint rule or CI check on `dbName` literals, not relied on as prose alone.

## Examples

```ts
// BAD — kebab-case / camelCase
{ name: 'linkType', dbName: 'link-type' }
{ name: 'linkType', dbName: 'linkType' }

// GOOD — snake_case derived from the camelCase name
{ name: 'linkType', dbName: 'link_type' }
```

## When NOT to apply

- The value being edited is a `name`, `slug`, or admin-only string — not a database identifier.
- The change does not touch `dbName` (labels, admin UI props, hooks, validation).
