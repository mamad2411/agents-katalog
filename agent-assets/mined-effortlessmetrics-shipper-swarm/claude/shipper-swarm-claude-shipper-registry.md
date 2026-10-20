# CLAUDE.md

This file provides agent-specific guidance for working in crate shipper-registry.

## Scope

- Crate: shipper-registry
- Path: crates/shipper-registry
- Workspace root: h:\Code\Rust\shipper
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-registry
cargo test -p shipper-registry
cargo test -p shipper-registry --all-features
cargo fmt -p shipper-registry
cargo clippy -p shipper-registry --all-targets --all-features -- -D warnings
```

## Readiness ownership (issue #202)

`RegistryClient::is_version_visible_with_backoff{,_and_events}` in
`src/context.rs` is the **single** readiness polling loop for the workspace.
`shipper-core`'s engine calls straight into it and keeps no copy, so changes
here change engine behavior — treat it as production orchestration code, not
a convenience helper.

Two properties are load-bearing and covered by tests in this crate:

- **Local index reads are offline.** When `ReadinessConfig::index_path` is
  set, `visible_via_index` reads that file and parses it with
  `shipper_sparse_index::contains_version`; it must not issue an HTTP
  request. Tests assert a request count of zero against a counting mock.
- **`ReadinessEvidence::delay_before` is the delay actually slept**, carried
  forward in `pending_delay`, and equal to the `delay_ms` of the matching
  `ReadinessPollScheduled` event. Never recompute it with a fresh jitter draw.

The `ReadinessStarted` / `ReadinessComplete` / `ReadinessTimeout` /
`ReadinessError` envelope,
`Reporter` narration, and event-log persistence stay in `shipper-core`. This
crate must not learn about `EventLog`, `events.jsonl`, or `Reporter` — that
would invert the crate dependency.

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).
