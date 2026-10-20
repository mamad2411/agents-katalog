---
name: follow-lib-tanstack-config
description: Use TanStack Config — a build/publish toolchain for maintaining high-quality JS packages
argument-hint: "[package-dir]"
related:
  - follow-lib-tanstack-ecosystem
  - run-build
  - resolve-errors
---

## Goal

Use TanStack Config — the configuration and tooling TanStack itself uses to build + publish high-quality packages (ESM/CJS, types, publint-style checks)

## Scope

Use when maintaining/publishing library packages — **not app config**; app projects don't need it (use tsdown/tsup/vite per `follow-tool-*` instead)

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the config toolchain into the package

```bash
bun add -D @tanstack/config
```

### 2. Configure Package Build

> Goal: build/publish config per the TanStack standard

1. Read `https://tanstack.com/config/latest` — check the current config file format (`tanstack.config.*` or a `package.json` field)
2. Define entry points + output formats (ESM/CJS + `.d.ts`)
3. Run the build/publish checks the package provides — verify the exports map, types resolution, and publint-style issues before publishing

### 3. Verify

> Goal: the package build/publish passes checks

1. `/run-build` — complete outputs (ESM + CJS + types)
2. `npm pack --dry-run` — the published files are correct
3. `bunx publint` passes
4. On failure → `/resolve-errors` max 3 rounds

## Rules

- Use only for packages being published — apps are unrelated
- The exports map must resolve for `import`/`require`/`types` conditions alike
- Don't replace the project's existing build tool (tsdown/tsup) without reason — this config lib is optimized for TanStack-style publishing

## Expected Outcome

- The package builds with complete formats + types
- Publish checks pass with no exports/types issues
