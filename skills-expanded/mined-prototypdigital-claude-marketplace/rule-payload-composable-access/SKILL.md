---
name: payload-composable-access
description: Build Payload access control from named role-checker functions composed with or()/and() — never inline role checks in collection config.
---

# Payload composable access

Access control must read as a declarative composition of named, reusable checkers — not ad-hoc `req.user` inspection scattered across collections.

Why: inline role checks duplicate the same predicate across files, so they drift — one collection gets patched and another silently keeps the old, wrong rule, which is an authorization bug.

## Rules

- Define one **named `AccessFn` per role/condition** (`superAdminAccess`, `marketEditorAccess`, `authenticated`, `anyone`) in a shared access module. Each wraps a small role predicate; export them for reuse.
- Compose multiple conditions with **`or(...)` / `and(...)` combinators** over those named functions. The combinator returns an `AccessFn`, so it drops straight into `access: { read, create, update, delete }`.
- **Never inline** `req.user?.roles?.includes('...')` (or equivalent) directly in a collection/global/field `access` config. If a check is missing, add a named checker and compose it.
- Field-level access uses the same checkers via their `FieldAccess` variants — don't duplicate the role logic.
- Return a query constraint (`Where`) instead of a boolean when access is row-scoped (e.g. "only your market's docs"); compose those the same way.

## Examples

```ts
// BAD — inline role inspection, duplicated per collection, easy to drift
access: {
  update: ({ req: { user } }) => user?.roles?.includes('super-admin') || user?.roles?.includes('market-admin'),
}

// GOOD — named checkers composed with a combinator
access: {
  update: or(superAdminAccess, marketAdminAccess),
  delete: superAdminAccess,
}
```

## When NOT to apply

- Public, unauthenticated collections where `anyone` is the deliberate, single access function.
- One-off field `condition` UI logic (not access control).
