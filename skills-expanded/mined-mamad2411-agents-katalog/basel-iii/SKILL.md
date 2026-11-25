# Basel III/IV Framework

> Capital requirements, liquidity ratios, leverage — comprehensive Basel regulatory framework for banking supervision.

## When to Activate

- Capital adequacy calculations (CET1, Tier 1, Total Capital)
- Risk-weighted asset computation (credit, market, operational risk)
- Liquidity ratio analysis (LCR, NSFR)
- Leverage ratio assessment
- Capital buffer requirements
- FRTB (Fundamental Review of the Trading Book) implementation
- Basel IV output floor impact analysis
- Regulatory capital planning and stress testing

## Core Concepts

### Capital Structure

**Common Equity Tier 1 (CET1)** — highest quality:
- Common shares, retained earnings, accumulated OCI (with adjustments)
- Deductions: goodwill, intangible assets, deferred tax assets (threshold), investments in financial institutions
- Minimum requirement: 4.5% of RWA

**Additional Tier 1 (AT1)**:
- Perpetual instruments with loss-absorption features (CoCos — contingent convertibles)
- Write-down or conversion trigger at CET1 ratio of 5.125% (or higher)
- AT1 + CET1 minimum: 6.0% of RWA

**Tier 2 Capital**:
- Subordinated debt (minimum 5-year original maturity, amortized in last 5 years)
- Eligible provisions (up to limit)
- Total Capital minimum: 8.0% of RWA

### Capital Requirements Summary

```
                            Minimum    + Conservation    + Countercyclical    + G-SIB
CET1                         4.5%         7.0%             7.0-9.5%          8.0-10.5%
Tier 1                       6.0%         8.5%             8.5-11.0%         9.5-12.0%
Total Capital                8.0%        10.5%            10.5-13.0%        11.5-14.0%
```

### Capital Buffers

| Buffer | Size | Trigger | Effect when breached |
|--------|------|---------|---------------------|
| Conservation buffer | 2.5% CET1 | Always on | Restrictions on dividends, buybacks, bonuses |
| Countercyclical buffer | 0-2.5% CET1 | Set by national authority based on credit cycle | Restrictions on distributions |
| G-SIB surcharge | 1.0-3.5% CET1 | Systemically important banks (buckets 1-5) | Restrictions on distributions |
| D-SIB surcharge | Varies | National authority designation | Restrictions on distributions |

### Risk-Weighted Assets (RWA)

**Credit Risk — Standardized Approach:**
- Sovereign: 0% (AAA-AA), 20% (A), 50% (BBB), 100% (BB-B), 150% (below B), 100% (unrated)
- Banks: Based on External Credit Assessment or SCRA (Standardized Credit Risk Assessment)
- Corporate: 20-150% based on rating; SME support factor available
- Retail: 75% (regulatory retail), Residential mortgage: 20-70% (based on LTV)
- Commercial real estate: 60-150% (based on LTV and income-producing)

**Credit Risk — IRB Approaches:**
- Foundation IRB (F-IRB): Bank estimates PD; LGD, EAD, M prescribed by supervisor
- Advanced IRB (A-IRB): Bank estimates PD, LGD, EAD, M
- Key parameters: PD (Probability of Default), LGD (Loss Given Default), EAD (Exposure at Default), M (Maturity)
- RWA = K x 12.5 x EAD, where K is the capital requirement from the IRB formula

**Market Risk — FRTB:**
- Standardized Approach (SA): Sensitivities-based method (delta, vega, curvature) + Default Risk Charge + Residual Risk Add-on
- Internal Models Approach (IMA): Expected Shortfall (replaces VaR), with liquidity horizons, P&L attribution test, backtesting
- Boundary between banking book and trading book: stricter rules, reduced arbitrage

**Operational Risk — Basel IV:**
- New Standardized Approach replaces all previous approaches (BIA, TSA, AMA)
- Business Indicator Component (BIC) = Business Indicator x marginal coefficient (alpha)
- Internal Loss Multiplier (ILM) based on historical losses (optional, jurisdictional discretion)

### Liquidity Ratios

**Liquidity Coverage Ratio (LCR):**
```
LCR = High Quality Liquid Assets (HQLA) / Total net cash outflows over 30 days >= 100%
```
- HQLA Level 1: Cash, central bank reserves, sovereign bonds (0% risk weight) — no haircut
- HQLA Level 2A: 20% RW sovereign/PSE bonds, covered bonds (AA-) — 15% haircut, max 40% of HQLA
- HQLA Level 2B: Corporate bonds (A+ to BBB-), RMBS (AA), equities — 25-50% haircut, max 15% of HQLA
- Cash outflows: Retail deposits (3-10%), unsecured wholesale (5-100%), secured funding, derivative obligations
- Cash inflows: Contractual inflows capped at 75% of outflows

**Net Stable Funding Ratio (NSFR):**
```
NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF) >= 100%
```
- ASF: Weighted liabilities and equity (weight 0-100% based on stability)
- RSF: Weighted assets and off-balance sheet exposures (weight 0-100% based on liquidity)
- Ensures stable funding for assets over 1-year horizon

### Leverage Ratio

```
Leverage Ratio = Tier 1 Capital / Total Exposure Measure >= 3%
```
- Exposure measure: On-balance sheet items + derivative exposures (SA-CCR) + SFT exposures + off-balance sheet items
- Non-risk-based backstop to risk-weighted capital requirements
- G-SIB leverage ratio buffer: 50% of G-SIB surcharge

### Basel IV — Output Floor

- IRB banks: RWA cannot be less than 72.5% of standardized approach RWA
- Phase-in: 50% (2023) rising to 72.5% (2028) — timelines vary by jurisdiction
- Significant impact for banks with low-risk portfolios (e.g., residential mortgages)

## Methodology

### Capital Adequacy Assessment

1. **Classify capital instruments**: CET1, AT1, Tier 2 — apply deductions and adjustments
2. **Calculate credit risk RWA**: Standardized or IRB approach for each exposure class
3. **Calculate market risk RWA**: SA or IMA under FRTB rules
4. **Calculate operational risk RWA**: New Standardized Approach (BIC x coefficient)
5. **Apply output floor**: Max(IRB RWA, 72.5% x SA RWA)
6. **Compute capital ratios**: CET1%, Tier 1%, Total Capital%
7. **Assess buffer requirements**: Conservation + countercyclical + systemic
8. **Identify shortfall or surplus**: Actual ratios vs. requirements including buffers

### LCR Calculation Steps

1. **Inventory HQLA**: Classify Level 1, 2A, 2B; apply haircuts and caps
2. **Calculate cash outflows**: Apply run-off factors to each liability/commitment category
3. **Calculate cash inflows**: Apply inflow rates to maturing assets (cap at 75% of outflows)
4. **Net cash outflows**: Outflows - min(inflows, 75% x outflows)
5. **LCR**: HQLA / net cash outflows

### Stress Testing Integration

- Capital ratios under adverse scenarios (GDP decline, interest rate shock, credit losses)
- Supervisory stress tests (EBA, Fed CCAR/DFAST)
- Internal stress tests informing capital planning
- Reverse stress testing: What scenarios would breach minimum requirements?

## Templates

### Capital Ratio Computation

```
                                            Amount (EUR m)
CET1 Capital
  Common shares                               __________
  Retained earnings                           __________
  AOCI adjustments                            __________
  (-) Goodwill and intangibles                __________
  (-) Other regulatory deductions             __________
  = CET1 Capital                              __________

AT1 Capital                                   __________
Tier 1 Capital (CET1 + AT1)                   __________
Tier 2 Capital                                __________
Total Capital                                 __________

RWA — Credit Risk                             __________
RWA — Market Risk                             __________
RWA — Operational Risk                        __________
RWA — Output Floor Adjustment                 __________
Total RWA                                     __________

CET1 Ratio:       ____%    (min 4.5% + buffers)
Tier 1 Ratio:     ____%    (min 6.0% + buffers)
Total Cap Ratio:  ____%    (min 8.0% + buffers)
```

### LCR Summary

```
                                    Amount    Weight    Weighted
HQLA Level 1                        _____    100%      _____
HQLA Level 2A                       _____     85%      _____
HQLA Level 2B                       _____    50-75%    _____
Total HQLA                                             _____

Cash Outflows
  Retail deposits (stable)           _____     3-5%     _____
  Retail deposits (less stable)      _____     10%      _____
  Unsecured wholesale                _____    5-100%    _____
  Secured funding                    _____    varies    _____
Total Outflows                                          _____

Cash Inflows (capped at 75%)                            _____
Net Cash Outflows                                       _____

LCR = HQLA / Net Outflows =                            ____%
```

## Quality Gate

- [ ] Capital instruments correctly classified (CET1/AT1/T2) with all deductions applied
- [ ] Credit risk RWA uses correct approach (SA or IRB) per exposure class
- [ ] Market risk captured under FRTB framework (SA or IMA)
- [ ] Operational risk uses new standardized approach with correct BIC calculation
- [ ] Output floor applied (72.5% of SA RWA, or phase-in percentage)
- [ ] All applicable buffers identified (conservation, countercyclical, systemic)
- [ ] LCR HQLA composition respects caps (Level 2A: 40%, Level 2B: 15%)
- [ ] NSFR available and required stable funding weighted correctly
- [ ] Leverage ratio includes all exposure categories (derivatives via SA-CCR)
- [ ] Capital planning incorporates stress test results
