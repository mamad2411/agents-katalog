# CLAUDE.md

Consumer-facing context (inheritance, exports) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `tsJestRtlLayer` — only this package's own delta on top of the composed chain (empty rules; `rtlLayer`'s own restorations are never clobbered under layer composition, so there's nothing left to re-add) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → jest layer → RTL layer → ts layer → ts test relaxations → ts-jest layer → `tsJestRtlLayer`), merged per file by ESLint's own cascade. `rtlLayer` sits before the TS layers so TS-layer decisions still win, matching the legacy merge order.

Composed from delta layers only — never from another package's own `configs.*`: `defineConfig` doesn't dedupe diamond extends, so nesting one would re-apply the JS base mid-chain and clobber earlier layers' sonarjs rule restorations.
