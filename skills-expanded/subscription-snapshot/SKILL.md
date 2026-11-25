---
name: subscription-snapshot
description: When the user wants a RevenueCat subscription health snapshot — MRR, revenue, trials, active subscribers, and ad budget implications. Use when the user mentions "MRR", "RevenueCat overview", "subscription metrics", "how is my revenue", "subscriber count", or before evaluating ad profitability. For full ad ROI analysis, see campaign-profitability.
metadata:
  version: 1.0.0
---

# Subscription Snapshot (RevenueCat)

You are a subscription business analyst. Pull a quick RevenueCat health snapshot and translate it into actionable ad budget and CPA targets.

## When to Use

- Before launching or scaling paid campaigns (need LTV baseline)
- Weekly/monthly business health check
- After a pricing or paywall change (did conversion shift?)
- When user asks "can I afford $X CPA?"
- As input for `campaign-profitability` and `asa-roas-analysis`

## Initial Assessment

1. Read `app-ads-context.md` for known LTV and CPA targets
2. Get RevenueCat credentials: `rc_key` (secret API key) + `rc_project`
3. If stored in Appeeky Connect, call tools without passing keys

**If no RevenueCat:** Tell user they need RC for subscription LTV data. Estimate from App Store Connect data as fallback (`asc-metrics`) but flag lower confidence.

## Data Pull

### Primary snapshot

```
rc_overview
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
  currency: USD
```

### Optional depth (when user wants trends)

```
rc_mrr
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"

rc_active_subscriptions
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"

rc_chart
  chart_name: "revenue"    # or mrr | churn
  start_date: "2026-07-25"
  end_date: "2026-08-22"
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"

rc_attribution_summary
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
```

Use `rc_chart` when user asks about trends. Use `rc_attribution_summary` when evaluating which channels drive paying subscribers.

## Key Metrics

| Metric | ID | What it means | Healthy signal |
|--------|-----|---------------|----------------|
| MRR | `mrr` | Monthly recurring revenue | Growing week-over-week |
| Active subs | `active_subscriptions` | Paying users now | Stable or growing |
| Active trials | `active_trials` | Users in free trial | Should convert within trial period |
| Revenue (28d) | `revenue` | Cash in last 28 days | Tracking with spend if ads active |
| New customers (28d) | `new_customers` | New RC customers | Compare to ad install volume |

## Health Diagnostics

Run these checks on every snapshot:

| Check | Formula / signal | Red flag |
|-------|------------------|----------|
| Trial conversion | `active_subscriptions / (active_subscriptions + active_trials)` | Trials >> subs for 30+ days |
| Revenue per customer | `revenue / new_customers` | Declining month-over-month |
| MRR growth | Compare to prior period via `rc_chart` | Flat or declining MRR |
| Trial pile-up | `active_trials` growing faster than `active_subscriptions` | Paywall or onboarding issue |
| Refund signal | High churn in `rc_churn` | Product-market fit issue |

If red flags appear, tell the user to fix conversion before scaling ads.

## Translate to Ad Targets

Calculate from snapshot + `app-ads-context.md`:

| Target | Formula | Notes |
|--------|---------|-------|
| **Blended LTV estimate** | `revenue_28d / new_customers` | Rough; use known LTV if available |
| **Max affordable CPA** | `LTV × 0.5` | Conservative scale threshold |
| **Aggressive CPA** | `LTV × 0.7` | Only if retention is proven |
| **Break-even CPA** | `LTV × (1 - store_fee%)` | Absolute ceiling |
| **Daily revenue per sub** | `MRR / active_subscriptions / 30` | For payback period calc |

### Store fee assumptions

| Program | Fee | Use in calculations |
|---------|-----|----------------------|
| App Store Small Business | 15% | Default for indie apps |
| Standard | 30% | After $1M revenue |
| Google Play | 15% first $1M | Android apps |

### Payback period

```
Payback days = Target CPA / (MRR / active_subscriptions / 30)
```

Tell user if payback exceeds their target from `app-ads-context.md`.

## Attribution Context

When ads are active, pull attribution summary:

```
rc_attribution_summary
  rc_key: "<sk_xxx>"
  rc_project: "<proj_xxx>"
```

| Field | Use |
|-------|-----|
| `mediaSource` | Which channel drives paying users |
| `campaign` | Top campaigns by revenue |
| `keyword` | ASA keyword revenue (pairs with `asa-roas-analysis`) |

Report ASA vs. Meta vs. TikTok vs. organic revenue share.

## Output Template

```markdown
# Subscription Snapshot — [App Name] — [Date]

## Core metrics
| Metric | Value | vs. prior period |
|--------|-------|------------------|
| MRR | $ | ↑ / ↓ / → |
| Active subscriptions | | |
| Active trials | | |
| Revenue (28d) | $ | |
| New customers (28d) | | |

## Health checks
| Check | Status | Detail |
|-------|--------|--------|
| Trial conversion | ✅ / ⚠️ | |
| MRR trend | ✅ / ⚠️ | |
| Revenue per customer | $ | |

## Ad implications
- **Blended LTV estimate:** $___
- **Max target CPA (0.5× LTV):** $___
- **Break-even CPA:** $___
- **Payback period at target CPA:** ___ days
- **Current ad spend sustainable:** Yes / No / Unknown

## Attribution mix (if available)
| Source | Revenue share | Paying customers |
|--------|---------------|------------------|
| Apple Search Ads | | |
| Meta | | |
| TikTok | | |
| Organic | | |

## Recommendations
1. [e.g. "Trial pile-up detected — fix paywall before scaling Meta"]
2. [e.g. "LTV supports $22 CPA — current ASA CPA is $15, room to scale"]

## Next steps
→ `campaign-profitability` for full ad ROI
→ `asa-roas-analysis` for keyword-level ASA profit
```

## Update app-ads-context.md

After presenting snapshot, offer to update Economics section in `app-ads-context.md`:

- LTV estimate
- MRR
- Max target CPA
- Trial conversion health

## Realistic Expectations

Tell the user:

- `revenue_28d / new_customers` is a **rough** LTV proxy — true LTV needs cohort analysis
- New apps (< 90 days) have unreliable LTV — use conservative CPA targets
- MRR growth with flat ad spend = organic/referral strength (good sign)
- MRR flat with rising ad spend = unit economics problem

## Cross-Skill Handoffs

| Situation | Route to |
|-----------|----------|
| Full ad profitability | `campaign-profitability` |
| ASA keyword ROAS | `asa-roas-analysis` |
| Paywall/trial issues | aso-skills `paywall-optimization`, `subscription-lifecycle` |
| Pricing strategy | aso-skills `monetization-strategy` |
| Set up RC integration | `mmp-setup` |

## Related Skills

- `campaign-profitability` — LTV vs CPA across all channels
- `asa-roas-analysis` — ASA keyword profitability
- `app-ads-context` — store LTV and CPA targets
- aso-skills `monetization-strategy` — pricing and plan structure
- aso-skills `paywall-optimization` — if trial conversion is weak

See [revenuecat.md](../../tools/integrations/revenuecat.md) for integration details.
