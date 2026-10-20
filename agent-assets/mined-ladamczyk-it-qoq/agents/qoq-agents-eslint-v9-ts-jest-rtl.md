# @ladamczyk/qoq-eslint-v9-ts-jest-rtl — Agent Context

ESLint flat config template for TypeScript test files using Jest + React Testing Library. Extends `@ladamczyk/qoq-eslint-v9-ts-jest`.

## Exports

- `tsJestRtlLayer` — only this package's own delta on top of the composed chain (empty rules — it just names the config node; `rtlLayer`'s own restorations are never clobbered under layer composition, so there's nothing left to re-add)
- `configs.base` — the `defineConfig` array form: the full chain (JS base → jest layer → RTL layer → ts layer → ts test relaxations → ts-jest layer → `tsJestRtlLayer`), merged per file by ESLint's cascade. `rtlLayer` sits before the TS layers so TS-layer decisions still win, matching the legacy merge order

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts-jest-rtl';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.ts'],
  extends: [configs.base],
});
```

## Inheritance

Composes JS-Jest's `jestLayer`, JS-Jest-RTL's `rtlLayer`, and `eslint-v9-ts`'s `tsLayer`/`testLayer` with `eslint-v9-ts-jest`'s `tsJestLayer`, all as delta layers — never from another package's own `configs.*`, since `defineConfig` doesn't dedupe diamond extends. The JS-only `sonarjs/no-incompatible-assertion-types` disable that `eslint-v9-js-jest-rtl` appends to its own chain is deliberately absent here — this package has type information, so that rule stays enabled.
