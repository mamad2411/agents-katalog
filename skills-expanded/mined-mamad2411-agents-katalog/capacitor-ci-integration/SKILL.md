---
name: capacitor-ci-integration
description: Use when CapacitorJS build, test, signing, and artifact workflows must be automated in CI/CD with deterministic toolchains, reproducible outputs, and promotion-grade evidence.
---

# Capacitor CI Integration

## Specialization

Define and enforce a deterministic CI/CD contract for CapacitorJS projects across web build, cap sync, native compilation, testing, signing, and evidence packaging.

## Trigger Conditions

- A Capacitor project needs first-time CI automation.
- CI builds are flaky due to toolchain drift or non-deterministic native setup.
- Signed iOS or Android artifacts must be produced safely in automation.
- Release evidence must be durable and traceable for promotion decisions.

## Inputs

- Repository build commands and package manager.
- Target platforms: iOS, Android, or both.
- Signing strategy and secret management approach.
- Required test suites and quality gates.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- CI workflow blueprint for build, test, sync, native compile, and artifact publish.
- Toolchain pinning matrix (Node, Java, Xcode, Android SDK, CocoaPods).
- Secret and signing handling policy.
- Release evidence bundle checklist.
- Failure triage map with owner routing.

## Deterministic Workflow

1. Pin toolchain versions and cache keys.
2. Run dependency restore in clean mode (`npm ci` or equivalent).
3. Build web assets and run unit/integration tests.
4. Run `npx cap sync` after the web build only.
5. Compile native projects with release flags.
6. Apply signing from secrets only; never from repository files.
7. Publish artifacts and gate logs as durable CI outputs.
8. Fail fast on gate breaches and emit actionable diagnostics.

## Quality Gates

- Toolchain versions are explicit and immutable per workflow run.
- CI never depends on local machine state.
- Signing credentials are injected at runtime and redacted from logs.
- Artifacts include build metadata, commit SHA, and timestamp.

## Done Criteria

- CI produces reproducible native artifacts from a clean checkout.
- Required tests and quality gates are enforced before publish.
- Evidence artifacts support go/no-go and rollback decisions.
