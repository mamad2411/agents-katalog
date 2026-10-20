# CLAUDE.md

Consumer-facing context (inheritance, exports) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `rtlLayer` — only this package's own delta on top of JS-Jest (`eslint-plugin-testing-library`'s `flat/react` plugin/rules, `prefer-user-event`, and the RTL rule relaxations) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → jest layer → `rtlLayer` → a JS-only layer disabling `sonarjs/no-incompatible-assertion-types`), merged per file by ESLint's own cascade.

Composed from delta layers only — never from `eslint-v9-js-jest`'s own `configs.base`: `defineConfig` doesn't dedupe diamond extends, so nesting it would re-apply the JS base mid-chain and clobber the jest layer's rule restorations.
