# @ladamczyk/qoq-eslint-v9-js-vitest — Agent Context

ESLint flat config template for JavaScript test files using Vitest. Extends `@ladamczyk/qoq-eslint-v9-js`.

## Exports

- `vitestLayer` — only this package's delta on the JS base, as a flat-config layer for `defineConfig` composition (shared with `eslint-v9-ts-vitest`; deliberately excludes the JS-only relaxations)
- `configs.base` — the `defineConfig` array form: JS base → `vitestLayer` → JS-only relaxations, merged per file by ESLint's cascade

## Usage

Typically consumed via `qoq.config.js` using the `template` field, scoped to test file patterns. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-js-vitest';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.test.js'],
  extends: [configs.base],
});
```

## Added on top of the JS base

- **Plugin**: `@vitest/eslint-plugin` (recommended rules), plus a hand-picked set
  (`no-duplicate-hooks`, `no-conditional-in-test`, `no-test-return-statement`,
  `no-large-snapshots`, `prefer-strict-equal`, `prefer-to-be`, `no-test-prefixes`,
  `no-conditional-tests`, `prefer-hooks-in-order`, `max-nested-describe`,
  `require-to-throw-message`) not part of vitest's own `recommended` config
- Vitest globals injected into `languageOptions`
- `sonarjs/no-duplicate-string` disabled (common in test fixtures)
- Several `TEST_ONLY_SONARJS_RULES` restored here are disabled again: ones that duplicate
  a `@vitest/eslint-plugin` recommended rule (`no-skipped-tests`, `no-exclusive-tests`,
  `no-duplicate-test-title`, `no-empty-test-title`, `assertions-in-tests`), ones that
  hard-gate on Chai usage a Vitest consumer never has (`disabled-timeout`,
  `chai-determinate-assertion`, `no-same-argument-assert`), and
  `no-incompatible-assertion-types`, which is a hard no-op without a typed-linting
  parser (this package has none — `eslint-v9-ts-vitest` re-enables it, since it does)
