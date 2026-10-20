---
name: capacitor-release-readiness
description: Use when preparing a CapacitorJS app for App Store or Play Store submission including icon and splash screen generation, signing configuration, version management, store metadata, and go or no-go release evidence.
---

# Capacitor Release Readiness

## Specialization

Produce a release-ready CapacitorJS native build for iOS App Store and Google Play Store submission with deterministic signing, asset, versioning, and evidence gates — and an explicit go or no-go recommendation.

## Scope Boundaries

In scope:

- App icon and splash screen asset generation and Xcode / Android Studio integration.
- iOS signing: provisioning profiles, certificates, and `ExportOptions.plist`.
- Android signing: keystore configuration and `build.gradle` signing block.
- Version and build number management strategy.
- Store metadata readiness: screenshots, descriptions, and privacy policy requirements.
- Smoke test evidence and release checklist completion.
- Rollback plan documentation.

Out of scope:

- App Store Connect or Google Play Console account management.
- App Review process navigation.
- Backend infrastructure for production deployment.
- Marketing or ASO (App Store Optimization) strategy.

## Trigger Conditions

- A Capacitor app is ready for its first App Store or Play Store submission.
- A new version is being promoted to production and needs release evidence.
- Signing or asset configuration is failing in a CI/CD pipeline.
- A release checklist must be completed before promoting to production.

## Inputs

- App name, `appId`, current version, and build number.
- Target stores: iOS App Store, Google Play Store, or both.
- Signing credentials availability (certificates, provisioning profiles, keystore).
- CI/CD environment in use.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- App icon and splash screen asset set validation.
- Signing configuration verification for each target platform.
- Version and build number management plan.
- Store metadata readiness checklist with gaps.
- Smoke test evidence summary.
- Go or no-go recommendation with explicit residual risks.
- Rollback procedure documented and owner-assigned.

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand release requirements | All required assets and signing types identified |
| L2 First Release | Ship first App Store or Play Store build | Signing, assets, and metadata are complete |
| L3 CI/CD Release | Automate release pipeline | Signing and archive steps run reproducibly in CI |
| L4 Expert Governance | Release governance standard | Evidence, rollback, and approval chain are documented per release |

## App Icon and Splash Screen

### Icon Requirements (minimum)
| Platform | Sizes Required |
|---|---|
| iOS | 1024×1024 (App Store), 20–180px set via Xcode asset catalog |
| Android | 48–192px mdpi–xxxhdpi adaptive icon layers |

Use `@capacitor/assets` for automated generation from a single source image:
```bash
npx @capacitor/assets generate --ios --android
# Requires: resources/icon.png (1024×1024, no alpha) and resources/splash.png (2732×2732)
```

- iOS icons must not contain transparency (alpha channel); App Store will reject.
- Android adaptive icons require foreground and background layers; use `icon-foreground.png` and `icon-background.png`.

### Splash Screen
- Configure `@capacitor/splash-screen` in `capacitor.config.ts` with `launchShowDuration` and `backgroundColor`.
- Splash screen must not contain text; use logo only to avoid localization issues in review.

## iOS Signing Configuration

```bash
# Manual signing validation
xcodebuild -workspace ios/App/App.xcworkspace \
  -scheme App \
  -configuration Release \
  -archivePath ./App.xcarchive \
  archive \
  CODE_SIGN_IDENTITY="Apple Distribution" \
  PROVISIONING_PROFILE_SPECIFIER="<profile-name>"
```

- Use Automatic Signing in Xcode for development only; switch to Manual Signing for CI builds.
- Store provisioning profiles and certificates in a secrets manager or Fastlane Match; never commit to source control.
- `ExportOptions.plist` must specify `method: app-store` for App Store builds.

## Android Signing Configuration

```groovy
// android/app/build.gradle
android {
    signingConfigs {
        release {
            storeFile file(System.getenv("ANDROID_KEYSTORE_PATH"))
            storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
            keyAlias System.getenv("ANDROID_KEY_ALIAS")
            keyPassword System.getenv("ANDROID_KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

- Keystore credentials must be environment variables only; never hardcoded.
- Use Android App Bundle (`.aab`) for Play Store submission; APK is only for direct distribution.
- Enable ProGuard/R8 for release builds; test that ProGuard rules do not break Capacitor bridge classes.

## Version Management

```typescript
// capacitor.config.ts — version is metadata only; source of truth is native project
// iOS: CFBundleShortVersionString (version) and CFBundleVersion (build)
// Android: versionName and versionCode in build.gradle
```

- `versionCode` (Android) and `CFBundleVersion` (iOS) must increment monotonically; never reuse a build number.
- Use a single version source (e.g., `package.json` `version`) and propagate to native projects in CI.
- Semantic versioning: `major.minor.patch`; do not use pre-release suffixes in store builds.

## Store Metadata Checklist

### iOS App Store
- [ ] App name and subtitle match approved metadata.
- [ ] Screenshots at required sizes for each supported device family.
- [ ] Privacy policy URL is live and accessible.
- [ ] App Privacy nutrition labels are complete.
- [ ] Age rating questionnaire is completed.
- [ ] In-app purchase metadata is configured if applicable.

### Google Play Store
- [ ] Short description (80 chars) and full description (4000 chars) are complete.
- [ ] Screenshots for phone, 7-inch tablet, and 10-inch tablet.
- [ ] Feature graphic (1024×500) is provided.
- [ ] Content rating questionnaire is completed.
- [ ] Data safety section is complete.
- [ ] Privacy policy URL is live and accessible.

## Release Quality Gate

| Check | Requirement | Evidence |
|---|---|---|
| App icons | Present, correct sizes, no alpha (iOS) | Asset catalog validation |
| Splash screen | Configured, no text | Visual review |
| iOS signing | Manual signing, valid profile, correct method | Archive log |
| Android signing | Env-var keystore, AAB output | Build log |
| Build number | Incremented vs. last release | Version history |
| Store metadata | Checklist complete | Metadata review |
| Smoke tests | Core flows pass on physical device | Test evidence artifact |
| Security gate | CSP, secure storage, permissions audited | Security review sign-off |
| Rollback plan | Documented, executable, owner-assigned | Rollback artifact |

## Rollback Procedure Template

1. **Trigger**: Define what constitutes a rollback trigger (crash rate, critical defect report).
2. **Owner**: Name the release engineer responsible for executing rollback.
3. **iOS Steps**: Submit previous version via App Store Connect phased release controls; request expedited review if needed.
4. **Android Steps**: Use Google Play Console to halt rollout; promote previous release to 100%.
5. **Communication**: Notify stakeholders within 30 minutes of rollback trigger.
6. **Post-Mortem**: Schedule within 48 hours; record root cause and prevention action.

## Done Criteria

- All release quality gate checks pass or have explicit accepted exceptions with owner sign-off.
- App icons and splash screen assets are generated and validated.
- Signing is configured via environment variables in CI; no credentials in source control.
- Store metadata checklists are complete for each target store.
- Smoke test evidence is documented.
- Rollback procedure is documented, reviewed, and owner is named.
- Go or no-go recommendation is issued with residual risks listed.
