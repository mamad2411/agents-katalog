---
name: rnrepo
description: "Best practices for integrating and using RNRepo — Software Mansion's infrastructure for pre-built React Native library artifacts that reduces native build times by up to 2×. Use when setting up, configuring, or troubleshooting RNRepo in a React Native or Expo project. Trigger on: 'RNRepo', 'rnrepo', 'slow builds', 'build times', 'prebuilt artifacts', 'prebuilt libraries', '@rnrepo/expo-config-plugin', '@rnrepo/build-tools', 'prebuilds-plugin', 'rnrepo.config.json', 'DISABLE_RNREPO', 'packages.rnrepo.org', 'Maven prebuild', 'CocoaPods prebuild', 'xcframework prebuild', 'prebuild AAR', 'build from source', 'native compilation slow', 'Gradle plugin slow', 'pod install slow', 'CI build times'."
license: MIT
---

# RNRepo

Software Mansion's infrastructure for pre-building and distributing React Native library artifacts, reducing native build times by up to **2×** with zero infrastructure changes.

Read the relevant reference for the topic at hand. All references are in `references/`.

## Key facts

- **Beta, New Architecture only.** Works with React Native latest patches of 0.77, 0.78, 0.79 and all versions above 0.80.0.
- **How it works:** A Gradle plugin (Android) and CocoaPods plugin (iOS) intercept the build and substitute libraries with prebuilt artifacts from `packages.rnrepo.org`. Falls back to source if a prebuild is unavailable.
- **Expo CNG:** Use `@rnrepo/expo-config-plugin` — it configures both Android and iOS automatically.
- **Standard RN:** Install `@rnrepo/build-tools` and edit `android/build.gradle`, `android/app/build.gradle`, and `ios/Podfile` manually.
- **Opt out per library:** Add a `rnrepo.config.json` with a `denyList` at the project root. Required for libraries with **native patches** (Objective-C/Java/Kotlin). JS-only patches do NOT require opting out.
- **Opt out entirely:** Set `DISABLE_RNREPO=1` environment variable before the build command.

## References

| File | When to read |
|------|-------------|
| `references/installation.md` | Setting up RNRepo for the first time — Expo CNG, standard React Native, Android Gradle, iOS CocoaPods |
| `references/configuration.md` | Opting out specific libraries (denyList), disabling the plugin, Fingerprint config, GPG verification |
| `references/troubleshooting.md` | Build failures, C++ debug/release mismatch, duplicate `.so` files, Xcode version issues, empty repository list, verifying the plugin works |

## Purpose
Integrate and troubleshoot RNRepo (pre-built React Native library artifacts) to cut native build times up to 2x.

## When to use
Setting up, configuring or troubleshooting RNRepo in a React Native project.

## When NOT to use
- Projects on the old architecture or unsupported RN versions.
- JS-only build speed problems.

## Inputs
React Native version, Android/iOS build config, current build times.

## Core workflow
1. Check version and New Architecture support (Key facts).
2. Add the Gradle plugin (Android) and CocoaPods plugin (iOS) per references.
3. Run a clean build and compare times.
4. Troubleshoot using the relevant file in `references/`.

## Output requirements
Configured project and before/after build times.

## Example
```text
RN 0.79 app -> add plugins -> clean build drops from 12 to 7 minutes.
```

## Related skills
react-native-best-practices, radon-mcp
