---
name: follow-tool-eslint-config-flat
description: Write ESLint flat config — eslint.config.js structure, plugins, ignores
argument-hint: "[config-topic]"
related:
  - follow-tool-eslint
  - follow-lang-typescript
  - run-lint
---

## Goal

Write/adjust `eslint.config.js` (flat config) correctly — config array structure, plugins, files/ignores scoping

## Scope

- Covers the flat config format (`eslint.config.js`/`eslint.config.ts`) for ESLint 9+/10
- structure: array of config objects, `files`, `ignores`, `plugins`, `rules`, `languageOptions`
- migration to oxlint → `workflows/migrate-to-oxlint/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: know the original state before editing

1. Open `eslint.config.*` at the root — if only `.eslintrc*` exists instead → ESLint 10 does not support it; convert to flat config first (see the official migration docs)
2. List the plugins/presets in use from `package.json`
3. Check `.eslintignore` — it must move into `ignores` in the flat config

### 2. Config Structure

> Goal: correct array structure

1. `export default [ ... ]` — an array of config objects, order matters (later ones override)
2. Use `defineConfig()` from `eslint/config` for type safety
3. A global-ignores object: `{ ignores: [...] }` without `files` behaves like `.eslintignore`
4. Spread base presets (`js.configs.recommended`, `ts.configs.recommended`) before custom objects

### 3. Plugins And Language Options

> Goal: register plugins and the parser correctly

1. `plugins: { name: pluginObject }` — import the plugin then place it in the object; key = rule prefix
2. `languageOptions.parser` for TS → use `typescript-eslint` (not a standalone parser)
3. `languageOptions.globals` for env globals — use the `globals` package, e.g. `globals.browser`, `globals.node`
4. Scoped configs: `{ files: ['**/*.test.ts'], plugins: { ... }, rules: { ... } }` per concern

### 4. Rules And Ignores

> Goal: rules cover the right scope

1. Rules in an object with `files` cover only those files — an object without `files` applies to every file
2. Core ignores: `dist/`, `node_modules/` (default), `coverage/`, generated files, `*.config.*` when they need no linting
3. Put rule-disabling configs (e.g. `eslint-config-prettier`) last in the array
4. Check the effective config per file with `bunx eslint --print-config <file>`

### 5. Verify

> Goal: the flat config actually works

1. Run `bunx eslint .` → lints every intended file with no config error
2. Run `bunx eslint --print-config <file>` → verify the actually resolved rules/plugins
3. Confirm files that should be ignored are not linted
4. Config error → `/resolve-errors` max 3 rounds, then report

## Rules

### 1. Structure

- flat config only for ESLint 9+/10 — never create new `.eslintrc*`
- array order = precedence — presets first, overrides later, disables last
- use `defineConfig` when the file is `.ts`

### 2. Scope

- ignores in the flat config only — not `.eslintignore`
- plugins register per config object — the rule prefix must match the key

## Expected Outcome

- A correct `eslint.config.js/ts`: presets, plugins, scoped rules, ignores
- `eslint .` and `--print-config` show the intended effective config
