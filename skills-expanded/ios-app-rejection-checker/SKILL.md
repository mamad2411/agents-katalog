---
name: ios-app-rejection-checker
description: Check whether an iOS app will pass App Store review BEFORE submitting. Scans the project (native Swift/Xcode or Expo/React Native), its App Store metadata and its App Review notes for the things reviewers reject most - paywall disclosures, review prompts, permission strings, ATT, hidden IAP offers, account deletion, metadata claims - then does a reviewer-style read of the paywall, onboarding and listing, and writes a pass/risk report plus draft App Review notes. Use when the user says "will this pass review", "app review check", "preflight", "before I submit", "review my submission", "am I going to get rejected", "check against App Store guidelines", or is about to submit/resubmit a build.
user_invocable: true
---

# iOS App Rejection Checker

Predict App Review's verdict before Apple does. Two passes:

1. **Scanner** (`scripts/preflight.py`, stdlib Python): fast, deterministic static checks with file:line evidence.
2. **Reviewer pass** (you): confirm every scanner lead in the code, then check what a static scan can't: what the reviewer actually sees in the first minute, whether the paywall reads honestly, whether the listing matches the app.

The scanner produces leads, not verdicts. Never paste its output as the report. A finding you haven't confirmed in the code doesn't go in the Blockers list.

## Arguments

- Project directory (default: current directory). Monorepo: point at the app package.
- Optional `--metadata <file|dir>`: App Store listing. Auto-detected: `fastlane/metadata/en-US/`, `aso/en-US.md`, `ASO.md`, `docs/ASO.md`, `metadata.md`. Markdown files are parsed by heading (Name/Title, Subtitle, Keywords, Promotional text, Description, What's New) taking the first fenced block under each.
- Optional `--notes <file>`: App Review notes. Auto-detected: `aso/review-notes.md`, `review-notes.md`, `fastlane/metadata/review_information/notes.txt`, or a "Review notes" section of the metadata file.

- Optional `--online`: also fetch every Terms/Privacy URL found in the code. Use it whenever you have network access; a dead legal link is a rejection on its own.

If metadata or notes live only in App Store Connect, ask the user to paste them (or pull them with the ASC API if the project has a script for it). Without them, the 2.1(b) and 2.3.x checks are blind.

## Steps

### 0. Get the current rules

The guidelines move several times a year (Nov 2025, Feb 2026, Jun 2026 and 16 Oct 2026 all changed rejection surfaces; the Oct 2026 one added 2.5.19 hidden features and 2.3.14 creative assets and pulled AI content creation into 1.2). Before judging anything, fetch https://developer.apple.com/app-store/review/guidelines/ and skim https://developer.apple.com/news/ for review-related posts newer than the "verified" date at the top of `references/guidelines.md`. The live text wins over the reference files and over memory: when a finding rests on guideline wording, quote the live wording. The page often truncates near section 5; for anything past the cut, search for the subsection text and label it a secondary source. If there's no network, say the citations come from the bundled reference (and its date).

### 0b. What is being submitted?

For an update, find the last approved/submitted build (git tags, a handoff/STATUS/CHANGELOG file, or ask) and `git diff --stat` against it. Review the changed areas hardest. Confirm the version and build number were bumped; if the tree is identical to the approved build, say so up front. Read the project's own STATUS/TODO notes: known setup gaps (empty keys, unpublished legal pages) still go in the report, as blockers if they'd make the reviewer's build fail, labelled "(known, from STATUS.md)".

### 1. Run the scanner

```bash
python3 <this skill's dir>/scripts/preflight.py <project> --online --json > <scratch dir>/preflight.json
python3 <this skill's dir>/scripts/preflight.py <project> --online --brief  # one line per finding
```

Read `summary` first: project kind, whether IAP was detected, which files it treated as the paywall, which metadata/notes it found. If `paywall_files` is wrong or empty while the app clearly sells something, find the real purchase screen yourself and do step 3a by hand.

### 2. Confirm or dismiss every FAIL and WARN

Open each location. Known false-positive shapes:

| Rule | Dismiss when |
|---|---|
| REVIEW-ONBOARDING | the call is in a file named onboarding but only runs after real use (e.g. a returning-user flow) |
| HIDDEN-IAP-* | the identifier is an analytics event or notification id, not a purchasable offering/product |
| PERM-UNUSED / PERM-VAGUE (INFO) | the string comes from an SDK default and the prompt is never shown |
| DEV-URL / DEBUG-MENU | gated by a build flag the regex didn't see (check the flag's definition) |
| PAYWALL-* "found elsewhere" | the link/restore exists, but confirm it's on the purchase screen itself, not just Settings |
| ATT-ADS | ads are behind a hard-off flag in this build (still flag it as "before you turn ads on") |

Keep a short "dismissed" list with one-line reasons. It shows the user what was checked.

### 3. Reviewer pass (what the scanner can't see)

Read the code like a reviewer on a fresh iPad with a sandbox account. Classify the app first (accounts, subscriptions, UGC/chat, AI, web content, kids, health, finance, gambling, VPN, crypto): the classification decides which checks are load-bearing. Read `references/guidelines.md` for the rule details and the field notes from real rejections.

**a. The paywall, every variant.** Find every screen that can start a purchase (main paywall, onboarding paywall, winback/downsell, upgrade sheets, A/B variants).
- Billed price is the most prominent price. A "$0.77/week" breakdown may not be larger than "$39.99/year".
- A trial always says what it becomes: "7 days free, then $39.99/year".
- Prices come from StoreKit/RevenueCat at runtime. Hardcoded strings only as DEBUG fallbacks.
- Restore, Terms (EULA) and Privacy are on the screen, tappable, and open real pages.
- No false scarcity ("gone forever", fake countdowns), no guilt-trip close button copy, no disguised close button.
- A hard paywall is allowed, but the reviewer must be able to see what they're paying for (feature list or preview).
- The failure path: what does the screen show if StoreKit/RevenueCat returns no products or times out? Reviewers on a flaky sandbox see exactly this. It must not say "beta"/"launching soon", must not fall back to hardcoded prices, and must not let the user through.
- Trial copy matches the plan: "then $X/year" on the annual plan, not a per-month figure.
- Discount percentages in copy ("50% off") match what the offer actually computes.
- Total price billed is shown per period, and the trial is not more prominent than the billed amount. Cancel wording ("Cancel anytime in Settings") near the button.
- Every perk listed on the paywall exists in this build.
- Purchase errors surface to the user: no `catch {}` that swallows a failed product load or purchase, and the RevenueCat/StoreKit calls exist in the installed SDK version.
- No pre-selected most-expensive plan presented as the only option, no trial on/off toggle (Apple rejects those), loot boxes show odds before purchase.

**b. First launch → first value.** Trace the startup path in code:
- Permission prompts (notifications, camera, ATT) each come after a screen explaining why, never back to back on launch.
- Each explainer's promise matches the code. "Only reminders" / "nothing else" while the app schedules discount notifications is a 4.5.4 problem; "photos never leave your phone" while any code path uploads them is a privacy misstatement.
- Social proof (testimonials, results, star rows) is real. Quoting actual App Store reviews is fine; invented quotes and results are not.
- ATT resolves before any ad SDK initialises or loads an ad.
- No review prompt in onboarding or before a success moment (this rejection hits apps that were approved with it before).
- Small screens: onboarding/paywall CTAs inside a ScrollView or otherwise reachable on iPhone SE and in iPad compatibility mode.
- Nothing required that the feature doesn't need: no forced account for a non-account app, no mandatory phone/gender/birthday fields, the app is usable after denying notifications, tracking and location (5.1.1).
- Photo picking uses the system picker rather than full library access where possible.
- First launch isn't empty: seed sample content or a clear first action, so a reviewer doesn't conclude minimum functionality (4.2).
- If the core feature needs something the reviewer won't have (a heavy bag, a barcode, a second device, a partner, a location), there's a demo path or the notes explain it and a video shows it.

**c. Everything purchasable is findable.** List every product/offering the build can sell (RevenueCat offerings, StoreKit product IDs, promotional/win-back offers, offer codes, products only sold in an A/B arm). Check remote flags (PostHog, Firebase Remote Config, RevenueCat targeting) that hide or swap offers: the reviewer must be able to reach every product attached to the version with the flags as they'll be at review time. For each one write how the reviewer reaches it. Anything not on the main paywall needs step-by-step notes AND a screen recording attachment. Written steps alone have been rejected under 2.1(b) for an offer that was really there.

**d. Listing vs app.**
- Every feature in the description exists in this build (2.3.1). No "coming soon".
- If features are paid, the description says so (2.3.2): a short SUBSCRIPTION section is enough, prices optional.
- No prices in name/subtitle/keywords, no competitor or Apple trademarks in keywords (2.3.7), no other platforms (2.3.10).
- Health/fitness/finance claims are tracking/education language, not diagnose/treat/guarantee (1.4.1).
- Uniqueness (4.3, stricter since Jun 2026): if the app is in a crowded category or shares a template/codebase with the developer's other apps, say what clearly sets it apart, and put that in the review notes.
- The privacy policy page (fetch it) names the data collected, the SDKs/third parties including any AI provider, retention, and how to delete data; a two-line policy gets flagged.
- Rights (2.3.9, 5.2.1): screenshots, icons and in-app art use nothing borrowed: other brands, celebrity or idol photos, film stills, sports league marks, without permission. Icons and screenshots must suit a 4+ audience even when the app is rated higher (2.3.8).
- Hidden behaviour (2.5.19 since Oct 2026, previously 2.3.1): remote flags or endpoints that change features after review, dormant screens, or content that differs by region/date, need to be described in the notes with their state at review time. The penalty is now removal plus account termination, and obfuscation is named as an aggravating method. `#if DEBUG` / `__DEV__` code and launch arguments are fine: they are not in the App Store binary.
- Creative assets (2.3.14, Oct 2026): if any product-page header or search-result art was uploaded in App Store Connect, it must be about the app, suitable for all audiences, and carry no prices, discounts, unverifiable claims or misleading references to other apps.
- If a screenshots folder exists, look at the images: they must show the app in use (not only marketing art), no Android/other-platform frames, no prices if the user's convention is no prices.

**e. Category-specific.** Apply only what fits:
- Screen Time / Family Controls: entitlement approved for distribution; the app explains what gets blocked and how to undo it.
- HealthKit: only for health/fitness purposes; data never used for ads; health data not stored in iCloud documents.
- AI features: disclosure + consent before personal data (photos, health, messages) goes to a third-party model (5.1.2(i)); outputs filtered; for chat/companion apps, reporting.
- AI content creation (image/video/audio generation, and chat whose output can be shared): since Oct 2026 this is inside 1.2 by name. Needs a filter for objectionable material (nonconsensual intimate imagery is called out), a Report path with timely responses, Block where other users are involved, and published contact info. Unfixed violations after notice are a Developer Code of Conduct matter.
- User-generated content shown to other users: filter, report, block, contact info (1.2).
- Photo rating/scanning of bodies or faces: an age gate that excludes minors, and no sexualised framing (1.1).
- Accounts: in-app deletion (5.1.1(v)); Sign in with Apple when third-party login exists (4.8); demo account in the notes.
- Health apps: a "not medical advice / consult your doctor" line; no vitals measured with phone sensors.
- Apps that run downloaded code or generate apps (2.5.2, 4.7): new features ship through review, OTA updates only for fixes.
- Kids category: no third-party analytics/ads, parental gate before links and purchases.
- Gambling, crypto, VPN, medical devices: stop and tell the user these have their own rules and entitlements that are worth checking against the current guidelines.

### 3f. App Store Connect (outside the repo)

A large share of first-submission failures are ASC settings a repo can't show. If the `asc` CLI is installed (github.com/rudrankriyam/App-Store-Connect-CLI) and authenticated, run `asc validate` for the app and fold its errors into the report. Otherwise put these on the checklist:
- First auto-renewable subscription (and any new IAP) attached to this version's submission, with localizations, a review screenshot and prices set; Paid Apps agreement active.
- Privacy Policy URL, Support URL (both load), App Privacy answers published and matching every SDK (RevenueCat, analytics, attribution, AI provider).
- Terms of Use link in every localized description, or a custom EULA set.
- Age rating questionnaire answered with the 2026 questions (13+/16+/18+ tiers; AI chat, UGC, medical/wellness topics affect it).
- Screenshots for every required device size; 13-inch iPad screenshots if the app supports iPad. Creative assets (2.3.14), if uploaded: no prices or discounts in the art.
- Export compliance answered (or ITSAppUsesNonExemptEncryption in the build), content rights, EU trader status (DSA) if sold in the EU.
- Review contact info and a working demo account if "sign-in required" is ticked; notes rewritten for this version.
- Built with the current required Xcode/SDK (Xcode 26 since Apr 2026).

### 4. Write the report

Use this shape. Keep it scannable; the user wants to know whether to hit Submit.

```
# iOS App Rejection Check: <App> <version (build)>

**Verdict: Ready / Ready after fixes / Not ready**. One sentence on why.

## Blockers (will very likely be rejected)
1. <Title> (Guideline x.y) · Confidence: upload-blocked | common rejection | judgment call
   Where: `file:line`. Why a reviewer hits it (quote the live guideline when it matters). Fix.

## Risks (could be rejected, reviewer-dependent)
...

## Check on a device before submitting
- [ ] Fresh install on an iPad (and iPhone SE size): onboarding + paywall fully usable
- [ ] Sandbox purchase of every product, including hidden offers; Restore works
- [ ] Deny every permission: the app still works and doesn't loop the prompt
- [ ] Airplane mode / products fail to load: the paywall shows a retry state, not fake prices or a way through
- [ ] Every link in the app and listing (Terms, Privacy, Support) opens a real page
- [ ] <app-specific items>

## Dismissed scanner leads
- RULE: one-line reason

## Not checked
Runtime crashes, real purchase/restore behaviour, live server content, OAuth/OTP flows, remote-config state at review time, linked SDK internals (only app code was scanned), App Store Connect fields not provided. Never imply these were verified.

## Draft App Review notes
<paste-ready text from references/review-notes-template.md, filled in>
```

Confidence labels: **upload-blocked** only when App Store Connect / upload validation rejects it mechanically and the evidence reflects what ships (from source alone, say "upload-blocked if shipped as-is"); **common rejection** for patterns reviewers reject routinely or that match a real case in the field notes; **judgment call** for semantic calls (uniqueness, copy, claims) where reviewers vary. Never give approval odds or invent statistics.

Verdict rules, counting scanner findings and reviewer-pass findings alike: any confirmed blocker → "Not ready". Only risks or must-fix-before-submit items like stale notes → "Ready after fixes". Nothing confirmed → "Ready", and still include the device checklist. For Expo projects without a build number (EAS autoIncrement), write the version and "(build: EAS auto)".

### 5. Offer fixes

If the user is responding to a rejection rather than preventing one: "Metadata Rejected" means fix the listing and resubmit the same binary; a plain rejection needs a new build only if the fix is in the binary. Reply in the App Review thread in App Store Connect first, and only escalate to the App Review Board appeal (one per submission) with a specific compliance argument. Expedited review is for critical bug fixes or real time-sensitive events only.


Offer to fix confirmed issues. Don't edit code unless the user asks. Metadata fixes: give paste-ready text as plain text (no blockquotes). For hidden offers, give the exact recording steps.

## Testing the scanner

The repo (github.com/acalise/claude-skill-ios-app-rejection-checker) has two test layers: fixture tests (a planted-mistakes demo app and its fixed twin) and `tests/replay.py`, which replays real rejections by scanning the rejected and the fixed git revision of an app. When a new rejection comes in, add it as a replay case and plant it in the demo fixture before changing a rule.
