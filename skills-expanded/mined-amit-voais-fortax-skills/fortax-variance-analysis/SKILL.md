---
name: fortax-variance-analysis
description: Explain the movement between two periods, or budget vs actual vs forecast, line by line with the reason for each - price / volume / mix decomposition, headcount and salary variances, expense-category analysis, materiality thresholds, narratives that name the driver, text or Excel waterfall bridges, forecast accuracy and trends. For MIS reviews, audit analytical procedures, the Schedule III ratio note (reasons for change over 25%) and bank / investor questions. Typical asks - "variance analysis karo", "last year se kya badla aur kyun", "budget vs actual", "profit kyun gira", "sales badhi par margin kam kyun", "bridge chart bana do".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Decomposition methods, thresholds, narrative structure, waterfall and budget/forecast comparison adapted from anthropics/knowledge-work-plugins, https://github.com/anthropics/knowledge-work-plugins (Apache-2.0)"
---

# Variance analysis

Decompose variances, set materiality, write the reason for each material movement, and bridge from
one figure to the other. This skill helps prepare the analysis; the CA reviews it before it goes into
a report, an audit file or a client meeting.

**Numbers come from a workbook with formulas** (`fortax-xlsx-manipulation`): the current and comparison
figures are pulled from the trial balances or MIS, and every variance, effect and percentage is a
formula. The narrative quotes those cells; it never recomputes them.

## Inputs

- The two sets being compared: current vs previous period (TB or P&L), actual vs budget, actual vs
  forecast. Same ledger mapping on both sides — map with `fortax-financial-statements` Step 1 first.
- Drivers where available: quantities and rates (sales register by item, purchase register), headcount
  and salary register, price lists, the list of one-time items.
- The ledgers themselves, to find reasons. A reason is found in the entries, not invented.

## Decomposition techniques

### Price / volume

The basic decomposition, for revenue, cost of goods and anything expressible as price x volume.

```
Total variance = Actual - Budget (or Prior)

Volume effect  = (Actual volume - Budget volume) x Budget price
Price effect   = (Actual price - Budget price) x Actual volume
Mix effect     = residual (interaction term), or allocated proportionally

Check:  Volume effect + Price effect = Total variance
        (when mix is embedded in the price / volume terms)
```

Three-way (separating mix):

```
Volume effect = (Actual volume - Budget volume) x Budget price x Budget mix
Price effect  = (Actual price - Budget price) x Budget volume x Actual mix
Mix effect    = Budget price x Budget volume x (Actual mix - Budget mix)
```

Example — revenue:
- Budget: 10,000 units at Rs 500 = Rs 50,00,000
- Actual: 11,000 units at Rs 480 = Rs 52,80,000
- Total variance: +Rs 2,80,000 favourable
  - Volume effect: +1,000 units x Rs 500 = +Rs 5,00,000 (favourable — sold more units)
  - Price effect: -Rs 20 x 11,000 units = -Rs 2,20,000 (adverse — lower average selling price)
  - Net: +Rs 2,80,000

### Rate / mix

For blended rates across segments with different economics.

```
Rate effect = Sum of (Actual volume_i x (Actual rate_i - Budget rate_i))
Mix effect  = Sum of (Budget rate_i x (Actual volume_i - Expected volume_i at budget mix))
```

Example — gross margin: product A 60% margin, product B 40%. Budget mix 50:50 -> blended 50%. Actual
mix 40:60 -> blended 48%. Mix explains 2 percentage points of margin compression.

### Headcount / salary

```
Total salary variance = Actual salary cost - Budget salary cost

1. Headcount variance = (Actual HC - Budget HC) x Budget average cost
2. Rate variance      = (Actual average cost - Budget average cost) x Budget HC
3. Mix variance       = level / department mix shift
4. Timing variance    = hiring earlier or later than planned (part-period effect)
5. Attrition impact   = savings from unplanned exits (partly offset by replacement cost)
```

In India also separate: annual increments, statutory changes (minimum wage revision, PF wage ceiling,
bonus, gratuity valuation), and contract labour moved to or from payroll.

### Expense categories

For operating expenses where price / volume does not fit.

```
Total expense variance = Actual - Budget

1. Headcount-driven   (salaries, PF/ESI, staff welfare, recruitment)
2. Volume-driven      (freight, packing, commission, payment gateway charges, power)
3. Discretionary      (travel, advertisement, events, professional fees)
4. Contractual/fixed  (rent, insurance, software subscriptions, AMC)
5. One-time           (settlements, write-offs, project costs, penalties)
6. Timing / phasing   (spend shifted between periods vs plan; provisions missed or reversed)
```

Also check in Indian books: GST credit reversed or disallowed and charged to expense, interest and late
fee on statutory dues, prior-period items, and year-end provisions booked in one year and not the other.

## Materiality and investigation triggers

### Setting thresholds

1. **Financial statement materiality:** typically 1-5% of a benchmark (revenue, total assets, profit
   before tax) — for audit, use the materiality set under SA 320 in `fortax-audit`.
2. **Line size:** larger lines get lower % thresholds.
3. **Volatility:** volatile lines may need higher thresholds to avoid noise.
4. **Decision relevance:** what size of variance would change a decision?

### Framework

| Comparison | Amount threshold | % threshold | Trigger |
|---|---|---|---|
| Actual vs budget | client-specific | 10% | Either exceeded |
| Actual vs prior period | client-specific | 15% | Either exceeded |
| Actual vs forecast | client-specific | 5% | Either exceeded |
| Month on month | client-specific | 20% | Either exceeded |
| Audit analytical review of TB | Rs 1 lakh (or client-specific) | 20% | Either exceeded |
| Schedule III ratio note | — | 25% change in the ratio | Reason required |

Set amount thresholds for the client's size; common practice 0.5-1% of revenue for P&L lines.

### Priority when many variances cross thresholds

1. Largest absolute rupee variance — biggest profit impact.
2. Largest % variance — may be an error or a process problem.
3. Unexpected direction — opposite to trend or expectation.
4. New variance — a line that was on track and is now off.
5. Growing variance — larger each period.

## Narrative for each material variance

```
[Line item]: [Favourable / Adverse] variance of Rs [amount] ([x]%) vs [comparison] for [period]

Driver: [primary driver]
[2-3 sentences with the business reason, quantifying each contributing factor, citing the ledgers,
invoices or register rows that show it]

Outlook: [One-time / Expected to continue / Improving / Deteriorating]
Action: [None / Monitor / Investigate further / Update forecast / Ask the client]
```

Quality checklist — every narrative is:
- [ ] **Specific:** names the actual driver, not "higher than expected"
- [ ] **Quantified:** rupee and % impact of each driver
- [ ] **Causal:** why it happened, not just what
- [ ] **Forward-looking:** whether it will continue
- [ ] **Actionable:** follow-up or decision needed
- [ ] **Concise:** 2-4 sentences
- [ ] **Evidenced:** the reason is in the ledgers or documents; if not, it is a question for the client

Anti-patterns to avoid:
- "Revenue was higher than budget due to higher revenue" (circular).
- "Expenses were elevated this period" (which? why?).
- "Timing" without saying what was early or late and when it reverses.
- "One-time" without saying what the item was.
- "Various small items" for a material variance (decompose further).
- Explaining only the largest driver and ignoring offsetting items.

## Waterfall (bridge)

Shows how one value gets to another through positive and negative contributors.

```
Starting value: [budget / prior period]
Drivers:        [contributing factors with signed amounts]
Ending value:   [actual / current period]
Check:          Starting value + sum of drivers = Ending value   (a formula cell)
```

Text waterfall when no chart tool is available:

```
WATERFALL: Revenue — Q2 FY 2026-27 actual vs budget          (Rs lakh)

Q2 budget revenue                                     1,000.0
  |
  |--[+] Volume growth (new customers)                  +80.0
  |--[+] Higher sales to existing customers             +40.0
  |--[-] Price reductions / discounts                   -20.0
  |--[-] Customers lost / lower orders                  -35.0
  |--[+] Exchange gain on export sales                   +5.0
  |--[-] Timing (orders shifted to Q3)                  -15.0
  |
Q2 actual revenue                                     1,055.0

Net variance: +55.0 (+5.5% favourable)
```

Bridge reconciliation table:

| Driver | Amount | % of variance | Cumulative |
|---|---|---|---|
| Volume growth | +80.0 | 145% | +80.0 |
| Existing customers | +40.0 | 73% | +120.0 |
| Price reductions | -20.0 | -36% | +100.0 |
| Customers lost | -35.0 | -64% | +65.0 |
| Exchange gain | +5.0 | 9% | +70.0 |
| Timing | -15.0 | -27% | +55.0 |
| **Total variance** | **+55.0** | **100%** | |

Individual drivers can exceed 100% when there are offsetting items.

Good practice:
1. Order drivers from largest positive to largest negative, or in business sequence.
2. Keep to 5-8 drivers; group the small ones into "Other".
3. The bridge must reconcile (start + drivers = end) — a check cell.
4. In a chart, favourable and adverse bars in two distinct colours, with a legend.
5. Label each bar with amount and a short description.
6. Include a total variance bar.

In Excel, build the bridge as a stacked column chart with an invisible base series, or a native
waterfall chart where the Excel version supports it (openpyxl cannot write native waterfall charts; use
the stacked-column method).

## Budget vs actual vs forecast

Three-way table:

| Metric | Budget | Forecast | Actual | Budget var (Rs) | Budget var (%) | Forecast var (Rs) | Forecast var (%) |
|---|---|---|---|---|---|---|---|
| Revenue | | | | | | | |
| Cost of goods | | | | | | | |
| Gross margin | | | | | | | |

When to use each:
- **Actual vs budget:** annual performance, incentives, board reporting. Budget is set at the start of
  the year and not changed.
- **Actual vs forecast:** operational management, emerging issues. Forecast is updated monthly or
  quarterly.
- **Forecast vs budget:** how expectations moved since planning; planning accuracy.
- **Actual vs prior period:** trend, sequential performance; useful where the budget is not meaningful
  (new business, post-acquisition).
- **Actual vs same period last year:** growth adjusted for seasonality (festive quarters, March-end
  loading).

### Forecast accuracy

```
Forecast accuracy = 1 - |Actual - Forecast| / |Actual|
MAPE = average of |Actual - Forecast| / |Actual| across periods
```

| Period | Forecast | Actual | Variance | Accuracy |
|---|---|---|---|---|
| Apr | | | | |
| May | | | | |
| **Average** | | | **MAPE** | |

### Variance trends (systematic bias)

- **Consistently favourable:** budget may be too conservative.
- **Consistently adverse:** budget too aggressive, or execution problems.
- **Growing adverse:** deteriorating performance or unrealistic targets.
- **Shrinking:** forecast accuracy improving through the year (normal).
- **Volatile:** unpredictable business or weak forecasting method.

## Output

Into the client folder next to the inputs (e.g. `<Client>/<FY>/Audit/Variance_Q2_FY2026-27.xlsx`):
sheet `Data` (both sides, mapped), `Variance` (formulas, threshold flags), `Bridge` (with chart),
`Narratives`; and a short summary: verdict first (what moved most and why), then the material variances,
then the questions for the client where the ledgers do not show the reason.

## Credit

Adapted from anthropics/knowledge-work-plugins (Apache-2.0). Changed by Fortax: rupee examples, Indian
cost heads and statutory drivers, audit and Schedule III thresholds, workbook-first method.
