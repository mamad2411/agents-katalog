---
name: app-store-approval
description: Audit an iOS/iPadOS codebase for App Store rejection risks before submission. Use this skill whenever the user mentions App Store submission, App Review, TestFlight release, app rejection, ITMS errors, privacy manifests, PrivacyInfo.xcprivacy, App Store guidelines, paywall compliance, "is my app ready to ship", or preparing/pre-flight checking any iOS app for release — even if they don't explicitly say "audit". Also trigger when the user pastes an App Store rejection notice and wants to fix it.
license: MIT
---

# iOS App Store submission audit

Audit an existing iOS/iPadOS codebase for App Store rejection risks and produce
one report ranked by severity. Static checks first, judgement second, manual
checklist last.

**Do not trigger for Android / Google Play work.** This skill is iOS-only.

## Severity model

Every finding gets exactly one of these. Getting the level right matters more
than finding more items — a wall of maybes is useless to someone shipping
tomorrow.

| Level | Meaning |
|---|---|
| **HARD BLOCK** | Deterministic failure. The upload is rejected by App Store Connect, or review fails on a fact you can verify from the code (missing purpose string, undeclared required-reason API, missing account deletion). |
| **LIKELY REJECTION** | Matches a documented rejection cause. Not certain, but a reviewer following the guideline as written would reject it. |
| **RISK FLAG** | Needs human or metadata review: purpose-string quality, "ongoing value", minimum functionality, spam/duplication, metadata accuracy. |

When unsure between two levels, choose the lower one and say what would settle
it. Reviewer inconsistency is real — these are risk scores, not guarantees.

---

## Workflow

### 1. Detect the project

Confirm this is an iOS project before doing anything else. Look for:
`*.xcodeproj`, `*.xcworkspace`, `Package.swift`, `Podfile.lock`, `Info.plist`,
`PrivacyInfo.xcprivacy`, `pubspec.yaml` (Flutter), `project.pbxproj`.

If none are present, say so and stop — do not audit a non-iOS project.

### 2. Run the static scans

```bash
bash scripts/run_all.sh <project-root>
```

That runs all ten scans and prints project detection first. Individual scans, if
you only need one (e.g. the user pasted a specific ITMS error):

| Script | Covers |
|---|---|
| `scan_required_apis.sh` | ITMS-91053/91055/91056 — required-reason APIs vs `PrivacyInfo.xcprivacy` |
| `scan_sdks.sh` | ITMS-91061 — SDKs on Apple's 86-SDK list without a bundled manifest |
| `scan_plist.sh` | ITMS-90683 / 5.1.1 — missing, empty or generic purpose strings |
| `scan_ai_endpoints.sh` | 5.1.2(i) — AI calls without a consent gate |
| `scan_auth.sh` | 4.8 SSO, 5.1.1(v) account deletion, 5.1.1 forced login |
| `scan_paywall.sh` | 3.1.1 / 3.1.2 — purchase mechanism and the seven paywall elements |
| `scan_healthkit.sh` | 2.5.1 / 5.1.3 / 1.4.1 — HealthKit transparency and health data |
| `scan_functionality.sh` | 4.2 minimum functionality, 1.2 UGC, 2.3.1 hidden features, 4.7 mini apps |
| `scan_placeholders.sh` | 2.1 completeness, 2.3.10 other marketplaces |
| `scan_submission_readiness.sh` | ITMS-90022 icon/launch screen, export compliance, version keys, demo-credential requirement, in-app Terms link |

Scripts take the project root as their first argument and default to `.`.
They emit `[SEVERITY] guideline :: message` lines. Treat those severities as a
first pass — you own the final call after reading the references.

### 3. Read `references/deadlines.md` first

It is short and it gates everything else. Check the build SDK against the current
minimum (iOS 26 SDK / Xcode 26+ since April 28, 2026):

```bash
xcodebuild -version && xcodebuild -showsdks
```

If today is past **Q4 2026**, tell the user the dated facts in this skill are
unverified and fetch
<https://developer.apple.com/news/upcoming-requirements/>.

### 4. Read only the references the scans point at

Progressive disclosure — do not load all of them.

| Findings mention | Read |
|---|---|
| Privacy manifests, required-reason APIs, purpose strings, ATT, AI consent, health data | `references/privacy.md` |
| IAP, subscriptions, paywalls, external purchase links | `references/iap-storekit.md` |
| Metadata, screenshots, 4.3 spam, an existing rejection, the appeal path | `references/metadata-review.md` |
| Demo accounts, privacy policy/support URLs, EULA, App Privacy labels, age rating, export compliance, icons | `references/submission-artifacts.md` |
| Anything else, or to attach a guideline number | `references/rejection-db.md` |

`references/rejection-db.md` is the index: every guideline with the rule, the
detection signal, and the fix.

### 5. Cross-check every finding

For each one, attach:
- the **guideline number** or ITMS error code,
- **why Apple rejects it** (one sentence, from the rejection DB),
- **evidence**: `file:line`,
- the **fix**,
- the **source URL**.

Drop findings you cannot support with all five. A confident wrong finding costs
the user a day.

### 6. If the user pasted a rejection notice

1. Match the cited guideline in `references/rejection-db.md`.
2. Apply the fix from there; re-run the matching scan to confirm it is gone.
3. Read `references/metadata-review.md` for the Resolution Center reply and the
   appeal path — reply there first, fix-and-resubmit beats arguing in ~90% of
   fixable cases, and resubmissions should be surgical.
4. Sweep for the *same root cause elsewhere* in the app. Reviewers re-reject on a
   second instance of the issue they just flagged.

### 7. Ask what the repository cannot answer

Half of what gets an app rejected lives in App Store Connect, not in the code:
demo credentials, a live privacy policy URL, App Privacy labels, the age-rating
questionnaire, export compliance. Read
`references/submission-artifacts.md` and **ask the user** about these before
writing the report.

Ask only what the audit gave a reason to ask, in one batch, and keep it short:

| If the scans found | Ask |
|---|---|
| A login or account-creation flow | Are working demo credentials in App Review Information → Sign-in required? Do they reach every gated feature, including paid tiers? |
| Any data collection | Is the privacy policy URL live and public, and also linked in-app? |
| A subscription or IAP | Is the Terms/EULA link in the **Description** field, and does every IAP have a review screenshot? |
| `ITSAppUsesNonExemptEncryption` absent | Has export compliance been answered? Is TestFlight showing "Missing Compliance"? |
| A social feed or UGC surface | Is the age-rating questionnaire answered under the 5-tier system? |
| Anything at all | Is the Support URL live with a working contact method? Do the screenshots match this build? |

A **"no"** becomes a finding at its real severity — a login-gated app with no
demo account is a HARD BLOCK, not a checklist item. A **"yes"** becomes a
resolved line under SUBMISSION ARTIFACTS, so the report shows what was verified
rather than only what was broken. If the user does not know, record it as
unverified and keep it in the manual checklist.

Do not ask questions the code already answered, and do not re-ask on a re-run
within the same session.

### 8. Write the report

Write `APP_STORE_APPROVAL.md` in the project root. Structure:

````markdown
# App Store submission audit — <App name>
Audited <date> · <n> HARD BLOCK · <n> LIKELY REJECTION · <n> RISK FLAG
Guidelines verified August 2026 — re-verify at
https://developer.apple.com/app-store/review/guidelines/

## HARD BLOCK
### 1. ITMS-91053 — UserDefaults used with no privacy manifest entry
**Evidence:** `Sources/Storage/Cache.swift:14`, `Sources/App/Settings.swift:31`
**Why:** Apple rejects the upload when a required-reason API is used without a
declared reason. Nothing reaches review.
**Fix:** Add to `PrivacyInfo.xcprivacy`:
```xml
<dict>
  <key>NSPrivacyAccessedAPIType</key>
  <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
  <key>NSPrivacyAccessedAPITypeReasons</key>
  <array><string>CA92.1</string></array>
</dict>
```
**Source:** https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api

## LIKELY REJECTION
…

## RISK FLAG
…

## SUBMISSION ARTIFACTS
Things that live in App Store Connect, not in the code.

| Item | Status |
|---|---|
| Demo credentials in App Review Information | **MISSING — blocks review (2.1)** |
| Privacy policy URL live and linked in-app | Confirmed by developer |
| Support URL with contact method | Unverified — check before submitting |
| Export compliance (`ITSAppUsesNonExemptEncryption`) | Not set — TestFlight will show Missing Compliance |
| Age rating questionnaire | Confirmed by developer |

## Manual review checklist
…
````

Order sections HARD BLOCK → LIKELY REJECTION → RISK FLAG → SUBMISSION
ARTIFACTS, and order findings within each section by how long the fix takes
(quickest first) so the user can start immediately.

If a section is empty, keep the heading and write "None found." — an absent
section reads as an oversight.

### 9. Always end with the manual checklist

Static analysis cannot verify these. Include them verbatim in every report, as
unchecked boxes:

- [ ] Screenshots and description match the shipped build (2.3)
- [ ] Working demo account in App Review notes; tested on a cold install (2.1)
- [ ] Age-rating questionnaire answered under the 5-tier system; social feeds
      force 13+ from Sept 2026
- [ ] App Privacy labels match the actual data flows and `PrivacyInfo.xcprivacy` (5.1.1)
- [ ] Support URL is live and contains a real contact method (1.5)
- [ ] Privacy policy URL is live, and also linked inside the app (5.1.1(i))
- [ ] Terms of Use (EULA) link is in the App Store **Description** field (3.1.2)
- [ ] Built with the iOS 26 SDK / Xcode 26+, including on CI (ITMS-90725)
- [ ] Purpose strings name the feature, the benefit, and the data type (5.1.1)
- [ ] The paywall shows title, duration, full renewal price as the most
      prominent price, what is provided, Terms, Privacy, and Restore (3.1.2)
- [ ] Icon and app name use no other developer's brand (4.1(c))
- [ ] Export compliance answered — TestFlight is not stuck on "Missing Compliance"
- [ ] Every IAP has a review screenshot and description
- [ ] Tested on a physical device, cold install, in Airplane Mode too

Items the user confirmed in step 7 move to SUBMISSION ARTIFACTS as resolved —
do not make them tick a box they already answered.

---

## Judgement notes

- **Weight by frequency.** Performance (2.x) is the largest rejection bucket by
  far, then Legal (5.x). A 2.1 placeholder and a missing 5.1.1(v) delete button
  deserve more of the user's attention than an exotic 3.1.3 edge case.
- **Say what you cannot see.** If the app has a consent screen but you cannot
  tell whether it precedes the first network call, say exactly that and tell the
  user how to check.
- **Never invent a guideline number.** If you are not sure of the sub-number
  (3.1.x has moved repeatedly), cite the parent guideline and say the numbering
  should be confirmed against the live page.
- **This is not legal advice**, and Apple's guidelines change. Say so in the
  report footer.
