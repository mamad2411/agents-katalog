# @ladamczyk/qoq-eslint-v9-js-jest-rtl — Agent Context

ESLint flat config template for JavaScript test files using Jest + React Testing Library. Extends `@ladamczyk/qoq-eslint-v9-js-jest`.

## Exports

- `rtlLayer` — only this package's delta on top of JS-Jest (testing-library `flat/react` plugin/rules + `prefer-user-event`), as a flat-config layer for `defineConfig` composition (shared with `eslint-v9-ts-jest-rtl`)
- `configs.base` — the `defineConfig` array form: JS base → jest layer → `rtlLayer` → JS-only relaxations, merged per file by ESLint's cascade. Composed from delta layers only — never from `eslint-v9-js-jest`'s own `configs.base`, since `defineConfig` doesn't dedupe diamond extends and that would re-apply the JS base mid-chain and clobber the jest layer's rule restorations

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-js-jest-rtl';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.js'],
  extends: [configs.base],
});
```

## Added on top of JS-Jest

- **Plugin**: `eslint-plugin-testing-library` (`flat/react` config), plus
  `prefer-user-event` (not part of `flat/react`)
- `testing-library/prefer-screen-queries` disabled
