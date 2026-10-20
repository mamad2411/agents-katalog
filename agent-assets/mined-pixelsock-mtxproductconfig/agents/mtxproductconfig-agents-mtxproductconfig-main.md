<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Repository Guidelines

## Project Structure & Module Organization
- `src/`: Application code
  - `components/`: React UI (Shadcn UI + Tailwind)
  - `services/`: Supabase client wrappers, rules engine, product matching, SKU, images
  - `utils/` and `tools/`: small helpers and query validation
  - `test/`: dev-only runtime checks (no test runner configured)
- `scripts/`: Node/ bash utilities (schema, rules validation, types)
- `data/` and `deco-thin-svgs/`: curated option data and SVG assets
- `payload/`: admin/tools (not required to run the configurator)
- `docs/`: developer notes and workflow references

## Build, Test, and Development Commands
- `npm run dev`: Start Vite dev server (hot reload)
- `npm run build`: Type-check with `tsc` and produce production build
- `npm run preview`: Serve the built app locally
- `npm run lint`: ESLint over `ts/tsx`
- Useful scripts:
  - `npx tsx scripts/rules-phase2-validate.ts`: end-to-end rules validation against Supabase
  - `node scripts/introspect-schema.js`: schema sanity checks

Example: `VITE_SUPABASE_URL=https://<project>.supabase.co VITE_SUPABASE_ANON_KEY=... npm run dev`

## Coding Style & Naming Conventions
- Language: TypeScript + React 18, ESNext modules
- Style: 2‑space indentation, Prettier-compatible; keep imports sorted logically
- Linting: ESLint (`npm run lint`), strict TS in `tsconfig.json`
- Naming: `PascalCase` React components, `camelCase` functions/vars, `kebab-case` file names except React components
- Do not hard‑code option logic; all availability must derive from Supabase data + rules

## Testing Guidelines
- No formal test runner configured; use dev scripts and targeted checks:
  - `node test-rules-system.js`
  - `node test-configuration-matching.js`
  - `npx tsx scripts/rules-phase2-validate.ts`
- Prefer small, reproducible cases against the live Supabase API
- Add new checks under `src/test/` or `scripts/` following existing patterns

## Commit & Pull Request Guidelines
- Commits: concise, action‑oriented subjects; scope first when helpful
  - Examples: `rules: apply constraints on init`, `availability: compute light_direction per mirror_style`
- PRs must include:
  - Summary of changes and rationale
  - Screenshots/GIFs for UI changes
  - Steps to validate (commands, sample mirror styles)
  - Any Supabase tables/fields affected

## Security & Configuration Tips
- Do not commit secrets. `VITE_*` values are exposed to the browser; use only non‑sensitive tokens there.
- Server‑only secrets (e.g., Supabase service role keys) must remain outside client builds.
- Minimal env to run locally: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`.
