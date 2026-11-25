---
name: saas-growth-efficiency-metrics
description: Reference and formulas for 5 SaaS growth-efficiency metrics used in board/investor reporting — Magic Number, Rule of 40, Net Revenue Retention (NRR), LTV:CAC by channel, and CAC Payback Period — each with its formula, standard benchmark bands, common calculation traps, and the order to read all five together. Use when building a SaaS metrics dashboard, prepping a board deck, diagnosing whether growth spend is capital-efficient, or asked to explain/calculate Magic Number, Rule of 40, NRR, LTV:CAC, or CAC payback.
---

# SaaS Growth Efficiency Metrics

Source: reviewed from an uploaded SaaS metrics dashboard mockup — six
panels (Magic Number gauge, Rule of 40 stacked bar, Net Revenue Retention
waterfall, LTV:CAC scatter by channel, CAC Payback curve, and a summary
card). The panel layout and the specific benchmark thresholds shown
(0.5/0.75 Magic Number bands, 40% Rule of 40 line, 3:1/2:1 LTV:CAC lines,
<18-month CAC-payback mid-market target) are standard SaaS/VC convention,
reproduced here as a formula-plus-benchmark reference the way
`kpi-reference-handbook` does for general financial ratios. This skill
fills the SaaS-growth-specific gap that handbook doesn't cover — it isn't
a general 44-ratio library, it's the five numbers a SaaS board deck is
actually built around.

## 1. Magic Number

**Formula:** Net New ARR (current quarter, annualized) ÷ prior-quarter S&M
spend.

**Bands:** `<0.5` broken — S&M isn't converting; pause spend and fix
funnel/ICP before scaling. `0.5–0.75` fair — invest cautiously, dial in
before adding fuel. `>0.75` efficient — scale now, S&M is a reliable
lever.

**Trap:** must lag S&M spend by one quarter — this quarter's spend buys
next quarter's bookings, not this quarter's. Computing it same-quarter
misstates the ratio in either direction depending on sales-cycle length.

## 2. Rule of 40

**Formula:** Revenue growth rate % + profitability margin % (state which
margin — FCF margin or EBITDA margin; they are not interchangeable, and
switching which one feeds the sum between periods breaks the trend).

**Target:** the sum should be ≥ 40%.

**Trap:** the sum hides which lever is doing the work. A company can pass
at 60% growth / −20% margin (growth-stage, burning cash) or at 10% growth
/ 30% margin (profitability-stage, low growth) — always read growth % and
margin % as two separate lines (stacked bar, not a single number) so which
lever is carrying the score stays visible.

## 3. Net Revenue Retention (NRR)

**Formula:** (Starting ARR + Expansion − Contraction − Churn) ÷ Starting
ARR, expressed as a percentage.

**Bands:** `<100%` shrinking — losing more from the existing base than
expanding into it. `100–110%` healthy. `110–120%` strong. `120%+`
best-in-class (rare outside usage-based/land-and-expand pricing models).

**Presentation:** show as a waterfall — Starting ARR → Expansion → Churn →
Contraction → Ending ARR — never as a single blended percentage. A strong
headline NRR can hide a bad churn number under great expansion; the
waterfall makes both visible at once.

## 4. LTV:CAC by channel

**Formula:** Lifetime Value ÷ Customer Acquisition Cost, computed
**per channel** (cold outreach, Google Ads, LinkedIn Ads, events,
referral, inbound SEO, etc.) — never as one blended company-wide ratio.

**Bands:** `<2:1` kill zone — the channel destroys value net of
acquisition cost; cut it or fix the funnel. `2:1–3:1` breakeven-ish —
marginal, needs a specific reason to keep funding it. `>3:1` scale —
profitable to pour more budget in.

**Presentation:** a scatter plot (LTV on the Y axis, CAC on the X axis,
one bubble per channel, sized by spend) shows which channels are actually
working at a glance. A single blended CAC number hides exactly the
decision this metric exists to inform — which channels to cut and which
to scale.

## 5. CAC Payback Period

**Formula:** CAC ÷ (MRR per customer × Gross Margin %) — months until
gross profit from a customer repays the cost of acquiring them.

**Benchmark:** `<12 months` excellent. `12–18 months` healthy for
mid-market SaaS. `>18 months` a cash-efficiency problem regardless of how
good LTV:CAC looks on paper.

**Trap:** LTV:CAC can look fine on a long enough time horizon (say, a
5-year LTV window) while CAC payback quietly reveals the company runs out
of cash well before that horizon arrives. Never present LTV:CAC without
payback alongside it.

## Reading the five together — the actual board-review order

1. **Magic Number + Rule of 40 first** — the efficiency gate. If both are
   weak, don't move on to the rest yet; fix funnel/pricing/growth-vs-margin
   balance before optimizing anything downstream.
2. **NRR next** — is the existing customer base healthy. A strong Magic
   Number sitting on top of shrinking NRR is new-logo growth masking a
   leaky bucket.
3. **LTV:CAC by channel** — where efficient growth is actually coming
   from, so any budget reallocation targets the right channels.
4. **CAC Payback last** — the cash-timing check that catches problems
   ratio-based metrics (LTV:CAC) can miss entirely.

Treat a single quarter's snapshot of all five as a status check, not a
verdict — trend each metric over at least 3 quarters before acting on it;
a one-quarter dip in NRR from a single large churned account reads very
differently from a 4-quarter downtrend.

## Related skills in this repo

- **`kpi-reference-handbook`** — general financial-ratio reference across
  8 categories; this skill is the SaaS-growth-specific companion, not a
  replacement.
- **`growth-operating-framework`** — the 7-step *process* for
  capital-efficient growth; this skill is the numeric layer that steps 2
  (North Star metric) and 6 (capital efficiency) actually run on.
- **`business-intelligence-report`** / **`ceo-reporting-skill`** — use
  this skill's benchmark bands when a report needs to say whether a
  number is good, not just state it.
- **`saas-metrics-analyst`** (agent) — computes and flags all five from
  raw inputs.
- **`docs/procedures/saas-metrics-board-review.md`** — the review
  cadence/SOP.
- **`Artifacts/business/saas-growth-efficiency-dashboard.html`** — the
  live dashboard template built from this skill.
