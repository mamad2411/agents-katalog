---
name: flutter-release
description: Release-time conventions for this Flutter project — the `pubspec.yaml` `version: X.Y.Z+N` bump that stamps both native shells, `key.properties`-driven Android signing, fastlane match for iOS, the divergent per-store changelog layouts, Crashlytics / Sentry symbol upload on both sides, and the pre-release `flutter` command sequence. Load whenever cutting a build, bumping the version, regenerating signing config, or shipping to Play Console / App Store Connect. Intentionally small — does not duplicate the full app scaffolding (see `flutter-app-skeleton` for that).
---

# Flutter release

Everything a release pass touches across both platforms, and nothing it doesn't. One page so it's cheap for `flutter-release-engineer` to preload — `flutter-app-skeleton` is overkill for shipping work.

## Version-bump shape

`pubspec.yaml` is the single source of truth. One line moves per release:

```yaml
# pubspec.yaml
version: 1.4.0+17
```

- `1.4.0` is the marketing / user-visible version. Becomes Android's `versionName` and iOS's `CFBundleShortVersionString` (`MARKETING_VERSION`).
- `+17` is the build number. Becomes Android's `versionCode` and iOS's `CFBundleVersion` (`CURRENT_PROJECT_VERSION`).

`flutter build` reads `pubspec.yaml` and stamps **both** native projects automatically. **Don't** hand-edit `android/app/build.gradle.kts` `versionCode` / `versionName` or `ios/Runner/Info.plist` `CFBundleVersion` / `CFBundleShortVersionString` — those are templated from `pubspec.yaml` at build time, and any local edit drifts on the next `flutter build`.

For CI, the same can be overridden per-invocation without touching `pubspec.yaml`:

```bash
flutter build appbundle --release --build-name=1.4.0 --build-number=17
flutter build ipa       --release --build-name=1.4.0 --build-number=17
```

Rules:
- **Build number must be strictly monotonic across BOTH stores' shipped builds for the same marketing version.** TestFlight rejects a build whose `CFBundleVersion` ≤ the last accepted; Play Console rejects a track whose `versionCode` ≤ the highest shipped on any track. The safe rule for Flutter: never reuse a `+N`, period — bump it for every shipped artifact, even a hotfix to one store only.
- `1.4.0` is whatever marketing wants. Don't gate the build on it.
- Read the file before bumping. Concurrent PRs that both bump are the most common merge conflict — land the bump that's strictly higher than the release branch *right now*.

## Android signing (`key.properties`-driven)

Flutter's convention is `android/key.properties` (same shape as native Android's `keystore.properties`; wired in `android/app/build.gradle.kts`). The scaffold ships an unsigned debug build by default.

```properties
# android/key.properties.example  (committed; the real file is gitignored)
storePassword=changeme
keyPassword=changeme
keyAlias=release
storeFile=../release.keystore
```

Wire-up in `android/app/build.gradle.kts`:

```kts
val keystoreProps = Properties().apply {
    val f = rootProject.file("key.properties")
    if (f.exists()) f.inputStream().use(::load)
}

android {
    signingConfigs {
        if (keystoreProps.isNotEmpty()) {
            create("release") {
                storeFile = file(keystoreProps.getProperty("storeFile"))
                storePassword = keystoreProps.getProperty("storePassword")
                keyAlias = keystoreProps.getProperty("keyAlias")
                keyPassword = keystoreProps.getProperty("keyPassword")
            }
        }
    }
    buildTypes {
        release { if (keystoreProps.isNotEmpty()) signingConfig = signingConfigs.getByName("release") }
    }
}
```

Rules:
- The block is **silent** until `key.properties` exists — that's why local debug builds work for contributors without the keystore.
- On CI: write `key.properties` from a CI secret before `flutter build`. Never check it in. Decode the keystore from a base64 secret too.
- `.gitignore` must include `android/key.properties` and `*.keystore` / `*.jks`.

## iOS signing (fastlane match)

Shared signing assets live in a private git repo, encrypted with a passphrase; `fastlane match` pulls them down to CI and to dev machines. The hard rule is identical to a native iOS project:

- **No committed `.p12`, `.mobileprovision`, or `ExportOptions.plist` containing a team ID + UUID.** Match owns those.
- **App Store Connect API key** (`.p8` + key ID + issuer ID) lives in CI secrets — `fastlane pilot upload` reads it via env vars. Don't commit the `.p8`.
- `fastlane match appstore` before `flutter build ipa` on CI; locally, `match development` for device debug.

## fastlane changelog layout (divergent per platform)

Most Flutter teams write release notes once and script them into both layouts. The two layouts:

```
fastlane/
└── metadata/
    ├── android/
    │   ├── en-US/changelogs/17.txt    # build-number → release notes (≤ 500 chars)
    │   └── fr-FR/changelogs/17.txt
    └── <locale>/release_notes.txt     # iOS — one file per locale, overwritten per release
        # e.g. fastlane/metadata/en-US/release_notes.txt
```

- Android: one `<buildNumber>.txt` per locale; the `+N` from `pubspec.yaml`. Missing locales fall back to `en-US`. Don't commit a changelog for a `buildNumber` that doesn't exist yet — `supply` errors on dangling files.
- iOS: `release_notes.txt` is overwritten on every release — App Store Connect stores history server-side.

## Crashlytics / Sentry symbol upload

Crashlytics requires native plugin setup on both sides; Flutter doesn't unify it.

- **Android:** `cd android && ./gradlew :app:uploadCrashlyticsMappingFileRelease` after `flutter build appbundle --release`. Only exists when the Crashlytics Gradle plugin is applied.
- **iOS:** the `upload-symbols` run-script phase in Xcode runs automatically on archive when the Firebase Crashlytics pod is integrated. Verify it's wired in `Runner` target → Build Phases.
- **Sentry alternative for greenfield projects:** the `sentry_dart_plugin` package handles both platforms from a single Dart-side config (`sentry.properties` + `pubspec.yaml` entry). Recommend it for new projects — one tool instead of two.

## Pre-release command sequence

Run sequentially; bail on the first failure:

```bash
flutter analyze
flutter test
flutter build appbundle --release    # Android .aab for Play Store
flutter build ipa --release          # iOS archive for App Store
```

Notes:
- `flutter build apk --release` produces a sideload-only `.apk`. **Never upload an `.apk` to Play Console** — the dynamic delivery features (per-device split) only work from a bundle.
- `flutter build ipa --release` writes `build/ios/ipa/*.ipa`; `fastlane pilot upload --ipa build/ios/ipa/*.ipa` ships it to TestFlight.

## Pre-release checklist

Verify in this order:

1. **Build number strictly greater than the last shipped on BOTH stores.** Cross-reference TestFlight + Play Console internal track. Bump `+N` once for both.
2. **Signing material present in CI:** `android/key.properties` decoded from secret; iOS match repo accessible; App Store Connect API key in env.
3. **Changelog files in both layouts** for every locale you ship to (Android per-buildNumber file; iOS overwritten `release_notes.txt`).
4. **Native plugin sync:** `flutter pub get` ran, iOS pods up to date (`cd ios && pod install`). Stale pods after a plugin bump are the #1 surprise iOS archive failure.
5. **Crashlytics / Sentry symbol upload wired** on both platforms (verify the Xcode run-script phase is enabled and Gradle task exists on Android).
6. **No `print(...)` left in critical paths.** `flutter analyze` enforces this via the `avoid_print` lint when configured in `analysis_options.yaml`.
7. **Bundle, not APK, for Android upload.** Confirm `build/app/outputs/bundle/release/*.aab` exists.

## What the release engineer doesn't do

- **No manual edits to `android/app/build.gradle.kts` version fields or `ios/Runner/Info.plist` `CFBundleVersion`** — let `flutter build` stamp them from `pubspec.yaml`. Manual edits drift on the next build.
- **No feature changes.** If a release is blocked by a bug, file it and hand off — `flutter-build-expert` or `flutter-architect` fixes.
- **No commits of signing material.** Keystores, `key.properties`, decoded base64 secrets, `.p12`, `.mobileprovision`, App Store Connect `.p8` — none of these touch the repo.
- **No `dart format` on the release branch.** CI runs it on every PR; the release branch should already be clean. Reformatting at release time bloats the diff for no signal.

## Hard nos

- No build-number reuse across stores' shipped builds. Both stores reject duplicates; bump every artifact.
- No `flutter build apk` for Play Store upload — bundles only.
- No shipping a Flutter Profile or Debug build to either store. `--release` always.
- No `--no-tree-shake-icons` or other diagnostic flags carried into a release build. Strip experimental flags before tagging.
- No `applicationIdSuffix` / iOS bundle ID change between releases of the same shipped app — different ID = different app to both stores, ratings reset.
