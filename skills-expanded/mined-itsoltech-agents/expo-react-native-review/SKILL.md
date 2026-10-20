---
name: expo-react-native-review
description: "Review Expo architecture, dependencies, APIs, storage, OTA releases, platform QA, and tests."
---

# Expo React Native Review

Review Expo and React Native as a mobile system with native binaries, JavaScript updates, platform-specific behavior, device permissions, local data, and EAS release paths.

## Process

1. Inspect changed files, package pins, lockfiles, app config, `eas.json`, Expo Router routes, generated native diffs, config plugins, native dependencies, storage, API/cache code, tests, CI, release notes, and QA evidence.
2. For an existing repo, detect repo-pinned Expo SDK, React Native, React, Expo Router, EAS CLI, Node, package manager, and native dependency versions before judging APIs or defaults. For a new app, use latest stable. For Expo/RN/EAS compatibility, New Architecture, permissions, OTA, or store-release decisions, check current official docs through `itsol-current-tech-context`.
3. Build a review coverage map: behavior, architecture, dependencies, API/cache/offline, storage, UI states, lifecycle, platform behavior, security, release/OTA impact, tests, and QA.
4. Lead with findings by severity, with concrete user, data-loss, security, store-release, OTA, or rollback impact and file references.
5. Treat missing device QA, unverified permissions, native changes without a new binary, runtime-incompatible OTA, untested storage migrations, and dependency compatibility gaps as explicit review risks.

## Evidence

Prefer code, tests, app config, lockfiles, native generated diffs, EAS/build logs, crash telemetry, release metadata, platform QA, and official Expo/RN/EAS docs over assumptions.

## Focused References

- [01-review-coverage-findings.md](./references/01-review-coverage-findings.md) - review workflow, coverage map, severity, findings format, and mobile Definition of Done.
- [02-architecture-dependencies.md](./references/02-architecture-dependencies.md) - app architecture, Expo Router, CNG/prebuild, app config, generated code, SDK/dependency compatibility, and New Architecture risk.
- [03-api-storage-ui-platform.md](./references/03-api-storage-ui-platform.md) - API/cache/offline behavior, storage, UI states, lifecycle, navigation, performance, accessibility, and platform matrix.
- [04-security-release-tests.md](./references/04-security-release-tests.md) - security, permissions, OTA/release safety, tests, QA scenarios, CI gates, and review risk flags.
