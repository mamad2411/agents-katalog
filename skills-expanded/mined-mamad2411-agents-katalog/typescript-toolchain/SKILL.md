---
name: typescript-toolchain
description: "When to activate: ESLint, Prettier, tsup, swc, esbuild, lint-staged, husky, commitlint, semantic-release, CI setup"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# TypeScript Toolchain

## ESLint Config (flat config, eslint.config.ts)
```ts
import js from '@eslint/js'
import tsParser from '@typescript-eslint/parser'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import importPlugin from 'eslint-plugin-import'

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      import: importPlugin,
    },
    rules: {
      ...tsPlugin.configs['recommended-type-checked'].rules,
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/consistent-type-imports': ['error', { prefer: 'type-imports' }],
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'import/order': ['error', {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling'],
        'newlines-between': 'always',
        alphabetize: { order: 'asc' },
      }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
  {
    files: ['**/*.test.{ts,tsx}', '**/__tests__/**'],
    rules: { '@typescript-eslint/no-explicit-any': 'off' },
  },
]
```

## Prettier Config
```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

## tsup (library bundler)
```ts
// tsup.config.ts
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  sourcemap: true,
  clean: true,
  splitting: false,
  treeshake: true,
  external: ['react', 'react-dom'],
  esbuildOptions(options) {
    options.target = 'es2020'
  },
})
```

## lint-staged + husky
```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yaml,yml}": "prettier --write"
  }
}
```
```bash
# Setup
npx husky init
echo "npx lint-staged" > .husky/pre-commit
echo "npx commitlint --edit \$1" > .husky/commit-msg
```

## commitlint
```ts
// commitlint.config.ts
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'test', 'chore', 'perf', 'ci', 'revert',
    ]],
    'subject-max-length': [2, 'always', 72],
  },
}
```

## GitHub Actions CI
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:    { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with: { version: 9 }

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - run: pnpm type-check
      - run: pnpm lint
      - run: pnpm test --coverage
      - run: pnpm build

      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

## semantic-release
```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): ${nextRelease.version}"
    }],
    "@semantic-release/github"
  ]
}
```

## package.json Scripts Template
```json
{
  "scripts": {
    "dev":        "vite",
    "build":      "tsc -p tsconfig.build.json && vite build",
    "preview":    "vite preview",
    "type-check": "tsc --noEmit",
    "lint":       "eslint . --max-warnings 0",
    "lint:fix":   "eslint . --fix",
    "format":     "prettier --write .",
    "test":       "vitest run",
    "test:watch": "vitest",
    "test:ui":    "vitest --ui",
    "coverage":   "vitest run --coverage",
    "clean":      "rm -rf dist .next coverage"
  }
}
```
