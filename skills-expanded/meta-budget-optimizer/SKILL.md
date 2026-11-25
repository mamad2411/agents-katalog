---
name: meta-budget-optimizer
description: When the user wants to scale, pause, or reallocate Meta ad budget based on performance. Use when the user mentions "scale Meta ads", "increase Facebook budget", "pause underperforming Meta ads", "daily Meta optimization", or "budget rules for Facebook". For full diagnostics see meta-campaign-audit. For cross-channel moves see cross-channel-budget.
metadata:
  version: 1.0.0
---

# Meta Budget Optimizer

Daily and weekly **budget allocation rules** for Meta app campaigns. Apply after `meta-campaign-setup` launch and initial `meta-campaign-audit` at 48h.

Scale winners in small steps. Kill losers fast. Never let a bad ad eat 70% of spend unchecked.

## Initial Assessment

1. Read `app-ads-context.md` — target CPA, LTV, monthly cap
2. Confirm active campaigns via `meta_ads_list_campaigns`
3. Pull last 3 days ad-level insights before any change

## Core Rules Engine

| Condition | Confidence | Action |
|-----------|------------|--------|
| CPA < 0.8× target, 20+ conv | High | **+20% daily budget** |
| CPA 0.8–1.2× target | Medium | **Hold** budget |
| CPA 1.2–1.5× target, 15+ conv | Medium | Hold; watch 48h |
| CPA > 1.5× target, 15+ conv | High | **−20% budget** or pause weakest ad |
| Spend > 2× CPA, 0 conv | High | **Pause ad immediately** |
| Frequency > 3.5, CTR down 25%+ | Medium | **No scale** — add creative first |
| Ad set CPA < target, budget capped noon | High | Raise budget +20% |
| Campaign hits monthly cap | — | Reallocate from losers |

### Scale Increment Cap

**Never increase > 20% per day** on campaigns under $500/day — disrupts learning phase.

| Current daily budget | Max single increase |
|---------------------|---------------------|
| $30–100 | +20% ($6–20) |
| $100–500 | +20% |
| $500+ | +15–20% (test impact) |
| $2K+ | +10–15% optional cost cap test |

## Daily Workflow

### Step 1 — Pull Data

```
meta_ads_insights
  target_type: "ad_account"
  level: "ad"
  date_preset: "last_3d"
  fields: "spend,impressions,clicks,ctr,cpc,frequency,actions,cost_per_action_type"
  limit: 100
```

Or ad set scoped:
```
meta_ads_insights
  target_type: "adset"
  target_id: "<adset-id>"
  level: "ad"
  date_preset: "last_3d"
  fields: "spend,impressions,clicks,ctr,frequency,actions,cost_per_action_type"
```

### Step 2 — Rank Ads by CPA

Sort ads with ≥ 5 conversions by CPA ascending. Ads with 0 conversions: check spend vs 2× CPA kill rule first.

| Tier | Definition | Budget share target |
|------|------------|---------------------|
| S | CPA < 0.8× target | 50–70% of ad set spend |
| A | CPA 0.8–1.0× target | 20–30% |
| B | CPA 1.0–1.2× target | 10–20% hold |
| C | CPA > 1.2× target | Pause or min delivery |
| F | 0 conv, spend > 2× CPA | Pause |

### Step 3 — Apply Rules

Document each action before executing.

### Step 4 — Execute Updates

**Pause loser:**
```
meta_ads_update_ad
  ad_id: "<ad-id>"
  status: "PAUSED"
```

**Scale ad set:**
```
meta_ads_update_adset
  adset_id: "<adset-id>"
  daily_budget_minor: 6000
```

**Scale campaign (CBO only):**
```
meta_ads_update_campaign
  campaign_id: "<campaign-id>"
  daily_budget_minor: 15000
```

**Reduce budget:**
```
meta_ads_update_adset
  adset_id: "<adset-id>"
  daily_budget_minor: 4000
```

Writes: 2 Appeeky API credits each.

## Weekly Workflow

| Day | Action |
|-----|--------|
| Monday | Full audit — `meta-campaign-audit` scorecard |
| Tue–Thu | Daily optimizer (this skill) |
| Friday | Creative fatigue check; plan refresh |
| Weekend | Light check unless high spend |

### Weekly Reallocation

If running multiple ad sets:

1. Sum spend-weighted CPA per ad set
2. Shift 10–20% budget from worst quartile to best
3. Do not move > 20% total budget in one day

## Budget Cap Safety

### Monthly Pacing

```
Monthly cap from app-ads-context: $10,000
Days remaining: 12
Spend to date: $7,200
Remaining: $2,800 → max $233/day
```

If current run rate exceeds cap, reduce budgets proportionally — don't wait for month-end.

### Learning Phase Protection

| Situation | Rule |
|-----------|------|
| Ad set < 50 conversions total | Avoid > 20% budget changes |
| New creative added same day | Don't scale budget same day |
| Geo expansion launch | Start at test budget; don't scale 7d |

## Frequency Gate (no scale)

Before any scale action, check winner frequency:

```
meta_ads_insights
  target_type: "ad"
  target_id: "<winner-ad-id>"
  date_preset: "last_7d"
  fields: "frequency,ctr"
```

| Frequency | Scale? |
|-----------|--------|
| < 2.5 | Yes if CPA good |
| 2.5–3.5 | Scale cautiously (+10%) |
| > 3.5 | **No scale** — `ad-creative-edit` or new variant first |

## CBO vs ABO Strategy

| Mode | When | Optimizer focus |
|------|------|-----------------|
| ABO (ad set budget) | Testing phase | Per ad set rules |
| CBO (campaign budget) | 1+ proven ad sets | Campaign-level cap; pause bad ad sets |
| Hybrid | Scale phase | CBO on winners campaign; ABO on tests |

**Testing:** ABO — you control spend per test.
**Scaling:** CBO — Meta shifts to winners within campaign.

## Cross-Channel Rules

Pull comparison from `cross-channel-performance`:

| Condition | Action |
|-----------|--------|
| Meta CPA > TikTok CPA by 30%+ | Flag for `cross-channel-budget` |
| Meta ROAS best in portfolio | Protect Meta share |
| Meta CPA rising 3 days straight | Check creative fatigue before cut |
| ASA brand cheap, Meta broad expensive | Normal — different intent |

Do not slash Meta purely on CPA if LTV by channel differs — use `campaign-profitability`.

## Decision Log Template

```markdown
# Meta Budget Optimizer — [Date]

**Target CPA:** $20  |  **Period:** last_3d

## Actions Taken

| Entity | Before | After | Reason |
|--------|--------|-------|--------|
| Ad set US-iOS | $50/day | $60/day | CPA $14, 22 conv |
| Ad D - Transform | ACTIVE | PAUSED | $45 spend, 0 conv |
| Ad C - Premium | ACTIVE | ACTIVE | Hold — CPA $19, 8 conv |

## Ad Rankings

| Ad | Spend | Conv | CPA | Tier | Action |
|----|-------|------|-----|------|--------|
| B - UGC | $120 | 18 | $6.67 | S | Benefiting from scale |
| A - Problem | $95 | 12 | $7.92 | S | |
| C - Premium | $60 | 3 | $20.00 | B | Hold |
| D - Transform | $45 | 0 | — | F | Paused |

## Tomorrow
- [ ] Recheck C tier after 24h
- [ ] A′ creative on B if frequency > 3

## Monthly Pace
- Spend MTD: $X / $cap — on track / over
```

## Scenario Playbook

### Scenario: One ad dominates spend, good CPA

- **Action:** Allow — Meta found winner. Ensure losers paused if CPA bad.
- **Optional:** Duplicate winner to new ad set for incremental scale at 50+ conv.

### Scenario: All ads mediocre CPA (1.2–1.5×)

- **Action:** Hold budget. Run `ad-creative-edit` on best CTR ad.
- **Do not** scale hoping it fixes itself.

### Scenario: CPA spiked after scale

- **Action:** Revert last budget increase. Check frequency and creative age.
- **Rule:** If CPA > 1.3× target for 48h post-scale, roll back.

### Scenario: Budget spent by 2pm daily

- **Action:** +20% budget if CPA < target. If CPA bad, don't raise — delivery is telling you something.

### Scenario: iOS reporting lag

- **Action:** Use MMP CPA for decisions. Hold kills unless 2× CPA spend rule.

## Benchmarks

| Metric | Scale signal | Cut signal |
|--------|--------------|------------|
| CPA vs target | < 0.8× | > 1.5× |
| 3-day CPA trend | Flat or down | Up 25%+ |
| Frequency | < 3 | > 3.5 |
| Spend pacing | Even delivery | Front-loaded junk |
| Winner conv count | 20+ | < 5 (hold) |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| +50% budget day | Max +20% |
| Scaling with frequency 4 | Refresh creative first |
| Not pausing 0-conv ads | 2× CPA kill rule |
| Daily major restructures | One change type per day |
| Ignoring monthly cap | Pacing math weekly |
| CBO too early | ABO for tests first |
| Emotional creative loyalty | Data tier system |

## Pre-Flight Checklist

```
- [ ] last_3d insights pulled
- [ ] Target CPA from app-ads-context.md
- [ ] Losers identified (F tier)
- [ ] Frequency checked on scale candidates
- [ ] Budget increase ≤ 20%
- [ ] Monthly pace checked
- [ ] Actions logged for user
```

## Automation Cadence

| Spend level | Check frequency |
|-------------|-----------------|
| < $50/day | 1× daily |
| $50–200/day | 2× daily (morning, evening) |
| $200+/day | 2× daily + weekly audit |
| $1K+/day | Consider rules + human review |

**Don't hover hourly** — Meta delivery fluctuates intraday.

## Related Skills

- `meta-campaign-audit` — full diagnostic scorecard
- `meta-campaign-setup` — structure reference
- `ad-creative-edit` — fatigue refresh before scale
- `ad-creative-variants` — new batch when all tiers weak
- `campaign-profitability` — LTV-weighted decisions
- `cross-channel-budget` — reallocate vs TikTok/ASA
- `cross-channel-performance` — channel comparison data
- `app-ads-context` — caps and targets
