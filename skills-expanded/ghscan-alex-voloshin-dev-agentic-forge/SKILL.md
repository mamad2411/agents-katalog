---
name: javascript-patterns
description: JavaScript (Node) stack conventions agentic-forge applies when the detected stack is plain JavaScript — the toolchain (the repo's package manager / eslint / prettier), modern ESM and async idioms, gradual typing via JSDoc + // @ts-check, testing discipline, and the high-value JS pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# JavaScript patterns

The plain-JavaScript stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and
the `code-review` lint aspect) when `stacks.detect` reports JavaScript (a `package.json` with no
`tsconfig.json` — a TypeScript repo uses `typescript-patterns`). It carries only what is
**JS-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md). (Mechanism:
ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own scripts** (`package.json` `scripts`); use the package manager the
**lockfile** implies (`package-lock.json` → `npm`, `pnpm-lock.yaml` → `pnpm`, `yarn.lock` →
`yarn`, `bun.lock`/`bun.lockb` → `bun`). Defaults:

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `npm test` (often `vitest`/`jest`) | green; new behaviour covered |
| lint | `npm run lint` (or `eslint .`) | clean (no new `eslint-disable`) |
| format | `prettier --write .` | applied |
| types | `// @ts-check` + JSDoc (optionally `tsc --checkJs`) | no editor type errors |

## Idioms

- **ESM** (`import`/`export`); `const`/`let`, **never `var`**; `async`/`await` and **always
  `await`** (no floating promises); `===` (never `==`); `?.` / `??`.
- Array methods (`map`/`filter`/`reduce`/`find`) and destructuring over manual loops; template
  literals; small pure functions.
- **No static types, so validate at boundaries** — check external/`JSON.parse`/`response.json()`
  input with a schema validator or explicit guards **before returning or using it**; returning the
  raw parsed value (typed `unknown`/`any`) is *not* validation. Annotate with **JSDoc +
  `// @ts-check`** for editor safety.

## Testing

- The repo's runner (vitest/jest), arrange–act–assert. Cover the happy path plus a boundary and
  an error case. **Deterministic:** fake timers, no real network/clock — stub at boundaries.
- Never weaken, skip, or delete an existing test to go green.

## Pitfalls (JavaScript-specific, high-value)

- **Floating / unawaited promises**; missing `await`; unhandled rejections.
- **`==` and truthiness coercion** (`0`/`""`/`null`/`undefined`/`NaN`); use `===`.
- **`var` hoisting** and `this` rebinding (prefer arrow functions for callbacks).
- **Mutating shared objects/arrays** passed by reference; floating-point (`0.1 + 0.2`).
- **Prototype pollution** from merging untrusted JSON; unvalidated `process.env`/input.

## Definition of done (JavaScript)

eslint clean (no new disables), prettier applied, tests green with the new boundary/error cases,
no floating promises, external input validated at the boundary, JSDoc + `// @ts-check` where it
adds safety — using the repo's own scripts and package manager where declared.
