---
name: fin-financial-statements
version: 1.0.0
description: Build and tie out the three primary statements (P&L, balance sheet, cash flow) with articulation checks and variance commentary.
author: matrixx0070
tags: [finance, financial-statements, reporting, gaap, ifrs, variance, articulation]
---

# Financial Statements

## When to use
Use this to prepare or review the three primary financial statements for a period, confirm they articulate correctly, or produce a management reporting package with variance commentary.

**Not for:** decomposing a single variance into price/volume/mix drivers (fin-variance-analysis), building a forward cash *forecast* (fin-cash-flow — this uses the historical indirect-method statement), or reconciling underlying accounts (fin-reconciliation).

## Method
1. **Set the reporting basis.** State entity, period, currency, basis (GAAP / IFRS / management), and comparison columns (prior period, prior year, budget).
2. **Build the income statement.** Revenue, COGS, gross profit, operating expenses by category, operating income, other income/expense, taxes, net income; compute margins.
3. **Build the balance sheet.** Assets (current, non-current), liabilities (current, non-current), equity. Decision point: if assets ≠ liabilities + equity, stop — do not proceed to cash flow until it balances.
4. **Build the cash flow statement.** Operating (indirect: net income + non-cash + working-capital changes), investing, financing; sum to net change in cash.
5. **Tie the statements together.** Net income flows to retained earnings; ending cash equals the balance-sheet cash line; PP&E and debt roll forward.
6. **Run variance analysis.** For each material line compute change vs comparison in $ and %; flag anything past the materiality threshold.
7. **Write commentary.** Explain each flagged variance with its driver. Decision point: if a variance is material but you cannot name a driver, treat it as a possible error and re-check the ledger, not a story to invent.

## Example
Q2, GAAP, vs prior quarter. P&L: revenue $4.2M, net income $610k. Balance sheet balances at $18.4M = $11.0M + $7.4M. Cash flow starts from $610k NI, adds $180k depreciation, subtracts $240k AR growth, nets to +$390k operating; ending cash $2.1M — matches the balance-sheet cash line (articulation pass). Variance: opex +$150k (+9%) vs Q1, flagged; driver = two Q2 sales hires. Retained earnings roll: opening $6.79M + $610k = $7.4M — ties.

## Pitfalls
- **Force-balancing with a plug.** A "rounding" line hiding a real $30k gap masks a booking error — find it.
- **Ending cash that doesn't match the balance sheet.** If the cash-flow ending cash ≠ balance-sheet cash, the statements do not articulate; the package is wrong.
- **Copying prior-period commentary.** Stale narratives claim drivers that no longer apply — re-derive from this period's numbers.
- **Flagging every line.** Below-materiality noise buries the two variances leadership actually needs.

## Output format
```
Entity: <...> | Period: <...> | Basis: <...> | Compare: <...>
Income statement: | line | current | compare | $var | %var | margin |
Balance sheet: | ... |  →  A = L + E: <shown> [pass/fail]
Cash flow: operating / investing / financing → net change | ending cash
Articulation: NI→equity [pass/fail] | ending cash = BS cash [pass/fail]
Variances (material): | line | $var | %var | driver |
Commentary: <...>
```

## Reference

### The three statements and how they articulate
The statements are one interlocking system. If any tie below fails, the package is wrong — do not issue it.

| Tie-out | Rule |
|---|---|
| **Net income → equity** | Beginning retained earnings + net income − dividends = ending retained earnings |
| **Cash flow → balance sheet** | Ending cash on the cash-flow statement = cash line on the balance sheet |
| **Balance sheet identity** | Assets = Liabilities + Equity (every period) |
| **Depreciation** | On P&L (expense), added back on CFS (non-cash), and accumulated on BS (contra-asset) — same number in all three |
| **PP&E roll-forward** | Beginning PP&E + capex − disposals − depreciation = ending PP&E |
| **Debt roll-forward** | Beginning debt + draws − repayments = ending debt; interest on P&L, principal in financing |
| **AR/AP → CFS** | Increase in AR = cash use (subtract); increase in AP = cash source (add) |

### Indirect-method cash flow (operating section)
`Net income + non-cash items (depreciation, amortization, stock comp, deferred tax, impairments) ± changes in working capital + gains/losses reversed = cash from operations.` Working-capital sign rule: an **increase in an asset** (AR, inventory, prepaids) *uses* cash (subtract); an **increase in a liability** (AP, accrued, deferred revenue) *provides* cash (add). Investing = capex, acquisitions, asset sales, investments. Financing = debt draws/repayments, equity issuance/buybacks, dividends.

### Key ratios and formulas
| Ratio | Formula | Reads |
|---|---|---|
| Current ratio | Current assets ÷ current liabilities | Short-term liquidity (>1.0 healthy) |
| Quick ratio | (Current assets − inventory) ÷ current liabilities | Liquidity excluding inventory |
| Gross margin | Gross profit ÷ revenue | Unit economics |
| Operating margin | Operating income ÷ revenue | Core profitability |
| Net margin | Net income ÷ revenue | Bottom-line profitability |
| Return on equity | Net income ÷ average equity | Return to owners |
| Return on assets | Net income ÷ average total assets | Asset efficiency |
| Debt-to-equity | Total debt ÷ total equity | Leverage |
| Interest coverage | EBIT ÷ interest expense | Ability to service debt |
| DSO | (Average AR ÷ revenue) × days | Collection speed |
| DPO | (Average AP ÷ COGS) × days | Payment speed |
| DIO | (Average inventory ÷ COGS) × days | Inventory turns |
| Cash conversion cycle | DSO + DIO − DPO | Days cash is tied up |
| Working capital | Current assets − current liabilities | Operating liquidity buffer |

### Statement structure checklist
- **Income statement:** Revenue → COGS → gross profit → operating expenses → operating income (EBIT) → other income/expense, interest → pre-tax income → tax → net income. Compute margins at each level.
- **Balance sheet:** current assets, non-current assets | current liabilities, non-current liabilities, equity. Order current items by liquidity.
- **Cash flow:** operating + investing + financing = net change in cash; + beginning cash = ending cash (which must match the BS).

### Materiality and commentary
Set a materiality threshold before flux review (common: ≥5% and ≥ a dollar floor). Flag only lines past it; below-threshold noise buries the real story. Every flagged variance needs a named driver derived from *this* period's data — a material variance with no explainable driver is a suspected error; re-check the ledger rather than invent a narrative. Never force-balance with a plug; a "rounding" line hiding a real gap is a booking error waiting to be found. GAAP vs IFRS differences that affect statements: inventory (IFRS bans LIFO), development costs (IFRS may capitalize), asset revaluation (IFRS permits), and lease/impairment mechanics — state the basis up front.
