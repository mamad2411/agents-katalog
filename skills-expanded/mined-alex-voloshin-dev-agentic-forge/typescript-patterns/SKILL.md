---
name: typescript-patterns
description: TypeScript stack conventions agentic-forge applies when the detected stack is TypeScript — the toolchain (tsc / eslint / the repo's package manager), strict-typing idioms, testing discipline, layout, and the high-value TS pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# TypeScript patterns

The TypeScript stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports TypeScript. It carries only what is
**TypeScript-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md) —
Claude already knows general TS; this encodes the conventions and gates agentic-forge holds TS
work to. (Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own scripts** — read `package.json` `scripts` (`test` / `lint` / `build` /
`typecheck`) and run *those*. Use the package manager the repo **declares**: the `packageManager`
field first, then the lockfile — `yarn.lock` → `yarn`, `pnpm-lock.yaml` → `pnpm`,
`bun.lock`/`bun.lockb` → `bun`, `package-lock.json` → `npm` — and `npm` when nothing says
otherwise (`<pm> run <script>`, `<pm> install`). The fallbacks `stack-detect` reports name only
what `package.json` declares — the script, else a declared (dev)dependency run through the manager
(`npm exec --no --package=<pkg> --` / `yarn run` / `pnpm exec` / `bun run` — never a download), else
nothing:

| Job | Fallback (with npm) | Gate |
| --- | --- | --- |
| test | `npm run test`, else `vitest run` / `jest` if declared | green; new behaviour covered |
| lint | `npm run lint`, else `eslint .` if declared | clean (no new `eslint-disable`) |
| types | `npm run typecheck` / `type-check`, else `tsc --noEmit` if `typescript` is declared | clean under `strict` (no new `@ts-ignore`/`@ts-expect-error`) |
| format | `npm run format`, else `prettier --write .` if declared | applied |

Run the typecheck and lint on the change before declaring done; never silence a checker to
pass — fix the cause or justify the suppression in the diff.

## Idioms

- **`strict` on, `any` off.** Keep `tsconfig` strict; prefer `unknown` + narrowing, generics,
  and **discriminated unions** over `any`. Validate `JSON.parse`/external data into a typed
  shape (it returns `any`).
- Prefer `type`/`interface` for shapes; **union literals or `as const` objects** over `enum`;
  use `readonly`, `as const`, `satisfies`, and **`import type`** for type-only imports.
- ESM with named exports; `??` / `?.` over manual null checks; `async`/`await` over raw
  `.then` chains — and **always `await`** (no floating promises).

## Testing

- The repo's runner (vitest/jest), arrange–act–assert. Cover the **happy path plus a boundary
  and an error case** per behaviour. Add **type-level** assertions (`expectTypeOf`, `tsd`) when
  the change is about types.
- **Deterministic:** fake timers, no real network/clock/random — inject or stub at boundaries.
  Assert on behaviour and error type/message, not incidental formatting.
- Never weaken, skip, or delete an existing test to go green.

## Pitfalls (TypeScript-specific, high-value)

- **`any` leaks and unsound `as` casts**; the **non-null `!`** assertion hiding a real null.
- **Floating / unawaited promises**; missing `await`; unhandled rejections.
- **`==` instead of `===`**; truthiness coercion surprises.
- **Loose `tsconfig`** (no `strictNullChecks`); `skipLibCheck`/`@ts-ignore` masking errors.
- **`enum` runtime cost** and `const enum` cross-module pitfalls; structural-typing surprises
  (excess-property checks only on object literals).

## Definition of done (TypeScript)

`tsc --noEmit` clean under `strict` (no new `@ts-ignore`), eslint clean (no new disables),
prettier-formatted, tests green with the new boundary/error cases, no `any`/unsafe cast
introduced, public API typed and exported — using the repo's own scripts and package manager
where declared.
