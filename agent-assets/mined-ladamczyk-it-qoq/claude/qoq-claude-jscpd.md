# CLAUDE.md

Consumer-facing context (config values) lives in `AGENTS.md`.

## Commands

```bash
npm test # from the repo root — no per-package test script
```

## Internal architecture

This package is config-only: a single `index.json` file containing the JSCPD preset. No build step. Consumed directly by `JscpdExecutor` in `@ladamczyk/qoq-cli`.
