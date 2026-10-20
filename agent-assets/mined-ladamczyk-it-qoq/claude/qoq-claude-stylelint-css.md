# CLAUDE.md

Consumer-facing context (exported config, plugins) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib
npm test      # from the repo root — no per-package test script
```

## Internal architecture

Single source file `src/index.ts` that exports `baseConfig` — a plain Stylelint config object composed from `extends` (standard + clean-order + prettier) and three plugins (file-max-lines, high-performance-animation, no-unsupported-browser-features). No runtime logic; the object is assembled at import time.
