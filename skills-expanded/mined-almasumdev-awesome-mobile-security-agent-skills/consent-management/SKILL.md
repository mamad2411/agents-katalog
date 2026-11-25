---
name: consent-management
description: Platform consent frameworks on mobile — iOS App Tracking Transparency (ATT) and Android User Messaging Platform (UMP) for GDPR / CCPA. Use when integrating analytics, ads, or any cross-app tracking.
---

# Consent Management on Mobile

## Instructions

Consent on mobile has two dimensions: **platform policy** (App Store / Play rules) and **regulatory** (GDPR, CCPA, LGPD, PIPL). Both must pass.

### 1. iOS: App Tracking Transparency (ATT)

Required before you access the IDFA or perform cross-app/website tracking. The user sees a system prompt; only `.authorized` permits tracking.

```swift
import AppTrackingTransparency
import AdSupport

if #available(iOS 14.5, *) {
    ATTrackingManager.requestTrackingAuthorization { status in
        switch status {
        case .authorized:
            let idfa = ASIdentifierManager.shared().advertisingIdentifier
            AnalyticsSDK.enableTracking(idfa: idfa)
        case .denied, .restricted, .notDetermined:
            AnalyticsSDK.disableTracking()
        @unknown default: AnalyticsSDK.disableTracking()
        }
    }
}
```

Add a matching purpose string:

```xml
<key>NSUserTrackingUsageDescription</key>
<string>We use this to personalize ads you see in this app.</string>
```

Rules:
- Ask at a moment the user understands, not at first launch before any context.
- If the user denies, never re-prompt programmatically (Apple rejects this). They can re-enable in Settings.
- If denied, disable **all** cross-app tracking, not just IDFA — fingerprinting workarounds violate App Store 5.1.1.

### 2. Android: Play Policy + UMP

Play Store requires a consent flow for EEA / UK users when you use personalized ads or non-essential tracking. Google's **User Messaging Platform** (UMP) is the common path:

```kotlin
val params = ConsentRequestParameters.Builder()
    .setTagForUnderAgeOfConsent(false)
    .build()

consentInformation = UserMessagingPlatform.getConsentInformation(this)
consentInformation.requestConsentInfoUpdate(
    this, params,
    {
        UserMessagingPlatform.loadAndShowConsentFormIfRequired(this) { err ->
            if (consentInformation.canRequestAds()) {
                initializeMobileAdsSdk()
            }
        }
    },
    { err -> /* network / config error — block ads until resolved */ },
)
```

Same principle: do not load ad SDKs until consent status is known.

### 3. Lawful Basis (GDPR) — Beyond Ads

Consent is **one** of six lawful bases; often not the right one.

| Processing | Typical lawful basis |
| ---------- | -------------------- |
| Core feature (login, ordering) | Contract |
| Security & fraud prevention | Legitimate interest (documented) |
| Personalized ads / cross-site tracking | Consent |
| Product analytics (aggregate) | Legitimate interest or consent, depending on regulator |
| Marketing emails | Consent |

Document the basis per processing purpose in your privacy policy. Do not default everything to "consent" — it's fragile and creates UX friction.

### 4. Consent UX Rules

- Equal prominence for **Accept** and **Reject** buttons. No dark patterns.
- "Reject all" must be as easy as "Accept all" (one tap).
- No pre-ticked boxes.
- The consent decision must be **recorded** (timestamp, version, user ID / install ID) for audit.
- Support withdrawal: an always-reachable "Privacy Choices" screen in settings.

### 5. Per-Purpose Toggles

Use a Consent Management Platform (CMP) or roll your own `ConsentStore`:

```ts
type Purpose = 'analytics' | 'ads' | 'crash_reporting' | 'personalization';

interface ConsentRecord {
  purpose: Purpose;
  granted: boolean;
  recordedAt: string; // ISO
  version: string;    // policy version at time of consent
}
```

Every SDK initialization gates on the relevant purpose:

```ts
if (consent.granted('analytics')) Analytics.init();
if (consent.granted('crash_reporting')) Sentry.init();
```

Re-evaluate on every cold start; do not cache "we already initialized".

### 6. Minors

- iOS: `SKAdNetwork` + ATT plus App Store age rating.
- Android: `setTagForUnderAgeOfConsent(true)` where applicable; Play has strict Families policy.
- Under-16 users in the EEA need parental consent for most non-essential processing.

### 7. CCPA / CPRA (California)

- Honor a **Global Privacy Control** signal if your WebViews surface one.
- Provide a clear "Do Not Sell or Share My Personal Information" link in the app (Settings / About).
- "Sale" and "Share" are broader than cash sales — programmatic ads often qualify.

### 8. Audit Trail

- Store every consent change with timestamp and policy version.
- Be able to **prove** consent on demand to a regulator.
- When the privacy policy materially changes, prompt again — silent updates don't carry consent.

## Checklist

- [ ] ATT is requested at a contextually appropriate moment with a clear purpose string.
- [ ] Denied ATT disables all cross-app tracking, including fingerprinting.
- [ ] UMP (or equivalent CMP) gates ad SDKs for EEA / UK users.
- [ ] Lawful basis is documented per processing purpose — not defaulted to consent.
- [ ] Accept / Reject have equal prominence; no pre-ticked boxes.
- [ ] Per-purpose toggles gate SDK initialization on every launch.
- [ ] Consent events are stored with timestamp + policy version, and withdrawable from Settings.
- [ ] Privacy policy changes trigger re-prompting.
