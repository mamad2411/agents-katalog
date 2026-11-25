---
name: expo-react-native-implementation
description: "Implement Expo apps with Router, dev builds, CNG, native modules, state, storage, and tests."
---

# Expo React Native Implementation

Implement Expo / React Native mobile apps as production mobile software, not generic React screens. Treat the Expo SDK, native runtime, app config, development builds, OTA compatibility, and platform behavior as part of the feature contract.

## Process

1. Inspect repo-pinned Expo SDK, React Native, React, Expo Router, EAS CLI, Node, package manager, lockfile, app config, EAS profiles, test tools, and CI before choosing commands or versions.
2. For new projects or version-sensitive decisions, check current official Expo, React Native, EAS, and package docs through `itsol-current-tech-context`; do not assume npm latest React Native is compatible with the pinned Expo SDK.
3. Define the native contract early: app variant, bundle ID/package name, scheme, permissions, config plugins, development build needs, runtime version impact, and whether the change can ship by OTA or needs a new binary.
4. Keep screen components thin. Route API, server state, durable storage, permissions, navigation orchestration, native module calls, analytics, and offline sync through feature or shared adapters.
5. Use development builds for production-grade work. Expo Go is only enough for prototypes or features with no app-specific native runtime needs.
6. Add focused verification: lint, typecheck, tests, `expo-doctor`, dependency checks, prebuild/config checks when native config changes, and Android/iOS smoke tests for platform-sensitive behavior.

## Coordination

Use with `itsol-current-tech-context`, `ui-ux-workflow`, `ui-accessibility-motion`, `ui-performance-stability`, `hey-api-openapi-codegen`, `security-auth-session-review`, `security-files-integrations-review`, and release/security Expo skills when OTA, EAS, permissions, privacy, credentials, or store behavior are in scope. For TanStack Query in mobile apps, use `tanstack-query-react-nextjs-implementation` only for framework-agnostic query keys, cache, mutation, invalidation, and auth-cache patterns; ignore Next.js SSR/App Router guidance unless web/Next.js is also in scope.

## Reference Routing

- Version detection, project sizing, Expo fit, folder boundaries, Expo Router, TypeScript, linting, and dependency policy: read [01-project-architecture.md](./references/01-project-architecture.md).
- Development builds, Expo Go limits, Continuous Native Generation, prebuild, app config, config plugins, variants, environment variables, SDK upgrades, New Architecture, and React Compiler: read [02-development-builds-cng-config.md](./references/02-development-builds-cng-config.md).
- Mobile state, generated API clients, TanStack Query, network behavior, offline sync, SecureStore, AsyncStorage, SQLite, and filesystem storage: read [03-state-api-offline-storage.md](./references/03-state-api-offline-storage.md).
- Expo Modules API, native module API design, permissions/build-time configuration, lifecycle, background tasks, push notifications, deep links, and platform differences: read [04-native-modules-lifecycle-notifications.md](./references/04-native-modules-lifecycle-notifications.md).
- Rendering, lists, assets, startup, bundle analysis, native boundary performance, accessibility, unit/integration/E2E/native tests, release matrix, and QA scenarios: read [05-performance-accessibility-tests.md](./references/05-performance-accessibility-tests.md).

## Version Policy

- Existing repo: implement against pinned Expo SDK, React Native, React, Expo Router, EAS CLI, Node, package manager, native dependencies, app config, and EAS profiles.
- New project: use latest stable Expo choices only after checking official Expo, React Native, and EAS docs through `itsol-current-tech-context`.
- Install Expo and React Native version-sensitive packages with the repo's Expo-aware workflow, usually `npx expo install`, because Expo SDK compatibility controls the valid React Native package versions.
- Version-sensitive choices involving SDK upgrades, development builds, CNG/prebuild, config plugins, New Architecture, Expo Router, EAS, and OTA runtime compatibility require current official docs before finalizing.
