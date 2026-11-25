---
name: fina-3-statement-model
version: 1.0.0
description: Build a fully integrated three-statement operating model where the income statement, balance sheet, and cash flow flow from shared drivers and tie out every period with a self-balancing balance sheet.
author: matrixx0070
tags: [finance, financial-modeling, three-statement, fp&a, excel, forecasting, debt-schedule, working-capital, circularity]
capabilities: []
---

# Three-Statement Operating Model

## When to use
Use this when you need a single integrated model that projects the income statement, balance sheet, and cash flow statement together from a common set of operating drivers, with supporting schedules (working capital, PP&E, debt) and full articulation checks. This is the engine that feeds valuation and transaction work downstream.

**Not for:** discounting free cash flow to a valuation — use `fina-dcf-model`; a buyout with a specific capital structure and returns math — use `fina-lbo-model`; trading/transaction multiples benchmarking — use `fina-comps-analysis`; auditing an existing workbook's formulas and links — use `fina-audit-xls`; or producing the final formatted deliverable — use `fina-xlsx-author`.

## Method
1. **Lock the historicals and the timeline first.** You lay out at least three actual years across columns, then the forecast horizon (typically 5 years), with a single row of period headers driving every schedule. You color-code inputs (blue), formulas (black), and links to other tabs (green) so the model is legible before a single projection exists.
2. **Build the revenue driver stack.** You decompose revenue into a driver tree — price times volume, or units times ARPU, or segment build-up — never a single blended growth rate you cannot defend. Decision point: if the business is capacity-constrained, drive revenue off the PP&E/capacity schedule rather than off demand assumptions, because output cannot exceed installed capacity.
3. **Project the cost structure with fixed/variable split.** You model COGS and opex as a mix of percent-of-revenue (variable) and fixed dollars grown at inflation, arriving at EBITDA, then subtract D&A (from the PP&E schedule) to get EBIT.
4. **Build the working-capital schedule.** You forecast AR, inventory, and AP off days ratios (DSO, DIO, DPO) applied to revenue or COGS, then compute the period change in net working capital that feeds the cash flow statement.
5. **Build the PP&E and depreciation schedule.** You roll forward gross PP&E: opening plus capex less disposals; depreciate off the opening balance or a capex-vintage waterfall; the ending net PP&E links to the balance sheet and depreciation links to both the income statement and cash flow.
6. **Build the debt and interest schedule with a revolver and cash sweep.** You roll each tranche forward, compute mandatory amortization, then let a cash sweep pay down debt with excess cash and let a revolver draw to cover any shortfall to a minimum cash balance. Decision point: base interest on the average of opening and closing balances for accuracy — this creates a deliberate circular reference (interest → net income → cash → debt paydown → interest) that you resolve with iterative calculation plus a circuit-breaker switch; if the circularity destabilizes the file, flip the switch to charge interest on the opening balance instead.
7. **Assemble the cash flow statement (indirect method).** You start from net income, add back non-cash items (D&A), subtract the change in NWC, subtract capex, then layer financing flows (debt draws/repayments, dividends, equity). Ending cash equals opening cash plus net change.
8. **Wire the balance sheet and let cash and the revolver plug it.** Ending cash flows in from the cash flow statement; every other line links to its schedule; retained earnings rolls forward with net income less dividends. The balance sheet must balance with no hardcoded plug — assets equal liabilities plus equity by construction.
9. **Run the articulation checks.** You add a checks block that confirms the balance sheet balances every period, cash on the balance sheet ties to the cash flow ending cash, and retained earnings rolls correctly. Any nonzero check flags red before you trust an output.

## Example
A company posts Year 0 revenue of 1,000 with 60% variable COGS and 200 of fixed opex. You forecast 10% revenue growth, so Year 1 revenue is 1,100. Variable COGS is 660, fixed opex 206 (grown 3%), giving EBITDA of 234. Depreciation from the PP&E schedule is 90 (opening net PP&E 450, capex 120, straight-line over ~10 years). EBIT is 144. DSO of 45 on revenue of 1,100 puts AR at 136 versus 123 prior, a 13 use of cash; net NWC change is a 20 use overall. With debt of 500 at 6% on average balances, interest is roughly 29, pretax income 115, tax at 25% is 29, net income 86. Cash flow: 86 net income + 90 D&A − 20 NWC − 120 capex = 36 before financing; a mandatory 25 amortization leaves 11, which the sweep applies to debt. The balance sheet balances and the check row reads 0.

## Pitfalls
- **Hardcoded balance-sheet plug.** Never force the balance sheet to balance with a manual number; it hides real errors and breaks the moment an assumption changes. Let cash and the revolver be the only balancing items.
- **Interest circularity meltdown.** Turning on iterative calc without a circuit breaker means one bad formula spreads NaN/#REF across the whole file. Always ship a switch that flips interest to the opening balance so you can isolate the break.
- **Double-counting D&A.** If depreciation is both subtracted on the income statement and forgotten as an add-back on the cash flow, cash is understated every period. Trace D&A from one schedule to both statements.
- **Working capital sign errors.** An increase in AR is a use of cash (negative); flipping the sign silently inflates operating cash flow. Anchor every NWC line to "increase in asset = cash out."
- **Revolver that goes negative.** Without a MIN/MAX floor, a cash sweep can pay down more than the outstanding balance and create negative debt. Cap the sweep at the balance and cap the draw at the facility limit.
- **Retained earnings that don't roll.** Linking equity to a static number rather than opening RE plus net income less dividends breaks articulation the first forecast year.

## Output format
```
INTEGRATED THREE-STATEMENT MODEL
Company: <name>          Currency: <ccy>          ($ in 000s)

                         FY0A     FY1E     FY2E     FY3E
INCOME STATEMENT
  Revenue                1,000    1,100    1,210    1,331
  EBITDA                   240      234      262      293
  D&A                      (85)     (90)     (96)    (103)
  EBIT                     155      144      166      190
  Interest, net            (30)     (29)     (27)     (24)
  Pretax income            125      115      139      166
  Taxes                    (31)     (29)     (35)     (42)
  Net income                94       86      104      125

CASH FLOW (indirect)
  CFO                      160      156      178      201
  Capex                   (120)    (120)    (130)    (140)
  Financing              (25)      (25)     (30)     (35)
  Net change in cash        15       11       18       26

BALANCE SHEET
  Cash                      40       51       69       95
  Total assets           1,300    1,340    1,410    1,505
  Total liab + equity    1,300    1,340    1,410    1,505

CHECKS (must be 0)
  BS balances (A-L-E)        0        0        0        0
  Cash ties to CF            0        0        0        0
  RE roll                    0        0        0        0
```

## Reference

### Schedule roll-forwards
| Schedule | Ending balance formula | Feeds |
|---|---|---|
| Working capital (AR) | DSO / 365 × Revenue | ΔNWC on CF; AR on BS |
| Working capital (Inv) | DIO / 365 × COGS | ΔNWC on CF; Inventory on BS |
| Working capital (AP) | DPO / 365 × COGS | ΔNWC on CF; AP on BS |
| PP&E (net) | Opening net + Capex − D&A − Disposals | Net PP&E on BS; D&A on IS & CF |
| Debt (per tranche) | Opening − Mandatory amort − Sweep + Draw | Debt on BS; Interest on IS |
| Retained earnings | Opening RE + Net income − Dividends | Equity on BS |

### Circularity and the circuit-breaker switch
| Item | Convention |
|---|---|
| Interest expense | Rate × AVERAGE(opening debt, closing debt) |
| Why circular | Interest → NI → CFO → cash → sweep → closing debt → interest |
| Resolution | Enable iterative calculation (Excel: File ▸ Options ▸ Formulas ▸ ~100 iterations, 0.001 delta) |
| Circuit breaker | A `CIRC_SWITCH` cell: 1 = interest on average (iterative on); 0 = interest on OPENING balance (breaks the loop) |
| Recovery drill | Flip switch to 0, delete the errored cell, restore the formula, flip back to 1 |

### Cash flow (indirect method) mechanics
| Line | Source |
|---|---|
| Net income | Income statement |
| + D&A | PP&E schedule (non-cash add-back) |
| − Increase in NWC | Working-capital schedule (Δ = current − prior) |
| − Capex | PP&E schedule |
| = CFO + CFI (pre-financing FCF) | subtotal, feeds the sweep |
| ± Debt draws / (repayments) | Debt schedule |
| − Dividends | RE schedule |
| = Net change in cash | ties to BS cash delta |

### Cash sweep and revolver mechanics
| Step | Formula |
|---|---|
| Cash available for sweep | Pre-financing FCF − mandatory amort − minimum cash target |
| Optional sweep paydown | MIN(cash available × sweep %, term-loan opening balance) |
| Revolver draw | MAX(0, minimum cash − cash before revolver) |
| Revolver repay | MIN(revolver opening, excess cash above minimum) |

### QC / tie-out checks (checks row conventions)
| Check | Passes when |
|---|---|
| Balance sheet balances | Total assets − total liabilities − total equity = 0 every period |
| Cash ties | BS ending cash − CF ending cash = 0 |
| RE roll | BS retained earnings − (opening RE + NI − dividends) = 0 |
| Debt continuity | Opening + draws − repayments − ending = 0 per tranche |
| PP&E continuity | Opening + capex − D&A − disposals − ending = 0 |
| Sign convention | Every increase in an asset appears as a cash outflow |
| Aggregate flag | A single top-of-model cell = SUM of absolute check values; 0 = clean |

Once the checks read zero across the horizon, hand the unlevered earnings and capital structure to `fina-dcf-model` or `fina-lbo-model`, and format the deliverable with `fina-xlsx-author`.
