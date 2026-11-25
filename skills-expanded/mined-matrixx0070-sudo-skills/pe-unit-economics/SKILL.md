---
name: pe-unit-economics
version: 1.0.0
description: Analyze a target or portfolio company's unit economics — contribution margin, LTV, CAC, CAC payback, LTV:CAC, and cohort retention — to judge whether growth creates or destroys value and where the levers are.
author: matrixx0070
tags: [unit-economics, ltv-cac, contribution-margin, cohort-analysis, cac-payback, retention, private-equity]
capabilities: []
---

## When to use

Use this when the value of a business hinges on whether each customer (or unit) makes money and whether growth compounds or bleeds — recurring-revenue, subscription, marketplace, consumer, and transactional businesses especially. Reach for it in diligence to test a growth thesis (is this company buying unprofitable revenue?), or post-close to find the margin and retention levers that drive the value-creation plan. The output is a unit-economics assessment: contribution margin per unit, LTV, CAC and its payback, the LTV:CAC ratio, cohort retention curves, and a read on whether spending more to grow is accretive or dilutive — with the specific levers to fix it.

**Not for:** the broad go/no-go deal screen (use pe-deal-screening — unit economics is one input into it); the full diligence checklist across all workstreams (use pe-dd-checklist); modeling fund-level MOIC/IRR, leverage, and the entry/exit value-creation bridge (use pe-returns-analysis — unit economics feeds the revenue/margin assumptions but is not the returns model); building the whole value-creation plan (use pe-value-creation-plan — this sizes the growth/margin levers that plan executes); assessing AI-driven value (use pe-ai-readiness); writing the IC memo (use pe-ic-memo); origination (use pe-deal-sourcing); management-meeting prep (use pe-dd-meeting-prep); or ongoing KPI/covenant monitoring after close (use pe-portfolio-monitoring).

## Method

1. Define the "unit" and get clean inputs. Usually a customer or account; sometimes an order, seat, or location. Pull ARPA (average revenue per account, per period), gross/contribution margin, churn rate, and fully-loaded CAC. **Decision:** decide whether to measure on gross margin or true contribution margin (after variable service, support, and payment costs) — use contribution margin, because LTV built on gross margin overstates the real cash each customer returns.
2. Compute contribution margin per unit: revenue minus all variable costs to serve that unit. This is the foundation; every downstream metric inherits its accuracy.
3. Compute LTV. The standard form is `LTV = ARPA × gross (contribution) margin % ÷ churn rate`. Use the correct churn (customer vs revenue churn) and match the period (monthly churn → monthly ARPA, then the formula yields lifetime value directly). For businesses with net revenue retention above 100%, use the expansion-adjusted form (see Reference).
4. Compute CAC fully loaded: total sales *and* marketing spend (salaries, commissions, tooling, ad spend, overhead allocated) ÷ new customers acquired in the same period. **Decision:** insist on fully-loaded CAC — blended "marketing spend ÷ new customers" that omits sales headcount and commissions understates CAC and flatters the whole analysis.
5. Compute the two ratios that decide the verdict: `CAC payback (months) = CAC ÷ (ARPA × contribution margin %)` and `LTV:CAC = LTV ÷ CAC`. Benchmark against the rules of thumb (LTV:CAC ≥ 3; payback ≤ 12 months for SaaS — see Reference).
6. Build cohort retention curves. Group customers by acquisition period and track retained revenue over time. **Decision:** trust cohort-observed retention over a single blended churn number — blended churn hides a business where old cohorts are loyal but new cohorts churn fast (or vice versa), which changes the entire growth verdict.
7. Judge growth quality and name the levers. If LTV:CAC and payback are healthy and cohorts flat or expanding, growth is accretive — spending more to acquire creates value. If not, growth destroys value and must be fixed before scaled. Map the levers: raise ARPA (pricing/packaging), lift contribution margin (COGS/serve costs), cut churn (retention/onboarding), or lower CAC (channel mix/conversion) — and size each in cash.

## Example

A fund diligences a $30M-ARR B2B SaaS company growing 40%. Inputs: ARPA $12,000/yr, gross margin 80%, but true contribution margin 72% after support and payments; logo churn 18%/yr but net revenue retention 105% from expansion. Fully-loaded CAC (including the sales team and commissions the company had excluded) is $22,000, not the $9,000 marketing-only figure management quoted. On the honest numbers: LTV (expansion-adjusted) ≈ ARPA × contribution margin ÷ (churn − expansion) — with net retention above 100% the simple form breaks, so the team caps lifetime at a conservative 7 years → LTV ≈ $12,000 × 0.72 × 7 ≈ $60,480. LTV:CAC ≈ 60,480 ÷ 22,000 ≈ 2.75 (below the 3.0 bar). CAC payback = 22,000 ÷ (12,000 × 0.72) = 22,000 ÷ 8,640 ≈ 30 months — well over the 12-month benchmark. Cohorts reveal the real story: enterprise cohorts retain and expand strongly (payback ~14 months) while an SMB cohort churns at 35% with payback over 40 months. Verdict: growth is being subsidized by unprofitable SMB acquisition; the value-creation lever is to re-weight go-to-market toward enterprise and re-price or offboard SMB — modeled to move blended payback under 18 months and LTV:CAC above 3.5.

## Pitfalls

- **Using gross margin (or revenue) where contribution margin belongs.** LTV built on revenue or even gross margin overstates the cash each customer actually returns. Strip *all* variable serve costs first; the honest contribution margin is the foundation everything else stands on.
- **Blended CAC that hides the sales org.** "Ad spend ÷ new logos" ignores sales salaries, commissions, and tooling and can understate true CAC by 2–3x. Always use fully-loaded CAC, and separate blended CAC from paid/new-channel CAC.
- **A single churn number masking cohort divergence.** Blended churn can look fine while new cohorts churn fast and old ones prop up the average — or the reverse. Cohort curves, not one rate, tell you whether the business is getting better or worse at retention.
- **Mismatched periods and the wrong churn type.** Mixing monthly ARPA with annual churn, or using logo churn where revenue churn matters (or ignoring expansion/NRR), produces LTVs that are off by multiples. Match periods and pick the churn definition deliberately.
- **Reading LTV:CAC without payback.** A great LTV:CAC with a 30-month payback still means the business is cash-hungry and fragile to churn assumptions. Payback measures cash risk; the ratio measures long-run efficiency — you need both.

## Output format

```
# Unit Economics — <company> — <diligence | portfolio> — <date> — v<n>

## Unit definition & inputs
Unit: <customer/account/order>   Period: <monthly/annual>
ARPA <$> | Gross margin <%> | Contribution margin <%> | Churn (type) <%> | NRR <%> | Fully-loaded CAC <$>

## Core metrics
| Metric | Formula | Value | Benchmark | Pass? |
| Contribution margin / unit | Rev − variable serve costs | | | |
| LTV | ARPA × contrib margin ÷ churn | | | |
| CAC (fully loaded) | (S&M spend) ÷ new customers | | | |
| CAC payback (months) | CAC ÷ (ARPA × contrib margin) | | ≤12 (SaaS) | |
| LTV:CAC | LTV ÷ CAC | | ≥3 | |

## Cohort retention
| Cohort | M0 | M3 | M6 | M12 | M24 | Payback |
(retained revenue % by month since acquisition)

## Verdict
Growth quality: accretive | dilutive — <why>
Levers (sized in $): pricing/ARPA | contribution margin | churn/retention | CAC/channel
```

## Reference

Unit economics is how PE separates real, compounding growth from cash-burning growth. The formulas and benchmarks below are the standard ones; the discipline is in the input definitions.

### Core formulas

| Metric | Formula | Notes |
|--------|---------|-------|
| **Contribution margin (per unit)** | Revenue per unit − all variable costs to serve that unit | Foundation; use this, not gross margin, for LTV |
| **LTV** | `ARPA × gross (contribution) margin % ÷ churn rate` | Match the period; churn is the reciprocal of lifetime (1/churn = expected lifetime) |
| **LTV (expansion-adjusted)** | `ARPA × margin % ÷ (churn rate − expansion rate)` | For NRR > 100%; if churn ≤ expansion the series diverges — cap lifetime conservatively (e.g. 5–7 yrs) |
| **CAC** | `Total sales & marketing spend ÷ new customers acquired` (same period) | Fully loaded: salaries, commissions, tooling, ad spend, allocated overhead |
| **CAC payback (months)** | `CAC ÷ (ARPA_monthly × contribution margin %)` | Months to recover acquisition cost from gross-margin cash |
| **LTV:CAC ratio** | `LTV ÷ CAC` | The efficiency-of-growth headline number |

### Benchmarks (SaaS / recurring-revenue rules of thumb)

| Metric | Weak | Healthy | Strong |
|--------|------|---------|--------|
| **LTV:CAC** | < 3 | 3–5 | > 5 (may signal under-investment in growth) |
| **CAC payback** | > 18 mo | 12–18 mo | < 12 mo |
| **Gross margin (SaaS)** | < 70% | 70–80% | > 80% |
| **Net revenue retention (NRR)** | < 100% | 100–110% | > 120% |
| **Logo churn (annual, SMB→ent)** | > 20% | 10–20% | < 10% (enterprise: < 5%) |

A very high LTV:CAC is not automatically good — it can mean the company is under-spending on acquisition and leaving growth on the table. Read it with payback and growth rate.

### Churn definitions — pick deliberately

| Type | Measures | Use when |
|------|----------|----------|
| **Logo / customer churn** | % of *customers* lost | Homogeneous ARPA, count-based businesses |
| **Gross revenue churn** | % of *revenue* lost from churned/downgraded accounts | Revenue-weighted view; never exceeds 100% |
| **Net revenue retention (NRR)** | Revenue retained + expansion − churn/contraction | Expansion-heavy models; > 100% = negative net churn |

Using logo churn where revenue is concentrated (a few large accounts) will misstate LTV badly. Match churn type to how value concentrates.

### Cohort analysis — why the blended number lies

A cohort groups customers by acquisition period and tracks retained revenue (or logos) over subsequent months. Cohort curves reveal what a single blended churn rate hides:

- **Flattening curves** (retention stabilizes after early drop) = a healthy, sticky core — the business compounds.
- **Continuously declining curves** = no durable retention; growth must constantly replace churn (a leaky bucket).
- **Improving newer cohorts** = product/onboarding getting better; the future is brighter than the blend suggests.
- **Deteriorating newer cohorts** = the company is scaling acquisition into worse-fitting customers — a classic late-stage growth trap where headline growth masks a worsening engine.

Payback and LTV:CAC should be computed *per cohort or segment* where they diverge (e.g. enterprise vs SMB), because a blended verdict can approve a deal whose growth is actually being subsidized by an unprofitable segment.

### From unit economics to the value-creation levers

The four levers, and what each moves:

| Lever | Moves | Typical actions |
|-------|-------|-----------------|
| **ARPA ↑** | LTV ↑, payback ↓ | Pricing, packaging, upsell/cross-sell, remove discounting |
| **Contribution margin ↑** | LTV ↑, payback ↓ | COGS reduction, support automation, infra efficiency |
| **Churn ↓ / NRR ↑** | LTV ↑ (largest effect) | Onboarding, success motion, product stickiness, segment fit |
| **CAC ↓** | LTV:CAC ↑, payback ↓ | Channel-mix shift, conversion optimization, sales efficiency |

Churn/retention usually has the largest LTV leverage because LTV is inversely proportional to churn — halving churn can double LTV. Size each lever in cash so it feeds directly into the returns model and the value-creation plan.
