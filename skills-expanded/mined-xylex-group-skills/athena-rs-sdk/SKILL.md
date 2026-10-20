---
name: athena-rs-sdk
description: Rust Athena SDK/client playbook for `athena_rs`. Use when working with `AthenaClient`, `AthenaClientBuilder`, `BackendType`, fluent CRUD builders, typed `Gateway*Request` contracts, `Gateway::REQUEST`, SQL/RPC/CQL execution, endpoint derivation, and gateway-vs-direct connection behavior against existing Athena servers or databases. Do not use for Actix handlers, admin/provisioning APIs, workers, daemon logic, or broader server runtime changes unless the SDK contract itself is the problem.
---

# Athena RS SDK

Work from the SDK surface outward. Prefer the Rust client code under `src/client/`, the SDK examples under `examples/`, and `tests/sdk_gateway_examples_e2e.rs` before touching server routes.

Current repo target: `athena_rs` `3.16.1`.

## Source of truth order

Read in this order:

1. `src/client/mod.rs`
2. `src/client/{builder,backend,config,query_builder,gateway_api}.rs`
3. `examples/README.md` and the relevant `examples/gateway_*.rs` files
4. `tests/sdk_gateway_examples_e2e.rs`
5. `README.md` `## SDK`
6. `src/lib.rs` exports

If docs and source disagree, prefer the current source, tests, and examples in this checkout.

## Stay in SDK scope

Use this skill for:

- adding or fixing Rust code that uses Athena over HTTP or direct backend connections
- adjusting the fluent client API or typed request contracts
- clarifying how gateway routing, translation, and direct backend mode behave
- writing SDK examples, README snippets, or SDK-focused tests

Do not use this skill for:

- `src/api/**` Actix handlers
- admin, provisioning, daemon, worker, websocket, or auth runtime changes
- `athena-js` storage/OpenAPI parity work unless `athena_rs` itself is gaining a matching Rust SDK builder or typed request contract
- server config/debug work unless the issue is definitely in the Rust SDK contract

## Pick the mode first

Decide this before changing code.

Gateway-routed mode:

- Set a client name with `AthenaClient::new(...)`, `new_with_backend(...)`, or builder `.client(...)`.
- Use an Athena base URL like `http://localhost:4052` or `https://mirror3.athena-db.com`.
- Use an Athena API key.
- Athena sends requests to routes like `/gateway/fetch`, `/gateway/insert`, `/gateway/update`, `/gateway/delete`, `/gateway/sql`, and `/gateway/rpc`.
- `BackendType` selects translation behavior, not a direct database connection.

Direct mode:

- Omit `.client(...)`.
- Use a direct backend URL, not an Athena gateway base URL.
- `BackendType::Native`, `PostgreSQL`, `Neon`, and `Postgrest` resolve to direct Postgres access.
- `BackendType::Supabase` resolves to direct Supabase access.
- `BackendType::Scylla` resolves to direct Scylla access.

Important consequences from `src/client/mod.rs`:

- `client_name` present means Athena uses `GatewayBackend`.
- `rpc_request(...)` only works in Athena gateway client mode.
- `new_direct(...)` is only the right shortcut when default direct `Native` behavior is acceptable. Prefer the builder when backend choice or pool/health settings matter.

## Construction patterns

Gateway mode, default native translation:

```rust
use athena_rs::AthenaClient;

let client = AthenaClient::new(
    "http://localhost:4052",
    "secret",
    "reporting",
).await?;
```

Gateway mode with explicit backend:

```rust
use athena_rs::{AthenaClient, BackendType};

let client = AthenaClient::new_with_backend(
    "http://localhost:4052",
    "secret",
    "reporting",
    BackendType::Neon,
).await?;
```

Builder when you need explicit pool, health, SSL, port, or database settings:

```rust
use athena_rs::{AthenaClient, AthenaClientBuilder, BackendType};
use std::time::Duration;

let builder: AthenaClientBuilder = AthenaClient::builder()
    .backend(BackendType::PostgreSQL)
    .url("postgres://user:pass@localhost:5432/app")
    .ssl(true)
    .database("app")
    .max_connections(20)
    .connection_timeout(Duration::from_secs(5))
    .health_tracking(true);

let client = AthenaClient::build(builder).await?;
```

Use the builder for direct Postgres more often than `new_direct(...)`. The URL in direct Postgres mode is a Postgres connection string, not an Athena base URL.

## Prefer the fluent builders for CRUD

The normal entrypoints are:

- `select(...)` and the alias `fetch(...)`
- `insert(...)`
- `update(...)`
- `delete(...)`
- `update_by_id(...)`
- `delete_by_id(...)`
- `rpc(...)`
- `sql(...)`, `execute_sql(...)`, `execute_sql_in_schema(...)`
- `execute_cql(...)`

Copy-paste workflow:

```rust
use athena_rs::AthenaClient;
use serde_json::json;

let client = AthenaClient::new("http://localhost:4052", "secret", "reporting").await?;

let inserted = client
    .insert("users")
    .payload(json!({
        "email": "workflow.user@example.com",
        "status": "pending"
    }))
    .execute()
    .await?;

let fetched = client
    .fetch("users")
    .columns(["id", "email", "status"])
    .where_eq("email", "workflow.user@example.com")
    .limit(1)
    .execute()
    .await?;

let updated = client
    .update("users")
    .where_eq("email", "workflow.user@example.com")
    .payload(json!({ "status": "active" }))
    .execute()
    .await?;

let deleted = client
    .delete("users")
    .where_eq("email", "workflow.user@example.com")
    .execute()
    .await?;
```

Useful builder details from `src/client/query_builder.rs`:

- `.schema_name(...)` exists on fetch/insert/update/delete builders.
- `.raw_select(...)` exists on fetch/select for PostgREST-style nested relation projections.
- shared select/update/delete filters are `where_eq`, `where_neq`, `where_gt`, `where_lt`, `where_in`.
- ordering is `order_by("column", OrderDirection::Asc | Desc)`.
- pagination is `limit(...)` and `offset(...)`.

## Use typed gateway requests when a serializable contract matters

Use these when the task wants explicit request structs or reusable request payloads:

- `GatewayFetchRequest`
- `GatewayInsertRequest`
- `GatewayUpdateRequest`
- `GatewayDeleteRequest`
- `GatewaySqlRequest`
- `GatewayRpcRequest`
- `GatewayRequest`
- `Gateway::REQUEST`

Copy-paste example:

```rust
use athena_rs::{
    AthenaClient, Gateway, GatewayFetchRequest, GatewaySqlRequest,
};
use serde_json::json;

let client = AthenaClient::new("http://localhost:4052", "secret", "reporting").await?;

let fetch_request = GatewayFetchRequest::new("users")
    .columns(["id", "email"])
    .where_eq("status", "active")
    .limit(20);

let fetched = client.fetch_request(fetch_request).await?;

let updated = client
    .update_request(
        Gateway::REQUEST
            .update("users", json!({ "status": "active" }))
            .where_eq("email", "new.user@example.com"),
    )
    .await?;

let sql = client
    .sql_request(GatewaySqlRequest::new("SELECT 1 AS ok"))
    .await?;
```

Remember:

- typed CRUD requests and fluent CRUD builders converge into the same client execution path
- typed CRUD still benefits from the same identifier and scope safeguards
- `GatewaySqlRequest` is the raw-SQL escape hatch and does not sanitize SQL text

## RPC, SQL, and CQL rules

RPC:

- use `client.rpc("fn_name", json!(...))`
- chain `.select(...)`, filter methods like `.eq(...)`, `.order(...)`, `.limit(...)`, `.offset(...)`, `.count_exact()`
- `rpc_request(...)` and `RpcBuilder` require gateway client mode

```rust
use athena_rs::{AthenaClient, OrderDirection};
use serde_json::json;

let rows = client
    .rpc("echo_all_cities", json!({}))
    .select("name,population")
    .eq("name", "The Shire")
    .order("name", OrderDirection::Asc)
    .limit(10)
    .count_exact()
    .execute()
    .await?;
```

SQL:

- use `sql(...)` or `execute_sql(...)` for trusted operator-authored SQL only
- use `execute_sql_in_schema(...)` or `GatewaySqlRequest::schema_name(...)` for explicit schema override
- do not build raw SQL from untrusted values when a builder or typed CRUD request can express the same operation

CQL:

- use `execute_cql(...)`
- keep it scoped to Scylla/Cassandra tasks
- do not add CQL behavior to normal Postgres gateway flows

## Safety rails that matter

Preserve these behaviors:

- builder-based CRUD is the safest surface for user-controlled values
- `update(...)` and `delete(...)` reject unfiltered mutations unless the caller explicitly opts in with `unsafe_unfiltered()`
- raw SQL APIs forward SQL verbatim
- public config/debug surfaces redact secrets through `ClientConfig` and `ConnectionConfig`
- route constants and helpers come from `Gateway::*_PATH`, `GatewayRoutes`, and `build_gateway_endpoint(...)`

Common mistakes:

- passing an Athena base URL into direct Postgres mode
- changing `src/api/**` when the issue is actually in `src/client/translator.rs`, `query_builder.rs`, or `gateway_api.rs`
- assuming `AthenaClientBuilder` has its own async `.build()` method; the current construction path is `AthenaClient::build(builder).await`
- expecting RPC to work without gateway client mode
- replacing existing aliases like `fetch(...)` or `Gateway::REQUEST` with new wrappers instead of extending the current surface

## Change seams

When you add or change public SDK behavior, inspect these files together:

- `src/client/mod.rs` for public methods and routing behavior
- `src/client/query_builder.rs` for fluent builder methods and scope rules
- `src/client/gateway_api.rs` for typed request structs and route constants
- `src/client/builder.rs` and `src/client/config.rs` for client construction/config
- `src/lib.rs` for top-level re-exports
- `examples/*.rs` for copy-paste usage
- `tests/sdk_gateway_examples_e2e.rs` for gateway contract validation
- `README.md` `## SDK` when user-facing behavior changes

Keep additions additive unless the user explicitly asks for a breaking redesign.

## Validation

After SDK-facing changes, run the narrowest proof that matches the seam you changed.

Common checks:

```powershell
cargo test --lib
cargo run --example gateway_fetch_builder
cargo run --example gateway_typed_requests
```

If the change affects public gateway routing, typed request contracts, filters, or builder behavior, also use the SDK E2E suite:

```powershell
$env:ATHENA_RUN_GATEWAY_SDK_E2E = "1"
$env:ATHENA_E2E_BASE_URL = "https://mirror3.athena-db.com"
$env:ATHENA_E2E_CLIENT = "athena_logging"
$env:ATHENA_E2E_TABLE = "athena_e2e_adapter"
$env:ATHENA_E2E_KEY = "<your-athena-key>"
cargo test --test sdk_gateway_examples_e2e -- --nocapture
```

Use focused examples/tests whenever possible:

- `examples/gateway_fetch_builder.rs`
- `examples/gateway_insert_builder.rs`
- `examples/gateway_update_builder.rs`
- `examples/gateway_delete_builder.rs`
- `examples/gateway_rpc_builder.rs`
- `examples/gateway_typed_requests.rs`
- `examples/gateway_row_id_shortcuts.rs`
- `tests/sdk_gateway_examples_e2e.rs`

If a request shape changes, verify the example, the E2E suite, and the re-exports together before calling the work done.
