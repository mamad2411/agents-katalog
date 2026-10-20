---
name: cross-platform-mobile
description: Build, upgrade, debug, or ship cross-platform iOS/Android apps with Expo (React Native), bare React Native, or Flutter. Use this skill whenever the user mentions Expo, EAS, Expo Router, React Native, Flutter, Dart, TestFlight, Google Play target API level, app store submission, SDK upgrades, config plugins, native module errors, over-the-air updates, or asks which mobile stack to pick, even if they only say "mobile app" or "app for iPhone and Android". Not for websites, backend-only work, or fully native Swift/Kotlin apps.
---

# Cross-platform mobile

Default stack when the user has no preference and no existing repo: **Expo + TypeScript + Expo Router + EAS**. Deviate only for a reason from `references/stack-decision.md`.

## Workflow

1. **Detect the stack** from the repo: `app.json`/`app.config.*` + `expo` in package.json (Expo), `pubspec.yaml` (Flutter), `ios/` + `android/` committed with `react-native` and no `expo` (bare RN). Greenfield: read `references/stack-decision.md`.
2. **Check freshness.** Read `references/current-state.md`. If its date is older than 30 days, or any fact in it drives your recommendation (versions, store deadlines), verify with a live search and say when it disagrees with the file.
3. **Run `scripts/preflight.sh`** in the project root before changing anything. Fix FAIL lines first; report WARN lines.
4. **Read the stack reference** you need: `references/expo.md` or `references/flutter.md`.
5. **Change the smallest thing.** Never upgrade the framework and refactor features in the same commit.
6. **Verify** on both platforms: type-check, build or launch, exercise the changed flow. State plainly what you did not test (e.g. "iOS not built: no Mac available").
7. **Shipping?** Follow `references/release-checklist.md`.

## Hard rules

- Never state a framework version, target-SDK number, or store deadline from memory. Take it from `current-state.md` or a live source.
- Expo packages are installed with `npx expo install <pkg>`, never bare `npm install`, so versions match the SDK. Follow with `npx expo-doctor`.
- The Legacy Architecture is gone in current Expo SDKs. Do not add or suggest `newArchEnabled`.
- Anything prefixed `EXPO_PUBLIC_` is bundled into the app and readable by users. Never put secrets there; secrets live on a server or in EAS secrets used at build time only for non-runtime needs.
- Tokens and credentials go in `expo-secure-store` (or `flutter_secure_storage`), never AsyncStorage/SharedPreferences.
- In a managed/CNG Expo project, do not hand-edit `ios/` or `android/`. Use config plugins or `expo-build-properties`. If those folders are committed, treat it as bare and say so.
- Expo Go cannot run arbitrary native code. When a library needs native code outside Expo Go, switch to a development build.
- Every new permission needs three things: the runtime request, the iOS usage string, and a matching store privacy disclosure.
- OTA updates (EAS Update, Shorebird) ship JS/Dart and assets only. A native dependency change needs a new store build, and the runtime version must change with it.

## Output style

Give exact commands, not descriptions of commands. When proposing a dependency, name the alternative you rejected and why in one line.
