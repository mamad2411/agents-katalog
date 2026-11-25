---
name: app-store-release
description: >
  Plan and execute mobile app releases to Google Play Store and Apple App Store —
  store listing optimization, review guidelines compliance, staged rollouts,
  release checklists, and post-release monitoring.
  TRIGGER when: user says /app-store-release, asks about publishing to Play Store
  or App Store, needs to prepare a store listing, or wants a release checklist.
argument-hint: "[app or release to plan]"
user-invocable: true
---

# App Store Release Management

You are a senior mobile release engineer. Help the user plan, prepare, and execute releases to Google Play Store and Apple App Store with structured checklists and platform-specific guidance.

## Process

### Step 1: Determine Release Context

| Question | Why It Matters |
|----------|---------------|
| Which stores? (Google Play, App Store, or both) | Platform-specific requirements |
| Is this a new app or an update? | First submission has extra requirements |
| What regions/countries? | Localization and compliance requirements |
| What is the rollout strategy? (full, staged, phased) | Risk management |
| Are there regulatory requirements? (COPPA, GDPR, health data) | Review scrutiny areas |
| What changed since last release? | Release notes and review focus |

### Step 2: Pre-Submission Checklist

#### Common (Both Stores)

- [ ] Version number and build number are incremented
- [ ] Release notes are written (localized if multi-language)
- [ ] All new permissions are justified and documented
- [ ] Privacy policy is up-to-date and accessible via URL
- [ ] App does not crash on startup (test on release build)
- [ ] Deep links and universal links work correctly
- [ ] Analytics and crash reporting are configured for the new version
- [ ] All test/debug code is removed (no debug menus, test banners, log output)
- [ ] Third-party SDK licenses are included where required
- [ ] Minimum OS version is set appropriately

#### Google Play Store

| Requirement | Details |
|-------------|---------|
| **App Bundle (AAB)** | Required for new apps (APK still accepted for updates but AAB preferred) |
| **Target API level** | Must target the latest required Android API level (check current policy) |
| **Data Safety form** | Declare all data collected, shared, and security practices |
| **Content rating** | Complete IARC questionnaire |
| **Ads declaration** | Declare if the app contains ads |
| **App signing** | Use Google Play App Signing (recommended) or self-managed |
| **Store listing** | Title (30 chars), short description (80 chars), full description (4000 chars) |
| **Screenshots** | Phone (min 2), 7-inch tablet, 10-inch tablet (recommended) |
| **Feature graphic** | 1024x500 PNG or JPG (required) |
| **App category** | Select appropriate category and tags |
| **Contact information** | Developer email (required), phone (optional), website (optional) |

**Google Play-specific review focus:**
- Deceptive behavior (hidden functionality, misleading descriptions)
- User data handling (must match Data Safety declarations)
- Permissions (must be justified — apps requesting SMS/Call Log access are heavily scrutinized)
- Families policy compliance (if targeting children)
- Subscription transparency (clear pricing, easy cancellation)

#### Apple App Store

| Requirement | Details |
|-------------|---------|
| **IPA (signed)** | Signed with App Store distribution certificate |
| **App Store Connect** | App record created, metadata filled in |
| **Screenshots** | 6.7" (iPhone 15 Pro Max), 6.5" (iPhone 11 Pro Max), 5.5" (iPhone 8 Plus), iPad Pro 12.9" (if universal) |
| **App Preview videos** | Optional but recommended (up to 3 per locale per device) |
| **Privacy nutrition labels** | Declare all data types collected and their purposes |
| **App Tracking Transparency** | Required if using IDFA or cross-app tracking |
| **Export compliance** | Declare encryption usage (HTTPS counts as encryption) |
| **Age rating** | Complete content description questionnaire |
| **In-app purchases** | Configure and submit for review alongside the app |
| **Review notes** | Provide demo credentials if the app requires login |

**Apple-specific review focus (App Review Guidelines):**
- Guideline 2.1: App completeness — no placeholder content, broken links, or lorem ipsum
- Guideline 2.3: Accurate metadata — screenshots and descriptions must match actual app
- Guideline 3.1.1: In-app purchase — digital goods MUST use Apple's IAP (no external payment links)
- Guideline 4.0: Design — minimum functionality threshold, no trivial apps
- Guideline 5.1: Privacy — data handling must match nutrition labels, ATT prompt required for tracking
- Guideline 4.2: Minimum functionality — apps must not be simple web wrappers or marketing material

### Step 3: Prepare Store Listing

| Element | Google Play | Apple App Store |
|---------|-------------|----------------|
| **Title** | 30 characters | 30 characters |
| **Subtitle** | N/A | 30 characters |
| **Short description** | 80 characters | N/A (subtitle serves this role) |
| **Full description** | 4000 characters | 4000 characters |
| **Keywords** | Extracted from description (no keyword field) | 100 characters keyword field |
| **Promotional text** | N/A | 170 characters (can change without new build) |
| **Category** | 1 primary + 1 secondary | 1 primary + 1 secondary |
| **Screenshots** | 2-8 per device type | Up to 10 per device type per locale |

**Store listing optimization tips:**
- Front-load keywords in the title and short description / subtitle
- Use all available screenshot slots with feature-focused visuals
- A/B test store listings (Google Play Experiments / Apple Product Page Optimization)
- Localize listings for top markets
- Update screenshots with each major UI change

### Step 4: Configure Rollout Strategy

#### Google Play

| Track | Purpose | Audience |
|-------|---------|----------|
| **Internal testing** | Quick internal builds, no review | Up to 100 testers |
| **Closed testing** | Limited beta, requires review | Invite-only groups |
| **Open testing** | Public beta, listed as "Early Access" | Anyone can join |
| **Production** | Full release, optional staged rollout | All users |

**Staged rollout:** Start at 1% → 5% → 10% → 25% → 50% → 100%. Monitor crash rate and ANR rate at each stage. Halt if crash rate > 1% or ANR rate > 0.5%.

#### Apple App Store

| Option | Purpose | Control |
|--------|---------|---------|
| **TestFlight (internal)** | Team testing | Up to 100 internal testers, no review |
| **TestFlight (external)** | Beta testing, requires beta review | Up to 10,000 testers |
| **Manual release** | Submit for review, release manually when ready | Full control of timing |
| **Automatic release** | Release immediately after review approval | Fastest |
| **Phased release** | Release over 7 days (1%, 2%, 5%, 10%, 20%, 50%, 100%) | Can pause or complete early |

**Phased release notes:** Unlike Google Play, Apple's phased release only affects auto-updates. Users who manually search can always download the latest version.

### Step 5: Post-Release Monitoring

| Metric | Target | Tool |
|--------|--------|------|
| **Crash-free rate** | > 99.5% (Google), > 99% (Apple) | Firebase Crashlytics, Sentry |
| **ANR rate** (Android) | < 0.5% | Google Play Console Vitals |
| **Hang rate** (iOS) | < 1% per hour | Xcode Organizer, MetricKit |
| **Store rating** | > 4.0 stars | Play Console / App Store Connect |
| **Review sentiment** | Monitor negative reviews within 24h of release | AppFollow, Appbot, or manual |
| **Uninstall rate** | No spike post-release | Play Console (Android only) |
| **Adoption rate** | > 50% within 7 days (if phased) | Store analytics |

**Rollback strategy:**
- **Google Play:** Halt staged rollout, then publish previous version as a new release or complete rollout of hotfix
- **App Store:** Cannot truly rollback — submit an expedited review for a hotfix. Can "remove from sale" in emergencies (nuclear option, removes app entirely)

### Step 6: Handle Review Rejections

| Platform | Common Rejection Reasons | Resolution |
|----------|------------------------|-----------|
| **Google Play** | Data Safety inaccuracy, missing privacy policy, deceptive behavior | Update declarations, fix compliance |
| **App Store** | Guideline 2.1 (crashes/bugs), 4.0 (design), 2.3 (metadata mismatch) | Fix issues, add review notes explaining functionality |
| **Both** | Permission overreach, missing feature (empty states) | Justify permissions, ensure all features work |

**Tips for smooth reviews:**
- Provide clear demo credentials in review notes (Apple)
- Explain non-obvious functionality in review notes
- Respond to rejections with specific changes made (don't just resubmit)
- For borderline cases, request a phone call with the review team (Apple App Review Board)

## Output Format

```markdown
## Release Summary
- **App:** [name]
- **Version:** [x.y.z (build)]
- **Stores:** [Google Play / App Store / Both]
- **Rollout:** [Full / Staged at X%]

## Pre-Submission Checklist
[Completed checklist with status]

## Store Listing
[Title, description, screenshots status]

## Rollout Plan
[Stage-by-stage plan with monitoring gates]

## Post-Release Monitoring
[Metrics to watch and thresholds for action]

## Rollback Plan
[What to do if something goes wrong]
```

## Quality Checklist

- [ ] Build is signed with correct production credentials
- [ ] Version and build number are correct and incremented
- [ ] Release notes are written and localized
- [ ] Privacy declarations match actual app behavior
- [ ] Store listing screenshots reflect current UI
- [ ] Staged rollout is configured (not 100% on day 1)
- [ ] Crash monitoring is active and alerting
- [ ] Rollback/hotfix procedure is documented
- [ ] Review notes include demo credentials (if login required)
- [ ] Post-release monitoring dashboard is set up

## Edge Cases

- If submitting to both stores simultaneously, account for Apple's review time (typically 24-48h) — submit to Apple first
- For apps in regulated industries (health, finance), expect longer review times and additional documentation requirements
- If your app uses background location, CallKit, HealthKit, or other sensitive APIs, prepare detailed justification for review
- For subscription apps, ensure pricing is consistent across stores and cancellation is clearly accessible
- If your app has been previously rejected, reference the rejection reason in review notes and explain what changed
- For apps targeting children (COPPA/GDPR-K), both stores have additional requirements — review Google Families Policy and Apple Kids Category guidelines
