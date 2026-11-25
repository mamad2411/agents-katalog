---
name: financial-statements
description: Generates GAAP/IFRS-compliant financial statements — income statement (P&L), balance sheet, cash flow statement — with current vs. prior period vs. prior-year comparison columns, dollar and percent change, basis-point margin moves, and material-variance flagging. Make sure to use this skill whenever the user says "generate financials for [period]", "build a P&L", "prepare the balance sheet", "run cash flow", "monthly/quarterly close output", "financials for the board", "comparative statements", "consolidated financials", "GAAP P&L", "IFRS package", "FY-end statements", or any request for a formal financial report. Includes presentation classification (ASC 220/210/230 / IAS 1/7), disaggregation rules (ASC 606), required note checklist, period-end adjustment checklist, and Puerto Rico / Act 60 / bilingual considerations. Do NOT use for: explaining WHY a variance happened (use finance:variance-analysis — this skill flags, the other explains), individual journal entries (use finance:journal-entry), reconciling specific accounts to subledgers or banks (use finance:reconciliation), operational SaaS KPI dashboards that are NOT GAAP statements such as ARR/NRR/CAC trend boards (use data:build-dashboard), SOX 404 control testing (use finance:audit-support), or close-process task scheduling (use finance:close-management).
---

# Financial Statements

GAAP/IFRS-compliant P&L, balance sheet, and cash flow with current vs. prior period vs. prior-year columns, dollar and percent change, basis-point margin moves, material-variance flags, and disclosure-note checklist.

## When to use vs. defer

| Use this skill when... | Defer to... |
|---|---|
| Generating formal P&L / BS / CF | — |
| Comparative period reporting (current / prior / prior-year) | — |
| Auto-flagging material variances ON the statements | Then chain to `finance:variance-analysis` to EXPLAIN them |
| Pre-statement adjustment checklist | Individual entries → `finance:journal-entry` |
| Disclosure note checklist (ASC 606 disagg, concentration, going concern) | — |
| SaaS metrics on a separate KPI page accompanying GAAP statements | Standalone operational dashboard → `data:build-dashboard` |
| Statement-level variance flagging | Driver decomposition (volume × price × mix) → `finance:variance-analysis` |
| Identify reconciling item on the face of the statement | Tie-out work → `finance:reconciliation` |
| Quarterly close output for review | SOX control testing → `finance:audit-support` |
| Close calendar produces these statements as a deliverable | Close calendar / status → `finance:close-management` |
| Raw spreadsheet manipulation, custom workpaper formulas, ad-hoc xlsx authoring | `xlsx` |

**Defining characteristic:** This skill PRODUCES the statements and FLAGS what looks unusual. It does not EXPLAIN drivers (that's variance-analysis), find tie-out differences (that's reconciliation), or book entries (that's journal-entry).

## Statement set produced

### 1) Income statement (P&L)

Classified by function (US default). For each line, present three comparison columns plus dollar and percent change, plus optional budget column.

```
                                Current    Prior      Prior YR    $ Δ vs    % Δ vs   $ Δ vs    % Δ vs   Budget    $ Δ vs
                                Period     Period     Same Per.   Prior     Prior    PY        PY       (opt)     Bud
                                --------   --------   ---------   -------   ------   -------   ------   -------   -------
Revenue
  Subscription / ARR-bearing    $XX,XXX    $XX,XXX    $XX,XXX     $X,XXX    X.X%     $X,XXX    X.X%     $XX,XXX   $X,XXX
  Professional services         $XX,XXX    $XX,XXX    $XX,XXX     ...
  Other revenue                 $XX,XXX    $XX,XXX    $XX,XXX     ...
                                --------   --------   ---------   -------            -------            -------
Total revenue                   $XX,XXX    $XX,XXX    $XX,XXX     ...

Cost of revenue
  Hosting / cloud infrastructure
  Customer support
  Implementation services
  Third-party software embedded in product
                                --------   --------   ---------
Gross profit                    $XX,XXX    $XX,XXX    $XX,XXX
  Gross margin %                XX.X%      XX.X%      XX.X%       —         X bps    —         X bps

Operating expenses
  Sales & marketing
  Research & development
  General & administrative
  Compliance program (SOC 2 audit, pen test, GRC tooling) [break out if material]
  Cyber insurance premium       [break out if material]
                                --------   --------   ---------
Total operating expenses        $XX,XXX    $XX,XXX    $XX,XXX

Operating income (loss)         $XX,XXX    $XX,XXX    $XX,XXX
  Operating margin %            XX.X%      XX.X%      XX.X%       —         X bps    —         X bps

Other income / (expense)
  Interest income
  Interest expense
  FX gain/(loss)
  Other, net

Income (loss) before tax        $XX,XXX    $XX,XXX    $XX,XXX
Tax provision                   $XX,XXX    $XX,XXX    $XX,XXX
  [If Puerto Rico Act 60 entity: show federal vs. PR provision separately
   and disclose effective rate impact in notes]

Net income (loss)               $XX,XXX    $XX,XXX    $XX,XXX
  Net margin %                  XX.X%      XX.X%      XX.X%       —         X bps    —         X bps

EPS (basic / diluted)           [if applicable]
```

**Calculations:**
- $ change = Current − Comparison
- % change = (Current − Comparison) / |Comparison| × 100; show "n/m" (not meaningful) if Comparison ≈ 0 or sign-flipped
- Margin change = (Current margin − Comparison margin) × 10,000 bps; e.g., 84.2% → 81.7% = −250 bps

**SaaS / cybersec context (the operator's PR cybersec founder context):** Surface ARR, NRR, gross retention, CAC, CAC payback, magic number, LTV/CAC on a SEPARATE accompanying KPI page — these are NOT on the GAAP P&L. If user asks ONLY for SaaS metrics with no GAAP statements, defer to `data:build-dashboard`.

### 2) Balance sheet

Classified, current/non-current split, presented in liquidity order. Two periods minimum (current period-end vs. prior year-end).

```
ASSETS
Current assets
  Cash and equivalents
  Short-term investments
  Accounts receivable, net of allowance for credit losses (ASC 326)
  Prepaid expenses and other current assets
Total current assets

Non-current assets
  Property, plant & equipment, net of accumulated depreciation
  Operating lease right-of-use assets (ASC 842)
  Intangible assets, net
  Goodwill (not amortized; tested for impairment ASC 350)
  Long-term investments
  Deferred tax assets
  Other long-term assets
Total non-current assets
TOTAL ASSETS

LIABILITIES
Current liabilities
  Accounts payable
  Accrued expenses (incl. payroll, bonus, audit fees)
  Deferred revenue, current
  Current portion of long-term debt
  Operating lease liabilities, current
  Income taxes payable
Total current liabilities

Non-current liabilities
  Long-term debt
  Deferred revenue, long-term
  Operating lease liabilities, long-term
  Deferred tax liabilities
  Other long-term liabilities
Total non-current liabilities
TOTAL LIABILITIES

EQUITY
  Common stock
  Additional paid-in capital
  Retained earnings (accumulated deficit)
  Accumulated other comprehensive income / (loss)
  Treasury stock
Total stockholders' equity
TOTAL LIABILITIES AND STOCKHOLDERS' EQUITY
```

**Verification:** TOTAL ASSETS must equal TOTAL LIABILITIES + EQUITY to the cent. If off, flag and chain to `finance:reconciliation`.

### 3) Cash flow statement (indirect method — US default)

```
CASH FLOWS FROM OPERATING ACTIVITIES
Net income (loss)
Adjustments to reconcile net income to net cash from operating:
  + Depreciation and amortization
  + Stock-based compensation
  + Amortization of debt issuance costs / deferred financing
  + Deferred income taxes
  + Loss / (gain) on disposal of assets
  + Impairment charges
  + Other non-cash items
Changes in operating assets and liabilities:
  +/− Accounts receivable
  +/− Inventory
  +/− Prepaid expenses and other assets
  +/− Accounts payable
  +/− Accrued liabilities
  +/− Deferred revenue
  +/− Other liabilities
Net cash provided by (used in) operating activities

CASH FLOWS FROM INVESTING ACTIVITIES
  Purchases of property and equipment
  Purchases of investments
  Proceeds from sale / maturity of investments
  Acquisitions, net of cash acquired
  Other investing activities
Net cash provided by (used in) investing activities

CASH FLOWS FROM FINANCING ACTIVITIES
  Proceeds from issuance of debt
  Repayment of debt
  Proceeds from issuance of common stock / option exercises
  Repurchases of common stock
  Dividends paid
  Payment of debt issuance costs
  Other financing activities
Net cash provided by (used in) financing activities

Effect of exchange rate changes on cash
Net increase (decrease) in cash and cash equivalents
Cash and cash equivalents, beginning of period
Cash and cash equivalents, end of period

Supplemental disclosures (required):
  Interest paid
  Income taxes paid
Non-cash investing/financing activities (disclose separately):
  Right-of-use assets obtained in exchange for new lease liabilities
  Stock issued in connection with acquisitions
```

## Comparative period discipline

**Default three-column presentation:**
- Current period
- Prior period (immediately preceding — MoM if monthly, QoQ if quarterly)
- Prior year same period (YoY — handles seasonality)

**For each line, compute and display:**
- $ change vs. prior period
- % change vs. prior period
- $ change vs. prior year
- % change vs. prior year
- For margins/ratios: basis-point change (1 bp = 0.01%)

**Optional fourth/fifth columns:**
- Budget (annual operating plan, locked at year start)
- Latest forecast (rolling)
- TTM (trailing 12 months) for trend smoothing

**When to use which comparison:**
| Comparison | Best for |
|---|---|
| vs. Prior period | Sequential operating tempo |
| vs. Prior year | Growth, seasonality-adjusted |
| vs. Budget | Annual performance, comp decisions |
| vs. Forecast | Operating management, emerging issues |
| TTM / R12 | Smoothing seasonality, trend lines |

## Material-variance flagging (statement-level)

This skill FLAGS — `finance:variance-analysis` EXPLAINS.

### Three flag tiers

| Tier | Trigger | Action on the statement |
|---|---|---|
| **FLAG (informational)** | Δ > 10% AND $ exceeds line-item materiality | Mark with `▲` / `▼`; suggest chain to variance-analysis |
| **INVESTIGATE (urgent)** | Sign change, new line item, disappeared line item, ratio outside 2-yr historical range, or single-customer concentration crosses 10% | Mark with `‼`; require explanation before finalizing |
| **DISCLOSE (notes)** | Triggers a required GAAP/IFRS disclosure (e.g., concentration, going concern, subsequent event, related party, segment change) | Add to disclosure-note checklist |

### Suggested line-item materiality (scale to org size)

| Line item size | Dollar threshold | % threshold |
|---|---|---|
| > $10M | $500K | 5% |
| $1M – $10M | $100K | 10% |
| < $1M | $50K | 15% |

### What to write next to each flag

- "▲ Hosting cost +32% vs. prior quarter ($420K) — chain to `finance:variance-analysis` for driver decomposition"
- "‼ Deferred revenue dropped $1.2M with no corresponding revenue lift — investigate via `finance:reconciliation`"
- "‼ Customer X reached 11% of total revenue — add ASC 280 customer-concentration disclosure to notes"
- "▲ Cyber insurance premium +45% YoY — flag for variance-analysis (renewal cycle, claims history, market hardening)"
- "▲ Compliance program spend +60% YoY — likely SOC 2 Type II ramp or new pen test cadence; chain to variance-analysis"

## Period-end adjustment pre-flight checklist

Before producing finals, confirm each item is booked. If any are missing, list them and pause:

- [ ] Accruals (unbilled vendor invoices, payroll through period-end, bonus accrual)
- [ ] Prepaid amortization current (insurance, software subscriptions)
- [ ] Deferred revenue recognition current (ASC 606 over-time recognition)
- [ ] Depreciation / amortization (PP&E, intangibles, ROU assets)
- [ ] Bad debt provision update (ASC 326 CECL)
- [ ] Inventory write-downs (if applicable)
- [ ] FX revaluation of foreign-currency monetary balances
- [ ] Tax provision (current + deferred)
- [ ] Equity method pickup (if applicable)
- [ ] Stock-based compensation expense (graded vesting catch-up if needed)
- [ ] Lease liability remeasurement (ASC 842, if any modifications)
- [ ] Reclassifications (current portion of LT debt, contra-account netting, intercompany elimination)

For individual entry mechanics, defer to `finance:journal-entry`.

## Disclosure-note checklist (ASC / IFRS)

Surface as accompanying notes — these don't go ON the face of the statements:

- Significant accounting policies (revenue recognition, leases, SBC, taxes)
- Revenue disaggregation (ASC 606) — by product line, geography, timing of recognition, contract type
- Customer concentration — any single customer >10% of revenue (ASC 280)
- Geographic concentration — revenue and long-lived assets by country
- Lease maturity schedule (ASC 842)
- Debt maturity schedule
- Income tax rate reconciliation (statutory vs. effective; for PR Act 60 entities, show jurisdictional split)
- Stock-based compensation (plan, grants outstanding, valuation assumptions)
- Goodwill and intangibles roll-forward
- Going concern considerations
- Subsequent events (through issuance date)
- Related party transactions
- Commitments and contingencies (litigation, indemnification, cyber-incident reserves)
- Segment reporting (ASC 280, if multiple operating segments)

## Puerto Rico / Act 60 / bilingual considerations

For PR-domiciled entities (relevant to the operator's context):

- **Tax provision:** Show PR corporate tax (typically 4% under Act 60 export-services decree) separately from US federal/state. Effective rate reconciliation must show the Act 60 benefit explicitly to be defensible.
- **Bilingual statements:** If filing with PR Department of State, Hacienda, or local lenders, produce English and Spanish columns. Standard label translations:
  - Income Statement → Estado de Resultados
  - Balance Sheet → Estado de Situación / Balance General
  - Cash Flow Statement → Estado de Flujos de Efectivo
  - Revenue → Ingresos
  - Cost of revenue → Costo de ingresos
  - Gross profit → Ganancia bruta
  - Operating expenses → Gastos operativos
  - Operating income → Ingreso operativo
  - Net income → Ingreso neto / Ganancia neta
- **Currency:** USD for both columns (PR uses USD); no FX translation issue between the two columns.
- **Decree compliance disclosures:** Note Act 60 grant number, decree term, and any compliance-condition flags (e.g., minimum employment, charity contribution requirement).

## Cybersecurity-product cost taxonomy (suggested COGS / OpEx breakdown)

For a security SaaS, the following lines often warrant separate disclosure to make gross margin and unit economics legible:

**In COGS:**
- Hosting / cloud infrastructure (AWS / GCP / Azure) — typically the largest line
- Threat intel feeds, vulnerability databases, third-party scanners (cost of goods embedded in product)
- 24/7 SOC / on-call labor (if MDR-style offering)
- Customer support
- Implementation / onboarding services

**In OpEx (G&A):**
- Cyber insurance premium (often material; growing 30–60% YoY in current market)
- Compliance program: SOC 2 audit fees, ISO 27001 surveillance, pen test fees, GRC tooling (Vanta / Drata / Secureframe), virtual CISO
- Legal — privacy / data-protection counsel
- Customer-facing trust assurances (TrustCenter / Whistic / SafeBase)

**In OpEx (S&M):**
- Channel partner fees (MSP / MSSP rev share)
- Industry analyst fees (Gartner Magic Quadrant prep, Forrester Wave)

## Output structure

1. **The three statements** in classified GAAP/IFRS format with current / prior / prior-year columns and $ + % + bps changes
2. **Optional budget / forecast columns** if the user has a plan loaded
3. **Materiality flags** (▲ FLAG / ‼ INVESTIGATE) inline next to flagged lines, each with suggested chain (variance-analysis / reconciliation / disclosure)
4. **Pre-statement adjustment checklist** — confirmed or outstanding
5. **Disclosure note checklist** — items requiring footnote treatment
6. **Optional accompanying KPI page** for SaaS / cybersec metrics (ARR, NRR, gross retention, net retention, CAC, CAC payback, magic number, LTV/CAC, Rule of 40) — clearly labeled as non-GAAP supplemental
7. **Bilingual EN/ES** version if PR filing context detected
8. **Suggested chains:**
   - Any FLAG → `finance:variance-analysis`
   - Any tie-out problem (BS doesn't balance, CF doesn't reconcile to BS cash movement) → `finance:reconciliation`
   - Any new entry needed before finalization → `finance:journal-entry`
   - Any concentration / going concern / subsequent event → add to disclosure notes

**Important:** This skill assists with workflows. All statements should be reviewed by qualified financial professionals — and counsel for PR Act 60 disclosures — before reliance, especially for external reporting (lender filings, board packages, audited financials, regulatory submissions).
