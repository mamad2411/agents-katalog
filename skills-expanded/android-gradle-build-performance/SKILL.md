---
name: "android-gradle-build-performance"
description: "Diagnose and improve Android and Gradle build performance with scans, cache checks, and bottleneck audits."
metadata:
  version: "0.1.0"
  category: "quality-release"
  tags: ["android", "gradle", "build-performance", "ci", "ksp"]
  triggers:
    include: ["android gradle build performance", "configuration cache android build", "ksp vs kapt android", "slow gradle build in android", "ci build cache diagnosis android"]
    exclude: ["deep link only", "compose semantics only", "room dao only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Gradle Build Performance

## When To Use
- Use this skill when the request is about: android gradle build performance, configuration cache android build, ksp vs kapt android.
- Primary outcome: Diagnose and improve Android and Gradle build performance with scans, cache checks, and bottleneck audits.
- Use this skill when the problem is build speed, task churn, cache misses, or CI wall time rather than build-logic structure.
- Read `references/patterns.md` when you need the measurement ladder or the most common Gradle performance smells.
- Read `references/scenarios.md` for audit-first entry points on the example projects.
- Handoff skills when the scope expands:
- `android-gradle-build-logic`
- `android-ci-cd-release-playstore`

## Workflow
1. Identify whether the problem is local developer feedback time, CI build duration, or both.
2. Measure one build path at a time with `--profile`, `--scan`, configuration-cache diagnostics, or the bundled audit script before proposing a fix.
3. Check `gradle.properties`, plugin wiring, dependency declarations, task registration style, and module conventions for common performance smells.
4. Apply one high-confidence optimization at a time, then compare before and after behavior instead of stacking changes.
5. Hand off structural Gradle refactors or release-pipeline changes once the performance bottleneck is isolated.

## Guardrails
- Do not recommend broad rewrites when a single cache, plugin, or dependency pattern is the real bottleneck.
- Separate measurement from speculation; call out what was observed vs inferred.
- Prefer KSP, configuration cache, and lazy task configuration when the toolchain supports them.
- Treat dynamic dependency versions, changing modules, and eager task creation as performance regressions unless there is a deliberate reason.
- Keep CI guidance reproducible on the example projects before suggesting org-wide rollout.

## Anti-Patterns
- Turning on every Gradle flag without checking compatibility or failures.
- Blaming AGP upgrades for slow builds without measuring task hot spots.
- Mixing build-logic architecture advice with build-time diagnosis in one pass.
- Using dynamic dependency versions that force repeated resolution work.

## Review Focus
- Configuration time vs execution time vs dependency resolution vs test wall time.
- Configuration cache compatibility and lazy task registration.
- KSP vs kapt and annotation-processor hotspots.
- Remote/local cache value, dynamic dependencies, and CI-specific bottlenecks.

## Examples
### Happy path
- Scenario: Audit the Compose fixture for build cache, configuration cache, KSP, and eager task creation smells.
- Command: `python3 skills/android-gradle-build-performance/scripts/audit_build_performance.py examples/orbittasks-compose --json`

### Edge case
- Scenario: Compare XML and Compose fixture build settings before choosing a CI build optimization.
- Command: `bash skills/android-gradle-build-performance/scripts/run_examples.sh`

### Failure recovery
- Scenario: Re-check a project after enabling performance flags so regressions are caught before rollout.
- Command: `python3 skills/android-gradle-build-performance/scripts/audit_build_performance.py examples/orbittasks-xml`

## Done Checklist
- The bottleneck is tied to a specific phase, flag, plugin, or dependency pattern.
- Proposed optimizations are measurable and reversible.
- The recommended fix is compatible with the current Android and Gradle toolchain.
- Structural Gradle work is handed off separately from performance tuning.

## Official References
- [https://docs.gradle.org/current/userguide/performance.html](https://docs.gradle.org/current/userguide/performance.html)
- [https://docs.gradle.org/current/userguide/configuration_cache.html](https://docs.gradle.org/current/userguide/configuration_cache.html)
- [https://docs.gradle.org/current/userguide/task_configuration_avoidance.html](https://docs.gradle.org/current/userguide/task_configuration_avoidance.html)
- [https://developer.android.com/build/optimize-your-build](https://developer.android.com/build/optimize-your-build)
- [https://developer.android.com/build/ksp](https://developer.android.com/build/ksp)
