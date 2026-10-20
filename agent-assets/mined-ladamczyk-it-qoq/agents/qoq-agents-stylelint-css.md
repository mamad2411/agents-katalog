# @ladamczyk/qoq-stylelint-css — Agent Context

Stylelint configuration template for CSS projects. All other `@ladamczyk/qoq-stylelint-*` packages extend this one.

## Exports

- `baseConfig` — Stylelint config object, ready to use or extend
- `default` — the same object, so `extends: ['@ladamczyk/qoq-stylelint-css']` resolves

## Usage

Typically consumed via `qoq.config.js` using the `template` field (handled by `@ladamczyk/qoq-cli`). For manual use:

```js
import { baseConfig } from '@ladamczyk/qoq-stylelint-css';

export default baseConfig;
```

## Included rule sets & plugins

| Source                                      | Purpose                                               |
| ------------------------------------------- | ----------------------------------------------------- |
| `stylelint-config-standard`                 | Standard CSS rules                                    |
| `stylelint-config-clean-order`              | Property declaration ordering                         |
| `stylelint-prettier`                        | Prettier as a Stylelint rule                          |
| `stylelint-file-max-lines`                  | Max 600 lines per file                                |
| `stylelint-high-performance-animation`      | Warns on low-performance animation properties         |
| `stylelint-no-unsupported-browser-features` | Warns on unsupported CSS features (severity: warning) |
