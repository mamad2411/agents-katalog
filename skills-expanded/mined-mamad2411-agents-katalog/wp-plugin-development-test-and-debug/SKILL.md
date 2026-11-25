---
name: wp-plugin-development-test-and-debug
description: Designs a WordPress and PHP compatibility matrix, runs maintained quality tools, reproduces plugin failures, and verifies positive, negative, lifecycle, upgrade, and uninstall behavior. Use for testing or debugging.
---

# WordPress Plugin Testing and Debugging

Use this skill to turn compatibility claims and bug reports into repeatable evidence.

## Inputs to collect

- Supported WordPress, PHP, database, browser, and dependency ranges.
- Multisite, object cache, cron, REST, Ajax, filesystem, external-service, and localization requirements.
- Existing Composer, Node, test, lint, static-analysis, container, and CI configuration.
- Exact reproduction steps, environment, logs, expected behavior, and last known good version.
- Install, activation, upgrade, deactivation, uninstall, and rollback expectations.

## Method

1. Build the smallest risk-based matrix with [test matrix](resources/test-matrix.md).
2. Use project-native commands first, then apply the maintained tools in [tooling baseline](resources/tooling-baseline.md).
3. Reproduce a reported failure before editing. Record the exact environment and minimal failing case.
4. Classify the failure as bootstrap, dependency, permission, input, storage, migration, cache, cron, HTTP, rendering, compatibility, packaging, or environment behavior.
5. Add a focused regression test that fails for the observed reason.
6. Implement the smallest correction without widening compatibility claims.
7. Run focused tests, then the relevant matrix and static/runtime checks.
8. Verify negative authorization/input cases and lifecycle paths affected by the change.
9. Run the [test and debug workflow](workflows/test-and-debug-workflow.md).

## Test principles

- Test the lowest supported WordPress/PHP combination and the current stable combination.
- Add intermediate versions when APIs, dependencies, or prior regressions justify them.
- Separate unit tests from WordPress integration/runtime tests.
- Test public contracts and failure behavior, not private implementation details alone.
- Make remote-service tests deterministic with fakes or controlled test servers.
- Treat object cache, cron, time zones, locales, Multisite, and clean installs as explicit environments when relevant.
- Test upgrades from every supported schema/data version that users can realistically have.
- Test uninstall in preserve-data and delete-owned-data modes where the plugin supports both.
- Do not mark a flaky test as solved by retrying it without identifying nondeterminism.

## Required output

Report:

- reproduction and root cause
- test added or existing test evidence
- exact environments and commands used
- focused and matrix results
- lifecycle, authorization, compatibility, and packaging impact
- untested combinations and residual risk
