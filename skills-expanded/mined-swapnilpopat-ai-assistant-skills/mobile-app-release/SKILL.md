---
name: mobile-app-release
description: Release engineering for mobile apps on the App Store, Google Play, and alternative stores. Use when configuring code signing, setting up CI/CD for mobile, managing TestFlight/Play tracks, planning staged rollouts, privacy disclosures, OTA updates, and store review readiness.
source: self
---

# Mobile App Release

End-to-end release engineering for mobile apps. Covers Apple App Store, Google Play, Huawei AppGallery, Amazon Appstore, and side-loading channels (enterprise, ad-hoc, internal distribution).

## When to Use

- Setting up first-time publishing for a new mobile app
- Building or hardening a mobile CI/CD pipeline (signing, build, upload, release)
- Planning a staged rollout, phased release, or release health monitoring
- Preparing privacy disclosures, age ratings, or export compliance
- Recovering from store rejections or removed listings

## Versioning

- Follow `MAJOR.MINOR.PATCH` semantic versioning for the public marketing version.
- Use a strictly monotonic build number derived from CI build ID or git commit count — never reset it.
- Tag every release in git (`v1.4.0+1234`) and attach build artifacts and dSYMs/mapping files.
- Maintain a single source of truth for version (e.g., `version.properties` or fastlane `app_store_build_number`).

## Code Signing

### iOS

- Use **App Store Connect API keys** for CI signing — never commit `.p12`, `.mobileprovision`, or session cookies.
- Manage profiles with **Fastlane Match** (encrypted git repo) or Xcode Cloud automatic signing.
- Enable **App Store Signing** (Xcode "Automatically manage signing" only for local dev; CI uses match/manual).
- Use distribution certs scoped per-team; rotate when engineers leave.
- Notarize macOS companion builds; Hardened Runtime on by default.

### Android

- Use **Play App Signing**: Google holds the app signing key, you keep the upload key.
- Store the upload keystore in a secret manager (GitHub Actions Secrets, Vault, GCP Secret Manager).
- Sign with **APK Signature Scheme v2/v3/v4**; v1-only signing is not accepted on modern Android.
- For internal/enterprise distribution, sign with a separate keystore from the Play upload key.

## CI/CD

- Build on hosted runners with the correct Xcode/Android SDK versions pinned (matrix-tested if you support multiple).
- Cache: Gradle (`~/.gradle/caches`, `~/.gradle/wrapper`), CocoaPods (`Pods/`, `~/Library/Caches/CocoaPods`), SPM (`~/Library/Developer/Xcode/DerivedData/SourcePackages`), Flutter SDK + pub cache, npm/yarn/pnpm.
- Pipeline stages: lint → unit tests → build (debug + release) → instrumented/UI tests → sign → upload → release notes → notify.
- Use Fastlane (lanes per platform) or platform-native tooling (Xcode Cloud, Gradle Play Publisher).
- Generate and upload **dSYMs (iOS)** and **mapping.txt + native debug symbols (Android)** to your crash reporter on every release build.
- Make the pipeline **idempotent** — re-running a release tag must not produce a different artifact hash.

## Distribution Tracks

### Apple

- **TestFlight Internal:** for the team (up to 100 testers, no review).
- **TestFlight External:** beta testers, lightweight Beta App Review.
- **Phased Release:** 7-day automated rollout to App Store users; can pause but not roll back.
- **Expedited Review:** request only for critical fixes; abuse triggers slower future reviews.

### Google Play

- **Internal testing:** instant, up to 100 testers.
- **Closed testing:** alpha groups, list- or email-managed.
- **Open testing:** public beta, opt-in.
- **Production with staged rollout:** start at 1-5%, increase as health metrics stay green.
- **Halt rollout** immediately on regressions; resume after a fix.

### Other Stores

- **Huawei AppGallery:** required for HMS-only devices in some markets; submit alongside Play.
- **Amazon Appstore:** for Fire tablets / Fire TV; uses APK or AAB.
- **Samsung Galaxy Store:** optional, useful for Samsung-specific features.
- **Enterprise / MDM:** Apple Business Manager, Android Enterprise (Managed Google Play), Intune, Jamf.

## Release Notes & Metadata

- Maintain a structured changelog (Keep a Changelog format) and derive store release notes from it.
- Localize release notes for every supported store locale.
- Keep screenshots, preview videos, and store descriptions in version control (use Fastlane `deliver`/`supply`).
- Update what's-new copy to be user-facing, not engineering-facing.

## Privacy, Compliance, and Disclosures

- **Apple:**
  - Maintain `PrivacyInfo.xcprivacy` with required-reason API declarations and tracking domains.
  - Fill out App Privacy details (data collection, linking, tracking) accurately and consistently.
  - Declare export compliance for crypto usage (`ITSAppUsesNonExemptEncryption`).
- **Google:**
  - Complete the **Data Safety form**; align with the actual SDK behavior (audit third-party SDKs).
  - Declare sensitive permissions (location, SMS, accessibility services) with justification.
  - Provide an accurate target audience and content rating (IARC questionnaire).
- **Both:** publish a privacy policy URL; ensure it covers every region you ship to (GDPR, CCPA, LGPD, PIPL).
- **GDPR/CCPA:** implement consent flow before initializing analytics/ads SDKs in opt-in regions.

## Staged Rollouts & Release Health

- Define release-health SLOs before rollout: crash-free users ≥ 99.5%, ANR rate < 0.47%, key-flow success ≥ 99%.
- Start at 1-5% for at least 24 hours; double daily if metrics hold.
- Monitor: crashes, ANRs/hangs, install/uninstall rate, store rating delta, key conversion metrics, latency.
- Have a documented rollback procedure: halt rollout, prepare hotfix, push expedited.
- Use feature flags so a bad feature can be disabled without a new release.

## OTA Updates (where supported)

- React Native / Flutter: use **EAS Update**, **CodePush** (in maintenance), or **Shorebird**.
- **Never** push native code or change app behavior in ways the stores prohibit (Apple Guideline 4.5.4 / Google's policy).
- Sign and verify update bundles; pin a public key in the binary.
- Stage OTA updates by version range and rollout percentage; monitor crash deltas tied to the bundle ID.

## App Store Review Readiness

- **Common rejection reasons:** broken sign-in (no demo account), missing privacy policy, IAP for digital goods sold via web, intrusive permissions without rationale, design that mimics system UI.
- Provide a working demo account and clear test instructions in App Store Connect's review notes.
- Avoid placeholder content, lorem ipsum, or "coming soon" screens in submitted builds.
- Test on the lowest supported OS and on iPad if `UIRequiredDeviceCapabilities` allows it.
- For subscriptions, comply with auto-renewable subscription disclosure rules verbatim.

## Crash & Performance Reporting

- Wire up Crashlytics, Sentry, Bugsnag, or Embrace on day one; configure release identifier (version + build).
- Symbolicate automatically by uploading dSYMs / mapping files in CI.
- Tag crashes with rollout cohort (staged rollout %, OTA bundle ID) for fast triage.
- Set alert thresholds tied to release health SLOs; page on regression, not on absolute count.

## Anti-Patterns

- Committing keystores, `.p12` files, or provisioning profiles to git
- Manual builds from a developer laptop for production releases
- Missing or stale dSYM/mapping uploads — unsymbolicated crashes are useless
- Skipping staged rollout to "ship faster" — bugs reach 100% of users before metrics catch up
- Filling Data Safety / App Privacy forms inaccurately — Google and Apple do audit
- Pushing OTA updates that change native behavior or violate store policy
- Ignoring ANR / hang metrics and tracking only crashes
- Letting upload keys live in a single engineer's local keychain

## Release Checklist

- [ ] Version + build number bumped, tagged in git, changelog updated
- [ ] Release build is signed via CI with secrets from a vault (no local signing)
- [ ] dSYMs / mapping files / native symbols uploaded to crash reporter
- [ ] Privacy manifest (iOS) and Data Safety form (Android) match the actual SDKs in the build
- [ ] Release notes localized for every supported store locale
- [ ] Demo account and review notes provided in App Store Connect
- [ ] Staged rollout plan documented with halt/rollback criteria
- [ ] Release health dashboards and alerts configured for the new version
- [ ] Feature flags allow disabling risky features without a new release
