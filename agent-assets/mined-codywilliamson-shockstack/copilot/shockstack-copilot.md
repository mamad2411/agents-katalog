# ShockStack

Convention-first monorepo: Astro 5 + Vue 3 + Tailwind 4, optional .NET 10 backend.

## Structure

- `frontend/` — Astro 5, Vue 3, Tailwind 4, Better Auth, Drizzle ORM
- `backend/` — .NET 10 Web API, clean architecture (optional)
- `packages/tokens/` — Style Dictionary design tokens

## Conventions

- pnpm workspaces + Turborepo
- Conventional commits
- Tailwind 4 via `@tailwindcss/vite`
- CSS-first animations; JS motion allowed when CSS can't reasonably express it
- Design Tokens: Edit `docs/system/DESIGN.md` -> run `pnpm --filter @shockstack/tokens build` to extract via `@google/design.md` and export variables.
- See `docs/system/` for detailed docs
