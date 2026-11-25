---
name: athena-workspace-map
description: >
  Map Athena monorepo surfaces: which folder owns which package, app, crate, or service,
  and where published npm/Cargo names resolve on disk. Use when deciding if work belongs in
  packages/athena-js vs packages/athena-auth-ui vs apps/* vs services/* vs crates/* vs consumer
  repos (e.g. speedrun-formations); when routing Linear issues to the correct codebase;
  when answering "where is X" or "which package owns Y". Use when the user runs /athena-workspace-map.
---

# Athena workspace map

Route work to the **owning path** before editing. Prefer this skill for placement questions; use `athena-architecture` for runtime request flow and crate boundaries inside the Rust server.

## Decision order (issue / TODO routing)

1. **Does the issue cite a consumer path** (e.g. `src/components/...` under SuitsFinance/speedrun-formations)?  
   → Work in that **app repo**, not under `packages/*` unless the bug is in a published export.
2. **Does the import start with `@xylex-group/athena` or `@xylex-group/athena/*`?**  
   → `packages/athena-js` (published package name `@xylex-group/athena`).
3. **Auth UI components, pages, tables, HeroUI surfaces, `@xylex-group/athena-auth-ui`?**  
   → `packages/athena-auth-ui` (local `package.json` name may be `athena-auth-ui`; treat as auth-ui package).
4. **Cloudflare auth worker / Wrangler container for auth?**  
   → `services/athena-auth`.
5. **Rust gateway, SQL, billing, storage routes, OpenAPI for server?**  
   → repo root `src/`, `crates/`, `sql/`, root `openapi*.yaml`.
6. **Operator studio, docs site, marketing, desktop, edge workers?**  
   → `apps/<name>`.

When unsure, open the file with the symbol and walk **one import hop** to the package boundary. Do not move consumer wrappers into packages unless the user asks for a library extraction.

## Top-level layout (this repo: `athena`)

| Path | Owns | Notes |
| --- | --- | --- |
| `src/` | Root Rust runtime / server + SDK surface (`athena_rs`) | Primary server binary surface |
| `crates/` | Focused Rust workspace crates | See `crates/MANIFEST.md` |
| `packages/` | Published / consumable JS (and related) SDKs | Not Cargo members |
| `apps/` | Product/operator surfaces | See `apps/MANIFEST.md` |
| `services/` | Deployable workers / operators outside `apps/` | e.g. auth worker |
| `sql/` | Provision / migration SQL | Server-owned data contracts |
| `docs/` | Repo-local architecture & workspace docs | Not the Fumadocs product app |
| `examples/`, `benches/`, `tests/` | Samples, benches, integration | |
| `openapi.yaml`, `openapi-wss.yaml` | HTTP / WSS contracts | Root |

Canonical generated maps:

- `docs/workspace-manifest.md`
- `apps/MANIFEST.md`
- `crates/MANIFEST.md`
- Root `README.md`

Refresh manifests via workspace doc generators when layout changes (`athena-workspace-docs` skill / `scripts/generate_workspace_docs.py`).

## npm / JS packages (`packages/`)

| Disk path | Typical import / name | Responsibility | Put work here when… |
| --- | --- | --- | --- |
| `packages/athena-js` | `@xylex-group/athena`, subpaths `/react`, `/next`, `/cloudflare`, … | JS client, auth client, query builders, React query client, **edge D1/R2 adapter**, generator CLI | Client construction, fluent query API, React hooks, Cloudflare edge drop-in (`db.d1` / `storage.r2`), SDK types |
| `packages/athena-auth-ui` | auth UI package / `@xylex-group/athena-auth-ui` | Auth/settings/workspace UI, tables, HeroUI implementations, examples | UI components, auth pages, billing UI cards, TanStack helpers under auth-ui |
| `packages/better-auth-athena` | `@xylex-group/better-auth-athena` | Better Auth adapter bridge | Better Auth + Athena adapter |
| `packages/create-athena-app` | `create-athena-app` | Scaffold templates | Template provider wiring, starter QueryClient patterns |
| `packages/athena-py` | Python package tree | Python client surface | Python SDK only |

### React query-client ownership (common confusion)

| Symbol / pattern | Owner |
| --- | --- |
| `createAthenaQueryClient`, `AthenaQueryClient`, `AthenaQueryClientProvider`, `useAthenaQueryClient` | **`packages/athena-js`** → `src/react/` (`@xylex-group/athena/react`) |
| App wrapper named `AthenaReactProvider` that memos a client and wraps `AthenaQueryClientProvider` | **Consumer app** (e.g. speedrun-formations `src/components/athena-query-provider.tsx`) |
| `getAthenaQueryClient` / TanStack helpers in auth UI | **`packages/athena-auth-ui`** (UI-layer TanStack), not the Athena-native query client |

**SUI-2019-class work** ("isolate query-client construction at provider boundary" with `userId` in an app `AthenaReactProvider`) → **consumer repo**, using APIs from **`@xylex-group/athena`**. Not athena-auth-ui unless the bug is in UI package code.

## Apps (`apps/`)

| Disk path | Package / kind | Responsibility |
| --- | --- | --- |
| `apps/web` | `athena-studio` | Operator web app |
| `apps/docs` | `athena-docs` | Product documentation (Fumadocs / OpenNext) |
| `apps/desktop` | Tauri / desktop | Desktop shell around runtime |
| `apps/marketing` | marketing monorepo | Marketing site(s) |
| `apps/cloudflare-athena` | `athena-cloudflare-athena` | Edge container wrapper Worker |
| `apps/cloudflare-d1-proxy` | `athena-cloudflare-d1-proxy` | **Server-side** D1 proxy for athena_rs (not the JS edge materializer) |
| `apps/wss-gateway` / `apps/athena-wss-gateway-rust` | WSS gateway | Protocol adapter |
| `apps/cdc-api` | compose stack | CDC-related API stack |

## Services (`services/`)

| Disk path | Responsibility |
| --- | --- |
| `services/athena-auth` | Athena Auth Cloudflare Worker (deployable auth) |
| `services/athena-operator` | Operator service surface |

## Rust crates (summary)

- All under `crates/athena-*` plus root `src/` / workspace `Cargo.toml`.
- Prefer `crates/MANIFEST.md` and `athena-architecture` / `athena-rs` for which crate owns a route domain (billing, storage, chat, gateway, etc.).
- Do **not** put JS client construction logic in Rust crates.

## External consumer repos (same org, not this monorepo)

Issues filed against apps that **depend on** Athena packages still live in the app:

| Repo (example) | Role | Relationship |
| --- | --- | --- |
| `SuitsFinance/speedrun-formations` | Product app | Imports `@xylex-group/athena`; local providers/wrappers |
| Other Suits / Xylex apps | Consumers | Same rule: app path first, package only if export is wrong |

Local clones may be empty or missing; verify with `gh` / remote before claiming "not in monorepo".

## Agent procedure

When the user asks where something lives or which package to edit:

1. Parse issue **Source Location**, import path, and symbol name.
2. Match against tables above.
3. Answer with:
   - **Owning path** (disk)
   - **Published name** (if any)
   - **What not to touch**
   - **One-line reason**
4. If work spans package + consumer (e.g. missing SDK API + app usage), split: package PR first, then consumer.

## Anti-patterns

- Editing `packages/athena-auth-ui` for `@xylex-group/athena/react` bugs.
- Editing `packages/athena-js` for a consumer-only `AthenaReactProvider` TODO that only wraps the SDK.
- Treating `apps/docs` content as the only architecture source of truth for crate layout (`docs/` + manifests are authoritative for workspace maps).
- Assuming sibling folders under `~/documents/github/*` are always full clones.

## Related skills

- `athena-architecture` — runtime modes, crate ownership for server behavior
- `athena-js` / `athena-jsm` — JS client usage
- `athena-js-cloudflare-edge-adapter` — D1/R2 drop-in on `createClient`, hybrid, ADRs 0015–0020 (`packages/athena-js/src/cloudflare/**`)
- `athena-auth-ui` — UI package work
- `athena-rs` / `athena-rs-sdk` — Rust server vs Rust client SDK
- `athena-workspace-docs` — regenerating MANIFEST / README maps

## Reference file

For a denser checklist used during routing, see [references/package-map.md](references/package-map.md).
