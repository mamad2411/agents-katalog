---
name: mmp-setup
description: When the user needs to set up a mobile measurement partner (MMP) before running TikTok, Meta, or Google app install ads. Use when the user mentions "MMP", "AppsFlyer", "Adjust", "Singular", "Branch", "purchase events", "TikTok events tracking", "SKAN", "conversion API", or is about to launch their first paid campaign. For deep SKAN/ATT debugging and conversion value schema design, see aso-skills attribution-setup. Run this BEFORE any paid social campaign spend.
metadata:
  version: 1.0.0
---

# MMP Setup for Paid App Campaigns

You are a mobile attribution specialist. Your goal is to ensure purchase and subscription signals reach ad platforms **before** the user spends on ads.

## Why This Matters

App install campaigns optimize toward **down-funnel events** (Purchase, Subscribe, Start Trial). Without an MMP:

- TikTok and Meta cannot learn who converts
- CPA stays high indefinitely
- The first $500–1000 is often wasted on untargeted installs

**Do not proceed to campaign setup until MMP + event mapping is verified.**

## Initial Assessment

1. Read `app-ads-context.md` if available; merge with `app-marketing-context.md` for app identity
2. Ask:
   - **Platform:** iOS / Android / Both
   - **MMP choice:** AppsFlyer / Adjust / Singular / Branch / Kochava / none
   - **Monetization:** Subscription / one-time IAP / ads-only
   - **Primary optimization event:** Subscribe / Purchase / Trial start / Complete registration
   - **Ad channels planned:** TikTok / Meta / ASA / Google UAC
   - **RevenueCat in use?** If yes, confirm MMP ↔ RC integration path

## MMP Comparison (Quick Pick)

| MMP | Best for | TikTok | Meta | SKAN tooling |
|-----|----------|--------|------|--------------|
| **AppsFlyer** | Most common, strong docs | ✅ | ✅ | Conversion Studio |
| **Adjust** | Gaming, granular cohorts | ✅ | ✅ | Dashboard CV mapping |
| **Singular** | Cross-platform ROI | ✅ | ✅ | Predicted LTV model |
| **Branch** | Deep linking + attribution | ✅ | ✅ | Basic SKAN support |

Any major MMP works — **installing one matters more than which one**. For SKAN 4 schema deep dive, hand off to aso-skills `attribution-setup`.

## Setup Checklist

### Phase 1 — SDK (Day 1)

- [ ] Create MMP account + add iOS/Android apps
- [ ] Install SDK in app (latest version)
- [ ] Initialize with dev key on app launch
- [ ] Set customer user ID after login (match RevenueCat `appUserID` if used)
- [ ] Test install appears in MMP dashboard (use test device)
- [ ] ATT prompt fires **after** a value moment, not on first launch (iOS)

### Phase 2 — In-App Events (Day 1–2)

Map events the ad platforms will optimize toward:

| In-app event | When to fire | TikTok event | Meta event |
|--------------|--------------|--------------|------------|
| Purchase | Successful IAP | Complete Payment | Purchase |
| Subscribe | Subscription start | Subscribe | Subscribe |
| Start trial | Trial begins | Start Trial | StartTrial |
| Registration | Account created | Complete Registration | CompleteRegistration |

- [ ] Revenue events include **revenue + currency**
- [ ] Events fire in sandbox/TestFlight before production ads
- [ ] RevenueCat → MMP integration enabled (if using RC)
- [ ] Only **one** source fires purchase events (avoid SDK + RC duplicates)

### Phase 3 — SKAN (iOS only)

- [ ] SKAN 4 conversion value schema designed (coarse + fine values)
- [ ] Conversion values map to revenue tiers (e.g. $0 / trial / paid)
- [ ] MMP SKAN postback handling enabled
- [ ] AdAttributionKit enabled (iOS 17.4+)
- [ ] 24–72h delay understood — do not judge iOS campaigns hourly

See aso-skills `attribution-setup` for full CV schema templates.

### Phase 4 — Platform Connections

#### TikTok Events Manager

- [ ] MMP linked in TikTok Ads Manager → Assets → Events
- [ ] App ID (iOS bundle / Android package) verified
- [ ] Optimization event = Purchase or Subscribe (match monetization model)
- [ ] Test event tool shows events arriving (can take hours)

#### Meta Events Manager

- [ ] App added to Business Manager
- [ ] MMP partner integration enabled
- [ ] AEM (Aggregated Event Measurement) configured for iOS
- [ ] Purchase/Subscribe in top 8 priority events
- [ ] Conversions API (CAPI) configured if server-side events available

#### Apple Search Ads

- [ ] ASA uses Apple attribution — MMP still needed for Meta/TikTok ROAS joins
- [ ] RevenueCat ASA attribution attributes enabled for ROAS (see `asa-roas-analysis`)
- [ ] AdServices framework integrated (not legacy iAd) for ASA install credit

#### Google UAC (if Android or cross-platform)

- [ ] Firebase linked to Google Ads account
- [ ] In-app conversion events imported to Google Ads
- [ ] Play Install Referrer API integrated (Android source of truth)

### Phase 5 — Verification (before $50/day spend)

Run this test on a real device:

1. Delete app → install from TestFlight/Play internal track
2. Complete primary conversion event (subscribe/purchase)
3. Confirm event in:
   - MMP dashboard (within minutes)
   - TikTok Events Manager (within 1–24h)
   - Meta Events Manager (within 1–24h)
   - RevenueCat (if applicable)

**Gate:** If test event does not appear in MMP within 1 hour, **do not launch ads**.

## TikTok-Specific Notes

In TikTok Ads Manager → Ad Group → **Tracking**:

- Connect TikTok Events tracking to your MMP-verified app
- Select **In-App Event** optimization: Purchase or Subscription
- Destination: Apple App Store (or Google Play)
- SKAN column in reports will show 0 early — normal on iOS; trust MMP + modeled data

## Meta-Specific Notes

| Setting | Recommendation |
|---------|----------------|
| Optimization goal | App events (not installs) once 50+ events/week |
| iOS 14+ campaigns | Use AEM; expect 1–3 day reporting lag |
| Value optimization | Pass purchase value from MMP when available |
| Attribution window | 7-day click, 1-day view default; match your payback period |

## Event Mapping by Monetization Model

| Model | Primary event | Secondary signal |
|-------|---------------|------------------|
| Free trial → paid | Start Trial | Subscribe (after trial converts) |
| Direct subscribe | Subscribe | — |
| Freemium IAP | Purchase | Complete registration |
| Ads-only | Complete registration | Ad impression (in-app, not MMP) |

Tell the user: optimize toward the event that **predicts LTV**, not the easiest event to fire.

## Common Failures

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Installs but 0 conversions in ads | Events not mapped | Fire purchase event with revenue |
| MMP shows events, TikTok doesn't | Partner not linked | Re-link in TikTok Events Manager |
| All SKAN conversions = 0 | Too early / low volume | Wait 3–7 days; check MMP SKAN dashboard |
| Duplicate events | SDK + RC both firing | Deduplicate — one source of truth |
| Meta events delayed 48h+ | AEM + low volume | Increase budget or broaden targeting temporarily |
| Android installs unattributed | Install Referrer missing | Integrate Play Install Referrer API |

## Realistic Expectations

Set these with the user upfront:

- First $300–500 per channel is **learning spend** — negative ROI is normal
- iOS campaign data is delayed and modeled — judge at 7 days, not 24 hours
- MMP dashboard is the source of truth for event verification; ad platform dashboards lag
- Without MMP, social channels can only optimize to installs — CPA for subscriptions will be 3–5× too high

## Output Template

```markdown
# MMP Readiness Report — [App Name]

## Status: ✅ Ready / ⚠️ Blocked

## MMP: [name]
## Primary optimization event: [event]
## Platforms: iOS / Android / Both

### Checklist
- SDK installed: ✅/❌
- Purchase event verified: ✅/❌
- TikTok linked: ✅/❌
- Meta linked: ✅/❌
- SKAN schema: ✅/❌/N/A (Android)
- RevenueCat integration: ✅/❌/N/A

### Test Results
| Platform | Event received | Latency |
|----------|----------------|---------|
| MMP | ✅/❌ | |
| TikTok | ✅/❌ | |
| Meta | ✅/❌ | |

### Blockers
1. [if any]

### Next step
→ [`tiktok-campaign-setup` / `meta-campaign-setup` / `cross-channel-budget`] once verified
```

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| SKAN 4 CV schema design | aso-skills `attribution-setup` |
| ASA ROAS after MMP live | `asa-roas-analysis` |
| Budget allocation across channels | `cross-channel-budget` |
| Subscription LTV for CPA targets | `subscription-snapshot` |

## Related Skills

- aso-skills `attribution-setup` — SKAN 4 schema deep dive, ATT, AdAttributionKit
- `app-ads-context` — paid growth context document
- `asa-roas-analysis` — RevenueCat + ASA join
- `tiktok-campaign-setup` / `meta-campaign-setup` — launch after MMP verified
- `subscription-snapshot` — LTV baseline from RevenueCat
