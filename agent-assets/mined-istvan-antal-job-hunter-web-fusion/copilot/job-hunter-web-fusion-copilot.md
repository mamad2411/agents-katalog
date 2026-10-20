## Copilot instructions for job-hunter-web-fusion

Goal: make AI agents productive in this React + Vite + Express bridge that surfaces and controls the Deno/TypeORM job-hunter backend.

Big picture

-   This app is a thin UI/server wrapper around the sibling repo `job-hunter` (Deno). It imports backend TypeORM entities and AI functions directly via relative paths (e.g. `../../../../job-hunter/entities/Job.ts`, `../../../../job-hunter/ai/computeCompatibility`).
-   Server (`src/main/server.ts`) exposes POST `/api/:function` and dispatches to functions in `src/main/functions.ts` with a lightweight Context (currently `{ user?: User }`).
-   Client calls server with fetch. Hooks in `src/core/data.ts` and `src/core/serverHooksCreators.ts` unify query/mutation patterns.
-   DB access reuses TypeORM entities from `job-hunter`. A Postgres `DataSource` is created in `src/core/db.ts` using env `DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_LOGGING`.
-   Vite serves the client; in dev the Express server mounts Vite middlewares when `CLIENT_DEV=1` script is used.

Conventions & patterns

-   Server API wiring: add a function in `src/**/api/*.ts` and export it from `src/main/functions.ts`. It will be available at `/api/<name>`; client calls via `useQuery('name', { params: [...] })` or by `createServerHook('name')`.
-   Each server function receives `(args..., context)` where `context.user` derives from the JWT cookie `access-token` (decoded with `JWT_SECRET`). Use it for auth when added.
-   Always use the shared `dataSource` from `src/core/db.ts` for DB work and `getRepository(Job)` for queries. Entities are imported from the backend repo.
-   Query building: prefer TypeORM QueryBuilder for aggregates (see `src/stats/api/fetchStats.ts`). Simple lists use `repository.find({ where, order, take })` (`src/home/api/fetchJobs.ts`).
-   Cookies: server may return cookies by tagging the result with `withCookies()` from `src/core/http.ts`.
-   Env and ports: Vite dev server port via `VITE__PORT` in `vite.config.ts`; API proxy `/api` -> `http://localhost:14001`. Express listens on `PORT` (default 14001). Run client+server with `bun run server`.

Build & run workflows

-   Install: `pnpm|npm|bun install` then ensure sibling `job-hunter` is present (imports use relative paths).
-   Dev (client+server in one): `bun run server` (sets `CLIENT_DEV=1` to mount Vite).
-   Dev (client only): `npm run dev` then point API to running server on 14001.
-   Build: `npm run build` -> emits client to `dist/`; Express serves `dist/` statically.
-   Lint: `npm run lint` (ESLint with TypeScript, React hooks, refresh plugins).

Integration with job-hunter backend

-   DB schema and migrations are owned by `job-hunter`. Run tasks from that repo to migrate: `deno task migrate`, `deno task generate-migration`, etc. Ensure Postgres is running (docker-compose in backend repo exposes service `db`).
-   Shared AI: `computeCompatibility(description)` is imported directly and used by `src/analyze/api/computeJobCompatibility.ts`.
-   Re-analyze flow: `src/analyze/api/reAnalyze.ts` flags a Job by `id` with `reAnalyze=true`; backend scheduled task picks it up next run.

Key files/directories

-   `src/main/server.ts` – Express server, JWT handling, Vite middleware in dev, API dispatch.
-   `src/main/functions.ts` – registry mapping endpoint names to handlers.
-   `src/core/db.ts` – TypeORM DataSource wired to Postgres and backend entities.
-   `src/core/data.ts` & `src/core/serverHooksCreators.ts` – client hooks to call server.
-   `src/home/api/*` – job actions and list/read endpoints.
-   `src/stats/api/fetchStats.ts` – example of cross-entity analytics with QueryBuilder.

Examples

-   List jobs with filters (unknown/known rate): see `src/home/api/fetchJobs.ts` using TypeORM `where` and `Not()`.
-   Stats with daily averages: see `src/stats/api/fetchStats.ts` using JSONB operators on `payRate`.
-   Apply/dismiss job: update flags and `updated` timestamp via `repository.update({ id }, { ... })`.

Gotchas

-   Cross-repo imports require this workspace layout: both projects checked out side-by-side as in this monorepo workspace. Paths assume `job-hunter-web-fusion` sibling of `job-hunter`.
-   Ensure `reflect-metadata` is imported once before TypeORM usage (already in `src/core/db.ts`).
-   Keep response shapes serializable; hooks expect JSON. Return `null` for void endpoints.
-   The client Job interface in `src/core/job.ts` reflects Mongo-style `_id`, but the live entity is Postgres/TypeORM `Job`; use the entity types from backend when server-side.

CI & tasks

-   No dedicated CI here; rely on backend CI for DB and analysis workflows. Consider adding Vite/ESLint checks if needed.

Environment

-   Required: Postgres env vars; Optional: `PORT` (default 14001), `JWT_SECRET` for cookie auth, `VITE__PORT` for dev client port.
