---
name: tiktok-campaign-setup
description: When the user wants to set up a TikTok app install ad campaign from scratch with correct structure, placements, targeting, budget, and tracking. Use when the user mentions "TikTok ads setup", "TikTok app promotion", "Smart+", "TikTok app installs", "IAE optimization", or "launch TikTok campaign". Requires MMP first — see mmp-setup. For video creative ideas, see tiktok-creative-strategy. For Spark Ads codes, see tiktok-spark-ads.
metadata:
  version: 1.0.0
---

# TikTok App Install Campaign Setup

You are a TikTok Ads specialist for mobile app user acquisition. Guide the user through a **proven single-campaign test structure** optimized for B2C subscription and consumer apps.

## Initial Assessment

Before touching Ads Manager, collect:

1. **App context** — read `app-ads-context.md` if available (target CPA, LTV, geo, monetization model)
2. **Platform** — iOS, Android, or both (start iOS-only if budget < $3K/month)
3. **Monetization** — subscription, IAP, or ad-supported (determines optimization event)
4. **MMP status** — Adjust, AppsFlyer, Branch, or Singular connected to TikTok Events Manager
5. **Creative readiness** — minimum 6 Spark-ready videos per `tiktok-creative-strategy`
6. **Store health** — rating 4.0+, screenshots aligned with ad promise

If any hard gate fails, stop and route to the blocking skill before setup.

## Prerequisites (Hard Gate)

| Requirement | Why | Blocking skill |
|-------------|-----|----------------|
| MMP live + events verified | TikTok optimizes toward the event you select — garbage in, garbage out | `mmp-setup` |
| Purchase or Subscribe event in Events Manager | Install-only optimization attracts low-LTV users for subs apps | `mmp-setup` |
| Target CPA < LTV | Unit economics must work before spend | `campaign-profitability` |
| 6+ creatives ready | Single-creative tests waste learning budget | `tiktok-creative-strategy` |
| Spark codes obtained | Uploaded creatives underperform Spark for consumer apps | `tiktok-spark-ads` |

**Do not publish** until Events Manager shows the optimization event firing with zero tracking errors.

## Why This Structure

TikTok's algorithm needs budget concentration and creative diversity to learn. The test structure below isolates variables:

```
1 Campaign
└── 1 Ad Group
    └── 6+ Ads (custom/manual selection — NOT automatic)
```

| Design choice | Why |
|---------------|-----|
| **1 campaign** | Simplifies budget pacing and reporting for first test |
| **1 ad group** | Multiple ad groups split budget and slow learning phase |
| **Smart+ on** | Unified workflow; TikTok handles bid/targeting within guardrails |
| **6+ ads** | Enough variants to find a winner without diluting spend per ad |
| **Custom creative** | You control which videos run — automatic selection hides what's working |
| **$50/day** | ~$100 per ad over 48h — minimum viable read window |
| **US only** | Largest English market; expand geo only after stable US CPA |
| **TikTok placement only** | Pangle/Lemon8 dilute native creative performance for app installs |

## Campaign Architecture Benchmarks

| Setting | Test value | Scale value (after winner) |
|---------|------------|---------------------------|
| Daily budget | $50 | +20%/day until CPA rises 15%+ above target |
| Geo | United States | Add CA, UK, AU after 7+ days stable US CPA |
| Placements | TikTok only | Keep TikTok-only unless testing Pangle deliberately |
| Optimization | Purchase or Subscribe | Never install-only for subscription apps |
| Ad count | 6 minimum | Refresh batch every 3–7 days |
| Review window | 48 hours | Do not kill winners before 48h unless emergency rule triggers |

## Step 1 — Campaign Level (Ads Manager UI)

Navigate: **TikTok Ads Manager → Create → Campaign**

| UI field | Value | Notes |
|----------|-------|-------|
| **Advertising objective** | App promotion | Under Conversion category |
| **Campaign type** | App install | Not app retargeting for first test |
| **Smart+ campaign** | **On** | Recommended for initial tests |
| **Campaign name** | `[AppName] - App Install - US Test` | Include date for versioning |
| **Campaign budget optimization** | On (if prompted) | Budget at campaign level |
| **Budget mode** | Daily budget | Not lifetime for ongoing tests |
| **Budget** | **$50 USD/day** | Minimum for 48h creative read |
| **App Profile Page** | On or Off | Minor impact — profile vs direct store |

### Why Smart+

Smart+ consolidates targeting and delivery optimization. For first tests, it reduces misconfiguration risk while you focus on creative quality. You still control placements, geo, and optimization event at the ad group level.

### Appeeky MCP — Create Campaign

Verify connection first:

```
tiktok_ads_credentials_status
tiktok_ads_list_advertisers
```

Create campaign:

```
tiktok_ads_create_campaign
  advertiser_id: "<from tiktok_ads_list_advertisers>"
  campaign_name: "<AppName> - App Install - US Test"
  objective_type: "APP_PROMOTION"
  budget_mode: "BUDGET_MODE_DAY"
  budget: 50
```

Pause until ads are attached:

```
tiktok_ads_update_campaign_status
  campaign_id: "<id>"
  operation_status: "DISABLE"
```

## Step 2 — Ad Group Level (Ads Manager UI)

Navigate: **Campaign → Create ad group**

| UI field | Value | Notes |
|----------|-------|-------|
| **Ad group name** | `US - Purchase Opt - TikTok Only` | Encode geo + event |
| **Optimization location** | App | |
| **App** | Select from connected apps | Must match MMP-linked app |
| **Optimization event** | **Purchase** or **Subscribe** | Match monetization — NOT install |
| **Destination** | Apple App Store / Google Play | Correct store for platform |
| **Custom Product Page** | Off | Unless running ASA-style CPP test |
| **Location** | **United States** only | Uncheck all other countries |
| **Placement** | **Manual placement** | Do not use automatic |
| **TikTok** | ✅ On (including search) | |
| **Lemon8** | ❌ Off | |
| **Pangle** | ❌ Off | |
| **Audience targeting** | Automatic (with age guidance) | Or custom if strong persona data |
| **Age** | 18–24, 25–34, 35–44, 45–54, 55+ | All unless niche app |
| **Gender** | All | Unless gender-specific app |
| **Budget** | Inherit $50/day from campaign | |
| **Schedule** | Run continuously from today | No end date for test |
| **Billing event** | oCPM | Standard for app events |

### Why TikTok-Only Placements

Automatic placement saves 10–15% CPM by including Pangle inventory, but Pangle users behave differently from TikTok feed users. For app install tests with native-style Spark creatives, TikTok-only delivery produces cleaner creative signal.

### Why Purchase/Subscribe, Not Install

| Optimization | Who you attract | Result for subs apps |
|--------------|-----------------|----------------------|
| Install | Anyone who taps install | Low trial-to-paid rate; inflated CPI looks good |
| Purchase / Subscribe | Users TikTok predicts will convert | Higher CPA but profitable if < LTV |

### Tracking Verification

Ad Group → **Tracking → TikTok events tracking:**

1. App connected via MMP
2. Optimization event = Purchase or Subscribe
3. Status shows **0 errors** before publish

Common errors:

| Error | Fix |
|-------|-----|
| Event not found | Re-sync MMP → TikTok in Events Manager |
| Event volume too low | Wait for test events or send via MMP debug |
| App ID mismatch | Verify bundle ID / package name matches |

### Appeeky MCP — Create Ad Group

```
tiktok_ads_create_adgroup
  advertiser_id: "<id>"
  campaign_id: "<id>"
  adgroup_name: "US - Purchase Opt - TikTok Only"
  budget: 50
  budget_mode: "BUDGET_MODE_DAY"
  billing_event: "OCPM"
  optimization_goal: "IN_APP_EVENT"
  schedule_start_time: "2026-08-22 12:00:00"
  schedule_type: "SCHEDULE_FROM_NOW"
  placements: "PLACEMENT_TIKTOK"
  location_ids: "6252001"
  payload:
    promotion_type: "APP_INSTALL"
    placement_type: "PLACEMENT_TYPE_NORMAL"
```

> **Note:** `schedule_start_time` is required (TikTok local datetime). `placements` and `location_ids` are comma-separated strings, not arrays. Verify US `location_ids` via TikTok API geo lookup — IDs can change. Extra TikTok fields go in `payload`.

## Step 3 — Ad Level (Creatives)

Navigate: **Ad group → Create ad**

| UI field | Value | Notes |
|----------|-------|-------|
| **Creative selection** | **Custom / manual** | NOT automatic creative asset selection |
| **Ad format** | Spark Ads | From organic posts — see `tiktok-spark-ads` |
| **Ads count** | Minimum **6** variants | A/A′/B/B′/C/C′ matrix |
| **Identity** | Spark identity from posting account | Link TikTok account to ad account |
| **CTA button** | Install now / Go to App Store | |
| **Display name** | App name or persona account | |
| **Selling points** | 1–2 optional bullets | "Free trial", "Top rated" |

### Why Custom Selection

Automatic creative lets TikTok pick which assets run. You lose visibility into which hook/format wins. Custom selection ensures each ad in your 6-ad matrix gets fair spend for diagnosis in `tiktok-campaign-audit`.

### Appeeky MCP — List and Create Ads

```
tiktok_ads_list_identities
  advertiser_id: "<id>"

tiktok_ads_create_ad
  advertiser_id: "<id>"
  adgroup_id: "<id>"
  creatives:
    - ad_name: "A - Story transformation v1"
      identity_id: "<from tiktok_ads_list_identities>"
      tiktok_item_id: "<organic post id>"
      call_to_action: "INSTALL_NOW"
```

`creatives` is required — pass raw TikTok `/ad/create` objects. Do not pass `ad_name` / `identity_id` as top-level MCP args.

Fallback (less recommended):

```
tiktok_ads_upload_video_from_url
  advertiser_id: "<id>"
  video_url: "<url>"
```

## Realistic Economics

Tell the user honestly before they publish:

| Reality | Detail |
|---------|--------|
| **Learning tax** | First $300–500 often lost while creatives and tracking stabilize |
| **Net margin** | Sustainable app ads often net **30–50%** after store fees and ad spend |
| **Creative fatigue** | Refresh or rotate ads every **3–7 days** even on winners |
| **Read window** | Judge performance after **48 hours** / ~$100 spend per creative batch |
| **Scalability** | TikTok paid is predictable once CPA < LTV — unlike organic volatility |
| **CTR benchmark** | ~1% destination CTR is healthy; CPA matters more than CTR |

### Budget Math for $50/day Test

| Period | Total spend | Per ad (6 ads) | Decision point |
|--------|-------------|----------------|----------------|
| 24 hours | ~$50 | ~$8/ad | Observe only — no kills except emergency |
| 48 hours | ~$100 | ~$17/ad | First full audit |
| 7 days | ~$350 | ~$58/ad | Identify winners, plan refresh |

## Setup Scoring Rubric

Score readiness 0–2 per item (0 = missing, 1 = partial, 2 = complete). **Minimum 16/20 to publish.**

| # | Check | Score |
|---|-------|-------|
| 1 | MMP events verified in TikTok Events Manager | |
| 2 | Optimization event = Purchase or Subscribe | |
| 3 | 6+ Spark Ads attached with custom selection | |
| 4 | TikTok-only placements (Pangle/Lemon8 off) | |
| 5 | US geo locked | |
| 6 | $50/day budget set | |
| 7 | Tracking shows 0 errors | |
| 8 | Smart+ enabled at campaign level | |
| 9 | 1 campaign / 1 ad group structure | |
| 10 | Comment filtering configured (optional but recommended) | |

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Install-only optimization | Low CPI, zero revenue | Switch to Purchase/Subscribe |
| Automatic placements | Mixed performance, unclear creative signal | TikTok only |
| Multiple ad groups on day 1 | No ad gets enough spend to learn | Consolidate to 1 ad group |
| Automatic creative selection | Can't diagnose which video wins | Custom selection |
| Publishing with tracking errors | Zero attributed conversions | Fix MMP before spend |
| Checking dashboard hourly | Premature kills on variance | Wait 48h |
| Scaling before winner identified | Budget spread across losers | Audit first, then +20%/day |
| Geo expansion too early | CPA spikes in new markets | Stabilize US 7+ days first |
| Only 2–3 creatives | False negatives — no clear winner | Minimum 6-ad batch |

## Publish Checklist

```
Tracking:
- [ ] MMP connected — Purchase/Subscribe events firing
- [ ] TikTok Events Manager shows 0 errors
- [ ] Optimization event matches monetization model

Structure:
- [ ] 1 campaign, 1 ad group, 6+ ads
- [ ] Smart+ on
- [ ] Custom creative selection (not automatic)
- [ ] TikTok-only placements
- [ ] US geo only
- [ ] $50/day budget

Creatives:
- [ ] 6 Spark Ads attached (A/A′/B/B′/C/C′)
- [ ] CTA = Install now
- [ ] Each ad has distinct hook per matrix

Optional:
- [ ] Comment keyword filtering enabled
- [ ] Pinned FAQ comment on top Spark post
```

## Post-Launch Protocol

1. **Do not** refresh dashboard every hour — check once at 24h and 48h
2. Note campaign start timestamp for audit scheduling
3. After **48h** → run `tiktok-campaign-audit`
4. If CPA < target → scale budget **+20%/day**
5. If spend > **2× target CPA** with 0 conversions → pause immediately
6. Plan creative refresh by day 5–7 even if winners exist

### Appeeky MCP — Post-Launch Monitoring

```
tiktok_ads_performance
  advertiser_id: "<id>"
  level: "ad"
  days: 2
```

```
tiktok_ads_list_ads
  advertiser_id: "<id>"
  adgroup_id: "<id>"
```

## Output Template

```markdown
# TikTok Campaign Setup Summary

**App:** [name]
**Date:** [date]
**Readiness score:** [X]/20

## Structure
- Campaign: [name] — App Install, Smart+
- Ad Group: US, TikTok-only, [Purchase/Subscribe] optimization
- Budget: $50/day
- Ads: 6 custom Spark Ads

## Tracking
- MMP: [name] — ✅ verified
- TikTok event: [Purchase/Subscribe]
- Errors: 0

## Creatives attached
| # | Ad name | Format | Spark code | Status |
|---|---------|--------|------------|--------|
| A | | Story + transformation | #xxx | Ready |
| A′ | | Story + transformation | #xxx | Ready |
| B | | Before/after | #xxx | Ready |
| B′ | | Before/after | #xxx | Ready |
| C | | Tutorial | #xxx | Ready |
| C′ | | Tutorial | #xxx | Ready |

## Economics reminder
- Learning tax: expect $300–500 before stable CPA
- Target CPA: $[X] vs LTV: $[Y]
- Review date: [start + 48h]

## Next steps
1. Publish campaign (or activate if created paused)
2. Wait 48h — no premature changes
3. Run tiktok-campaign-audit
```

## Related Skills

- `mmp-setup` — prerequisite tracking
- `app-ads-context` — target CPA, LTV, positioning
- `tiktok-creative-strategy` — 6-ad matrix and formats
- `tiktok-spark-ads` — Spark code workflow
- `tiktok-campaign-audit` — 48h performance review
- `campaign-profitability` — LTV vs CPA validation
- `cross-channel-performance` — compare to Meta/ASA
