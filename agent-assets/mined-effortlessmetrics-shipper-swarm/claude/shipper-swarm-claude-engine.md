# Layer: `engine` (orchestration — top of the stack)

**Position in the architecture:** Layer 5 (top). Coordinates all lower layers.

## Single responsibility

Orchestrate the **plan -> preflight -> publish -> resume** pipeline. Loop
through the plan, invoke registry/cargo operations, persist state after each
step, retry on transient failures, classify errors.

## Import rules

`engine` modules MAY import from any layer below: `crate::plan::*`,
`crate::state::*`, `crate::runtime::*`, `crate::ops::*`, `crate::types`, plus
public crates (`shipper_registry`, `shipper_webhook`, `shipper_retry`, etc.).

`engine` is the top of the dependency tree — nothing imports from `engine`
except `lib.rs` re-exports and `shipper-cli`.

## What lives here

- `engine/mod.rs` — current orchestration entry points (`run_preflight`,
  `run_publish`, `run_resume`) and the `Reporter` trait. This file was moved
  verbatim from `crates/shipper/src/engine.rs` when the `engine/` layer dir
  was introduced.
- `engine/execute_package.rs` - canonical per-package Cargo/retry/readiness/
  reconciliation executor. Scheduling belongs to mode-specific scheduler
  modules; durable package outcomes belong here and in `transition.rs`.
- `engine/reconcile.rs` - ambiguous-publish reconciliation against registry
  truth (`Published` / `NotPublished` / `StillUnknown`).
- `engine/test_readiness.rs` - test-only reporter/event adapter for the
  engine-level readiness characterization tests.

## Readiness ownership (issue #202)

The readiness **polling loop** — backoff, jitter, `index_path` handling,
sparse-index fallback, and `ReadinessEvidence` — is owned by
`shipper_registry::RegistryClient::is_version_visible_with_backoff{,_and_events}`.
There is no engine-side copy; `engine/readiness.rs` was deleted. Call the
`RegistryClient` method directly from `execute_package.rs` and `reconcile.rs`
— do **not** reintroduce a forwarding wrapper.

What the engine owns is the *envelope* around a poll run, because
`shipper-registry` cannot depend on `shipper-core` and therefore has no
knowledge of `EventLog`, `events.jsonl`, or `Reporter`:

- the `ReadinessStarted` / `ReadinessComplete` / `ReadinessTimeout` /
  `ReadinessError` events,
- the `Reporter` narration, and
- flushing each emitted event through the event log.

Production code applies that envelope inline in `execute_package.rs`;
`test_readiness.rs` mirrors it for tests. Behavior changes to the loop belong
in `crates/shipper-registry/src/context.rs`.
- `engine/parallel/` — wave-based parallel publish (was the standalone
  `shipper-engine-parallel` crate, absorbed in the same PR that created this
  layer dir).
- Future: `engine/preflight/`, `engine/publish/`, and `engine/resume/` as
  `engine/mod.rs` gets split up.
