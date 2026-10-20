# @ladamczyk/qoq-eslint-v9-ts-jest — Agent Context

ESLint flat config template for TypeScript test files using Jest. Composes `@ladamczyk/qoq-eslint-v9-js-jest`'s `jestLayer` and `@ladamczyk/qoq-eslint-v9-ts`'s `tsLayer`/`testLayer`.

## Exports

- `tsJestLayer` — only this package's own delta on top of the composed chain (empty rules — it just names the config node; layer composition means the jest layer's restorations and the ts layers' relaxations are never re-applied here)
- `configs.base` — the `defineConfig` array form: the full chain (JS base → jest layer → ts layer → ts test relaxations → `tsJestLayer`), merged per file by ESLint's cascade

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts-jest';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.ts'],
  extends: [configs.base],
});
```

## Inheritance

Combines JS-Jest's `jestLayer` (Jest plugin + globals) with `eslint-v9-ts`'s `tsLayer` and `testLayer` (TypeScript parser + relaxed unsafe rules), composed as delta layers by `configs.base`'s linear chain — never from another package's own `configs.*`, since `defineConfig` doesn't dedupe diamond extends. The JS-only `sonarjs/no-incompatible-assertion-types` disable that `eslint-v9-js-jest` appends to its own `configs.base` is deliberately absent here — this package has type information, so that rule stays enabled.
