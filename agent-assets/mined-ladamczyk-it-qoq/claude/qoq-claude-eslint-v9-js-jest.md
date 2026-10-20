# CLAUDE.md

Consumer-facing context (exports, plugins, disabled rules) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `jestLayer` — only this package's own delta on top of the JS base (Jest plugin + globals, restored test-lifecycle sonarjs rules, jest-specific extras, and the test-file rule relaxations) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → `jestLayer` → a JS-only layer disabling `sonarjs/no-incompatible-assertion-types`, a hard no-op without a typed-linting parser), merged per file by ESLint's own cascade.
