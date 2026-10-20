---
name: follow-tool-stryker-mutator-setup-stryker
description: Install Stryker Mutator with config and test runner integration
argument-hint: "[scope]"
related:
  - follow-tool-stryker-mutator
  - follow-tool-vitest
  - run-test
  - update-tests
---

## Goal

Install and configure Stryker Mutator so mutation testing runs — core, runner plugin, config file, smoke run

## Scope

- First-time Stryker setup in a JavaScript/TypeScript project
- Covers: install, `stryker init`, config keys, test runner integration, verify run
- Does not cover: performance tuning/incremental (`workflows/optimize mutation`)

## Execute

### 1. Check Prerequisites

> Goal: Check the environment and test runner before install

1. Check Node.js >= 22 (required by Stryker v10) — see official docs for the latest version
2. Identify the current test runner from `package.json`: `vitest`, `jest`, `mocha` — run `/follow-tool-vitest` if using vitest
3. Run the regular test suite first — tests must be green and non-flaky before mutation testing
4. Check `package.json` — if `@stryker-mutator/core` is already there (idempotent check) → skip install

### 2. Install Packages

> Goal: Install the Stryker core and runner plugin

1. Install `bun add -D @stryker-mutator/core`
2. Install the runner plugin matching the test runner, e.g. `bun add -D @stryker-mutator/vitest-runner`
3. If using TypeScript → install `bun add -D @stryker-mutator/typescript-checker`
4. See plugin options in `references/cli.md` or the official docs

### 3. Initialize Config

> Goal: Create the minimal Stryker config

1. Run `bunx stryker init` to generate the config (pick the runner/reporters matching what's installed)
2. Review `stryker.config.json`/`stryker.config.mjs` — define `testRunner`, `mutate`, `reporters`, `coverageAnalysis`
3. Set the `mutate` glob explicitly — e.g. `['src/**/*.ts', '!src/**/*.test.ts']`; don't mutate the whole repo
4. Set `coverageAnalysis: 'perTest'` — faster and more precise than `all`
5. Set `ignorePatterns` for generated/vendored dirs

### 4. Run Smoke Mutation

> Goal: Verify Stryker works with the real suite

1. Run `bunx stryker run` on a small scope first (temporarily narrow `mutate`, or accept a long run)
2. If there are problems → debug with `bunx stryker run --logLevel trace`
3. Open `reports/mutation/html/index.html` and check the report
4. Confirm mutants were generated, tests ran, and results include `killed`/`survived`/`timeout`

### 5. Wire Scripts

> Goal: Add scripts and keep artifacts tidy

1. Add `"test:mutation": "stryker run"` to `package.json`
2. Add `reports/mutation/` (or the output dir you set) to `.gitignore`
3. If verification fails → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Tests must be green and stable first — never set up Stryker on a flaky suite
- `mutate` must be explicit — never mutate tests, configs, or generated files
- Use `coverageAnalysis: 'perTest'` as the default
- Use official docs as the primary source — check the docs whenever an option is unclear
- Mutation runs are slow — smoke run on a small scope before scaling up

## Expected Outcome

- Stryker installed with the runner plugin and a correct config
- A successful smoke mutation run with an HTML report
- The `test:mutation` script ready to use
