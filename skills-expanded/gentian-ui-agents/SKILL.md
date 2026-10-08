# AGENTS.md — Gentian shell development

## Project overview

`gentian-ui` is the kernel shell for Gentian OS — login hub, desktop/mobile bases, app
launcher, and iframe window host. It dogfoods
[gentian-app-template](https://github.com/gentian-org/gentian-app-template) — same
backend/frontend/chart layout and security modules. This repo is the **kernel shell**
instance; see template `docs/AGENTS.md` for catalogue-app specifics (`profile/`, AppProfile
publish flow). See [README.md](README.md) for scope and layout.

## Build & deployment — CI/GitOps only

* CI builds the `gentian-portal-api`/`gentian-portal-web` images via
  `.github/workflows/gentian-portal.yaml` on pushes to `develop`. Cluster rollout is automatic
  via Argo CD Image Updater on the `gentian-portal` Application in `gentian-deployments`.
* **Do not build/push images or deploy/patch the cluster yourself** — let CI and Argo CD
  reconcile. Deleting a stuck resource to speed up reconciliation is fine; hand-patching a
  replacement is not.

## Security & licensing

* **Never commit secrets** (OIDC client secrets, API keys) — see [docs/security.md](docs/security.md).
* **Respect third-party license terms** when adding dependencies or vendoring code.

## Directory map

| Path | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI entrypoint |
| `backend/app/core/config.py` | Settings from environment |
| `backend/app/core/auth.py` | OIDC JWT validation |
| `backend/app/core/tenant.py` | JWT tenant/realm context (kernel multi-realm) |
| `backend/app/core/authz.py` | ReBAC PEP hook (OpenFGA / AuthZEN) |
| `backend/app/core/logging_middleware.py` | M7 log redaction |
| `backend/app/db/session.py` | Tenant-scoped DB session stub |
| `backend/app/api/routes/` | HTTP routers (`session`, `apps`, `prefs`) |
| `frontend/src/auth/` | OIDC provider, RequireAuth, token helpers |
| `frontend/src/pages/` | Login, Desktop, Mobile |
| `frontend/design-system/` | Brand tokens (`gentian-theme.css`) — vendored |
| `frontend/public/fonts/` | Self-hosted Hanken Grotesk + Commit Mono |
| `frontend/public/tiles/` | App launcher tile SVGs |
| `frontend/src/shell/` | App menu, background, launcher |
| `frontend/src/stores/` | Zustand client state |
| `frontend/src/api/client.ts` | Typed fetch + Bearer token |
| `frontend/src/router.tsx` | TanStack Router |
| `chart/` | Kernel Helm (Gateway API HTTPRoute) |

## Add an API endpoint

1. Create `backend/app/api/routes/<feature>.py` with an `APIRouter`.
2. Register it in `backend/app/main.py`.
3. Protect routes with `Depends(get_current_user)`.
4. Use `check_permission()` or `require_permission()` for sensitive ops (M22).

## Add a React page

1. Add component under `frontend/src/pages/`.
2. Register route in `frontend/src/router.tsx` under the `shell` layout if auth required.
3. Load server data with TanStack Query via `api/client.ts`.
4. Use Zustand in `frontend/src/stores/` for local UI state.

## Edge routing

Production uses **Gateway API** (`chart/templates/httproute.yaml`) on
`kernel-public-gateway`. Routes `/api`, `/healthz`, `/readyz` → API; `/` → web.
See [docs/security.md](docs/security.md).

## Local dev

```bash
docker compose -f docker-compose.dev.yaml up --build
```

- UI: http://localhost:5173
- API: http://localhost:8000/docs

`AUTH_DISABLED=true` and `VITE_AUTH_DISABLED=true` skip OIDC locally.

See [docs/security.md](docs/security.md) and [docs/architecture.md](docs/architecture.md).
