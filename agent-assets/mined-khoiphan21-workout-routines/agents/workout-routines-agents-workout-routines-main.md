# AGENTS.md

## Cursor Cloud specific instructions

This is a VitePress static documentation site for a workout program. There is one service: the VitePress dev server.

## Hevy API

- **API docs:** https://api.hevyapp.com/docs/
- **API key:** Set `HEVY_API_KEY_KHOIPHAN21` in the environment, or copy [`.env.example`](.env.example) to `.env.local` (gitignored) and add your key there. Scripts load `.env.local` automatically when the env var is unset.

- **Dev server:** `npm run docs:dev` (port 5173 by default). Supports hot-reload for `.md` and `.mts` config changes.
- **Push to Hevy:** `npm run hevy:push -- <program>` — program path required (e.g. `push-pull-homegym`). Validates bundle, resolves custom exercises by **mapping id first** (not cache title alone), reconciles routine IDs, then upserts. **Does not POST new exercises** unless they are in `mapping.toCreate` or you pass `--allow-create`. Auto-fetches exercise cache unless `--no-fetch`. Requires `HEVY_API_KEY_KHOIPHAN21` or `HEVY_API_KEY`.
- **Validate bundle:** `npm run hevy:validate -- <program>` — checks enums, duplicate Hevy titles for customs, mapping/title consistency, and cache coverage (reads `libs/hevy/cache/exercise-templates.json` only).
- **Sync all khoiphan21 programs:** `npm run hevy:sync-khoiphan21` — account duplicate check, validate each program, push with shared in-memory template index, post-push cache refresh. Flags: `--validate-only`, `--push-only`, plus forwarded push flags.
- **Pull routines from Hevy:** `npm run hevy:fetch` then `npm run hevy:pull-routines` — refreshes `libs/hevy/cache/*` and rewrites each local `hevy/routines.json` snapshot from live Hevy routines by tracked routine ID and matching folder. No API writes.
- **CI:** On pull requests to `main`, workflow [`.github/workflows/hevy-sync-khoiphan21.yml`](.github/workflows/hevy-sync-khoiphan21.yml) validates all khoiphan21 bundles only (no API push). Push to Hevy is manual via the safe workflow below.
- **Map exercises:** `npm run hevy:map -- <program>` — updates `hevy/mapping.json` and `hevy/status.md`. Custom slugs use [`libs/hevy/template-index.mjs`](libs/hevy/template-index.mjs) (fails on ambiguous duplicate titles). Optional `--fetch`.
- **Push flags:**
  - `--dry-run` — no API writes
  - `--fetch` — refresh exercise cache before push
  - `--no-fetch` — require on-disk cache (errors if missing)
  - `--allow-create` — allow POST for any custom not resolved (default: only slugs in `mapping.toCreate`)
  - `--force-create <slug>` — recreate one custom (new Hevy id)
  - `--recreate-routines` — clear local routine ids before reconcile; requires `--i-know-recreate`
  - `--allow-duplicate-routines` — skip error when Hevy folder has multiple routines with the same title
  - `--skip-reconcile` — skip Hevy folder/id sync
- **Safe workflow:**

```bash
npm run hevy:fetch-exercises
npm run hevy:map -- <program>
npm run hevy:validate -- <program>
npm run hevy:list-duplicates -- --fetch
npm run hevy:push -- <program>   # add --allow-create if mapping has toCreate
# or: npm run hevy:sync-khoiphan21
```

- **List folder routines:** `npm run hevy:list-folder -- <program>` — KEEP vs DELETE for orphan cleanup (Hevy has no DELETE routine API).
- **List duplicate exercises:** `npm run hevy:list-duplicates` (`--fetch`, `--verbose`) — DELETE ids for manual cleanup in the Hevy app; RECREATE section for missing keepers.
- **Troubleshooting duplicates:** Regenerating `routines.json` without `preserveRoutineIds()` causes orphan routines. Push **fails** instead of creating a second routine when a same-title routine already exists in the folder. After deleting routines on Hevy: `npm run hevy:push -- <program> --recreate-routines --i-know-recreate`.
- **Renaming a custom exercise:** update `custom-exercises.json`, re-map, delete old template in Hevy manually; push will not create a duplicate title without `--allow-create`.
- **Invalid muscleGroup:** Use Hevy enums (`lats`, `upper_back`, not `back`). Validation fails locally before push.
- **Hevy cache:** `libs/hevy/cache/exercise-templates.json`. Stale cache warning after 24h (`HEVY_CACHE_MAX_AGE_MS` to override). **Account mapping:** `libs/hevy/account/khoiphan21/exercise-mapping.json`.
- **Build:** `npm run docs:build` — outputs to `.vitepress/dist`.
- **Preview built site:** `npm run docs:preview` — serves the production build locally.
- **CI (PRs to main):** `hevy-sync-khoiphan21` validates all khoiphan21 Hevy bundles; `deploy-docs` builds the site on push to main.
- The VitePress config at `.vitepress/config.mts` auto-generates sidebar navigation from all `.md` files in the repo (excluding `node_modules`, `.git`, `.github`, `.cursor`, `dist`).
- `index.md` is a symlink to `README.md` — this is required for the VitePress dev server to serve the homepage at `/`.
