# CLAUDE.md

Consumer-facing context (exports, plugins, key rules) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

- **`src/index.ts`** — exports `jsLayer`, the root delta layer of the whole `eslint-v9-*` chain (assembled at import time by composing rules from all plugins), plus `configs.base` (`jsLayer` wrapped in a `defineConfig` array for `defineConfig`/`extends`-style composition), the `EslintLayer`/`EslintConfig`/`EslintConfigPlugin` types, and `getNoRestrictedImportsPaths()`. The pre-`defineConfig` name `baseConfig` is gone — the root is a delta layer like every other package's, not the object others merge into.
- **`src/tools.ts`** — exports `executeInspector()`, used by the `bin` entry to generate ESLint stats files (consumed by tests in other packages via `npm run config-inspector` at the root).
- **`src/stats.ts`** (exported as `@ladamczyk/qoq-eslint-v9-js/stats`) — parses the `structured-clone` payload that `@eslint/config-inspector build` writes under a package's `stats/__rpc-dump/` and exposes `getEnabledRuleNames()` / `getEnabledDeprecatedRules()`. Every `eslint-v9-*` package's `src/stats.spec.ts` imports these to assert it enables no deprecated rules.

This is the root of the ESLint inheritance chain. Every other `eslint-v9-*` package composes `jsLayer` — this package's own delta layer — directly into its own `configs.*` chain, and never by nesting another package's already-composed `configs.*`: `defineConfig` doesn't dedupe diamond extends, so a nested `configs.*` would re-apply `jsLayer` mid-chain and clobber earlier layers' sonarjs rule restorations.

Every layer in the chain — all twelve packages — is declared `EslintLayer` (`Linter.Config`), not `EslintConfig`: a delta layer may legitimately carry no `rules` at all. `EslintConfig` stays for rule records (`EslintConfig['rules']`).
