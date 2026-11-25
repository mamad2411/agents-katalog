# covenant-analysis

Covenant analysis — financial covenants, incurrence vs maintenance tests.

## When to Activate

- Reviewing loan agreements or bond indentures for covenant terms
- Analyzing covenant headroom and breach risk
- Negotiating covenant packages in new financing
- Assessing EBITDA adjustments and their impact on covenant compliance
- Evaluating covenant-lite structures versus traditional covenant packages
- Monitoring portfolio companies for covenant compliance
- Advising on waiver or amendment processes following a potential breach

## Core Concepts

### Covenant Types

**Financial covenants** — quantitative tests on financial metrics:
- **Leverage ratio**: Net Debt / EBITDA — most common. Typically tested quarterly on a trailing twelve-month (TTM) basis
- **Interest coverage ratio (ICR)**: EBITDA / Interest Expense. Ensures the borrower can service debt from operating cash flow
- **Fixed charge coverage ratio (FCCR)**: (EBITDA - Capex - Taxes) / (Interest + Scheduled Principal). More conservative than ICR — captures total fixed obligations
- **Debt service coverage ratio (DSCR)**: Net Operating Income / Total Debt Service. Common in project finance and real estate
- **Minimum EBITDA or revenue**: Absolute floor rather than a ratio — prevents the denominator problem when EBITDA approaches zero
- **Maximum capex**: Limits annual capital expenditure. Unused amounts may carry forward (basket mechanics)

**Affirmative covenants** — actions the borrower must take:
- Deliver financial statements (monthly, quarterly, annual audited)
- Maintain insurance, pay taxes, comply with laws
- Provide compliance certificates with each reporting period
- Notify lenders of material adverse changes or events of default

**Negative covenants** — restrictions on borrower actions:
- Limitations on additional indebtedness (debt incurrence tests, permitted debt baskets)
- Restrictions on liens, asset sales, dividends/distributions, investments, affiliate transactions
- Change of control provisions (often trigger mandatory prepayment or put right)
- Limitations on mergers, consolidations, and fundamental changes

### Maintenance vs. Incurrence Covenants

**Maintenance covenants** (tested periodically):
- Must be satisfied at each testing date (typically quarterly)
- Breach triggers a default (or event of default after cure period)
- Common in leveraged loans and bank facilities
- Provide early warning and lender intervention rights

**Incurrence covenants** (tested only upon a specific action):
- Must be satisfied only when the borrower takes a specified action (e.g., incurring new debt, making a distribution, completing an acquisition)
- If the borrower takes no action, the covenant is never tested — even if financial performance deteriorates
- Standard in high-yield bonds
- Less protective for creditors but more flexible for borrowers

### Leverage Ratio

The centerpiece of most covenant packages:

- **Definition matters**: Net Debt typically includes funded debt minus unrestricted cash. EBITDA definition is negotiated and often includes extensive add-backs
- **Typical levels by risk profile**:
  - Investment grade: < 3.0x
  - Leveraged loan: 4.0-6.0x at close (stepping down over time)
  - Highly leveraged: 6.0-8.0x (often covenant-lite)
- **Step-downs**: Initial covenant level may be set with headroom, stepping down over 2-3 years as the borrower is expected to deleverage
- **Net vs. gross**: Net leverage deducts cash; gross leverage does not. Cash adjustment may be capped

### EBITDA Adjustments

The definition of EBITDA in credit agreements is almost always broader than accounting EBITDA:

- **Permitted add-backs**: Restructuring charges, transaction costs, non-recurring expenses, stock-based compensation, management fees, run-rate synergies from acquisitions, cost savings initiatives
- **Run-rate synergies**: Often capped at 15-25% of EBITDA and subject to a realization period (12-24 months)
- **Pro forma adjustments**: Acquisitions and dispositions treated as if they occurred at the start of the test period
- **Uncapped add-backs**: Some aggressive documents allow uncapped add-backs — "Adjusted EBITDA" can far exceed accounting EBITDA
- **Capped add-backs**: Better practice caps total add-backs as a percentage of EBITDA (e.g., 20-25%)

### Covenant Headroom Analysis

Headroom is the buffer between actual performance and the covenant threshold:

```
Headroom = (Actual ratio - Covenant threshold) / Covenant threshold
```

For a leverage covenant where lower is better:
```
Headroom = (Covenant max - Actual leverage) / Covenant max
```

- **Adequate headroom**: Typically 15-25% provides comfort for normal business variability
- **Tight headroom (< 10%)**: Signals potential breach risk — triggers enhanced monitoring
- **Sensitivity analysis**: Model headroom under downside scenarios (revenue decline, margin compression, working capital deterioration)
- **Cure rights**: Equity cure provisions allow the sponsor to inject cash to cure a covenant breach. Typically limited to 2-3 cures over the life of the facility, not consecutive quarters

### Covenant Lite (Cov-Lite)

Term loans with no maintenance financial covenants — only incurrence tests:

- **Prevalence**: Cov-lite has become the majority of leveraged loan issuance since 2018
- **Implication for lenders**: No early warning trigger from quarterly testing. Default may only occur upon payment default or a significant negative event
- **Springing covenants**: Some cov-lite facilities include a springing leverage test that only activates if the revolving credit facility is drawn beyond a threshold (typically 35-40%)
- **Borrower advantage**: Greater operational flexibility; no risk of technical breach during temporary underperformance
- **Lender mitigation**: Tighter negative covenants, restricted payment conditions, asset sale sweep provisions

## Methodology

1. **Document review**: Read the credit agreement or indenture — focus on definitions (EBITDA, Net Debt, Permitted Indebtedness), financial covenant section, events of default, and remedies
2. **Definition mapping**: Extract the precise definition of each covenant metric. Map each add-back and adjustment to the borrower's financial data
3. **Historical compliance**: Calculate each covenant metric for the last 8 quarters using the agreement definition — not management's adjusted figures
4. **Headroom analysis**: Compute headroom for each covenant at each test date. Identify the tightest covenant (binding constraint)
5. **Forward projection**: Model covenant metrics under base, upside, and downside scenarios over the remaining term
6. **Breach scenario analysis**: Determine what level of revenue decline, margin compression, or capex overrun would trigger a breach
7. **Remedies and cure assessment**: If breach risk is elevated, evaluate cure rights, waiver feasibility, and amendment costs

## Templates

### Covenant Compliance Summary

```
Test Date: Q4 20XX (TTM basis)

Covenant               | Definition         | Threshold | Actual  | Headroom | Status
-----------------------|--------------------|-----------|---------|---------|---------
Net Leverage           | Net Debt / Adj EBITDA | < 5.50x  | 4.85x  | 11.8%   | Pass
Interest Coverage      | Adj EBITDA / Interest | > 2.00x  | 3.25x  | 62.5%   | Pass
Fixed Charge Coverage  | (EBITDA-Capex) / DS  | > 1.10x  | 1.35x  | 22.7%   | Pass
Max Capex              | Annual capex         | < $25M   | $21.2M | 15.2%   | Pass

Binding covenant: Net Leverage (tightest headroom at 11.8%)
Trend: Headroom narrowing — was 18.5% two quarters ago
```

### EBITDA Bridge (Accounting to Covenant)

```
                                            EUR M
Reported EBITDA (Accounting)                 42.0
  + Stock-based compensation                  3.5
  + Restructuring charges                     2.8
  + Transaction / advisory fees               1.2
  + Non-recurring litigation costs            0.9
  + Run-rate synergies (capped at 20%)        4.0
  + Pro forma acquisition EBITDA              6.5
  - Pro forma disposal EBITDA               (2.1)
Adjusted EBITDA (Covenant Definition)        58.8

Adjusted EBITDA is 40% higher than reported EBITDA.
Run-rate synergies represent 6.8% of Adjusted EBITDA (within 20% cap).
```

### Covenant Sensitivity Matrix

```
Revenue Decline from Base Case:
               0%     -5%    -10%    -15%    -20%
Net Leverage  4.85x   5.12x   5.45x   5.88x   6.42x
Covenant Max  5.50x   5.50x   5.50x   5.50x   5.50x
Headroom      11.8%   6.9%    0.9%   BREACH  BREACH

Margin Compression from Base Case:
               0bp   -100bp  -200bp  -300bp  -400bp
Net Leverage  4.85x   5.05x   5.28x   5.55x   5.86x
Headroom      11.8%   8.2%    4.0%   BREACH  BREACH

Breakeven: Revenue can decline ~9.5% or margins compress ~220bp
before leverage covenant breach (assuming no management action).
```

### Waiver / Amendment Checklist

```
1. Identify the covenant(s) at risk and projected breach date
2. Quantify the severity: How far below/above threshold?
3. Assess cure rights: Equity cure available? How many remain?
4. Prepare amendment request:
   - Revised covenant levels sought (temporary or permanent)
   - Business plan demonstrating path to compliance
   - Consideration offered (fee, margin increase, additional reporting)
5. Lender group dynamics: Required majority (typically 50-66.7%)
6. Timeline: Allow 4-8 weeks for syndicated facilities
7. Legal review: Confirm no cross-default triggers in other facilities
```

## Quality Gate

- [ ] Credit agreement definitions extracted verbatim — EBITDA, Net Debt, and each covenant metric
- [ ] All permitted add-backs identified and mapped to financial line items
- [ ] Covenant compliance calculated using the agreement definition, not management's adjusted figures
- [ ] Headroom analyzed for each covenant; binding constraint identified
- [ ] Forward projection models covenant metrics under at least three scenarios (base, upside, downside)
- [ ] Breakeven analysis completed — identifies the performance decline that triggers a breach
- [ ] Cure rights documented: number remaining, amount, consecutive quarter restrictions
- [ ] Cross-default provisions checked across all facilities
- [ ] Step-down schedule tracked — upcoming tightening of covenant levels flagged
- [ ] EBITDA add-back caps verified; run-rate synergies tested for reasonableness
- [ ] Compliance certificate template matches the credit agreement requirements
