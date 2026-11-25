---
name: js-react-native
description: >
  Builds and troubleshoots Ditto React Native CLI applications on iOS and Android using @dittolive/ditto: native linking, Hermes/JSI, permissions, lifecycle, providers and device tests. Routes Expo projects to js-expo and shares native config with Swift/Kotlin.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto React Native

Use [js-sdk](../js-sdk/SKILL.md) for SDK syntax and [native-app-config](../native-app-config/SKILL.md)
for OS declarations. For an Expo project use [js-expo](../js-expo/SKILL.md).

## Build an existing or new app

1. Inspect package.json, lockfile, ios/Podfile, Android Gradle files and architecture
   settings. Use the project's package manager. This starter baseline is Ditto 5.2.0,
   RN 0.86.3 / React 19.2.3 (New Architecture, Hermes). For a different RN line inspect
   the installed SDK's codegen/Gradle/podspec and build it; broad minimum-version docs
   do not establish every React Native/New Architecture combination.
2. Keep an already-installed `@dittolive/ditto` version; otherwise install the
   version the user asked for, or else the latest stable (npm `latest`, 5.2.0 when authored). For the provided string-UUID task UI also install
   `uuid@11.1.0`, `react-native-get-random-values@1.11.0`, and the framework-compatible
   `react-native-safe-area-context`. Wrap the root in SafeAreaProvider; the core RN
   SafeAreaView can leave Android edge-to-edge controls under the status bar. Verify autolinking with
   `npx react-native config`; the dependency must appear once. Install CocoaPods
   through the existing Gemfile/Bundler workflow when present (`bundle exec pod install`
   from ios), and open the .xcworkspace. Do not add another native Ditto SDK manually.
3. Apply [Apple configuration](../native-app-config/references/apple.md) to the app
   target and [Android configuration](../native-app-config/references/android.md) to
   the merged application manifest. Do not assume library manifests supply permissions:
   the published 5.2.0 RN manifests are empty. Expo's plugin adds them separately.
4. Before starting mesh sync, use [permission adapter](assets/permissions.ts) with
   the shared [permission plan](../native-app-config/assets/android-permissions.ts).
   The plan branches on API 23/31/33; Android 12 Wi-Fi Aware still needs location.
   Explain the request, handle denial and never-ask-again, offer Settings and recheck
   on return. Do not repeatedly prompt. A local-only fallback may open the store and
   keep sync stopped; denied permissions must not be represented as mesh-ready.
5. Copy [runtime](../js-sdk/assets/runtime.ts), [provider/hook](../js-sdk/assets/DittoProvider.tsx),
   [tasks](../js-sdk/assets/tasks.ts), [TasksScreen](assets/TasksScreen.tsx) and
   [App](assets/App.tsx) into the app's src directory. The starter expects a local
   config JSON outside src; keep it out of version control. Mount above navigation.
   The Expo generator assembles these same assets into a runnable project.
6. Use sandbox-relative persistent directories; no Node fs/path imports in native code.
   Keep one application/account owner. Preserve user data on errors, and await close
   during account replacement after unmounting consumers and draining writes.
7. Build and run iOS and Android; a successful Metro bundle does not prove native linking.
   Turn off remote JS execution/debuggers that move JS outside the device's JSI runtime.
   Use on-device Hermes debugging. A missing native module needs a rebuild, not a JS retry.

## Android build configuration

For duplicate native libraries, apply the scoped packagingOptions recommended by the
[Ditto install guide](https://docs.ditto.live/sdk/latest/install-guides/react-native)
to android/app/build.gradle: pickFirst for `lib/**/libdittoffi.so`, `libjsi.so`,
`libreact_nativemodule_core.so`, `libturbomodulejsijni.so`, `libreactnative.so`.
Preserve the app's AGP syntax (jniLibs.pickFirsts on newer DSLs). Do not broadly pick
all `.so` files to conceal unrelated dependency conflicts. Keep generated NDK/Kotlin
versions compatible with the RN template; don't downgrade to old doc example values.

## Lifecycle, background and updates

AppState transitions are not permission grants. Decide whether the product needs
foreground-only sync (stop on background, resume after permission recheck) or background
work; document that choice. iOS background modes grant limited opportunities, not
unlimited execution. Android long-running connected-device work requires a real native
foreground service, notification and service-type permissions; see shared config.
No JavaScript timer can keep the OS process alive indefinitely.

Fast Refresh can leave a native instance alive while replacing JS. If a directory-lock
error occurs, perform a full reload/restart and disable Fast Refresh for that session;
never generate random storage paths or delete the database. A global variable is not
a guarantee across JS runtime resets. Native SDK updates require an app binary rebuild.

## Acceptance checks

- Launch, grant/deny permissions, add/edit/delete while disconnected, force quit and
  relaunch: local native data remains. Observe errors and loading/empty UI.
- Unmount/remount the screen and change filters: no duplicate observers or old rows.
- Two physical devices, same database and authorized identity: subscribe on both,
  write on one and observe the other, repeat without internet; record actual transport.
- Test denial/revocation, device lock/background/foreground, and reconnect on iOS/Android.
- Check release signing, Android merged manifest and packaged iOS plist/entitlements.

Simulators/emulators prove app integration only, not BLE or Wi-Fi Aware. Record each
check's device, OS, SDK version and outcome.

Sources: <https://docs.ditto.live/sdk/latest/install-guides/react-native>,
<https://docs.ditto.live/sdk/latest/compatibility/react-native>, published package build files.

## Native compiler and signing checks

The published Ditto 5.2.0 Android rustls dependency contains Kotlin 2.3 metadata.
Old Kotlin 2.1 compiler templates fail to read it. Align the actual root Kotlin
Gradle plugin/compiler with the selected RN template; changing only a stdlib property
is insufficient. Do not suppress metadata-version validation. The Expo recipe pins a
verified framework combination rather than copying old Kotlin values from install examples.

On iOS, keep embedding/signing enabled for DittoCore, including simulator builds.
Use ad-hoc simulator signing (`CODE_SIGN_IDENTITY=-`) instead of
`CODE_SIGNING_ALLOWED=NO`; an unsigned embedded framework can build and then fail
at launch with a dyld signature error. Follow the [Expo compatibility boundary](../js-expo/SKILL.md#framework-compatibility-boundary)
for scene lifecycle requirements and the verified RN release; new RN versions can
remove native bridge APIs even when JavaScript typechecking passes.
