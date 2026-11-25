---
name: follow-lang-typescript
description: Develop TypeScript projects with maximum type safety and code quality best practices
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-javascript
  - follow-best-practice
  - setup-cicd
  - use-scripts
  - run-typecheck
  - run-test
  - run-lint
  - run-format
  - no-use-ignore
  - improve
  - deep-research
  - follow-lib-tstyche
---

## Goal

Develop TypeScript projects with maximum type safety and code quality best practices

## Scope

For TypeScript projects — type system, code quality, testing, documentation. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time strict scaffold); verify the current TypeScript version/behavior via `/deep-research` at use time (the native-compiler era changed defaults; check breaking changes per release, official docs: https://www.typescriptlang.org/docs/)

## Execute

### 1. Check Version And Setup Type System

> Goal: configure strict TypeScript for maximum type safety with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest stable TypeScript, its default compiler behaviors, current TS practices, removed options, and programmatic-API status before configuring or coding; tool inventory → `references/toolchain.md`
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): runtime pin, strict tsconfig, quality dev deps, verify
3. Enable `strict: true` plus the enhanced checks in `tsconfig.json`: `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noUnusedLocals`, `noUnusedParameters`, `noImplicitReturns`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`, `isolatedModules`, `noUncheckedSideEffectImports`
4. Use type narrowing (`typeof`, type guards `value is T`) instead of type assertions (`as`); discriminated unions for complex state
5. Never use `any` — use `unknown` and narrow before use; mark immutable properties `readonly`
6. Use utility types (`Partial`, `Pick`, `Omit`, `Awaited`, `Parameters`, `ReturnType`), `satisfies` to validate without widening, and exhaustive switch with `never`

### 2. Use Modern Type Features

> Goal: use the type system's expressiveness where it earns its keep

1. Use `as const` and branded types for domain-specific values
2. Use template literal types and conditional types for type logic
3. Use `infer` and mapped types for type transformations
4. Use `keyof` and `typeof` operators for type queries
5. Keep advanced types readable — prefer a simple interface over clever type gymnastics

### 3. Setup Code Quality

> Goal: enforce conventions for maintainable code

1. Annotate function return types; use `const` over `let`
2. Use named exports (tree-shaking) and `import type` for type-only imports (enforced by `verbatimModuleSyntax`)
3. Use `interface` for extensible object shapes, `type` for unions/tuples/complex types
4. Use `===`, template literals, destructuring, and generic constraints (`K extends keyof T`)
5. Run the linter/formatter via `/run-lint`/`/run-format`; Biome or ESLint per project config

### 4. Setup Testing

> Goal: type-safe testing with vitest and type coverage

1. Use `vitest` for unit testing; type-safe mocks with `vi.fn()`/`vi.spyOn()`
2. Assert types with `expect-type` (`expectTypeOf(add(1, 2)).toEqualTypeOf<number>()`) in runtime suites; for a dedicated type-test layer (public API type contracts, multi-TypeScript-version targets) use `tstyche` per `/follow-lib-tstyche`
3. Check type coverage with `type-coverage` (`npx type-coverage --detail`) — target: no `any` in the codebase
4. Run `/run-test` and `/run-typecheck` until green

### 5. Setup Documentation

> Goal: document public API with JSDoc/TSDoc

1. Use `/** */` JSDoc/TSDoc on public functions with `@param`, `@returns`, `@example`
2. Use `@remarks` for notes and `@deprecated` (with migration hint) for deprecated APIs

## Rules

### 1. Type System

- `strict: true` plus the enhanced checks listed above; never suppress with `any` or `@ts-ignore` — fix the type (see `/no-use-ignore`)
- Narrow, don't assert; `satisfies` over casting; exhaustive switch with `never`

### 2. Code Quality

- Return-type annotations, `const`, named exports, `import type`, `interface` vs `type` per shape complexity
- `===` only, template literals, generic constraints for reusable code

### 3. No Stale Pins

- Do not pin TypeScript versions or compiler defaults from memory in code or docs; `references/toolchain.md` holds roles/commands only — live-check via `/deep-research` at use time

- Use /follow-lang-javascript if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed
- Use /run-typecheck if needed
- Use /improve typesafe if needed

## Expected Outcome

- Maximum type safety via strict mode and enhanced compiler options
- Modern type features used where they add real safety
- Consistent code quality per best practices
- Type-safe tests with `expect-type`/`tstyche` (`/follow-lib-tstyche`) and full type coverage
- Complete JSDoc/TSDoc on public APIs
