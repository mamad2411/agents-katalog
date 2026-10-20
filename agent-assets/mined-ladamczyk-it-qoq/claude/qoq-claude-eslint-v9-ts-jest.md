# CLAUDE.md

Consumer-facing context (inheritance, exports) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `tsJestLayer` — only this package's own delta on top of the composed chain (empty rules; it just names the config node, since layer composition means the jest layer's restorations and the ts layers' relaxations are never re-applied here) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → jest layer → ts layer → ts test relaxations → `tsJestLayer`), merged per file by ESLint's own cascade. The JS-only `sonarjs/no-incompatible-assertion-types` disable that `eslint-v9-js-jest` appends to its own `configs.base` is deliberately absent here — this package has type information, so that rule stays enabled.

Composed from delta layers only — never from another package's own `configs.*`: `defineConfig` doesn't dedupe diamond extends, so nesting one would re-apply the JS base mid-chain and clobber earlier layers' sonarjs rule restorations.
