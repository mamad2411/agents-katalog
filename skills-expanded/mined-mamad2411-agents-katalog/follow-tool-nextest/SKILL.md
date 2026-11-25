---
name: follow-tool-nextest
description: Set up and use cargo-nextest as a fast test runner in Rust projects
argument-hint: "[scope]"
related:
  - follow-lang-rust
  - follow-tool-cargo
  - follow-test
  - update-tests
  - follow-tool-mutants-rs
  - run-test
---

## Goal

Set up and use cargo-nextest as a fast, efficient test runner in Rust projects

## Scope

For Rust projects using the Cargo build system

- Use this skill instead of `cargo test` for unit/integration tests — doctests still need `cargo test --doc`
- If the goal is mutation testing (test quality) rather than a test runner → use `/follow-tool-mutants-rs`

- Latest: `cargo-nextest@0.9.146` (crates.io) (verified 2026-09-24)

## Execute

### 1. Installation

> Goal: install cargo-nextest on the environment

1. Install with `cargo binstall cargo-nextest --secure`
2. Or install from pre-built binaries via `https://get.nexte.st/latest/{linux,mac,windows}`
3. On Windows `winget install nextest.cargo-nextest` also works
4. Install from source with `cargo install cargo-nextest --locked`
5. Update with `cargo nextest self-update`
6. See details in 

### 2. Run Tests

> Goal: run tests with cargo-nextest instead of `cargo test`

1. Run all tests with `cargo nextest run`
2. Run a single package with `cargo nextest run -p my-package`
3. Run doctests separately (nextest doesn't support doctests) with `cargo test --doc`
4. See details in 

### 3. Configuration

> Goal: create `.config/nextest.toml` for repository-specific configuration

1. Create `.config/nextest.toml` at the Cargo workspace root
2. Define profiles for local and CI runs
3. Use a profile when running: `cargo nextest run --profile ci`
4. See details in 

### 4. List Tests

> Goal: show all tests before running

1. Run `cargo nextest list` to list all tests
2. Run `cargo nextest list --verbose` for verbose output (binary paths, skipped tests)
3. See details in 

### 5. Profiles

> Goal: use profiles for local and CI runs

1. `default`: for local development
2. `ci`: for CI (`fail-fast = false`)
3. Create custom profiles in `.config/nextest.toml` with the `inherits` keyword
4. Avoid naming profiles with a `default-` prefix
5. See details in 

### 6. CI Integration

> Goal: add cargo-nextest to the CI pipeline

1. Install cargo-nextest in CI with `cargo binstall cargo-nextest --secure`
2. Run tests with `cargo nextest run --profile ci`
3. Use JUnit output for test reporting
4. See details in 

## Rules

### 1. Test Execution

- Use `cargo nextest run` instead of `cargo test` for better performance
- Run doctests separately from cargo-nextest with `cargo test --doc`
- Use `cargo nextest run -p <package>` to run a single package

### 2. Profiles

- Use `--profile ci` in CI to run every test even when some fail
- Use the `default` profile for local development
- Set `fail-fast = false` in the CI profile
- Avoid naming profiles with a `default-` prefix
- Use the `inherits` keyword for profile inheritance

### 3. Configuration

- Review the configuration in `.config/nextest.toml`
- Repository config at `.config/nextest.toml` is checked into VCS
- Personal config at `~/.config/nextest/config.toml`
- Use `--config-file` to override the config location

- Use /follow-lang-rust if needed
- Use /follow-tool-cargo if needed
- Use /follow-test if needed
- Use /update-tests if needed
- Use /follow-tool-mutants-rs if needed
- Use /run-test if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A fast and efficient test runner
- Tests run in parallel automatically
- Proper CI integration
- Reduced test execution time

