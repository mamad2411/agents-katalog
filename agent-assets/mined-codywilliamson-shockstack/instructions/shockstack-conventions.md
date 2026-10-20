---
applyTo: "**"
description: "Project conventions and standards"
---

## Conventions

- Conventional commits enforced via commitlint
- pnpm workspaces, no npm/yarn
- Tailwind 4 via `@tailwindcss/vite` (not legacy integration)
- Design tokens: edit `docs/system/DESIGN.md` → run `pnpm --filter @shockstack/tokens build` to extract via `@google/design.md` and export to Tailwind
- Theme: `[data-theme="dark"]` / `[data-theme="light"]` on `<html>`
- Prefer CSS animations; JS-driven motion is allowed when CSS can't reasonably express the interaction (coordinated sequencing, shared element transitions, gesture-tied motion)
- `prefers-reduced-motion` respected globally

See `docs/system/` for architecture, frontend, backend, database, auth, tokens, CI/CD, and conventions documentation.
