---
name: google-ads-budget-management
description: "When the user wants help with Google Ads budget pacing, monthly budget tracking, campaign budget allocation, shared budgets, budget forecasting, underspending or overspending campaigns, or how to distribute spend across campaigns to hit targets. Triggers on 'budget pacing', 'campaign budget', 'underspending', 'overspending', 'monthly budget target', 'shared budget', 'budget allocation', 'budget optimization', 'hit budget target', 'budget forecast', 'limited by budget', or 'how to allocate budget across campaigns'. For bid strategies and how they interact with budget see google-ads-bidding."
metadata:
  version: 1.0.0
---

# Google Ads — Budget Management & Pacing

You are a Google Ads budget specialist. Your goal is to ensure every campaign spends its budget on the highest-value opportunities — hitting monthly targets without overspending, reallocating from low-efficiency campaigns to high-efficiency ones, and keeping the algorithm out of budget-constrained learning mode.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. Account State
- Total monthly budget target across the account?
- Current month-to-date spend and days remaining in the month?
- How many campaigns? Are they all under the same budget authority?
- Any campaigns with fixed, immovable budgets (e.g., client contract for brand)?

### 2. Current Setup
- Are campaigns using individual daily budgets or shared budgets?
- What bid strategies are active? (Smart Bidding interacts with budget constraints differently than manual)
- Any campaigns showing "Limited by budget" in the status column?

### 3. Goals
- Pacing check: are we on track to hit monthly target?
- Reallocation: move spend from low-ROAS to high-ROAS campaigns?
- Fix underspending: campaign not spending its full budget?
- Fix overspending: campaign exceeding its target?

---

## How Google Ads Budgets Work

### Daily Budget vs Monthly Spend
Google can spend up to **2× your daily budget on any given day** to capture high-demand opportunities. However, Google guarantees your monthly spend will not exceed:
```
Daily budget × 30.4 (average days per month)
```

**Implication:** A $100/day budget is not strictly $100/day — Google will spend $40 one day and $160 the next based on traffic volume. Total monthly cap: ~$3,040.

**Important:** This is per campaign. Account-level budgets are managed through shared budgets or manual allocation — not an account cap.

### Budget Delivery Method
As of 2019, Google only offers **standard delivery** (default). Accelerated delivery was removed. Standard delivery spreads budget evenly across the day based on predicted traffic patterns.

### Budget Status Labels (what they mean)

| Status | Meaning | Action |
|--------|---------|--------|
| Limited by budget | Campaign hitting daily budget cap before day ends — leaving impressions on the table | Increase budget or improve efficiency |
| Eligible | Campaigns not hitting cap — potential underspend | Check bids, targeting, match types |
| Campaign paused | No spend | N/A |

---

## Pacing: Are You on Track?

### The Pacing Formula

```
Expected spend to date = (Monthly target / Days in month) × Days elapsed
Actual spend to date = Pull from account

Pacing ratio = Actual MTD spend / Expected MTD spend

> 1.0 = Overpacing (will overshoot target at current rate)
< 1.0 = Underpacing (will undershoot target at current rate)
```

### Projecting end-of-month spend

```
Projected monthly spend = (MTD spend / Days elapsed) × Days in month
```

**Example:**
- Monthly target: $50,000
- Day 12 of 31
- MTD spend: $17,500
- Daily run rate: $17,500 / 12 = $1,458/day
- Projected: $1,458 × 31 = $45,200 → **Underpacing by ~$4,800**

### What "on track" actually means

A flat run rate assumption is imperfect. Adjust for:
- **Weekday/weekend patterns:** B2B accounts often spend 20-30% less on weekends — don't panic on Monday morning
- **Month-end patterns:** Many accounts accelerate in the last week; early-month underpacing sometimes self-corrects
- **Seasonal modifiers:** If you know demand spikes in week 3, underpacing in week 1 may be intentional

---

## Budget Allocation: Where Should Each Dollar Go?

Budget allocation across campaigns is one of the highest-leverage decisions in an account. Moving $5,000/mo from a campaign with $80 CPA to one with $35 CPA generates nearly 100 more conversions at the same total spend.

### The Allocation Framework

**Step 1 — Rank campaigns by efficiency**
Pull 60-90 days of data. Sort by CPA (ascending) or ROAS (descending).

| Campaign | Spend/mo | CPA | Conversions | Is budget the constraint? |
|----------|----------|-----|-------------|--------------------------|
| Brand | $8,000 | $18 | 444 | No — impression share >90% |
| Non-Brand: Core | $15,000 | $32 | 468 | Yes — "limited by budget" |
| Non-Brand: Long Tail | $6,000 | $29 | 207 | No — 62% IS lost to rank |
| Competitor | $4,000 | $55 | 73 | No |
| Retargeting | $2,000 | $22 | 90 | No |
| Display | $5,000 | $90 | 55 | No |

**Step 2 — Identify marginal efficiency**
Which campaign would produce the most additional conversions for the next $1,000?
- Non-Brand Core: budget-constrained and efficient ($32 CPA) → highest priority
- Retargeting: $22 CPA but audience size naturally caps scale — limited upside
- Display: $90 CPA → lowest priority for incremental budget

**Step 3 — Reallocation decision**

Move budget from:
- Campaigns limited by audience size (brand campaign with 90%+ impression share can't absorb more)
- Low-efficiency campaigns (Display at $90 CPA when core Search is $32)

Move budget to:
- "Limited by budget" campaigns that have proven efficiency
- Campaigns with IS Lost to Budget > 20% and strong CPA

---

## Fixing Underspending

An underspending campaign is leaving potential conversions on the table. Before increasing budget, diagnose why.

### Common causes and fixes

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Bids too low for auction | Impression share lost to rank > 30% | Increase bids or improve QS |
| Targeting too narrow | Very small audience or geo | Expand match types, loosen geo or audience |
| Keyword volume too low | Low search volume keywords only | Expand keyword list, add broader match types |
| Smart Bidding in learning mode | Recent strategy or target change | Wait 2-4 weeks for learning to complete |
| Target CPA too aggressive | tCPA set below achievable level | Raise tCPA by 15-20%; let algorithm find volume |
| Target ROAS too aggressive | tROAS set above historical level | Lower tROAS target by 10-20% |
| Ad disapprovals | Ads not serving | Check Ads tab for disapprovals |
| Budget large but targeting small | Small geo or very niche audience | Broaden targeting before increasing budget further |

**Key rule:** Don't increase a campaign's budget to fix underspend — fix the underlying cause first. More budget into a constrained system doesn't produce more spend.

---

## Fixing Overspending

Overspending creates billing risk and budget shortfalls in other campaigns. It also means the campaign is spending beyond its efficient frontier.

### How overspending happens

1. Budget set too high relative to available inventory (less common with standard delivery)
2. Smart Bidding finding more conversion opportunities than the target allowed for (a good problem, but still overspend)
3. Month-end acceleration catching up

### Fixes

**Reduce daily budget:** The most direct lever. Recalculate the daily budget needed to hit monthly target:
```
Remaining daily budget = (Monthly target - MTD spend) / Remaining days in month
```

**Tighten bid strategy targets:** If Smart Bidding is aggressively spending because it's finding conversions, raise tCPA or lower tROAS slightly to reduce its bidding ceiling.

**Apply portfolio bid strategy with spend caps:** For accounts managing to strict monthly caps, a portfolio bid strategy with a campaign spend target enforces a hard monthly ceiling (available in some account types).

---

## Shared Budgets

Shared budgets pool a single budget across multiple campaigns. Google automatically allocates within the pool toward whichever campaign has the best opportunity at that moment.

### When shared budgets help

- Multiple campaigns with similar goals and fluctuating demand (e.g., 5 geographic campaigns that peak at different times)
- When you want Google to dynamically shift spend to the best performer within a group

### When shared budgets hurt

- When you need guaranteed minimums per campaign (Google may underspend a low-demand campaign)
- When campaigns have very different CPAs and you want to control allocation manually
- When one campaign would dominate the shared budget, starving others
- With Smart Bidding — each Smart Bidding campaign is already optimizing; shared budgets can conflict with the individual campaign's tCPA/tROAS targets

**Best practice:** Use shared budgets sparingly. Individual campaign budgets with active monitoring give more control and clearer performance attribution.

---

## Smart Bidding and Budget Interaction

This is the most commonly misunderstood relationship in Google Ads budget management.

### Budget constrains Smart Bidding learning

Smart Bidding needs volume to optimize. A campaign with a tCPA target that's also "limited by budget" is being starved of the learning data it needs. The algorithm can't find its optimal bid patterns if it's only entering 30% of available auctions.

**Rule:** If you're using Smart Bidding, don't constrain the campaign with a budget so tight it's perpetually "limited by budget." Either increase the budget or lower the tCPA/tROAS target to reduce spend per conversion.

### tCPA × budget = expected monthly conversions

A quick sanity check on whether a campaign budget is appropriately sized:
```
Expected daily conversions = Daily budget / tCPA target
Example: $200 daily budget / $40 tCPA = 5 conversions/day expected
```
If this number is below 1 conversion/day, Smart Bidding may not have enough signal to optimize effectively. Recommend either increasing budget or consolidating campaigns.

### Budget changes trigger learning

Increasing or decreasing daily budget by more than 20% can restart or extend the Smart Bidding learning period. For stable, optimized campaigns:
- Make budget changes in increments of 15-20% or less
- Avoid large changes in the days before a key performance period

---

## Budget Planning and Forecasting

### Monthly budget planning

**Step 1:** Pull the last 3 months of spend by campaign
**Step 2:** Calculate average daily spend per campaign
**Step 3:** Model next month adjusting for:
- Seasonal lift/decline (compare same month last year)
- Planned budget changes (new campaign launches, pauses)
- Upcoming promotions or events

**Step 4:** Sum to confirm total fits within monthly cap
**Step 5:** Set daily budgets = projected monthly / 30.4

### Seasonal budget allocation

Don't set and forget annual budgets. Build a budget calendar with adjustments:

| Period | Adjustment | Reason |
|--------|-----------|--------|
| Jan-Feb (post-holiday) | -10-15% | Demand typically lower |
| Q2 product launch | +25% | New traffic opportunity |
| Summer (B2B) | -10% | Decision-maker holidays |
| Q4 Oct-Nov (e-com) | +30-50% | Pre-holiday demand surge |
| Dec 25-Jan 1 | Campaign-specific | Varies dramatically by category |

---

## Optimization Checklist

### Weekly (10 min)
- [ ] Check MTD spend vs target — calculate pacing ratio
- [ ] Flag any campaign showing "limited by budget" — is the constraint intentional?
- [ ] Check for any unexpected spend surges (anomaly in daily spend)

### Monthly
- [ ] Recalculate daily budgets for new month based on targets
- [ ] Run allocation efficiency check — CPA/ROAS by campaign, reallocate bottom 20%
- [ ] Review shared budget pools — is allocation landing where intended?
- [ ] Check Smart Bidding campaigns: are any perpetually in learning mode due to budget?

### Quarterly
- [ ] Full budget audit — is spend distribution still aligned with business priorities?
- [ ] Seasonal adjustment planning for next 90 days
- [ ] Review if any campaigns' budget headroom has changed (new keywords, expanded geo)

---

## Common Mistakes

**Setting daily budgets in round numbers without pacing math**
"Let's set it at $500/day" without calculating whether $500 × 30.4 = $15,200 fits the monthly target. Always work backward from monthly targets.

**Reducing budget to fix a Smart Bidding underperformance issue**
If tCPA campaigns are over CPA target, reducing budget doesn't fix the targeting — it just slows the bleeding. Fix the tCPA target, campaign structure, or conversion tracking first.

**Using shared budgets across campaigns with very different CPAs**
A $200 CPA brand campaign and a $40 CPA non-brand campaign in the same shared budget pool will have Google allocate toward the campaign generating more conversions — usually the non-brand one. This may or may not be what you want, but it's rarely intentional.

**Making large budget changes on Smart Bidding campaigns**
A 3× budget increase triggers an extended learning period. The campaign may look like it's performing worse for 2-3 weeks. Plan large budget changes with enough lead time before any key performance period.

**Chasing monthly target with frantic end-of-month budget increases**
If you're 30% underpaced with 3 days left, tripling budgets won't get you there — the auction doesn't have enough volume. Budget realistically and accept that some months will underspend for structural reasons.

---

## Related Skills

- **google-ads-bidding**: Smart Bidding strategies and how they interact with budget constraints; tCPA/tROAS targets directly affect how much budget the algorithm will spend
- **google-ads-anomaly-detection**: Catching unexpected spend changes before they compound into major over/underspend
- **google-ads-scripts**: Automating budget pacing alerts and projections
- **google-ads-segmentation**: Geographic and device performance data informs intelligent budget reallocation
