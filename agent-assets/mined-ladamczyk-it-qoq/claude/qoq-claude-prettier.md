# CLAUDE.md

Consumer-facing context (config values) lives in `AGENTS.md`.

## Commands

```bash
npm test # from the repo root — no per-package test script
```

## Internal architecture

Config-only package: `index.json` holds the Prettier preset, `src/index.js` re-exports it for programmatic use. No build step required.
