---
name: follow-tool-tsdown-setup-tsdown
description: Install tsdown and create tsdown.config.ts — entry/dts/sourcemap
argument-hint: "[project-path]"
related:
  - follow-tool-tsdown
  - follow-tool-rolldown
  - follow-lang-typescript
---

## Goal

Install tsdown and set up a basic `tsdown.config.ts` for a TypeScript library — entry, formats, dts, sourcemap, package scripts

## Scope

- First-time tsdown setup in a TypeScript library project
- Covers install, `tsdown.config.ts`, `entry`/`format`/`dts`/`sourcemap`, build scripts
- Migration from tsup → `workflows/migrate-from-tsup/SKILL.md`

## Execute

### 1. Prerequisites

> Goal: the project is ready for tsdown

1. Confirm it is a TypeScript library project — with `tsconfig.json` and entries in `src/`
2. Check the Node.js version against the requirement in the parent skill or official docs
3. If a tsdown setup already exists → verify only, skip to step 5

### 2. Install

> Goal: Install tsdown

1. `bun add -D tsdown`, or scaffold a new project with `bun create tsdown@latest`
2. Verify with `bunx tsdown --version`

### 3. Create Config

> Goal: the minimal `tsdown.config.ts` needed

1. Create `tsdown.config.ts` at the root using `defineConfig` from `tsdown`
2. Set `entry` — a string/array/object pointing to entry files such as `src/index.ts`
3. Set `format: ['esm', 'cjs']` per the consumers, and `platform` (`node`/`browser`/`neutral`)
4. Enable `dts: true` for `.d.ts` generation, and `sourcemap` when wanted
5. Other options (`clean`, `minify`, `external`, `publint`, `attw`) → add per need, see official docs

### 4. Package Scripts And Exports

> Goal: build is runnable and the package points to the right output

1. Add `"build": "tsdown"` and `"dev": "tsdown --watch"` to `package.json`
2. Check `exports`/`main`/`module`/`types` point at the `dist/` files tsdown produces — see official docs for the pattern

### 5. Verify

> Goal: build passes with complete output

1. Run `bun run build` → no errors
2. Check `dist/`: `.mjs`/`.cjs` per the formats, `.d.ts`/`.d.cts` complete, sourcemaps if enabled
3. If `publint`/`attw` are enabled → their results must pass
4. If verification fails → `/resolve-errors` max 3 rounds, then report

## Rules

### 1. Setup

- Always use `defineConfig`, start with a minimal config and add more later
- Use only options from official docs — never guess

### 2. Package Hygiene

- `exports` must match the real output files — a mismatch = consumers can't import
- `files` in `package.json` must include `dist`

- Use /follow-tool-tsdown if needed
- Use /follow-tool-rolldown if needed
- Use /follow-lang-typescript if needed

## Expected Outcome

- tsdown installed with a correct `tsdown.config.ts`
- `bun run build` produces `dist/` with complete JS + `.d.ts`
- `package.json` exports point to the right output
