# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::ops::cargo`

**Layer:** ops (layer 1, bottom)
**Single responsibility:** Shell out to `cargo metadata` and `cargo publish` and return the captured/truncated output.
**Was:** standalone crate `shipper-cargo` (absorbed during decrating Phase 2).

## Public-to-crate API

Public module path: `shipper_core::cargo`. Inside `shipper-core` itself, use
`crate::cargo`. The install-facing `shipper` facade does not re-export this
module.

- `CargoOutput` — value type: exit code, stdout/stderr tails, duration, timed-out flag.
- `cargo_publish(workspace_root, package, registry, allow_dirty, no_verify, output_lines, timeout)` — spawn `cargo publish -p <pkg>` with optional wall-clock timeout.
- `cargo_publish_dry_run_workspace` / `cargo_publish_dry_run_package` — dry-run variants.
- `load_metadata(manifest_path)` — invokes `cargo metadata`; used by `crate::plan`.
- `WorkspaceMetadata` — thin wrapper around `cargo_metadata::Metadata` with helpers (`publishable_packages`, `topological_order`, `workspace_members`, etc.).
- `PackageInfo` — serializable package summary.
- `is_valid_package_name(name)` — crates.io naming rule check.
- `workspace_member_names(&metadata)` — convenience.
- `get_version(manifest_path)` / `get_package_name(manifest_path)` — root-package introspection helpers.
- `pub use shipper_output_sanitizer::redact_sensitive;` — re-export; callers that log cargo output should funnel it through here.

## Invariants & gotchas

- **`SHIPPER_CARGO_BIN` override.** `cargo_program()` returns `$SHIPPER_CARGO_BIN` if set (used by tests to point at fake cargo binaries), else `"cargo"`. An empty string env var is NOT treated as unset — it is passed through verbatim.
- **Timeout is a polling loop.** `cargo_publish` with `Some(timeout)` polls `try_wait` every 100ms and SIGKILLs on deadline; on timeout the returned `CargoOutput` has `timed_out: true`, `exit_code: -1`, and a stderr tail annotated with `cargo publish timed out after ...`.
- **Output is always tailed + redacted.** Every `CargoOutput.stdout_tail` / `stderr_tail` is passed through `shipper_output_sanitizer::tail_lines`, which internally applies `redact_sensitive`. Callers can assume bearer tokens / `CARGO_REGISTRY_TOKEN=` values / `CARGO_REGISTRIES_<NAME>_TOKEN=` values are `[REDACTED]` before they ever reach `receipt.json` or the event log.
- **Redaction is idempotent** (see `redact_is_idempotent_*` tests).
- **Non-default registries only.** `--registry` is passed through only when the registry name is non-empty and not literally `crates-io`; the crates.io default is implicit.
- **`WorkspaceMetadata::is_publishable`** treats version `0.0.0` as non-publishable and `publish = []` as non-publishable, matching Cargo's own semantics.
- **`topological_order`** is a DFS-based visitor (distinct from the Kahn/BTreeSet sort in `crate::plan`). It's still useful for diagnostics; production planning goes through `crate::plan::build_release_plan`.

## Architectural notes

- Layer-1 pure I/O. Must not import from `engine`, `plan`, `state`, or `runtime` (enforced by `.github/workflows/architecture-guard.yml`).
- Depends on `crate::ops::process` for the timeout-aware subprocess primitive; all subprocess spawning goes through there so Windows/Unix timeout handling is unified.
- External deps: `anyhow`, `cargo_metadata`, `serde`, `shipper_output_sanitizer`.

