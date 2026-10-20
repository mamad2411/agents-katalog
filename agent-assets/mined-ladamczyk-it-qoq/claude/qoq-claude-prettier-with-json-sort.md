# CLAUDE.md

Consumer-facing context (config values) lives in `AGENTS.md`.

## Commands

```bash
npm test # from the repo root — no per-package test script
```

## Internal architecture

Config-only package: `index.json` extends the base prettier config with `prettier-plugin-sort-json`. No build step required.
