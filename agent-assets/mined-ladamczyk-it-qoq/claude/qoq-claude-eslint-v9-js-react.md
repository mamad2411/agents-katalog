# CLAUDE.md

Consumer-facing context (exports, plugins, import order rule) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib ESM-only + ./bin inspector
npm test      # from the repo root — no per-package test script
```

## Internal architecture

`src/index.ts` builds `reactLayer` — only this package's own delta on top of the JS base (React/JSX plugins, browser globals, restored React-only sonarjs rules, adjusted import-order/no-restricted-imports rules) and the React rule relaxations — plus `configs.base`, the `defineConfig` array form of the chain (JS base → `reactLayer`), merged per file by ESLint's own cascade. The import order rule and no-restricted-imports rule are patched versions of the JS base rules — they are reconstructed by spreading the original rule config and adding React-specific entries.

`src/rules/no-multi-comp.ts` holds the custom `no-multi-comp` rule (re-exported from `index.ts` via `export *`). It is a plain `Rule.RuleModule` whose component detection is delegated to `@eslint-react/core`'s `getFunctionComponentCollector` — the same machinery `@eslint-react/eslint-plugin` uses — rather than re-implementing detection like `react/no-multi-comp`. Legacy class components are intentionally not supported. The collector's `visitor` is run during traversal and merged with our own `Program:exit` (a small `mergeListeners` helper composes listeners that share a selector); at exit we call `api.getAllComponents(program)`, sort by source position, and report every component after the first. The rule takes no options. `@eslint-react/core` is ESM-only (like `@eslint-react/eslint-plugin` and `eslint-plugin-react-refresh`), which is why this package — and `eslint-v9-ts-react` — ship **ESM-only** (`./lib/index.mjs`, no CJS output): Rolldown externalizes deps, and an externalized `require()` of an `import`-only package can't resolve (`ERR_PACKAGE_PATH_NOT_EXPORTED`). The React Rolldown configs override the shared one to drop the CJS output; the `exports` map exposes only the `import` condition.

To enable the rule under the `@eslint-react/` prefix without mutating the shared plugin singleton, `index.ts` builds `reactPluginWithCustomRules` — a shallow copy of `reactPlugin` with the custom rule merged into its `rules` map — and registers _that_ as the `@eslint-react` plugin.
