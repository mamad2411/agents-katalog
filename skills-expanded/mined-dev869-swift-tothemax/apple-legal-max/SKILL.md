---
name: apple-legal-max
description: Legal and privacy compliance for Apple-platform apps (iOS/iPadOS/macOS/watchOS/tvOS/visionOS). Use this skill WHENEVER a task touches - privacy policy, terms of service, ToS, EULA, license agreement, privacy manifest, PrivacyInfo.xcprivacy, required reason APIs, App Tracking Transparency, ATT, IDFA, tracking domains, privacy nutrition labels, App Privacy details, GDPR, CCPA/CPRA, US state privacy laws, COPPA, kids apps, children's privacy, age ratings, account deletion requirements, data deletion, export compliance, encryption declarations, ITSAppUsesNonExemptEncryption, France ANSSI declaration, EU DMA, alternative app marketplaces, web distribution, external purchase links, DSA trader status, subscription legal terms, or auto-renewal disclosures. Also use when drafting or reviewing ANY legal document or App Store Connect privacy/legal field for an app, when adding an SDK that collects data, or when a user asks "what legal stuff does my app need?" Sibling skill app-review-max owns App Review rejection mechanics; this skill owns the law and Apple's privacy/legal rules themselves.
---

# Apple Legal Max — Legal & Privacy Compliance for Apple-Platform Apps

Everything a shipping Apple-platform app must have to be legally and policy-compliant: Apple's enforced privacy rules, the regulations that actually apply, and the documents the app needs. Cite the governing rule (App Review Guideline number or regulation article) for every requirement you state.

**MANDATORY FRAMING — tell the user this once per conversation, early:** "I'm not a lawyer and this isn't legal advice. This is engineering-grade compliance guidance based on Apple's published rules and the text of the regulations; have counsel review anything you'll actually publish or rely on — especially for kids' apps, health/financial data, or EU/regulated markets."

Fast-moving areas (EU DMA fees, US state age-verification laws, India DPDP) are marked **[as of July 2026 — verify]**. When one is load-bearing for the user's decision, re-verify against developer.apple.com before answering.

## Reference files — load on demand

| File | Load when |
|---|---|
| `references/privacy-manifests.md` | PrivacyInfo.xcprivacy, required reason APIs, tracking domains, SDK manifests, nutrition-label aggregation |
| `references/regulations-for-apps.md` | GDPR, CCPA/US states, COPPA/kids, DPDP, EU DMA/DSA, export compliance & France |
| `references/document-templates.md` | Drafting privacy policy / ToS / EULA / subscription terms; where each URL goes in App Store Connect |

## Compliance map — what applies when

Walk the app through these questions. Each "yes" pulls in obligations:

| Question | If YES, applies | Governing rules |
|---|---|---|
| Does the app (or any SDK in it) collect ANY data? | Privacy policy, accurate nutrition labels, privacy manifest data-type entries | Guideline 5.1.1(i), 5.1.2(i); App Privacy details |
| Does it **track** (link user/device data with third-party data for ads or share with data brokers)? | ATT prompt before tracking, `NSPrivacyTracking=true`, tracking domains declared, "Data Used to Track You" label | Guideline 5.1.2; ATT framework docs |
| Account creation in-app? | In-app account **deletion** (not just deactivation), discoverable, initiates full deletion | Guideline 5.1.1(v) |
| Third-party/social login offered? | Must also offer Sign in with Apple or an equivalent privacy-focused option | Guideline 4.8 |
| Made **for kids** or targets children? | Kids Category rules, no third-party ads/analytics (narrow exceptions), COPPA (US), GDPR Art 8 (EU), parental gates | Guidelines 1.3, 5.1.4; COPPA Rule (amended, in force) |
| Auto-renewable subscriptions? | Full auto-renew disclosure in app + metadata, ToS/EULA link in app AND App Store metadata, privacy policy link | Guideline 3.1.2; state auto-renewal laws (CA ARL etc.) |
| Health, fitness, or medical data? | HealthKit rules, no ads from health data, research consent; HIPAA only if a covered entity/BA; WA My Health My Data | Guidelines 5.1.3, 1.4.1; RCW 19.373 |
| Uses ANY encryption (incl. HTTPS)? | Export compliance answer every build; France ANSSI declaration if non-exempt crypto and distributing in France | `ITSAppUsesNonExemptEncryption`; US EAR; French decree 2007-663 |
| Distributed in the EU? | GDPR, DSA **trader status** (mandatory since Feb 2025 — no trader status = removed from EU App Store), DMA options (alt marketplaces, web distribution, external purchase links) | GDPR; DSA Art 30/31; Apple DMA terms **[as of July 2026 — verify fees]** |
| Distributed in the US? | ~19–20 state comprehensive privacy laws in force (CA, VA, CO, CT, UT, TX, OR, MT, FL, DE, IA, NE, NH, NJ, TN, MN, MD, IN, KY, RI); GPC honoring in ~12 states | See regulations reference |
| Any SDK from Apple's "commonly used SDKs" list? | SDK must ship its own privacy manifest + signature | developer.apple.com third-party SDK requirements |
| User-generated content? | Moderation, blocking, reporting, contact info | Guideline 1.2 |

## The non-negotiables Apple itself enforces

These are rejection/removal triggers regardless of what any law says:

1. **Privacy policy URL — always required, every app.** In App Store Connect metadata AND accessible within the app. Must state what's collected, how used, third-party sharing (and that those parties give equal protection), retention/deletion, and how to revoke consent. — 5.1.1(i)
2. **Account deletion if account creation.** In-app initiation of *deletion* (deactivation is not enough). Highly regulated industries may use extra confirmation steps but the entry point must be in the app. — 5.1.1(v)
3. **ATT before any tracking.** No fingerprinting, no "we'll track anyway via server-side matching." Declared `NSPrivacyTrackingDomains` are network-blocked until the user grants ATT permission. Denied ATT ≠ degraded core functionality. — 5.1.2, 2.3.1
4. **Nutrition label accuracy.** Labels must match actual behavior *including every SDK*. Apple audits; mismatch = rejection or removal. Update labels when behavior changes — labels are editable any time without a new binary. — 5.1.1, 5.1.2(i)
5. **Privacy manifest completeness.** Required-reason APIs used without a declared reason (or with an invalid reason code) → ITMS-91053 rejection at upload. — TN3183/TN3184
6. **Purpose strings.** Every permission prompt (`NSCameraUsageDescription` etc.) needs a specific, honest purpose string. — 5.1.1(i)
7. **Standard vs custom EULA.** Apple's standard EULA (LAE) applies by default — most apps need nothing. A custom EULA must include Apple's Minimum Terms (Apple not a party; Apple as third-party beneficiary; developer owns support, warranty, IP claims) and is set in App Store Connect App Information. Subscription apps using the standard EULA must still link "Terms of Use (EULA)" in the app description or in-app. — 3.1.2, Schedule "Instructions for Minimum Terms"
8. **Subscription disclosure.** Before purchase: title, length of subscription, price and price/unit, that it auto-renews until canceled, and cancellation instructions. — 3.1.2(a)
9. **Kids Category.** No third-party analytics or advertising (limited, contractually-bound exceptions); no links out / purchases without parental gate. — 1.3
10. **Age rating questionnaire.** New tier system (4+, 9+, 13+, 16+, 18+; 12+/17+ retired). The updated questions (in-app controls, capabilities, medical/wellness, violence) were mandatory to answer by Jan 31, 2026 — unanswered = update submissions blocked. Set a higher rating if your own policy requires an older minimum age. — App Store Connect age ratings **[system revamped 2025]**
11. **Trader status for the EU.** DSA requires verified trader contact info displayed on the EU product page; non-compliant apps are removed from the EU storefront. — DSA Art 30/31, enforced by Apple since Feb 17, 2025.

## Decision flow — what documents does this app need?

```
START: every App Store app
├─► Privacy Policy ................................ ALWAYS (5.1.1(i))
├─► Collects data? ─ yes ─► nutrition labels accurate + manifest entries
├─► Accounts? ─ yes ─► account-deletion flow + deletion described in policy
├─► Subscriptions or paid tiers?
│     ├─ standard EULA OK? ─► link Apple standard "Terms of Use (EULA)"
│     │                        (https://www.apple.com/legal/internet-services/itunes/dev/stdeula/)
│     └─ need custom terms (user conduct, UGC, service SLA)?
│           ─► Terms of Service (service contract) and/or custom EULA
│              with Apple Minimum Terms; upload EULA in App Store Connect
├─► UGC / social / marketplace? ─► ToS with acceptable-use, moderation,
│                                   takedown, DMCA agent (US)
├─► Kids? ─► COPPA-compliant direct notice + verifiable parental consent
│            program; privacy policy child section
├─► EU? ─► GDPR-grade policy (lawful bases, rights, transfers, DPO/rep
│           contacts) + trader status + (if used) DMA-channel disclosures
├─► Subscriptions? ─► auto-renewal disclosure block (in purchase UI +
│                      description) per 3.1.2 and state ARLs
└─► Encryption? ─► export compliance answer; France ANSSI declaration
                    if non-exempt and on the French storefront
```

Minimal viable set for a simple, no-account, no-ads utility app: **privacy policy + accurate "Data Not Collected" label + privacy manifest + export-compliance answer.** Nothing else.

## Quick reference — data types → nutrition label categories

Apple's App Privacy label categories and what maps into them (declare each as *Linked to you* / *Not linked*, and separately whether *Used to track*):

| You collect… | Label category |
|---|---|
| Name, email, phone, physical address, other contact info | **Contact Info** |
| Health/medical data, fitness/exercise data (HealthKit, Movement Disorder API, clinical) | **Health & Fitness** |
| Payment info, credit score, salary, income, assets | **Financial Info** |
| Precise location (GPS-level), coarse location (region/city) | **Location** |
| Racial/ethnic data, sexual orientation, pregnancy, disability, religious/political views, biometric data | **Sensitive Info** |
| Address book / contact list access | **Contacts** |
| Emails or texts content, photos or videos, audio data, gameplay content, customer support content, other user content | **User Content** |
| Web browsing history (content viewed outside the app) | **Browsing History** |
| In-app search history | **Search History** |
| User ID (account ID, handle), device ID (IDFA, IDFV, or derived) | **Identifiers** |
| Purchase history or purchasing tendencies | **Purchases** |
| Product interaction (launches, taps, views), advertising data, other usage data | **Usage Data** |
| Crash data, performance data (launch time, hangs, energy), other diagnostics | **Diagnostics** |
| Environment scanning (mesh/scene data, e.g. ARKit/visionOS) | **Surroundings** |
| Hand/head movement, other body data | **Body** |
| Anything else | **Other Data** |

Rules of thumb:
- **Every SDK counts.** Firebase Analytics collecting device ID = you declare Identifiers + Usage Data even if "you" collect nothing.
- **"Collected" = transmitted off-device** and retained longer than servicing the request. Purely on-device processing is not "collected."
- **Optional disclosure exemptions** (infrequent, optional feedback forms etc.) are narrow — read the App Privacy details page before relying on one.
- IP address used for anything beyond transient service delivery can itself be a collected identifier / coarse location.

## Working style for this skill

- Answer with **checklists keyed to rules** ("required by 5.1.1(v)", "GDPR Art 17"), not vibes.
- Distinguish **Apple policy** (rejection risk) from **law** (liability risk) — users constantly conflate them.
- When drafting documents, use `references/document-templates.md` skeletons; produce structure + accurate factual content, and flag every spot needing counsel or business decisions (jurisdiction, arbitration, data-sale stance).
- When auditing an app: enumerate SDKs first (Package.swift/Podfile.lock), then data flows, then map to labels/manifest, then documents. SDK-derived collection is the #1 source of label inaccuracy.
- Never claim compliance is achieved; say "these items satisfy X's stated requirements as published; confirm with counsel."
- For App Review rejection strategy, appeals, and review mechanics, defer to the sibling **app-review-max** skill; this skill supplies the substantive legal/privacy fixes.

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `app-review-max` enforces these requirements at review time (it owns Resolution Center strategy); `apple-release-ops` owns where the resulting URLs/labels get entered in App Store Connect.
No quality ecosystem companion exists for this facet (verified July 2026) — this skill is the source of truth. A locally-installed `legal` skill may exist for general indie-dev documents; this skill's Apple-specific and 2026-regulation content wins on conflicts.
