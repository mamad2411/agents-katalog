# @ladamczyk/qoq-eslint-v9-js-react — Agent Context

ESLint flat config template for JavaScript + React projects. Extends `@ladamczyk/qoq-eslint-v9-js`.

## Exports

- `reactLayer` — only this package's delta on the JS base (React/JSX plugins, browser globals, restored React-only sonarjs rules, adjusted import-order/no-restricted-imports rules), as a flat-config layer for `defineConfig` composition (shared with `eslint-v9-ts-react`)
- `configs.base` — the `defineConfig` array form: JS base → `reactLayer`, merged per file by ESLint's cascade
- `noMultiCompRule` / `NO_MULTI_COMP_RULE_NAME` — the custom `no-multi-comp` rule (re-exported for TS-React to reuse)

## Usage

Typically consumed via `qoq.config.js` using the `template` field. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-js-react';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.jsx'],
  extends: [configs.base],
});
```

## Added on top of the JS base

- **Plugins**: `@eslint-react`, `@stylistic`, `eslint-plugin-compat`, `eslint-plugin-react-refresh`
- `ecmaFeatures.jsx: true`
- Browser globals added on top of the JS base's node globals (so `window`/`document` don't trip `no-undef`)
- Import order rule adjusted: `react*` imports are placed before all other groups
- `lodash/debounce` restricted — use `use-debounce` in React projects
- Stylistic formatting rules are disabled (Prettier handles formatting)
- `@eslint-react/no-multi-comp` — our custom rule enforcing one React component per file (inspired by `react/no-multi-comp`, but it reuses `@eslint-react/core`'s function-component collector; legacy class components are not supported). Registered into the `@eslint-react` namespace via a shallow copy of the plugin. Takes no options.
- `react-refresh/only-export-components` — keeps jsx/tsx modules Fast-Refresh (HMR) safe by flagging files that mix component and non-component exports. Enabled with `allowConstantExport: true` (Vite-style constant exports are allowed). Not a `@eslint-react` rule — Fast Refresh is a separate concern, so it comes from the dedicated `eslint-plugin-react-refresh`.
