---
name: "rust-quality"
description: "Use when implementing, refactoring, reviewing, or testing Rust code in SVDO Meter. Enforces repository conventions, correctness, maintainability, error handling, concurrency discipline, testing, dependency hygiene, and CI quality gates."
---

# Rust Quality Standards

## Goal

Produce boring, explicit, maintainable Rust suitable for a long-lived CLI/telemetry product. Prefer correctness, clear ownership, deterministic behavior, testability, and stable boundaries over cleverness or premature abstraction.

These rules apply to all production Rust unless a documented exception exists.

## Toolchain and workspace baseline

Use the current stable Rust toolchain pinned in `rust-toolchain.toml` for reproducible local and CI builds. Use Rust 2024 edition for new crates unless compatibility requirements explicitly dictate otherwise. Cargo workspaces should use resolver version 3.

Root manifest pattern:

```toml
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
edition = "2024"
license = "Apache-2.0"

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"
tracing = "0.1"
```

Centralize shared dependency versions in `[workspace.dependencies]` rather than allowing crates to drift independently without reason.

Commit `Cargo.lock` for the application workspace.

## Formatting and linting

Required CI gates:

```bash
cargo fmt --all -- --check
cargo check --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo deny check
```

Use `cargo test` as the baseline. `cargo nextest` may be used in CI for speed, but standard `cargo test` must continue to work.

Treat Clippy warnings as errors in CI. Do not globally disable broad lint groups to make CI green.

Prefer narrow, local lint exceptions with a reason:

```rust
#[allow(clippy::too_many_arguments)]
// Reason: serialized protocol constructor mirrors external schema.
fn from_wire(...) { ... }
```

Do not use crate-wide `#![allow(clippy::all)]` or equivalent.

## Unsafe Rust

Forbid unsafe code by default across workspace crates:

```toml
[workspace.lints.rust]
unsafe_code = "forbid"
```

If a future requirement genuinely needs unsafe/FFI/platform primitives, isolate that code in a narrowly scoped crate with:

- documented safety invariants;
- targeted tests;
- code ownership/review requirements;
- minimal public surface;
- no `unsafe` escaping into ordinary application code.

Do not relax the entire workspace to support one exceptional integration.

## Module and crate design

A module should have one clear reason to change.

Prefer small public APIs and private implementation details.

Default visibility is private. Use `pub(crate)` before `pub` when external consumers do not need the symbol.

Do not create `utils.rs`, `helpers.rs`, or `common.rs` dumping grounds. Name modules after the domain concept or responsibility:

Prefer:

```text
session.rs
reducer.rs
jsonl.rs
codex.rs
```

Instead of:

```text
utils.rs
helpers.rs
misc.rs
```

Keep Clap parsing and user-facing CLI concerns in the binary crate. Business logic must be callable without Clap.

## Types over primitives

Use domain newtypes when values have distinct meaning or validation.

Prefer:

```rust
pub struct TicketId(String);
pub struct SessionId(String);
pub struct RunId(Uuid);
```

Instead of:

```rust
fn run(ticket: String, session: String, run_id: String)
```

Benefits:

- prevents accidental argument swapping;
- provides a home for validation/formatting;
- makes public APIs self-documenting.

Do not newtype every integer/string mechanically. Use them where semantics matter.

## Ownership and borrowing

Prefer borrowing in read-only APIs when ownership is unnecessary:

```rust
fn normalize(event: &Value) -> Option<MeterEvent>
```

Prefer owned values at asynchronous/task/process boundaries when ownership simplifies lifetime correctness.

Do not introduce complex lifetime signatures merely to avoid a small clone. Clone intentionally where it improves isolation and the data is small; avoid cloning large event payloads in hot paths.

Use `Arc<T>` only for genuinely shared ownership across concurrent tasks. Do not default every service to `Arc<Mutex<T>>`.

## Strings and paths

Use:

- `Path` / `PathBuf` for filesystem paths;
- `OsStr` / `OsString` for process arguments when non-UTF-8 values may exist;
- `String` for true UTF-8 domain text;
- `&str` for borrowed UTF-8 text.

Never assume all filesystem paths are valid UTF-8.

Avoid lossy path conversion except for display/logging, and mark it as display-only.

## Enums over boolean soup

Prefer enums when a flag has semantic states.

Prefer:

```rust
pub enum RawEventRetention {
    Disabled,
    MetadataOnly,
    Full,
}
```

Instead of:

```rust
include_raw: bool,
metadata_only: bool,
```

For independent binary capabilities, booleans may remain appropriate.

## Configuration

Parse configuration into typed structs once at program startup.

Validate configuration before starting a measured run.

Use `#[serde(deny_unknown_fields)]` selectively on user-owned configuration where silently ignoring a typo would be dangerous. Do not use it on external provider event payloads that must tolerate forward-compatible fields.

Do not pass a global untyped JSON value throughout the application.

Use explicit defaults and make them visible/documented.

## Error handling

Library crates use typed errors, normally with `thiserror`.

Example:

```rust
#[derive(Debug, thiserror::Error)]
pub enum HarnessError {
    #[error("failed to start harness process")]
    Spawn(#[source] std::io::Error),

    #[error("harness emitted invalid JSON event")]
    InvalidEvent(#[source] serde_json::Error),

    #[error("harness exited with status {0}")]
    Exit(i32),
}
```

The binary/composition layer may use `anyhow` for top-level context and presentation if desired.

Prefer:

```rust
store.append(&event).await
    .context("failed to append run-start event")?;
```

Instead of:

```rust
.map_err(|_| "something went wrong")?;
```

Preserve error sources. Do not discard diagnostic context.

Do not use `unwrap()` or `expect()` in production paths for recoverable external input, file I/O, subprocess output, network input, configuration, or event parsing.

`expect()` is acceptable only for programmer invariants that are locally obvious and cannot depend on external state; include a message explaining the invariant.

Do not panic because a provider added or omitted an event field.

## Result boundaries

Return errors to the layer that can make a policy decision.

Examples:

- adapter detects malformed provider line → returns/parses into adapter error or records a recoverable parsing diagnostic according to policy;
- engine decides whether malformed optional telemetry should fail the measured run;
- binary converts final error into exit code and human-readable message.

Do not make deep adapter code call `std::process::exit`.

## Async and concurrency

Use Tokio for process/network/file orchestration where asynchronous I/O provides real value.

Do not make pure reducers/domain code async.

Use bounded channels:

```rust
let (tx, rx) = tokio::sync::mpsc::channel(256);
```

Avoid `unbounded_channel()` for provider event streams unless a documented invariant proves bounded production.

Backpressure is preferable to unbounded memory growth.

Never hold a mutex guard across `.await` unless the lock type and design explicitly support it and the critical section is justified.

Prefer actor/task ownership or message passing for mutable async state before introducing shared mutable locks.

Use cancellation-aware loops. Child processes and event writers must terminate predictably when the run is cancelled.

## Blocking work

Do not perform expensive/blocking filesystem, compression, crypto, or CPU-heavy parsing on Tokio worker threads when it can materially block other tasks.

Use `spawn_blocking` for genuinely blocking operations that cannot use async APIs.

Do not wrap tiny synchronous operations in `spawn_blocking` unnecessarily.

## Streams and memory

Provider output is untrusted/unbounded input.

Process incrementally.

Prefer:

```text
read line/event → validate size → parse → normalize → append → discard
```

Instead of:

```text
read entire process output → parse giant Vec<Value> → write at end
```

Define maximum accepted event/line size. Handle oversized records with a typed error or truncation policy; never allocate based solely on an untrusted length without a bound.

Avoid retaining raw provider events in memory after durable append unless needed for a bounded aggregation window.

## Time

Use UTC timestamps for persisted events.

Use monotonic time (`std::time::Instant`) for elapsed-duration measurement.

Do not calculate elapsed durations by subtracting wall-clock timestamps; wall clocks can jump.

Persist wall-clock `occurred_at`/`observed_at` for chronology and monotonic-derived duration fields for elapsed time.

## Serialization

Canonical events use Serde with explicit schema names.

Prefer stable snake_case field names.

Use tagged enums for canonical event variants.

Avoid flattening arbitrary provider fields into the top-level canonical event; names may collide as schemas evolve.

Never serialize internal Rust `Debug` output as an interchange format.

Use integer units for exact machine measurements where practical, e.g. milliseconds/nanoseconds/bytes/tokens.

## Event reducers and reporting

Aggregation logic must be deterministic and testable without I/O.

Prefer:

```rust
let mut reducer = RunReducer::default();
for event in events {
    reducer.apply(&event);
}
let summary = reducer.finish();
```

Instead of updating metrics in multiple unrelated callback locations.

Derived report fields should be functions over factual source data.

Do not persist changing pricing/business logic as if it were an observed provider fact. If cost is reported by a provider, mark it as provider-reported; otherwise compute it in reporting with an explicit pricing/version input.

## Traits and abstraction

Create a trait when there is:

- more than one implementation;
- a clear external boundary;
- a meaningful test seam;
- plugin/adapter behavior that is intentionally replaceable.

Good traits:

```text
HarnessAdapter
EventStore
Connector
Clock (if deterministic tests need one)
```

Avoid traits for every domain struct or one-off helper.

Prefer concrete types internally until polymorphism is actually needed.

## Dynamic dispatch vs enums

Use dynamic dispatch where runtime-selected third-party adapters need a common interface and object safety is straightforward.

Use enums when the closed set is small and compile-time exhaustive matching provides value.

Do not introduce generic type parameters across the entire application solely to eliminate one virtual call in a CLI telemetry product.

Optimize for maintainability before micro-performance.

## Observability

Use `tracing` spans with structured fields:

```rust
tracing::info_span!(
    "harness_run",
    run_id = %run_id,
    ticket_id = %ticket_id,
    harness = harness.name(),
)
```

Do not log prompts, model output, environment variables, auth headers, connector secrets, or raw provider payloads by default.

Use tracing for application diagnostics; canonical telemetry is a separate data product.

## Testing strategy

### Unit tests

Use for:

- event normalization;
- IDs/validation;
- reducers;
- duration/token aggregation;
- config validation;
- error policy.

### Fixture/contract tests

Every harness adapter should have checked-in sanitized fixtures representing provider JSON/event output.

Test:

- first session event;
- token usage;
- command/tool event lifecycle;
- success;
- provider error;
- cancellation where representable;
- unknown/new event kind;
- missing optional field;
- malformed line;
- large-but-valid line boundary.

Do not require Codex/Claude/Gemini credentials in ordinary CI.

### Integration tests

Use a fake executable/script or tiny test fixture binary to verify:

- process argument construction;
- stdout/stderr streaming;
- exit code handling;
- cancellation;
- timeout behavior;
- event persistence order.

Avoid shell-based integration fixtures when testing shell-avoidance guarantees; use a small Rust fixture binary where cross-platform support matters.

### Property tests

Use property-based tests where they add meaningful confidence, especially:

- reducers never panic for arbitrary event ordering permitted by schema;
- normalization never panics on arbitrary valid JSON values;
- JSONL serialize/deserialize round trips;
- ID/config validation invariants.

Do not apply property testing mechanically to simple getters.

### Snapshot tests

Useful for terminal/JSON report formatting and sanitized provider fixtures. Keep snapshots reviewed and deterministic; do not snapshot timestamps/random IDs without normalization.

## Test behavior, not implementation details

Prefer asserting canonical events and summaries.

Instead of asserting every internal function call or mock interaction.

A harness contract test should answer: given this provider stream, what canonical facts are emitted?

## Dependency quality

Before adding a crate, ask:

- Can std/Tokio already do this clearly?
- Is the crate maintained?
- Is the dependency tree reasonable?
- Are default features larger than needed?
- Is the license acceptable?
- Does it introduce native/system dependencies?
- Is it necessary in `meter-core`, or can it stay in an adapter?

Keep HTTP/cloud SDK dependencies out of core crates.

Prefer feature-minimized dependencies when it materially reduces attack surface/compile size, but do not create brittle feature micromanagement without benefit.

Do not use wildcard dependency versions.

## Public API discipline

Treat public structs/enums as commitments even inside a workspace if multiple crates consume them.

Prefer constructors and methods that preserve invariants over making every field public.

Use `#[non_exhaustive]` where external extension of a public enum/struct is expected and semver compatibility matters.

Document behavior and invariants, not obvious syntax.

## Comments

Comment why, not what.

Bad:

```rust
// Increment count
count += 1;
```

Good:

```rust
// Count resumptions separately from runs because a ticket may create a new
// provider session after compaction or user reset.
resumptions += 1;
```

Delete stale comments during refactors.

## This instead of that

### Errors

Use `thiserror` typed errors in library crates.

Instead of `Box<dyn Error>` or string errors everywhere.

### Top-level errors

Use `anyhow` only at application/composition boundaries when convenient.

Instead of leaking `anyhow::Error` throughout reusable core/domain APIs.

### External input

Use fallible parsing and explicit validation.

Instead of `unwrap()` on CLI/provider/file/network data.

### Commands

Use direct argv construction.

Instead of shell command strings.

### State

Use event-derived state and deterministic reducers.

Instead of mutable global singleton metrics.

### Concurrency

Use bounded channels and owned tasks.

Instead of unbounded queues and `Arc<Mutex<_>>` as the default design.

### Paths

Use `PathBuf`/`OsString`.

Instead of UTF-8 `String` for paths/argv.

### Configuration

Use typed structs/enums per harness.

Instead of one `serde_json::Value` tree accessed by magic keys throughout the code.

### Providers

Use fixture-driven adapters tolerant of unknown events.

Instead of compiling provider schema assumptions deeply into reporting.

### Models

Use model selection inside the harness config.

Instead of one adapter implementation per model.

## Definition of done for a Rust change

A change is complete when:

- code is formatted;
- Clippy passes with warnings denied;
- tests cover success and relevant failure paths;
- public API changes are intentional;
- no new `unwrap`/`expect` was added on external input;
- no new shell invocation was added;
- no unbounded channel/buffer was added without documented justification;
- metrics/schema changes include compatibility consideration and tests;
- provider changes include sanitized fixture coverage;
- new dependencies pass license/advisory/source policy;
- operational logs contain no secrets/content by default;
- documentation/config examples are updated when behavior changes.
