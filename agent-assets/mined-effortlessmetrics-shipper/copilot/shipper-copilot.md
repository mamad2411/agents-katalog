# Copilot instructions for shipper

This file collects repository-specific guidance for automated assistants (Copilot/CLI agents) to work effectively in this Rust workspace.

---

## Quick summary

- Repository is a Rust workspace. The product is split across three primary crates: `crates/shipper-core` (engine/library), `crates/shipper-cli` (CLI adapter), and `crates/shipper` (install façade + binary).
- `shipper-core` builds deterministic `ReleasePlan`s and runs preflight / publish / resume / rehearsal flows. `shipper-cli` wraps it with `clap` and owns operator-facing output. `shipper` is what users `cargo install`.

---

## Build, test, and lint commands

From the repository root:

- Build (debug): `cargo build`
- Build (release): `cargo build --release`
- Install the CLI locally (recommended for manual testing):
  - `cargo install --path crates/shipper --locked`
- Run the CLI without installing:
  - `cargo run -p shipper -- <command>` (preferred — runs the `shipper` binary)
  - `cargo run -p shipper-cli -- <command>` (equivalent — same code path)

Tests / single-test usage:
- All workspace tests: `cargo test`
- Engine crate: `cargo test -p shipper-core`
- CLI adapter: `cargo test -p shipper-cli`
- Façade integration tests: `cargo test -p shipper`
- By name: `cargo test -p shipper-core some_test_name`
- Exact: `cargo test -p shipper-core some_test_name -- --exact`
- Integration test binary: `cargo test --test <testname> -p shipper-cli`

Formatting & linting:
- Format: `cargo fmt --all`
- Check formatting (CI): `cargo fmt --all -- --check`
- Clippy (recommended flags): `cargo clippy --workspace --all-targets --all-features -- -D warnings`

Toolchain:
- The workspace declares `rust-version = "1.95"` in `Cargo.toml`.

---

## High-level architecture (big picture)

Three-crate product shape (#95):

```
shipper (install face — carries the `shipper` binary)
  -> shipper-cli (real CLI adapter; pub fn run())
       -> shipper-core (engine — no CLI deps)
```

- `crates/shipper-core` — library only. Modules: `auth`, `cargo`, `cargo_failure`, `config`, `encryption`, `engine` (with `engine::parallel`, `engine::plan_yank`, `engine::fix_forward`), `git`, `lock`, `plan`, `registry`, `retry`, `runtime`, `state`, `store`, `types`, `webhook`. No `clap`. This is the stable embedding surface.
- `crates/shipper-cli` — CLI adapter. Owns argparse, subcommand dispatch, help text, progress rendering. Exposes `pub fn run() -> anyhow::Result<()>`. Both the `shipper` and `shipper-cli` binaries forward to this one function.
- `crates/shipper` — install face. 3-line binary forwarding to `shipper_cli::run()`, plus a library that re-exports a curated subset of `shipper-core` (`engine`, `plan`, `types`, `config`, `state`, `store`) for drivers that prefer the product name. Engine internals (`auth`, `cargo`, `encryption`, `git`, `lock`, `registry`, `retry`, `runtime`, `webhook`) are **not** re-exported here — embedders reach through `shipper-core` directly.

Primary flow (plan → preflight → publish → resume):
  1. Build a deterministic `ReleasePlan` from the workspace manifest (`shipper_core::plan::build_plan` returns `PlannedWorkspace`).
  2. Optionally run preflight checks (git cleanliness, publishability, ownership, registry reachability).
  3. Execute the plan: publish crates one-by-one using `cargo publish -p <crate>` with retry/backoff and verification of registry visibility.
  4. Persist progress to `.shipper/state.json`, the append-only event log `.shipper/events.jsonl`, and an end-of-run `.shipper/receipt.json`.

Persistence & audit:
- By default `.shipper/` lives in the workspace root. Use `--state-dir <path>` to change. Events are the authoritative source of truth; state is a projection; receipts are summaries.

Configuration:
- Project settings via `.shipper.toml` (see `docs/configuration.md`).
- Sections: `[policy]`, `[verify]`, `[readiness]`, `[output]`, `[lock]`, `[retry]`, `[flags]`, `[parallel]`, `[registry]`.
- CLI flags always take precedence over config file values.
- Ownership and git-cleanliness flags live in `[flags]` (not a separate `[preflight]` section).

Registry & auth:
- Shipper performs explicit registry checks (version existence and optional owners checks) and resolves tokens from the standard places: `CARGO_REGISTRY_TOKEN`, `CARGO_REGISTRIES_<NAME>_TOKEN`, or `$CARGO_HOME/credentials.toml`. OIDC / Trusted Publishing is also supported on CI.

Error handling and retries:
- The engine applies exponential backoff with jitter for retryable failures and verifies registry state before treating a step as failed (see `docs/failure-modes.md`).

---

## Where work goes

- Behavior / engine / state / ops changes → `crates/shipper-core`
- CLI changes (arguments, help text, output, subcommands) → `crates/shipper-cli`
- `crates/shipper` itself should rarely move — it's the install face. Only touch it for product-surface decisions (curated re-export list, README, binary wrapper).

## Key conventions and repository-specific patterns

- State files: `.shipper/state.json` (resumable state), `.shipper/events.jsonl` (truth), `.shipper/receipt.json` (summary). Prefer `--state-dir` for CI artifact storage.
- Token resolution: treat tokens as opaque strings; resolve from `CARGO_REGISTRY_TOKEN`, `CARGO_REGISTRIES_<NAME>_TOKEN`, or `CARGO_HOME` credentials.
- Unsafe code: the workspace Cargo.toml sets `unsafe_code = "forbid"` — no unsafe blocks.
- Tests:
  - Many tests use `serial_test` and are intentionally run serially (tests may mutate global env or filesystem); use `#[serial]` in tests that need isolation.
  - Tests mock registry interactions with `tiny_http` — never hit real registries.
  - Snapshot testing uses `insta`. Property-based testing uses `proptest`.
- CLI flags commonly used during development/debugging:
  - `--manifest-path <path>` (defaults to `Cargo.toml`)
  - `--config <path>` to use a custom `.shipper.toml`
  - `--state-dir <path>` to relocate state/receipts
  - `--package` to restrict to specific packages
  - `--skip-ownership-check` and `--strict-ownership` to control owners preflight behavior
  - `--no-verify` to pass `--no-verify` to `cargo publish`
- Config subcommands:
  - `config init` accepts `-o`/`--output`
  - `config validate` accepts `-p`/`--path`
- Readiness config-only settings: `prefer_index` and `index_path` are only settable via `.shipper.toml`, not via CLI flags.

---

## Where to look for more details

- `README.md` (root) — quick start, commands, and install instructions.
- `docs/structure.md` — full workspace and module map for the three-crate shape.
- `docs/architecture.md` — layer boundaries and import rules.
- `docs/configuration.md` — `.shipper.toml` reference with all sections and options.
- `docs/preflight.md` — preflight verification guide.
- `docs/readiness.md` — readiness checking guide.
- `docs/failure-modes.md` — notes on partial publishes, ambiguous timeouts, rate limiting, and CI cancellations.
- `templates/` — example CI workflows for GitHub/GitLab.
- `crates/shipper-core/src/` — engine implementation entry points and module breakdown.
- `crates/shipper-cli/src/` — CLI implementation.

---

## AI assistant / Copilot notes

- `CLAUDE.md` in the repository root provides repo-specific guidance for Claude Code sessions.
- This file (`copilot-instructions.md`) is the primary source of repo-specific guidance for Copilot sessions.

---

If anything should be expanded (more examples, CI-specific notes, or per-crate testing guidance), say which area to expand and a short rationale.
