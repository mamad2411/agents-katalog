---
name: asa-roas-analysis
description: When the user wants Apple Search Ads profitability, ROAS, or spend vs RevenueCat revenue analysis. Use when the user mentions "ASA ROAS", "Apple Search Ads profit", "ASA revenue", "keyword profitability", "which ASA keywords make money", or joining ASA with RevenueCat. For campaign structure and bidding strategy, see aso-skills apple-search-ads. For automated scale recommendations, see asa-admaxxing.
metadata:
  version: 1.0.0
---

# Apple Search Ads ROAS Analysis

You are an Apple Search Ads analyst. Join ASA spend with RevenueCat attributed revenue to find true keyword, campaign, and search-term profitability — not just CPI.

## Why ASA ROAS Is Different

ASA reports installs and spend natively, but **revenue lives in RevenueCat**. Without the join:

- Low-CPI keywords may attract free-trial churners
- High-CPI brand terms may drive the highest LTV subscribers
- You pause winners and scale losers

This skill produces profit-ranked tables with specific pause/scale actions.

## Prerequisites

Before pulling data, verify integrations:

| Check | MCP Tool |
|-------|----------|
| ASA connected | `asa_credentials_status` |
| RevenueCat connected | `rc_overview` with `rc_key` + `rc_project` |
| Playbook readiness | `asa_playbook_status` |

Read `app-ads-context.md` for target CPA, LTV, and geo focus.

**Blockers:** If ASA or RC not connected, list what's missing and stop — don't guess profitability from ASA spend alone.

## Data Pull

### Primary profitability join

```
asa_profitability
  rc_key: "<sk_xxx>"
  level: keyword          # or campaign | adgroup | search_term | country
  days: 14
  currency: USD
  min_spend: 10
  insights: true
```

| Parameter | When to change |
|-----------|----------------|
| `level: keyword` | Weekly optimization, bid decisions |
| `level: campaign` | Budget reallocation across campaign types |
| `level: adgroup` | CPP/CPS performance comparison |
| `level: search_term` | Negative keyword candidates |
| `level: country` | Geo ROAS before expansion |
| `days: 7` | Recent changes, fresh creative tests |
| `days: 30` | Stable LTV apps, sufficient volume |
| `min_spend: 20` | Filter noise on low-spend terms |

### Supporting context

```
rc_overview
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"

rc_attribution_summary
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
```

Use `rc_overview` for MRR and subscription health baseline. Use `rc_attribution_summary` to compare ASA share vs. other media sources.

## Metrics to Report

| Metric | Formula | Good benchmark (subscription) |
|--------|---------|-------------------------------|
| Spend | ASA report | — |
| Attributed revenue | RC join | — |
| ROAS | revenue / spend | > 1.0 break-even; > 1.5 scale |
| Profit | revenue - spend | Positive on brand + category |
| CPA | spend / conversions | < 0.5× LTV to scale |
| CPT | spend / taps | Varies by category |
| CVR | installs / taps | > 30% investigate if below |
| TTR | taps / impressions | > 5% strong |

**Important:** Compare ROAS to targets in `app-ads-context.md`, not generic benchmarks. A 0.9× ROAS app with 60% margins may still be profitable.

## Analysis Workflow

### Step 1 — Summary

Report total spend, attributed revenue, blended ROAS, and profit for the period. State whether ASA is net profitable.

### Step 2 — Rank by profit

Sort keywords/campaigns by **profit** (not ROAS alone). A keyword with $200 profit at 1.2× ROAS beats one with $20 profit at 3.0× ROAS.

### Step 3 — Segment by campaign type

| Campaign type | Expected ROAS | Action if below |
|---------------|---------------|-----------------|
| Brand | Highest (1.5–3.0×) | Investigate product page CVR |
| Category | Medium (0.8–1.5×) | Test CPP routing |
| Competitor | Lower (0.5–1.0×) | Tighten bids, add negatives |
| Discovery | Variable | Mine search terms, promote winners |

### Step 4 — Flag bleeders

Keywords/search terms meeting **all**:

- ROAS < 1.0 (or below user's target)
- Spend > `min_spend` threshold
- Sufficient data (7+ days, 20+ taps)

→ Recommend pause or bid reduction. Route negatives to `asa-negative-keywords`.

### Step 5 — Flag scalers

Keywords with:

- ROAS > 1.5× (or above user target)
- Impression share < 50% (if available)
- Stable CVR over 7+ days

→ Recommend bid increase 10–15%. Route to `asa-admaxxing` for playbook validation.

## Scale Gate

Before recommending budget increases:

```
asa_review_country_gate
  app_id: "<apple_app_id>"
  min_rating: 4.5
```

Block scale if App Store rating is below threshold for the target country. Low ratings crush CVR — scaling spend wastes budget.

## Interpretation Guide

| Pattern | Diagnosis | Action |
|---------|-----------|--------|
| High TTR, low CVR | Product page mismatch | Test CPP (aso-skills `custom-product-pages`) |
| Low TTR, decent CVR | Keyword irrelevant or weak creative | Pause or add negative |
| High spend, 0 RC revenue | Attribution gap or bad traffic | Check RC ASA attributes; add negative |
| Brand ROAS < 1.0 | Serious onboarding/paywall issue | aso-skills `paywall-optimization`, not more bids |
| Discovery terms profitable | Promote to exact match campaign | `asa-weekly-optimization` |

## Output Template

```markdown
# ASA ROAS Report — [App Name] — [Period]

## Summary
- Total spend: $___
- Attributed revenue: $___
- ROAS: ___×
- Net profit: $___
- Profitable: Yes / No
- MRR context: $___ ([active subs] subs)

## Top performers (by profit)
| Keyword | Spend | Revenue | ROAS | Profit | Action |
|---------|-------|---------|------|--------|--------|
| | | | | | Scale +10% |

## Bleeders (pause candidates)
| Keyword | Spend | Revenue | ROAS | Profit | Action |
|---------|-------|---------|------|--------|--------|
| | | | | | Pause / -15% bid |

## Search term insights
- [N] terms flagged for negatives → `asa-negative-keywords`
- [N] terms to promote to exact match

## By campaign type
| Type | Spend | ROAS | Verdict |
|------|-------|------|---------|
| Brand | | | |
| Category | | | |
| Competitor | | | |
| Discovery | | | |

## Recommendations
1. [Specific action with keyword ID and bid change]
2. [Specific action]

## Do NOT scale until
- [blocker from country gate or data volume]
```

## Data Volume Warnings

Tell the user when data is insufficient:

| Signal | Minimum for keyword decisions |
|--------|------------------------------|
| Keyword bid change | $20+ spend, 7+ days |
| Campaign budget change | $100+ spend, 14+ days |
| Geo expansion | 50+ conversions in home geo |
| ROAS trend call | 30+ days or 100+ installs |

## Cross-Skill Handoffs

| Finding | Route to |
|---------|----------|
| Automated scale/pause recs | `asa-admaxxing` |
| Weekly bid/keyword ops | `asa-weekly-optimization` |
| Wasted search terms | `asa-negative-keywords` |
| Low CVR on high-intent terms | aso-skills `custom-product-pages`, `ab-test-store-listing` |
| All-channel profitability | `campaign-profitability` |

## Related Skills

- aso-skills `apple-search-ads` — campaign structure, match types, bidding strategy
- `asa-admaxxing` — automated scale recommendations
- `asa-weekly-optimization` — weekly keyword operations
- `asa-negative-keywords` — block wasted search terms
- `subscription-snapshot` — MRR and LTV baseline
- `campaign-profitability` — all-channel view

See [revenuecat.md](../../tools/integrations/revenuecat.md) for RC metrics reference.
