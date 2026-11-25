---
name: typescript
description: >-
  TypeScript conventions: strict mode, ESLint, explicit types, node: imports,
  string enums, complexity limits, and ESM readiness. Use when writing or
  reviewing TypeScript anywhere in the repository.
---

# TypeScript

Applies to all TypeScript in this repository (paths from `project-context`).

## Compiler strictness

- **Always use TypeScript strict mode** — `"strict": true` in `tsconfig.json`.
- Enable or preserve strict-family flags: `strictNullChecks`, `noImplicitAny`, `strictBindCallApply`, `noFallthroughCasesInSwitch`, `forceConsistentCasingInFileNames`.
- Do not weaken compiler options to silence errors — fix the types.

## ESLint

- Follow **strict ESLint rulesets** configured per package.
- **Do not disable or ignore ESLint rules** unless there is no practical alternative — and then:
  - Scope the suppression to the smallest line/block (`eslint-disable-next-line` with rule name).
  - Add a one-line comment explaining **why**.
  - Never blanket `eslint-disable` for a whole file without PM approval.
- Run lint on touched packages before handoff.

## Explicit types

- Prefer **explicit types** — parameters and **return types** on public/exported functions.
- Avoid `any`; use `unknown` + narrowing when shape is uncertain.
- Prefer `interface` or `type` for object shapes at module boundaries; use discriminated unions for variant data.

```typescript
// Prefer
function calculateTotal(items: LineItem[]): number {
  // ...
}

// Avoid
function calculateTotal(items) {
  // ...
}
```

## Imports

- Prefer **`node:`-prefixed** built-in imports:

```typescript
import { readFile } from "node:fs/promises";
import path from "node:path";
```

- Use path aliases (`@/…`) where configured in `tsconfig.json`.
- Group imports: external → internal → relative; match neighboring files.

## Enums and string unions

- Prefer **`enum` with string values** (or `as const` object + derived type) over bare `string` for fixed sets.
- Use plain string union types only when the set is truly open-ended or external.

## Complexity

- Split functions that mix validation, transformation, and I/O.
- Target: one clear responsibility per function; extract helpers when nesting exceeds ~3 levels or logic exceeds ~40–50 lines.
- Prefer early returns (see `clean-code` skill) to flatten control flow.

## Module system (ESM readiness)

- Prefer ESM (`import` / `export`) over CommonJS.
- Some frameworks (e.g. NestJS) may still compile to CommonJS — stay ESM-compatible in source (`import`/`export`, avoid unnecessary `require()`).
- New shared packages should be authored as ESM-first.

## Framework notes

- **NestJS (optional):** DTOs with explicit property types + validators; services throw HTTP exceptions for expected failures.
- **Next.js (optional):** Typed props; typed API client responses; keep `'use client'` files focused.

## Review self-check

- [ ] `strict` respected; no new `any` without justification
- [ ] Explicit return types on exported/public functions
- [ ] No broad ESLint disables; lint passes
- [ ] String enums (or `as const`) for fixed domain value sets
- [ ] Complex logic split into named helpers
- [ ] `node:` prefix on Node built-in imports
- [ ] No unnecessary CJS patterns in new code
