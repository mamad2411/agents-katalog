---
name: zod-dynamic-schema-type-inference
description: |
  Fix TypeScript type inference loss when dynamically constructing Zod object schemas.
  Use when: (1) `z.infer<typeof schema>` produces `Record<string, unknown>` instead of
  typed fields, (2) Building a schema factory that constructs `z.object()` from dynamic
  field maps, (3) Component props typed from Zod schema show 'unknown' for all fields,
  (4) Type error "'data.fieldName' is of type 'unknown'" after refactoring schemas to
  use a factory pattern. Covers Zod 3 and Zod 4.
author: Claude Code
version: 1.0.0
date: 2026-03-02
---

# Zod Dynamic Schema Construction Type Inference Loss

## Problem

When building a Zod schema factory that dynamically constructs `z.object()` from a
`Record<string, z.ZodType>`, TypeScript's `z.infer<>` produces `Record<string, unknown>`
instead of properly-typed fields. This breaks all downstream type usage — components,
server actions, and form handlers that depend on typed schema inference get `unknown`
for every field.

## Context / Trigger Conditions

- Building a schema factory or helper that returns `z.ZodObject<Record<string, z.ZodType>>`
- Type error: `'data.fieldName' is of type 'unknown'`
- `z.infer<typeof generatedSchema>` resolves to `Record<string, unknown>` in IDE hover
- Refactoring hand-written Zod schemas to use a centralized factory/generator
- Using ORM metadata (Prisma, ZenStack, Drizzle) to auto-generate Zod schemas at runtime

## Root Cause

`z.object()` accepts `Record<string, z.ZodType>` at runtime, but TypeScript needs the
**literal object type** of the shape parameter to infer field types. When the shape is
typed as `Record<string, z.ZodType>`, TypeScript only knows the values are "some Zod type"
— it cannot narrow to `ZodString`, `ZodNumber`, `ZodUUID`, etc. per field.

```typescript
// BAD: Returns z.ZodObject<Record<string, z.ZodType>>
// z.infer<> produces Record<string, unknown>
function makeModelSchema(fields: Record<string, z.ZodType>) {
  return z.object(fields);
}

const schema = makeModelSchema({
  name: z.string(),
  age: z.number(),
});
type T = z.infer<typeof schema>; // { [x: string]: unknown } — BROKEN
```

## Solution: Per-Field Typed Helpers

Instead of building the whole object schema dynamically, export **typed helper functions**
that return concrete Zod types. Each consumer file constructs `z.object({})` explicitly
with these helpers, preserving the literal type that TypeScript needs.

```typescript
// factory.ts — export per-field typed helpers
export function fk(label: string): z.ZodUUID {
  return z.uuid(`Invalid ${label} ID`);
}

export function str(model: string, field: string): z.ZodString {
  // Read constraints from metadata (ORM schema, config, etc.)
  const constraints = getFieldConstraints(model, field);
  let s = z.string().trim();
  if (constraints.minLength) s = s.min(constraints.minLength);
  if (constraints.maxLength) s = s.max(constraints.maxLength);
  return s;
}

export function int(model: string, field: string): z.ZodNumber {
  const constraints = getFieldConstraints(model, field);
  let n = z.number().int();
  if (constraints.gte !== undefined) n = n.gte(constraints.gte);
  if (constraints.lte !== undefined) n = n.lte(constraints.lte);
  return n;
}
```

```typescript
// user.ts — explicit z.object() preserves type inference
import { fk, str, int } from "./factory";

export const userSchema = z.object({
  name: str("User", "name"),       // TypeScript sees z.ZodString
  email: str("User", "email"),     // TypeScript sees z.ZodString
  age: int("User", "age"),         // TypeScript sees z.ZodNumber
  teamId: fk("team"),              // TypeScript sees z.ZodUUID
});

type User = z.infer<typeof userSchema>;
// { name: string; email: string; age: number; teamId: string } — CORRECT
```

### Why This Works

- Each helper has a **concrete return type** (`z.ZodString`, `z.ZodNumber`, `z.ZodUUID`)
- The `z.object({})` call sees the literal shape `{ name: z.ZodString, email: z.ZodString, ... }`
- TypeScript can infer each field type precisely
- Runtime behavior is identical — constraints are still read from metadata

### Alternative: Generic Function with Type Parameter

If you must return a whole schema from a function, use a generic type parameter:

```typescript
function makeSchema<T extends z.ZodRawShape>(shape: T) {
  return z.object(shape);
}

// Caller must pass a literal object — NOT a variable typed as Record
const schema = makeSchema({
  name: z.string(),
  age: z.number(),
});
// Works because TypeScript infers T as { name: z.ZodString, age: z.ZodNumber }
```

**Limitation**: This only works when the shape is a literal at the call site. If you're
building the shape dynamically from metadata, the type information is lost before the
call — which is why per-field helpers are the robust solution.

## Verification

After applying the fix:
1. Hover over `z.infer<typeof schema>` in your IDE — should show named fields, not `Record`
2. Run `tsc --noEmit` — no "'unknown'" type errors on schema-derived data
3. Components using `z.infer<typeof schema>` as props should compile without casts

## Notes

- This applies to both Zod 3 and Zod 4 — the type inference mechanism is the same
- The per-field helper pattern also works well with `.omit()`, `.pick()`, `.partial()`,
  `.extend()` — all composition methods preserve the inferred types
- If using an ORM schema factory (e.g., `@zenstackhq/zod`, Drizzle-Zod), test that
  `z.infer<>` produces typed fields before adopting it — some generate `Record<string, unknown>`
- Custom validators from shared modules (e.g., `monetaryAmountSchema`, `ukPostcodeSchema`)
  can be mixed freely with factory helpers since they have concrete return types
