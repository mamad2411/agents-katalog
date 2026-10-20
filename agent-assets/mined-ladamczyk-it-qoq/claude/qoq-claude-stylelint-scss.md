# CLAUDE.md

Consumer-facing context (exported config, inheritance) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib
npm test      # from the repo root — no per-package test script
```

## Internal architecture

Single source file `src/index.ts`. Spreads `@ladamczyk/qoq-stylelint-css`'s `baseConfig`, overrides `extends` to use `stylelint-config-standard-scss`, and adds an SCSS-specific `overrides` entry that suppresses the `css-nesting` unsupported-feature warning.
