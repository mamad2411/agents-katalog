# @ladamczyk/qoq-eslint-v9-ts-vitest-rtl — Agent Context

ESLint flat config template for TypeScript test files using Vitest + React Testing Library. Extends `@ladamczyk/qoq-eslint-v9-ts-vitest`.

## Exports

- `tsVitestRtlLayer` — only this package's own delta on top of the composed chain (empty rules — it just names the config node; `rtlLayer`'s restoration of `prefer-screen-queries` staying off already covers the delta, so there's nothing left to add)
- `configs.base` — the `defineConfig` array form: the full chain (JS base → vitest layer → RTL layer → ts layer → ts test relaxations → ts-vitest layer → `tsVitestRtlLayer`), merged per file by ESLint's cascade. `rtlLayer` sits before the TS layers so TS-layer decisions still win, matching the legacy merge order

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts-vitest-rtl';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.tsx'],
  extends: [configs.base],
});
```

## Inheritance

Composes JS-Vitest's `vitestLayer`, JS-Vitest-RTL's `rtlLayer`, and `eslint-v9-ts`'s `tsLayer`/`testLayer` with `eslint-v9-ts-vitest`'s `tsVitestLayer`, all as delta layers — never from another package's own `configs.*`, since `defineConfig` doesn't dedupe diamond extends.
