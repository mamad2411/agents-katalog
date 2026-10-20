# @ladamczyk/qoq-eslint-v9-ts-vitest — Agent Context

ESLint flat config template for TypeScript test files using Vitest. Composes `@ladamczyk/qoq-eslint-v9-js-vitest`'s `vitestLayer` and `@ladamczyk/qoq-eslint-v9-ts`'s `tsLayer`/`testLayer`.

## Exports

- `tsVitestLayer` — only this package's own delta (the vitest typecheck setting)
- `configs.base` — the `defineConfig` array form of the full chain: JS base → `vitestLayer` → `tsLayer` → `testLayer` → `tsVitestLayer`, merged per file by ESLint's cascade (the ts layers are true deltas that never clobber the vitest layer's restorations)

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts-vitest';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.ts'],
  extends: [configs.base],
});
```

## Inheritance

Combines JS-Vitest's `vitestLayer` (Vitest plugin + globals) with `eslint-v9-ts`'s `tsLayer` and `testLayer` (TypeScript parser + relaxed unsafe rules), composed as delta layers — never from another package's own `configs.*`, since `defineConfig` doesn't dedupe diamond extends. The JS-only vitest relaxations from `eslint-v9-js-vitest` are deliberately absent — they don't apply under typed linting.
