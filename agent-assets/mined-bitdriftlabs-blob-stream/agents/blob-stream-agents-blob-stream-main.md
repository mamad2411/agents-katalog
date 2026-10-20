# Agent Guidelines

- [DEVELOPMENT.md](DEVELOPMENT.md) is the canonical human workflow reference.
- Use [bitdriftlabs/ai-instructions](https://github.com/bitdriftlabs/ai-instructions) for shared
  language and style guidance. Resolve Rust commands from the command-owning checkout root: a
  standalone Blob Stream checkout uses Cargo by default; a nested monorepo checkout follows the
  enclosing monorepo's Bazel execution profile and its `AGENTS.md`. The rules below apply in both
  contexts unless marked as monorepo-specific.

## Architecture Changes

- Read the [Design overview](docs/design/README.md) before changing architecture-sensitive behavior.
- Update the owning document in `docs/design/` in the same change when altering wire protocol,
  partitioning or routing, lease or sequence behavior, durable storage layout, delivery or cursor
  guarantees, consumer coordination, or an operational contract.
- Use [Infrastructure setup](docs/infrastructure.md) and [Operations](docs/operations.md) as the
  sources for deployment and runbook documentation. Do not duplicate those contracts elsewhere.
- Write documentation as a current-state reference. Do not retain migration history, removed
  controls, or impossible configuration paths in current configuration and operations documents.

## Rust Assertions

- Do not use `assert!` in production code. Conditions reachable from configuration, network data,
  user input, or external state must return an error or be rejected at the earliest normal boundary.
- Use `debug_assert!` freely for internal invariants whose violation indicates a programming defect.
  In hot or locked code, validate and construct errors before entering the path, then keep a nearby
  debug assertion to document the proven invariant.
- Test code may use ordinary assertions.

## Deterministic Integration Tests

Follow [plans/TEST_AUDIT.md](plans/TEST_AUDIT.md). In addition:

- For `ManualTimeProvider`, advance logical time only after a lifecycle gate or registered logical
  sleep. Never make a test pass by adding a wall-clock sleep or extending a wall-clock deadline.

### Monorepo Bazel Tests

Run these commands from the `blob-stream` directory inside the monorepo; from the monorepo root,
use `./bazelw` instead.

- Validate an edited test with `--nocache_test_results`, and wait for a prior Bazel command to finish
  before editing its inputs. Bazel intentionally avoids caching outputs built while sources change.
- Run service-backed integration tests through generated Nextest wrappers, never a raw `__libtest`
  target. For example:

  ```sh
  ../bazelw test --nocache_test_results --test_output=streamed \
    --test_arg=-E \
    --test_arg='test(lease_expiry_takeover_preserves_progress)' \
    //blob-stream/blob-stream-integration-tests:end-to-end-test
  ```

- `--test_filter` selects a Bazel target; use Nextest expressions through `--test_arg` to select one
  Rust test.
- Pass logs through Bazel with `--test_env`, for example
  `--test_env=RUST_LOG=blob_stream=debug,bd=debug`.
- Prove a deflaked test with uncached serial repetitions:

  ```sh
  ../bazelw test --nocache_test_results --runs_per_test=25 --local_test_jobs=1 \
    --test_arg=-E \
    --test_arg='test(lease_expiry_takeover_preserves_progress)' \
    //blob-stream/blob-stream-integration-tests:end-to-end-test
  ```

## Telemetry

- Add focused debug or trace logs around unclear asynchronous, concurrent, or lifecycle transitions.
  Keep logs that provide durable operational observability. Use trace only when debug output does
  not explain the relevant state transition.
- Assert metrics in tests through `bd_server_stats::test::util::stats::Helper`; do not serialize
  Prometheus output and match raw text.
- Exported OTEL spans support at most 16 attributes. Put additional correlated recovery or handoff
  state in a bounded JSON attribute such as `recovery.summary_json` or `handoff.snapshot_json`.
- Add a metric only when it has operational value that cannot be derived from existing metrics.
