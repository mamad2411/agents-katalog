---
name: typescript-conventions
description: TypeScript conventions — strict: true, never any, discriminated unions over optional fields, Result types over throw, satisfies over as, as const over enum. Use when writing or reviewing TypeScript.
license: MIT
---

# TypeScript conventions

## Types

- strict: true always
- Never any — use unknown and narrow
- Discriminated unions over optional fields
- Type-only imports
- Result types over throw for handleable failures

## Patterns

- `as const` over `enum`
- `satisfies` over `as`
- `readonly` for immutables
- Brand types for IDs

## Async

- async/await over .then
- Handle rejections
- Promise.all parallel, allSettled partial success

## Banned

- any
- @ts-ignore (use @ts-expect-error)
- Unsafe `as` where `satisfies` works
- Mutating params
- enum (use union + as const)
- Silent catch

## Tsconfig extras

- noUncheckedIndexedAccess
- noImplicitOverride
- exactOptionalPropertyTypes

---

Full content + 15 worked examples at https://github.com/HermeticOrmus/typescript-conventions-skills.
