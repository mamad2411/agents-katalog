---
description: Do not run typecheck/build locally; user runs build pipelines
alwaysApply: true
---

# Build and typecheck

Do **not** run package typecheck or production build commands yourself (e.g. `pnpm exec tsc --noEmit`, `pnpm run build`, `npm run build`, workspace `turbo` build tasks) unless:

- The user **explicitly** asks you to run them, or  
- You need a one-off command to **verify** something they directly requested (e.g. reproducing a reported failure).

Assume CI and the user’s local/dev workflows will run builds and typechecks. Prefer editing code and letting those pipelines surface issues.

Lint-only or small diagnostic commands are fine when they help a focused fix.
