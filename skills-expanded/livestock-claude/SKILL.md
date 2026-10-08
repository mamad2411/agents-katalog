# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

HB Livestock PWA (v2.1.0) — offline-first cattle ranch management app. **UI text is entirely in Spanish; all code, identifiers, comments, and docs are in English.** Field users have low technical experience and intermittent connectivity, so every read comes from IndexedDB and every write lands there first.

## Commands

```bash
conda activate livestock                                  # Python 3.11 env (backend)

# Backend — run from repo root
uvicorn backend.app.main:app --reload --port 8000

# Frontend — run from frontend/
npm run dev          # Vite dev server; proxies /api and /health to localhost:8000
npm run check        # svelte-kit sync + svelte-check (the only type/lint gate)
npm run build
npm run preview

# Local Supabase test stack — run from repo root
docker compose up -d        # db + PostgREST + storage-api + nginx gateway on :54321
docker compose logs -f bootstrap
```

The backend never speaks SQL — it talks HTTP to PostgREST (`/rest/v1`) and the Storage API (`/storage/v1`) — so a bare Postgres container cannot back it locally. `docker-compose.yml` runs the minimum subset of a self-hosted Supabase that does, and `backend/.env.development.example` already points at it (`SUPABASE_URL=http://127.0.0.1:54321`, login token `local-dev-token`).

Three details in that stack are load-bearing, each mapped to a failure that cost real time:

- `docker/db-init/99999999000000_local-roles.sql` sets passwords on `authenticator` and `supabase_storage_admin`, which `supabase/postgres` creates passwordless. It is mounted as a **single file into the image's `migrations/` directory**, not into `init-scripts/`: `migrate.sh` runs init-scripts *before* the migrations that create those roles, so an init-scripts hook aborts the entrypoint and the container restart-loops. Mounting the directory would hide the 53 migrations the image ships.
- The `storage` healthcheck must probe `127.0.0.1`, not `localhost` — the container resolves `localhost` to `[::1]` first and storage-api binds IPv4 only.
- On **rootless Docker**, published ports are silently dropped unless `slirp4netns` is installed and RootlessKit is pinned to `--port-driver=builtin`; with the pasta/implicit default, `docker ps` reports the mapping but no listener exists. See README §2b.

There is **no test suite and no linter config** in this repo. `npm run check` is the verification step for frontend changes; the backend has no automated checks.

In development keep `VITE_API_URL` empty so the Vite proxy handles `/api` — setting it causes CORS problems in the VS Code web viewer.

Env files are mode-specific: `frontend/.env.development` / `.env.production`, and `backend/.env.<APP_ENV>` (defaults to `development`, falls back to `backend/.env`). Copy from the `.example` files.

## Architecture

Three layers: **SvelteKit PWA (IndexedDB) → FastAPI (thin sync/photo proxy) → Supabase (PostgREST tables + Storage)**. The backend holds no database of its own; it authenticates, merges, and forwards over HTTP with `httpx`.

### Frontend (`frontend/src/lib`, `frontend/src/routes`)

- Svelte 5 runes (`$state`, `$props`, `Snippet`) — not stores, not Svelte 4 syntax.
- `db.ts` — Dexie schema, currently at **version 4**. Sync flags are numeric `0|1` (not booleans/strings) so they can be indexed; any field queried with `.where()` must exist in the version's index list or Dexie throws `SchemaError`. Adding a queryable field means adding a new `db.version(n)` block.
- `store.ts` — the only place that writes business records. Pattern: build record → `synced: 0` → `db.<table>.add/update`. **Deletes are always soft** (`deleted: 1, synced: 0`); rows are physically removed only after the sync engine confirms the server took them.
- `sync.ts` — the sync engine, and the most subtle file in the repo. Push-then-pull, last-write-wins on `updated_at`. Load-bearing invariants, each mapped to a past bug:
  - Photos sync *before* tables, so animal records can pick up the resulting public URL.
  - Photos have **no remote table** — they exist only as Storage objects, so they never pass through the table sync and its soft-delete cleanup. Deleting one is a separate purge (`purgeDeletedPhotos()`) that calls `DELETE /api/photos/{id}` and then drops the local row; it runs in a `finally` so it fires even when there is nothing to upload. Omitting it is what once left deletions pending forever.
  - Remote data overwrites a local row **only when `local.synced === 1`** — a row edited during a sync keeps the local version.
  - Content is compared field by field (`hasRecordChanged`), not just by timestamp, because rows can be edited directly in Supabase.
  - `apiGetSyncState()` is a cheap version/modified_at probe used to skip full pulls (Render/Supabase free tiers).
  - Polling (60 s) is gated on the Page Visibility API; it also syncs immediately on window focus and on the `online` event. Consecutive failures back off exponentially to a 16-minute cap, which `syncAll(true)` deliberately bypasses.
- `api.ts` — every HTTP call; attaches the Bearer token from `localStorage['auth_token']`.
- Pages load data in `onMount` and re-read on the `sync-complete` window event. There is no global store and no live-query layer — that event *is* the reactivity mechanism for post-sync refresh.
- Route group `(app)` is auth-guarded in `+layout.ts` (`ssr = false`, redirect to `/login`); it also mounts `initSync()`.
- Domain logic lives in plain `lib/*.ts` modules computed from IndexedDB (`genealogy.ts`, `health.ts`, `missingAnimals.ts`, `recorridos.ts`) — no backend endpoints back these views.

### Backend (`backend/app`)

- `routers/sync.py` — `POST /api/sync/{table}` (push + receive merged), `GET /api/sync/pull`, `GET /api/sync/state`. Sync version is in-memory, so a restart forces clients into a full sync. On any Supabase failure the router **returns the client's own records back** rather than erroring, so offline clients never lose data.
- `services/supabase.py` — all PostgREST and Storage access. `services/sheets.py` is Supabase-backed despite the name (table/PK maps live there). Google Sheets/Drive are fully gone — no `credentials.json`.
- `main.py` — `GET /health/db` is the only endpoint that touches Supabase outside the sync/photo flows; `/health`, `/`, and `/api/sync/state` all answer from memory. An external daily cron calls it to keep the free-tier Supabase project from pausing after ~7 days of inactivity (see README). Don't "optimize" it into a memory-only check.
- `auth.py` — single shared secret in `AUTH_TOKEN`, compared with `hmac.compare_digest`. Suitable only for the small trusted team this app targets.

### Data model

Per-table primary keys, used identically on both sides: `animals.animal_id`, `health.salud_id`, `reproduction.reproduccion_id`, `observations.observacion_id`, `sales.venta_id`, `recorridos.entry_id` (plus a non-unique `recorrido_id` grouping the animals seen in one patrol). IDs are `PREFIX-<8 hex>` via `generateId()` (`ANI`, `SAL`, `REP`, `OBS`, `VEN`, `REC`/`RCE`, `PHO`).

Every business record carries `SyncMeta`: `synced`, `deleted`, `created_at`, `updated_at`, `created_by`. Field names are `snake_case` everywhere — TS interfaces, Pydantic models, and Supabase columns must stay aligned; `frontend/src/lib/types.ts` and `backend/app/models.py` mirror each other. Enum *values* are Spanish strings (`'Vaca'`, `'Vivo(a)'`, `'Desparasitación'`) matching what is stored in Supabase.

`AnimalPhoto.photo_url` holds the **Supabase Storage public URL**; the animal's own `foto_url` column mirrors it, and that mirror is what carries a photo (or its removal) to the other devices. Photos live as base64 `data_url` in IndexedDB until uploaded (compressed to 800px / JPEG 70% in `compressImage.ts`); the bucket must be publicly readable.

Design assumption throughout: <200 animals, so full-table sync is fine — no pagination or delta sync.

## Conventions

- Commit messages follow the `.github/skills/conventional-commit-messages` skill (Conventional Commits, imperative, English).
- Update `CHANGELOG.md` (Keep-a-Changelog format) for user-visible changes; the version appears in `frontend/package.json`, `README.md`, and `backend/app/main.py`.
- Mobile-first Tailwind 4 (no config file — `@import 'tailwindcss'` in `app.css`); `max-w-lg` containers, large touch targets, safe-area vars `--sab`/`--sat`.
- Dates are stored ISO and entered through the shared `DateField` (`DD/MM/YYYY` with native picker fallback); photos open through the shared `photoLightbox` host.

## Stale docs

`.copilot-context.md` describes React 19 + Google Sheets/Drive and is **obsolete** — do not follow it. `ARCHITECTURE.md` and `README.md` are current. `suggests.md` holds open product ideas (notably: deleting a reproduction record does not cascade to its calf animal).