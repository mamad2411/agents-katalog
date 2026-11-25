---
name: biome
description: Fast linting/formatting for TypeScript/React. Use when setting up linter, migrating from ESLint/Prettier, or running code quality checks.
version: 1.0.0
---

# Biome

## Overview

Biome is a fast Rust-based toolchain that combines formatting, linting, and import organization. **25x faster than Prettier**, **15x faster than ESLint**. Replaces ESLint + Prettier with single tool.

**Key features (v2.0)**:
- 97% Prettier compatibility, 340+ lint rules
- Type-aware linting without TypeScript compiler
- Supports: JS, TS, JSX, TSX, JSON, CSS, GraphQL
- Framework domains: react, next, solid, test

## When to Use This Skill

- Setting up linting/formatting for new project
- Migrating from ESLint + Prettier
- Configuring pre-commit hooks
- Setting up CI code quality checks
- Configuring monorepo linting

## Instructions

### 1. Installation

```bash
# npm/pnpm/yarn
npm install --save-dev --save-exact @biomejs/biome
npx @biomejs/biome init

# Bun
bun add -D -E @biomejs/biome
bunx @biomejs/biome init
```

### 2. Configuration (biome.json)

**Recommended for React/TypeScript:**

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "domains": {
        "react": "recommended"
      },
      "correctness": {
        "noUnusedVariables": "error"
      },
      "nursery": {
        "noFloatingPromises": "error"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all",
      "semicolons": "always"
    }
  },
  "organizeImports": {
    "enabled": true
  },
  "files": {
    "ignore": ["node_modules", "dist", "build", ".next", "coverage"]
  },
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  }
}
```

### 3. Package.json Scripts

```json
{
  "scripts": {
    "check": "biome check .",
    "check:fix": "biome check --write .",
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format --write .",
    "ci": "biome ci ."
  }
}
```

### 4. Commands

```bash
# Check all (lint + format + imports) - recommended
npx @biomejs/biome check --write

# CI mode (fails on issues, no auto-fix)
npx @biomejs/biome ci

# Format only
npx @biomejs/biome format --write .

# Lint only
npx @biomejs/biome lint --write .
```

## Migration from ESLint/Prettier

```bash
# Auto-migrate configs
npx @biomejs/biome migrate eslint --write
npx @biomejs/biome migrate prettier --write
```

**Manual steps:**
1. Run migration commands
2. Review generated `biome.json`
3. Delete: `.eslintrc.*`, `.prettierrc.*`, `.eslintignore`, `.prettierignore`
4. Remove ESLint/Prettier from `package.json`
5. Update pre-commit hooks and CI

## Biome v2 Features

### Domains

Enable framework-specific rules automatically:

```json
{
  "linter": {
    "rules": {
      "domains": {
        "react": "recommended",
        "next": "recommended",
        "test": "all"
      }
    }
  }
}
```

Biome auto-detects from `package.json` dependencies.

### Type Inference (Biotype)

Type-aware linting without TypeScript compiler (~85% coverage):

```json
{
  "linter": {
    "rules": {
      "nursery": {
        "noFloatingPromises": "error"
      }
    }
  }
}
```

### Multi-file Analysis

```json
{
  "linter": {
    "rules": {
      "nursery": {
        "noImportCycles": "error",
        "noPrivateImports": "error"
      }
    }
  }
}
```

### Suppressions

```typescript
// Single line
// biome-ignore lint/suspicious/noExplicitAny: legacy code
const data: any = fetchData();

// Entire file
// biome-ignore-all lint/suspicious/noExplicitAny

// Range
// biome-ignore-start lint/style/noVar
var legacy = "code";
// biome-ignore-end
```

## Monorepo Setup

**Root config:**
```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "formatter": { "indentStyle": "space", "indentWidth": 2 },
  "linter": { "rules": { "recommended": true } }
}
```

**Package config (`packages/web/biome.json`):**
```json
{
  "root": false,
  "extends": "//",
  "linter": {
    "rules": {
      "domains": { "react": "recommended" }
    }
  }
}
```

## Pre-commit Hooks

### Lefthook (Recommended)

```bash
npm install -D lefthook
npx lefthook install
```

**lefthook.yml:**
```yaml
pre-commit:
  commands:
    biome:
      run: npx @biomejs/biome check --write --no-errors-on-unmatched --files-ignore-unknown=true {staged_files}
      stage_fixed: true
```

### Husky + lint-staged

```json
{
  "lint-staged": {
    "*.{js,ts,jsx,tsx,json,css}": ["biome check --write --no-errors-on-unmatched"]
  }
}
```

## VS Code Integration

Install: [Biome VS Code Extension](https://marketplace.visualstudio.com/items?itemName=biomejs.biome)

**.vscode/settings.json:**
```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "biome.enabled": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports.biome": "explicit",
    "source.fixAll.biome": "explicit"
  }
}
```

## CI (GitHub Actions)

```yaml
name: Code Quality
on: [push, pull_request]

jobs:
  biome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: biomejs/setup-biome@v2
      - run: biome ci --changed
```

## Quick Reference

| Task | Command |
|------|---------|
| Check all + fix | `biome check --write .` |
| CI mode | `biome ci .` |
| Lint only | `biome lint .` |
| Format only | `biome format --write .` |
| Migrate ESLint | `biome migrate eslint --write` |
| Migrate Prettier | `biome migrate prettier --write` |

## Guidelines

### Do

- Use `biome check --write` as primary command (lint + format + imports)
- Commit `biome.json` to repo
- Use `--changed` in CI for speed
- Enable relevant domains (react, next, test)
- Use `--no-errors-on-unmatched` in hooks

### Don't

- Mix Biome with ESLint/Prettier in same project
- Forget to remove old linter configs after migration
- Skip `--write` flag when you want auto-fix
- Ignore `nursery` rules - they have useful type-aware checks

## Limitations

| Limitation | Workaround |
|------------|------------|
| JSON-only config | Use `extends` for shared configs |
| Vue/Svelte/Astro | Partial support (improving) |
| YAML/Markdown | Not supported |
| Some ESLint plugins | Check rule compatibility |
