---
name: rust-crate-setup
description: >
  Maps and enforces the path-rs Rust library crate layout, feature flags, module
  boundaries, public API re-exports, testing matrix, examples, benches, CI gates,
  MSRV, and coding conventions. Use when working in path-rs, adding modules or
  public APIs, wiring Cargo features, writing integration/edge tests or examples,
  packaging for crates.io, or when the user runs /rust-crate-setup. Triggers:
  path-rs setup, crate structure, Cargo.toml features, module organization,
  rustdoc missing_docs, CI matrix, MSRV 1.85, dual license, lexical vs canonicalize.
---

# path-rs crate setup

Load this skill before changing crate layout, features, public exports, tests, examples, benches, or CI. This is a **single-package library crate** (not a workspace). Package name `path-rs`; Rust crate/module path `path_rs`.

## Identity

| Field | Value |
| --- | --- |
| Package | `path-rs` |
| Edition | `2024` |
| MSRV | `1.85` (`rust-version` + `clippy.toml` `msrv`) |
| License | MIT OR Apache-2.0 |
| Repo | https://github.com/xylex-group/path-rs |
| Role | Complements `std::path::{Path, PathBuf}` — does **not** replace them |

Internal path representation is always `Path` / `PathBuf` / `OsStr`. Never use `String` as a filesystem path or string-concatenate path segments.

## Architectural boundary

Provide **generic path mechanics** only:

- expansion, lexical normalize/resolve, platform dirs, listing, search, cache, identity keys

Do **not** put product-specific logic in this crate (repo inventories, VCS roots, watchers, cloud remotes, mutation stores). Those belong in application adapters that compose these APIs.

## Layout

```text
path-rs/
├── Cargo.toml              # package, features, optional deps, [[example]]/[[test]]/[[bench]]
├── src/
│   ├── lib.rs              # crate root: modules, feature-gated re-exports, crate docs
│   ├── error.rs            # PathError (thiserror, #[non_exhaustive])
│   ├── internal/           # pub(crate) only — components, validation
│   ├── expand.rs, normalize.rs, resolve.rs, platform.rs, dirs.rs, …
│   ├── listing.rs, discovery.rs, search.rs  # feature-gated modules
│   └── cache.rs            # always present; PersistentCache feature-gated
├── tests/                  # integration + edge_* suites (many need required-features)
├── examples/               # one binary per surface; some need required-features
├── benches/                # criterion, harness = false
├── rustfmt.toml / clippy.toml / deny.toml
├── .github/workflows/      # ci.yml, release.yml, security.yml
└── README.md, CHANGELOG.md, SECURITY.md, CONTRIBUTING.md, LICENSE-*
```

`Cargo.toml` `include` is the publish allowlist — keep source, examples, tests, benches, README, CHANGELOG, licenses, and `Cargo.toml` only.

## Feature flags

| Feature | Default? | Optional deps | Exposes |
| --- | ---: | --- | --- |
| `listing` | yes | `walkdir` | `listing`, `discovery` modules |
| `search` | yes | `globset` (+ implies `listing`) | `search` module |
| `persistent-cache` | no | `serde`, `serde_json` | `cache::PersistentCache` |
| `unicode` | no | `unicode-normalization` | `logical_path_key` |
| `async` | no | `tokio` (`fs`, `rt`) | spawn_blocking wrappers on list/search |

Always-on surface (no feature): expand, normalize, resolve, platform, dirs, identity, inspect, match_path, metadata helpers, text/utf8, in-memory `cache`, `PathError`.

When adding a feature:

1. Declare optional dep + feature in `Cargo.toml`.
2. Gate module with `#[cfg(feature = "...")]` and `#[cfg_attr(docsrs, doc(cfg(...)))]`.
3. Re-export public items from `lib.rs` under the same gates.
4. Add `[[example]]` / `[[test]]` / `[[bench]]` `required-features` when the binary needs them.
5. Document the flag in `lib.rs` crate docs and README.
6. Verify `cargo check --no-default-features` and `cargo check --all-features`.

docs.rs metadata:

```toml
[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
```

## Module and API conventions

### lib.rs

- `#![deny(missing_docs)]` and `#![warn(rust_2018_idioms)]`
- `#![cfg_attr(docsrs, feature(doc_cfg))]`
- Private `mod foo;` for always-on modules; `pub mod` only when the module is a documented public namespace (`listing`, `discovery`, `search`, `cache`)
- Prefer re-exporting leaf items from `lib.rs` so callers use `path_rs::normalize` not deep paths
- Crate-level rustdoc must keep the **operation matrix** (filesystem access / existence / symlinks) accurate

### Per-module files

- Module rustdoc states whether the API does I/O, needs existence, and follows symlinks
- Public functions take `impl AsRef<Path>` where natural; return `Result<…, PathError>` for fallible work
- Options structs use field-init-friendly public fields + `Default` when applicable
- Unit tests live in the same file under `#[cfg(test)]` for focused logic
- Shared path-component / NUL checks go in `src/internal/` (`pub(crate)`), not duplicated

### Errors

- Single public error: `PathError` in `error.rs` (`thiserror`, `#[non_exhaustive]`)
- Prefer structured variants with context fields over bare strings
- Do not leak third-party error types as public fields unless necessary
- Match style of existing constructors/helpers when adding variants

### Security / semantics (do not regress)

1. Lexical APIs must not hide filesystem I/O.
2. Do not follow symlinks by default.
3. Do not enable caching by default.
4. Lexical root containment is not symlink-safe — document that.
5. Never expand shell command substitution (`$(…)`, backticks).
6. Reject Windows drive-relative paths (`C:foo`, `C:`) where the rest of the crate does.

## Dependencies

| Kind | Crates |
| --- | --- |
| Always | `thiserror`, `dirs`, `dunce` |
| Optional | `walkdir`, `globset`, `serde`/`serde_json`, `unicode-normalization`, `tokio` |
| Dev | `tempfile`, `assert_fs`, `proptest`, `criterion` |

Prefer small, well-known crates. Run license/source policy via `deny.toml` (crates.io only; allowlisted licenses). Clippy: `avoid-breaking-exported-api = true`.

## Tests

### Layers

| Layer | Location | Purpose |
| --- | --- | --- |
| Unit | `src/**/*.rs` `#[cfg(test)]` | Pure logic, platform `cfg` branches |
| Integration | `tests/*.rs` | Public API black-box |
| Edge | `tests/edge_*.rs` | Boundary / OS / error / feature edge cases |
| Property | `proptest!` in integration or unit | Idempotence / invariants |

### Feature-gated tests

Tests that need `listing`/`search` must be declared in `Cargo.toml`:

```toml
[[test]]
name = "listing"
required-features = ["listing"]
```

Without `required-features`, `cargo test --no-default-features` will fail to compile those targets.

### Platform gates

Use `#[cfg(unix)]` / `#[cfg(windows)]` for OS-specific expectations (drive letters, UNC, Unix root). Keep shared cases portable.

### When fixing a bug

Add a regression test that fails before the fix (integration or edge preferred for public API). Name tests after behavior, not ticket IDs alone.

## Examples and benches

- **Examples**: short binaries under `examples/`; return `Result<(), path_rs::PathError>` or print clearly. Register `required-features` in `Cargo.toml` when needed.
- **Benches**: Criterion, `harness = false`, `black_box` inputs. Gate listing/search benches with features.

Run:

```bash
cargo run --example normalize
cargo run --example search --features search
cargo bench --bench normalize
```

## Local and CI verification

Mirror `CONTRIBUTING.md` and `.github/workflows/ci.yml`:

```bash
cargo fmt --all -- --check
cargo check
cargo check --no-default-features
cargo check --all-features
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
cargo test --no-default-features
cargo doc --all-features --no-deps
# MSRV (CI uses 1.85):
cargo +1.85 check --all-features
# Publish hygiene:
cargo package
cargo publish --dry-run
```

CI matrix: **ubuntu / macos / windows**, plus separate MSRV and package jobs. `RUSTFLAGS: -D warnings` and `RUSTDOCFLAGS: -D warnings` in CI — treat warnings as errors.

## Adding a new public API (checklist)

1. Choose the owning module (or new `src/<name>.rs` + `mod` in `lib.rs`).
2. Document FS access / existence / symlink behavior in rustdoc.
3. Return `PathError`; keep options explicit (no silent I/O or cache).
4. Re-export from `lib.rs` (feature-gated if needed).
5. Unit tests + integration and/or `edge_*` coverage.
6. Example snippet if user-facing and non-obvious.
7. Update crate-level operation matrix in `lib.rs` and README when the matrix changes.
8. Run full feature matrix checks above.
9. Prefer small, reviewable PRs; imperative commit subjects (`fix: …`, `feat: …`).

## What not to do

- Do not introduce a Cargo workspace unless explicitly requested.
- Do not replace `Path`/`PathBuf` with string path types.
- Do not add network, process, or VCS dependencies for core path work.
- Do not `git add` publish-excluded junk; respect `include` and dual license files.
- Do not weaken `missing_docs` or skip feature-gated `doc(cfg)` on new gated exports.

## Quick map: source modules

| Module | Responsibility |
| --- | --- |
| `expand` | `~`, `%VAR%`, `$VAR` / `${VAR}`, optional WSL translate |
| `normalize` | Lexical normalize vs `canonicalize_existing` |
| `resolve` | absolute, resolve_against, join_relative, resolve_inside |
| `platform` | Drive-relative, UNC, verbatim, reserved names, WSL, display simplify |
| `dirs` | Platform dirs + `app_paths` policies |
| `identity` | Path identity keys, dedup, display |
| `inspect` | Directory existence / inspection summaries |
| `match_path` | Executable / command-line path matching (no process exec) |
| `metadata` | `FileEntry`, sort, traversal error policy |
| `text` / `utf8` | Token normalization; UTF-8 conversion; optional NFC key |
| `listing` / `discovery` / `search` | Walk, visit, glob/predicate search (features) |
| `cache` | Memory + optional persistent discovery cache |
| `containment` | Lexical inside/ensure_inside |
| `internal` | Shared validation and component helpers |
