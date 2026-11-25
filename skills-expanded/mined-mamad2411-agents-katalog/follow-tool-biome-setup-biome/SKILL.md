---
name: follow-tool-biome-setup-biome
description: Install Biome and create biome.json — editor integration, CLI basics
argument-hint: "[project-path]"
related:
  - follow-tool-biome
  - run-lint
  - run-format
  - setup-cicd
---

## Goal

Install Biome in the project — correct `biome.json`/`biome.jsonc`, working editor format-on-save, CLI scripts ready

## Scope

- First-time Biome setup (linter + formatter + assist)
- Covers install, config file, editor integration, CLI basics
- Migration from ESLint/Prettier → `workflows/migrate-from-eslint-prettier/SKILL.md`

## Execute

### 1. Prerequisites

> Goal: environment ready before installing

1. Confirm `package.json` exists and identify the package manager the project uses
2. If `biome.json`/`biome.jsonc` + `@biomejs/biome` in deps already exist → verify only, skip to step 5

### 2. Install And Init

> Goal: install and create the config

1. `bun add -D @biomejs/biome` or the project's package manager
2. Run `bunx biome init` to create the config — or hand-write `biome.jsonc` per the parent skill
3. Set `$schema` pointing to `./node_modules/@biomejs/biome/configuration_schema.json` for autocomplete
4. Enable `vcs` integration (`enabled`, `clientKind: "git"`, `useIgnoreFile: true`)

### 3. Configure Features

> Goal: enable linter/formatter/assist per need

1. `linter.enabled: true` + recommended rules — add rules only where the project wants them
2. `formatter.enabled: true` — set indent/line width if different from defaults
3. `assist.enabled: true` for import sorting/actions
4. monorepo → root `biome.jsonc` + workspace configs with `root: false` + `extends` (see the parent skill)
5. For uncertain options → see official docs (`biomejs.dev`)

### 4. Editor Integration

> Goal: format-on-save and linting in the editor

1. VS Code: install the Biome extension, set `"editor.defaultFormatter": "biomejs.biome"` and `editor.formatOnSave` in `.vscode/settings.json`
2. Enable `source.fixAll.biome` in `codeActionsOnSave` if auto-fix is wanted
3. Other editors → see official docs for supported extensions/LSP
4. If the project previously used Prettier/ESLint extensions → disable them for JS/TS to prevent conflicts

### 5. CLI And Verify

> Goal: scripts work and output is correct

1. Add scripts: `"lint": "biome lint"`, `"lint:fix": "biome lint --write"`, `"format": "biome format --write"` per the parent skill
2. Run `bun run lint` + `bun run format` → work with no config errors
3. Run `bunx biome check .` → reports real diagnostics
4. On a config error → `/resolve-errors` max 3 rounds, then report

## Rules

### 1. Setup

- Use `biome.jsonc` (comments supported) per the parent skill
- Minimal config first — never copy a whole rules block without understanding it
- Use only options from the official docs

### 2. Conflicts

- Never run Biome in parallel with Prettier/ESLint on the same files without a plan — do `migrate-from-eslint-prettier` when switching
- Disable conflicting editor formatters for JS/TS

- Use /run-lint if needed
- Use /run-format if needed
- Use /setup-cicd if needed

## Expected Outcome

- Biome installed with a valid config
- Editor format-on-save + fix actions work
- `lint`/`format`/`check` scripts run without config errors
