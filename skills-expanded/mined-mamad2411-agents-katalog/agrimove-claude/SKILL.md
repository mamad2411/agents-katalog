# CLAUDE.md

## Project Overview

**Farmmove** is a pnpm monorepo for the **AgriMove Ghana** platform — a website and API for an agricultural mobility initiative in Ghana. The frontend is a React SPA; the backend is an Express 5 API server. Both connect to Supabase (PostgreSQL) as the database.

## Monorepo Structure

```
farmmove/
├── artifacts/
│   ├── agrimove-ghana/     # React frontend (Vite, Tailwind, shadcn/ui)
│   ├── api-server/         # Express 5 API server
│   ├── api-client-react/   # Generated React Query hooks (from OpenAPI spec)
│   ├── api-spec/           # OpenAPI 3.1 spec + Orval codegen config
│   └── api-zod/            # Generated Zod schemas from OpenAPI spec
├── lib/
│   └── db/                 # Drizzle ORM schema + DB connection
├── scripts/                # One-off utility scripts
├── supabase/               # Supabase config/migrations
├── pnpm-workspace.yaml
├── tsconfig.base.json      # Shared TS config (composite, bundler resolution, es2022)
└── tsconfig.json           # Root TS project references
```

## Tech Stack

| Layer | Technology |
|---|---|
| Package manager | pnpm workspaces |
| Node.js | 24 |
| TypeScript | 5.9 |
| Frontend | React 19, Vite 7, Tailwind CSS 4, shadcn/ui (Radix), Wouter (routing), Framer Motion |
| Backend | Express 5, Pino (logging) |
| Database | PostgreSQL via Supabase, Drizzle ORM, drizzle-zod |
| Validation | Zod (v4 API: `zod/v4`) |
| API codegen | Orval (from OpenAPI spec → React Query hooks + Zod schemas) |
| Build | esbuild (api-server), Vite (frontend) |

## Key Commands

### Root (run from project root)
```bash
pnpm run typecheck          # Full typecheck using tsc --build (always run from root)
pnpm run build              # Typecheck then build all packages
```

### Frontend (`artifacts/agrimove-ghana`)
```bash
pnpm --filter @workspace/agrimove-ghana run dev     # Dev server
pnpm --filter @workspace/agrimove-ghana run build   # Production build
pnpm --filter @workspace/agrimove-ghana run typecheck
```

### API Server (`artifacts/api-server`)
```bash
pnpm --filter @workspace/api-server run dev         # Build + start
pnpm --filter @workspace/api-server run build       # esbuild bundle → dist/index.cjs
pnpm --filter @workspace/api-server run typecheck
```

### Database (`lib/db`)
```bash
pnpm --filter @workspace/db run push                # Push schema changes (dev)
pnpm --filter @workspace/db run push-force          # Force push (dev fallback)
```

### API Codegen (`lib/api-spec`)
```bash
pnpm --filter @workspace/api-spec run codegen       # Regenerate client hooks + Zod schemas from openapi.yaml
```

### Scripts (`scripts`)
```bash
pnpm --filter @workspace/scripts run <script-name>
```

## TypeScript Rules

- **Always typecheck from the root** — `pnpm run typecheck`. Running `tsc` inside a single package fails if its dependencies haven't been built.
- All packages use `composite: true` and extend `tsconfig.base.json`.
- `emitDeclarationOnly` — `tsc` only emits `.d.ts` files; bundling is done by Vite/esbuild.
- When package A depends on package B, A's `tsconfig.json` must list B in `references`.

## Frontend Details (`artifacts/agrimove-ghana`)

- **Routing**: Wouter (`wouter`) — not React Router.
- **UI components**: shadcn/ui (Radix primitives + Tailwind) in `src/components/ui/`.
- **Pages**: `src/pages/` — Home, About, HowItWorks, Impact, GetInvolved, Media, Admin, Privacy, Terms.
- **Animations**: Framer Motion — shared motion config in `src/lib/motion.ts`.
- **Supabase client**: `src/lib/supabase.ts`.
- **Site config/constants**: `src/lib/site.ts`.
- **Contact/mailto helpers**: `src/lib/mailto.ts`.
- **Hero images**: `src/lib/heroImages.ts`.
- **Env**: see `artifacts/agrimove-ghana/.env.example`.

## Backend Details (`artifacts/api-server`)

- **Entry**: `src/index.ts` — reads `PORT`, starts Express.
- **App setup**: `src/app.ts` — mounts CORS, body parsing, routes at `/api`.
- **Routes**: `src/routes/index.ts` mounts sub-routers.
  - `GET /api/health` — health check.
  - `GET /api/inquiries` — list inquiries (admin-authenticated).
  - `POST /api/inquiries` — submit inquiry (public).
- **Admin auth**: `src/lib/adminAuth.ts`.
- **Supabase client (server)**: `src/lib/supabase.ts`.
- **Env**: see `artifacts/api-server/.env.example`.

## Database Schema (`lib/db`)

- `inquiries` table: `id`, `first_name`, `last_name`, `email`, `organisation`, `interest`, `message`, `created_at`.
- Each model file exports: Drizzle table, insert schema (drizzle-zod), and TypeScript types.
- Schema barrel: `lib/db/src/schema/index.ts` re-exports all models.

## Adding New Features

### New API endpoint
1. Add/update the model in `lib/db/src/schema/<model>.ts` and export from `schema/index.ts`.
2. Run `pnpm --filter @workspace/db run push` to sync the DB.
3. Add the route in `artifacts/api-server/src/routes/<resource>.ts` and mount it in `src/routes/index.ts`.
4. Update `lib/api-spec/openapi.yaml` and run codegen if the frontend needs typed client hooks.

### New frontend page
1. Create `artifacts/agrimove-ghana/src/pages/<Page>.tsx`.
2. Add a route in `artifacts/agrimove-ghana/src/App.tsx`.
3. Add a nav link in `src/components/Navbar.tsx` if needed.

## Environment Variables

- Frontend env vars must be prefixed `VITE_` to be exposed to the browser.
- API server reads `PORT`, `DATABASE_URL`, Supabase credentials, and admin auth secrets.
- Copy `.env.example` files in each artifact to `.env` and fill in values.
