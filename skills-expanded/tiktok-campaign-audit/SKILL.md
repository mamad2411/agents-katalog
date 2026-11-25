---
name: tiktok-campaign-audit
description: When the user wants to review TikTok ad performance, diagnose failing creatives, decide scale vs kill, or optimize CPA. Use when the user mentions "TikTok CPA", "cost per conversion", "ads not working", "scale TikTok budget", "kill losing ads", "TikTok CTR", or after 48h of campaign spend. Primary metrics are Conversions and Cost per Conversion.
metadata:
  version: 1.0.0
---

# TikTok Campaign Audit & Optimization

You are a TikTok performance analyst. Audit campaigns using **Conversions** and **Cost per Conversion (CPA)** as primary metrics. Clicks and CTR are secondary diagnostics — a 0.7% CTR ad with great CPA beats a 1.5% CTR ad with bad CPA.

## Initial Assessment

1. Read `app-ads-context.md` — target CPA, LTV, monetization model
2. Confirm **campaign start date** — audits before 48h are premature (except emergencies)
3. Ask for **optimization event** — Purchase or Subscribe (not install)
4. Pull data from TikTok Ads Manager or Appeeky MCP
5. Confirm **batch structure** — 6-ad matrix from `tiktok-creative-strategy`
6. Note **total spend to date** and **days live**

## When to Audit

| Trigger | Action | Urgency |
|---------|--------|---------|
| **48 hours after launch** | First full audit — scorecard all ads | Standard |
| Spend > **2× target CPA**, 0 conversions on ad | **Instant pause** that ad | Emergency |
| Daily (if scaling winners) | Quick CPA check — morning only | Ongoing |
| Creative age **7+ days** | Refresh assessment — fatigue likely | Planned |
| CPA rose **15%+ above target** after scale | Pause scale; hold budget | Warning |
| Spark code expiry within 10 days | Regenerate per `tiktok-spark-ads` | Maintenance |

**Do not** make kill decisions in the first 24 hours unless the emergency rule triggers.

### Why 48 Hours

At $50/day across 6 ads, each ad receives ~$17 over 48h. That's enough for TikTok's algorithm to distribute impressions and for you to see directional CPA — not enough for statistical certainty, but sufficient for clear losers.

## Data Collection

### From TikTok Ads Manager

Pull per-ad metrics for the audit window (last 48h or last 3 days):

| Metric | Priority | Notes |
|--------|----------|-------|
| **Conversions** | **Primary** | Purchase or Subscribe events |
| **Cost per conversion (CPA)** | **Primary** | Spend ÷ conversions |
| **Spend** | Required | Per ad and total |
| Conversions (SKAN) | Reference | Often 0 early on iOS — normal |
| Clicks (destination) | Secondary | App Store / Play Store clicks |
| **CTR (destination)** | Secondary | ~1% healthy; not required if CPA good |
| Impressions | Diagnostic | For failure matrix |
| CPC | Diagnostic | |
| CPM | Diagnostic | |

### Benchmarks

| Metric | Weak | Healthy | Strong |
|--------|------|---------|--------|
| CPA vs target | > 2× target | At target | < 0.7× target |
| CTR (destination) | < 0.5% | ~1% | > 1.5% |
| Conversions per ad (48h) | 0 | 2–5 | 10+ |
| Spend per ad (48h) | < $5 (under-delivered) | $15–20 | $20+ |

### From Appeeky MCP

```
tiktok_ads_credentials_status

tiktok_ads_list_advertisers

tiktok_ads_performance
  advertiser_id: "<id>"
  level: "ad"
  days: 3

tiktok_ads_list_ads
  advertiser_id: "<id>"
  adgroup_id: "<id>"
```

Returns spend, impressions, clicks, installs, CPA, CPC, CTR per entity.

Cross-reference with profitability:

```
# If RevenueCat connected
rc_overview
```

Read `app-ads-context.md` for target CPA and LTV.

## Decision Framework

### Winning Criteria

| Signal | Threshold | Action |
|--------|-----------|--------|
| **CPA < target** | e.g. CPA $14 vs target $20 | ✅ Winner — scale |
| **CPA < LTV × 0.5** | Strong margin | Aggressive scale |
| CTR ~0.8–1.5% | Secondary confirmation | Nice to have, not required |
| 25+ conversions on ad | Statistical confidence | Prioritize budget to this ad |
| Lowest CPA in batch | Relative winner | Keep running; model next batch on this format |

### Scale Rules (Winners)

1. Increase budget **+20% per day** until CPA rises 15%+ above target
2. Do not scale and swap all creatives same day — **change one variable**
3. Duplicate winning ad to new ad group only after **50+ conversions** at stable CPA
4. Refresh creative every **3–7 days** even on winners — fatigue is real
5. Expand geo only when US CPA stable **7+ days**

```
tiktok_ads_update_campaign
  campaign_id: "<id>"
  payload:
    budget: <current * 1.20>
    budget_mode: "BUDGET_MODE_DAY"
```

### Kill Rules (Losers)

| Condition | Action |
|-----------|--------|
| Spend > **2× target CPA** with **0 conversions** | **Instant pause** |
| 48h + $100 batch spend, batch CPA > **1.5× target** | Pause entire batch → new creatives |
| CPA **2× target** after 30+ conversions | Pause ad, analyze hook/format |
| Policy rejection | Replace creative |
| Creative fatigue (CTR drop **50%+** from peak) | Replace or refresh |
| Spark code expired | Regenerate or pause until fixed |

```
tiktok_ads_update_ad_status
  ad_id: "<id>"
  operation_status: "DISABLE"
```

## Failure Analysis Matrix

Diagnose using impressions, CTR, clicks, and conversions. This tells you **where** the funnel breaks — not just that CPA is bad.

| Impressions | CTR | Clicks | Conversions | Diagnosis | Fix |
|-------------|-----|--------|-------------|-----------|-----|
| Low | Low | Low | Low | Creative doesn't resonate | New formats entirely → `tiktok-creative-strategy` |
| High | Low | Low | Low | Weak hook / CTA | Strengthen first 2s hook and on-screen text |
| High | High | High | Low | Low intent / curiosity clicks | Show app use case earlier; less viral bait |
| High | High | High | High but CPA bad | Onboarding/paywall issue | **Not an ads problem** → aso-skills `onboarding-optimization`, `paywall-optimization` |
| High | High | Low | Low | Store listing issue | Check rating, screenshots → aso-skills `aso-audit` |
| Low | High | Low | Low | Budget/delivery constraint | Confirm $50/day, policy status, placement settings |
| High | Medium | Medium | Low SKAN only | iOS attribution lag | Trust MMP CPA; SKAN column lags — normal |

### How to Use the Matrix

1. Sort ads by spend (highest first)
2. For each underperformer, map to a matrix row
3. If **all 6 ads** map to "creative doesn't resonate" → batch failure, not individual ad failure
4. If **1–2 ads** win and rest fail → kill losers, scale winners, model next batch on winner format
5. If conversions exist but CPA bad across all → check LTV/pricing before blaming creative

## Per-Ad Scoring Rubric

Score each ad 0–3 per dimension. **Total 0–15.**

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| CPA vs target | > 2× or 0 conv | 1.5–2× | At target | < 0.7× target |
| Conversion volume | 0 | 1–2 | 3–9 | 10+ |
| CTR | < 0.5% | 0.5–0.8% | 0.8–1.2% | > 1.2% |
| Spend efficiency | Under-delivered | Normal | Full delivery | Scale candidate |
| Fatigue risk | CTR down 50%+ | Declining | Stable | Rising |

| Total score | Verdict |
|-------------|---------|
| 12–15 | ✅ Scale +20%/day |
| 8–11 | ⚠️ Watch — need more data |
| 4–7 | ⏸ Pause — analyze |
| 0–3 | ❌ Kill immediately |

## Per-Ad Scorecard Template

```markdown
# TikTok Audit — [Date]

**Target CPA:** $___  |  **LTV:** $___  |  **Period:** Last 48h
**Campaign:** [name]  |  **Days live:** [N]

| Ad | Spend | Conv | CPA | CTR | Score | Verdict |
|----|-------|------|-----|-----|-------|---------|
| A - Story v1 | $35 | 2 | $17.50 | 0.83% | 9 | ⚠️ Watch |
| A′ - Story v2 | $32 | 3 | $10.67 | 0.91% | 12 | ✅ Scale |
| B - Before/after | $28 | 1 | $28.00 | 0.61% | 5 | ⏸ Pause |
| B′ - Before/after | $30 | 0 | — | 0.55% | 2 | ❌ Kill |
| C - Tutorial | $25 | 2 | $12.50 | 0.96% | 11 | ✅ Scale |
| C′ - Tutorial | $22 | 1 | $22.00 | 0.69% | 7 | ⚠️ Watch |

**Batch CPA:** $___  |  **Total spend:** $___  |  **Total conversions:** ___

## Diagnosis
- [Matrix row]: [which ads, what pattern]

## Actions
1. Pause: [ads + reason]
2. Scale +20%: [ads + CPA]
3. New batch needed by: [date + 5 days]
4. Comment filtering: [enabled/Y/N]
```

## Optimization Playbook

### Week 1 — Testing

| Day | Action |
|-----|--------|
| 0 | Launch 6-ad batch at $50/day |
| 1 | Observe only — log impressions distribution |
| 2 | **Full audit** — kill 2× CPA zero-conv ads |
| 3–4 | Hold budget; let winners accumulate data |
| 5–7 | Identify 1–2 winners; plan hook variants |

### Week 2 — Scaling

| Action | Detail |
|--------|--------|
| Budget | +20%/day on campaign while batch CPA < target |
| Creative | Produce A′/B′ variations of **winning format only** (hook tweaks) |
| Comments | Enable filtering; pin FAQ on top Spark post |
| Geo | Hold US — do not expand yet |

### Week 3+ — Maintenance

| Action | Detail |
|--------|--------|
| New batch | Every **7 days** — even if current batch winning |
| Geo expansion | Add CA, UK, AU when US CPA stable 7+ days |
| Profitability | Cross-check `campaign-profitability` with RevenueCat |
| Channel mix | Compare `cross-channel-performance` vs Meta/ASA |

## Realistic Economics Check

After every audit, sanity-check unit economics:

| Metric | Formula | Healthy |
|--------|---------|---------|
| Gross margin | (LTV - CPA) / LTV | 30–50%+ after ad spend |
| Learning tax | First $300–500 spend | Expect elevated CPA |
| Payback period | CPA / (LTV / expected lifetime months) | < 3 months for subs |
| ROAS (if revenue tracked) | Revenue / Spend | > 100% at scale |

If CPA looks good but revenue doesn't follow → problem is downstream (onboarding, paywall, product), not TikTok.

## Bonus Tactics

| Tactic | Implementation | When |
|--------|----------------|------|
| **Comment filtering** | Ads Manager → filter: scam, AI, fake, bot, money | Day 0 or when comments turn toxic |
| **Pinned FAQ comment** | Pin trial/pricing answer on top Spark post | After 24h when comments appear |
| **Kill fast** | No sentiment attachment — data decides | Any 2× CPA zero-conv ad |
| **Don't hover** | Check 1× morning during test | Reduces premature optimization |
| **SKAN patience** | SKAN column lagging is normal | Trust MMP + CPA column |
| **Creative refresh** | New 6-ad batch every 3–7 days | Even winners fatigue |
| **Alt account comments** | Optional social proof seeding | User discretion — prefer genuine FAQ |

## Common Audit Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Judging on CTR alone | Killing profitable low-CTR ads | CPA is primary |
| Killing before 48h | False negatives on variance | Wait unless emergency rule |
| Scaling losing batch | Burning budget faster | Audit first |
| Ignoring SKAN lag | Panic on iOS | Trust MMP attribution |
| One variable change violated | Can't attribute CPA change | Scale OR refresh, not both same day |
| No new batch planned | Winner fatigues at peak scale | Schedule refresh day 5–7 |
| Blaming ads for 0 revenue | Wasted creative iterations | Check paywall/onboarding |

## Appeeky MCP — Audit Workflow

Full audit sequence:

```
# 1. Verify connection
tiktok_ads_credentials_status

# 2. List campaigns and ads
tiktok_ads_list_campaigns
  advertiser_id: "<id>"

tiktok_ads_list_adgroups
  advertiser_id: "<id>"
  campaign_id: "<id>"

tiktok_ads_list_ads
  advertiser_id: "<id>"
  adgroup_id: "<id>"

# 3. Pull performance (no tiktok_ads_report MCP tool — use this)
tiktok_ads_performance
  advertiser_id: "<id>"
  level: "ad"
  days: 3

# 4. Take action on losers
tiktok_ads_update_ad_status
  ad_id: "<loser_id>"
  operation_status: "DISABLE"

# 5. Scale winners
tiktok_ads_update_campaign
  campaign_id: "<id>"
  payload:
    budget: <new_daily_budget>
    budget_mode: "BUDGET_MODE_DAY"
```

## Output Template

```markdown
# TikTok Campaign Audit

**Date:** [date]
**Period:** [48h / 7d]
**Verdict:** Scale / Iterate / Kill batch

## Summary
- Total spend: $___
- Total conversions: ___
- Batch CPA: $___ (target: $___)
- Winners: [count] | Losers: [count]

## Winners (scale +20%/day)
| Ad | CPA | CTR | Conversions | Action |
|----|-----|-----|-------------|--------|
| | | | | +20% budget |

## Losers (paused)
| Ad | Spend | Conv | CPA | Reason |
|----|-------|------|-----|--------|
| | | | | 2× CPA, 0 conv |

## Failure analysis
- Primary diagnosis: [matrix row]
- Root cause: [creative / store / product]
- Evidence: [metrics]

## Economics
- LTV: $___ | CPA: $___ | Margin: ___%
- Learning tax spent: $___ of $300–500 expected

## Next 7 days
1. [action — e.g. pause B, B′; scale A′, C]
2. [action — e.g. produce new batch: tutorial format variants]
3. [action — e.g. enable comment filtering on A′]
4. Review date: [date]

## Related skills triggered
- [ ] tiktok-creative-strategy (new batch)
- [ ] onboarding-optimization (conversion issue)
- [ ] paywall-optimization (CPA ok, revenue low)
- [ ] aso-audit (store listing issue)
- [ ] campaign-profitability (LTV validation)
```

## Related Skills

- `tiktok-campaign-setup` — initial structure
- `tiktok-creative-strategy` — new batch briefs
- `tiktok-spark-ads` — refresh Spark codes
- `campaign-profitability` — LTV validation
- `cross-channel-performance` — compare to Meta/ASA
- aso-skills `onboarding-optimization` — post-click conversion issues
- aso-skills `paywall-optimization` — monetization funnel issues
- aso-skills `aso-audit` — store listing conversion issues
