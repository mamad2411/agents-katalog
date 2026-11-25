---
name: capacitor-privacy-compliance
description: Use when a CapacitorJS app must satisfy Apple Privacy Manifest requirements, App Tracking Transparency prompts, Android Play Store data safety declarations, or GDPR/CCPA consent flows — covering authoring, SDK disclosure, and submission-readiness verification.
---

# Capacitor Privacy Compliance

## Specialization

Implement and verify privacy compliance artifacts required for App Store and Play Store submission of CapacitorJS applications. Covers the full surface: iOS `PrivacyInfo.xcprivacy` authoring and required-reason API declarations, third-party SDK privacy disclosures, App Tracking Transparency (ATT) prompt design and timing, Android Play Store data safety form completion, and GDPR/CCPA in-app consent flow patterns at the Capacitor layer.

## Scope Boundaries

In scope:

- iOS `PrivacyInfo.xcprivacy` — authoring, required-reason API categories, and SDK aggregation.
- Apple required-reason APIs: file timestamps (`NSPrivacyAccessedAPICategoryFileTimestamp`), user defaults (`NSPrivacyAccessedAPICategoryUserDefaults`), system boot time, disk space, and active keyboard APIs.
- Third-party SDK privacy manifest aggregation — identifying which Capacitor plugins and native dependencies require their own `PrivacyInfo.xcprivacy`.
- App Tracking Transparency (ATT): `NSUserTrackingUsageDescription`, ATT prompt timing strategy, denial handling, and SKAdNetwork configuration.
- Android Play Store data safety form — mapping app data collection to form categories, retention periods, and sharing disclosures.
- GDPR/CCPA consent UI patterns at the Capacitor layer: consent capture, storage, and propagation to analytics/ad SDKs.
- Privacy audit: detecting undisclosed API usage and third-party SDKs missing privacy manifests.

Out of scope:

- Full legal compliance review (GDPR DPA, CCPA CPRA regulatory interpretation — requires legal counsel).
- App Store review appeal processes.
- General security hardening (`capacitor-security`).
- Analytics SDK integration depth (`capacitor-observability`).
- Full release submission workflow (`capacitor-release-readiness`).

## Trigger Conditions

- App Store submission was rejected due to missing or incomplete `PrivacyInfo.xcprivacy`.
- Xcode build produces a "missing privacy manifest" warning for a Capacitor plugin or dependency.
- The app uses ATT-gated advertising or cross-app tracking and has no ATT prompt implementation.
- Play Store data safety form is incomplete or does not reflect actual data collection.
- A privacy audit or legal review identified undisclosed data collection.
- A new Capacitor plugin is being added and its privacy implications are unknown.
- GDPR/CCPA consent capture is missing or not propagating correctly to SDKs.

## Inputs

- Xcode project output: list of `PrivacyInfo.xcprivacy` warnings from build log.
- Full list of Capacitor plugins in use (from `package.json`).
- List of native third-party SDKs (CocoaPods, Swift Package Manager, Gradle dependencies).
- Whether the app uses advertising identifiers (IDFA) or cross-app tracking.
- Target markets and applicable regulations (EU → GDPR, California → CCPA/CPRA, etc.).
- Analytics, crash reporting, and ad SDKs in use.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- `PrivacyInfo.xcprivacy` file with all required-reason API categories and SDK privacy disclosures.
- SDK privacy manifest gap report: plugins/SDKs that need their own manifests but are missing them.
- ATT implementation (if cross-app tracking is used): usage description string, prompt timing strategy, and denial handler.
- Android data safety form completion guide mapped to actual app data collection.
- GDPR/CCPA consent capture pattern (if regulated markets are targeted).
- Privacy audit findings: undisclosed API usage, missing SDK manifests, ATT gaps.
- Rejected-candidate table with deterministic reason codes.
- Closure check: build produces no privacy manifest warnings; submission checklist passes.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Identify applicable privacy requirements and gap surface | Requirements list and gap inventory documented |
| L2 Delivery | Author `PrivacyInfo.xcprivacy`; complete Android data safety form; implement ATT prompt if required | Build produces no privacy manifest warnings; form is complete |
| L3 Hardening | Add SDK gap remediation, consent flow, GDPR/CCPA propagation, and pre-submission audit | Privacy audit findings are zero or risk-accepted; submission checklist passes |
| L4 Expert Standardization | Reusable privacy compliance model for multi-app compendium use | Templates, SDK inventory, and audit runbook documented |

## Deterministic Workflow

1. Run an Xcode archive build and capture all `PrivacyInfo.xcprivacy`-related warnings.
2. Enumerate all Capacitor plugins from `package.json` and all native SDKs from `Podfile.lock` and `build.gradle` dependency tree.
3. For each plugin and SDK, determine: (a) does it use a required-reason API category? (b) does it ship its own `PrivacyInfo.xcprivacy`? If not, it must be declared in the app-level manifest.
4. Author or update `ios/App/App/PrivacyInfo.xcprivacy` with all required-reason API entries and collected-data types for first-party collection.
5. Determine whether the app uses IDFA or cross-app tracking. If yes, implement ATT: add `NSUserTrackingUsageDescription` to `Info.plist`, request permission at the correct lifecycle point, handle granted/denied states.
6. Complete the Android Play Store data safety form: map each collected data type to form categories, set sharing and retention disclosures, and save the form.
7. If GDPR/CCPA is applicable, implement consent capture: show consent UI before any analytics/ad SDK initializes; store consent decision; propagate to SDKs on each app launch.
8. Run a privacy audit pass: confirm no required-reason API is used without disclosure; confirm all third-party SDKs have manifests; confirm ATT is implemented if tracking is present.
9. Re-run Xcode archive — zero privacy manifest warnings is the gate.
10. Document SDK inventory with privacy manifest status, data collection categories, and owner.

## PrivacyInfo.xcprivacy Pattern

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <!-- Required-reason API declarations -->
  <key>NSPrivacyAccessedAPITypes</key>
  <array>
    <!-- File timestamp APIs — used by @capacitor/filesystem -->
    <dict>
      <key>NSPrivacyAccessedAPIType</key>
      <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
      <key>NSPrivacyAccessedAPITypeReasons</key>
      <array>
        <string>C617.1</string> <!-- display to user or provide to user on request -->
      </array>
    </dict>
    <!-- User defaults — used by @capacitor/preferences -->
    <dict>
      <key>NSPrivacyAccessedAPIType</key>
      <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
      <key>NSPrivacyAccessedAPITypeReasons</key>
      <array>
        <string>CA92.1</string> <!-- access own app's user defaults only -->
      </array>
    </dict>
  </array>

  <!-- First-party data collection -->
  <key>NSPrivacyCollectedDataTypes</key>
  <array>
    <dict>
      <key>NSPrivacyCollectedDataType</key>
      <string>NSPrivacyCollectedDataTypeCrashData</string>
      <key>NSPrivacyCollectedDataTypeLinked</key>
      <false/>
      <key>NSPrivacyCollectedDataTypeTracking</key>
      <false/>
      <key>NSPrivacyCollectedDataTypePurposes</key>
      <array>
        <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
      </array>
    </dict>
  </array>

  <!-- Set to true only if app uses IDFA or cross-app tracking -->
  <key>NSPrivacyTracking</key>
  <false/>
  <key>NSPrivacyTrackingDomains</key>
  <array/>
</dict>
</plist>
```

## ATT Implementation Pattern

```typescript
// Only implement if NSPrivacyTracking is true in PrivacyInfo.xcprivacy
// Use a community plugin or native bridge for ATT on Capacitor

import { Capacitor } from '@capacitor/core';

async function requestTrackingPermission(): Promise<void> {
  if (Capacitor.getPlatform() !== 'ios') return;

  // Soft-ask first: explain why tracking benefits the user
  const userWantsToProceed = await showTrackingRationale();
  if (!userWantsToProceed) return;

  // Request ATT permission (requires plugin: capacitor-ios-app-tracking or equivalent)
  const { status } = await AppTrackingTransparency.requestPermission();

  if (status === 'authorized') {
    // Initialize ad/analytics SDKs that require IDFA
    initializeAdSDKs();
  } else {
    // Use limited ad targeting or contextual ads only
    initializeLimitedAdSDKs();
  }
}

// Call after first meaningful interaction — NOT on cold launch
// Apple guidance: do not request ATT on first app open; wait for onboarding completion
```

## GDPR/CCPA Consent Pattern

```typescript
// capacitor/privacy-consent.ts
import { Preferences } from '@capacitor/preferences';

const CONSENT_KEY = 'privacy_consent_v1';

export interface ConsentDecision {
  analytics: boolean;
  advertising: boolean;
  timestamp: string;
}

export async function getStoredConsent(): Promise<ConsentDecision | null> {
  const { value } = await Preferences.get({ key: CONSENT_KEY });
  return value ? JSON.parse(value) : null;
}

export async function storeConsent(decision: ConsentDecision): Promise<void> {
  await Preferences.set({ key: CONSENT_KEY, value: JSON.stringify(decision) });
}

export async function initializeSDKsWithConsent(): Promise<void> {
  const consent = await getStoredConsent();
  if (!consent) {
    // Show consent UI — do not initialize any tracking SDK until consent is captured
    return;
  }
  if (consent.analytics) initializeAnalytics();
  if (consent.advertising) initializeAdSDKs();
}
```

## SDK Privacy Manifest Audit Checklist

Common Capacitor plugins with required-reason API usage:

| Plugin | Required-reason API | Ships own manifest (as of 2025)? |
|---|---|---|
| `@capacitor/filesystem` | `NSPrivacyAccessedAPICategoryFileTimestamp` | Yes — verify version |
| `@capacitor/preferences` | `NSPrivacyAccessedAPICategoryUserDefaults` | Yes — verify version |
| `@capacitor/device` | `NSPrivacyAccessedAPICategoryDiskSpace`, boot time | Yes — verify version |
| `@capacitor/push-notifications` | None directly — verify Firebase SDK | Firebase SDK ships manifest |
| `@capacitor/camera` | None directly | Yes — verify version |
| Custom plugins | Audit native code for `NSFileModificationDate`, `UserDefaults`, `systemUptime` | Must be declared in app manifest |

**Rule:** If a plugin does not ship its own `PrivacyInfo.xcprivacy`, all required-reason APIs it accesses must be declared in the app-level manifest.

## Quality Gates

- Xcode archive build produces zero `PrivacyInfo.xcprivacy` warnings.
- Every required-reason API used by the app and its dependencies is declared with a valid reason code.
- `NSPrivacyTracking` is `true` only if the app uses IDFA or cross-app tracking identifiers.
- ATT prompt is implemented if `NSPrivacyTracking` is `true`; prompt timing follows Apple guidance (not on cold launch).
- Android data safety form is complete; all collected data types, sharing disclosures, and retention periods are accurate.
- No analytics or ad SDK initializes before consent is captured in GDPR/CCPA-applicable markets.
- SDK inventory exists with privacy manifest status for every native dependency.

## Done Criteria

- `PrivacyInfo.xcprivacy` is authored and committed; Xcode build is clean.
- All third-party SDK privacy manifest gaps are resolved or risk-accepted with owner.
- ATT implementation is in place if cross-app tracking is used.
- Android data safety form is complete and saved in Play Console.
- GDPR/CCPA consent flow captures, stores, and propagates consent before SDK initialization (if applicable).
- SDK privacy inventory is documented with manifest status, data categories, and owner.
- Pre-submission privacy checklist passes with zero open blockers.
