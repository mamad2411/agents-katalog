---
name: typescript-hero
description: Elite TypeScript rigor for writing, reviewing, refactoring, or migrating any .ts/.tsx/.mts/.cts code. Enforces a ZERO-`any` policy, maximally-strict tsconfig, modern TS 5.x idioms (`satisfies`, `const` type params, `NoInfer`, `using`, `isolatedDeclarations`), and production-grade patterns (branded types, parse-don't-validate with Zod/Valibot/ArkType, `Result<T,E>`, exhaustive `never`, type-level state machines). Use whenever TypeScript code is involved or the user mentions types, tsconfig, generics, type-safety, "TS error", Zod, Valibot, tRPC, Effect, or migrating JS→TS.
---

# TypeScript Hero

Type-system rigor at staff-engineer level. Treat types as a correctness tool, not decoration. Runtime bugs catchable at compile time are a process failure.

## Non-negotiable rules

1. **No `any`.** Not in signatures, generics, casts, `@ts-ignore`, ambient declarations, or "temporarily". Use `unknown` and narrow. See `references/no-any-playbook.md` for all 16 replacement scenarios.
2. **Parse, don't validate.** Every external data boundary (HTTP, `JSON.parse`, `localStorage`, env vars, form input, LLM output, IPC) crosses through a schema parser (Zod/Valibot/ArkType). No casting past the boundary. See `references/runtime-safety.md`.
3. **Make illegal states unrepresentable.** Discriminated unions with literal tags + branded types. If your type allows a state you check at runtime, the type is wrong.
4. **Total > partial functions.** Expected failures return `Result<T, E>` or a discriminated union. `throw` is reserved for invariant violations (bugs), not control flow. See `references/error-handling.md`.
5. **Immutable by default.** `readonly` on every property, `readonly T[]` on array inputs, `as const` on literal data.
6. **Infer internally, annotate at boundaries.** Public/exported surface is fully annotated (return type included). Internal code lets TS infer.
7. **Every `as` is a lie** unless post-parser or post-type-guard. Treat like `eval`: rare, commented, reviewed.

## Workflow — when invoked

### Step 1 — Inspect (read-only)

```bash
npx tsc --version && node -v
npx tsc --showConfig | head -120
ls -1 pnpm-workspace.yaml turbo.json nx.json lerna.json 2>/dev/null
node -e 'const p=require("./package.json");const d={...p.dependencies,...p.devDependencies};for (const k of ["zod","valibot","arktype","effect","ts-pattern","@total-typescript/ts-reset","neverthrow"]) if (d[k]) console.log(k,d[k])' 2>/dev/null
```

Adapt to what exists. Don't impose Zod if the project uses Valibot. Don't restructure into a monorepo to fix a type error.

### Step 2 — Audit tsconfig

Verify these flags before touching code. Missing or `false` → fix first.

- `"strict": true`
- `"noUncheckedIndexedAccess": true`
- `"exactOptionalPropertyTypes": true`
- `"noImplicitOverride": true`
- `"noFallthroughCasesInSwitch": true`
- `"noPropertyAccessFromIndexSignature": true`
- `"verbatimModuleSyntax": true`
- `"isolatedModules": true` (and `"isolatedDeclarations": true` for libraries)
- `"skipLibCheck": true`

Full baseline config, flag-by-flag rationale, monorepo setup, and lint rules in `references/strict-tsconfig.md`.

### Step 3 — Route to the right reference

Pick the references to load based on what the task needs. Do not load everything.

| Task | Load |
|---|---|
| Any `any` appears, or replacing one | `references/no-any-playbook.md` |
| tsconfig setup, monorepo, lint rules | `references/strict-tsconfig.md` |
| `satisfies`, `NoInfer`, `using`, `isolatedDeclarations`, variance, `ts-reset` | `references/modern-features.md` |
| Branded/phantom types, discriminated unions, state machines, template literals, HKT, enums, utility types | `references/advanced-patterns.md` |
| External data entering the system (HTTP/env/LLM/form/storage) | `references/runtime-safety.md` |
| Error handling, `Result`, typed errors, async pitfalls | `references/error-handling.md` |
| Designing a library API, event emitter, HTTP client, builder, DI, route registry | `references/api-design.md` |
| Non-trivial generics or DSLs | `references/testing-types.md` |
| Slow `tsc`, large monorepo, IDE lag | `references/performance.md` |
| Reviewing a PR | `references/code-review-checklist.md` |

### Step 4 — Validate

```bash
npx tsc --noEmit
npx vitest run --typecheck --run 2>/dev/null || true
npm run -s lint 2>/dev/null || npx biome check . 2>/dev/null || npx eslint . 2>/dev/null
```

A change is not done until `tsc --noEmit` passes at zero errors on the project's actual tsconfig — not a relaxed one.

## `any` shortcut table

Before opening `no-any-playbook.md`, try the quick map:

| Situation | Wrong | Right |
|---|---|---|
| Unknown shape | `any` | `unknown` + narrow (type guard or Zod) |
| Arbitrary function | `(...args: any[]) => any` | `(...args: readonly unknown[]) => unknown` |
| Arbitrary object | `any` / `object` / `{}` | `Record<string, unknown>` or concrete interface |
| `JSON.parse` output | `JSON.parse(s) as Foo` | `FooSchema.parse(JSON.parse(s))` |
| Untyped third-party | `declare module "x"` with `any` | narrow `.d.ts` with `unknown` + used methods |
| Generic constraint | `<T extends any>` | `<T>` (no constraint) |
| React event | `(e: any) => …` | `React.ChangeEvent<HTMLInputElement>` |
| `catch` clause | `catch (e: any)` | `catch (e: unknown)` then narrow |
| Incompatible bridge | `as any` | `as unknown as T` (commented boundary) |

`unknown` is the universal safe replacement — it forces narrowing.

## Anti-patterns — reject on sight

- `any` in any form.
- `// @ts-ignore` without `// @ts-expect-error` + description + expiry.
- `as` that widens or crosses unrelated types without going through `unknown`.
- `Function` — use a specific signature.
- `Object` / `{}` as "any object" — `{}` means "anything except null/undefined".
- `enum` — use `as const` object + literal union.
- `namespace X {}` — use modules.
- Optional `x?: T` when you mean `x: T | undefined` (they differ under `exactOptionalPropertyTypes`).
- `throw` in a function whose signature doesn't acknowledge failure.
- Deep barrel files re-exporting hundreds of symbols.
- Return-type annotations on every internal function.

## Detect every `any` in a project

```bash
npx tsc --noEmit --noImplicitAny --strict
grep -rEn ':\s*any(\s|[,;\)\]>]|$)|<any>|as any|any\[\]|Record<[^,]+,\s*any>' --include='*.ts' --include='*.tsx' --include='*.mts' --include='*.cts' src/
```

## Communication

When correcting typed code, show the diff: current type → corrected type → the class of bug the corrected type now prevents that the old one missed. Never rewrite silently.

The goal is not TypeScript that compiles. The goal is TypeScript that makes the class of bug you just prevented **impossible for the next person on the codebase**.
