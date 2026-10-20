---
name: follow-create-oxlint-plugin
description: Configure and use Oxlint built-in and JavaScript plugins
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-eslint
  - ship
  - run-lint
  - run-format
---
## Goal

Configure and use Oxlint plugins, both built-in and JavaScript plugins, for linting

## Scope

For setting up Oxlint plugins, both built-in (native) and JavaScript plugins, for linting

- Packages: `oxlint`, `oxlint-tsgolint` (optional type-aware preview) — always confirm the latest versions via `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for later reference (create oxlint plugins)

### 2. Setup

> Goal: Install oxlint and check the existing config file

1. Install oxlint with `bun add -D oxlint`
2. Check whether a config file already exists

### 3. Create Config File

> Goal: Create the config file at the project root

1. Create `.oxlintrc.json`/`.oxlintrc.jsonc` (standalone binary or Node) or `oxlint.config.ts` (Node-based package only) at the root — add `"$schema": "./node_modules/oxlint/configuration_schema.json"` for autocomplete
2. Generate a starter config with `oxlint --init`; point to a specific config with `oxlint -c <path>` (disables nested lookup)
3. Pick the format you need — `oxlint.config.ts` requires Node v22.18+ or v24+; only one config file per directory is allowed (JSON and TS cannot coexist)

### 4. Configure Built-in Plugins

> Goal: Enable built-in plugins via the `plugins` field

1. Choose the built-in plugins you need (react, unicorn, typescript, oxc, import, jest, vitest, jsx-a11y, nextjs — native in Rust)
2. Define them via the `plugins` field in the config
3. Set categories for severity

### 5. Configure JS Plugins (Optional)

> Goal: Define JavaScript plugins via the `jsPlugins` field

1. Install the desired ESLint plugins — the Oxlint JS plugin API is compatible with ESLint v9+, so most work out of the box (alpha — not covered by semver; report bugs where behavior differs from ESLint)
2. Define them via the `jsPlugins` field in the config — paths are any import specifier (`./plugin.js`, `eslint-plugin-foo`, `@foo/eslint-plugin`) resolved relative to the config file
3. Use a custom name for reserved plugin names

### 6. Verify

> Goal: Test the plugins with oxlint

1. Run `oxlint` to test the plugins
2. Verify the rules work correctly

### 7. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Config File

- Use `.oxlintrc.json` or `oxlint.config.ts`
- Place the file at the project root
- oxlint detects the config file automatically

### 2. Built-in Plugins

- Use the `plugins` field for native plugins
- Setting `plugins` overwrites the default plugin set
- List every plugin you need in the array
- Use CLI flags such as `--import-plugin` to enable a plugin

### 3. JS Plugins

- Use the `jsPlugins` field for JavaScript plugins — the array can mix strings (`"eslint-plugin-foo"`, name derived from the specifier) and objects (`{ "name": "alias", "specifier": "eslint-plugin-foo" }`)
- JS plugins are in alpha stage and not subject to semver
- Use a custom name (object form) for reserved plugin names

### 4. Reserved Plugin Names

- Default-on: `eslint`, `typescript`, `unicorn`, `oxc`; opt-in: `react`, `react-perf`, `nextjs`, `import`, `jsdoc`, `jsx-a11y`, `node`, `promise`, `jest`, `vitest`, `vue`
- These are implemented natively in Rust — `plugins: []` disables all of them; enable via CLI `--<name>-plugin`, disable via `--disable-<name>-plugin`
- A custom name is required if you want the JavaScript version

### 5. Categories

- Oxlint enables `correctness` by default; severity values: `"off"`/`"allow"`, `"warn"`, `"error"`/`"deny"` — other related fields: `rules`, `overrides` (by file pattern), `settings` (shared across rules); CLI `-A`/`--allow` disables a rule/category
- correctness: code that is definitely wrong or useless
- suspicious: code that is likely wrong or useless
- pedantic: strict rules that may produce false positives
- perf: rules for improving runtime performance
- style: rules for consistent style
- restriction: rules that forbid specific patterns or features
- nursery: rules under development that may change

- Use /follow-create-sdk when needed
- Use /follow-tool-eslint when needed
- Use /run-lint when needed
- Use /run-format when needed

## Expected Outcome

- Config file created at the root
- Built-in plugins configured correctly
- JS plugins configured correctly (if used)
- Rules work when running `oxlint`
