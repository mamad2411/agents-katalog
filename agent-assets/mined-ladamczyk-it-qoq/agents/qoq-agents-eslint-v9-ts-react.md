# @ladamczyk/qoq-eslint-v9-ts-react — Agent Context

ESLint flat config template for TypeScript + React projects. Composes `@ladamczyk/qoq-eslint-v9-js-react`'s `reactLayer` and `@ladamczyk/qoq-eslint-v9-ts`'s `tsLayer`.

## Exports

- `tsReactLayer` — only this package's own delta on top of the composed chain (typescript-eslint's `recommended-typescript` react rules)
- `configs.base` — the `defineConfig` array form: the full chain (JS base → React layer → ts layer → `tsReactLayer`), merged per file by ESLint's cascade

## Usage

Typically consumed via `qoq.config.js` using the `template` field. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts-react';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.tsx'],
  extends: [configs.base],
});
```

## Inheritance

Composes JS-React's `reactLayer` (plugins: `@eslint-react`, `@stylistic`, `compat`, `react-refresh`) with `eslint-v9-ts`'s `tsLayer` (TypeScript parser + `@typescript-eslint` rules) and this package's own `tsReactLayer` (`@eslint-react/recommended-typescript` rules), all as delta layers merged per file by ESLint's cascade — never from another package's own `configs.*`, since `defineConfig` doesn't dedupe diamond extends. The custom `@eslint-react/no-multi-comp` rule (defined in `eslint-v9-js-react`) is inherited via `reactLayer`; layer composition never clobbers it, so it needs no re-assertion here. The Fast-Refresh rule `react-refresh/only-export-components` is likewise inherited from `reactLayer` unchanged.
