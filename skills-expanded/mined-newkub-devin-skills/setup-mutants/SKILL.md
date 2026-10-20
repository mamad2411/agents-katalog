---
name: follow-tool-mutants-rs-setup-mutants
description: Install cargo-mutants with a config file and a baseline run for Rust projects
argument-hint: "[scope]"
related:
  - follow-tool-mutants-rs
  - follow-lang-rust
  - follow-tool-cargo
  - follow-tool-nextest
  - run-test
---

## Goal

Install and configure cargo-mutants so mutation testing runs on a Rust project — install, `.cargo/mutants.toml`, baseline run

## Scope

- First-time setup of cargo-mutants in a Cargo workspace/project
- Covers: install, config file, baseline run, verify output
- Doesn't cover: sharding/CI optimization (`workflows/optimize mutation`)

## Execute

### 1. Check Prerequisites

> Goal: check the environment and test suite before install

1. Verify it's a Cargo project (`Cargo.toml` at the root) — do `/follow-tool-cargo` if cargo needs setup first
2. Run `cargo test` or `cargo nextest run` — tests must be green and not flaky before mutation testing
3. Verify the project builds on the host platform — cargo-mutants doesn't support cross-compilation
4. Check `cargo mutants --version` — if already present (idempotent check) → skip install

### 2. Install cargo-mutants

> Goal: install the cargo-mutants binary

1. Install with `cargo install --locked cargo-mutants`
2. Or faster with `cargo binstall cargo-mutants` (prebuilt binary)
3. Verify with `cargo mutants --version`

### 3. Create Config

> Goal: create a minimal `.cargo/mutants.toml`

1. Create `.cargo/mutants.toml` at the source tree root — check it into VCS
2. Set top-level keys (there is no `[mutants]` table): `timeout_multiplier`, `examine_globs`, `exclude_globs`, `test_package`
3. If using nextest → `test_tool = "nextest"` (faster due to fail-fast) — do `/follow-tool-nextest` if not set up yet
4. Set `exclude_globs` for generated/vendored/test-only code
5. See more config keys in `references/cli.md` or official docs

### 4. Baseline Run

> Goal: run mutation testing for the first time on a limited scope

1. Run `cargo mutants -f <file.rs>` on a small file first — confirm the pipeline works
2. Run a full `cargo mutants` if the scope is reasonable — or limit it with `examine_globs`
3. Check the output in `mutants.out/` — look at `missed`/`NOT CAUGHT`, `caught`, `unviable`, `timeout`
4. Record the baseline: mutant count, caught/missed ratio — to compare with later runs

### 5. Verify

> Goal: confirm the setup is reproducible

1. Re-run with the same args — results must be consistent (not flaky)
2. Verify fails → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Tests must be green and stable first — never run on a flaky suite
- No source code changes are needed to use cargo-mutants — by default
- Keep `.cargo/mutants.toml` in VCS — no secrets or absolute paths
- Set `timeout_multiplier`/`minimum_test_timeout` appropriately — prevents hanging tests
- Baseline on a small scope first — a full run can take a very long time

## Expected Outcome

- cargo-mutants installed and `.cargo/mutants.toml` committed
- Baseline run succeeds with `mutants.out/` results
- Initial caught/missed mutants known, for tracking onward
