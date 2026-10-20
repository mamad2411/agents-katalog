---
name: "budget-vs-actual"
description: "Budget vs actuals analysis: variance explanation, trend identification, reforecast recommendations"
---

# Budget vs Actual Skill

## When to activate
- Running monthly or quarterly budget vs. actuals (BvA) analysis
- Explaining variances to leadership, the board, or investors
- Identifying trends early to enable course correction
- Building a reforecast after significant variance from original budget
- Producing a management commentary section to accompany financial reports

## When NOT to use
- Audited financial statement preparation — requires a licensed accountant
- Tax computation — different adjustments apply, use a tax advisor
- Investor-facing prospectuses — regulated disclosure, requires legal review
- You have no budget baseline — run a financial planning session first (`/financial-plan`)

## IMPORTANT

All variance figures must carry a `[VERIFY]` marker until confirmed against source data. Management commentary is only as good as the data behind it — flag where estimates, accruals, or preliminary figures have been used.

## Instructions

### Core BvA analysis prompt

```
Run a budget vs. actuals analysis for [COMPANY] — [PERIOD: Month/Quarter/YTD].

Paste your data or provide these inputs:

REVENUE:
- Budget: $[X]
- Actual: $[X]
- Variance: $[X] ([X]% F/U) ← Claude will calculate if you provide budget + actual

COST OF REVENUE:
- Budget: $[X]
- Actual: $[X]

GROSS PROFIT:
- Budget: $[X]
- Actual: $[X]

OPEX BY LINE:
Sales & Marketing: Budget $[X] | Actual $[X]
R&D / Engineering: Budget $[X] | Actual $[X]
G&A: Budget $[X] | Actual $[X]
Other: Budget $[X] | Actual $[X]

EBITDA / OPERATING LOSS:
- Budget: $[X]
- Actual: $[X]

NET BURN (cash):
- Budget: $[X]
- Actual: $[X]

CONTEXT:
- Main reasons for variances (brief): [describe what you know]
- Any one-time items: [yes/no — describe]
- Prior month actuals (for trend): [optional]

Produce:
1. Variance summary table ($ and %)
2. Management commentary for each material variance (>5% or >$X threshold)
3. Trend analysis vs. prior period
4. Early warning signals
5. Reforecast recommendation
```

### Variance analysis framework

```typescript
type VarianceDirection = 'FAVORABLE' | 'UNFAVORABLE'

interface LineItemVariance {
  name: string
  budget: number
  actual: number
  variance: number            // actual - budget (negative = favorable for costs)
  variancePct: number         // variance / budget * 100
  direction: VarianceDirection
  material: boolean           // true if abs(variancePct) > threshold (usually 5-10%)
  explanation: string         // root cause
  oneTimeItem: boolean        // if true, adjust run-rate for reforecast
  forwardImplication: string  // what this means for next period
}

// CONVENTION:
// Revenue: positive variance = favorable (actual > budget = beat)
// Costs: negative variance = favorable (actual < budget = underspend)
// Use F (favorable) / U (unfavorable) notation in tables

// MATERIALITY THRESHOLDS (customise):
// Large company: >5% AND >$50K
// Startup: >10% OR >$10K
// Always flag any line that is >20% regardless of dollar amount
```

### Variance table generator

```
Generate a budget vs. actuals variance table for [PERIOD].

Format:

| Line Item | Budget | Actual | Variance $ | Variance % | F/U | Commentary |
|---|---|---|---|---|---|---|
| Revenue | $[X] | $[X] | $[X] | [X]% | F/U | [1-line explanation] |
| Cost of Revenue | $[X] | $[X] | $[X] | [X]% | F/U | [1-line explanation] |
| Gross Profit | $[X] | $[X] | $[X] | [X]% | F/U | — |
| **Gross Margin %** | [X]% | [X]% | [X]bps | — | F/U | — |
| Sales & Marketing | $[X] | $[X] | $[X] | [X]% | F/U | [1-line explanation] |
| R&D | $[X] | $[X] | $[X] | [X]% | F/U | [1-line explanation] |
| G&A | $[X] | $[X] | $[X] | [X]% | F/U | [1-line explanation] |
| EBITDA | $[X] | $[X] | $[X] | [X]% | F/U | — |
| Net Burn | $[X] | $[X] | $[X] | [X]% | F/U | — |

Rules:
- All $ in thousands (or millions if specified)
- Round to nearest $K
- Flag rows where |variance %| > [THRESHOLD]% with ⚠
- One-time items: add "(one-time)" to commentary
```

### Management commentary prompt

```
Write management commentary for the following material variances.

REVENUE VARIANCE — $[X]K [F/U] ([X]%):
Context: [what happened — e.g. 2 deals slipped, pricing change, churn, seasonal]
Write commentary that: explains the root cause, quantifies the driver, distinguishes
recurring vs. one-time, and notes the forward implication.

Format:
"Revenue came in at $[X]K, $[X]K [below/above] budget ([X]%). The primary driver was
[root cause]. [Quantification]. [One-time vs. structural]. [Forward implication]."

OPEX VARIANCE — [Line Item] — $[X]K [F/U] ([X]%):
Context: [e.g. hiring slower than planned, vendor contract delayed, one-time consultant fee]
Write commentary using the same format.

Rules for good management commentary:
- Specific, not vague ("three enterprise deals slipped" not "slower sales")
- Quantify each driver ("representing $180K of the $240K shortfall")
- Separate recurring from one-time items explicitly
- Include the forward implication (does this variance persist into next month?)
- Do not be defensive — describe what happened and what's being done
```

### Reforecast prompt

```
Build a reforecast based on BvA results.

Original full-year budget:
[Paste or describe original annual budget by line]

Year-to-date actuals ([X] months):
[Paste YTD actuals]

Key changes to assumptions:
1. Revenue: [e.g. Q1 shortfall of $X was timing only — no structural change]
2. Headcount: [e.g. 2 hires delayed from Q1 to Q2 — impact $X/month in cost timing]
3. One-time items: [e.g. $X restructuring charge not in original budget]
4. Market conditions: [any change to the underlying assumptions]

Produce:
- Revised full-year forecast by quarter
- Variance to original budget (how much has the full-year changed and why)
- Best case / base case / downside scenario (3 scenarios)
- Revised cash runway at each scenario
- Key assumptions that drive the range between scenarios

Format the output as a reforecast narrative + supporting table.
Mark all reforecast figures [VERIFY].
```

### Trend analysis prompt

```
Run a 6-month trend analysis.

Provide data for the last 6 months (or as many as available):
[Month 1]: Revenue $X, Gross Margin X%, Net Burn $X, [Key KPI] X
[Month 2]: ...
...
[Month 6]: ...

Analyse:
1. Revenue trajectory: is growth accelerating, stable, or decelerating?
   - Calculate MoM growth rates
   - Identify inflection points

2. Margin trend: is gross margin expanding, contracting, or stable?
   - Flag if gross margin compresses >2pp in a month — investigate COGS

3. Burn trend: is burn increasing or decreasing relative to revenue?
   - Calculate burn multiple each month: net burn / net new ARR
   - A burn multiple >2x indicates inefficient growth

4. Leading indicators to watch:
   - Pipeline / bookings trend (leading → revenue with X months lag)
   - New customer count trend
   - Churn rate trend

5. Early warnings:
   - Any metric that has moved in the wrong direction for 2+ consecutive months
   - Any single-month outlier that could distort the trend

Output: trend table + 3-sentence commentary per metric.
```

### CFO commentary template

```
Write the CFO financial summary for [PERIOD].

This 1-page section goes to the CEO, board, and investors. It must:
- Open with the headline verdict (on track, ahead, behind, and by how much)
- Cover: revenue, gross margin, burn, runway in one paragraph
- Explain the 2-3 most material variances in plain language
- State what the reforecast shows for the rest of the year
- End with any actions being taken and any decisions required

Length: 250-350 words. No bullet points — full sentences. Tone: direct, no spin.

Key figures:
[Paste your actual figures here]

Key variances to explain:
[List the 2-3 biggest variances and root causes]

Reforecast summary:
[What does the revised full-year look like?]
```

### Sensitivity analysis

```
Run sensitivity analysis on the reforecast.

Base case assumptions:
- Revenue growth rate: [X]% MoM
- Gross margin: [X]%
- Monthly burn: $[X]K
- Cash on hand: $[X]K

Sensitivity 1 — Revenue downside (10% below base):
- Revised monthly revenue: $[X]K
- Impact on annual revenue: $[X]K
- Impact on runway (extra months of burn at lower revenue): [X] months

Sensitivity 2 — Burn increase (hired 2 positions earlier than planned):
- Additional monthly burn: $[X]K
- Runway impact: [X] months less

Sensitivity 3 — Combined (revenue miss + burn increase):
- Most conservative scenario
- Minimum runway: [X] months
- Break-even threshold: at what revenue level does the company become self-sustaining?

Format as a tornado chart description + scenario table.
[VERIFY] all sensitivity outputs against actual financial model.
```

## Example

**User:** Run a BvA analysis. Revenue budget $500K, actual $435K. S&M budget $180K, actual $162K. R&D budget $210K, actual $218K. G&A budget $80K, actual $74K. Net burn budget $170K, actual $219K.

**Expected output:**
```markdown
# Budget vs Actuals — [Period]
[VERIFY all figures below]

## Variance Summary

| Line Item | Budget | Actual | Variance $ | Variance % | F/U |
|---|---|---|---|---|---|
| Revenue | $500K | $435K | ($65K) | (13.0%) | ⚠ U |
| Cost of Revenue | [needed] | [needed] | — | — | — |
| Gross Profit | [calculated] | [calculated] | — | — | — |
| Sales & Marketing | $180K | $162K | $18K | 10.0% | F |
| R&D | $210K | $218K | ($8K) | (3.8%) | U |
| G&A | $80K | $74K | $6K | 7.5% | F |
| Net Burn | $170K | $219K | ($49K) | (28.8%) | ⚠ U |

## Management Commentary

**Revenue — ($65K) | (13.0%) Unfavorable [VERIFY]**
Revenue came in at $435K against a $500K budget, a shortfall of $65K (13%). 
[Root cause needed from management — e.g. "Two enterprise deals totalling $55K slipped 
to next month, accounting for 85% of the miss. The remaining $10K reflects lower 
average deal sizes in the SMB segment."]
Forward implication: If slipped deals close in [next period], YTD revenue recovers. 
If structural, recommend $480K reforecast for next month.

**Net Burn — ($49K) | (28.8%) Unfavorable [VERIFY]**
Net burn of $219K exceeded budget by $49K. Despite opex savings in S&M ($18K F) 
and G&A ($6K F), the revenue shortfall of $65K drove the burn overage, with a 
partial offset from cost savings. Burn multiple: [net burn $219K / net new ARR — 
net new ARR figure needed to calculate].

**Sales & Marketing — $18K | 10.0% Favorable [VERIFY]**
S&M came in $18K below budget. Investigate whether this is: (a) planned events/campaigns 
delayed — cost timing, will hit next period; or (b) headcount vacancy — structural 
underspend. Distinguish before forecasting.

## Reforecast Flag
Given the revenue miss and elevated burn, a reforecast is recommended. 
Provide [next 6 months] pipeline and hiring plan for a full reforecast model.
```

---
