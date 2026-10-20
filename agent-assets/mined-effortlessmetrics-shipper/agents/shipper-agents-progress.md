# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::output::progress`

**Crate:** `shipper-cli`
**Single responsibility:** Per-crate publish progress UI — progress bars, status indicators, elapsed-time display.
**Was:** standalone crate `shipper-progress` (absorbed into `shipper-cli` during decrating Phase 5).

## Public-to-crate API

- `ProgressReporter` — the main reporter struct.
  - `::new(total_packages, quiet)` — construct with TTY autodetection.
  - `::silent(total_packages)` — non-TTY reporter used by tests.
  - `set_package(index, name, version)` — record the active package.
  - `finish_package()` — mark the current package complete.
  - `set_status(status)` — update the current status message.
  - `finish()` — finalize reporting.
- `is_tty()` — helper reporting whether stdout is a terminal.

## Layout

- `mod.rs` — production code: `ProgressReporter`, `is_tty()`.
- `tests.rs` — unit tests.
- `proptests.rs` — property-based tests (was `mod property_tests` + `mod proptests`).
- `bdd_tests.rs` — behavior-style tests (was `tests/progress_bdd.rs`).
- `snapshot_tests.rs` — `insta` snapshot tests (was `tests/snapshots.rs`).
- `snapshots/` — `insta` snapshot files.

## Invariants

- Detects TTY vs non-TTY output and degrades gracefully (no spinner spam in CI logs).
- Silent / quiet mode fully suppresses output.
- `total_packages()` is immutable after construction.
- `current_name()` always has the form `"name@version"` after `set_package`.

