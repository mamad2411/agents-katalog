---
name: athena-rs
description: >
  Server/runtime playbook for the Athena Rust monorepo (`athena_rs`): logging client vs
  X-Athena-Client tenant DBs, bootstrap catalog merge, chat session auth logging, gateway
  request paths, AppState, schema self-heal, and catalog load-failure penalties. Use when
  debugging or changing athena-rs server code, postgres client registry, athena_logging,
  chat/WSS auth, bootstrap warnings, or auto-disable of catalog clients. Use when the user
  runs /athena-rs. Prefer athena-rs-sdk for the public Rust client SDK only; prefer
  athena-architecture for high-level crate maps; prefer athena-storage/athena-billing for
  those domains.
---

# Athena RS (server runtime)

Work from **request path + pool ownership** first. Wrong-database bugs (writes/self-heal on
`athena_logging` when the tenant DB was intended) are a top failure mode.

Current workspace: `athena` monorepo, package `athena_rs`.

## Sibling skills (do not collapse scopes)

| Skill | Use for |
|---|---|
| **athena-rs** (this) | Server handlers, bootstrap, registry, logging vs tenant DB, chat auth log, catalog penalties |
| `athena-rs-sdk` | Public `AthenaClient` / fluent CRUD / gateway request types |
| `athena-architecture` | Crate/runtime mode map, deployment ownership |
| `athena-storage` | `/storage/*`, S3 catalog |
| `athena-billing` | billing routes and Mollie sinks |
| `athena-auth-*` | Auth product / UI / worker, not generic gateway chat |

## Source of truth order

1. Live code for the seam (search first, then read)
2. `src/bootstrap/mod.rs`, `src/bootstrap/postgres_init.rs`
3. `src/config.rs` + `config.yaml` (gateway section; env `ATHENA_GATEWAY_*`)
4. `src/data/clients.rs` (`athena_clients` catalog on logging DB)
5. `src/api/chat/**` for chat/WSS session auth
6. `sql/provision.sql` + `crates/athena-provisioning` for **tenant** schema
7. `sql/athena_clients.sql` and gateway log SQL for **logging** schema
8. Docs under `docs/architecture_*.md` only after code

If docs and code disagree, **code wins**.

## Hard rule: logging DB vs tenant DB

### Logging client (`gateway.logging_client`, often `athena_logging`)

Control-plane + observability. Typical residents:

- `athena_clients` (catalog of tenants / URIs / `is_active` / `is_frozen` / metadata)
- `athena_client_configs`
- `gateway_request_log` / `gateway_operation_log`
- `client_statistics` / `client_table_statistics`
- client pressure / connection samples
- pipeline templates + `pipeline_step_log`
- daemon / ops tables that key off the control plane

Resolve pool via `state.logging_client_name` + `pg_registry.get_pool(...)`.

### Tenant / `X-Athena-Client` (e.g. `suits-formations`)

Application schema from provisioning (`sql/provision.sql`, `EXPECTED_TABLES`). Includes auth
product tables, chat tables, **and** `athena.chat_session_auth_log`.

Resolve pool via request client name (`required_client_name` / header) + `pg_registry.get_pool(client)`.

### Never put these on the logging DB

- `athena.chat_session_auth_log` — write + runtime self-heal on the **request client** pool
  (`src/api/chat/auth_logging.rs`). Not bootstrap-on-logging.
- Other provisioned tenant product tables

When adding a table, decide: **catalog/ops (logging)** vs **tenant provisioned**. Mirror that
decision in SQL location, ensure/heal target pool, and insert path.

## Catalog client load failures + auto-disable

Database-backed clients come from `athena_clients` on the logging pool
(`merge_athena_clients_from_records` in bootstrap when
`gateway.database_backed_client_loading` is true).

On registry load failure (bootstrap merge, on-demand `ensure_catalog_database_client_loaded`,
reconnect worker):

1. Record penalty in `athena_clients.metadata.registry_load_penalty`
2. Consecutive failures inside a rolling window (default **24h**)
3. At threshold (default **10**) with auto-disable on → set `is_active = false`
4. Success clears consecutive failure count

Policy (config + env via `gateway_value`):

| Config key | Env | Default |
|---|---|---|
| `catalog_client_load_failure_auto_disable` | `ATHENA_GATEWAY_CATALOG_CLIENT_LOAD_FAILURE_AUTO_DISABLE` | `true` |
| `catalog_client_load_failure_threshold` | `ATHENA_GATEWAY_CATALOG_CLIENT_LOAD_FAILURE_THRESHOLD` | `10` |
| `catalog_client_load_failure_window_hours` | `ATHENA_GATEWAY_CATALOG_CLIENT_LOAD_FAILURE_WINDOW_HOURS` | `24` |

Code seams:

- pure + DB: `src/data/clients.rs` (`RegistryLoadPenaltyPolicy`,
  `record_catalog_client_registry_load_outcome`)
- merge: `src/bootstrap/postgres_init.rs` (`CatalogMergePenaltyContext`)
- on-demand: `src/athena/postgres_clients.rs`
- reconnect: `src/daemon/mod.rs` `spawn_registry_reconnect_worker`
- AppState field: `gateway_catalog_client_load_failure_policy`

Warn logs like `Failed to load database-backed client into local registry` mean remote URI/pool
connect failed for a **catalog row**; penalties live on logging DB, not on the remote tenant.

## Chat session auth log

- Auth resolution: `src/api/chat/auth.rs` → `spawn_chat_session_auth_log`
- Writer/heal: `src/api/chat/auth_logging.rs`
- Target pool: **X-Athena-Client**, not logging
- Schema ready cache: **per client name**, not a single global flag
- Provisioned in tenant SQL (`chat_session_auth_log` in expected tables)

## Bootstrap orientation

`src/bootstrap/mod.rs`:

1. Config postgres clients → registry
2. Optional logging client override URI
3. On logging pool: ensure control-plane tables (client configs, pipeline templates/logs)
4. Seed/sync config clients into `athena_clients`
5. Optionally load + merge catalog clients with load-failure penalties
6. Background stats refresh on logging pool
7. Build `AppState`

Do **not** reintroduce ensure of tenant-only tables on the logging pool.

## Request-path orientation

1. Resolve `X-Athena-Client` / host routing
2. Auth (API key / session) against the correct pool (auth client vs tenant)
3. Gateway/chat/storage handlers use **tenant** pool unless the feature is explicitly logging/catalog
4. Best-effort logs: gateway request logs → logging; chat session auth → tenant

## Schema self-heal

Use `athena_schema_heal` with a plan name and **client_name that matches the pool** being
mutated. Log `client_name=` in heal messages must equal the target registry key (e.g.
`suits-formations`, never `athena_logging` for tenant tables).

## Common log triage

| Symptom | Likely meaning |
|---|---|
| `tracing file logging ... /var/log/athena Permission denied` | FS log dir only; set `ATHENA_TRACING_LOG_DIR` or fix ownership — not Postgres |
| `Failed to load database-backed client ...` | Catalog row pool connect failed; penalty on logging `athena_clients` |
| `Applied chat session auth log schema self-heal` with `client_name=athena_logging` | **Bug** — heal must target request client |
| Same heal with `client_name=suits-formations` | Expected tenant self-heal |

## Change checklist

When touching multi-tenant data paths:

1. Name the **owning pool** (logging vs request client) in the PR/commit note
2. Keep provision SQL and runtime write path on the same side of that split
3. For catalog lifecycle, update metadata/`is_active` on logging only
4. Prefer focused tests next to pure policy logic (`registry_load_penalty_*`) and module unit tests
5. Validate Rust in **WSL2**, not native Windows `cargo test`

## Validation

Focused:

```powershell
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --lib registry_load_penalty'
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --lib chat::auth_logging'
```

Broader lib when cross-cutting:

```powershell
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --lib'
```

## References

- [references/logging-vs-tenant.md](references/logging-vs-tenant.md) — table ownership quick map
- [references/key-seams.md](references/key-seams.md) — file map for common tasks
