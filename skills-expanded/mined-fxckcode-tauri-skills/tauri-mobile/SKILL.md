---
name: tauri-mobile
description: Build, run, test, and ship Tauri 2 Android and iOS applications across native toolchains. Use when adding mobile targets, selecting devices, handing off to native IDEs, or preparing mobile distribution.
---

# Tauri mobile

This skill is scoped to Tauri 2. Verify version-sensitive fields and commands against the installed Tauri CLI and the current [official mobile documentation](https://v2.tauri.app/start/prerequisites/).

## Workflow

1. Confirm the mobile target and host OS. Android requires the Android Studio/SDK toolchain, platform tools, an installed API level, and a configured device or emulator. iOS development requires macOS, Xcode, Apple platform components, signing identity, and a simulator or registered device. Check the [prerequisites](https://v2.tauri.app/start/prerequisites/) page before changing project files.
2. Inspect `src-tauri/`, `tauri.conf.json`, frontend build settings, capabilities, plugins, and lockfiles. Add mobile targets using the installed CLI's `tauri android init` or `tauri ios init` flow; do not hand-copy generated native projects.
3. Start development with the CLI (`tauri android dev` or `tauri ios dev`) and select the intended emulator/device using the CLI's current device-list and device-selection options. Verify the frontend dev URL is reachable from the target and that native logs are visible.
4. When native changes are needed, use `tauri android` with Android Studio or `tauri ios` with Xcode as the documented handoff. Keep generated native project changes reviewable and rerun the CLI after configuration changes where required.
5. Review mobile capability differences: filesystem, notifications, deep links, biometric, camera, and other plugins may have different permissions, implementations, or support on Android and iOS. Test denied and unavailable-platform behavior rather than assuming desktop parity.
6. Before release, build each target in a clean, signed environment. Verify bundle identifiers, entitlements/manifest permissions, icons/resources, minimum OS versions, provisioning/signing, store metadata, update strategy, and rollback plan using the [mobile distribution](https://v2.tauri.app/distribute/) guidance.

## Constraints

- Mobile apps use native WebViews and platform packaging; a desktop dev build is not evidence of mobile correctness.
- Do not commit signing keys, provisioning profiles, keystores, or API credentials.
- Do not promise in-app updater behavior or identical plugin support on mobile without testing the target store/platform rules.
- Keep Android and iOS configuration explicit and separate where their permissions, lifecycle, or release policies differ.

## Official navigation

- [Create a project](https://v2.tauri.app/start/create-project/)
- [Mobile development and dev server](https://v2.tauri.app/develop/)
- [Mobile plugin development](https://v2.tauri.app/develop/plugins/develop-mobile)
- [Distribution](https://v2.tauri.app/distribute/)
