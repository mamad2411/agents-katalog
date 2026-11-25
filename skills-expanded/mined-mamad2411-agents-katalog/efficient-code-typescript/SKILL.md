---
name: efficient-code-typescript
description: Applies when writing or reviewing TypeScript code. Extends the core efficient-code principles with TypeScript-specific rules around type erasure, const enum vs enum emit cost, decorator overhead, tsc target impact, and the JS runtime gotchas that all TS code inherits.
---

# Efficient Code — TypeScript

This skill assumes you also have the core `efficient-code` skill active **and** the `efficient-code-javascript` skill active — every JS runtime gotcha applies to TS at runtime because TS compiles to JS. This skill adds the TS-specific rules.

## What TS actually gives you (and doesn't) at runtime

- **TypeScript adds no runtime containers.** `Map<K,V>`, `Set<T>`, `Array<T>` are JS built-ins with TS type definitions on top.
- **`ReadonlyArray<T>` / `readonly T[]`** — **type-level only**. No runtime immutability. Runtime code can still mutate the underlying array.
- **`Record<K, V>`** — type alias for `{[k: K]: V}`, no runtime cost.
- **`as const`** — type-level narrowing, erased.
- **`satisfies`** — compile-time constraint check, erased.
- **`const enum`** — inlined at compile time, emits NO runtime object.
- **`enum`** (non-const) — emits a runtime object with forward **and** reverse mapping; heavier than a plain `const` object with `as const`.

## TypeScript-specific gotchas

1. **Types erase at runtime.** `interface`, `type`, generic parameters, `satisfies`, `as`, return types — all gone after compilation. No reflection on types; no `instanceof MyInterface`.
2. **`readonly` is a type-level annotation, not `Object.freeze`.** The field can still be reassigned from code the compiler doesn't type-check (JS interop, `any`, dynamic imports).
3. **`private` / `protected` modifiers are type-level only** (unlike JS `#private` class fields, which are enforced at runtime and produce more stable hidden classes). Prefer ES `#private` fields when you want real encapsulation and better shape stability.
4. **Decorators (legacy `experimentalDecorators` or TC39 stage-3) wrap functions/classes at runtime.** They add indirection and can break inlining. Measure before using on hot methods.
5. **Numeric `enum` emits bidirectional mapping; string `enum` emits only forward mapping.** If you don't need reverse lookups, use a string `enum` or a `const` object.
6. **`const enum` is unsafe across module boundaries under `isolatedModules`** (required by Babel, esbuild, swc) — use `as const` object literals instead.
7. **Parameter property shorthand** `constructor(public x: number)` emits a field assignment — same cost as manual.
8. **`tsc` target matters.** Targeting `ES5` transpiles classes to function/prototype chains and `async` to state machines with regenerator-runtime — heavy. Target `ES2020+` when you can.
9. **`useDefineForClassFields: true`** emits standards-compliant field definitions (`Object.defineProperty`); `false` emits constructor assignments. The former is slightly slower on V8 due to `defineProperty` semantics but required for decorators.
10. **`import type { X } from '...'`** is fully erased. Use it to avoid retaining modules at runtime.
11. **`namespace` with nested exports emits IIFEs** — prefer ES modules.
12. **tsc's emit of `?.` and `??` expands to nested ternaries on older targets.** Readable source, larger compiled output.
13. **TypeScript does NOT improve runtime performance.** It improves your ability to reason about the code; the JS VM sees only the emitted output.
14. **All JS runtime gotchas apply** — hidden classes, monomorphic call sites, holey arrays, `forEach` vs `for`. See the `efficient-code-javascript` skill.

## Profiling

Runtime: same tools as JavaScript — Chrome DevTools Performance panel, `node --prof`.

Compile-time: `tsc --extendedDiagnostics` and `tsc --generateTrace` for understanding slow type-checks.

## Sources

- https://www.typescriptlang.org/docs/handbook/
- https://www.typescriptlang.org/docs/handbook/enums.html
- https://github.com/microsoft/TypeScript/wiki/Performance
- https://www.typescriptlang.org/tsconfig
- https://v8.dev/blog/fast-properties
