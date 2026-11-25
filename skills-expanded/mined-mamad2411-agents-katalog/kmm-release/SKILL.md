---
name: kmm-release
description: Release-time conventions for this Kotlin Multiplatform project — version sync across the shared module and both apps, Android `versionCode`/`versionName` bumps + keystore-driven signing, iOS `MARKETING_VERSION`/`CFBundleVersion` bumps + fastlane match, XCFramework rebuild, fastlane changelog layouts for both stores, Crashlytics mapping + dSYM uploads, and the combined pre-release Gradle/xcodebuild command sequence. Load whenever cutting a build on either platform, bumping versions, regenerating signing, or shipping. Intentionally small — does not duplicate the app skeleton (see `kmm-app-skeleton`).
---

# KMM release

Everything a KMP release pass touches across both stores, and nothing it doesn't. KMM ships from one shared module into two apps (`:androidApp` to Play, `iosApp/` to App Store), so every release is two parallel pipelines that share business logic and diverge on packaging, signing, and metadata.

## Version sync across the shared module + both apps

`:shared` is an artifact — it has no user-facing version. Both apps do. The convention here is **(a) a single marketing version in `gradle/libs.versions.toml`, read by both apps**:

```toml
# gradle/libs.versions.toml
[versions]
appMarketing = "1.4.0"
```

Android side (`:androidApp/build.gradle.kts`):

```kts
android {
    defaultConfig {
        versionCode = 17                                      // store-specific monotonic
        versionName = libs.versions.appMarketing.get()        // shared marketing string
    }
}
```

iOS side — write the marketing version into an xcconfig the project reads:

```bash
# scripts/sync-ios-version.sh — called from a Gradle task or CI step
VERSION="$(./gradlew -q :shared:printAppMarketing)"
sed -i.bak "s/^MARKETING_VERSION = .*/MARKETING_VERSION = $VERSION/" iosApp/Config/Version.xcconfig
```

Rules:
- **`versionName` / `MARKETING_VERSION` are shared.** They're whatever marketing wants and they should match across stores so support tickets line up.
- **`versionCode` (Android) and `CFBundleVersion` (iOS) are NOT shared.** Each store enforces its own monotonic counter across all tracks and TestFlight builds. A single shared integer breaks the moment one store needs an extra hotfix build.
- Read both `:androidApp/build.gradle.kts` and `iosApp/Config/Version.xcconfig` before bumping — concurrent PRs that bump are the most common merge conflict.

Independent-bump policy (option (b)) is sometimes right when the two apps have intentionally diverged (e.g. iOS lagging on a feature). Use it deliberately; default is sync.

## Android side

`:androidApp/build.gradle.kts` is the source of truth for the Android bump. Same shape as a single-stack Android repo — `versionCode` strictly increasing across **all** shipped tracks and flavors.

Signing config reads from a root-level `keystore.properties`:

```kts
val keystoreProps = Properties().apply {
    val f = rootProject.file("keystore.properties")
    if (f.exists()) f.inputStream().use(::load)
}

android {
    signingConfigs {
        if (keystoreProps.isNotEmpty()) {
            create("release") {
                storeFile = rootProject.file(keystoreProps.getProperty("storeFile"))
                storePassword = keystoreProps.getProperty("storePassword")
                keyAlias = keystoreProps.getProperty("keyAlias")
                keyPassword = keystoreProps.getProperty("keyPassword")
            }
        }
    }
    buildTypes {
        release {
            if (keystoreProps.isNotEmpty()) signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

The signing block is **silent** until `keystore.properties` exists — that's why local debug builds work for contributors who don't have the keystore. On CI, write `keystore.properties` (and decode the keystore from a base64 secret) before invoking Gradle; never commit either. `.gitignore` must include `keystore.properties` and `*.keystore`.

Build the release artifact:

```bash
./gradlew :androidApp:bundleRelease            # .aab for Play Store
./gradlew :androidApp:assembleRelease          # .apk for sideload only
```

Don't upload an `.apk` to Play Console — bundle-only features (per-device split delivery) require the `.aab`.

## iOS side

`iosApp/iosApp.xcodeproj` reads `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` (== `CFBundleVersion`, the iOS build number) from xcconfig:

```
// iosApp/Config/Version.xcconfig
MARKETING_VERSION = 1.4.0
CURRENT_PROJECT_VERSION = 42
```

The shared framework is rebuilt before the iOS archive. Two paths exist:

```bash
./gradlew :shared:packForXcode              # writes the framework into the iOS build dir
# or (preferred for CI) the embedAndSign script the Xcode "Run Script" phase calls:
./gradlew :shared:embedAndSignAppleFrameworkForXcode
```

For external consumption (SPM `binaryTarget` / a published Pod) you assemble an XCFramework instead — see "Shared module distribution" below.

Signing: **fastlane match** for certificates and provisioning profiles. The release engineer runs `bundle exec fastlane match appstore --readonly` on CI; the read-write call only happens when a profile expires or a new device is registered.

Archive + export:

```bash
xcodebuild archive \
  -workspace iosApp/iosApp.xcworkspace \
  -scheme iosApp \
  -configuration Release \
  -archivePath build/iosApp.xcarchive

xcodebuild -exportArchive \
  -archivePath build/iosApp.xcarchive \
  -exportOptionsPlist iosApp/ExportOptions.plist \
  -exportPath build/iosApp-export
```

Upload to TestFlight with **fastlane pilot**:

```bash
bundle exec fastlane pilot upload --ipa build/iosApp-export/iosApp.ipa
```

## fastlane changelog layout

The two stores have divergent shapes. Both live under `fastlane/`:

```
fastlane/
├── metadata/
│   ├── android/                              # supply (Play Console)
│   │   ├── en-US/changelogs/17.txt           # versionCode → release notes, ≤ 500 chars
│   │   └── fr-FR/changelogs/17.txt
│   └── en-US/                                # deliver (App Store Connect)
│       └── release_notes.txt                 # single file, overwritten each release
└── Fastfile
```

Android: one `<versionCode>.txt` per locale, dangling files break `supply`. iOS: a single `release_notes.txt` per locale, overwritten — App Store Connect tracks history server-side. Commit both before tagging the release.

## Shared module distribution (optional)

Most KMM projects keep `:shared` private to the repo and don't publish it. If yours does, the two flows:

**XCFramework via SPM `binaryTarget`:**

```bash
./gradlew :shared:assembleXCFramework        # outputs shared/build/XCFrameworks/release/
```

Upload the zipped XCFramework, compute its checksum with `swift package compute-checksum`, and bump the URL + checksum in the consuming `Package.swift`.

**CocoaPods:** if the project ships a podspec, run `./gradlew :shared:podspec` to regenerate it, then `pod lib lint` and `pod trunk push`.

If neither applies, skip this section — `:shared` is consumed in-repo via the embedAndSign script and there's nothing to publish.

## dSYM / mapping uploads

Android (R8 mapping → Crashlytics):

```bash
./gradlew :androidApp:uploadCrashlyticsMappingFileRelease
```

Task only exists when the Crashlytics Gradle plugin is applied. Automate in CI right after `bundleRelease`.

iOS dSYMs — two routes depending on which crash backend you use:

```bash
# Firebase Crashlytics — the upload-symbols script ships with the SDK
"${PODS_ROOT}/FirebaseCrashlytics/upload-symbols" \
  -gsp iosApp/GoogleService-Info.plist -p ios build/iosApp.xcarchive/dSYMs

# Sentry
sentry-cli debug-files upload --org <org> --project <proj> build/iosApp.xcarchive/dSYMs
```

If `:shared` is a **dynamic** framework, its dSYM lives inside the xcarchive too and gets uploaded by the same call — no extra step. For a static framework the symbols are inlined into the app binary's dSYM, also covered automatically.

## Pre-release checklist

Combined across both platforms. Bail on the first failure:

1. **Android `versionCode` strictly greater** than the last shipped code on every Play track (`internal`, `closed`, `production`).
2. **iOS `CFBundleVersion` strictly greater** than the last shipped TestFlight build for the same `MARKETING_VERSION`.
3. **Marketing version matches** between `libs.versions.toml` → `:androidApp` `versionName` → iOS `Version.xcconfig` `MARKETING_VERSION` (unless deliberately diverged).
4. **XCFramework rebuilt** against the just-resolved `:shared` version — stale frameworks are the #1 cause of "works locally, crashes in TestFlight."
5. **Changelog files in place:** `fastlane/metadata/android/<locale>/changelogs/<versionCode>.txt` for every Android locale, `fastlane/metadata/<locale>/release_notes.txt` for every iOS locale.
6. **Both signing identities present:** `keystore.properties` decoded on CI for Android; fastlane match certs synced for iOS.
7. **Crashlytics mapping uploaded** (Android, Firebase projects only); **dSYMs uploaded** (iOS).

## Pre-release command sequence

Run in this order; bail on first failure:

```bash
./gradlew :shared:check
./gradlew :androidApp:lintRelease :androidApp:testReleaseUnitTest :androidApp:bundleRelease
xcodebuild test \
  -workspace iosApp/iosApp.xcworkspace \
  -scheme iosApp \
  -destination 'platform=iOS Simulator,name=iPhone 15'
xcodebuild archive \
  -workspace iosApp/iosApp.xcworkspace \
  -scheme iosApp \
  -configuration Release \
  -archivePath build/iosApp.xcarchive
```

`bundleRelease` runs the per-variant R8 + signing pipeline, so adding `:androidApp:assembleRelease` to the same line roughly doubles the time for no extra coverage. Run `assembleRelease` separately only when you need an `.apk` for internal QA. `xcodebuild test` before `xcodebuild archive` because a green archive of failing code is worse than a slow build.

## What the release engineer doesn't do

- **No feature changes.** A bug that blocks the release gets filed and handed back to `kmm-engineer` or `kmm-architect`.
- **No `expect/actual` platform-impl edits** at release time — those are shared-module surgery and need their own review cycle.
- **No ProGuard / R8 rule edits** that weren't requested by a crash or build failure. New rules go through `kmm-build-expert`.
- **No commits of signing material.** Keystores, `keystore.properties`, decoded base64 secrets, provisioning profiles, `.p12` certs — none of these touch the repo.

## Hard nos

- No `versionCode` reuse across Android tracks. Play Console rejects it; nor does this skill.
- No `CFBundleVersion` reuse for the same `MARKETING_VERSION` on iOS. TestFlight rejects it.
- No shipping iOS without the just-rebuilt `:shared` framework — every `xcodebuild archive` must follow a `:shared` rebuild in the same session.
- No `applicationIdSuffix` / `PRODUCT_BUNDLE_IDENTIFIER` change between releases of the same shipped app — both stores treat it as a different app and reset ratings/reviews.
- No `fastlane supply --skip-upload-changelogs` or `fastlane pilot --skip_waiting_for_build_processing` to "ship faster" — the changelog and the processed build are part of the release record.
