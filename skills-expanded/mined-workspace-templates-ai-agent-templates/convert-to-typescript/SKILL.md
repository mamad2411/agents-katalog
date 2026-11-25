---
name: convert-to-typescript
description: Converts a JavaScript file to TypeScript with real types and no any shortcuts, and keeps the build and tests passing.
disable-model-invocation: true
---

Convert to TypeScript: $ARGUMENTS

1. Read the target file and everything that imports it. Check `tsconfig.json` for `strict`, `allowJs` and path aliases, and follow the strictness already set.
2. Rename with `git mv` so history follows (`.js` to `.ts`, `.jsx` to `.tsx`).
3. Derive types from real usage: read call sites, tests and JSON shapes. Prefer `interface` or `type` for domain objects, union types for fixed options, generics for containers, and `unknown` plus narrowing for untrusted input.
4. Never write `any`, `as any` or `@ts-ignore`. Use `@ts-expect-error` with a reason only where a library type is wrong, and report each one.
5. Add types for dependencies from `@types/*` when missing, but ask before installing.
6. Fix real bugs the compiler exposes in a separate list, not silently.

Run `tsc --noEmit` and the tests. Report the new types, the remaining suppressions, and any bug found. Do not convert other files unless asked.
