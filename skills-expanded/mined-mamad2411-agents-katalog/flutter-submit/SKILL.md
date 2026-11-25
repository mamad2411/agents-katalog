---
name: flutter-submit
description: App Store and Play Store submission gate for a Flutter app. `check` audits the actual repo before the release candidate is built — missing per-permission usage strings, an absent in-app account-deletion route, a targetSdk below the Play deadline, every collecting SDK in pubspec.yaml, and user-facing features behind an off flag. `triage` maps a pasted rejection to its likely real cause and a concrete fix. Usage — /flutter-submit <check|triage> [rejection text]
argument-hint: "<check|triage> [rejection text]"
arguments:
  - name: subcommand
    description: "Sub-command: check, triage"
  - name: args
    description: "For triage: the rejection text pasted from App Store Connect or Play Console"
user-invocable: true
context: fork
effort: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(find *)
  - Bash(ls *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(sed *)
  - Bash(awk *)
  - Bash(plutil *)
  - Bash(flutter *)
  - Bash(command -v *)
---

# Flutter Submit

Sub-command is `$ARGUMENTS[0]`. Remaining words are `$ARGUMENTS` minus the first token.

> **Run `check` before you build the release candidate, not after.**
> None of what follows is visible from the code. It surfaces at submission, when the release
> is already late, and every item costs days: a store metadata change needs a new build, a
> missing usage string needs a code change and a new build, a `targetSdk` bump needs a
> regression pass. A one-week review round-trip on top of that is the difference between
> shipping on the date and shipping next sprint.

---

## `/flutter-submit check`

An audit of the repo. Every step below reads real files and reports what is actually there.
Do not lecture the user about store policy for things you did not check — say explicitly
which items are repo-verifiable and which are console-only.

### Step 1 — Locate the app

```bash
find . -maxdepth 3 -name pubspec.yaml -not -path '*/build/*' -not -path '*/.dart_tool/*'
find ios -maxdepth 3 -name 'Info.plist' -not -path '*/Pods/*' 2>/dev/null
find android -maxdepth 3 -name 'build.gradle*' -o -maxdepth 3 -name 'AndroidManifest.xml' 2>/dev/null
grep -n '^version:' pubspec.yaml
```

Note the flavor layout: multiple `Info.plist` files or `android/app/src/<flavor>/` directories
mean each step below must run per flavor. A usage string present in `Runner/Info.plist` but
absent from the release flavor's plist is the same crash.

If there is no `pubspec.yaml`, stop and say so.

---

### Step 2 — Per-permission usage strings (Apple: hard crash, not a rejection)

iOS terminates the process the first time a permission API is called with no matching
`Info.plist` string. It is not a warning and not a review note — it is a crash on the
reviewer's first tap. A biometric prompt with no `NSFaceIDUsageDescription` crashes on the
login screen, so review never gets past it.

Read the declared plugins, then the declared strings, then diff them:

```bash
sed -n '/^dependencies:/,/^dev_dependencies:/p' pubspec.yaml | grep -E '^\s{2}[a-z_]+:'
grep -o 'NS[A-Za-z]*UsageDescription' ios/Runner/Info.plist | sort -u
grep -o 'android:name="android.permission.[A-Z_]*"' android/app/src/main/AndroidManifest.xml | sort -u
```

Map each plugin found to the key it requires. Report a **Blocker** for every required key
with no entry, and for every key present whose value is boilerplate
(`"We need this permission"`, the Xcode placeholder, an empty string) — Apple rejects vague
strings under Guideline 5.1.1 even when the key exists.

| Plugin in `pubspec.yaml` | Required `Info.plist` key | Android counterpart |
|---|---|---|
| `local_auth` | `NSFaceIDUsageDescription` | `USE_BIOMETRIC` |
| `camera`, `mobile_scanner`, `qr_code_scanner` | `NSCameraUsageDescription` | `CAMERA` |
| `image_picker`, `photo_manager`, `gal` | `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSPhotoLibraryAddUsageDescription` (save) | `READ_MEDIA_IMAGES` |
| `geolocator`, `location`, `google_maps_flutter` (user location) | `NSLocationWhenInUseUsageDescription`; also `NSLocationAlwaysAndWhenInUseUsageDescription` if background | `ACCESS_FINE_LOCATION`, `ACCESS_BACKGROUND_LOCATION` |
| `record`, `flutter_sound`, `agora_rtc_engine`, `livekit_client` | `NSMicrophoneUsageDescription` | `RECORD_AUDIO` |
| `speech_to_text` | `NSMicrophoneUsageDescription`, `NSSpeechRecognitionUsageDescription` | `RECORD_AUDIO` |
| `flutter_contacts`, `contacts_service` | `NSContactsUsageDescription` | `READ_CONTACTS` |
| `flutter_blue_plus`, `flutter_reactive_ble` | `NSBluetoothAlwaysUsageDescription` | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` |
| `device_calendar` | `NSCalendarsFullAccessUsageDescription` (iOS 17+), `NSCalendarsUsageDescription` | `READ_CALENDAR` |
| `health` | `NSHealthShareUsageDescription`, `NSHealthUpdateUsageDescription` | — |
| `app_tracking_transparency`, `google_mobile_ads`, `appsflyer_sdk`, `adjust_sdk` | `NSUserTrackingUsageDescription` | `AD_ID` |
| `flutter_local_notifications`, `firebase_messaging` | — | `POST_NOTIFICATIONS` (Android 13+) |

Two traps worth checking explicitly:

```bash
grep -rn 'PERMISSION_' ios/Podfile
find ios -name 'PrivacyInfo.xcprivacy' -not -path '*/Pods/*'
```

- **`permission_handler`** compiles every permission handler into the binary unless the
  Podfile sets `GCC_PREPROCESSOR_DEFINITIONS` to disable the ones you do not use. Left at the
  default it links APIs you never call, which draws both a static-analysis flag and a demand
  for usage strings you had no reason to write. If `permission_handler` is in `pubspec.yaml`
  and the Podfile has no `PERMISSION_*=0` block, report it.
- **`PrivacyInfo.xcprivacy`** on the app target is required for required-reason APIs. If the
  app uses `shared_preferences` (`NSUserDefaults`, reason `CA92.1`), file timestamps, disk
  space, or `getActiveProcessorCount`, and there is no manifest on the Runner target, report
  it. Plugins ship their own; the app target's is yours.

---

### Step 3 — In-app account deletion

Apple requires an in-app deletion path from any app that offers account creation
(Guideline 5.1.1(v)). Google requires the same **plus a publicly reachable web URL** that
works without installing the app, declared in the Play Console Data Safety form.

```bash
grep -rniE 'delete.?account|close.?account|deleteUser' lib --include='*.dart' -l
grep -rniE 'delete.?account' lib --include='*.dart' | grep -iE 'route|path|go\(|push|GoRoute'
```

Classify what you find:

- **No match anywhere** → Blocker. There is no deletion path.
- **A repository or provider method with no screen that reaches it** → Blocker. The API exists
  but the user cannot get to it; this reads to a reviewer identically to having none.
- **A screen exists** → confirm the route is reachable from a signed-in menu in at most a
  couple of taps, and that the flow completes in the app. Deletion that opens a browser,
  emails support, or says "contact us to delete your account" is the single most common
  form of this rejection, and it is rejected even though the feature exists.
- **In-app deletion present, no web URL** → Blocker for Google only. Note it separately so
  nobody assumes the Apple pass covers Play.

Also check the account is genuinely deleted rather than flagged: a soft-delete that leaves
the data addressable contradicts the Data Safety declaration made in Step 5.

---

### Step 4 — `targetSdk` against the Play deadline

```bash
grep -nE 'targetSdk|compileSdk|minSdk' android/app/build.gradle android/app/build.gradle.kts 2>/dev/null
```

**If the value is a literal** (`targetSdk = 34`), compare it directly.

**If it is `flutter.targetSdkVersion`** — the common default — grep tells you nothing. The
number comes from the Flutter SDK the build machine uses, so the repo and CI can disagree.
Resolve it:

```bash
flutter --version
FLUTTER_ROOT=$(dirname "$(dirname "$(readlink -f "$(command -v flutter)")")")
grep -rn 'targetSdkVersion' "$FLUTTER_ROOT/packages/flutter_tools/gradle/" | head -5
```

Report the resolved number and where it came from. If it resolves below the deadline, the fix
is either upgrading Flutter or pinning `targetSdk = <N>` explicitly in `build.gradle.kts` —
pinning is the safer choice before a release, because it stops a CI Flutter upgrade from
silently moving it.

Deadlines (**verify against the Play Console before acting — this table rots annually**):

| Store | Rule | Recent enforcement |
|---|---|---|
| Google Play | `targetSdk` within one year of the latest major Android release; enforced 31 August each year, extensions to ~1 November on request | API 34 (2024), API 35 (2025), API 36 (2026) |
| Apple | Build with the current-year SDK — a Flutter/Xcode version question, not a `pubspec.yaml` one | iOS 18 SDK / Xcode 16 since April 2025 |

The Play deadline is published months ahead and is the one date in this whole file that is
knowable a year in advance. A release planned for late August with a stale `targetSdk` is a
planning failure, not a submission failure — flag it in the report as a date risk.

---

### Step 5 — Inventory every collecting SDK for disclosure review

```bash
sed -n '/^dependencies:/,/^dev_dependencies:/p' pubspec.yaml | grep -E '^\s{2}[a-z_0-9]+:'
```

List **every** dependency that collects anything, with what it collects, as a table the user
takes to the nutrition labels and the Data Safety form. This step is a report, not a
pass/fail — the tool cannot know what was declared in the consoles.

Say this plainly in the output: **the declaration is the developer's responsibility, not the
vendor's.** An analytics or ads SDK collecting an identifier you did not declare is a
rejection, and "the SDK does that on its own" is not a defence. Re-run this step whenever a
dependency is added — a transitive SDK arriving in a routine `pub upgrade` is how a
previously accurate declaration goes stale.

Common collectors and what to declare:

| Dependency | Collects |
|---|---|
| `firebase_analytics` | Usage data, app instance ID, coarse location from IP |
| `firebase_crashlytics` | Crash logs, device identifiers, any user ID you set |
| `firebase_messaging` | FCM registration token — a device identifier |
| `firebase_performance` | Performance data, network URLs |
| `google_mobile_ads` | Advertising ID, device data — triggers ATT on iOS |
| `appsflyer_sdk`, `adjust_sdk`, `branch_io` | Attribution identifiers, install referrer |
| `amplitude_flutter`, `mixpanel_flutter`, `posthog_flutter`, `segment_*` | Product analytics, user IDs |
| `sentry_flutter`, `datadog_flutter_plugin` | Crash and error data, breadcrumbs, request URLs |
| `onesignal_flutter`, `braze_plugin`, `clevertap_plugin` | Push tokens, profile attributes, behaviour |
| `intercom_flutter`, `zendesk_*` | Contact info, support conversations |
| `smartlook`, `uxcam`, session-replay SDKs | Screen recordings — declare, and mask PII fields |
| `purchases_flutter` (RevenueCat), `flutter_stripe` | Purchase history, IDFV, payment metadata |
| `amplify_auth_cognito`, `firebase_auth` | Email, user ID, auth tokens |
| `connectivity_plus`, `device_info_plus` | Device and network attributes — often forgotten |

Flag any SDK present but with no matching declaration the user can point to. Ask them to
confirm each row against the live form rather than assuming last release's answers hold.

---

### Step 6 — User-facing features behind an off flag

A reviewer sees the app exactly as it ships. Anything gated off is, to them, absent — and if
the listing, screenshots, or release notes describe it, that is a Guideline 2.3.x mismatch on
top of missing functionality.

```bash
grep -rniE 'featureFlag|feature_flag|remoteConfig|isEnabled|kSwitch|flags\.' lib --include='*.dart' | head -40
find . -name 'remote_config_defaults*' -o -name '*flags*.dart' -not -path '*/build/*' | head
```

For each flag found, determine its **default** value — the value the reviewer gets, since the
review device usually has no remote config fetched on first launch. Report as a Blocker any
flag that is off by default and gates a screen, route, or nav entry. The two acceptable
resolutions: turn it on for the release, or write into the review notes exactly how to enable
it, with the account or code needed. Silence is not one of them.

Cross-check against the release notes and store description if either is in the repo.

---

### Step 7 — Console-only items (report as manual, do not guess)

The repo cannot answer these. List them as an explicit manual checklist so nothing is assumed
to have passed just because the automated steps did:

| Requirement | Apple | Google |
|---|---|---|
| Demo account for review | Required, must be live and reachable | Demo account / testing instructions |
| Privacy disclosure | Nutrition labels + privacy manifest | Data Safety form |
| Payments | IAP for digital goods; no external purchase links | Play Billing for digital goods |
| Content rating | Age rating questionnaire | Content rating questionnaire |
| Metadata | Screenshots per device class, description, what's new | Store listing, graphics |

Two of these fail often enough to call out by name:

- **Demo credentials** — verify them the day of submission, on a device, in an incognito
  session. Expired, wrong, or 2FA-gated credentials are the most common single cause of
  "incomplete information", and the account is normally the last thing anyone tests.
- **Store metadata and screenshots** should be versioned in the repo and generated, not
  hand-edited in two consoles. If they only exist in the consoles, note it — the two listings
  drift, and the drift is invisible until a reviewer reads one of them.

---

### Step 8 — Write the report

Write `SUBMIT-CHECK-<version>.md`:

```markdown
# Submission Check — <app name> <version>
_Date: <today>_
_Target: App Store + Play Store_

## Summary
- Blockers: <N> · Warnings: <N> · Manual: <N>
- Verdict: 🚫 Do not build the RC / ⚠️ Build, resolve before submit / ✅ Clear

## Blockers

| # | Finding | File | Store | Status |
|---|---|---|---|---|
| 1 | `local_auth` in pubspec, no `NSFaceIDUsageDescription` — crash on first biometric prompt | ios/Runner/Info.plist | Apple | Open |
| 2 | No web account-deletion URL | — | Google | Open |

## Warnings
…

## Manual — verify in the console
- [ ] Demo account tested today on a device
- [ ] Data Safety form matches the SDK inventory below
…

## SDK disclosure inventory
| Dependency | Collects | Declared? |
|---|---|---|
…
```

Then present the summary table and ask which items to fix, in the same shape as
`/dev-review`:

> **Submission check complete. <N> blockers, <N> warnings, <N> manual items.**
>
> Which would you like to fix now?
> - Item numbers (e.g. `1 3`)
> - `all` — fix every repo-fixable item
> - `skip <number> — <reason>`

Fix only what lives in the repo: usage strings, a `targetSdk` pin, a flag default, a
deletion route. Console items you can only hand back as a checklist. Update each item's
Status as you go, and finish by restating the verdict — **if any blocker is still open, say
the release candidate should not be built yet.**

---

## `/flutter-submit triage <rejection text>`

Read the pasted rejection. Name the likely **cause**, not the rejection — the store's wording
describes a symptom the reviewer saw, and repeating it back is worth nothing. For each,
confirm the diagnosis against the repo before recommending anything.

### Incomplete information (Apple 2.1)

**Almost always: the reviewer could not sign in.** Wrong credentials, an expired trial
account, a password rotated since last submission, or a 2FA/SMS/email OTP gate the reviewer
cannot pass. It is rarely about missing metadata, whatever the wording suggests.

Confirm: sign in with the exact demo credentials from the submission, on a device, from a
clean install. Check whether the account hits an OTP, an email verification, an
invite/allow-list check, or a region gate.

Fix: a permanent review account exempt from OTP and from expiry, with the exemption keyed on
the account rather than a build flag. Put the credentials in the review notes with any extra
step spelled out.

### Broken functionality / crash (Apple 2.1, Play pre-launch report)

**Usually one of three:** a crash on the reviewer's OS version (typically the newest, which
your device fleet may not have), a crash or empty state specific to the reviewer's region or
locale, or a feature behind a flag that was off so the flow dead-ends.

Confirm: read the attached crash log and symbolicate it. Run the flow on the latest OS
simulator, then again with the device region set to the review region — Apple's reviewers are
usually in the US, Google's vary. Re-run Step 6 above on the submitted commit.

Fix: the actual crash. If it was a flag, turn it on or document the toggle in the notes.

### Privacy mismatch (Apple 5.1.2, Play Data Safety)

**Means the declaration differs from observed traffic.** The reviewer or Play's scanner saw
the app send something not declared — most often an advertising or device identifier from an
SDK nobody thought about, sent before consent, or sent by a dependency added since the last
declaration.

Confirm: proxy the app on a clean install and log every outbound host before any consent
prompt. Compare against the Step 5 inventory and the live form.

Fix: correct the declaration to match reality, or stop the traffic. Do both in the same
submission or the next review sees the same mismatch.

### Account deletion missing (Apple 5.1.1(v), Play)

**Means it is buried, web-only, or "contact support"** — much more often than genuinely
absent. Deletion four levels into a settings tree, deletion that opens a browser, or deletion
that files a support ticket all fail.

Confirm: count the taps from the signed-in home screen. Check the flow completes in-app.
Check Google's separate web URL requirement.

Fix: a visible entry in account settings, in-app completion, and a public web URL for Play.

### Minimum functionality (Apple 4.2)

**Means the app reads as a website wrapper.** Common triggers: most screens are `WebView`, no
platform integration (push, biometrics, offline, share, widgets), or it is a thin catalogue
with no account-specific behaviour.

Confirm: count `WebView`/`flutter_inappwebview` usage against native screens.

Fix: native screens for the core flows and real platform integration. This is a product
change, not a resubmission — do not promise a fast turnaround on it.

### External payment link (Apple 3.1.1)

**Means a link out for digital goods** — a "manage subscription on our site" link, an upgrade
CTA opening a browser, or a `url_launcher` call reachable from a paywall.

Confirm: `grep -rn 'url_launcher\|launchUrl' lib --include='*.dart'` and trace which of those
are reachable from purchase or upgrade surfaces.

Fix: IAP for digital goods. Physical goods and services consumed outside the app are exempt —
be sure which one this is before rewriting a payment flow.

---

### Before resubmitting

1. **Reply in the review thread with specifics** — what the cause was, what changed, the
   build number that carries the fix, and step-by-step repro for the reviewer including
   credentials. A bare resubmission usually routes to the same reviewer, who repeats the same
   test and reaches the same conclusion; the thread is the only channel that changes it.
2. **Attach evidence** where there is any — a screen recording of the deletion flow, the
   symbolicated crash resolved, the corrected Data Safety form.
3. **Do not spend expedited review here.** Requests are remembered against the account and
   granting gets harder the more you ask. Reserve it for a production outage or a security
   fix, not for a self-inflicted rejection.
4. **Re-run `/flutter-submit check`** on the fix commit before building the new RC. A
   rejection fix that introduces a second blocker costs another full round-trip.
