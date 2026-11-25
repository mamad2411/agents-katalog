---
name: meta-campaign-setup
description: When the user wants to set up a Meta (Facebook/Instagram) app install ad campaign with correct structure, targeting, and tracking. Use when the user mentions "Meta ads setup", "Facebook app install", "Instagram app ads", "Meta app promotion", or "Facebook campaign structure". Requires mmp-setup first. For creative generation see meta-ad-creative or ad-creative-to-meta.
metadata:
  version: 1.0.0
---

# Meta App Install Campaign Setup

You are a Meta Ads specialist for mobile app UA. Set up **correct structure, tracking, and test budgets** before spending. Campaigns start PAUSED until user confirms.

Structure beats hacks. Wrong optimization goal or missing MMP events wastes the entire test budget.

## Initial Assessment

1. **`mmp-setup` complete** — Purchase/Subscribe firing in Meta Events Manager (last 7 days)
2. **`app-ads-context.md`** — target CPA, LTV, geo, monthly budget
3. **Meta OAuth** — `meta_ads_credentials_status` → connected. Then `meta_ads_list_advertisable_applications` + `meta_ads_list_pages`.
4. **Creatives ready** — minimum 3 via `meta-ad-creative` or `ad-creative-variants`

If any prerequisite fails, stop and resolve before creating campaigns.

## Account Structure

### Recommended Hierarchy

```
Ad Account
└── Campaign: [App] - App Promotion - [Geo]
    └── Ad Set: [Geo] - [Platform] - [Optimization event]
        ├── Ad: Creative A
        ├── Ad: Creative B
        ├── Ad: Creative C
        └── Ad: Creative D–E (optional)
```

### Budget Tier Structure

| Monthly budget | Campaigns | Ad sets | Creatives | Daily budget |
|----------------|-----------|---------|-----------|--------------|
| < $1.5K | 1 | 1 | 3 | $30–50 |
| $1.5K–10K | 1 | 2 (iOS/Android or geo) | 5 | $50–100 per set |
| $10K–50K | 1–2 per geo | 2–3 per campaign | 5–8 | Scale winners |
| $50K+ | Per geo + objective | LAL + broad | Continuous refresh | CBO at scale |

**First test:** One campaign, one ad set, 3–5 creatives. Do not over-segment before data.

## Campaign Level Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Objective | **App promotion** (`OUTCOME_APP_PROMOTION`) | Not Traffic or Engagement |
| Campaign budget (CBO) | Off for initial test | Enable after winner found |
| iOS 14+ | AEM + SKAN | Delayed reporting normal |
| Special ad categories | None unless regulated | Health, housing, credit |
| Status | **PAUSED** | Until user activates |

```
meta_ads_create_campaign
  ad_account_id: "act_1234567890"
  name: "FocusApp - App Installs - US"
  objective: "OUTCOME_APP_PROMOTION"
  status: "PAUSED"
  is_adset_budget_sharing_enabled: false
```

List existing campaigns:
```
meta_ads_list_campaigns
  ad_account_id: "act_1234567890"
```

## Ad Set Level Settings

| Setting | Test phase | Scale phase |
|---------|------------|-------------|
| Optimization | App event: **Purchase** or **Subscribe** | Same |
| Destination | `APP` (`destination_type`) | Same — never default `WEBSITE` |
| Billing | Impressions | Impressions |
| Bid strategy | Lowest cost (default) | Cost cap optional at scale |
| Daily budget | $30–50 minimum | +20%/day on winners |
| Geo | US (or primary market) | Expand after 7d stable CPA |
| Placements | **Advantage+ ON** | Meta handles placement mix |
| Age | 18–65+ or app-specific | Narrow if data supports |
| Gender | All unless category-specific | |
| Audience | **Broad** | LAL 1% after 100+ events |

```
meta_ads_create_adset
  ad_account_id: "act_1234567890"
  campaign_id: "<campaign-id>"
  name: "US - iOS - Purchase"
  daily_budget_minor: 5000
  billing_event: "IMPRESSIONS"
  optimization_goal: "OFFSITE_CONVERSIONS"
  destination_type: "APP"
  promoted_object: {
    "application_id": "<meta-app-id>",
    "object_store_url": "https://apps.apple.com/us/app/id123456789",
    "custom_event_type": "PURCHASE"
  }
  targeting: { "geo_locations": { "countries": ["US"] } }
  status: "PAUSED"
```

Use `SUBSCRIBE` if that is the primary MMP event.

### iOS vs Android Split

| Approach | When |
|----------|------|
| iOS only ad set | iOS-first app, limited budget |
| Android only ad set | Play-first or Android-primary |
| Separate ad sets | Budget > $3K/mo — cleaner CPA per platform |
| Combined | Tiny budget only — harder to diagnose |

### promoted_object Checklist

- [ ] `application_id` matches Events Manager app
- [ ] `object_store_url` is full store URL for correct platform
- [ ] `custom_event_type` is `PURCHASE` or `SUBSCRIBE` (not omitted)
- [ ] App SDK / MMP sending events to Meta

## Ad Level Settings

| Setting | Value |
|---------|-------|
| Creatives | 3–5 minimum (`ad-creative-variants`) |
| Format mix | Static required; add video if available |
| CTA | Install Now (`INSTALL_MOBILE_APP`) |
| Primary text | Benefit-first; hook in first 125 chars |
| Naming | `[App] - [Geo] - VarX - [Angle] - [date]` |

Use `ad-creative-to-meta` for automated creative + ad creation. Skip `meta_ads_create_app_install_draft` for subscription/IAP apps — it defaults to `APP_INSTALLS` and cannot set `custom_event_type`. Use campaign + ad set as above.

## Tracking Setup (critical)

### Events Manager Verification

Before launch, confirm in Meta Events Manager:

| Event | Source | Required for |
|-------|--------|--------------|
| App Install | MMP / SDK | Funnel baseline |
| Complete Registration | Optional | Activation campaigns |
| Purchase | MMP | Subscription apps |
| Subscribe | MMP | Subscription apps |
| Start Trial | MMP | Freemium subs |

### MMP → Meta Path

```
App → MMP (AppsFlyer/Adjust/Singular) → Meta partner integration
```

Skill: `mmp-setup`. Without this, optimization degrades to installs or link clicks.

### iOS ATT Expectations

| Phenomenon | Normal? | Action |
|------------|---------|--------|
| 24–48h conversion delay | Yes | Don't panic-pause |
| SKAN null conversions early | Yes | Trust MMP modeled data |
| Meta vs MMP CPA gap 20%+ | Common | Use MMP as source of truth |
| Zero events after 72h | No | Debug mmp-setup |

## Audience Strategy (phased)

### Phase 1 — Broad (days 1–14)

- No interest stacking
- Let creative + optimization find converters
- 3–5 creative variants

### Phase 2 — Lookalike (after 100+ purchase events)

| LAL % | Use |
|-------|-----|
| 1% | Highest quality scale |
| 1–3% | Expansion |
| 3–5% | Only if 1% CPA stable |

### Phase 3 — Interest stacks (optional)

Layer only after broad + LAL baseline. Interest targeting shrinks over time on Meta — creative matters more.

## Creative Requirements

| Asset | Spec | Source |
|-------|------|--------|
| Square static | 1024×1024 | `meta-ad-creative` |
| Vertical video | 9:16, 15–30s | Manual / TikTok pipeline |
| Primary text variants | 3–5 hooks | Appeeky copy |
| Refresh cadence | Every 2–3 weeks | Frequency > 3 |

## Launch Checklist

```
Prerequisites:
- [ ] mmp-setup — Purchase/Subscribe in last 7 days
- [ ] meta_ads_credentials_status connected
- [ ] Default ad account + Page set
- [ ] app-ads-context.md has target CPA

Campaign:
- [ ] Objective = App Promotion
- [ ] Status = PAUSED
- [ ] Naming convention applied

Ad set:
- [ ] Optimization = Purchase/Subscribe (not installs)
- [ ] `destination_type` = `APP`
- [ ] promoted_object correct
- [ ] Daily budget ≥ $30
- [ ] Geo matches launch plan
- [ ] Advantage+ placements ON

Ads:
- [ ] 3–5 creatives uploaded
- [ ] Copy reviewed for policy claims
- [ ] All ads PAUSED

User:
- [ ] Summary presented
- [ ] Explicit approval to activate
- [ ] 48h audit scheduled (meta-campaign-audit)
```

## Activation Sequence

Only after user confirms:

```
meta_ads_update_campaign
  campaign_id: "<id>"
  status: "ACTIVE"

meta_ads_update_adset
  adset_id: "<id>"
  status: "ACTIVE"

meta_ads_update_ad
  ad_id: "<id>"
  status: "ACTIVE"
```

## Output Template

```markdown
# Meta Campaign Setup — [App Name]

## Structure
| Level | Name | ID | Budget | Status |
|-------|------|-----|--------|--------|
| Campaign | | | — | PAUSED |
| Ad Set | | | $50/day | PAUSED |
| Ads | × N creatives | | — | PAUSED |

## Settings Summary
- **Objective:** App Promotion
- **Optimization:** Purchase
- **Geo:** US
- **Platform:** iOS
- **Placements:** Advantage+

## Tracking
- **MMP:** [AppsFlyer/Adjust/...]
- **Events verified:** Purchase ✅ / Subscribe ✅
- **Meta app ID:** [id]

## Creatives Attached
| Ad | Variant | Preview |
|----|---------|---------|
| | A - Problem | [url] |

## Target Economics
- **Target CPA:** $[X]
- **LTV:** $[X]
- **Test budget:** $[X]/day × 5 days = $[X]

## Before Go-Live
- [ ] User approved activation
- [ ] iOS reporting delay explained

## Post-Launch
- **48h:** meta-campaign-audit
- **Week 1:** meta-budget-optimizer daily
```

## Benchmarks (setup validation)

| Check | Pass | Fail — fix before launch |
|-------|------|------------------------|
| Events in last 7d | ≥ 1 purchase/sub | mmp-setup |
| Creatives count | ≥ 3 | ad-creative-variants |
| Daily budget | ≥ $30 | Raise or reduce variants |
| Optimization event | Purchase/Subscribe | Change ad set |
| Store URL | Opens correct app | Fix promoted_object |

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Traffic objective | Junk clicks | App Promotion only |
| Optimize for installs | Low LTV users | Purchase/Subscribe |
| One creative | No learning | 3–5 variants |
| Interest-heavy day 1 | Premature narrowing | Broad + creative test |
| Activating without MMP | Blind optimization | mmp-setup first |
| $10/day budget | No exit velocity | $30+ or fewer variants |
| Ignoring iOS delay | Premature pauses | Wait 48h |

## Common API Errors

| Error | Fix |
|-------|-----|
| OAuth expired | `meta_ads_oauth_start` |
| Invalid application_id | Register app in Events Manager |
| Budget below minimum | Increase `daily_budget_minor` |
| Policy review | Soften claims in primary text |

## Related Skills

- `mmp-setup` — prerequisite
- `app-ads-context` — economics and geo
- `meta-ad-creative` — static creative generation
- `ad-creative-variants` — test batch
- `ad-creative-to-meta` — automated pipeline
- `meta-campaign-audit` — 48h review
- `meta-budget-optimizer` — daily scale rules
- `competitor-ad-teardown` — angles before creative
- aso-skills `ua-campaign` — cross-channel UA strategy
