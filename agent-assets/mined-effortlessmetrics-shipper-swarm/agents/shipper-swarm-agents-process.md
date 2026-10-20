# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Layer: `ops::process` (process execution)

**Position:** Layer 1 (ops). Crate-private submodule of `shipper-core`.

## Single responsibility

Cross-platform command execution: spawn child processes, capture stdout/stderr,
apply optional timeouts, and shell out to `cargo`. Used by `ops::cargo` to
invoke `cargo publish`, `cargo package`, and friends with retry-friendly
result types.

## What lives here

- `types` — `CommandResult` and `CommandOutput` result types (serde-friendly).
- `run` — Basic command runners: `run_command`, `run_command_in_dir`,
  `run_command_with_env`, `run_command_streaming`, `run_command_simple`.
- `timeout` — `run_command_with_timeout` which polls the child and kills it
  if it exceeds the deadline.
- `which` — `command_exists`/`which` helpers delegating to the `which` crate.
- `cargo` — `run_cargo`, `run_cargo_in_dir`, `cargo_dry_run`, `cargo_publish`
  convenience wrappers.

## Import rules

`ops::process` is Layer 1:
- MUST NOT import from `crate::engine`, `crate::plan`, `crate::state`, `crate::runtime`.
- MAY import from `crate::types` and external crates.

## Visibility

Everything in this subsystem is `pub(crate)`. None of it is part of shipper-core's
public API — it's an internal implementation detail that callers (primarily
`ops::cargo`) consume via the `ops::process` facade.

## History

Absorbed from the standalone `shipper-process` microcrate (1948 LOC) in the
Phase 2 decrating effort. See `docs/decrating-plan.md` §6.

