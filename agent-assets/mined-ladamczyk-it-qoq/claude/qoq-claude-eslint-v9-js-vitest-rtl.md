# CLAUDE.md

Consumer-facing context (inheritance, exports) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib CJS+ESM + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` exports `rtlLayer` — only this package's own delta on top of JS-Vitest (`eslint-plugin-testing-library`'s `flat/react` plugin/rules, `prefer-user-event`, and the RTL rule relaxations) — and `configs.base`, the `defineConfig` array form of the full chain (JS base → vitest layer → `rtlLayer` → a JS-only layer disabling `sonarjs/no-incompatible-assertion-types`), merged per file by ESLint's own cascade. Mirrors `eslint-v9-js-jest-rtl` with the Vitest base instead.

Composed from delta layers only — never from `eslint-v9-js-vitest`'s own `configs.base`: `defineConfig` doesn't dedupe diamond extends, so nesting it would re-apply the JS base mid-chain and clobber the vitest layer's rule restorations.
