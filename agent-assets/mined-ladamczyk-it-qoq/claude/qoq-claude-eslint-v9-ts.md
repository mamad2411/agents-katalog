# CLAUDE.md

Consumer-facing context (exports, naming conventions, added plugins) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` defines the package's deltas as flat-config layers (`tsLayer` — TypeScript parser, `@typescript-eslint` rule sets, import-x TS adjustments, naming conventions; `testLayer` — test-file relaxations of `tsLayer`'s unsafe-type rules; `strictLayer` — opt-in strictness rules from typescript-eslint's `strict` family) and exports `configs.base` / `configs.test` / `configs.strict`, the `defineConfig` array forms (JS base → `tsLayer` [→ `testLayer` | `strictLayer`]), merged per file by ESLint's own cascade instead of being pre-merged.
