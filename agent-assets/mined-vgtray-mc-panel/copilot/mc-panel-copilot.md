# Copilot Instructions for MCPanel

## Architecture & services
- Monorepo: backend (Fastify/TypeScript) + frontend (Next.js App Router). Docker Compose (frontend 3000, backend 4000, Postgres, Redis). Traefik on external `dokploy-network`; MC servers run as dedicated containers via Docker API.
- Backend entry: `backend/src/index.ts` wires Fastify routes, JWT/cookie auth, CORS, multipart, Socket.IO (`initSocketServer`), starts BullMQ worker (`startWorker`) and backup scheduler.
- Job system: queue name `mcpanel-install` (see `backend/src/jobs/queue.ts`, `worker.ts`). Handlers under `backend/src/jobs/handlers/` perform installs (mods, modpacks, plugins) and backups. Jobs update progress via `updateJobProgress`.
- Modpack install flow: `install-modpack.ts` downloads CurseForge/Modrinth archives, extracts, copies overrides/config/world, records installed mods in DB, updates server type/loader/version, then recreates the MC container via `dockerService.createMinecraftServer`. Downloads cache under `MC_CACHE_PATH` (`/data/cache` in compose).
- Docker integration: `docker.service.ts` uses dockerode against `DOCKER_SOCKET`, network `DOCKER_NETWORK` (compose sets `${COMPOSE_PROJECT_NAME}_default`). Creates per-server containers named `mcpanel-mc-${serverId}` mounting `/data/servers/<id>:/data` with rcon ports managed. Keep this in sync if changing network names or mount paths.
- File manager API: `backend/src/routes/files.routes.ts` → `filemanager.service.ts`. Paths resolved relative to `MC_SERVERS_PATH` and block traversal. Root listing auto-creates the server dir. Some extensions are blocked for editing; listing still returns all entries.
- Marketplace API: `backend/src/routes/marketplace.routes.ts` orchestrates Modrinth/CurseForge installs via jobs. Types `MOD/MODPACK/PLUGIN/DATAPACK` in `services/*`.
- Environment config: `backend/src/config/env.ts` defines required env (JWT_SECRET, DATABASE_URL, REDIS_URL, DOCKER_NETWORK, MC_* paths, PORT, CORS_ORIGINS, CURSEFORGE_API_KEY, RESEND, PANEL_URL). Defaults for MC paths point to `./data/...` but compose mounts `/data/...`.

## Frontend
- Next.js (App Router) in `frontend/src/app`. Uses Zustand stores (`src/stores`), React Query hooks (`src/hooks`) and Socket.IO client (`use-socket`, `use-job-progress`). UI built with shadcn components under `src/components/ui` plus custom `file-editor`, `install-button`, `job-progress`.
- Marketplace + server pages under `src/app/dashboard/**`; server detail tabs (overview/console/files/backups/marketplace/settings) pull from backend routes. Ensure API paths match `/api/*` prefixes defined in backend routes.

## Data & paths
- Server files live at `MC_SERVERS_PATH/<serverId>` with subdirs created by docker service (`mods`, `plugins`, `config`, `world`). Modpack overrides copied into server root; additional dirs `config/mods/scripts/kubejs/defaultconfigs/world` copied when present.
- Cache: `MC_CACHE_PATH` used for downloads; jobs may reuse cached archives (md5 key from URL).

## Commands & workflows
- Backend: `npm run dev` (tsx watch), `npm run build` (tsc), `npm run start` (dist). Prisma: `npm run db:generate`, `db:push`, `db:migrate`. Requires Node >=20.
- Frontend: `npm run dev`, `npm run build`, `npm run start`, `npm run lint`. Next 16 App Router.
- Compose (prod example): ensure env vars for API_URL/WS_URL/PANEL_URL/JWT_SECRET/DB_PASSWORD/etc. Frontend must listen on 0.0.0.0:3000 for Traefik; backend on 0.0.0.0:4000.
- Debug remote deploys via VS Code: you can open the integrated browser (Simple Browser) and use its inspector/console to check runtime issues against the Dokploy-hosted build without rebuilding locally.

## Conventions & cautions
- TypeScript ESM (`"type": "module"`). Use absolute imports with relative paths (no tsconfig paths declared). Keep job progress updates consistent (`step`, `progress`, `message`).
- When touching Docker orchestration, keep network names aligned (`dokploy-network` external + compose default for DB/Redis) and update `DOCKER_NETWORK` if the default changes.
- File operations must stay within resolved server path; respect blocked traversal and editable extension rules. For listing, return all entries; for editing, enforce extension whitelist.
- Modpack installs should handle both Modrinth `.mrpack` and CurseForge `manifest.json` formats; preserve overrides and log skipped client-only files.

## What to check first for bugs
- Empty server folders after modpack install: inspect `install-modpack.ts` copy steps (overrides, additional dirs) and cache usage; ensure download URLs and network reachability; confirm server recreation via docker service.
- File explorer missing items: see `filemanager.service.listDirectory` sorting and path resolution; ensure frontend consumes `files` response fully.

Feedback welcome: tell me if anything is unclear or missing so I can refine these instructions.
