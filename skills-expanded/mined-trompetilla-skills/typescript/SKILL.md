---
name: TypeScript
description: Avoid common TypeScript mistakes — any leaks, inference failures, and type narrowing traps.
metadata: {"clawdbot":{"emoji":"🔷","requires":{"bins":["tsc"]},"os":["linux","darwin","win32"]}}
---

## Stop Using `any`
- `unknown` forces you to narrow before use — `any` silently breaks type safety
- API responses: type them or use `unknown`, never `any`
- When you don't know the type, that's `unknown`, not `any`

## Narrowing Failures
- `filter(Boolean)` doesn't narrow — use `.filter((x): x is T => Boolean(x))`
- `Object.keys(obj)` returns `string[]`, not `keyof typeof obj` — intentional, objects can have extra keys
- `Array.isArray()` narrows to `any[]` — may need assertion for element type
- `in` operator narrows but only if property is in exactly one branch of union

## Literal Type Traps
- `let x = "hello"` is `string` — use `const` or `as const` for literal type
- Object properties widen: `{ status: "ok" }` has `status: string` — use `as const` or type annotation
- Function return types widen — annotate explicitly for literal returns

## Inference Limits
- Callbacks lose inference in some array methods — annotate parameter when TS guesses wrong
- Generic functions need usage to infer — `fn<T>()` can't infer, pass a value or annotate
- Nested generics often fail — break into steps with explicit types

## Discriminated Unions
- Add a literal `type` or `kind` field to each variant — enables exhaustive switch
- Exhaustive check: `default: const _never: never = x` — compile error if case missed
- Don't mix discriminated with optional properties — breaks narrowing

## `satisfies` vs Type Annotation
- `const x: Type = val` widens to Type — loses literal info
- `const x = val satisfies Type` keeps literal, checks compatibility — prefer for config objects

## Strict Null Gotchas
- Optional chaining `?.` returns `undefined`, not `null` — matters for APIs expecting `null`
- `??` only catches `null`/`undefined` — `||` catches all falsy including `0` and `""`
- Non-null `!` should be last resort — prefer narrowing or early return

## Module Boundaries
- `import type` for type-only imports — stripped at runtime, avoids bundler issues
- Re-exporting types: `export type { X }` — prevents accidental runtime dependency
- `.d.ts` augmentation: use `declare module` with exact module path
