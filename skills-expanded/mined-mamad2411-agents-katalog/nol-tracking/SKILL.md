---
name: nol-tracking
description: >
  Contains verified year-by-year NOL regime variance table (2007-2026+), FIFO utilization
  waterfall with worked examples, and Section 382 ownership change limitation formulas.
  C-corp net operating loss carryforward, carryback, 80% TCJA limitation, CARES Act
  5-year carryback, Form 1120 Line 29a, Form 1139 tentative refund, Florida state NOL
  conformity. Consult when computing how much NOL a C-corp can deduct this year, ordering
  mixed-era losses (pre-TCJA vs post-TCJA), building a multi-year NOL tracking schedule,
  reconstructing delinquent-year NOL waterfalls, evaluating Section 382 after an ownership
  change, or determining carryback eligibility and refund procedures.
---

# NOL Tracking

Operational skill for net operating loss computation, carryforward management, and
utilization planning for C-corporations filing Form 1120.

> **State-specific scope:** Federal NOL computation, carryback/carryforward rules,
> utilization ordering, Section 382 limitations, and refund procedures are nationally
> applicable. The State NOL Conformity section marked (Florida) contains
> **Florida**-specific NOL rules. Practitioners in other states should substitute
> their state's conformity rules.

## NOL Computation

A net operating loss occurs when a C-corporation's allowable deductions exceed gross
income for the tax year. The NOL is the negative amount on Form 1120 Line 30 (taxable
income before NOL deduction and special deductions).

**Computation sequence:**
1. Start with gross income (Line 11)
2. Subtract all deductions (Lines 12-27) — compensation, rents, taxes, depreciation, etc.
3. Arrive at taxable income before NOL deduction (Line 28 minus Line 29a/29b adjustments)
4. If the result is negative, the excess is the current-year NOL

**Items that cannot create or increase an NOL:**
- NOL deductions carried from other years — a prior carryforward cannot generate a new NOL
- Capital losses exceeding capital gains — C-corps carry net capital losses separately (3-year carryback / 5-year carryforward, not through the NOL system)

## Carryback and Carryforward Rules by Era

### Pre-TCJA (NOLs Arising Before January 1, 2018)

- **Carryback**: 2 years (taxpayer may elect to waive and carry forward only)
- **Carryforward**: 20 years (expiration date matters — track it)
- **Utilization limit**: 100% of taxable income
- **Ordering**: FIFO — apply to earliest available year first

### Post-TCJA (NOLs Arising After December 31, 2017)

- **Carryback**: None (eliminated for most taxpayers)
- **Carryforward**: Indefinite (no expiration)
- **Utilization limit**: 80% of taxable income (computed without regard to the NOL deduction itself) — the remaining 20% is always taxable
- **Ordering**: FIFO within the post-2017 bucket, but post-2017 NOLs apply only after all pre-2018 NOLs are consumed

### CARES Act Exception (2018, 2019, 2020 NOLs Only)

The CARES Act retroactively restored carryback for NOLs arising in tax years beginning
in 2018, 2019, and 2020:

- **5-year carryback** for NOLs arising in these three years
- **100% utilization** — the 80% limit was suspended for tax years beginning before January 1, 2021
- Taxpayers could elect to waive the carryback
- **Form 1139** available for quick tentative refund (12-month filing window from NOL year-end)

The CARES Act carryback attaches to the NOL's year of origin, not the year it is used.
A pre-existing NOL carried into 2020 did not acquire a new carryback right.

### Farming Loss Exception

Farming losses retain a 2-year carryback regardless of TCJA. The farming loss is the
lesser of: (a) the year's NOL, or (b) the net loss attributable to farming businesses.

## Utilization Ordering Rules

When a corporation holds NOLs from multiple years, the ordering determines which NOLs
are consumed first and at what rate.

**Sequence:**
1. **Apply oldest NOL first (FIFO)** — a 2016 NOL is used before a 2019 NOL
2. **Pre-2018 NOLs offset 100% of taxable income** — no percentage limitation
3. **Post-2017 NOLs offset 80% of remaining taxable income** — computed on the taxable income amount remaining after pre-2018 NOLs are applied
4. **Within the 80% bucket**, oldest post-2017 NOL first

### Worked Example

Corporation holds:
- 2016 NOL: $50,000 (pre-TCJA — 100% offset, 20-year carryforward expiring 2036)
- 2019 NOL: $100,000 (post-TCJA — 80% limit, indefinite carryforward)

2025 taxable income before NOL deduction: $200,000

| Step | Action | Amount Used | Remaining Income |
|------|--------|-------------|-----------------|
| 1 | Apply 2016 NOL at 100% | $50,000 | $150,000 |
| 2 | Compute 80% cap on remainder | 80% x $150,000 = $120,000 max | — |
| 3 | Apply 2019 NOL (capped at $120,000 but only $100,000 available) | $100,000 | $50,000 |

Result: Taxable income after NOL = $50,000. Both NOLs fully consumed.

If the 2019 NOL were $200,000 instead, only $120,000 would be used (80% of $150,000),
and $80,000 would carry forward indefinitely.

### Utilization Limit by Tax Year of Use

| Tax Year NOL Is Used In | Pre-2018 NOLs | Post-2017 NOLs |
|--------------------------|---------------|----------------|
| 2018-2020 | 100% offset | 100% offset (CARES Act suspended 80% limit) |
| 2021+ | 100% offset | 80% of taxable income (after pre-2018 NOLs) |

## Year-by-Year Regime Summary

| NOL Arising In | Carryback | Carryforward | Utilization Limit | Notes |
|----------------|-----------|--------------|-------------------|-------|
| Pre-2018 | 2 years | 20 years | 100% | Standard pre-TCJA |
| 2018 | 5 years (CARES) | Indefinite | 100% (CARES suspended 80%) | Retroactive carryback |
| 2019 | 5 years (CARES) | Indefinite | 100% (CARES suspended 80%) | Same CARES treatment |
| 2020 | 5 years (CARES) | Indefinite | 100% (CARES suspended 80%) | Last CARES year |
| 2021+ | None | Indefinite | 80% | TCJA rules fully apply |

## Section 382 Ownership Change Limitation

When a corporation undergoes an "ownership change" (more than 50-percentage-point shift
in stock ownership by 5% shareholders during a rolling 3-year testing period), IRC Section
382 limits annual NOL utilization to:

**Section 382 annual limit = Fair market value of stock immediately before the ownership change x long-term tax-exempt rate**

- The annual limit caps how much pre-change NOL can offset post-change taxable income each year
- Unused Section 382 limit carries forward (stacks on top of the next year's limit)
- Built-in gains/losses recognized within 5 years of the ownership change may increase or decrease the annual limit
- If the corporation fails the continuity of business enterprise test for 2 years post-change, the Section 382 limit drops to zero

**When to flag Section 382**: Any transaction involving significant equity changes — new investor rounds, redemptions, share transfers among shareholders, mergers, acquisitions. The 5% shareholder tracking requirement applies even to non-public C-corporations.

## NOL Schedule Workpaper

### Required Tracking Fields Per NOL Year

For each year in which an NOL arises, maintain:

- **Year arose** — tax year the NOL was generated
- **Original NOL amount** — the computed loss for that year
- **Regime** — pre-TCJA, CARES Act, or post-TCJA (determines carryback rights and utilization cap)
- **Utilization history** — amount used in each subsequent year, applied against which year's income
- **Remaining balance** — original amount minus cumulative utilization
- **Expiration date** — 20 years after year arose for pre-2018 NOLs; "indefinite" for post-2017 NOLs

### Waterfall Format

Build the NOL schedule as a year-by-year waterfall showing, for each year:

```
Year: [Tax Year]
  Beginning NOL carryforward balance (by year of origin)
  + Current-year NOL (if any)
  - NOL utilization this year (detail which NOL year was consumed and amount)
  = Ending NOL carryforward balance (by year of origin)
```

This format ties directly to Form 1120 Line 29a (NOL deduction) and supports the
NOL deduction statement that must accompany the return.

## Refund Procedures for NOL Carrybacks

### Form 1139 — Tentative Refund (Quick)

- File within 12 months after close of the NOL year
- IRS processes within 90 days
- Refund is tentative — subject to later audit
- Available only for carryback-eligible NOLs (pre-TCJA or CARES Act years)

### Form 1120X — Amended Return

- File within the refund statute of limitations (later of 3 years from filing or 2 years from payment)
- Used when the Form 1139 deadline has passed or additional adjustments are needed
- Longer processing time

## State NOL Conformity

### Florida

Florida maintains a separate state NOL computed on apportioned Florida taxable income:

- Post-2017 NOLs: 80% limitation applies (conforming to federal TCJA)
- Pre-2018 NOLs: 20-year carryforward
- Post-2017 NOLs: Indefinite carryforward (conforming to federal)
- Florida did **not** adopt the CARES Act 5-year carryback
- A federal NOL does not automatically create a Florida NOL — the corporation may have had positive Florida taxable income even in a federal loss year

Florida NOLs are tracked independently from federal NOLs on a separate schedule.

### Other States

State conformity varies. Common patterns:
- Piggyback states conform to federal NOL rules entirely
- Some states impose their own carryback/forward periods
- Some states cap utilization at their own percentage
- Very few states adopted the CARES Act carryback

Invoke `tax-prep:state-returns` for state-specific NOL rules when preparing state filings.

## Multi-Year Reconstruction

When reconstructing delinquent returns across multiple years:

1. Compute each year's taxable income/loss independently
2. Apply NOL carryforwards in strict FIFO order across the full timeline
3. For years where carryback was available but no return was filed — the carryback right may be preserved if the return is filed within the refund statute (but the refund statute may have expired for very old years)
4. Build the NOL waterfall schedule across all years to verify consistency

## Supporting References

Read these for deeper detail:

- `references/nol-tracking.md` — Full NOL rules including the complete year-by-year variance table (2007-2026+), detailed computation examples, ARRA small business carryback exceptions (2008-2009), and authoritative IRC/IRS citations. Sections:
  - NOL Fundamentals — computation mechanics and exclusions
  - Carryback and Carryforward Rules — pre-TCJA, post-TCJA, CARES Act, farming exception
  - Utilization Ordering Rules — FIFO logic with worked example
  - Refund Procedures — Form 1139 vs Form 1120X
  - State NOL Conformity — Florida-specific rules and other-state patterns
  - Year-by-Year Variance Table — regime lookup by NOL origin year
  - NOL Tracking — per-year tracking fields and reconstruction guidance
  - Authoritative References — IRC 172, CARES Act 2303, Form 1139, Florida Statute 220.13

## Cross-Plugin References

For upstream data needed by NOL tracking:
- Invoke `accounting-foundation:entity-profile` for entity type confirmation (C-corp status), fiscal year, ownership structure (relevant to Section 382 testing)
- Invoke `accounting-foundation:financial-statements` for income statement data feeding NOL computation
- Invoke `accounting-foundation:chart-of-accounts` for GL account mapping — NOL-related accounts (9xxx tax accounts, 2800s deferred tax liabilities)
- Invoke `bookkeeping:monthly-close` for verified trial balance data underlying taxable income computation
- Invoke `qbo-integration:qbo-reporting` for QBO-sourced P&L data feeding the NOL computation
- Invoke `tax-prep:state-returns` for state-specific NOL conformity rules and Florida F-1120 NOL schedule
- Invoke `tax-prep:business-tax-schema` for Form 1120 line definitions by tax year (Line 29a NOL deduction placement varies by form revision)
- Invoke `financial-planning:tax-provision` for deferred tax asset recognition related to NOL carryforwards (ASC 740 valuation allowance)

## Cross-Plugin Consumers

- `tax-prep:form-1120-prep` — NOL deduction amount for Form 1120 Line 29a and NOL deduction statement
- `tax-prep:tax-planning` — NOL utilization projections for year-end planning scenarios
- `tax-prep:tax-compliance` — NOL schedule as required supporting documentation
- `tax-prep:state-returns` — federal NOL data as input to state NOL conformity analysis
- `financial-planning:budgeting-forecasting` — projected NOL utilization affecting cash tax forecasts
- `financial-planning:variance-analysis` — NOL impact on effective tax rate variances
- `financial-planning:financial-modeling` — NOL carryforward balances in valuation and financial models
