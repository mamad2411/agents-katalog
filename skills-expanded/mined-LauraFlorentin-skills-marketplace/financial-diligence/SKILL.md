---
name: financial-diligence
description: >
  Financial due diligence and Quality of Earnings (QoE) reporting. Automates
  trial balance tie-outs, EBITDA adjustment validation, working capital analysis,
  and debt-like item identification. Detects candidate anomalies in general ledgers
  and creates traceable reconciliation workpapers for specialist review.
  Use when user asks to "run financial due diligence", "analyze financials", "quality of earnings", or mentions financial DD, QofE, or financial analysis.
---

# Financial Diligence

Protect confidential financial, payroll, customer, bank, and tax data. Use only authorized sources, minimize personal data, preserve a source-to-workpaper audit trail, and route accounting, tax, and purchase-price conclusions to qualified professionals.

A Quality of Earnings analysis can inform price and agreement negotiations. This skill supports traceable reconciliation and issue identification; it does not replace accountants, financial advisers, or transaction judgment.

## Quality of Earnings Report Structure

| Section | Focus |
|---------|-------|
| Quality of Earnings Summary | Bridge between reported and run-rate adjusted EBITDA |
| Revenue & Margin Analysis | Customer concentration, product mix, volume vs. price trends |
| EBITDA Adjustments | Validate or refute each management add-back |
| Net Working Capital (NWC) | Historical peg calculation, seasonality, aged receivables, obsolete inventory |
| Debt and Debt-Like Items | Off-balance-sheet liabilities, deferred revenue, unpaid bonuses, unfunded capex |

## AI-Assisted Workflow

### Trial Balance Reconciliation

1. **Ingest** trial balances, audited financials, bank statements, and tax returns (3-5 year lookback)
2. **Map** granular account codes to standard FDD analytical groupings
3. **Reconcile** across data sources, flagging discrepancies
4. **Detect anomalies** — sudden expense spikes, unusual journal entries near deal launch

### EBITDA Adjustment Analysis

For each proposed management add-back:

```
## EBITDA Bridge

### Reported EBITDA: $[X]M

| # | Adjustment | Amount | Category | Defensibility | Notes |
|---|-----------|--------|----------|---------------|-------|
| 1 | Owner excess compensation | $[X]K | Recurring normalization | HIGH | Benchmarked against market rate |
| 2 | One-time litigation | $[X]K | Non-recurring | HIGH | Settlement confirmed, no ongoing exposure |
| 3 | "COVID impact" | $[X]K | Disputed | LOW | Revenue decline appears structural |
| ... | ... | ... | ... | ... | ... |

### Adjusted EBITDA: $[X]M
### Buy-Side Recommended EBITDA: $[X]M (variance: $[X]K)
```

### Net Working Capital Analysis

```
## NWC Peg Analysis

### Trailing 12-Month Average NWC: $[X]M

| Component | Avg Balance | Seasonality | Flags |
|-----------|------------|-------------|-------|
| Accounts Receivable | $[X]M | [Pattern] | [Aged AR > 90 days: $X] |
| Inventory | $[X]M | [Pattern] | [Obsolete: $X] |
| Prepaid Expenses | $[X]M | | |
| Accounts Payable | ($[X]M) | | [Stretched beyond terms?] |
| Accrued Liabilities | ($[X]M) | | |

### Recommended NWC Target: $[X]M
### Mechanism: [Dollar-for-dollar adjustment / collar]
```

## Operating Guidelines

- Always validate management's reported EBITDA independently — never accept at face value
- Distinguish between truly non-recurring items and items management wishes were non-recurring
- Flag revenue recognition policy changes during the lookback period
- Identify related-party transactions and verify arm's-length pricing
- For NWC, exclude cash and debt from the calculation unless specified in the purchase agreement
- AI outputs are analytical aids — the subjective debate over valid add-backs requires human judgment
- Record source coverage, reconciliation exceptions, preparer, reviewer, and actual effort rather than promising a fixed time saving


## Examples

**Input**: "Run a QoE analysis on this target's three-year P&L."

**EBITDA bridge output**:
| Item | Amount | Type |
|---|---|---|
| Reported EBITDA | $18.2M | — |
| + Owner salary above market | +$1.2M | Non-recurring |
| – One-time insurance recovery | –$0.8M | Non-recurring |
| – Understated capex (lease restructure) | –$1.4M | Run-rate |
| **Adjusted EBITDA (QoE)** | **$17.2M** | — |

**Finding**: Reported EBITDA overstated by $1.0M (5.5%) — material enough to impact valuation by ~$10M at 10x multiple.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Trial balance doesn't tie to P&L | Accounting errors or plug entries | Request a full GL export; flag any journal entry >5% of EBITDA without documentation |
| Working capital peg disputes | Different normalization methodologies | Align on peg definition (12-month average vs. spot) in the LOI |
| Revenue recognized incorrectly | ASC 606 misapplication | Engage accounting advisors for revenue recognition memo |
| Hidden liabilities in debt schedule | Off-balance-sheet items | Request all operating leases, earnouts, and contingent liabilities |
