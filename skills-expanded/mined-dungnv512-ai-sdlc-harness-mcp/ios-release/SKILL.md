---
name: ios-release
description: iOS App Store release checklist for Flutter apps — Info.plist keys, entitlements, PrivacyInfo.xcprivacy, App Tracking Transparency, universal links, TestFlight, fastlane match/pilot/deliver. MANDATORY TRIGGERS - "ios release", "app store", "info.plist", "entitlements", "privacy manifest", "xcprivacy", "ats", "app transport security", "app store connect", "testflight", "fastlane ios", "universal links", "apple-app-site-association".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: ios-release

## When to use

Any task that touches the iOS distribution pipeline: adding a new native
permission, preparing a release build for App Store review, updating the
`PrivacyInfo.xcprivacy` manifest, wiring universal links, or running a
TestFlight cycle.

> This skill covers *configuration guidance only*. Actual signing config in
> `ios/Runner.xcodeproj`, Fastfile lane changes, and provisioning profile
> updates require a human release-engineer ticket — treat these as
> off-limits for automated changes in your project's equivalent of
> CLAUDE.md §9.

---

## Inputs

- Feature slug or release tag (e.g. `v1.4.0`)
- List of new native permissions the feature requires
- Domain(s) for universal links (placeholder used below: `example.com`)
- Target store tracks (`testflight-internal` / `testflight-external` / `production`)

---

## Steps

### 1. Verify Info.plist required keys

Open `ios/Runner/Info.plist`. Confirm every key used by the app is present
with a properly localized usage string for each locale you ship:

| Key | When required |
|-----|---------------|
| `NSCameraUsageDescription` | Camera access (identity verification, avatar capture) |
| `NSPhotoLibraryUsageDescription` | Photo library read (post images, avatar) |
| `NSPhotoLibraryAddUsageDescription` | Save-to-library (post images) |
| `NSFaceIDUsageDescription` | Face ID biometric step-up (`local_auth`) |
| `NSUserTrackingUsageDescription` | ATT prompt (analytics opt-in, consent-gated) |

Usage strings are localized via `.lproj` files for App Store review.
Maintain one `.lproj/InfoPlist.strings` file per locale you support (e.g.
`ios/Runner/en.lproj/InfoPlist.strings`).

Do not add `NSLocationWhenInUseUsageDescription` speculatively — only add
it when a feature explicitly requires location.

`UIBackgroundModes` must include `remote-notification` for silent push; do
not add `fetch` without explicit product approval.

### 2. Check App Transport Security (ATS)

The app must **not** contain `NSAllowsArbitraryLoads: true` in any flavor
including dev.

```xml
<key>NSAppTransportSecurity</key>
<dict>
  <!-- No NSAllowsArbitraryLoads. Domain exceptions only when justified. -->
</dict>
```

If a domain exception is genuinely needed, add `NSExceptionDomains` with
`NSExceptionAllowsInsecureHTTPLoads: false` and
`NSExceptionRequiresForwardSecrecy: true`. Log the exception as a security
note in the PR body referencing your project's security checklist.

### 3. Update PrivacyInfo.xcprivacy

Apple requires a `PrivacyInfo.xcprivacy` manifest for required-reason API
usage (mandatory since May 2024). File location:
`ios/Runner/PrivacyInfo.xcprivacy`

See template at `.claude/skills/ios-release/templates/PrivacyInfo.xcprivacy.example`.

Required fields:

- `NSPrivacyTracking`: `false` unless ATT authorized.
- `NSPrivacyTrackingDomains`: tracking domains list (empty when analytics
  is off by default pending user consent).
- `NSPrivacyCollectedDataTypes`: array mapping every data point in your
  project's data/sub-processor register to an Apple data-type identifier.
- `NSPrivacyAccessedAPITypes`: at minimum include:
  - `NSPrivacyAccessedAPICategoryFileTimestamp` → reason `C617.1`
  - `NSPrivacyAccessedAPICategorySystemBootTime` → reason `35F9.1`
  - `NSPrivacyAccessedAPICategoryDiskSpace` → reason `E174.1`
  - `NSPrivacyAccessedAPICategoryUserDefaults` → reason `CA92.1`

Reference: [Privacy Manifest Files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)

### 4. Entitlements

File: `ios/Runner/Runner.entitlements`

| Entitlement | Required for |
|-------------|-------------|
| `com.apple.developer.associated-domains` | Universal links (`applinks:example.com`) |
| `aps-environment` | Push notifications (`production` in prod, `development` in dev) |
| `com.apple.developer.devicecheck.appattest-environment` | App Attest (`production`) |

Do not add unused entitlements — App Store review rejects apps with
entitlements not backed by capability toggles in the Apple Developer portal.

### 5. App Tracking Transparency (ATT)

ATT must be requested *after* the user opts into analytics on your app's
privacy/consent screen. Never show ATT at cold start.

Flow:
1. User toggles analytics on the privacy settings screen.
2. `ConsentService.grantAnalytics()` calls
   `AppTrackingTransparency.requestTrackingAuthorization()`.
3. Only on `authorized` does PostHog or Firebase Analytics activate.

Violating this order breaches
[App Store Review Guidelines §5.1.2](https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing).

### 6. App Privacy Nutrition Labels

Update in App Store Connect before each submission:

| Data type | Purpose | Linked to identity? | Tracking? |
|-----------|---------|---------------------|-----------|
| Name | Account creation | Yes | No |
| Email address | Account, communications | Yes | No |
| Phone number | OTP verification | Yes | No |
| User content (posts, items) | App functionality | Yes | No |
| Crash data | App analytics (opt-in) | No | No |
| Product analytics | App analytics (opt-in) | No | No |
| Device ID | Security / fraud prevention | No | No |

Reference: [App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/)

### 7. Universal Links

AASA must be served at
`https://example.com/.well-known/apple-app-site-association` without
redirect, content-type `application/json`.

Template: `.claude/skills/deep-linking/templates/apple-app-site-association.json.example`

Entitlement:
```xml
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:example.com</string>
</array>
```

Verify:
```bash
xcrun simctl openurl booted "https://example.com/p/test-post-id"
```

Reference: [Universal Links](https://developer.apple.com/ios/universal-links/)

### 8. Screenshot specifications

| Required size | Device reference |
|---------------|-----------------|
| 6.7" (1290×2796) | iPhone 15 Pro Max |
| 6.5" (1242×2688) | iPhone 11 Pro Max |
| 5.5" (1242×2208) | iPhone 8 Plus |

Screenshots must show actual app content. Do not use wireframes or
placeholder data.

### 9. fastlane lanes (release-engineer territory)

Do **not** modify `Fastfile` or provisioning profiles without a human
ticket. Expected lanes (see template `Fastfile.ios.example`):

| Lane | Purpose |
|------|---------|
| `ios match_dev` | Sync dev certs via `match` (development) |
| `ios match_appstore` | Sync App Store distribution certs |
| `ios testflight` | Build + upload to TestFlight internal |
| `ios testflight_external` | Promote to external beta group |
| `ios app_store_prod` | Submit for review + phased rollout |

Use App Store Connect API key (`.p8`) stored as `APPSTORE_CONNECT_API_KEY`
CI secret — never username/password (2FA breaks CI).

Reference: [fastlane docs](https://docs.fastlane.tools/)

### 10. App Store Review hot-spots (common causes of rejection)

| Guideline | Concern |
|-----------|---------|
| §1.6 Personal Attacks | User content moderation pipeline must be live |
| §2.5.1 Software Requirements | No undocumented private API calls |
| §4.7 / 4.7.5 HTML5 + downloaded code | No code-push / Shorebird runtime |
| §5.1 Privacy | Consent screen required before tracking; ATT via Apple's API only |
| §5.1.1 Data Collection | Sensitive/identity data retained per your project's documented retention rules only |

---

## Output

- `ios/Runner/Info.plist` updated (permission keys + localized strings)
- `ios/Runner/PrivacyInfo.xcprivacy` updated
- `ios/Runner/Runner.entitlements` verified
- PR note confirming App Privacy nutrition labels updated in App Store Connect

---

## Anti-patterns

- `NSAllowsArbitraryLoads: true` in any flavor — blocked by CI Semgrep rule.
- Requesting ATT at cold start before user consent — violates §5.1.2.
- Entitlements not backed by Apple Developer portal capability toggles.
- Embedding `.p8` API key in repo — must be a CI secret.
- `NSPrivacyTracking: true` with an empty tracking-domains array — binary
  will be rejected at App Store validation.

---

## See also

- `.claude/skills/deep-linking/SKILL.md` — AASA setup
- `.claude/skills/mobile-security/SKILL.md` — App Attest, cert pinning
- `.claude/skills/push-notifications/SKILL.md` — APNs entitlement
- your project's privacy/consent documentation — consent screen, data mapping
- your project's deployment doc — Mobile distribution
