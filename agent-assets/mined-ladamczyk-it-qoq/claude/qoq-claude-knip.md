# CLAUDE.md

Consumer-facing context (exports, pre-built configs) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib
npm test      # from the repo root — no per-package test script
```

## Internal architecture

Two source files:

- **`src/knipConfig.ts`** — `getKnipConfig()` factory that assembles a plain Knip config object from its parameters, all with defaults
- **`src/index.ts`** — re-exports `getKnipConfig` and calls it four times to produce the `jsConfig`, `jsReactConfig`, `tsConfig`, and `tsReactConfig` convenience exports
