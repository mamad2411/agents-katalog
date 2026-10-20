# @ladamczyk/qoq-eslint-v9-js-jest — Agent Context

ESLint flat config template for JavaScript test files using Jest. Extends `@ladamczyk/qoq-eslint-v9-js`.

## Exports

- `jestLayer` — only this package's delta on the JS base (Jest plugin + globals, restored test-lifecycle sonarjs rules, jest-specific extras), as a flat-config layer for `defineConfig` composition (shared with `eslint-v9-ts-jest`; deliberately excludes the JS-only relaxations)
- `configs.base` — the `defineConfig` array form: JS base → `jestLayer` → JS-only relaxations, merged per file by ESLint's cascade

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-js-jest';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.js'],
  extends: [configs.base],
});
```

## Added on top of the JS base

- **Plugin**: `eslint-plugin-jest` (recommended rules), plus `no-duplicate-hooks`,
  `no-large-snapshots`, `prefer-strict-equal`, `no-conditional-in-test`,
  `require-to-throw-message`, `no-test-return-statement`, `prefer-to-be`,
  `prefer-hooks-in-order`, `max-nested-describe` (not part of jest's own
  `recommended` config)
- Jest globals injected into `languageOptions`
- `sonarjs/no-duplicate-string` disabled (common in test fixtures)
- Several `TEST_ONLY_SONARJS_RULES` restored here are disabled again:
  ones that duplicate an `eslint-plugin-jest` recommended rule (`no-skipped-tests`,
  `no-exclusive-tests`, `no-duplicate-test-title`, `assertions-in-tests`,
  `no-empty-test-title`), ones that hard-gate on Mocha/Chai usage a Jest consumer never
  has (`disabled-timeout`, `chai-determinate-assertion`, `no-same-argument-assert`),
  and `no-incompatible-assertion-types`, which is a hard no-op without a typed-linting
  parser (this package has none — `eslint-v9-ts-jest` re-enables it, since it does)
