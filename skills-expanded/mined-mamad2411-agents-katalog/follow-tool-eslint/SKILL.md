---
name: follow-tool-eslint
description: Configure ESLint 10 with a complete plugin setup for TypeScript/Vue/Nuxt
argument-hint: "[scope]"
related:
  - follow-create-plugins
  - use-agent-browser
  - use-astgrep
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - run-lint
  - run-format

---

## Goal

Configure ESLint 10 with the flat config format and a complete plugin setup

## Scope

Use for configuring ESLint 10 in TypeScript, Vue, and Nuxt projects

- Latest: `eslint@10.11.0` — flat config only (eslintrc removed), Node `^20.19 | ^22.13 | >=24` (verified 2026-09-26) — pairs with `typescript-eslint@8.70.1`

- eslint-plugin-oxlint: read official docs via `/learn-from-web`
- References: [cli](references/cli.md) 
## Execute

### 1. Install Core Dependencies

> Goal: install ESLint core dependencies

1. Run `bun add -D eslint @eslint/js typescript-eslint`
2. Run `bun add -D eslint-config-prettier`

### 2. Install Vue/Nuxt Plugins

> Goal: install Vue and Nuxt ESLint plugins

1. Run `bun add -D eslint-plugin-vue @vue/eslint-config-typescript`
2. Run `bun add -D @nuxt/eslint-config`

### 3. Install Code Quality Plugins

> Goal: install plugins for code quality and security

1. Run `bun add -D eslint-plugin-import eslint-plugin-unused-imports`
2. Run `bun add -D eslint-plugin-no-secrets eslint-plugin-regexp`
3. Run `bun add -D eslint-plugin-functional eslint-plugin-oxlint`

### 4. Install Testing/A11y Plugins

> Goal: install plugins for testing and accessibility

1. Run `bun add -D eslint-plugin-vitest eslint-plugin-vue-a11y`

### 5. Create Flat Config

> Goal: create `eslint.config.ts` in flat config format

Create `eslint.config.ts` with the flat config format

```typescript [eslint.config.ts]
import { defineConfig } from 'eslint/config'
import js from '@eslint/js'
import ts from 'typescript-eslint'
import vue from 'eslint-plugin-vue'
import prettier from 'eslint-config-prettier'
import importPlugin from 'eslint-plugin-import'
import unusedImports from 'eslint-plugin-unused-imports'
import noSecrets from 'eslint-plugin-no-secrets'
import regexp from 'eslint-plugin-regexp'
import functional from 'eslint-plugin-functional'
import oxlint from 'eslint-plugin-oxlint'
import vitest from 'eslint-plugin-vitest'
import vueA11y from 'eslint-plugin-vue-a11y'

export default defineConfig([
  js.configs.recommended,
  ...ts.configs.recommended,
  ...vue.configs['flat/recommended'],
  prettier,
  {
    files: ['/*.{ts,tsx,vue}'],
    plugins: {
      import: importPlugin,
      'unused-imports': unusedImports,
      'no-secrets': noSecrets,
      regexp,
      functional,
      oxlint,
      vitest,
      'vue-a11y': vueA11y
    },
    rules: {
      'import/order': ['warn', { alphabetize: { order: 'asc' } }],
      'import/no-cycle': 'error',
      'import/no-unresolved': 'error',
      'unused-imports/no-unused-imports': 'warn',
      'no-secrets/no-secrets': 'error',
      'regexp/prefer-regexp-exec': 'warn',
      'functional/immutable-data': 'warn',
      'functional/no-let': 'warn',
      'oxlint/unicorn/no-array-for-each': 'warn'
    }
  },
  {
    ignores: ['dist/', 'node_modules/', '.nuxt/', '*.config.js']
  }
])
```

### 6. Add Package Scripts

> Goal: add linting scripts to `package.json`

```json [package.json]
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "lint:report": "eslint . --format json -o eslint-report.json"
  }
}
```

### 7. Configure IDE

> Goal: set IDE settings for ESLint integration

```json [.vscode/settings.json]
{
  "eslint.validate": ["javascript", "typescript", "vue"],
  "eslint.format.enable": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

### 8. Dispatch To Workflow

> Goal: dispatch specialized work to the appropriate workflow

| Topic | Workflow |-------|----------| write/edit the flat config (`eslint.config.js`) | `workflows/config-flat/SKILL.md` | migrate to oxlint | `workflows/migrate-to-oxlint/SKILL.md` 
## Rules

### 1. Vue/Nuxt Configuration

Configure ESLint for Vue and Nuxt projects

- Use `eslint-plugin-vue` for Vue 3 linting rules and template linting
- Use `@vue/eslint-config-typescript` for the official Vue + TypeScript config
- Use `@nuxt/eslint-config` for Nuxt 3 project-aware config

### 2. Import/Export Management

Manage imports and exports in an orderly way

- Use `eslint-plugin-import` for import ordering, validation, auto-sort
- Use `eslint-plugin-unused-imports` for auto-removing unused imports
- Use `import/no-cycle` to detect circular dependencies

### 3. Code Quality & Security

Check code quality and security

- Use `eslint-plugin-no-secrets` to detect hardcoded secrets/API keys
- Use `eslint-plugin-regexp` for RegExp best practices
- Use `eslint-plugin-functional` for functional programming rules
- Use `eslint-plugin-oxlint` for fast Rust-based linting

### 4. Testing & Accessibility

Check testing and accessibility

- Use `eslint-plugin-vitest` for Vitest linting rules
- Use `eslint-plugin-vue-a11y` for Vue accessibility rules

### 5. Configuration Standards

Configure per ESLint 10 standards

- Use `eslint.config.ts` instead of `.eslintrc` (Flat Config — eslintrc was removed in ESLint 10)
- Use `defineConfig()` from `eslint/config`
- Use `typescript-eslint` instead of `@typescript-eslint/parser`
- Put the `prettier` config last
- Do not use `.eslintignore` in ESLint 10 — use `ignores` in the flat config
- Config lookup in v10 starts from the linted file's directory upward (not cwd) — pass `--config <path>` to keep the old behavior
- Migrate from v9 → v10 with the codemod `npx codemod @eslint/v9-to-v10` (Codemod Registry — not an npm package; has sub-codemods `@eslint/v9-to-v10-config`, `-custom-rules`, `-ruletester`, `-linter-api`) per the official guide `https://eslint.org/docs/latest/use/migrate-to-10.0.0`
- Check plugin compatibility with ESLint 10 before upgrading (`typescript-eslint`, `eslint-plugin-*`)

- Use `/follow-create-plugins` (eslint) if needed
- Use `/use-agent-browser` if needed
- Use `/use-astgrep` if needed
- Use `/follow-tool-usage` if needed
- Use `/follow-best-practice` if needed
- Use `/setup-cicd` if needed
- Use `/run-lint` if needed
- Use `/run-format` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

1. ESLint 10 with flat config and a complete plugin setup
2. Vue 3 + TypeScript + Nuxt 3 support
3. Import ordering and circular dependency detection
4. Security checks for hardcoded secrets
5. Functional programming best practices
6. Fast linting with oxlint
7. Test linting with vitest
8. Accessibility rules for Vue
