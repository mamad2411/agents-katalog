# @ladamczyk/qoq-stylelint-scss — Agent Context

Stylelint configuration template for SCSS projects. Extends `@ladamczyk/qoq-stylelint-css`.

## Exports

- `baseConfig` — Stylelint config object for SCSS, ready to use or extend
- `default` — the same object, so `extends: ['@ladamczyk/qoq-stylelint-scss']` resolves

## Usage

Typically consumed via `qoq.config.js` using the `template` field (handled by `@ladamczyk/qoq-cli`). For manual use:

```js
import { baseConfig } from '@ladamczyk/qoq-stylelint-scss';

export default baseConfig;
```

## Added on top of CSS base

- Replaces `stylelint-config-standard` with `stylelint-config-standard-scss`
- SCSS file override: `css-nesting` browser feature suppressed from unsupported-feature warnings
