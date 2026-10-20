---
name: rust-modules
description: "When to activate: Rust modules, Cargo.toml, workspaces, crate organization, pub visibility, use declarations, features, dependencies"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: rust
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Rust Modules and Cargo

## Module Organization

```
my_crate/
├── Cargo.toml
└── src/
    ├── lib.rs
    ├── config.rs
    ├── models/
    │   ├── mod.rs
    │   ├── user.rs
    │   └── post.rs
    └── services/
        ├── mod.rs
        ├── auth.rs
        └── email.rs
```

```rust
// src/lib.rs
pub mod config;
pub mod models;
pub mod services;

pub use models::user::User;
pub use models::post::Post;
```

## Visibility

```rust
pub struct Config {
    pub name: String,
    pub(crate) internal_id: u32,
    pub(super) parent_only: bool,
    private_secret: String,
}

impl Config {
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into(), internal_id: 0, parent_only: false, private_secret: String::new() }
    }
    pub fn name(&self) -> &str { &self.name }
}

pub(crate) fn internal_helper() { /* ... */ }
```

## Cargo.toml: Common Patterns

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
anyhow = "1"
tracing = "0.1"

[dev-dependencies]
tokio = { version = "1", features = ["full", "test-util"] }
proptest = "1"
tempfile = "3"

[[bin]]
name = "server"
path = "src/bin/server.rs"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

## Feature Flags

```toml
[features]
default = ["tokio-runtime"]
tokio-runtime = ["tokio/full"]
metrics = ["prometheus"]
tls = ["rustls"]
full = ["metrics", "tls"]

[dependencies]
tokio = { version = "1", optional = true }
prometheus = { version = "0.13", optional = true }
rustls = { version = "0.23", optional = true }
```

```rust
#[cfg(feature = "metrics")]
pub mod metrics;

#[cfg(not(feature = "metrics"))]
pub fn record_request(_: &str) {}
```

## Workspaces

```toml
# Cargo.toml (workspace root)
[workspace]
members = [
    "crates/core",
    "crates/server",
    "crates/worker",
    "crates/client",
]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
anyhow = "1"

[workspace.package]
edition = "2021"
license = "MIT OR Apache-2.0"
```

```toml
# crates/server/Cargo.toml
[package]
name = "server"
version.workspace = true
edition.workspace = true

[dependencies]
core = { path = "../core" }
tokio.workspace = true
serde.workspace = true
```

## Useful Cargo Commands

```bash
cargo new my-crate              # new binary crate
cargo new --lib my-lib          # new library crate
cargo add tokio --features full # add dependency
cargo add --dev proptest        # add dev dependency
cargo build --release           # optimized build
cargo test                      # run all tests
cargo clippy -- -D warnings     # lint, deny warnings
cargo fmt --check               # check formatting
cargo audit                     # security advisories
cargo tree                      # dependency tree
cargo doc --open                # build and open docs
```

## Common Anti-Patterns

- **Everything in `main.rs` or `lib.rs`** — organize by feature domain; split files > 300 lines
- **`pub` everything by default** — expose only what external callers need
- **Deeply nested module trees** — prefer flat `modules/` directories
- **Overlapping feature flags** — keep features additive and non-conflicting
- **Missing `resolver = "2"` in workspace** — required for correct feature unification
