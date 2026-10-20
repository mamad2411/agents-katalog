---
name: cooper-feed-dashboard
description: >-
  Cooper's personal feed dashboard at feed.cm.xyz (Waku + CF Worker + D1) and
  the local ~/feed bootstrap. Use when Cooper asks about the daily feed
  dashboard, feed.cm.xyz, build-feed push, D1 snapshot ingest, Access gate,
  or why localhost:8654 is stale. Supplements operator-status (upstream may be
  author-locked from agent patches).
version: 1.0.0
metadata:
  hermes:
    tags: [feed, dashboard, cloudflare, d1, waku, alchemy, cm.xyz]
    category: devops
    related_skills: [operator-status, alchemy, gog]
---

# Cooper Feed Dashboard (`feed.cm.xyz`)

Class skill for the personal operator feed surface.

## Surfaces

| Surface | Path | URL |
|---|---|---|
| **Production (prefer)** | `~/git/darkmatter/feed` | **https://feed.cm.xyz** |
| Local legacy | `~/feed` + launchd | http://localhost:8654 |
| workers.dev | same Worker | https://cooper-feed.drtkmttr.workers.dev |

There is **no** pre-existing `feed.cm.xyz` DNS historically — production was cut over this session. If Cooper says "the dashboard is on the linux server / hasn't updated," check **feed.cm.xyz first**, not only localhost.

## Architecture (prod)

```
build-feed.py / Daily Feed Builder cron
    → ~/feed/src/feed-data.json  (local artifact still written)
    → bun scripts/push-feed.ts   (Bearer <REDACTED>
    → CF Worker cooper-feed
         POST /api/ingest → D1 feed_snapshot
         GET  /api/feed   → latest JSON
         ASSETS           → Waku dist/public UI
```

Auth model:
- **Browser:** Cloudflare Access on `feed.cm.xyz` — app `feed` (id `c048f55f-b168-4b57-ab99-f346dcec337e`, AUD `5479b6bd476cdb2519a525a313d4dc76295056b105e629ca378790e1c7a205c3`, team domain **`drkmttr`.cloudflareaccess.com** — note drkmttr, not darkmatter). Policies: reusable `cooper` (`allow`: emails + Cooper IP + service tokens) + app-specific `feed-agents-and-ip` (**`non_identity`**: IP + `cooper`/`openclaw` service tokens).
- **Ingest/API from agents:** send BOTH `Authorization: Bearer <REDACTED> and Access headers `CF-Access-Client-Id/Secret` (himitsu `cf-access-client-id`/`-secret`, token name `cooper`). `scripts/push-feed.ts` and the `build-feed.py` push hook already do this.
- **Access API:** the wrangler OAuth token lacks Access scopes (error 10000). Use himitsu `cloudflare-global-api-token` + `cloudflare-email` with `X-Auth-Email`/`X-Auth-Key`. Full gating recipe + the `non_identity` rule: `references/cloudflare-access-gating.md`. Reusable policies can't be edited via the app policies endpoint (error 12130) — use `/access/policies/<id>` or add app-specific policies.

## Quickops

```bash
# Health
curl -sS https://feed.cm.xyz/api/healthz
curl -sS https://feed.cm.xyz/api/meta | jq .

# Push current local snapshot
export FEED_INGEST_TOKEN=<REDACTED>
bun ~/git/darkmatter/feed/scripts/push-feed.ts \
  --from ~/feed/src/feed-data.json \
  --url https://feed.cm.xyz

# Rebuild local + auto-push (hook in build-feed.py)
FEED_INGEST_TOKEN=<REDACTED>

# Redeploy
cd ~/git/darkmatter/feed
bun run build
FEED_INGEST_TOKEN=<REDACTED>
  bun alchemy deploy ./alchemy.run.ts --stage prod --profile default --yes
```

Waku build needs **Vite 8** (`vite@^8`). Effect/alchemy peer: **effect@4.0.0-beta.102** (not beta.66).

## Alchemy deploy pitfalls (this stack)

| Symptom | Fix |
|---|---|
| `Schema.Defect is not a function` | Pin `effect` + `@effect/platform-*` to `4.0.0-beta.102` (alchemy ≥beta.100 peer) |
| Interactive "State Store out of date (expected v7, observed v8)" hang | Apply platform patch `platform/patches/alchemy@2.0.0-beta.66.patch` into `node_modules/alchemy` **and** pass `--yes` |
| Deploy OK but `feed.cm.xyz` → CF **1104 Script not found** | Custom domain row can exist while traffic 1104s; add zone route `feed.cm.xyz/*` → `cooper-feed`. Stack now declares `routes: [{ pattern: "feed.cm.xyz/*" }]` |
| workers.dev 1042 on `*.darkmatter.workers.dev` | Account subdomain is **`drtkmttr`**, URL is `https://cooper-feed.drtkmttr.workers.dev` |
| Access API 10000 Authentication error | Wrangler OAuth token often lacks Access write — create Zero Trust app in dashboard manually |

cm.xyz zone lives on **darkmatter** CF account `acb126dc2c4cf93764fa69d9bd55a3cf`.

## UI/data pitfalls

- **Transparent shadcn sidebar on Tailwind v4** — ui/sidebar uses dedicated tokens (`--sidebar`, `--sidebar-foreground`, `--sidebar-accent`, `--sidebar-border`, `--sidebar-ring` + primary variants). A theme defining only the base palette leaves `bg-sidebar` unresolved → see-through rail. `src/styles.css` defines all 8 (sidebar `240 5.9% 7.5%`, accent/border `240 3.7% 15.9%`); verify edge CSS actually changed after deploy — hash collisions can mask a no-change rebuild.
- **Sidebar must push content** — main pane uses `SidebarInset` (not a bare `div.flex-1`). Default shadcn `Sidebar` is `fixed` + gap spacer; without `SidebarInset` as the peer flex child, content looks overlaid. Prefer `collapsible="icon"`.
- **Action items are single-column response cards** — `action_needed` items render `ResponseComposer` (MC + recommended badge + freeform note → clipboard Hermes prompt). Optional curated choices via item `response_options: [{id?, label, recommended?, prompt?}]`. Blocked kanban uses recommendation `actions` (copy/secret/choice) with the same note field; choice actions reuse `ResponseComposer`. Defaults when no curated options: do hinted action / draft / snooze / skip. Details: `references/ui-ingest-and-routes.md`.
- **Never hand-write stub `~/.hermes/feed/cron-json/*.json`** — a manual triage pass writing a minimal `{generated_at, accounts, note}` shape clobbers the cron-authored full schema (`{source, run_time, items[]}`) and that dashboard section renders empty until the next cron run. Match the full schema (`operator-status` → `references/cron-json-schema.md`) and re-run `build-feed.py` after manual writes.
- **Deploy needs** `CLOUDFLARE_ACCOUNT_ID=acb126dc2c4cf93764fa69d9bd55a3cf` + `FEED_INGEST_TOKEN` + CF API token/wrangler auth. Purge `feed.cm.xyz/` cache if HTML still points at old asset hashes after deploy.
- **Access `allow_authenticate_via_warp`** — was enabled on feed + 20 internal apps (Aug 2026) to skip email OTP when WARP is connected, then **reverted** because the WARP+Tailscale dual-stack broke `.lan`/`.internal` split DNS. Do not re-enable without solving the DNS conflict first (see `warp-tailscale-coexistence` skill). Access works fine via email OTP / service tokens without WARP.
- **Cron → D1** — collectors write cron-json only; Daily Feed Builder `9acdbe616b8f` must run `build-feed.py` push for prod freshness.

## Code layout (`~/git/darkmatter/feed`)

| Path | Role |
|---|---|
| `src/worker.ts` | D1 + ASSETS + `/api/*` |
| `src/pages/*` + `src/components/dashboard.tsx` | Waku UI (dashboard fetches `/api/feed`) |
| `migrations/0001_init.sql` | `feed_snapshot`, `feed_ingest_log` |
| `alchemy.run.ts` | D1 + Worker + domain/route |
| `scripts/push-feed.ts` | Snapshot publisher |
| `README.md` | Operator notes |

## Local bootstrap still useful

Daily Feed Builder cron still generates recommendations + runs `build-feed.py` on the Mac. Production freshness = last successful **ingest**, not only last local rebuild.

**Header badge = data snapshot age** (`generated_at` from D1), not UI deploy time. If it looks stuck on an old day while you just redeployed UI, run:

```bash
export FEED_INGEST_TOKEN=<REDACTED>
export CF_ACCESS_CLIENT_ID="$(himitsu read cf-access-client-id)"
export CF_ACCESS_CLIENT_SECRET=<REDACTED>
bun ~/git/darkmatter/feed/scripts/push-feed.ts --from ~/feed/src/feed-data.json
# or: python3 ~/.hermes/scripts/build-feed.py   # now pushes after successful build
```

`build-feed.py` must call `push_remote_snapshot()` **before** `sys.exit` and falls back to `himitsu read feed/ingest-token` when cron env lacks `FEED_INGEST_TOKEN` (a prior dead-code block after `sys.exit` left prod on 2026-07-30 for days).

```bash
launchctl list | grep feed-server   # local 8654
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8654/
curl -s -o /dev/null -w "%{http_code}\n" https://feed.cm.xyz/
```

## References

- `references/feed-cm-xyz.md` — deploy transcript anchors, IDs, Access app/policy IDs
- `references/cloudflare-access-gating.md` — CF Access service-token + IP gating recipe (`non_identity` decision, headers, global-key vs OAuth token)
- `references/ui-ingest-and-routes.md` — live routes, cron→D1 path, ResponseComposer / SidebarInset contracts, WARP Access flag
- Sibling: `operator-status` (broader weekly/report; may be author-locked)
- Sibling: `alchemy` (org Alchemy deploy skill)
- Sibling: `warp-tailscale-coexistence` (WARP + Tailscale dual-stack; never thrash tunnels)
