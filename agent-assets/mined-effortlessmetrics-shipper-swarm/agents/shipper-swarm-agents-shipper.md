# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

This file provides agent-specific guidance for working in crate `shipper`.

## Role

`shipper` is the **install face** of the product, not the engine.

- Binary: `src/bin/shipper.rs` — 3 lines, forwards to `shipper_cli::run()`.
- Library: `src/lib.rs` — curated re-export of `shipper-core`'s public
  surface for drivers that prefer the product name.
- Engine: lives in `shipper-core`.
- CLI: lives in `shipper-cli`.

```text
shipper (this crate)       install target + curated re-export
  -> shipper-cli           clap parsing, subcommand dispatch, output
       -> shipper-core     engine (plan, preflight, publish, resume, …)
```

Behavior changes belong in `shipper-core` (or `shipper-cli` for
CLI-surface changes). This crate's surface should move rarely — it
exists to be a stable "install me" handle.

## Curated re-exports

`src/lib.rs` re-exports: `config`, `engine`, `plan`, `state`, `store`,
`types`. These are the modules a programmatic driver would reach for.

Engine internals (`auth`, `cargo`, `encryption`, `git`, `lock`,
`registry`, `retry`, `runtime`, `webhook`, `cargo_failure`) are
intentionally not re-exported. Reach for them through `shipper-core`
directly if you're embedding.

## Useful commands

```bash
cargo check -p shipper
cargo test -p shipper
cargo test -p shipper --all-features
cargo fmt -p shipper
cargo clippy -p shipper --all-targets --all-features -- -D warnings

# Build + sanity-check the installable binary
cargo build -p shipper --release
./target/release/shipper --help
```

## Context

- Keep changes small. Most real work should happen in `shipper-core`
  or `shipper-cli`, not here.
- Preserve public API compatibility on the curated re-exports. If a
  driver imports `shipper::engine::run_publish`, that path must keep
  working.
- Don't add CLI dependencies (`clap`, `indicatif`, shell completions)
  — those belong in `shipper-cli`.
- Don't add new engine modules here — those belong in `shipper-core`.
- If tests in `tests/` reach beyond the curated façade, update them
  to import from `shipper_core::X` instead (and note it in the PR).

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).
