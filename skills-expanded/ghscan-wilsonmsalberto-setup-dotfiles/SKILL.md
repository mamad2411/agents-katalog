---
name: graphql-schema-guard
description: |
  GraphQL schema change guardian. Use AUTOMATICALLY when:
  - Modifying .graphql files
  - Changing type definitions
  - Adding/removing fields from types
  - Modifying resolvers that affect schema

  Prevents breaking changes and ensures schema consistency.
---

# GraphQL Schema Guard

## Purpose
Prevent breaking GraphQL schema changes that could affect clients.

## When This Triggers
- Any modification to `.graphql` files
- Changes to type definitions in TypeScript
- Resolver modifications that affect return types

## Checklist Before Schema Changes

### Breaking Changes to Avoid
- [ ] Removing fields from types
- [ ] Changing field types (e.g., `String` to `Int`)
- [ ] Removing types entirely
- [ ] Making nullable fields non-nullable
- [ ] Removing enum values
- [ ] Changing argument types

### Safe Changes
- Adding new fields (nullable by default)
- Adding new types
- Adding new enum values
- Deprecating fields (use `@deprecated`)
- Adding optional arguments

## Deprecation Pattern

```graphql
type User {
  id: ID!
  name: String!
  fullName: String! @deprecated(reason: "Use 'name' instead")
}
```

## Verification Steps

1. **Check schema diff**
   ```bash
   pnpm generate  # Regenerate schema
   git diff src/schema.graphql
   ```

2. **Review breaking changes**
   - Are any fields being removed?
   - Are any types changing?
   - Will existing queries still work?

3. **Consider client impact**
   - Optimus-web uses these types
   - Mobile apps may cache queries
   - Third-party integrations may exist

## Multi-Tenant Considerations

Different markets may have different data:
- `otomotopl` - Poland specific fields
- `autovitro` - Romania specific fields
- `carspt` - Portugal specific fields

Ensure schema changes work across all markets.

## Before Completing

- [ ] Schema regenerated (`pnpm generate`)
- [ ] No breaking changes OR deprecation plan in place
- [ ] Types are correctly nullable/non-nullable
- [ ] Documentation updated if needed
