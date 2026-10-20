---
name: expo-react-native-debugging
description: "Debug Expo across Metro, dev/native builds, EAS, OTA runtime, APIs, and storage."
---

# Expo React Native Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Debug Expo / React Native by locating the failing boundary first: JavaScript, Metro, Expo Router, native Android/iOS, CNG/prebuild/config plugin, development build, EAS Build, OTA/runtime/channel, API/network, storage/migration, device lifecycle, or observability.

## Process

1. State expected behavior, actual behavior, impact, platform, OS, device/simulator, app variant, app version, build number/versionCode, runtime version, update ID/channel, Expo SDK, React Native, and whether the failure is dev, preview, production, EAS-only, or OTA-only.
2. Inspect repo-pinned Expo SDK, React Native, Expo Router, EAS CLI, Node, package manager, native dependencies, app config, EAS profiles, test tools, and CI before recommending version-specific fixes.
3. For new-project, upgrade, EAS, OTA, or native compatibility advice, check current official Expo, React Native, EAS, and package docs through `itsol-current-tech-context`.
4. Gather evidence before changing code: Metro output, React Native DevTools, Expo dev menu, `expo-doctor`, resolved app config, native logs, EAS build logs, OTA deployment data, crash report metadata, API request IDs, and storage migration state.
5. Reproduce in the mode that fails. If a release build, EAS build, or OTA update fails, do not rely only on Expo Go or the Metro development server.
6. Fix one boundary at a time. Add a regression test when the repo supports it; otherwise document the narrowest reliable manual verification on Android and iOS when platform behavior is relevant.
7. Use `itsol-bug-debugging` for user-facing defects and follow its Technical Fix Plan gate when required by the resolved workflow mode.

## Coordination

Use with `itsol-current-tech-context`, `itsol-bug-debugging`, `ui-performance-stability`, `ui-frontend-testing-qa`, `hey-api-openapi-contract-debugging`, `security-auth-session-review`, `infra-observability`, and release/security Expo skills when OTA, EAS, permissions, privacy, credentials, or store behavior are part of the failure. For TanStack Query in mobile apps, use `tanstack-query-react-nextjs-debugging` only for framework-agnostic query keys, cache, mutation, invalidation, and auth-cache behavior; ignore Next.js SSR/App Router guidance unless web/Next.js is also in scope.

## Reference Routing

- Evidence matrix, repro isolation, version detection, mode/platform classification, and cache-reset discipline: read [01-evidence-and-triage.md](./references/01-evidence-and-triage.md).
- Metro, JavaScript, Expo Router, development builds, Expo Go limits, CNG/prebuild, config plugins, native build logs, Android, iOS, and New Architecture failures: read [02-metro-dev-build-native-build.md](./references/02-metro-dev-build-native-build.md).
- EAS Build, EAS-only failures, EAS environments, EAS Update, OTA runtime/channel/branch, asset loading, rollback, and update metadata: read [03-eas-build-update-runtime.md](./references/03-eas-build-update-runtime.md).
- API/network/auth, TanStack Query, generated clients, offline sync, local storage, SecureStore, SQLite, filesystem, platform-specific behavior, lifecycle, permissions, deep links, and push: read [04-api-storage-platform.md](./references/04-api-storage-platform.md).
- Crash reporting, logs, release metadata, monitoring, source maps, maintenance signals, performance regressions, and final debugging reports: read [05-observability-maintenance.md](./references/05-observability-maintenance.md).

## Version Policy

- Existing repo: debug against pinned Expo SDK, React Native, React, Expo Router, EAS CLI, Node, package manager, native dependencies, app config, EAS profiles, and CI/release configuration.
- New-project or upgrade-sensitive advice: use latest stable choices only after checking official Expo, React Native, and EAS docs through `itsol-current-tech-context`.
- Symptoms involving SDK upgrades, development builds, CNG/prebuild, config plugins, New Architecture, Expo Router, EAS Build, EAS Update, or native module APIs require current official docs before recommending version-specific fixes.
