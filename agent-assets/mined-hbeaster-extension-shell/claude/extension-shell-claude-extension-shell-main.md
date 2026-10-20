# Shell — AI assistant guide

Single-service web app: Vue 3 SPA + ASP.NET Core (.NET 10) API, served together from one container in production.

## Repo map

| Path | What it is |
| --- | --- |
| `shell/` | The shell application — frontend, backend, and the image that serves them together |
| `shell/frontend/` | Vue 3 + Vite + TypeScript SPA (create-vue layout: `src/views`, `src/components`, `src/router`, `src/stores`, `src/services`) |
| `shell/backend/` | .NET solution — API in `src/Shell.Api` (controllers), tests in `tests/Shell.Api.Tests` (xUnit) |
| `extensions/` | Independently built web-component extensions — one standalone npm package per folder (own lockfile); shell-owned `scripts/build-all.mjs` + `scripts/assemble.mjs` → `extensions/dist/<id>/` holding `package.json` + `extension.js` + `icon.svg` |
| `helm/shell/` | Helm chart: Deployment, Service, optional Ingress |
| `docs/adr/` | Architecture Decision Records (numbered, MADR-style) |
| `docs/architecture/` | Numbered architecture snapshots with mermaid diagrams |
| `docs/standards/` | Normative standards (RFC 2119 style, numbered): 001 extension consumption, 002 extension authoring & communication |
| `plans/` | Working plans for larger efforts |
| `shell/Dockerfile` | Multi-stage build: Vue dist → .NET publish → aspnet runtime (build context is the repo root) |
| `extensions/Dockerfile.extensions` | Layers built extensions onto the shell image (`FROM shell:latest`, copies `extensions/dist/` → `wwwroot/extensions/`). Build context is `extensions/`, with its own `.dockerignore` |
| `extensions/Dockerfile.extensions-image` | Packages the assembled dist as a standalone OCI image (`FROM scratch`, never run) for the k8s `image` volume type |

## Commands

Frontend (run in `shell/frontend/`):

- `npm run dev` — Vite dev server (proxies `/api` → `http://localhost:5000`)
- `npm run lint` — oxlint + ESLint (auto-fixes)
- `npm run test:unit -- --run` — Vitest, single pass
- `npm run build` — type-check + production build

Backend (run in `shell/backend/`):

- `dotnet run --project src/Shell.Api` — API on `http://localhost:5000`
- `dotnet test` — xUnit suites
- `dotnet format --verify-no-changes` — style gate (analyzers at `latest-recommended`)

Extensions:

- `npm ci && npm run build` (run in `extensions/<id>/`) — build one extension in isolation (Vite lib mode)
- `node scripts/build-all.mjs` (run in `extensions/`) — build every extension independently, then assemble `extensions/dist/` (bundles, icons, manifests)
- `node scripts/assemble.mjs` (run in `extensions/`) — assemble already-built extensions into `extensions/dist/`
- No HMR: rebuild to see changes in dev; the backend serves `extensions/dist` at `/extensions` in Development (`Extensions:RootPath`). No backend restart needed — `/api/extensions` rescans the directory on every call.

Full stack:

- `docker build -f shell/Dockerfile -t shell .` (repo root) then `docker run -p 8080:8080 shell`
- `docker build -f extensions/Dockerfile.extensions -t shell-ext extensions/` (after building `shell`) — shell + extensions image. Note the context is `extensions/`, not the repo root
- `docker build -f extensions/Dockerfile.extensions-image -t shell-extensions:latest extensions/` — the dist as a standalone OCI image, for mount mode
- `helm lint helm/shell` / `helm template helm/shell`
- `helm template helm/shell --set extensions.enabled=true --set extensions.volume.persistentVolumeClaim.claimName=x` — render the mounted-extension mode

## Conventions

- API endpoints: attribute-routed controllers under `/api/*`, one controller per resource, in `shell/backend/src/Shell.Api/Controllers/`.
- Frontend API calls go through `shell/frontend/src/services/api.ts` — add typed functions there, never `fetch` directly in components. (Extension discovery lives in `services/extensions.ts` even though it calls `/api/extensions`: `api.ts` throws, and `App.vue` calls this from `onMounted` with nothing to catch a rejection, so it soft-fails to an empty list. See ADR 0012.)
- Extensions are web components: one folder per extension in `extensions/`, describing itself in a `bc-extension` section of its own `package.json` (`type`, `tag` starting with `ext-`, optional `displayName`/`module`/`icon`/`discovery`/`services`; the id is the folder name, and there is no `extension.json`). Each is a standalone npm package (own committed `package-lock.json`) that must build in isolation and must not know about, or communicate with, any other extension — only the shell knows the installed set. They talk to the shell only via DOM `CustomEvent`s on their host element (`shell:notify` opens the shell modal). Widening this contract needs a new ADR.
- Extension discovery is `GET /api/extensions` (ADR 0012, STD 001 §5.2): the backend scans the extensions root on every request, so the folder contents are the configuration and a remounted volume needs no restart. `discovery` and `services` are carried through but not enforced — the shell mounts a hostable extension regardless. There is no `registry.json`.
- Extension delivery has two modes (ADR 0009, STD 001 §5.6): the layered `shell-ext` image (default), or a volume holding an assembled dist — one folder per extension, no index file — mounted read-only over `/app/wwwroot/extensions` via the chart's opt-in `extensions` block. Mount mode needs no shell configuration: the discovery endpoint reads whatever is at that path. The modes are mutually exclusive: a mount shadows baked extensions silently, so mount mode uses the plain `shell` image. Because the folders *are* the configuration, whatever populates the volume must clear it first — a stale folder is served and listed.
- Health endpoint is `/healthz` (used by k8s probes) — don't rename without updating the Helm values.
- Significant technical decisions get a new ADR in `docs/adr/` (next number, MADR format: Context / Decision / Consequences).
- Architecture changes get a new numbered file in `docs/architecture/` with updated mermaid diagrams; never edit old snapshots.
- Before considering work done: frontend `lint` + `test:unit` + `build` and backend `dotnet test` + `dotnet format --verify-no-changes` must pass.
