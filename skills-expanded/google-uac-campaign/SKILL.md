---
name: google-uac-campaign
description: When the user wants to set up Google Universal App Campaigns (UAC) for Android or iOS app installs. Use when the user mentions "Google UAC", "Google app campaigns", "Google Ads for apps", "Android paid installs", or "Google App Campaign". Framework guide — no Appeeky Google Ads API yet. For MMP setup, see mmp-setup. For budget allocation, see cross-channel-budget.
metadata:
  version: 1.0.0
---

# Google UAC Campaign Setup

You are a Google App Campaigns specialist. Guide the user through UAC setup, asset requirements, bidding strategy, and measurement — all via Google Ads UI since Appeeky has no Google Ads API integration yet.

## When to Use UAC

| Signal | UAC fit |
|--------|---------|
| Android-primary app | **Strong** — Google's native platform |
| iOS + broad audience | Medium — works but ASA usually outperforms |
| High search intent (utility) | Low — prefer ASA for iOS, UAC Search for Android |
| Visual consumer app | Medium — test after TikTok/Meta prove creative |
| Gaming | **Strong** — YouTube + Play Store distribution |
| Monthly budget < $1.5K | Weak — not enough for UAC learning phase |

Read `app-ads-context.md` for platform priority and budget.

## Prerequisites

Before UAC setup:

- [ ] App published on Google Play (Android) or App Store (iOS)
- [ ] MMP installed and verified (`mmp-setup`)
- [ ] Firebase project linked to Google Ads account
- [ ] Google Play Install Referrer API integrated (Android)
- [ ] In-app conversion events configured in Firebase
- [ ] Minimum $30–50/day budget for 7+ days

### Firebase ↔ Google Ads linking

1. Firebase Console → Project Settings → Integrations → Google Ads
2. Link Google Ads account
3. Import Firebase events as conversions in Google Ads
4. Set primary conversion: `in_app_purchase` or custom subscribe event

## Campaign Structure

```
App Campaign
├── Goal: **In-app actions** (Purchase / Subscribe) — not Installs
├── Bidding: Target CPA (after learning) or Maximize conversions
├── Budget: $30–50/day minimum
└── Asset groups
    ├── Videos (5+ required, 15–30s each)
    ├── Images (5+ required, 1200×1200 and 1200×628)
    ├── Headlines (5 required, 30 chars max)
    └── Descriptions (5 required, 90 chars max)
```

Google auto-mixes assets across Search, Display, YouTube, and Play Store. You don't control placement — **creative quality is everything**.

## Setup Steps

### Step 1 — Create campaign

1. Google Ads → New Campaign → App promotion
2. Select platform: Android (Play Store) or iOS (App Store)
3. Goal: **In-app actions** (not installs) if subscription/IAP app
4. Select conversion event: Purchase or Subscribe
5. Target locations and languages
6. Set daily budget

### Step 2 — Upload assets

| Asset type | Minimum | Specs | Tips |
|------------|---------|-------|------|
| Videos | 5 | 15–30s, landscape + portrait | Reuse TikTok winners |
| Images | 5 | 1200×1200, 1200×628 | Reuse Meta static ads |
| Headlines | 5 | 30 characters max | Lead with benefit, not app name |
| Descriptions | 5 | 90 characters max | Include social proof |
| HTML5 | Optional | Playable ads for games | Test if available |

**Google requires 20+ total assets** for optimal performance. More assets = more combinations tested.

### Step 3 — Bidding strategy

| Phase | Strategy | Duration |
|-------|----------|----------|
| Learning | Maximize conversions (no CPA target) | Days 1–7 |
| Optimization | Target CPA (set 20% above actual CPA) | Days 8–30 |
| Scale | Lower target CPA 10% every 7 days | Day 30+ |

**Do not set target CPA on day 1** — Google needs 50+ conversions to optimize.

### Step 4 — Verify tracking

1. Install app on test device from ad click
2. Complete conversion event
3. Check Firebase → Events (within minutes)
4. Check Google Ads → Conversions (within 24–48h)
5. Check MMP dashboard (within minutes)

## Asset Strategy

### Reuse from other channels

| Source | UAC asset type |
|--------|----------------|
| TikTok video winners | UAC video assets (reformat to 16:9 if needed) |
| Meta static ads | UAC image assets (1200×628) |
| App Store screenshots | UAC image assets (1200×1200) |
| App preview video | UAC video assets (trim to 30s) |

### Headline formulas

| Type | Example (30 chars max) |
|------|------------------------|
| Benefit | "Track Habits in 30 Sec" |
| Social proof | "1M+ Users Trust [App]" |
| Problem | "Stop Forgetting Tasks" |
| Feature | "AI Meal Plans Daily" |
| Urgency | "Free Trial — Start Now" |

Provide 5 headlines with different angles — Google tests combinations.

## Budget Guidelines

| Monthly budget | Daily budget | Expected learning period |
|----------------|-------------|-------------------------|
| $1,500 | $50/day | 14 days |
| $3,000 | $100/day | 7 days |
| $10,000 | $333/day | 5 days |

UAC needs **more learning time than TikTok** — judge at 7 days minimum, 14 days ideally. Do not run UAC below ~$1.5K/month ($50/day).

Include in `cross-channel-budget` allocation — typically 0% until social is proven; 5–10% only at $10K+.

## Measurement

| Source | What it tracks | Reliability |
|--------|----------------|-------------|
| Google Ads dashboard | Installs + in-app actions (Google-attributed) | High for Android |
| Firebase | All in-app events | Source of truth for events |
| MMP (AppsFlyer/Adjust) | Cross-channel attribution | Compare vs Google (10–20% discrepancy normal) |
| Play Console | Install source report | Android organic vs paid |

**Tell the user:** Google and MMP install counts will differ 10–20%. Use MMP for cross-channel comparison, Google for UAC optimization.

## Optimization Cadence

| Frequency | Action |
|-----------|--------|
| Day 3 | Check install volume — is campaign spending? |
| Day 7 | Review CPA/CPI, first asset performance |
| Day 14 | Replace bottom 2 assets, add 2 new variants |
| Day 30 | Set target CPA, evaluate ROAS |
| Monthly | Refresh 30% of assets, review geo performance |

### Asset performance signals

| Signal | Action |
|--------|--------|
| Low impressions on video | Google isn't serving it — replace |
| High impressions, low installs | Weak hook — replace video |
| One headline dominating | Add variations of that angle |
| CPA rising after 21 days | Creative fatigue — refresh assets |

## iOS UAC Notes

- Works but ASA almost always outperforms for iOS search intent
- Use UAC for YouTube/Display reach, not search intent
- SKAN applies — same delays as TikTok/Meta on iOS
- Budget priority: ASA first, then Meta/TikTok, then UAC

## Common Failures

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Campaign not spending | Too few assets or budget too low | Add assets, raise budget to $50/day |
| Installs but 0 in-app actions | Wrong conversion event | Link Firebase events to Google Ads |
| High CPI, low quality | Broad targeting by default | Switch to in-app action optimization |
| Google vs MMP mismatch > 30% | Attribution window difference | Normal; use MMP for cross-channel |
| Assets disapproved | Policy violation | Check text overlay, health claims |

## Output Template

```markdown
# Google UAC Setup Plan — [App Name]

## Prerequisites
- [ ] MMP verified
- [ ] Firebase linked to Google Ads
- [ ] Conversion events imported
- [ ] 20+ assets prepared

## Campaign config
- **Platform:** Android / iOS
- **Goal:** In-app actions → [event]
- **Daily budget:** $___
- **Bidding:** Maximize conversions (week 1) → Target CPA $___ (week 2+)
- **Geos:** [list]

## Asset inventory
| Type | Count | Source |
|------|-------|--------|
| Videos | | TikTok winners / new |
| Images | | Meta statics / screenshots |
| Headlines | 5 | [list] |
| Descriptions | 5 | [list] |

## Timeline
| Week | Action | Budget |
|------|--------|--------|
| 1 | Launch, maximize conversions | $/day |
| 2 | Review CPA, set target | $/day |
| 3–4 | Optimize assets, scale if profitable | $/day |

## Success criteria
- CPA < $___ by day 14
- 50+ conversions for target CPA bidding
- Add to `cross-channel-performance` at day 7
```

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| MMP not ready | `mmp-setup` |
| Budget allocation | `cross-channel-budget` |
| Performance review | `cross-channel-performance` |
| Profitability check | `campaign-profitability` |
| iOS search intent | aso-skills `apple-search-ads` (prefer ASA) |
| Creative assets | `tiktok-creative-strategy` or `meta-ad-creative` |

## Related Skills

- `mmp-setup` — attribution before UAC launch
- `cross-channel-budget` — include UAC in monthly plan
- `cross-channel-performance` — add UAC when running
- `campaign-profitability` — evaluate UAC ROAS
- `tiktok-campaign-setup` / `meta-campaign-setup` — social channels before UAC
