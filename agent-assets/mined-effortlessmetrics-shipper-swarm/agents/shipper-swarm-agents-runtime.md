# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `shipper_config::runtime`

**Crate:** `shipper-config`
**Single responsibility:** Convert `shipper-config` types (config file structures) into `shipper-types::RuntimeOptions` (the runtime-options shape the engine consumes).
**Was:** standalone crate `shipper-config-runtime` (absorbed into `shipper-config::runtime` during Phase 5 of the decrating effort).

## Public API

- `pub fn into_runtime_options(value: crate::RuntimeOptions) -> shipper_types::RuntimeOptions`

## Why this lives in shipper-config (not in shipper)

This is a pure adapter from config-shape to types-shape. It has no I/O, no orchestration, and no policy decisions. The split as a separate crate was unnecessary microcrating; the conversion naturally belongs next to the config types it reshapes.

## Tests

- Unit tests: `crates/shipper-config/src/runtime/mod.rs` (`#[cfg(test)] mod tests`), including `snapshot_tests`, `flag_precedence`, `default_value_tests`, `partial_config_tests`, `policy_combination_tests`, `registry_tests`, `proptest_hardened`, `composite_tests`.
- Integration tests: `crates/shipper-config/tests/config_runtime_bdd.rs`, `config_runtime_contract.rs`, `config_runtime_proptest.rs`.
- Snapshots: `crates/shipper-config/src/runtime/snapshots/` (prefix `shipper_config__runtime__...`).

