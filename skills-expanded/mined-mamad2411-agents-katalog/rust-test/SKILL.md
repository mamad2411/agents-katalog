---
name: rust-test
description: Design, patch, audit, or align Rust tests with evidence-based guidance for unit tests, integration/e2e tests, doctests, insta snapshots, compile-fail/UI tests, golden files, fixtures, property tests, fuzz tests, async/concurrency tests, unsafe-code validation, Criterion benchmarks, Cargo test semantics, Rust 1.97 test idioms, feature/target/MSRV matrices, flaky-test triage, coverage/mutation evidence, and focused validation.
---

# rust-test

Use this skill when the user asks to add, fix, refactor, audit, or explain Rust tests or Rust test strategy. It is especially relevant for generated output, diagnostics, CLI output, serialization, parsers, proc macros, fixture-heavy tests, public documentation examples, fuzz/property validation, async or concurrent behavior, unsafe or FFI-heavy code, feature-flag, target-specific, or MSRV-sensitive behavior, flaky tests, performance-sensitive code, Cargo test command selection, coverage/mutation evidence, and snapshot review workflows.

## Operating principle

Tests should express the contract clearly and fail with useful diffs. Match the test type to the contract being protected: unit tests for narrow logic, integration/e2e tests for public workflows and real boundaries, doctests for public examples, compile-fail/UI tests for compiler-facing contracts, snapshots/goldens for reviewable deterministic output, property/fuzz tests for broad input spaces, async/concurrency tests for task lifecycle and synchronization behavior, unsafe-code validation for invariants the type system cannot prove, and benchmarks for performance behavior. Prefer the repository's existing test conventions. Do not silently introduce new dev-dependencies, test runners, fuzzers, benchmark harnesses, async runtimes, Miri/sanitizer/loom gates, or snapshot tools unless the repository already uses them or the user explicitly asks to standardize on them.

Do not add mock-centric test strategies as a default. When behavior depends on collaboration across modules, processes, services, filesystems, CLIs, async tasks, protocols, or target-specific behavior, prefer the smallest real integration/e2e seam that proves the public behavior. Use fakes, stubs, or test doubles only when the repository already uses that approach, the real boundary is impractical, and the test still asserts observable behavior rather than implementation call choreography.

## Boundary with rust-best-practices

Keep this skill test-scoped. Use it for assertion choice, test harness shape, doctest behavior, UI/diagnostic expectations, snapshot/golden review, fuzz/property/benchmark harnesses, async/concurrency validation, unsafe-code evidence, and Cargo validation semantics. Do not use it to give broad implementation style guidance such as API ownership, generic dispatch, error type design, builder/type-state selection, comment policy, lint policy, or production performance refactors unless those choices are the explicit test contract. When the user asks for overall Rust code patterns, route that work to `rust-best-practices`; when the user asks whether tests prove the behavior, stay here.

## Rust 1.97 test-specific baseline

Assume Rust 1.97 stable only when the repository does not declare a stricter MSRV. The Rust 1.97 guidance in this skill is limited to testing surfaces:

- prefer stable `assert_matches!` for enum variants, typed errors, state transitions, parse outcomes, and other structured pattern assertions when the repository MSRV is Rust 1.96 or newer;
- import `std::assert_matches` in ordinary tests and doctests, or `core::assert_matches` for `no_std` contexts;
- do not replace clear `assert_eq!`, boolean `assert!` checks with useful messages, structural assertions, or snapshots/goldens just to use a macro;
- do not use `debug_assert_matches!` as the normal test assertion; reserve it for debug-only internal invariants or existing repository style;
- inspect Cargo 1.97 configuration such as `build.warnings` and `resolver.lockfile-path` before interpreting command failures or claiming which lockfile a test used;
- treat Rust 1.97 Cargo, rustdoc, compiler, target, symbol-mangling, linker-warning, `pin!`, and deprecation changes as test-selection or expectation-file evidence, not as permission to refactor production code under this skill.

## When to use this skill

Use it for:

- Rust unit, integration, end-to-end, doc, fixture, regression, and example tests;
- deciding whether `insta` snapshot tests fit a Rust change;
- updating and reviewing `.snap`, `.snap.new`, `.pending-snap`, `.stderr`, golden, fixture, generated-output, corpus, or benchmark expectation files;
- proc-macro, compiler diagnostic, doctest `compile_fail`, or UI tests;
- property-based tests for invariants, round trips, parser/formatter behavior, generated inputs, and stateful contracts;
- fuzz targets, minimized crash regressions, corpus updates, and input-hardening strategy;
- async runtime behavior, task cancellation, channels, streams, timeouts, fake time, shutdown, and concurrency regressions;
- unsafe code, FFI boundaries, pointer manipulation, custom allocators, atomics, panic/drop safety, Miri, sanitizer, or loom validation strategy;
- feature-flag combinations, `cfg` gates, target triples, `no_std`, WASM, embedded, platform-specific behavior, and MSRV-sensitive test selection;
- Criterion or other existing Rust benchmark harnesses for performance-sensitive code;
- replacing brittle text assertions or mock-only assertions with clearer structural, snapshot, integration, or e2e assertions;
- choosing focused validation commands for Rust test, benchmark, doctest, fuzz, feature/target/MSRV, unsafe-code, nextest, coverage/mutation, or expectation-file changes.

Do not use it for non-Rust testing unless the repository explicitly routes that work here.

## Decision kernel

1. Inspect current Rust test evidence before changing strategy.
2. Identify the contract: pure logic, public API, public workflow, documentation example, compiler diagnostic, generated output, robustness across inputs, async/concurrency behavior, unsafe-code invariant, target/feature support, or performance.
3. Preserve existing harnesses, fixture layout, naming, runners, benchmark/fuzz layout, and snapshot workflow.
4. Use unit tests for small deterministic logic and integration/e2e tests for public seams or cross-component behavior.
5. Use doctests for public documentation examples and README/API samples that should compile or run.
6. Use `insta` for reviewable large or structured outputs when it is already used, requested, or explicitly proposed.
7. Use compile-fail/UI tests for compiler diagnostics, proc macros, trait-bound failures, and type-level contracts when configured or requested.
8. Use property tests when invariants should hold across many generated inputs and the repository already uses or requests that style.
9. Use fuzz tests for parser, deserializer, protocol, unsafe, or untrusted-input surfaces when fuzzing is configured or explicitly requested.
10. Use Criterion or the repository's benchmark harness when performance is part of the contract or regression risk.
11. Avoid mock-only verification for public behavior; prefer the smallest real integration/e2e seam, fixture, or local fake that preserves the observable contract.
12. Normalize nondeterministic output before asserting, snapshotting, goldening, fuzzing, or benchmarking it.
13. Validate with focused commands and review expectation-file diffs intentionally.
14. Treat feature flags, mutually exclusive features, `cfg` gates, target triples, MSRV, and `no_std`/WASM/embedded constraints as part of the tested contract when they affect behavior or compilation.
15. For async, concurrent, time-sensitive, or background-task behavior, prefer deterministic synchronization, fake or paused time, joined tasks, and repository-standard runtime patterns over sleeps and timing assumptions.
16. For unsafe, FFI, atomics, custom allocators, or memory-invariant changes, pair public functional tests with invariant-focused regressions and use Miri, sanitizers, loom, or fuzzing only when configured, requested, or clearly labeled as recommended.
17. Prefer structural assertions for typed errors, variants, spans, exit codes, and machine-readable fields. On the Rust 1.97 baseline, use `assert_matches!` for single-pattern variant assertions when the repository MSRV is Rust 1.96 or newer and the mismatched value should be printed. Assert exact text only when wording is part of the public contract.
18. Keep Rust 1.97 guidance test-specific. Do not drift into broad implementation style choices covered by `rust-best-practices` unless the code pattern itself is being tested.
19. In workspaces, identify the affected package graph before selecting validation. Prefer package-scoped commands first, then dependent package tests when public APIs or shared fixtures changed.
20. Account for Cargo test semantics before claiming what a command proves: package selection, target selection, doctests, examples, feature flags, test filters, and libtest arguments all matter.
21. Treat retries and serial execution as flake triage tools, not correctness fixes. Prefer root-cause repairs such as deterministic synchronization, isolated temp resources, explicit task joins, and stable ordering.

## Required evidence

Before patching or recommending test changes, inspect the relevant subset of:

- `Cargo.toml`, workspace manifests, dev-dependencies, feature flags, feature matrices, bench targets, fuzz manifests, and workspace dependency policy;
- `rust-toolchain.toml`, package `rust-version`, `.cargo/config.toml`, Cargo 1.97 `build.warnings` or `resolver.lockfile-path`, MSRV policy, target matrix, `no_std`/WASM/embedded support, platform-specific `cfg`s, Rust 1.97-sensitive doctest or target configuration, and feature-combination expectations affected by the change;
- existing `tests/`, `src/**/tests`, `benches/`, `examples/`, `fixtures/`, `snapshots/`, `fuzz/`, corpus directories, UI-test directories, generated outputs, and e2e harnesses;
- CI workflows, `justfile`, `Makefile`, `cargo-nextest` config, `cargo-insta` config, benchmark scripts, fuzz scripts, target-specific jobs, feature-matrix jobs, MSRV jobs, coverage/mutation jobs, or other runner files;
- existing `insta`, `trybuild`, UI-test, golden-file, fixture, property-test, fuzz, doctest, Criterion, `cargo bench`, `cargo-fuzz`, `nextest`, `cargo hack`, async-runtime, fake-time, concurrency, Miri, sanitizer, loom, coverage, mutation-testing, or e2e usage;
- existing coverage, mutation-testing, or quality-gate tooling only when the repository already uses it or the user asks about coverage strength;
- public docs, README examples, CLI help, schemas, generated outputs, diagnostics, protocols, compatibility files, target/platform guarantees, or performance claims affected by the change.

If evidence is incomplete, produce an evidence-limited patch, audit, or strategy note instead of guessing.

## Evidence tiers

Use the narrowest evidence tier that can answer the request.

- **Tier 0 — Brief explanation or command recommendation:** inspect only directly relevant manifest, runner, or command-semantics facts when available. Do not perform full repository reconnaissance.
- **Tier 1 — Focused test patch:** inspect the affected crate manifest, nearby tests, relevant fixtures/snapshots/expectations, and the narrowest validation command.
- **Tier 2 — Cross-surface patch or audit:** inspect workspace manifests, CI/runner files, feature flags, affected packages, target/MSRV policy, expectation-file workflows, and dependent crates when public APIs or shared fixtures changed.
- **Tier 3 — Tool adoption or strategy:** inspect current tool usage, CI policy, MSRV, feature/target matrix, dev-dependency policy, maintenance burden, and whether the tool should be current policy or only **Recommended**.

If required evidence is missing, state the evidence limit and proceed with a conservative recommendation rather than inventing repository policy.

## Output modes

For substantive work, declare the mode before the main response:

- **Patch:** edit tests, fixtures, snapshots, benchmarks, fuzz targets, expectations, or validation guidance with minimal changes.
- **Audit:** review an existing Rust test suite or proposed test plan and return findings by severity.
- **Strategy:** propose a focused test approach for a specific Rust change.
- **Checklist:** apply `checklists/rust-test-checklist.md`.

For brief explanations or command recommendations that do not patch or audit files, keep the response concise while preserving evidence and validation boundaries.

When ambiguous, choose Audit for existing tests and Strategy for a planned change. Choose Patch only when the user asked for edits or the required change is obvious.

### Audit severities

- **Critical:** likely to hide regressions, accept wrong public behavior, make tests non-deterministic, update expectations without review, or measure performance in a misleading way.
- **Important:** likely to make tests brittle, mock implementation details, miss public seams, run too broadly or slowly, add noisy benchmark/fuzz gates, or poorly align with public contracts.
- **Nice to have:** improves naming, fixture organization, diagnostics, benchmark grouping, fuzz corpus hygiene, review ergonomics, or validation targeting.

## Pattern map

Use these support files as source material, not default output. Summarize only the relevant pattern unless the user asks for a full checklist or patch:

- `patterns/automated-testing.md`: core unit, integration, doctest, assertion, parameterized, and snapshot test shape.
- `patterns/rust-1-97-testing-baseline.md`: Rust 1.97 test-specific assertion, doctest, Cargo/rustdoc, target, and compatibility guidance without broad code-style overlap.
- `patterns/cargo-test-semantics.md`: Cargo package/target/feature/doctest/libtest command semantics and what a validation command proves.
- `patterns/boundary-and-e2e.md`: public seams, integration/e2e tests, CLI binary integration, and avoiding mock-centric verification.
- `patterns/doctests-and-examples.md`: doctests, README examples, rustdoc mechanics, `no_run`, `compile_fail`, and public API samples.
- `patterns/insta-snapshots.md`: when and how to use `insta` snapshots.
- `patterns/compile-fail-and-diagnostics.md`: proc-macro, compiler diagnostic, doctest compile-fail, `trybuild` expectation workflows, and UI-test patterns.
- `patterns/fixtures-and-golden.md`: fixtures, golden files, generated output, structural assertions, and deterministic comparisons.
- `patterns/property-and-fuzz.md`: property tests, fuzz targets, corpus handling, and minimized regressions.
- `patterns/async-concurrency-and-time.md`: async runtimes, cancellation, channels, fake time, concurrency, and flake-resistant scheduling tests.
- `patterns/flaky-tests.md`: nondeterministic failure triage, retry policy, serial execution limits, and root-cause stabilization.
- `patterns/unsafe-and-memory.md`: unsafe code, FFI, atomics, custom allocators, Miri, sanitizer, loom, and memory-invariant validation.
- `patterns/benchmarks-and-performance.md`: Criterion, `cargo bench`, benchmark layout, and performance validation.
- `patterns/feature-msrv-matrix.md`: feature combinations, target triples, `no_std`/WASM/embedded support, MSRV, and `cargo hack` guidance.
- `patterns/coverage-and-mutation.md`: coverage and mutation-testing as supporting evidence for test strength.
- `patterns/validation.md`: focused Rust validation wording and command selection.
- `checklists/rust-test-checklist.md`: final review checklist.

## Dependency boundary

A new testing, fuzzing, benchmarking, snapshot, async-runtime, fake-time, sanitizer, Miri, loom, coverage, mutation-testing, feature-matrix, or command-runner dependency is a code change, not a default recommendation. Add or require a new Rust test dependency only when:

1. the repository already uses it in the relevant workspace or has standardized on it;
2. the user explicitly asked to introduce or standardize the tool; or
3. the response is an audit/strategy proposal that clearly labels the dependency as **Recommended**, not current repository policy.

When adding a dev-dependency or tool-specific dependency, follow the repository's existing dependency placement, feature, workspace-version, MSRV, CI, and target-platform conventions.

## Final response format

Include applicable items:

- selected mode;
- tests, fixtures, snapshots, benchmarks, fuzz targets, expectations, or files changed/audited;
- evidence used for the test strategy;
- validation performed with exact commands;
- snapshot/golden/diagnostic/corpus/benchmark expectations reviewed or not reviewed;
- validation not performed and why;
- attempted validation failures and whether they appear related to the change;
- remaining risks or missing evidence.

Use exact validation wording:

- `Validated with: <command>` only when the command ran successfully.
- `Attempted validation with: <command>` when the command ran but failed; include the relevant failure summary and whether the failure appears related to the change.
- `Reviewed only; not executed because: <reason>` for static review without execution.
- `Not validated; missing repo access / command unavailable / outside requested scope: <reason>` when validation was not possible or not attempted.
