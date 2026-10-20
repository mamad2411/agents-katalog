---
name: follow-lib-zod-define-schemas
description: Zod schema design — objects, unions, discriminated unions, refinements, transforms, inference, composability
argument-hint: "[scope]"
related:
  - follow-lib-zod
  - run-typecheck
  - run-test
  - resolve-errors
---

## Goal

Write complete Zod schemas — primitives→complex types, refinements/transforms, type inference, schema composition patterns

## Scope

schema authoring — object/array/union/record/tuple schemas, `.refine`/`.superRefine`/`.transform`, `z.infer`, generics, recursive schemas, branded types

## Execute

### 1. Core Types

```ts
import { z } from 'zod'

const User = z.object({
  id: z.uuid(),                          // v4: top-level string formats
  email: z.email(),
  name: z.string().min(1).max(100),
  age: z.int().min(0).optional(),
  role: z.enum(['admin', 'user']),
  tags: z.array(z.string()).default([]),
  metadata: z.record(z.string(), z.unknown()),
  createdAt: z.iso.datetime(),           // iso string → validated
})

type User = z.infer<typeof User>         // derive TS type — single source
```

- v4: `z.uuid()`, `z.email()`, `z.url()`, `z.iso.datetime()` are top-level (faster than the `z.string().email()` chain)
- `z.literal`, `z.union`, `z.tuple`, `z.null`, `z.unknown`, `z.any`, `z.never`, `z.templateLiteral`

### 2. Unions And Discriminated

```ts
const Event = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('scroll'), y: z.number() }),
])
```

- `z.discriminatedUnion` — faster + better errors than `z.union` (requires a literal discriminator)
- `z.union` — the fallback when there is no discriminator field

### 3. Refinements And Transforms

```ts
const Password = z.string().min(8).regex(/[A-Z]/, 'needs uppercase')
  .refine(s => !s.includes('password'), 'too weak')

const DateCoerced = z.coerce.date()                          // string → Date
const Slug = z.string().transform(s => s.toLowerCase())
const Positive = z.number().check(z.positive())              // v4 check() API
```

- `.refine` sync checks; `.refine` async with an async fn; `.superRefine` multi-issue custom (v3) → v4 `.check()`
- `.transform` — the output type differs from the input (`z.input` vs `z.output` types)
- `.pipe()` — chain schemas post-parse (validate → transform pipeline)

### 4. Composition Patterns

- `.extend`, `.merge`, `.pick`, `.omit`, `.partial`, `.required`, `.deepPartial`
- Recursive: `const Node: z.ZodType<Node> = z.lazy(() => z.object({ children: z.array(Node) }))`
- Generic: `const Paginated = <T>(item: z.ZodType<T>) => z.object({ items: z.array(item), total: z.int() })`
- Branded: `z.string().brand<'UserId'>()` — nominal typing
- `.catch(default)` — fallback on invalid; `.readonly()` — freeze the output type

## Rules

- Derive types from the schema only: `z.infer`/`z.output` — never write a duplicate interface
- `discriminatedUnion` before `union` when a discriminator exists
- Keep `.transform` separate from `.refine` — refine=validate, transform=change value
- Schemas only at boundaries — internally trust the inferred types
- Prefer the v4 API — `z.uuid()` etc. top-level; `.check()` instead of some chained methods (check the v4 docs)

## Expected Outcome

- Schemas are composable, types derive via `z.infer`
- Unions/refinements/transforms use the right patterns
