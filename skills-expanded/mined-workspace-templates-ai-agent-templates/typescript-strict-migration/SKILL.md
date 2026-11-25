---
name: typescript-strict-migration
description: Moves a TypeScript project to strict mode one compiler flag at a time, fixing each wave of errors with real types instead of any casts or ts-ignore.
---

# TypeScript strict migration

The aim is a green `tsc --noEmit` after every flag, with no new escape hatches.

## Steps

1. Read `tsconfig.json` (and any extended config). Run `npx tsc --noEmit` and record the baseline error count. Count existing `any`, `@ts-ignore` and `as unknown as` so you can show they did not grow.
2. Enable flags in this order, running `tsc` after each: `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`. When all are on, replace them with `"strict": true`.
3. For each flag, group errors by file and fix the leaf modules first (utilities, types), then the code that uses them.
4. Fix with real types:
   - Missing annotations: write the type from how the value is used; derive it with `typeof` or `ReturnType` when possible.
   - Possibly null: narrow with a check or an early return. Use `?.` and `??` only when the fallback is correct.
   - Catch variables: narrow with `instanceof Error`.
   - Uninitialized properties: initialize in the constructor or mark optional; use `!` only with a comment naming the guarantee.
5. If a flag yields over 150 errors, split by directory and use a per-folder tsconfig that extends the base.
6. Run the tests and the linter before moving to the next flag.

## Rules

- Never add `any`, `@ts-ignore` or a blanket non-null `!` to clear an error.
- Do not change runtime behavior; if a fix needs a behavior change, report it.

## Report

Per flag: errors fixed, files touched, and the final counts of any and ignores compared with the start.
