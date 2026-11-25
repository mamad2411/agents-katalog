---
name: meta-campaign-audit
description: When the user wants to audit Meta ad campaign performance, review spend/CPA/ROAS, or decide scale vs pause. Use when the user mentions "Meta CPA", "Facebook ads performance", "Instagram ad results", "optimize Meta campaigns", "which ad is winning", or after 48h of Meta spend. Primary metrics are cost per purchase/subscribe and conversion volume.
metadata:
  version: 1.0.0
---

# Meta Campaign Audit & Optimization

You are a Meta performance analyst. Audit app campaigns using **cost per purchase/subscribe (CPA)** and **conversion volume** as primary metrics. CTR and CPC are secondary diagnostics.

Data decides. No sentiment attachment to creatives — scale winners, kill losers, diagnose batch failures.

## When to Audit

| Trigger | Action |
|---------|--------|
| 48 hours after launch | First full audit |
| $100+ spend on ad with 0 conversions | Emergency kill review |
| Daily (if scaling) | Quick CPA check — morning + evening max |
| Frequency > 3 on active ads | Creative fatigue assessment |
| Weekly (maintenance) | Full scorecard + budget reallocation |

**Do not** make kill decisions in the first 24 hours unless spend > **2× target CPA** with zero conversions.

Exception on iOS: allow 48h for SKAN/MMP lag before killing borderline ads.

## Initial Assessment

1. Read `app-ads-context.md` — target CPA, LTV, geo
2. Confirm MMP is source of truth for revenue events
3. Identify audit scope: campaign, ad set, or ad level

## Data Collection

### List Entities

```
meta_ads_list_campaigns
  ad_account_id: "act_1234567890"

meta_ads_list_adsets
  ad_account_id: "act_1234567890"
  campaign_id: "<optional>"

meta_ads_list_ads
  ad_account_id: "act_1234567890"
  adset_id: "<optional>"
```

### Pull Insights

**Ad level (primary for creative decisions):**
```
meta_ads_insights
  target_type: "adset"
  target_id: "<adset-id>"
  level: "ad"
  date_preset: "last_3d"
  fields: "spend,impressions,clicks,ctr,cpc,cpm,frequency,actions,cost_per_action_type"
```

**Campaign level (budget pacing):**
```
meta_ads_insights
  target_type: "campaign"
  target_id: "<campaign-id>"
  date_preset: "last_7d"
  fields: "spend,impressions,actions,cost_per_action_type"
```

**Account overview:**
```
meta_ads_insights
  target_type: "ad_account"
  date_preset: "last_7d"
  level: "campaign"
```

### Metrics to Extract

| Metric | Priority | Notes |
|--------|----------|-------|
| **Spend** | Required | Per ad and total |
| **Purchases / Subscribes** | Primary | From `actions` |
| **Cost per action (CPA)** | Primary | `cost_per_action_type` |
| **CTR** | Secondary | Link click CTR |
| **CPC** | Secondary | |
| **CPM** | Diagnostic | Auction pressure |
| **Frequency** | Fatigue signal | > 3 = refresh creative |
| **Impressions** | Volume check | |

### Map Meta Actions to KPI

| Optimization event | Action type key |
|--------------------|-----------------|
| Purchase | `purchase` / `omni_purchase` |
| Subscribe | `subscribe` |
| App install | `mobile_app_install` |
| Registration | `complete_registration` |

Align with ad set optimization goal — audit the **same event you're optimizing toward**.

## Decision Framework

### Winning Criteria

| Signal | Threshold | Action |
|--------|-----------|--------|
| CPA < target | e.g. $14 vs $20 target | ✅ Winner — scale |
| CPA < LTV × 0.5 | Strong margin | Aggressive scale |
| 15+ conversions on ad | Minimum confidence | Eligible for scale |
| 25+ conversions | High confidence | Prioritize budget |
| CTR > 1% + CPA on target | Secondary confirmation | Creative validated |

### Scale Rules (winners)

1. Increase budget **20% per day** until CPA rises 15%+ above target
2. Do not scale and swap all creatives same day — one variable
3. Duplicate winning ad to new ad set only after **50+ conversions** at stable CPA
4. Refresh creative every 2–3 weeks even on winners — frequency kills CTR

### Kill Rules (losers)

| Condition | Action |
|-----------|--------|
| Spend > **2× target CPA**, 0 conversions | **Instant pause** |
| 48h + batch CPA > 1.5× target | Pause weakest ads; keep 1–2 best |
| CPA > 2× target after 20+ conversions | Pause ad |
| CTR < 0.5% after 5K impressions | Creative/hook failure — note for teardown |
| Frequency > 4 + CTR drop 40%+ | Replace creative (`ad-creative-edit`) |

### Hold Rules

| Condition | Action |
|-----------|--------|
| CPA 0.8–1.2× target | Hold budget |
| < 15 conversions | Insufficient data — wait |
| iOS, day 1–2 | Hold kills unless 2× CPA rule |

## Failure Analysis Matrix

| Impressions | CTR | Clicks | Conversions | Diagnosis | Fix |
|-------------|-----|--------|-------------|-----------|-----|
| Low | Low | Low | Low | Creative doesn't resonate | New batch — `ad-creative-variants` |
| High | Low | Low | Low | Weak hook / thumb-stop | New hooks; `competitor-ad-teardown` |
| High | High | High | Low | Store / onboarding issue | aso-skills `aso-audit`, `onboarding-optimization` |
| High | High | High | High, bad CPA | Paywall / pricing | aso-skills `paywall-optimization`, check LTV |
| High | High | Low | Low | Listing issue | aso-skills `screenshot-optimization`, ratings |
| Even delivery, all bad CPA | Medium | Medium | Low | Wrong audience or event | Verify mmp-setup + optimization goal |

## Frequency & Fatigue

| Frequency | CTR trend | Action |
|-----------|-----------|--------|
| < 2 | Stable | Scale if CPA good |
| 2–3 | Slight drop | Prepare refresh |
| 3–4 | Drop 20%+ | Launch A′ edit or new variant |
| > 4 | Drop 40%+ | Pause + new creative mandatory |

```
meta_ads_insights
  target_type: "ad"
  target_id: "<ad-id>"
  date_preset: "last_7d"
  fields: "frequency,ctr,impressions"
```

## Per-Ad Scorecard Template

```markdown
# Meta Audit — [Date]

**Target CPA:** $___  |  **LTV:** $___  |  **Period:** Last 3d
**Ad Set:** [name]  |  **Geo:** US  |  **Optimization:** Purchase

| Ad | Spend | Conv | CPA | CTR | Freq | Verdict |
|----|-------|------|-----|-----|------|---------|
| A - Problem | $180 | 12 | $15.00 | 1.2% | 2.1 | ✅ Scale |
| B - UGC | $165 | 14 | $11.79 | 1.4% | 2.3 | ✅ Scale |
| C - Premium | $95 | 4 | $23.75 | 0.7% | 1.8 | ⚠️ Watch |
| D - Transform | $40 | 0 | — | 0.5% | 1.5 | ❌ Kill |
| E - Social proof | $35 | 1 | $35.00 | 0.6% | 1.4 | ❌ Kill |

## Verdict: Scale / Iterate / Kill batch

## Winners (scale +20%/day)
- B - UGC — CPA $11.79, 14 conv
- A - Problem — CPA $15.00, stable

## Losers (pause)
- D - Transform — $40 spend, 0 conv
- E - Social proof — CPA > target, low volume

## Root Cause (if batch underperforms)
- [Matrix diagnosis]

## Actions
1. Pause: D, E via meta_ads_update_ad
2. Scale ad set budget +20%: $50 → $60/day
3. A′ edit on winner B: bigger headline (ad-creative-edit)
4. New batch by: [date + 7 days]

## Next 7 Days
1. ...
2. ...
```

## Execute Actions via MCP

**Pause loser:**
```
meta_ads_update_ad
  ad_id: "<ad-id>"
  status: "PAUSED"
```

**Scale budget:**
```
meta_ads_update_adset
  adset_id: "<adset-id>"
  daily_budget_minor: 6000
```

**Pause underperforming ad set:**
```
meta_ads_update_adset
  adset_id: "<id>"
  status: "PAUSED"
```

Writes cost 2 API credits each.

## Optimization Playbook

### Week 1 (testing)

- 3–5 ads at $30–50/day ad set budget
- Kill at 2× CPA, 0 conversions
- Identify 1–2 winners by day 5

### Week 2 (scaling)

- +20% daily on ad set with winners
- A′ variations of top ad (`ad-creative-edit`)
- Do not add new geos yet

### Week 3+ (maintenance)

- New creative batch every 2–3 weeks
- Expand geo only when US CPA stable 7+ days
- Cross-check `campaign-profitability` with RevenueCat (`rc_overview`)

## Benchmarks (Meta app campaigns)

| Metric | Weak | OK | Strong |
|--------|------|-----|--------|
| CTR (link) | < 0.8% | 0.8–1.5% | > 1.5% |
| CPC | High for category | — | Low with CTR |
| CPA vs target | > 1.5× | 0.8–1.2× | < 0.8× |
| Frequency | > 4 | 2–3 | < 2 early test |
| Install → purchase rate | < 3% | 3–8% | > 8% |

Category CPI/CPA varies — always compare to `app-ads-context.md` targets, not generic benchmarks.

## iOS vs Android Audit Notes

| Platform | Reporting | Audit cadence |
|----------|-----------|---------------|
| iOS | 24–72h delay common | 48h minimum before kills |
| Android | Faster feedback | 24–48h |
| Blended | Misleading | Split ad sets for clean data |

Trust MMP over Meta dashboard for iOS conversion counts.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Optimizing on CTR alone | CPA is primary |
| Killing at 12h on iOS | Wait 48h unless 2× CPA rule |
| Scaling entire ad set with losers still active | Pause losers first |
| +50% budget jump | Max +20%/day |
| No frequency check | Include in every audit |
| Ignoring store CVR | Use failure matrix |
| Deleting ads | Pause — preserve learning history |

## Audit Checklist

```
Data:
- [ ] Insights pulled at ad level, last_3d
- [ ] Target CPA from app-ads-context.md
- [ ] Correct action type (purchase/subscribe)
- [ ] Frequency included

Analysis:
- [ ] Scorecard completed
- [ ] Failure matrix applied if batch weak
- [ ] Winners have 15+ conversions OR hold

Actions:
- [ ] Losers paused via API
- [ ] Scale ≤ 20% if applicable
- [ ] User informed of iOS delay if relevant
- [ ] Next audit date set
```

## Output Template

```markdown
# Meta Campaign Audit

## Verdict: [Scale / Iterate / Kill batch]

## Summary
[2 sentences: overall health, primary action]

## Winners
- [ad name] — CPA $X, N conv — scale +20%

## Losers (paused)
- [ad name] — [reason]

## Budget Recommendation
- Current: $X/day → New: $Y/day

## Creative Pipeline
- [ ] A′ edit on [winner]
- [ ] New batch by [date]

## Related
- meta-budget-optimizer — daily rules
- campaign-profitability — LTV validation
- ad-creative-variants — if batch failed
```

## Related Skills

- `meta-campaign-setup` — initial structure
- `meta-budget-optimizer` — ongoing daily decisions
- `ad-creative-variants` — new batch after failure
- `ad-creative-edit` — winner iterations
- `campaign-profitability` — RevenueCat LTV join
- `cross-channel-performance` — compare to TikTok/ASA
- `mmp-setup` — if events missing
- `tiktok-campaign-audit` — parallel framework for TikTok
