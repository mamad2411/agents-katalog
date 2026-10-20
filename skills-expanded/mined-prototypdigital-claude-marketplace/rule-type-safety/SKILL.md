---
name: type-safety
description: Enforce strict type safety — no implicit any, no unguarded assertions.
---

# Type safety

**Why:** `any` and unchecked `as` assertions silence the compiler, letting type errors reach runtime as crashes the type system was meant to catch.

## Rules

- Never use `any`. Use `unknown` when the type is genuinely uncertain, then narrow.
- Avoid type assertions (`as`) unless you add a comment explaining why it's safe.
- Enable and respect `strict` mode in `tsconfig.json`.
- Prefer type guards (`typeof`, `instanceof`, discriminated unions) over assertions.
- Use `satisfies` for object literals when you want type checking without widening.

## Examples

```ts
// BAD
const data: any = fetchData();
const name = (response as User).name;

// GOOD
const data: unknown = fetchData();
if (isUser(data)) {
  const name = data.name;
}
```

`strict` mode and the no-`any` ban are deterministic invariants; enforce them with `tsconfig` `strict: true` and ESLint `@typescript-eslint/no-explicit-any` in CI rather than this prose alone.
