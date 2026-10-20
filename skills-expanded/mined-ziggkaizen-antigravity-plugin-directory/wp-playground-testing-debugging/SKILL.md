---
name: wp-playground-testing-debugging
description: Plans and runs WordPress Playground PHPUnit, Playwright, compatibility, snapshot, Xdebug, and failure-triage workflows with isolated state and reproducible evidence.
---

# WordPress Playground testing and debugging

Use this skill for PHPUnit, Playwright, compatibility matrices, bug reproduction, Xdebug setup, or Playground failure triage.

## Required inputs

- Component and test entry points.
- Supported WordPress/PHP matrix.
- CLI/Node versions.
- Build/dependency requirements.
- Shared or per-test state requirements.
- Browser and CI constraints.
- Expected diagnostics and artifacts.

## Procedure

1. Define the minimum supported, primary, and forward-looking matrix.
2. Pin the Playground CLI in committed automation.
3. Use a clean Blueprint fixture.
4. Choose shared server only for read-only tests; prefer per-test/reset state for mutating tests.
5. Ensure server processes close even on failure.
6. Run PHPUnit with the component mounted at its real WordPress path.
7. Run Playwright with conservative startup/assertion timeouts, one worker unless ports are isolated, web-first assertions, traces, and screenshots.
8. Capture exact versions, commands, Blueprint, logs, trace, screenshot, and snapshot.
9. Reproduce from clean state.
10. Read `resources/troubleshooting.md` and escalate when the environment lacks required fidelity.

## Workflow

Use `workflows/test-and-debug-workflow.md`.

## Resources and examples

- `resources/test-matrix.md`
- `resources/troubleshooting.md`
- `examples/phpunit-playwright-examples.md`
