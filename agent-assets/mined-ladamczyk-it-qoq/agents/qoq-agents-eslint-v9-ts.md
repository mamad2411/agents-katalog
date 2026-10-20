# @ladamczyk/qoq-eslint-v9-ts — Agent Context

ESLint flat config template for TypeScript projects. Extends `@ladamczyk/qoq-eslint-v9-js` and adds TypeScript-specific rules.

## Exports

- `tsLayer` — only this package's delta on the JS base (TypeScript parser, `@typescript-eslint` rule sets, import-x TS adjustments, naming conventions, etc.), as a flat-config layer for `defineConfig` composition (shared with every `eslint-v9-ts-*` sibling)
- `testLayer` — delta layer with test-file relaxations (disables `@typescript-eslint/no-unsafe-argument`, `@typescript-eslint/no-unsafe-member-access`, `sonarjs/no-duplicate-string`; `no-unsafe-assignment` is already off in `tsLayer`)
- `strictLayer` — opt-in strictness delta layer: hand-picked type-aware rules from typescript-eslint's `strict` family (`no-non-null-assertion`, `no-unnecessary-condition`, `prefer-reduce-type-parameter`, `use-unknown-in-catch-callback-variable`)
- `configs.base` / `configs.test` / `configs.strict` — `defineConfig` array forms (JS base + the matching layers), merged per file by ESLint's cascade

## Usage

Typically consumed via `qoq.config.js` using the `template` field. For manual use:

```js
import { configs } from '@ladamczyk/qoq-eslint-v9-ts';
import { defineConfig } from 'eslint/config';

export default defineConfig({
  files: ['**/*.ts'],
  extends: [configs.base],
});
```

For test files use `configs.test`; for the opt-in strictness layer use `configs.strict`.

## Added on top of the JS base

- **Parser**: `typescript-eslint` with `projectService: true`
- **Resolver**: `eslint-import-resolver-typescript` (replaces the Node resolver)
- **Plugins**: `@typescript-eslint`
- **Rule sets**: `typescript-eslint/recommended` + `recommended-requiring-type-checking` at their
  native severities (`no-unsafe-assignment`/`no-misused-promises` are tuned by hand)
- **import-x**: inherits the JS base's import-x rules (`recommended` + `no-cycle`
  `ignoreExternal: true` + `order`/`no-empty-named-blocks`/`no-mutable-exports`/`no-named-default`),
  layers `eslint-plugin-import-x`'s own `typescript` config on top (turns `import-x/named` off), and
  additionally disables `namespace`/`default`/`no-named-as-default-member` — TypeScript's compiler
  already guarantees what they check and they're among the slowest import-x rules.
- **Extra hand-picked rules not in either recommended set**: `no-import-type-side-effects`,
  `no-deprecated`, `no-shadow`

## Naming conventions enforced

| Selector                       | Convention             |
| ------------------------------ | ---------------------- |
| Interfaces                     | `I` prefix, PascalCase |
| Type aliases                   | `T` prefix, PascalCase |
| Enums                          | `E` prefix, PascalCase |
| Enum members                   | UPPER_CASE             |
| Classes                        | PascalCase             |
| Static class properties        | UPPER_CASE             |
| Methods, functions, parameters | camelCase              |
