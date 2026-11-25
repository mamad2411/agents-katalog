---
name: privacy-by-design
description: Privacy-by-design principles on mobile — data minimization, purpose binding, consent. Use when introducing new data collection or third-party SDKs.
---

# Privacy by Design

## Instructions

Privacy by Design is an engineering posture, not a legal afterthought. Decisions made in the first week of a feature outweigh months of compliance paperwork.

### 1. The Three Questions

Before adding any data collection, answer in the PR description:

1. **What** exactly are we collecting (field list, types, precision)?
2. **Why** — which user-facing feature does it enable?
3. **For how long** — retention and deletion policy.

If you can't answer cleanly, don't add it.

### 2. Data Minimization

Collect the least-precise data that still makes the feature work:

- Location: need it only for "find nearest store"? Use `CLLocationManager` at **reduced accuracy** (`desiredAccuracy = kCLLocationAccuracyKilometer`) or Android's `PRIORITY_BALANCED_POWER_ACCURACY`. Consider iOS 14+ **approximate location** (`requestWhenInUseAuthorization` + user choice).
- Contacts: need a phone number only to check membership? Hash client-side, ping server with prefix-truncated hashes (k-anonymity) — don't upload the full contact book.
- Photos: use the **PhotoPicker** (`PHPickerViewController` on iOS, `ActivityResultContracts.PickVisualMedia` on Android) — you get the chosen asset without full library access.

```swift
var config = PHPickerConfiguration(photoLibrary: .shared())
config.selectionLimit = 1
config.filter = .images
let picker = PHPickerViewController(configuration: config)
// No Photos permission prompt required for this path.
```

```kotlin
val launcher = registerForActivityResult(
    ActivityResultContracts.PickVisualMedia()
) { uri -> /* process one image; no READ_MEDIA_IMAGES needed */ }
launcher.launch(
    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
)
```

### 3. Purpose Binding

- Each data field has **one** documented purpose.
- Reuse for a new purpose requires a new consent event, not a silent expansion.
- Analytics events that "might be useful later" are a red flag; collect when you have a concrete use.

### 4. On-Device Over Off-Device

- Perform processing on-device when feasible (ML classification, thumbnailing, redaction).
- Ship only derived / aggregate signals off-device.
- Apple's App Store policy, Google's Play Data Safety, and GDPR all reward this architecturally.

### 5. Identifiers

| Identifier | Use with caution |
| ---------- | ---------------- |
| IDFA / GAID | Advertising only; needs ATT on iOS, UMP consent on EEA Android. |
| `ASIdentifierManager` / advertising ID | Same as above. |
| `UIDevice.identifierForVendor` / `Settings.Secure.ANDROID_ID` | Scoped identifiers; still PII under GDPR. |
| Server-issued user ID | Prefer this for analytics / crash correlation. |
| IMEI / MAC / serial | Do not use on modern OSes; restricted and often unavailable. |

Use the weakest identifier that works. Generate a random install ID scoped to your app (`UUID.randomUUID()` stored in Keychain / Keystore) for things like A/B bucketing.

### 6. Third-Party SDKs

Each SDK added is a data-sharing decision:

- Enumerate what it sends (many SDKs send IP, install ID, app events by default).
- Add to Apple's Privacy Manifest (`PrivacyInfo.xcprivacy`) and Google Play's Data Safety form.
- Prefer SDKs that support **delayed initialization** until after consent.
- Audit at least yearly — SDKs expand scope between releases.

### 7. Logs, Crash Reports, Analytics

These are the three places PII leaks most often.

- Never log raw request / response bodies with user data in release builds.
- Strip PII from crash reports (stack traces are fine; user input in a `toString()` is not).
- For analytics, log **categories** ("filter_applied") not **content** ("searched for: alice@example.com").

```kotlin
// Don't
Timber.d("User profile: $profile")
// Do
Timber.d("Loaded profile uid=${profile.id.hashPrefix(8)}")
```

### 8. Default Settings

- Telemetry / crash reporting: **opt-in** in regulated regions, clearly disclosed elsewhere.
- Personalization / recommendations that rely on behavior: **opt-in**.
- Background location, microphone, camera: never "always" by default.

### 9. Data Export and Deletion

Shipping a feature → shipping an export path and a delete path. Build them alongside, not after launch. See [gdpr-mobile](../../compliance/gdpr-mobile/SKILL.md).

## Checklist

- [ ] Every new field has a documented purpose and retention period.
- [ ] Location / photos / contacts use the least-privileged API (reduced accuracy, PhotoPicker, hashed lookup).
- [ ] No feature reuses data for a new purpose without fresh consent.
- [ ] Processing happens on-device where feasible.
- [ ] Identifiers used are the weakest that work; no deprecated hardware identifiers.
- [ ] Every third-party SDK is entered in the iOS Privacy Manifest and Play Data Safety form.
- [ ] Logs, crash reports, and analytics do not carry raw PII.
- [ ] Export and delete paths ship with the feature, not later.
