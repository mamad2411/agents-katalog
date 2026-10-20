---
name: capacitor-migration-upgrades
description: Use when upgrading CapacitorJS major or minor versions and related plugins with deterministic compatibility checks, migration sequencing, rollback planning, and release-risk controls.
---

# Capacitor Migration Upgrades

## Specialization

Plan and execute CapacitorJS upgrade paths with controlled blast radius by validating compatibility, sequencing migrations, and enforcing rollback-ready release gates.

## Trigger Conditions

- Upgrading Capacitor major/minor versions.
- Upgrading official or community plugins with breaking changes.
- Resolving deprecated APIs or bridge behavior changes.
- Standardizing upgrade playbooks across multiple projects.

## Inputs

- Current and target Capacitor versions.
- Plugin inventory with current versions.
- Native runtime versions (Xcode, iOS SDK, Android Gradle, Kotlin).
- Release window, rollback tolerance, and risk level.

## Required Outputs

- Compatibility matrix: core, plugins, native toolchain.
- Sequenced migration plan with checkpoints.
- Breaking-change remediation ledger.
- Rollback procedure and fallback version targets.
- Upgrade gate verdict with residual risk summary.

## Deterministic Workflow

1. Build a current-state inventory of Capacitor core, plugins, and native toolchains.
2. Validate target-version compatibility using official release notes and plugin docs.
3. Sequence upgrade steps: core first, then official plugins, then community plugins.
4. Run build, sync, and test checkpoints after each sequence step.
5. Track breaking changes in a remediation ledger with owners.
6. Validate rollback path at each checkpoint.
7. Issue final go/no-go with unresolved risks.

## Upgrade Rules

- Avoid skipping major versions unless explicitly supported.
- Upgrade plugins in compatibility cohorts, not ad hoc.
- Treat deprecation warnings as migration work, not noise.
- Lock toolchain versions during migration to isolate variables.

## Quality Gates

- Compatibility matrix is complete and evidence-backed.
- Each migration checkpoint passes build and test gates.
- Rollback path is executable without undocumented context.
- Unresolved breaking changes are explicitly dispositioned.

## Done Criteria

- Target Capacitor version is reached with passing checkpoints.
- Breaking changes are resolved or explicitly accepted with owner sign-off.
- Rollback and release recommendation are documented.
