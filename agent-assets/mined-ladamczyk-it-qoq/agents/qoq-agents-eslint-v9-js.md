# @ladamczyk/qoq-eslint-v9-js — Agent Context

Base ESLint flat config template for vanilla JavaScript projects. All other `@ladamczyk/qoq-eslint-v9-*` packages extend this one.

## Exports

- `jsLayer` — the root delta layer of the qoq ESLint configuration chain, as a plain flat-config object. Every downstream `@ladamczyk/qoq-eslint-v9-*` package consumes it directly in its own `configs.*` chain; prefer `configs.base` below for your own composition
- `configs.base` — `jsLayer` wrapped in a `defineConfig` array, for ESLint-native composition (`defineConfig({ files: [...], extends: [configs.base] })`)
- `EslintLayer` — the type every `eslint-v9-*` package's delta layer is declared with
- `EslintConfig` / `EslintConfigPlugin` — TypeScript types for config objects and plugins
- `getNoRestrictedImportsPaths(extra?)` — returns `no-restricted-imports` paths array; auto-detects lodash and es-toolkit in the consumer project and adds usage guidance
- `getNoRestrictedImportsRule(extraPaths?)` — the full `no-restricted-imports` rule entry (paths above + the one-level-back relative-import pattern), so extending packages can add paths without re-assembling the tuple
- `restoreSonarjsRules(names, excluded?)` — rule entries re-enabling a disabled sonarjs group (`TEST_ONLY_SONARJS_RULES` / `REACT_ONLY_SONARJS_RULES`) at sonarjs's own recommended severity
- `@ladamczyk/qoq-eslint-v9-js/stats` subpath — `getEnabledRuleNames(config)` and `getEnabledDeprecatedRules(config, statsDir)` read a `@eslint/config-inspector build` payload (a package's `stats/` dir) so a test can fail when the config enables a deprecated rule

## Usage

Typically consumed via `qoq.config.js` using the `template` field (handled by `@ladamczyk/qoq-cli`). For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-js';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.js'],
  extends: [configs.base],
});
```

## Included plugins & key rules

| Plugin                   | Purpose                                          |
| ------------------------ | ------------------------------------------------ |
| `@eslint/js`             | JS recommended rules                             |
| `eslint-config-prettier` | Disables rules that conflict with Prettier       |
| `eslint-plugin-import-x` | Import ordering, cycles, duplicates              |
| `eslint-plugin-sonarjs`  | Code quality (cognitive complexity, duplication) |

Prettier is not run through ESLint — it's a separate, standalone check (`@ladamczyk/qoq-prettier*` + the CLI's Prettier executor). `eslint-config-prettier` only turns off ESLint/plugin rules that would otherwise fight Prettier's formatting.

Key limits: max 600 lines per file, max 200 lines per function. Relative imports deeper than one level (`../../*`) are forbidden — use path aliases instead.
