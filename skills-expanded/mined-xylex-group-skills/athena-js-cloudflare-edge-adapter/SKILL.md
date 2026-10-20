---
name: athena-js-cloudflare-edge-adapter
description: >
  Implement, debug, document, or test the Athena JS Cloudflare edge adapter: D1/R2
  drop-in backends on createClient, hybrid remote auth/billing, D1 SQL compiler,
  capabilities, and runtime mode façades. Use for createClient({ db: { d1 }, storage: { r2 } }),
  createCloudflareClient, createAthenaRuntime, createAthenaFromWorkerEnv, gatewayTransport
  injection, cloudflare-edge capabilities, rowid-bounded deletes, sparse insert batches,
  hybrid billing URL routing, ADR 0015–0020, packages/athena-js/src/cloudflare/**, or
  examples/cloudflare. Use when the user runs /athena-js-cloudflare-edge-adapter.
  Prefer this over generic $athena-js / $athena-jsm when the task is edge/D1/R2-specific.
  Distinguish from apps/cloudflare-d1-proxy (server-side proxy) and $athena-auth-cloudflare-worker
  (auth Worker deploy).
---

# Athena JS Cloudflare edge adapter

Work from `packages/athena-js` in the Athena monorepo. Edge is an **execution backend** on the single `createClient` materializer (ADR 0001 / 0015 / 0016), not a second client product.

## Source of truth (read in order)

1. `packages/athena-js/docs/adr/README.md` — catalog; cluster **0015–0020**
2. `packages/athena-js/docs/cloudflare-edge-local.md` — operator guide
3. `packages/athena-js/src/v3-client.ts` — `db.d1` / `storage.r2` materialization
4. `packages/athena-js/src/cloudflare/**` — transport, SQL, R2, runtime façades
5. `packages/athena-js/package.json` export `./cloudflare`
6. `packages/athena-js/test/cloudflare-*.test.ts`
7. `packages/athena-js/examples/cloudflare/**`

If docs and source disagree, trust **source + tests**, then update ADRs/docs.

Detailed contracts: [references/edge-surface.md](references/edge-surface.md), [references/adr-map.md](references/adr-map.md).

## Topology (do not confuse)

| Path | When | Entry |
| --- | --- | --- |
| **Edge-local** | App Worker owns D1/R2 | `createClient({ db: { d1 }, storage: { r2 } })` |
| **Hybrid** | Local D1/R2 + remote Athena root | same + `url` / `key` |
| **Gateway HTTP** | Remote athena_rs | `createClient({ url, key })` |
| **D1 proxy** | Server-side Athena → D1 | `apps/cloudflare-d1-proxy` (not this skill’s materializer) |

## Canonical construction — only `createClient`

**Every** path materializes through root `createClient`. No second core.

```ts
import { createClient } from '@xylex-group/athena'

// Gateway
createClient({ url: env.ATHENA_URL, key: env.ATHENA_API_KEY })

// Edge (nested)
createClient({
  db: { d1: env.DB, sessionMode: 'first-unconstrained' },
  storage: { r2: env.FILES, prefix: 'app/' },
})

// Edge (top-level aliases folded into db/storage)
createClient({ d1: env.DB, r2: env.FILES, storagePrefix: 'app/' })

// Hybrid
createClient({ db: { d1: env.DB }, url: env.ATHENA_URL, key: env.ATHENA_API_KEY })

// Switch when both D1 and URL exist
createClient({
  d1: env.DB,
  url: env.ATHENA_URL,
  key: env.ATHENA_API_KEY,
  mode: 'auto', // edge | gateway | auto
  prefer: 'edge', // when both
})
```

### Façades (map config only — must call `createClient`)

| API | Role |
| --- | --- |
| `createCloudflareClient` | maps `{ d1, r2 }` → `createClient` |
| `createAthenaRuntime` | maps runtime shape → `createClient` + `{ mode, client }` |
| `createAthenaFromWorkerEnv` | maps `env.DB` / `FILES` / `ATHENA_*` → `createClient` |
| `resolveAthenaExecutionMode` | pure mode helper (also used inside `createClient`) |

Never reimplement fluent builders or transports inside façades.

## Implementation map

| Concern | Path |
| --- | --- |
| Binding materialization | `src/v3-client.ts` → `materializeEdgeBindings` |
| D1 gateway transport | `src/cloudflare/d1/transport.ts` |
| D1 SQL compiler | `src/cloudflare/d1/sql.ts` |
| D1 runner / batch | `src/cloudflare/d1/runner.ts` |
| Postgres→SQLite rewrite | `src/cloudflare/d1/sql-rewrite.ts` |
| R2 L3a storage | `src/cloudflare/r2/storage.ts` |
| Capabilities | `src/cloudflare/capabilities.ts` |
| Edge façade | `src/cloudflare/edge-client.ts` |
| Runtime / Worker env | `src/cloudflare/runtime.ts` |
| Structural types | `src/cloudflare/types.ts` |
| Fluent limit/offset on mutations | `src/client.ts` (update/delete payloads) |
| Delete payload fields | `src/gateway/types.ts` → `AthenaDeletePayload` |

## Hard rules

### Drop-in (ADR 0016)

- Prefer `createClient({ db: { d1 }, storage: { r2 } })` in new code and docs.
- `createCloudflareClient` only maps top-level `d1`/`r2` → service options.
- Strip `r2` / `prefix` from HTTP storage options when building internal storage config.

### Hybrid routing (ADR 0018)

- D1 sentinel `https://athena.local/cloudflare-edge` is **not** a real HTTP base.
- When `db.d1` + remote `url`: set `billing.url` to remote root (unless overridden).
- Billing must never hit `athena.local` in hybrid tests.
- `storage.objects` true if **R2 or** remote root enables storage; `storage.local` only with R2.

### D1 SQL (ADR 0017)

- Compile gateway payloads to SQLite; fail with `D1SqlCompileError` codes.
- Mutation bounds: copy `limit`/`offset` onto update and delete payloads from builder state.
- Bounded mutations: rowid IN (SELECT rowid ... LIMIT/OFFSET).
- `.range()` / `.limit()` without order must not fall through to unbounded DELETE or UPDATE.
- Sparse multi-row inserts → batch of single-row statements; sum `meta.changes` for count.
- stripNulls default true on returned rows (omit null-valued keys); honor strip_nulls: false.
- head: true on insert/upsert suppresses RETURNING; count from meta.changes.
- Select aliases: use quoteSelectColumnsExpression (`user_id:id` -> `"id" AS "user_id"`).
- Unfiltered update/delete rejected on edge.
- RPC unsupported on D1 transport.

### Capabilities (ADR 0020)

- Always set honest `client.capabilities`.
- Edge default layers: `query` + `flatCrud` true; `rpc` / `relations` false; `findManyAst` false until implemented.
- `withContext` preserves capabilities.

### Mode resolution (ADR 0019)

- `auto`: only D1 → edge; only URL → gateway; both → `prefer` (default **edge**).
- Env: `ATHENA_EXECUTION_MODE`, `ATHENA_EXECUTION_PREFER`.
- Worker keys: `DB`, `FILES`, `ATHENA_URL`, `ATHENA_API_KEY`, `ATHENA_AUTH_URL`, `ATHENA_CLIENT`.

### What not to do

- Do not invent a second client core or fork fluent API for edge.
- Do not put D1/R2 construction into Next façades (they only resolve context).
- Do not treat edge-local as multi-tenant Athena client registry.
- Do not assume PostgreSQL SQL works unchanged on D1.
- Do not confuse with `apps/cloudflare-d1-proxy` or auth Worker deploy skills.

## Workflow for changes

1. Classify: drop-in config, transport/SQL, hybrid routing, capabilities, runtime façade, or docs/ADR.
2. Read the matching ADR(s) 0015–0020.
3. Change the owning file from the implementation map (one seam).
4. Add/adjust focused `test/cloudflare-*.test.ts` (and query-builder tests if payload shape changes).
5. Keep `docs/cloudflare-edge-local.md` + ADRs aligned when contracts change.
6. Examples under `examples/cloudflare/` should show drop-in `createClient` where possible.

## Validation

Narrowest first, from `packages/athena-js`:

```bash
pnpm exec tsx --test test/cloudflare-client.test.ts test/cloudflare-transport.test.ts test/cloudflare-d1-sql.test.ts test/cloudflare-runtime.test.ts
```

Also run when touching fluent payloads:

```bash
pnpm exec tsx --test test/query-builder-behavior.test.ts
```

Package-facing: `pnpm typecheck` then `pnpm check:all` as needed.

## Related skills

| Skill | Use instead when… |
| --- | --- |
| `$athena-js` / `$athena-jsm` | General runtime, not edge-specific |
| `$athena-js-v3-migration` | v2→v3 constructor migration |
| `$athena-client-instantiation-migration` | App wrapper → published adapters |
| `$athena-storage` | Server `/storage/*` Rust routes |
| `$athena-auth-cloudflare-worker` | Auth Worker Wrangler/deploy |
| `$athena-workspace-map` | Which package/app owns the file |
| `$wrangler` / `$workers-best-practices` | Wrangler/Workers platform hygiene |
