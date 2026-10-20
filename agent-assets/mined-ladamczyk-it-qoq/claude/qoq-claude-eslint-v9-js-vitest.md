# CLAUDE.md

Consumer-facing context (exports, plugins, disabled rules) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `vitestLayer` — only this package's own delta on top of the JS base (`@vitest/eslint-plugin` + globals, restored test-lifecycle sonarjs rules, vitest-specific extras, and the test-file rule relaxations) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → `vitestLayer` → a JS-only layer disabling `sonarjs/no-incompatible-assertion-types`), merged per file by ESLint's own cascade. `vitestLayer` deliberately excludes the JS-only relaxations so `eslint-v9-ts-vitest` can compose it directly without inheriting a disable that doesn't apply once type information is available.
