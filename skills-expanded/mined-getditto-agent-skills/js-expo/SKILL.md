---
name: js-expo
description: >
  Builds Ditto React Native apps with Expo development builds, prebuild and EAS. Uses @dittolive/ditto config plugin, shared native permissions and tested provider assets. Covers Expo Router integration, native rebuilds and Expo web routing; Expo Go cannot load Ditto.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto with Expo

Use [js-sdk](../js-sdk/SKILL.md) for API syntax, [js-react-native](../js-react-native/SKILL.md)
for native app lifecycle and [native-app-config](../native-app-config/SKILL.md) for OS
requirements. **Expo Go cannot run Ditto**; use a custom development build.

## New app recipe

The generator resolves sibling skills from this installation; install the complete
`ditto-js` plugin rather than copying only this folder.

```bash
python3 <installed-js-expo>/scripts/create-app.py ./DittoTasks
cd DittoTasks
npm install
npm run typecheck
npm run android
# On macOS with Xcode: npm run ios
```

Before launching, replace config.local.json's databaseID/offlineLicense with development
credentials. The placeholder is intentionally nonfunctional; never invent a license.
The generated .gitignore excludes it. The app builds without real credentials but cannot
start sync. Production auth must use the runtime's server/token-provider mode.

This baseline pins Expo 57.0.31, RN 0.86.3, React 19.2.3 and Ditto 5.2.0. It includes
loading/error/retry/empty states, permission handling, local CRUD, observer subscriptions,
and an application-level provider. Choose app IDs/name/icons before distributing it.
The generator refuses an existing directory; use a diff to integrate an existing app.

## Existing Expo project

1. Inspect the project's Expo SDK/RN pair, lockfile and native-directory ownership.
   Use `npx expo install --check` and `npx expo-doctor` to diagnose compatibility;
   don't force the starter's framework versions into an existing app.
2. Keep an already-installed `@dittolive/ditto` version. If it is absent, install
   the version the user asked for, or else the latest stable (npm `latest`, 5.2.0 when authored); use `npx expo install expo-dev-client
   @expo/config-plugins expo-build-properties` for framework-compatible peers.
3. Add `@dittolive/ditto` to app.json/app.config plugins once. The
   [app config](assets/app.json) supplies Bluetooth/local-network purpose strings.
   The shipping plugin merges Bonjour/background modes, Android permissions and native
   packagingOptions; it does **not** request Android runtime permissions or set all
   application-specific entitlements. Use the shared permission adapter too.
4. Generated native files are outputs. Keep durable changes in app config/config plugins.
   For optional data protection set ios.entitlements with the exact key/value in the
   [Apple guide](../native-app-config/references/apple.md). Do not inject developer-only
   native build workarounds into every project; inspect the installed plugin first.
5. Run `npx expo prebuild --no-install`, inspect native output, then build with
   `npx expo run:ios` / `npx expo run:android`. After dependency/plugin changes,
   regenerate and rebuild. `--clean` deletes native directories: use it only when
   generated native sources are reproducible and local edits are saved elsewhere.
6. Start Metro with `npx expo start --dev-client`. If the native module is missing,
   verify the installed binary was rebuilt with the same SDK as the JS bundle.

## Router and platform boundaries

For Expo Router, mount DittoProvider in the root layout around Slot/Stack, with the
runtime owned outside render. Put SDK initialization inside the runtime's start path,
not a component constructor. Navigation screen cleanup cancels queries, not the database.
The supplied starter uses registerRootComponent and needs no router dependency.

Expo web is a **browser target**: route to [js-web](../js-web/SKILL.md), serve WASM and
use browser storage limitations. Keep `.native` and `.web` bootstrap files if supporting
both; the native App asset's permissions/credential imports are not a web recipe.

## EAS, updates and release

A development profile uses developmentClient:true and internal distribution; select
an iOS simulator profile only for simulator builds. Preserve existing signing settings.
EAS uploads/builds are a separate deployment step; local generation and tests need no
EAS account. Configure secrets in the appropriate environment without committing them.
`EXPO_PUBLIC_*` values are embedded in JS and are not secrets.

An OTA update cannot add/change Ditto's native binary, permissions or entitlements.
Rebuild when native SDK/plugin/framework versions change and give incompatible binaries
separate runtimeVersion policies. Test the release artifact, not only a dev client.

## Verification

Run the generated project's typecheck, export both native bundles, inspect prebuild
outputs, compile/install on each platform, and execute the RN acceptance checks.
Keep these evidence levels separate when you report results.
Check regenerated config twice: arrays/permissions should not duplicate or erase other
plugins' settings. Native radio/background verification still requires real devices.

Sources: <https://docs.ditto.live/sdk/latest/install-guides/react-native>,
<https://docs.expo.dev/workflow/continuous-native-generation/>,
<https://docs.expo.dev/develop/development-builds/introduction/>.

## Framework compatibility boundary

The starter enables `expo-build-properties` → `ios.enableSceneSupport`. Xcode 27 /
iOS 27 require the scene lifecycle; Expo 57 needs this explicit opt-in and the pinned
patches include its implementation. Do not remove it merely because compilation passes.
See [Expo’s scene migration guide](https://github.com/expo/fyi/blob/main/ios-scene-lifecycle.md).

Ditto 5.2.0 failed native iOS compilation with Expo 58.0.22 / RN 0.88.1 during
verification: its published DittoRNSDK.mm still references `RCTCxxBridge.runtime`,
which that RN release removed. Use the verified 57/0.86 combination for this starter;
recheck the published Ditto native bridge before upgrading. Do not patch node_modules
or disable architecture/type checks to hide an unsupported pairing.

The pinned Expo 57 Android template defaults to Kotlin 2.1.20, which cannot read
Ditto 5.2.0's rustls Kotlin 2.3 metadata. The starter sets `android.kotlinVersion`
to 2.3.0 and aligns the root Kotlin Gradle plugin through the scoped
[compiler plugin](assets/plugins/with-kotlin-compiler.cjs). Both are needed; the
property alone leaves other modules on the old compiler. The plugin rejects an
unknown Gradle template instead of silently editing the wrong dependency.
