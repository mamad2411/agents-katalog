# AGENTS.md

## Repository role

`EffortlessMetrics/shipper-swarm` is the active development repository.
`EffortlessMetrics/shipper` remains the release authority for crates.io
publishing, release evidence, tags, and signing credentials until that
authority is explicitly moved.

Normal PRs into `shipper-swarm/main` are squash-merged. Syncs from
`shipper-swarm/main` back to `shipper/main` use merge commits and must not be
squashed or rebased. See
[docs/status/SWARM_OPERATION.md](docs/status/SWARM_OPERATION.md).

Do not add crates.io publish tokens, release signing secrets, or release
workflow credentials to `shipper-swarm`.

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Orientation

- [**MISSION.md**](MISSION.md) — north star: mission, vision, audience, beliefs. Read before scoping non-trivial work.
- [**ROADMAP.md**](ROADMAP.md) — five pillars + nine-competency thesis, current status, now/next/later sequencing.
- [**docs/README.md**](docs/README.md) — documentation index (Diátaxis: tutorials/how-to/reference/explanation).
- [**docs/explanation/why-shipper.md**](docs/explanation/why-shipper.md) — the *why*, distilled.
- [**docs/product.md**](docs/product.md), [**docs/structure.md**](docs/structure.md), [**docs/tech.md**](docs/tech.md) — steering docs.
- [**docs/INVARIANTS.md**](docs/INVARIANTS.md) — events-as-truth contract.
- [**docs/status/SWARM_OPERATION.md**](docs/status/SWARM_OPERATION.md) — active-development repo, merge policy, and sync policy.
- [**docs/status/SWARM_SYNC.md**](docs/status/SWARM_SYNC.md) — release-authority repo sync policy imported from `shipper`.

## Useful command entry points

```bash
# Build
cargo build                    # debug
cargo build --release          # release (LTO + strip)

# Run CLI during development (without installing)
cargo run -p shipper -- <command>       # preferred: runs the `shipper` binary
cargo run -p shipper-cli -- <command>   # equivalent; same code path

# Install CLI locally
cargo install --path crates/shipper --locked

# Tests
cargo test                                         # all workspace tests
cargo test -p shipper-core                         # engine crate
cargo test -p shipper-cli                          # CLI adapter crate
cargo test -p shipper                              # façade (integration tests)
cargo test -p shipper-core some_test_name          # substring match
cargo test -p shipper-core some_test_name -- --exact # exact match
cargo test --test cli_e2e -p shipper-cli           # CLI integration tests only

# Lint & format
cargo fmt --all
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
```

## Architecture

Three-crate product shape (#95):

```
shipper (install face — carries the `shipper` binary + curated lib re-export)
  -> shipper-cli (real CLI adapter; exposes pub fn run())
       -> shipper-core (engine — no CLI deps, stable embedding surface)
```

- **`crates/shipper-core`** — all engine/library logic: plan, preflight, publish, resume, state, ops. No `clap`, no `indicatif`. This is where behavior changes land.
- **`crates/shipper-cli`** — CLI adapter. Owns `clap` derive types, subcommand dispatch, help text, progress rendering. Exposes `pub fn run() -> anyhow::Result<()>` as the embedding entry point.
- **`crates/shipper`** — install façade. 3-line binary forwarding to `shipper_cli::run()`, plus a library that re-exports a curated subset of `shipper-core` (`engine`, `plan`, `types`, `config`, `state`, `store`) for drivers that prefer the product name. Changes rarely.

When touching code: behavior work lives in `shipper-core`; CLI work (arguments, help text, output) lives in `shipper-cli`; the `shipper` crate mostly shouldn't move.

### Publishing Pipeline

The core flow is: **plan → preflight → publish → (resume if interrupted)**

1. **Plan** (`shipper-core/src/plan/`): Reads workspace via `cargo_metadata`, filters publishable crates, topologically sorts by intra-workspace dependencies (Kahn's algorithm with BTreeSet for determinism), generates a SHA256-based plan ID.
2. **Preflight** (`shipper-core/src/engine/`): Validates git cleanliness, registry reachability, dry-run, version existence, and optional ownership checks. Produces a `Finishability` assessment (Proven/NotProven/Failed).
3. **Publish** (`shipper-core/src/engine/`): Executes plan one crate at a time with retry/backoff. After each `cargo publish`, verifies registry visibility (API or sparse index) before proceeding. Persists `ExecutionState` to disk after every step for resumability.
4. **Resume**: Reloads state from `.shipper/state.json`, validates plan ID match, skips already-published packages, continues from first pending/failed.

### Key Abstractions

- **`StateStore` trait** (`shipper-core/src/state/store/`): Persistence abstraction for state/receipt/events. Currently filesystem-backed; designed for future cloud storage backends.
- **`Reporter` trait** (`shipper-core/src/engine/`): Pluggable output handler for publish/preflight progress.
- **`ErrorClass`** enum: Classifies failures as `Retryable` (HTTP 429, network), `Permanent` (auth, version conflict), or `Ambiguous` (upload may have succeeded despite client error). Only retryable errors trigger backoff retries.
- **`PublishPolicy`/`VerifyMode`/`ReadinessMethod`**: Configuration enums controlling safety vs speed tradeoffs.

### State Files

Written to `.shipper/` (configurable via `--state-dir`):
- `state.json` — resumable execution state (schema-versioned). **Projection** of events.
- `receipt.json` — audit receipt with evidence (stdout/stderr, exit codes, git context, environment fingerprint). **Summary** derived at end-of-run.
- `events.jsonl` — append-only event log. **Authoritative truth.**
- `lock` — distributed lock preventing concurrent publishes

### Events-as-truth invariant

`events.jsonl` is authoritative; `state.json` is a projection; `receipt.json` is a summary. See [docs/INVARIANTS.md](docs/INVARIANTS.md). When the three disagree, events win — and a drift is a bug. Tooling that needs ground truth should read events; tooling that needs fast "what's done" can read state.

In `state.json`, package status is at `.packages[].state.state`, not `.packages[].status` — common source of misreads.

## Product context

[**MISSION.md**](MISSION.md) is the north star — mission, vision, audience, and the nine convictions that produce every design decision. Read it before scoping non-trivial work.

Cargo 1.90 stabilized multi-package workspace publishing. Shipper's value is what Cargo still doesn't do, organized as nine competencies: **Prove, Survive, Reconcile, Narrate, Remediate, Harden, Profile, Integrate, Ergonomics**. See [ROADMAP.md](ROADMAP.md) and master tracking issue [#109](https://github.com/EffortlessMetrics/shipper/issues/109). **Reconcile is now stable:** ambiguous `cargo publish` outcomes must reconcile against registry truth and stop on `StillUnknown` instead of blind-retrying. The current open proof lane is Trusted Publishing default evidence; keep fallback/default claims bounded by `.shipper-meta/goals/active.toml` and [docs/status/SUPPORT_TIERS.md](docs/status/SUPPORT_TIERS.md).

## Conventions

- **`unsafe_code = "forbid"`** is enforced workspace-wide. No unsafe blocks.
- Edition 2024, MSRV 1.95, resolver v3.
- Tests that mutate environment variables or filesystem use `#[serial]` from `serial_test` for isolation.
- Registry interactions in tests use `tiny_http` mock servers, never real registries.
- Snapshot tests use `insta`. Property-based tests use `proptest`.
- Token resolution follows Cargo conventions: `CARGO_REGISTRY_TOKEN` → `CARGO_REGISTRIES_<NAME>_TOKEN` → `$CARGO_HOME/credentials.toml`. Tokens are opaque strings, never logged.
- Configuration can be set via `.shipper.toml` in workspace root; CLI flags override config file values. Config sections: `[policy]`, `[verify]`, `[readiness]`, `[output]`, `[lock]`, `[retry]`, `[flags]`, `[parallel]`, `[registry]`. Ownership/git settings live in `[flags]`, not a separate `[preflight]` section.
- `config init` uses `-o`/`--output`; `config validate` uses `-p`/`--path`.
- `prefer_index` and `index_path` (readiness) are config-file-only settings with no CLI flags.

## Automated review

Factory Droid runs automated review and security review on same-repo PRs and on the `@droid` mention. Review output is treated as a repair queue consumed by follow-up coding agents, not as a human approval signal.

- [`.factory/skills/review-guidelines/SKILL.md`](.factory/skills/review-guidelines/SKILL.md) — the active review skill: product contract, finding format, no-naked-LGTM record, evidence provenance, notification hygiene.
- [`.factory/rules/droid-review.md`](.factory/rules/droid-review.md) — the compact rule version: clean-review requirements, priority surfaces, repo lenses.
- [`docs/agent-context/review-invariants.md`](docs/agent-context/review-invariants.md) — durable product, CI, and Droid-workflow invariants a reviewer can rely on.
- [`docs/agent-context/droid-smoke-tests.md`](docs/agent-context/droid-smoke-tests.md) — how to verify the Droid workflows after a change.

When changing `.github/workflows/droid*.yml`, `.factory/`, or `docs/agent-context/`, follow the smoke-test procedure and update `review-invariants.md` if any invariant changes.
