---
name: follow-tool-mutants-rs
description: Set up and use cargo-mutants for mutation testing in Rust projects
argument-hint: "[scope]"
related:
  - follow-lang-rust
  - follow-tool-nextest
  - follow-tool-cargo
  - update-tests
  - follow-test
  - run-test

---

## Goal

Set up and use cargo-mutants for mutation testing to improve the quality of Rust tests

## Scope

For Rust projects using the Cargo build system that want to verify test quality with mutation testing

- For JS/TS mutation testing → use `/follow-tool-stryker-mutator` instead
- Needs a stable test suite first — if tests are still flaky, do `/follow-test` or `/update-tests` first

- Latest: `cargo-mutants@27.1.0` / `mutants@0.0.4` (crates.io) (verified 2026-09-13)

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

| Topic | Workflow |-------|----------| setup | `workflows/setup-mutants/SKILL.md` — cargo-mutants install, `.cargo/mutants.toml`, baseline run | optimize | `workflows/optimize-mutation/SKILL.md` — skip lists, shard/parallel jobs, CI integration 
1. If the argument matches a topic → read and follow `workflows/<name>/SKILL.md` instead of the steps below
2. If not → follow the steps below as usual

### 1. Installation

> Goal: install cargo-mutants on the environment

1. Install with `cargo install --locked cargo-mutants`
2. Or install with `cargo binstall cargo-mutants`
3. Check the version with `cargo mutants --version`
4. See details in 

### 2. Prerequisites

> Goal: verify the project is ready for mutation testing

1. Run `cargo test` or `cargo nextest run` to verify the tests are not flaky
2. Verify the project builds on the host platform
3. Avoid running mutation testing while the tests aren't stable
4. See details in 

### 3. Run Mutation Testing

> Goal: run mutation testing with cargo-mutants

1. Run `cargo mutants` at the root of the Rust project
2. Run a single file with `cargo mutants -f src/file.rs`
3. Run with a specific toolchain with `cargo +1.48 mutants`
4. Show caught/unviable mutants with `cargo mutants --caught` or `cargo mutants --unviable`
5. See details in 

### 4. Understand Results

> Goal: interpret the results and identify mutants to fix

1. `NOT CAUGHT` / `missed`: the tests didn't catch this mutant → add tests
2. `CAUGHT`: the tests caught this mutant → good test coverage
3. `UNVIABLE`: this mutant doesn't build → nothing to do
4. `timeout`: the mutant hangs the tests → investigate or skip
5. See details in 

### 5. Configuration

> Goal: configure cargo-mutants for the project

1. Create `.cargo/mutants.toml` at the source tree root when advanced config is needed (check it into VCS)
2. Set top-level keys such as `timeout_multiplier`, `exclude_globs`, `examine_globs`, `test_package`, `copy_target` (there is no `[mutants]` table)
3. Use `test_tool = "nextest"` or `--test-tool=nextest` to run tests through nextest (faster due to fail-fast)
4. Use `#[mutants::skip]` for functions or impls that shouldn't be mutated (requires the `mutants` crate as a regular dependency)
5. Use `--exclude-re "pattern"` or `exclude_re` in config to filter specific mutations (the `#[mutants::exclude_re]` attribute is still unreleased — needs the `mutants` crate ≥ 0.0.5)
6. See details in 

### 6. CI Integration

> Goal: add cargo-mutants to the CI pipeline

1. Add a `cargo mutants` step in GitHub Actions or whichever CI is used
2. Use `cargo mutants --file` for incremental testing in PRs
3. Use a full `cargo mutants` run on the main branch
4. See details in 

## Rules

### 1. Test Quality

- Trustworthy tests are required before running `cargo mutants`
- Cross-compilation is not supported
- Must build on the host platform
- No source code changes are needed to use cargo-mutants by default

### 2. Mutant Handling

- Use `#[mutants::skip]` for mutants that aren't interesting
- Use `--exclude-re "..."` or `exclude_re` in config to filter specific mutations
- Add tests for `NOT CAUGHT` mutants
- Run `cargo mutants` periodically to track test quality

### 3. Configuration

- Keep `.cargo/mutants.toml` at the source tree root when present
- Use appropriate `timeout_multiplier` / `minimum_test_timeout` to prevent hanging tests
- Don't hard-code paths or secrets in `.cargo/mutants.toml`

- Use /follow-lang-rust if needed
- Use /follow-tool-nextest if needed
- Use /follow-tool-cargo if needed
- Use /update-tests if needed
- Use /follow-test if needed
- Use /deep-test mutation if needed

## References

- [CLI reference](references/cli.md)
- Use /run-test if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Mutation testing runs automatically
- Test coverage and quality improve
- Missed mutants are identified and fixed
- The test suite becomes more reliable

