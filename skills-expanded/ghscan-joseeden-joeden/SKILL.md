---
name: clean-typescript
description: Use this skill when writing, reviewing, or refactoring TypeScript. Focuses on clear types, safe narrowing, practical inference, maintainable APIs, explicit null handling, typed errors, and avoiding clever or unsafe type patterns.
---

# Clean TypeScript

Use TypeScript to make code easier to understand and harder to misuse. Types should clarify intent and catch real mistakes without adding unnecessary ceremony.

## Type Philosophy

- Prefer readable types that explain the domain.
- Let TypeScript infer obvious local values.
- Add explicit types at module boundaries, public functions, exported components, API inputs/outputs, and complex return values.
- Avoid clever generic types unless they remove real duplication or protect an important contract.
- Keep type definitions close to the code they describe unless they are shared across modules.

## Avoid Unsafe Escape Hatches

- Avoid `any`.
- Use `unknown` when the value is genuinely not known yet, then narrow it before use.
- Avoid broad type assertions such as `as SomeType` unless there is no better way to prove the type.
- Treat non-null assertions (`!`) as a last resort.
- Prefer runtime validation for data from users, APIs, files, environment variables, or storage.

## Types and Interfaces

- Prefer `type` aliases for unions, utility types, function shapes, and most local object shapes.
- Use `interface` when a public object shape is intentionally extendable or declaration merging is useful.
- Keep types small, named, and composable.
- Name types by the concept they represent, not by implementation details.
- Avoid giant shared type buckets that make ownership unclear.

## Functions and APIs

- Give exported functions explicit return types.
- Keep function parameters simple and predictable.
- Use object parameters when a function has several related options.
- Avoid overloads unless they make a real public API easier to use.
- Prefer discriminated unions for APIs with different modes or states.

```ts
type SaveResult =
  | { ok: true; id: string }
  | { ok: false; reason: "unauthorized" | "invalid-input" };
```

## Nullability and Narrowing

- Handle `null` and `undefined` deliberately.
- Use control-flow narrowing, guards, and early returns.
- Prefer optional fields only when the value can truly be absent.
- Do not hide uncertain data behind non-null assertions.

```ts
if (!user) {
  return null;
}

return user.email;
```

## Constants and Unions

- Avoid `enum` for most application code.
- Prefer literal unions or `as const` objects when they are enough.
- Keep runtime output simple and predictable.

```ts
const NOTE_VISIBILITY = {
  Private: "private",
  Public: "public",
} as const;

type NoteVisibility =
  (typeof NOTE_VISIBILITY)[keyof typeof NOTE_VISIBILITY];
```

## Error and Result Shapes

- Model expected failure states explicitly.
- Use result objects or discriminated unions when callers are expected to handle failure.
- Throw for truly exceptional situations or when the surrounding framework expects thrown errors.
- Do not use vague return types that hide failure modes.

## Working With External Data

- Do not trust external data just because it has a TypeScript type.
- Parse or validate untrusted input at the boundary.
- Convert raw API/database/env data into application-friendly shapes early.
- Keep boundary types separate from internal domain types when they differ.

## Generics and Utilities

- Use generics when the caller and return type need to stay linked.
- Give generic parameters meaningful names when there is more than one.
- Avoid deeply nested conditional or mapped types unless they are isolated and documented.
- Prefer a small explicit type over an impressive type puzzle.

## Review Checklist

Before finishing:

- Are public boundaries typed clearly?
- Is `any` avoided or justified?
- Are assertions and non-null assertions rare?
- Are nullable values handled directly?
- Are errors and empty states represented honestly?
- Are generic or utility types understandable?
- Would a future maintainer know what each type means?
