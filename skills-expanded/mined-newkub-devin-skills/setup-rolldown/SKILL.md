---
name: follow-tool-rolldown-setup-rolldown
description: Install Rolldown and create rolldown.config.ts — entry/output basics
argument-hint: "[project-path]"
related:
  - follow-tool-rolldown
  - follow-tool-vite
  - follow-lang-typescript
---

## Goal

Install Rolldown and set up a basic `rolldown.config.ts` so it can bundle JavaScript/TypeScript — entry, output formats, build scripts

## Scope

- First-time setup of standalone Rolldown (not through Vite)
- Covers install, config file, `input`/`output` basics, package scripts
- Bundle optimization → `workflows/optimize-bundle/SKILL.md`; migration from Rollup → `workflows/migrate-from-rollup/SKILL.md`

## Execute

### 1. Prerequisites

> Goal: environment ready before install

1. Check the Node.js version `^20.19.0 || >=22.12.0`
2. Check `package.json` and the package manager the project uses
3. If already set up (`rolldown` in deps + config exists) → verify only, skip to step 5

### 2. Install

> Goal: install rolldown

1. `bun add -D rolldown` or the project's package manager
2. Verify with `bunx rolldown --version`

### 3. Create Config

> Goal: the minimal necessary `rolldown.config.ts`

1. Create `rolldown.config.ts` at the root using `defineConfig` from `rolldown`
2. Define `input` — a string or object of entry points
3. Define `output.dir`, `output.format` (`'esm'`/`'cjs'`/`'iife'`), and `output.sourcemap` if wanted
4. Write a minimal config first, then add options — see the official docs (`rolldown.rs`) for all options

### 4. Package Scripts

> Goal: run builds through scripts

1. Add `"build": "rolldown -c"` to `package.json` (for CLI flags see `bunx rolldown --help` or the official docs)
2. Add `"build:watch": "rolldown -c --watch"` if watch mode is wanted

### 5. Verify

> Goal: build passes and output is correct

1. Run `bun run build` → no errors
2. Check `dist/` (or the configured `output.dir`): files complete, format correct, sourcemap as set
3. Smoke test importing the output in a consumer or `node dist/<file>`
4. If verify fails → `/resolve-errors` max 3 rounds, then report

## Rules

### 1. Setup

- Always use `defineConfig`
- Minimal config first — never copy a full example config without understanding it
- Use only options from the official docs — never guess option names

### 2. Idempotent

- If a setup already exists → verify only; don't reinstall or overwrite the config

## Expected Outcome

- `rolldown` installed and `rolldown.config.ts` correct
- `bun run build` produces complete output in `dist/`
