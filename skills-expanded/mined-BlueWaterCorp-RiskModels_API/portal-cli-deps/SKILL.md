---
name: portal-cli-deps
description: RiskModels_API — Next.js root build typechecks cli/; mirror CLI deps in root package.json for Vercel, or exclude cli from tsconfig. Use when Vercel/CI fails on missing modules in cli/src or when editing cli/package.json.
---

# Portal + CLI dependency layout (RiskModels_API)

## Problem

- `next build` at the **repo root** typechecks **`cli/src`** (root `tsconfig` includes `**/*.ts`).
- **Vercel** only runs **`npm ci` at the root**; **`cli/package.json` is not installed** unless you add a separate step.

So imports like `inquirer` that exist only in `cli/package.json` can work in a mixed local setup but **fail on Vercel** with “Cannot find module”.

## Fix (pick one)

1. **Mirror deps on the root** — Add the same runtime packages to root `package.json` as in `cli/package.json`, add `@types/*` to root `devDependencies` if needed, run `npm install`, commit `package-lock.json`.
2. **Stop typechecking CLI from Next** — `exclude: ["cli"]` (or narrow `include`) in root `tsconfig.json`, and typecheck the CLI only via `cli/`’s own `npm run build` in CI.

## Commander typing

Do not use `cmd.optsWithGlobals<{…}>()` under strict TS; cast: `(cmd.optsWithGlobals() as { json?: boolean })`.

## Canonical write-up

See **“Next.js portal + cli/ (Vercel builds)”** in [AGENTS.md](../../../AGENTS.md).
