---
name: cargo-conventions
description:
  This skill should be used when managing Cargo.toml configuration, workspace setup, dependency
  management, feature flags, publishing crates, or configuring build profiles in Rust projects.
version: 0.1.0
---

# Cargo Conventions and Configuration Patterns

This skill defines comprehensive conventions for managing Rust projects with Cargo, covering
Cargo.toml structure, workspace management, dependency practices, feature flags, build profiles,
lints, and publishing.

## Cargo.toml Structure

### Section Ordering

Cargo.toml sections should follow a consistent order for readability.

```toml
# CORRECT: Standard section ordering
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
description = "A brief description"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/my-crate"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["category"]

[features]
default = ["json"]
json = ["dep:serde_json"]
xml = ["dep:quick-xml"]

[dependencies]
serde = { version = "1", features = ["derive"] }
thiserror = "2"

[dev-dependencies]
proptest = "1"
tokio = { version = "1", features = ["test-util", "macros"] }

[build-dependencies]
prost-build = "0.13"

[lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }

[profile.release]
lto = true
```

```toml
# WRONG: Randomly ordered sections
[dev-dependencies]
proptest = "1"

[profile.release]
lto = true

[package]
name = "my-crate"
version = "0.1.0"

[dependencies]
serde = "1"
```

### Edition and MSRV

Always specify the edition. Set `rust-version` (MSRV) for libraries to communicate the minimum
supported Rust version.

```toml
# CORRECT: Edition and MSRV specified
[package]
name = "my-lib"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
```

```toml
# WRONG: Missing edition (defaults may change between Cargo versions)
[package]
name = "my-lib"
version = "0.1.0"
```

## Lint Configuration

### Configure Lints in Cargo.toml

Since Rust 1.74, clippy lints should be configured in Cargo.toml using the `[lints]` table instead
of `#![warn(...)]` attributes in source files.

```toml
# CORRECT: Lints in Cargo.toml (modern approach)
[lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }
unwrap_used = "warn"
expect_used = "warn"

[lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"
```

```toml
# WRONG: Using a separate clippy.toml for lint configuration
# clippy.toml files are for clippy-specific settings like msrv,
# not for lint levels
```

```rust
// WRONG: Lint attributes in source files (use Cargo.toml instead)
#![warn(clippy::all, clippy::pedantic)]
#![forbid(unsafe_code)]
```

### Workspace Lint Inheritance

In workspaces, define lints once at the workspace level and inherit them in member crates.

```toml
# CORRECT: Workspace root Cargo.toml
[workspace.lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }
unwrap_used = "warn"

# Member crate Cargo.toml
[lints]
workspace = true
```

```toml
# WRONG: Duplicating lint config in every member crate
# crate-a/Cargo.toml
[lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }

# crate-b/Cargo.toml (same config repeated)
[lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
```

## Workspace Management

### Workspace Structure

Use workspaces for multi-crate projects to share dependencies and build artifacts.

```toml
# CORRECT: Workspace root Cargo.toml
[workspace]
resolver = "2"
members = [
    "crates/core",
    "crates/api",
    "crates/cli",
]

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/project"

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
thiserror = "2"
anyhow = "1"
```

```toml
# Member crate: crates/core/Cargo.toml
[package]
name = "project-core"
version.workspace = true
edition.workspace = true

[dependencies]
serde.workspace = true
thiserror.workspace = true
```

```toml
# WRONG: Duplicating dependency versions across member crates
# crates/core/Cargo.toml
[dependencies]
serde = { version = "1", features = ["derive"] }

# crates/api/Cargo.toml
[dependencies]
serde = { version = "1", features = ["derive"] }  # duplicated
```

### Virtual Workspaces

For projects that are only a collection of crates with no root crate, use a virtual workspace.

```toml
# CORRECT: Virtual workspace (no [package] section)
[workspace]
resolver = "2"
members = [
    "crates/*",
]

[workspace.dependencies]
# shared dependency catalog
```

```toml
# WRONG: Root crate that exists only to hold the workspace
[package]
name = "project-root"
version = "0.0.0"
publish = false

[workspace]
members = ["crates/*"]
```

## Feature Flags

### Features Must Be Additive

Feature flags must only add functionality, never change or remove existing behavior. Enabling an
additional feature should never break code that works without it.

```toml
# CORRECT: Features are purely additive
[features]
default = ["json"]
json = ["dep:serde", "dep:serde_json"]
xml = ["dep:quick-xml"]
tracing = ["dep:tracing"]
```

```toml
# WRONG: Mutually exclusive features
[features]
backend-postgres = ["dep:sqlx-postgres"]
backend-sqlite = ["dep:sqlx-sqlite"]
# These cannot be enabled together, violating the additive rule
```

### Use dep: Syntax for Optional Dependencies

Use the `dep:` syntax to enable optional dependencies without creating implicit feature names.

```toml
# CORRECT: dep: syntax (Rust 1.60+)
[features]
json = ["dep:serde", "dep:serde_json"]

[dependencies]
serde = { version = "1", optional = true }
serde_json = { version = "1", optional = true }
```

```toml
# WRONG: Implicit feature names from optional dependencies
[dependencies]
serde = { version = "1", optional = true }
serde_json = { version = "1", optional = true }
# This creates features named "serde" and "serde_json" implicitly
```

### Document Features

Document every feature flag in the crate-level documentation.

```rust
// CORRECT: Feature documentation in lib.rs
//! # Features
//!
//! - `json` (default): Enable JSON serialization via serde
//! - `xml`: Enable XML serialization via quick-xml
//! - `tracing`: Enable tracing instrumentation
```

## Dependency Management

### Version Requirements

Use semver-compatible version requirements. Prefer caret requirements for flexibility.

```toml
# CORRECT: Caret requirements (default, most flexible)
[dependencies]
serde = "1"           # Equivalent to >=1.0.0, <2.0.0
tokio = "1.35"        # Equivalent to >=1.35.0, <2.0.0
uuid = "1.7.0"        # Equivalent to >=1.7.0, <2.0.0
```

```toml
# WRONG: Pinning exact versions (prevents deduplication)
[dependencies]
serde = "=1.0.195"    # Exact pin prevents cargo from resolving conflicts
tokio = "=1.35.1"     # Forces all consumers to use this exact version
```

### Minimize Dependency Features

Only enable the features you actually use.

```toml
# CORRECT: Only enable needed features
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "net", "macros"] }
reqwest = { version = "0.12", default-features = false, features = ["json", "rustls-tls"] }
```

```toml
# WRONG: Enabling all features when you only need a subset
[dependencies]
tokio = { version = "1", features = ["full"] }
reqwest = "0.12"  # Pulls in default features including openssl
```

### Dev Dependencies Should Not Leak

Dev dependencies are only used for tests, examples, and benchmarks. They should never appear in
`[dependencies]`.

```toml
# CORRECT: Test-only dependencies in dev-dependencies
[dev-dependencies]
proptest = "1"
mockall = "0.13"
tempfile = "3"
criterion = { version = "0.5", features = ["html_reports"] }
```

```toml
# WRONG: Test frameworks in production dependencies
[dependencies]
proptest = "1"  # Will be compiled into the production binary
```

## Build Profiles

### Release Profile for Binaries Only

Customize `[profile.release]` only in binary crates (services, CLIs). Libraries should not set
release profiles because the consuming binary controls the profile.

```toml
# CORRECT: Release profile in a binary crate
[profile.release]
lto = true
codegen-units = 1
strip = true
```

```toml
# WRONG: Release profile in a library crate
# The library does not control how it is compiled; the binary crate does
[package]
name = "my-library"

[profile.release]
lto = true  # Has no effect when used as a dependency
```

### Profile Settings Explained

```toml
# Service/CLI production profile
[profile.release]
lto = true          # Link-Time Optimization: slower build, faster binary
codegen-units = 1   # Single codegen unit: slower build, better optimization
strip = true        # Remove debug symbols: smaller binary
panic = "abort"     # Abort on panic: smaller binary, no unwinding overhead

# Development profile tweaks (optional)
[profile.dev]
opt-level = 1       # Slight optimization for faster dev builds
```

### Custom Profiles

Use custom profiles for specific scenarios:

```toml
# Fast release builds for CI (skip LTO for speed)
[profile.ci]
inherits = "release"
lto = false
codegen-units = 16

# Profiling build with debug symbols
[profile.profiling]
inherits = "release"
debug = true
strip = false
```

## Publishing

### Pre-Publish Checklist

Before publishing to crates.io:

```toml
# CORRECT: All required metadata for publishing
[package]
name = "my-crate"
version = "1.0.0"
edition = "2021"
rust-version = "1.75"
description = "A concise description of what this crate does"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/my-crate"
documentation = "https://docs.rs/my-crate"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["development-tools"]
exclude = [
    "tests/",
    "benches/",
    ".github/",
    "*.profraw",
]
```

```toml
# WRONG: Missing required metadata
[package]
name = "my-crate"
version = "1.0.0"
# Missing: description, license, repository
# crates.io will reject this or it will have poor discoverability
```

### Exclude Unnecessary Files

Use `exclude` to keep the published crate small:

```toml
# CORRECT: Exclude non-essential files
[package]
exclude = [
    ".github/",
    ".gitignore",
    "tests/fixtures/large-data/",
    "benches/",
    "*.profraw",
    "coverage/",
]
```

### Version Crates Independently in Workspaces

When publishing workspace members, each crate should have its own version even if they share
`workspace.package.version`. Use `publish = false` for internal-only crates.

```toml
# Internal crate not meant for crates.io
[package]
name = "project-internal"
version.workspace = true
publish = false
```

## Cargo.lock Policy

### Libraries: Do Not Commit Cargo.lock

Libraries should gitignore `Cargo.lock` because consumers should resolve their own dependency
versions.

```text
# .gitignore for a library
/target
Cargo.lock
```

### Binaries: Commit Cargo.lock

Binary crates (services, CLIs) should commit `Cargo.lock` for reproducible builds.

```text
# .gitignore for a service/CLI
/target
# Note: Cargo.lock is NOT in .gitignore
```

## Conditional Compilation

### Platform-Specific Dependencies

```toml
# CORRECT: Platform-specific dependencies
[target.'cfg(unix)'.dependencies]
nix = "0.29"

[target.'cfg(windows)'.dependencies]
windows = { version = "0.58", features = ["Win32_Foundation"] }
```

### Feature-Gated Dependencies

```toml
# CORRECT: Dependencies only compiled when feature is enabled
[dependencies]
serde = { version = "1", optional = true, features = ["derive"] }
serde_json = { version = "1", optional = true }

[features]
json = ["dep:serde", "dep:serde_json"]
```

## Dependency Auditing

### cargo-deny Configuration

Use `cargo-deny` for comprehensive dependency auditing:

```toml
# deny.toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"

[licenses]
allow = [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-3.0",
]
confidence-threshold = 0.8

[bans]
multiple-versions = "warn"
wildcards = "deny"

deny = [
    # Deny specific problematic crates
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-git = []
```

```toml
# WRONG: No dependency auditing configured
# Vulnerable, unlicensed, or duplicate dependencies go unnoticed
```

### Regular Dependency Updates

```bash
# Check for outdated dependencies
cargo outdated

# Update within semver bounds
cargo update

# Check for security advisories
cargo audit

# Full dependency check
cargo deny check
```

## Rustfmt Configuration

### rustfmt.toml Settings

Keep `rustfmt.toml` minimal. Most defaults are correct.

```toml
# CORRECT: Minimal, intentional rustfmt.toml
edition = "2021"
max_width = 100
use_field_init_shorthand = true
use_try_shorthand = true
```

```toml
# WRONG: Over-configured rustfmt that fights the defaults
edition = "2021"
max_width = 120
tab_spaces = 2
fn_args_layout = "Compressed"
imports_granularity = "Module"
group_imports = "StdExternalCrate"
reorder_imports = false
# Too many non-default settings creates friction for contributors
```
