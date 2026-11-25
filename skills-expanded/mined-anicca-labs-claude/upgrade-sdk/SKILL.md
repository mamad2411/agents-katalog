---
name: upgrade-sdk
description: Upgrade an Expo SDK major version reliably (deps, patches, native rebuild, verification). Use when bumping Expo SDK / React Native, or when an upgrade breaks Metro bundling, native modules, or app startup.
---

# Upgrading Expo SDK

A major SDK bump (e.g. 55 → 56) is a **native upgrade**, not a dependency tweak. Static checks (tsc/lint/jest) pass while the app fails to build or boot — so the work isn't done until a dev client is rebuilt **and** the bundle compiles **and** the app boots on a simulator.

> Check the reference apps (`anicca-labs/reflect`, `anicca-labs/virtual-wallet`) `package.json` / `app.config.ts` / `eas.json` for a known-good post-upgrade state before starting.

## Sequence

1. **Bump core:** `yarn add expo@^<major>` then `yarn expo install --fix`. This aligns native modules but **skips some devDeps** — bump these manually: `jest-expo`, `eslint-config-expo`, `expo-build-properties`, `@types/react`.
2. **Re-port `yarn patch` patches** against the new version. The patch protocol string is version-pinned (`patch:expo-updates@npm%3A55.0.24#…`); run `yarn patch <pkg>`, re-apply the same hunks to the new source, `yarn patch-commit`, delete the stale patch file. (Only third-party packages use `yarn patch` — never `@anicca-labs/*`; fix those at source.)
3. **Update `resolutions` / pinned ranges** to the new SDK version (e.g. `expo-constants`).
4. **TypeScript 6:** set `ignoreDeprecations: "6.0"` in tsconfig (the `baseUrl` deprecation hard-errors otherwise).
5. **Verify static:** `tsc --noEmit`, `expo-doctor` (expect N/N), `jest`, `lint`.
6. **Rebuild the dev client** (`dev-client-ios` / `dev-client-android`) AND **compile the bundle** (`expo export`, or start Metro and load on a sim). This is where the real errors surface.
7. **Boot it on a simulator** and confirm it renders past the splash on both platforms.

> **Register config-providing Expo modules in `plugins[]`.** `expo install --fix` can't edit a dynamic `app.config.ts`, so it may finish with _"Cannot automatically write to dynamic config at: app.config.ts — Add the following to your Expo config"_ followed by a `plugins` array. Add exactly the modules it prints to your `plugins[]`: these are installed Expo modules that ship a config plugin, and listing them applies their native config at prebuild (autolinking handles the native module; config plugins must be listed explicitly). The list is **app-specific** — copy whatever the CLI prints rather than assuming a fixed set (in reflect it was `expo-font`, `expo-image`, `expo-localization`, `expo-status-bar`, `expo-web-browser`).

## Known breakage to expect

### Metro: "Cannot find module '@babel/plugin-transform-computed-properties'"

`@react-native/babel-preset` dynamically `require()`s babel plugins that the upgrade churn can prune from the tree. Add the missing one explicitly as a devDep (`yarn add -D @babel/plugin-transform-computed-properties`). Confirm by grepping the preset's required plugins for resolvability.

### Metro: "expo-router is no longer compatible with react-navigation" (SDK 56+)

expo-router forbids direct `@react-navigation/*` **value** imports. Migrate:

- `@react-navigation/native` → `expo-router/react-navigation` (ThemeProvider, DefaultTheme, DarkTheme)
- `@react-navigation/material-top-tabs` → `expo-router/js-top-tabs` (createMaterialTopTabNavigator)
- `@react-navigation/bottom-tabs` → `expo-router/js-tabs`
- `@react-navigation/elements` → `expo-router/react-navigation` (PlatformPressable)

Keep precise **types** with a type-only import from the original package (erased at build, doesn't trip the runtime check):

```ts
import { createMaterialTopTabNavigator } from 'expo-router/js-top-tabs';
import type { MaterialTopTabBarProps } from '@react-navigation/material-top-tabs';
```

### App crashes at startup: "Property 'MessageQueue' doesn't exist" (+ Expo modules "reading 'get'")

This is a **stale dev client** — the installed native binary is from before the upgrade and doesn't match the new JS bundle. The JS is fine; **rebuild and reinstall the dev client**. Don't debug the JS.

### Testing deps

- `jest` must be a **direct devDep** (`jest@29` for SDK 56) — jest-expo no longer bundles it.
- RNTL 14 needs the **`test-renderer@^1.0.0`** peer (replaces `react-test-renderer`).
- RNTL ≥12.4 auto-includes Jest matchers — remove `setupFilesAfterEnv: ['@testing-library/react-native/extend-expect']` (that path no longer exists).

### iOS: static frameworks + force-static the RN-Firebase pods (SDK 56)

If you use `@react-native-firebase/*`, SDK 56's pod graph needs `expo-build-properties` configured with `ios.useFrameworks: 'static'` **and** `forceStaticLinking` of the Firebase pods — otherwise the iOS build fails on the Firebase static/dynamic linking mismatch. In reflect's `app.config.ts` plugin block:

```ts
['expo-build-properties', {
  android: { minSdkVersion: 24 },
  ios: { useFrameworks: 'static', forceStaticLinking: ['RNFBApp', 'RNFBAnalytics', 'RNFBMessaging'] },
}]
```

List the `RNFB*` pods for exactly the Firebase modules you actually install.

### Native lib bumps can break iOS pods

A "stay current" bump (e.g. `react-native-purchases` 10.0.1 → 10.3.x) can pull an iOS pod version CocoaPods can't resolve, failing only the iOS build while Android passes. Pin native libs to a known-good version; don't bump them as part of an SDK upgrade unless required.

### CI store builds (SDK 56): iOS Xcode, Android disk, Apple purpose strings

A full `eas build --local` store deploy on a CI runner surfaces three SDK-56 issues that local builds (newer Xcode, plenty of disk) don't:

- **iOS needs Xcode 26.4.** SDK 56 ships `expo-modules-jsi` with `weak let`, which only the Swift toolchain in **Xcode 26.4+** accepts — older Xcode 26.x (e.g. 26.0) fails the `ExpoModulesJSI` xcframework build with `'weak' must be a mutable variable`. The `macos-15` runner tops out at Xcode 26.3, so use **`runs-on: macos-26`** and select **Xcode 26.4**. A `SWIFT_VERSION=5.0` post_install config plugin is a dead end here (it doesn't touch the prebuilt xcframework build) — fix the toolchain, not the language mode. After confirming this, **delete any now-obsolete `withSwiftVersion`-style pod patch plugins** under `plugins/` — building on Xcode 26.4 makes them dead code, and a leftover one only invites confusion.
- **Android: free disk before the build.** The full multi-ABI release build + lint-vital AARs exhausts the ubuntu runner's ~14 GB disk; `react-native-reanimated:bundleReleaseLocalLintAar` then fails with `Could not add file ... to ZIP` (it's disk, not reanimated). Add a step that removes unused toolchains (dotnet, ghc/.ghcup, swift, CodeQL, docker images) — keep the Android SDK/NDK and the hosted tool cache (Node).
- **iOS submit hits ITMS-90683 (missing purpose string).** Bundled SDKs (RevenueCat, expo-image, rive, react-native-svg) reference Photo Library APIs, so Apple rejects the _uploaded_ binary unless `NSPhotoLibraryUsageDescription` is in `ios.infoPlist` — even if the app never picks a photo. Note `eas submit` "success" only means _uploaded_; Apple validates asynchronously and emails the rejection.
- **CI toolchain: Node 23 + Corepack-managed Yarn 4, `package-manager-cache: false`.** Build the SDK 56 native deploy on **Node 23**, enable **Corepack**, and `corepack prepare yarn@4.9.2 --activate` (match `packageManager` in package.json). On `actions/setup-node@v5` you **must** set `package-manager-cache: false` — its default `true` runs the global Yarn 1 _before_ Corepack is enabled and fails against a `yarn@4.x` pin.

## Reliability rules

- **Capture real exit codes.** Running `cmd; echo "done"` in a background task makes the task exit 0 even when `cmd` failed (the echo's status wins). Check the actual command's `$?` and grep the log for `Build failed` / non-zero — don't trust a green wrapper.
- **Verify bumps with a real run.** A major dependency or GitHub-Action bump can break via a changed **default** (not just changed inputs). Run the actual build/CI before declaring it safe.
- **Keep the upgrade PR clean.** Don't run repo-wide `prettier --write` as part of an upgrade — it buries the real changes under formatting noise. Formatting is a separate PR.
