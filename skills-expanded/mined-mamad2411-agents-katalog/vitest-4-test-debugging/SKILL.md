---
name: vitest-4-test-debugging
description: Debugs failing and flaky Vitest 4 tests, focused tests, network leakage, timer issues, mock isolation, environment mismatches, snapshots, browser-mode failures, and CI-only failures. Use when tests fail, flake, hang, or behave differently locally and in CI.
license: MIT
compatibility: Vitest 4.x, Node.js 20+, and Vite 6+ when Vite integration is used.
---

# Vitest 4 Test Debugging

Use this skill when Vitest 4 tests fail, hang, flake, rely on `.only`, leak network calls, or differ between local and CI runs.

## Workflow

- `workflows/flaky-failing-test-debugging-workflow.md`: Use when triaging failing or flaky Vitest 4 tests.

## Resource

- `resources/flaky-test-patterns.md`: Use to identify common sources of nondeterministic tests.

## Example

- `examples/failing-test-triage-example.md`: Reference example for safe triage and verification.

## Scripts

Run scripts with `--help` before using:

- `scripts/vitest-4-no-focused-tests.mjs`: Hook script that prevents stopping with `.only` in test files.
- `scripts/vitest-4-flaky-test-detection.mjs`: Optional hook script that flags common flaky patterns.
- `scripts/vitest-4-related-tests-on-change.mjs`: Optional hook script that suggests related test commands from changed files.

## Debugging Standards

- Reproduce with the smallest command first.
- Do not update snapshots as the first response to a failure.
- Do not convert failures to skipped tests without approval.
- Classify the failure before changing code.
- Preserve or strengthen the behavior being tested.
- Report commands actually run and their results.
