# packages/spin

The dev-stack orchestrator (`@calibra/spin`). A tsdown-built TypeScript package: a `commander` CLI, an Ink terminal TUI, a bundled-React web panel, and the core orchestration engine. Replaces the legacy `scripts/spin/*.mjs`. See [README.md](README.md) for the operator guide.

## Build / layout

- **Two tsdown builds** (`tsdown.config.ts`): a node build (`cli.ts` + `agent/server.ts`, React/ink external, `fixedExtension: false` → `.js`) and a browser build (`agent/client.tsx`, `deps.alwaysBundle: [/.*/]` so **React 19 is bundled in** — never a CDN). The browser bundle must keep zero `esm.sh`/CDN references; CI asserts this.
- `src/core/*` — framework-agnostic engine. `src/commands/*` — one `register*` per CLI command. `src/agent/*` — the panel (server = node, client/components/hooks = browser). `src/tui/*` — the Ink TUI.

## Rules

- **Append-only ROLES.** The `ROLES` table in `core/ports.ts` is a frozen contract — existing `.claude/spin/<slug>.json` metas resolve by offset. Only ever **append** a role; never reorder/insert. `ports.test.ts` pins it.
- **Catalog is the source of truth.** `core/catalog.ts` (`SERVICES`, `DEMO_TENANTS`, `DB_ROLES`) drives the Caddyfile, snapshot, probes, and handoff. Add/change a service there, not in scattered renderers. `DEMO_TENANTS` must match `apps/api/database/seeders/main_seeder.ts` or tenant URLs 404.
- **Render loudly.** Config is rendered with type-safe template literals + `requirePort()` (throws on a missing port) — no string `{{TOKEN}}` engine, no silent empty values. A null port must abort the spin, not emit a broken line.
- **One snapshot contract.** `core/snapshot-types.ts` is **node-free** (`import type` only) so the browser bundle can consume it. The CLI, TUI, and panel all render `buildSnapshot()` — never fork a second service-shape.
- **No bare-db / always `postgres_admin`.** Migrations + seed run on `--connection=postgres_admin` (BYPASSRLS). Seeding on the RLS-enforced `calibra_app` role silently writes zero rows. See [[feedback_no_bare_db_tenant_queries]].
- **Panel binds 127.0.0.1.** The panel exposes destructive actions (reseed/migrate/restart) — never bind 0.0.0.0.
- **Secrets live in the meta, chmod 0600.** `appKey`/`glitchtipSecretKey`/`meiliMasterKey` are flat top-level fields (legacy-compatible); forward-migration only fills holes, never reallocates ports/secrets.
- **Canonical tenant URLs = Caddy TLS** (`<shop>.admin.<slug>.spin.localhost`); direct-port is a fallback. Keep the handoff, panel, env (`ADMIN_URL_TEMPLATE`/`CONSOLE_URL`), and impersonation on the one scheme.

## Deps

Only `commander` + `ink` are spin-specific (catalog). Everything else uses Node built-ins on purpose (custom logger, not pino; type-safe render, not yaml; `child_process`, not execa; `crypto.randomUUID`, not nanoid). Adding a dep needs sign-off per the repo [AGENTS.md](../../AGENTS.md).
