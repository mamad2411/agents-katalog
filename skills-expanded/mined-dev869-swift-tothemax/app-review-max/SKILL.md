---
name: app-review-max
description: "Pass Apple App Review the first time and recover fast when rejected. USE THIS SKILL whenever the user is submitting to the App Store, preparing a submission, asks 'will this get rejected', mentions App Review, a rejection, Resolution Center, an appeal, or any guideline number (2.1, 2.3, 3.1.1, 4.3, 5.1.x, etc.); whenever they set up TestFlight external testing / Beta App Review; whenever they want pre-submission checks, QC, demo accounts, reviewer notes, metadata or screenshot review; and whenever they ask IAP/paywall/subscription questions framed as compliance ('is this allowed', 'can I link to my website for payment'). Covers rejection playbooks, monetization compliance (US anti-steering + EU DMA state as of mid-2026), and an archive-to-approval checklist. Defer privacy manifests, GDPR, and legal document drafting to apple-legal-max; defer versioning, phased release, and release automation to apple-release-ops."
---

# App Review Max — Pass Review, Recover From Rejection

You own one outcome: the app gets **approved**. Audit like a reviewer, fix like a developer, and write reviewer-facing text like someone who wants a 24-hour turnaround.

Scope boundaries: privacy manifests, nutrition labels, GDPR/CCPA, and legal documents belong to `apple-legal-max`. Build numbers, phased release, and release automation belong to `apple-release-ops`. This skill covers everything App Review and QC: guideline compliance, pre-submission checks, rejection recovery, and reviewer communication.

## How App Review Actually Works

Know the machine before you feed it:

1. **Upload-time automated checks.** The moment a build hits App Store Connect, automated analysis scans for private API usage, missing usage-description strings, malformed Info.plist entries, missing privacy manifest declarations, and invalid entitlements. These produce ITMS errors/warnings by email — fix them before human review ever starts.
2. **Human review.** A reviewer installs your build on a physical device (recent iOS, typically from a California/US network — plan geofencing and allowlists accordingly), reads your metadata, and exercises the app for minutes, not hours. They follow your App Review notes if you wrote any; they improvise if you didn't.
3. **Timeline.** Apple states 90% of submissions are reviewed within 24 hours. Budget 24–48h per attempt, and assume at least one rejection cycle for first submissions — plan launch dates with a week of buffer.
4. **What reviewers see.** Your binary, all metadata (name, subtitle, description, keywords, screenshots, previews), your privacy labels, the age-rating questionnaire, IAP products submitted with the build, and your App Review notes. They do NOT see your source code, your roadmap, or your intentions. If a feature is invisible or gated, it does not exist unless your notes make it exist.
5. **Rejection anatomy.** Rejections arrive in App Store Connect (Resolution Center thread) citing specific guideline numbers, often with screenshots of the offending screen. Two flavors: **binary rejected** (fix requires a new build) and **metadata rejected** (fix the listing text/screenshots and resubmit the same build — much faster).
6. **Scale context.** Apple reviews millions of submissions a year and rejects roughly a quarter of them. Rejection is routine process, not catastrophe. Treat the first rejection as a data point, not a verdict.

## Top Rejection Guidelines, Ranked by Frequency

Attack these in order — they cover the overwhelming majority of rejections. Deep dives with fixes and resubmission wording: [references/rejection-playbook.md](references/rejection-playbook.md).

| Rank | Guideline | What it is | One-line avoidance |
|---|---|---|---|
| 1 | **2.1 App Completeness** (~40% of all rejections) | Crashes, bugs, placeholder content, broken links, reviewer can't get past login | Test the exact archived build on a physical device + IPv6, and put a working demo account in App Review notes. |
| 2 | **2.3.x Accurate Metadata** | Screenshots not matching the app, misleading descriptions, hidden features, irrelevant keywords, prices in metadata | Every screenshot must be real UI from this build; describe only what this version does, in this version's UI. |
| 3 | **3.1.x Payments** | Digital goods sold outside IAP, missing restore, unclear subscription terms, non-compliant external links | Digital content/features go through IAP unless a 3.1.3 exception or your storefront's current external-link rules apply — verify region rules in [references/monetization-compliance.md](references/monetization-compliance.md). |
| 4 | **4.3 Spam / Design Minimum + 4.2 Minimum Functionality** | Template/copycat apps, thin wrappers around a website, duplicative submissions | Ship at least one capability a mobile-optimized website can't do, and never resubmit near-identical apps under new bundle IDs. |
| 5 | **5.1.x Privacy** | Missing/inaccessible privacy policy, vague permission strings, data collection without consent, undisclosed third-party AI sharing, no in-app account deletion | Every permission string names the feature it powers; privacy policy URL loads; account creation implies in-app account deletion; disclose and get consent before sending personal data to any third party, including AI APIs (5.1.2(i), tightened Nov 2025). |
| 6 | **4.0 Design** | Broken layouts, non-native UX, iPhone app unusable on iPad, ignoring safe areas | Run the release build on smallest and largest supported devices; fix anything that looks broken in 10 seconds of use. |

## Pre-Submission QC Checklist (Fast Pass)

Run this before every submission. Full ordered archive-to-approval list: [references/submission-checklist.md](references/submission-checklist.md).

- [ ] **Demo account**: working credentials in App Review notes; account pre-populated with realistic data; not expired; 2FA disabled or one-time codes provided. If login uses phone/SMS only, provide a test number that accepts a fixed code, or request demo-mode approval.
- [ ] **Login-wall rules**: don't require login unless the app has account-based core functionality (5.1.1(v)). If you offer any third-party login (Google, Facebook), Sign in with Apple or an equivalent privacy-respecting option is required (4.8). Account creation ⇒ in-app account deletion.
- [ ] **Reviewer notes written** — use the template below. Explain anything non-obvious: hardware dependencies, geo-restricted features, background modes, why permissions are needed.
- [ ] **IPv6**: app works on IPv6-only network (test via macOS NAT64 hotspot: Internet Sharing → "Create NAT64 network"). Review environment is IPv6/NAT64; hardcoded IPv4 literals and IPv4-only servers fail here.
- [ ] **Every link works**: support URL, marketing URL, privacy policy URL, and all in-app links (terms, help, EULA). Reviewers click them.
- [ ] **Zero placeholder content**: no lorem ipsum, "coming soon" screens, TODO strings, test data, or empty states that look broken.
- [ ] **IAP products** attached to the submission, in "Ready to Submit", visible in the app, purchasable in sandbox, with a working Restore Purchases control.
- [ ] **Permissions**: every requested permission has a specific usage string ("Camera scans receipts for expense capture", not "needs camera access"); no permission requested that isn't used.
- [ ] **Crash-free**: exercise the release-configuration build (not a debug build) on device: launch, all tabs, purchase flow, offline mode, empty states.
- [ ] **Metadata sanity**: name ≤30 chars, subtitle ≤30, keywords ≤100 (comma-separated, no spaces after commas), no prices/platform names ("Android") in any field, screenshots for 6.9" iPhone (and 13" iPad if iPad-enabled) showing actual UI.
- [ ] **Age rating questionnaire** current — Apple's revamped global ratings (4+, 9+, 13+, 16+, 18+) required updated answers by Jan 31, 2026; stale answers block submission.

## When You Get Rejected

1. **Read the actual guideline.** Open developer.apple.com/app-store/review/guidelines and read the full text of the cited number, not just the rejection summary. Half of all bad responses come from arguing against the summary instead of the rule.
2. **Classify the rejection.**
   - *Metadata rejected* → fix listing fields/screenshots, reply in the thread, resubmit same binary. Hours, not days.
   - *Binary rejected, you agree* → fix, bump build number, describe exactly what changed in the Resolution Center reply, resubmit.
   - *Reviewer couldn't find/access something* → don't change code. Reply with precise steps, fresh demo credentials, and a screen recording showing the feature working. This resolves a large share of 2.1 rejections without a new build.
   - *You believe the reviewer is wrong* → reply once in Resolution Center with a factual, guideline-quoting explanation. If the reply fails, appeal to the **App Review Board** (App Store Connect → Contact Us → Appeal). One appeal per rejection; the Board is a separate team and reads the whole thread.
3. **Resolution Center etiquette**: professional, specific, short. Quote the guideline text, state how you comply, attach evidence (video beats screenshots beats prose). Never argue policy fairness; argue facts. Never mention lawyers unless you mean it.
4. **Expedited review** (Contact Us → App Review → Expedite Request) is for: critical bug affecting live users, security fix, or a date-locked event (conference, regulatory deadline). Give the concrete reason and date. Don't burn it on a normal launch — repeat frivolous requests get future ones denied.
5. **Repeated 4.3/design rejections** are structural, not textual — no Resolution Center reply fixes "this app is too similar to others." Differentiate the product, then resubmit.

## App Review Notes Template

Paste into App Store Connect → App Review Information → Notes, adapted:

```
WHAT THIS APP DOES
One sentence. E.g., "Tracks strength workouts and syncs sets to HealthKit."

DEMO ACCOUNT
Email: review-demo@example.com
Password: <password>
This account is pre-loaded with sample workouts so all screens show real data.
(2FA is disabled on this account. / Use fixed SMS code 000000.)

HOW TO REACH KEY FEATURES
1. Paid content: Profile tab -> "Go Pro" shows the paywall. Sandbox purchases work; Restore is under Settings -> Restore Purchases.
2. <Feature reviewers might miss>: <exact tap path>.

PERMISSIONS
- Camera: scans gym equipment QR codes (Settings tab -> Scan).
- Location (While Using): finds nearby gyms on the Map tab. App is fully functional if denied.

ANYTHING UNUSUAL
- Requires no external hardware. / Pairs with <device>; demo video: <link>.
- Content is user-generated; moderation: report button on every post, 24h takedown.

CONTACT
<name>, <email>, <phone> - reachable during review.
```

## Legal-Flux Watchlist (verify before relying — state as of July 2026)

- **US external purchase links**: Allowed on the US storefront without entitlement (post-*Epic v. Apple* injunction, May 2025 guideline update). Ninth Circuit (Dec 2025) affirmed contempt but held Apple may charge a cost-justified commission on linked purchases; Apple's cert petition was granted by the Supreme Court in June 2026. **Rules and commission may change — re-verify guideline 3.1.1(a) before shipping external links.**
- **EU DMA**: External links, alternative marketplaces, and Web Distribution operate under Apple's June 2025 business terms; Core Technology Commission (5%) replaced the per-install Core Technology Fee on Jan 1, 2026. Fee math and entitlement details: [references/monetization-compliance.md](references/monetization-compliance.md).
- **US state age-verification laws** (Texas effective Jan 2026; Utah, Louisiana following): app stores + developers share age-assurance duties; Apple's Declared Age Range API is the compliance surface. Region-specific and moving.
- **Third-party AI data sharing** (5.1.2(i), Nov 2025): explicit disclosure + consent before sending personal data to external AI providers. Enforcement is active and expanding.
- **Xcode/SDK floor**: uploads must be built with Xcode 26 / platform SDK 26+ (enforced from late April 2026). Check developer.apple.com/news/upcoming-requirements before every submission cycle.

## References

- [references/rejection-playbook.md](references/rejection-playbook.md) — per-guideline deep dive: trigger, fix, resubmission wording.
- [references/monetization-compliance.md](references/monetization-compliance.md) — IAP vs external purchase by region, subscription and kids rules.
- [references/submission-checklist.md](references/submission-checklist.md) — exhaustive ordered checklist, archive → approval, incl. TestFlight external review.
- Apple guidelines: https://developer.apple.com/app-store/review/guidelines/ · Review process: https://developer.apple.com/distribute/app-review/

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `apple-legal-max` owns privacy manifests/labels/legal documents (route 5.1.x groundwork there); `apple-release-ops` owns the mechanics of getting builds up; `apple-hig-ux` owns fixing 4.x design rejections.
Ecosystem companions (delegate if installed): `apple-appstore-reviewer` for an adversarial pre-review simulation pass; `app-store-optimization` / `aso` for listing growth — ASO owns keywords/conversion, this skill owns compliance of the same metadata. Policy facts here are dated mid-2026 and win over older companion claims.
