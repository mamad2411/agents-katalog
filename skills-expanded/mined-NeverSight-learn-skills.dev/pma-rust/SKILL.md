---
name: pma-rust
description: Rust project implementation guide for multi-crate workspace projects. Covers workspace config, toolchain (nightly + rustfmt + clippy + cranky + cargo-deny), strict lint rules (no unsafe/unwrap/expect/panic), error handling (thiserror + anyhow), async runtime (Tokio), TLS (rustls + aws-lc-rs), CI/CD (GitHub Actions with test/build/docker/SBOM), and coding conventions. Use when scaffolding, developing, or reviewing Rust applications.
---

# Rust Project Implementation Guide

Standard Rust stack and conventions for multi-crate workspace projects.

## Tech Stack

| Category | Technology | Notes |
|---|---|---|
| **Core** |||
| Language | Rust | edition 2024, nightly toolchain |
| Build | Cargo workspaces | multi-crate monorepo |
| Task runner | just | command runner |
| **Async & HTTP** |||
| Runtime | Tokio | full features |
| HTTP server | Axum 0.8 | multipart, middleware, graceful shutdown |
| HTTP client | reqwest 0.12 | rustls-tls, no openssl |
| **Data** |||
| ORM | Diesel 2 | r2d2 pool, feature-gated backend |
| Concurrent cache | DashMap 6 | lock-free concurrent HashMap |
| **Config & CLI** |||
| Config | figment 0.10 | layered: defaults → file → env → CLI |
| Argument parsing | clap 4 | derive macros, subcommands |
| **Error Handling** |||
| Typed errors | thiserror 2 | per-crate error enums |
| Error propagation | anyhow 1.0 | boundary crossing |
| **Serialization** |||
| Serde | serde 1.0 + serde_json + toml | derive |
| **Linting** |||
| Format | rustfmt | edition 2024 |
| Lint | clippy + cargo-cranky | strict deny rules |
| Dependency audit | cargo-deny | license, ban, advisory |
| **Security** |||
| TLS | rustls 0.23 | aws-lc-rs provider, no openssl/ring |
| Token comparison | subtle 2 | constant-time to prevent timing attacks |

## Workspace Structure

```
Cargo.toml                          # [workspace] root
Cargo.lock
rust-toolchain                      # nightly-YYYY-MM-DD
rustfmt.toml
clippy.toml
Cranky.toml                         # cargo-cranky lint config
deny.toml                           # cargo-deny config
justfile                            # task runner
.cargo/
  config.toml                       # rustflags
.github/
  workflows/
    ci.yml
docs/
  architecture.md
  changelog.md
  task/
  plan/
crates/
  app/                              # main binary crate
    src/
      main.rs
      commands/
  core/                             # runtime services, state, DB
    src/
      services.rs                   # DI container
      db/
      protocols/
  common/                           # shared types, config, errors
    src/
      config/
      error.rs
      types/
      helpers/
  protocol-xxx/                     # per-protocol crate
    src/
      lib.rs
  db/                               # Diesel ORM + migrations
    src/
      lib.rs
      schema.rs
      models.rs
      migrations/
    diesel.toml
tests/                              # integration tests (TypeScript/Bun)
```

## Workspace Cargo.toml

```toml
[workspace]
resolver = "2"
members = ["crates/*"]
default-members = ["crates/app"]

[workspace.package]
version = "0.1.0"
edition = "2024"
license = "Apache-2.0"

[workspace.dependencies]
# Pin shared dependencies here
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "2"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "time", "local-time", "ansi"] }
clap = { version = "4", features = ["derive"] }
axum = { version = "0.8", features = ["multipart"] }
reqwest = { version = "0.12", default-features = false, features = ["json", "rustls-tls"] }
diesel = { version = "2", features = ["r2d2"] }
diesel_migrations = "2"
dashmap = "6"
subtle = "2"

[profile.release]
lto = true
panic = "abort"
strip = "debuginfo"
```

## Toolchain & Compiler Flags

### rust-toolchain

```
nightly-YYYY-MM-DD
```

Pin to a specific nightly date for reproducibility.

### .cargo/config.toml

```toml
[target.'cfg(all())']
rustflags = [
    "--cfg", "tokio_unstable",
    "-Zremap-cwd-prefix=/reproducible-cwd",
    "--remap-path-prefix=$HOME=/reproducible-home",
    "--remap-path-prefix=$PWD=/reproducible-pwd",
]
```

- `tokio_unstable`: enables tokio console + task IDs
- Path remapping: reproducible builds across environments

## Lint Configuration

### rustfmt.toml

```toml
imports_granularity = "Module"
group_imports = "StdExternalCrate"
```

Import groups: std → external crates → local crates, module granularity.

### clippy.toml

```toml
avoid-breaking-exported-api = false
allow-unwrap-in-tests = true
```

### Cranky.toml (cargo-cranky)

```toml
[cranky]
deny = [
    "unsafe_code",
    "clippy::unwrap_used",
    "clippy::expect_used",
    "clippy::panic",
    "clippy::indexing_slicing",
    "clippy::dbg_macro",
]
allow = [
    "clippy::result_large_err",
]
```

**Hard rule**: `unsafe`, `unwrap`, `expect`, `panic`, and index slicing are all **compile errors**. Only site-level `#[allow(...)]` can bypass them (e.g., at startup where failure is fatal).

### deny.toml (cargo-deny)

```toml
[bans]
deny = [
    { crate = "openssl-sys", use-instead = "rustls" },
]

[licenses]
allow = [
    "MIT", "Apache-2.0", "ISC",
    "BSD-2-Clause", "BSD-3-Clause",
    "Zlib", "CC0-1.0",
]
```

- **Ban openssl**: all TLS must use rustls + aws-lc-rs
- **License allowlist**: only permissive licenses

## Error Handling

Two-tier system:

1. **`thiserror`** — each crate defines its own error enum with `#[from]` conversions:

```rust
#[derive(thiserror::Error, Debug)]
pub enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sea_orm::DbErr),

    #[error("config error: {0}")]
    Config(#[from] ConfigError),

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}
```

2. **`anyhow::Result<T>`** — for propagation across crate boundaries where typed error is not needed.

### Secret Handling

Wrap secrets in a `Secret<T>` type that redacts `Debug` output:

```rust
pub struct Secret<T>(T);

impl<T> std::fmt::Debug for Secret<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("<secret>")
    }
}
```

Prevents accidental secret leakage in logs and error messages.

## Architecture Patterns

### Services (DI Container)

```rust
pub struct Services {
    pub db: Arc<Mutex<DatabaseConnection>>,
    pub config: Arc<Mutex<AppConfig>>,
    pub state: Arc<Mutex<State>>,
}
```

All services use `Arc<Mutex<T>>` for shared ownership. `Services` is cloned cheaply (all fields are `Arc`).

### Protocol Server Trait

```rust
pub trait ProtocolServer {
    fn name(&self) -> &'static str;
    fn run(self, address: ListenEndpoint) -> impl Future<Output = Result<()>> + Send;
}
```

### Trait Polymorphism

Prefer `enum_dispatch` over `Box<dyn Trait>` for zero-cost polymorphism at runtime.

### Deadlock Detection (Debug Only)

Wrap `tokio::sync::Mutex` with a 5-second timeout in debug builds:

```rust
#[cfg(debug_assertions)]
pub async fn lock(&self) -> MutexGuard<'_, T> {
    match tokio::time::timeout(Duration::from_secs(5), self.inner.lock()).await {
        Ok(guard) => guard,
        Err(_) => panic!("deadlock detected on mutex: {}", self.name),
    }
}
```

## Database (Diesel)

### Crate Structure

```
crates/
  db/                               # @project/db
    src/
      lib.rs
      schema.rs                     # diesel print-schema output
      models.rs                     # Queryable/Insertable structs
      migrations/
        00000000000000_create_xxx/
          up.sql
          down.sql
    diesel.toml
```

### diesel.toml

```toml
[print_schema]
file = "src/schema.rs"

[migrations_directory]
dir = "src/migrations"
```

### Feature Flags

```toml
[features]
default = ["sqlite"]
postgres = ["diesel/postgres"]
mysql = ["diesel/mysql"]
sqlite = ["diesel/sqlite"]
```

### Connection Pool

Use `diesel::r2d2` for connection pooling:

```rust
use diesel::r2d2::{self, ConnectionManager};

pub type DbPool = r2d2::Pool<ConnectionManager<SqliteConnection>>;

pub fn establish_pool(database_url: &str) -> DbPool {
    let manager = ConnectionManager::<SqliteConnection>::new(database_url);
    r2d2::Pool::builder()
        .max_size(10)
        .build(manager)
        .expect("failed to create pool")
}
```

### Migration

Run migrations at startup:

```rust
use diesel_migrations::{embed_migrations, EmbeddedMigrations, MigrationHarness};

const MIGRATIONS: EmbeddedMigrations = embed_migrations!("src/migrations");

pub fn run_migrations(conn: &mut impl MigrationHarness<diesel::sqlite::Sqlite>) {
    conn.run_pending_migrations(MIGRATIONS)
        .expect("failed to run migrations");
}
```

### CLI

```bash
# Install diesel CLI
cargo install diesel_cli --no-default-features --features sqlite

# Setup (creates diesel.toml + migrations dir)
diesel setup

# Generate migration
diesel migration generate create_users

# Run migrations
diesel migration run

# Print schema
diesel print-schema > src/schema.rs
```

## Configuration System (figment + clap)

Layered config with figment: **Defaults → TOML file → Env vars → CLI args** (later sources override earlier).

### Dependencies

```toml
[workspace.dependencies]
figment = { version = "0.10", features = ["toml", "env"] }
clap = { version = "4", features = ["derive"] }
serde = { version = "1", features = ["derive"] }
```

### Config Structs

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct AppConfig {
    pub server: ServerConfig,
    pub database: DatabaseConfig,
    pub logging: LoggingConfig,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct DatabaseConfig {
    pub url: String,
    pub max_connections: u32,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct LoggingConfig {
    pub level: String,
    pub format: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            server: ServerConfig { host: "0.0.0.0".into(), port: 3000 },
            database: DatabaseConfig { url: "sqlite://data.db".into(), max_connections: 10 },
            logging: LoggingConfig { level: "info".into(), format: "text".into() },
        }
    }
}
```

### CLI Struct

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp", about = "Application description")]
pub struct Cli {
    /// Config file path
    #[arg(short, long, default_value = "config.toml")]
    pub config: String,

    /// Override server port
    #[arg(long)]
    pub port: Option<u16>,

    /// Override log level
    #[arg(long)]
    pub log_level: Option<String>,

    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    /// Start the server
    Run,
    /// Check configuration validity
    Check,
    /// Print version info
    Version,
    /// Generate default config file
    Init,
}
```

### Layered Loading with figment

```rust
use figment::{Figment, providers::{Format, Toml, Env, Serialized}};

impl AppConfig {
    /// Load config: Defaults → TOML file → Env → CLI overrides
    pub fn load(cli: &Cli) -> anyhow::Result<Self> {
        let mut figment = Figment::new()
            // Layer 1: compiled defaults
            .merge(Serialized::defaults(AppConfig::default()))
            // Layer 2: config file (optional — missing file is OK)
            .merge(Toml::file(&cli.config))
            // Layer 3: env vars with APP_ prefix (APP_SERVER_PORT, APP_DATABASE_URL, etc.)
            .merge(Env::prefixed("APP_").split("_"));

        // Layer 4: CLI overrides (highest priority)
        if let Some(port) = cli.port {
            figment = figment.merge(Serialized::default("server.port", port));
        }
        if let Some(ref level) = cli.log_level {
            figment = figment.merge(Serialized::default("logging.level", level));
        }

        let config: AppConfig = figment.extract()?;
        Ok(config)
    }

    /// Auto-generate default config if file does not exist.
    pub fn ensure_exists(path: &str) -> anyhow::Result<()> {
        if !std::path::Path::new(path).exists() {
            let default = toml::to_string_pretty(&AppConfig::default())?;
            std::fs::write(path, default)?;
            eprintln!("generated default config at {path}, please edit and restart");
            std::process::exit(0);
        }
        Ok(())
    }
}
```

### Usage in main

```rust
use clap::Parser;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Command::Run => {
            let config = AppConfig::load(&cli)?;
            start_server(&config).await?;
        }
        Command::Check => {
            let config = AppConfig::load(&cli)?;
            println!("config OK: {config:#?}");
        }
        Command::Version => {
            println!("{}", env!("CARGO_PKG_VERSION"));
        }
        Command::Init => {
            AppConfig::ensure_exists(&cli.config)?;
        }
    }

    Ok(())
}
```

### Config File Format

```toml
# config.toml
[server]
host = "0.0.0.0"
port = 3000

[database]
url = "sqlite://data.db"
max_connections = 10

[logging]
level = "info"
format = "text"  # "text" or "json"
```

### Override Priority (low → high)

```
AppConfig::default()     # compiled defaults
  ↓
config.toml              # TOML file
  ↓
APP_SERVER_PORT=8080     # env vars (APP_ prefix, _ splits nested keys)
  ↓
--port 9090              # CLI args (highest priority)
```

### Conventions

- Use figment for layered merging — never hand-roll priority logic
- `Serialized::defaults()` ensures every field has a default even without a config file
- Env prefix (`APP_`) prevents collisions; `split("_")` maps `APP_SERVER_PORT` → `server.port`
- CLI overrides are explicit `Option<T>` fields — only merge when `Some`
- Keep config structs in `crates/app/src/config.rs`, CLI in `crates/app/src/cli.rs`
- `#[derive(Serialize)]` on config structs (needed for `Serialized::defaults`)
- Auto-generate config file via `init` subcommand for onboarding

## Signal Handling

Graceful shutdown with Tokio signal handlers:

```rust
use tokio::signal;

pub async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install SIGTERM handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => tracing::info!("received Ctrl+C, shutting down"),
        _ = terminate => tracing::info!("received SIGTERM, shutting down"),
    }
}
```

### Usage in main

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    let config = AppConfig::load(&cli)?;

    // Start server with graceful shutdown
    let server = start_server(&config);

    tokio::select! {
        result = server => result?,
        _ = shutdown_signal() => {
            tracing::info!("graceful shutdown complete");
        }
    }

    Ok(())
}
```

### Shutdown Checklist

- Flush pending database writes
- Close connection pools
- Complete in-flight requests (with timeout)
- Flush tracing/log buffers

## HTTP Server (Axum)

### Router Structure

```rust
use axum::{Router, routing::{get, post}, middleware};

pub fn create_router(state: AppState) -> Router {
    Router::new()
        // Public routes
        .route("/health", get(health))
        // Protected API routes
        .nest("/api/v1", api_routes()
            .layer(middleware::from_fn(verify_token)))
        .with_state(Arc::new(state))
}
```

### AppState

```rust
pub struct AppState {
    pub db: DbPool,
    pub config: AppConfig,
}
```

Pass as `State(state): State<Arc<AppState>>` in handlers.

### Handler Pattern

```rust
async fn get_item(
    State(state): State<Arc<AppState>>,
    Path(id): Path<i32>,
) -> Result<Json<Item>, AppError> {
    let conn = &mut state.db.get()?;
    let item = items::table.find(id).first(conn)?;
    Ok(Json(item))
}
```

### Auth Middleware

Use `subtle::ConstantTimeEq` for token comparison to prevent timing attacks:

```rust
use subtle::ConstantTimeEq;

async fn verify_token(
    headers: HeaderMap,
    request: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let token = headers.get("authorization")
        .and_then(|v| v.to_str().ok())
        .and_then(|v| v.strip_prefix("Bearer "));

    match token {
        Some(t) if t.as_bytes().ct_eq(expected.as_bytes()).into() => {
            Ok(next.run(request).await)
        }
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}
```

### Graceful Shutdown with Axum

```rust
let listener = tokio::net::TcpListener::bind(&addr).await?;
axum::serve(listener, router)
    .with_graceful_shutdown(shutdown_signal())
    .await?;
```

## Security Patterns

### Constant-Time Token Comparison

Always use `subtle::ConstantTimeEq` for auth token, API key, and HMAC comparisons. Never use `==` for secrets.

### SSRF Protection

When accepting user-provided URLs (webhooks, callbacks), validate the resolved IP:

```rust
use std::net::IpAddr;

fn is_private_ip(ip: IpAddr) -> bool {
    match ip {
        IpAddr::V4(v4) => {
            v4.is_private() || v4.is_loopback() || v4.is_link_local()
            || v4.is_broadcast() || v4.is_unspecified()
        }
        IpAddr::V6(v6) => v6.is_loopback() || v6.is_unspecified(),
    }
}

fn validate_webhook_url(url: &str) -> anyhow::Result<()> {
    let host = url::Url::parse(url)?.host_str()
        .ok_or_else(|| anyhow::anyhow!("no host"))?
        .to_string();
    let addrs = std::net::ToSocketAddrs::to_socket_addrs(
        &(host.as_str(), 443)
    )?;
    for addr in addrs {
        anyhow::ensure!(!is_private_ip(addr.ip()), "private IP not allowed");
    }
    Ok(())
}
```

### Concurrent Cache (DashMap)

Use `DashMap` for in-memory caches shared across async tasks:

```rust
use dashmap::DashMap;

pub struct Cache {
    inner: DashMap<String, CachedItem>,
}

impl Cache {
    pub fn get(&self, key: &str) -> Option<CachedItem> {
        self.inner.get(key).map(|v| v.clone())
    }

    pub fn insert(&self, key: String, value: CachedItem) {
        self.inner.insert(key, value);
    }
}
```

No `Mutex` needed — `DashMap` handles concurrent reads/writes internally.

## Logging

Multi-layer tracing setup with `tracing-subscriber`:

- **Console**: ANSI colors, env-filter, local-time
- **JSON**: structured JSON format for `--log-format json`
- **Database**: custom `Layer` that captures events at INFO+ and writes to DB
- Filter to only `{crate_prefix}`-prefixed targets for application logs

## CI Pipeline

### ci.yml (PR + push to main)

Two-stage pipeline: format gate first, then parallel checks.

```yaml
jobs:
  # Gate 1: format must pass before anything else runs
  fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: dtolnay/rust-toolchain@<sha>
      - run: cargo fmt --check

  # Gate 2: parallel checks after format passes
  clippy:
    needs: [fmt]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: dtolnay/rust-toolchain@<sha>
      - run: cargo cranky --all-targets -- -D warnings

  test:
    needs: [fmt]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: dtolnay/rust-toolchain@<sha>
      - run: cargo test --all-features

  deny:
    needs: [fmt]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: EmbarkStudios/cargo-deny-action@<sha>
```

Key: `fmt` is the first gate — no point running clippy/test if formatting is broken.

### CI Jobs Summary

| Job | Command | Gate |
|---|---|---|
| Format | `cargo fmt --check` | Must pass |
| Lint | `cargo cranky --all-features` | Must pass, zero warnings |
| Deny | `cargo deny check` | No banned deps, no license violations |
| Test | `cargo test --all-features` | Must pass |
| Build | `cargo build --all-features --release` | Must succeed |

## justfile Tasks

```just
# Common tasks
check:
    cargo cranky --all-features
    cargo test --all-features
    cargo fmt --check
    cargo deny check

fmt:
    cargo fmt

build:
    cargo build --all-features --release

config-schema:
    cargo run -p app -- config-schema > config-schema.json

openapi:
    cargo run -p admin -- openapi > openapi.json
```

## Conventions

| Area | Convention |
|---|---|
| Crate naming | `{project}-{module}` (e.g., `gated-core`, `gated-common`) |
| Imports | Module granularity, grouped std/external/local |
| Error types | Per-crate `thiserror` enum, `anyhow` for boundaries |
| No unsafe | Enforced by cranky deny rule |
| No unwrap/expect | Enforced by cranky; use `#[allow]` only at fatal startup points |
| Shared state | `Arc<Mutex<T>>` via `Services` DI container |
| Secrets | `Secret<T>` wrapper with redacted Debug |
| Token auth | `subtle::ConstantTimeEq` — never `==` for secrets |
| TLS | rustls + aws-lc-rs only; openssl banned |
| HTTP server | Axum 0.8 with middleware + graceful shutdown |
| Concurrent cache | DashMap — no Mutex needed for shared caches |
| Database | Diesel 2 + r2d2 pool; feature-gated backend (sqlite default) |
| Config | figment layered: Defaults → TOML → Env (`APP_` prefix) → CLI |
| CLI | clap 4 derive — `Parser` + `Subcommand`; `Option<T>` for overrides |
| Shutdown | Tokio signal handler; SIGINT + SIGTERM graceful shutdown |
| Reproducible builds | Path remapping via rustflags |
| Release profile | `lto = true`, `panic = "abort"`, `strip = "debuginfo"` |

