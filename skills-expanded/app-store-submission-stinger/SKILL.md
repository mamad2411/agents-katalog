---
name: "app-store-submission-stinger"
description: "Prepare iOS and Android app submissions. Use for store review, ASO, privacy forms, or rejection remediation. Read README.md for the guide map."
license: AGPL-3.0-or-later
---

# App Store Submission Stinger

Start with [README.md](README.md) for the workflow map and detailed references.

You are the operational playbook that equips `app-store-submission-wasp-drone` with current intelligence on getting through App Store and Google Play review in 2026.

Current submission preparation starts with [guide 06](guides/06-prepare-artifact-privacy-and-entitlement-evidence.md), observed 2026-10-07, and its primary research. Earlier May guides are historical where dates, metadata assumptions or regional payment statements conflict. Refresh store requirements for the intended submission date. This pair prepares publication evidence; missing native StoreKit/Billing implementers remain explicit gaps.

---

## Activation checklist

Before acting, orient around these five questions:

1. **Platform:** iOS only, Android only, or both?
2. **Stage:** Pre-submission prep, first-ever submission, resubmission after rejection, or live-app update?
3. **Monetization model:** Free, premium, subscription, consumable IAP, or mixed?
4. **Special categories:** Children's content? Health data? Financial services? Gambling?
5. **Rejection present?** If yes, paste the full rejection text including reason codes.

Your answer to (4) gates the entire workflow. Children's category apps require COPPA/GDPR-K compliance and are subject to the strictest metadata review on both platforms. Flag children's issues at the top of every report.

---

## Evidence preparation first

Use [the artifact/privacy/entitlement procedure](guides/06-prepare-artifact-privacy-and-entitlement-evidence.md), [worksheet](templates/store-evidence-worksheet.md) and [synthetic cases](examples/store-evidence-readiness-cases.md) before the lifecycle below. Artifact hashes, native validation, signing identity, actual SDK flows and native/server entitlement tests are separate proof requirements. A completed source worksheet does not establish store eligibility or native runtime correctness.

## Core workflow

The submission lifecycle runs in five stages. Each stage has a dedicated guide. Work through them in order; a clean exit from each stage reduces rejection risk at the next.

### Stage 1: ASO strategy

See `guides/01-aso-strategy.md`.

Describe metadata accurately and measure conversion from actual product-page evidence. The October primary archive does not establish numeric ranking weights or screenshot-caption indexing; do not present those historical marketing claims as platform facts.

**Quick checklist:**
- Title: ≤30 characters (iOS), ≤30 characters (Android): include primary keyword
- Subtitle (iOS): ≤30 characters; Android short description: ≤80 characters
- iOS keyword field: 100 characters, comma-separated, no spaces after commas, no repeated words, no app name
- Screenshots: select the current required sizes and counts from App Store Connect for the actual supported device family; accurately show the app
- Schedule metadata review around actual product and audience changes; no fixed algorithmic freshness claim is established here.

See `guides/01-aso-strategy.md` for the full keyword research methodology and screenshot story sequencing.

### Stage 2: Compliance

See `guides/02-compliance-checklist.md`.

Prepare platform-specific privacy declarations using guide 06; no ranked rejection-frequency claim is established by the current primary archive.

**iOS critical items:**
- Privacy nutrition label (App Store Connect > App Privacy): every data type collected must be declared
- PrivacyInfo.xcprivacy manifest: required for any SDK using one of Apple's 5 required-reason API categories (file timestamp, system boot time, disk space, user defaults, active keyboard); the manifest is typically missing from third-party SDKs, not the app target
- Age rating: complete the questionnaire in App Store Connect (honest answers, Apple cross-checks)

**Android critical items:**
- Data Safety form (Play Console > Store presence > App content > Data safety): maps data collection to declared types
- April 2026 policy changes (deadline: October 28, 2026):
  - Contacts permissions → must use Android Contact Picker
  - Precise location → must offer Android Location Button
  - Geofencing → no longer approved for foreground services
- Age rating: complete the IARC questionnaire

See `guides/02-compliance-checklist.md` for the full checklist with field-by-field guidance.

### Stage 3: Submission workflow

See `guides/05-timeline-and-process.md`.

Upload the build (Xcode Organizer / bundletool), complete all metadata, set version information, and submit for review. Key action: do NOT submit the same build twice in rapid succession: it can trigger an automated flag.

**Timeline evidence:** Current queue duration is unknown in this update. Treat old guide ranges as historical observations, not guaranteed 2026 baselines. Bind any new planning range and confidence to dated queue evidence.

Qualify expedited review through current Apple review support for the actual release; this update does not establish its approval frequency. See `guides/05-timeline-and-process.md` for the qualifying criteria.

### Stage 4: Rejection diagnosis and remediation

See `guides/03-rejection-playbook.md`.

When a rejection arrives, the first thing to do is NOT re-submit. Read the rejection carefully and identify whether it is:

- **Policy rejection**: guidelines violation (2.x, 3.x, 4.x on iOS; DeveloperPolicies section on Android)
- **Metadata rejection**: inaccurate title, description, screenshots, or keywords
- **Binary rejection**: crash, functionality issue, or missing feature
- **Legal rejection**: IP, privacy, or legal compliance issue

Apple rejection notes are frequently terse. When the note is ambiguous, produce two interpretations and two remediation paths. Do NOT re-submit with only one fix until you have ruled out the second interpretation.

See `guides/03-rejection-playbook.md` for the full taxonomy and remediation patterns, including the appeal process.

### Stage 5: IAP and subscription setup

See `guides/04-iap-setup.md`.

For iOS, use StoreKit 2 (StoreKit 1 deprecated at WWDC 2024; this is now the only recommended API path). Five production patterns that prevent the most common bugs:
1. Never hardcode prices: fetch from StoreKit
2. Always finish transactions after granting access (or use `.finish()` in SK2)
3. Start the transaction listener at app entry, not at purchase time
4. Handle the grace period for subscription lapses
5. Provide a working restore mechanism for restorable purchases under App Review Guideline 3.1.1; verify the selected native UX and implementation.

For Android, qualify the bundled Billing Library version against the current deprecation table in guide 06. On the observed October date, new submissions and updates need 8+ unless an applicable extension has been granted. See `guides/04-iap-setup.md` for the product ID taxonomy, subscription group structure, and pricing matrix guidance.

---

## Critical directives

These are the guardrails baked into every action this Stinger enables:

- **Always cite the specific guideline by section number** (e.g., "App Review Guideline 3.1.1", "Google Play Developer Policy: Impersonation"). Developers need these citations for appeals.
- **Never recommend workarounds that violate platform policies.** A bypass that passes today's review risks retroactive removal and account termination.
- **State timeline estimates as ranges with a confidence level.** Review times are non-deterministic; single-point estimates break release planning.
- **Flag children's category (COPPA / CIPA / GDPR-K) issues at the top of every report.** These carry the highest regulatory and account-termination risk.
- **When a rejection is ambiguous, produce two interpretations and two remediation paths.** One wrong interpretation = one wasted resubmission cycle.

---

## Guide index

| Guide | When to open it |
|---|---|
| `guides/00-principles.md` | Foundation: gatekeeper mindset, how reviewers work |
| `guides/01-aso-strategy.md` | Pre-submission: keyword strategy, screenshots, metadata |
| `guides/02-compliance-checklist.md` | Privacy, age rating, data safety (both platforms) |
| `guides/03-rejection-playbook.md` | Diagnosing and remediating any rejection |
| `guides/04-iap-setup.md` | StoreKit 2 and Google Play Billing Library 7 setup |
| `guides/05-timeline-and-process.md` | Review timelines, expedited review, TestFlight |

## Template index

| Template | Purpose |
|---|---|
| `templates/submission-readiness-report.md` | Go / no-go checklist before first submit |
| `templates/rejection-remediation-plan.md` | Structured remediation from a rejection notice |
| `templates/privacy-label-checklist.md` | iOS nutrition label + Android data safety pre-flight |

## Example index

| Example | What it demonstrates |
|---|---|
| `examples/happy-path-ios-submission.md` | Full iOS submission walkthrough: ASO → compliance → submit → approved |
| `examples/rejection-recovery-guideline-2-1.md` | Handling a common metadata rejection (Guideline 2.1) on iOS |

---

## Research trail

Primary research: the shipped `research/research-summary.md`. The manifest, `research/index.md`, and the external notes are source-repository research, not shipped with the plugin.

Key sources consulted:
- Apple App Review Guidelines (via secondary citations, 2026)
- Google Play Policy Update: April 15, 2026 (official; 3 breaking changes)
- PrivacyInfo.xcprivacy enforcement guide (Mobile App Wiki, 2026)
- StoreKit 2 SwiftUI guide (Swift Crafted, updated for iOS 26 / Swift 6.2)
- App Store review queue delay analysis (AppStoreReview, 2026; 104% volume increase)

---

*Command Brief: `ai-tools/command-briefs/app-store-submission-wasp-drone-command-brief.md`*
*Research: `research/`*
*Part of the Wasp Nest. Created 2026-05-20.*
