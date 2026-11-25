# lbo-modeling-detail

Detailed LBO modeling — debt capacity, returns sensitivity, value creation.

## When to Activate

- Building or reviewing a leveraged buyout financial model
- Assessing debt capacity for a potential acquisition target
- Structuring the debt package (tranches, terms, covenants)
- Analyzing sponsor returns under different operating and exit scenarios
- Decomposing value creation into its components (EBITDA growth, multiple expansion, deleveraging)
- Evaluating management equity rollover and co-investment terms
- Running sensitivity analysis on entry price, leverage, and exit assumptions

## Core Concepts

### Entry Thesis

Every LBO starts with a clear investment thesis that justifies why the asset is suitable for leveraged ownership:

- **Stable, predictable cash flows**: Essential to service debt. Recurring revenue models, contracted revenues, or essential-service businesses are ideal
- **Margin improvement opportunity**: Cost reduction, procurement optimization, operational efficiency — PE firms bring operational playbooks
- **Revenue growth potential**: Organic (new products, geographies, pricing) and inorganic (add-on acquisitions)
- **Asset-light or capex-efficient**: Free cash flow conversion should be high — low maintenance capex relative to EBITDA
- **Defensive characteristics**: Low cyclicality, high switching costs, market leadership, regulatory barriers
- **Clear exit path**: Identifiable buyers (strategic acquirers, larger PE funds, public markets) within 3-5 years

### Debt Capacity Analysis

Debt capacity is the maximum leverage the business can sustain while maintaining adequate debt service coverage and covenant compliance:

- **Leverage multiples by segment** (indicative senior secured capacity):
  - Large-cap stable businesses: 5.0-6.5x EBITDA
  - Mid-market: 4.0-5.5x EBITDA
  - Small-cap or cyclical: 3.0-4.5x EBITDA
  - Software/recurring revenue: 6.0-8.0x ARR (or higher with strong NRR)
- **Total leverage** (including subordinated debt): Typically 1.0-2.0x above senior capacity
- **Coverage floors**: Minimum interest coverage 2.0x, minimum FCCR 1.1x, minimum DSCR 1.2x
- **Cash flow test**: Model downside scenario — can the business service debt if EBITDA declines 20-30%?
- **Lender appetite**: Market conditions significantly affect available leverage. Bull markets: higher leverage, tighter pricing. Bear markets: lower leverage, wider pricing

### Debt Structure

A typical LBO debt structure consists of multiple tranches with different risk/return profiles:

**Senior Secured:**
- **Revolving Credit Facility (RCF)**: Undrawn at close (or minimally drawn). Provides liquidity for working capital and short-term needs. Typically 1-2x EBITDA. 5-year tenor. Springing covenant if drawn beyond threshold
- **Term Loan A (TLA)**: Amortizing (typically 5-10% per annum). 5-6 year tenor. Lower margin than TLB. Held by relationship banks
- **Term Loan B (TLB)**: Minimal amortization (1% per annum). 6-7 year tenor. Higher margin. Broadly syndicated to institutional investors (CLOs, loan funds). Typically the largest tranche

**Subordinated / Mezzanine:**
- **Second Lien**: Secured but junior to first lien. Higher margin, longer tenor, bullet maturity
- **High Yield Bonds**: Unsecured or secured. Fixed rate. 7-10 year tenor. Incurrence covenants only. Offers certainty of funding and long-dated maturity
- **Mezzanine**: Subordinated, often with warrants or equity kickers. 12-18% all-in return. Used when senior markets are constrained or leverage exceeds senior capacity

### Cash Flow Sweep

Mandatory prepayment of debt from excess cash flow:

```
Excess Cash Flow (ECF) Calculation:
  EBITDA
  - Cash interest paid
  - Cash taxes paid
  - Scheduled debt amortization
  - Maintenance capex
  - Change in working capital
  = Excess Cash Flow

Sweep percentage: Typically 50-75%, stepping down as leverage decreases
  > 4.0x leverage: 75% sweep
  3.0-4.0x leverage: 50% sweep
  < 3.0x leverage: 25% or 0% sweep
```

ECF sweeps accelerate deleveraging and are a key return driver in LBOs.

### PIK Toggle

Pay-in-kind (PIK) toggle notes give the borrower the option to pay interest in cash or capitalize it (add to principal):

- **Cash pay**: Interest paid in cash at the stated coupon
- **PIK**: Interest accrued and added to the principal balance. Preserves cash flow but increases the debt burden
- **Toggle spread**: PIK rate is typically 50-200bp higher than the cash pay rate to compensate for deferred cash receipt
- **Use case**: Provides flexibility during periods of cash flow stress. Common in highly leveraged or cyclical situations

### Management Equity Rollover

Existing management reinvests a portion of their equity proceeds into the new structure:

- **Rollover percentage**: Typically 25-50% of management's pre-deal equity value
- **Alignment**: Ensures management has meaningful economic exposure alongside the sponsor
- **Sweet equity / ratchet**: Management may receive a disproportionate share of equity (e.g., 15-20% of equity for 5% of the total investment) that vests over time or upon achievement of return hurdles
- **Co-investment**: Senior management may invest additional cash alongside the sponsor on the same terms
- **Leaver provisions**: Good leaver (fair market value), bad leaver (cost or nominal value), vesting schedule (typically 4-5 years with cliff)

### Value Creation Decomposition

Sponsor returns come from three sources:

```
Total Value Creation = EBITDA Growth + Multiple Expansion + Deleveraging

1. EBITDA Growth
   Entry EBITDA:          $100M
   Exit EBITDA:           $140M
   Growth contribution:   ($140M - $100M) * Exit Multiple = $400M * 40% = $160M

2. Multiple Expansion
   Entry multiple:        10.0x
   Exit multiple:         11.0x
   Expansion contribution: $140M * (11.0x - 10.0x) = $140M

3. Deleveraging
   Entry net debt:        $600M
   Exit net debt:         $350M
   Deleveraging contribution: $600M - $350M = $250M

Total equity value created: $160M + $140M + $250M = $550M
Entry equity:              $400M
Exit equity:               $950M ($140M * 11.0x - $350M)
MOIC:                      2.38x
IRR (over 5 years):        ~19%
```

## Methodology

1. **Operating model**: Build a detailed P&L, balance sheet, and cash flow forecast for the target. Include revenue drivers, margin assumptions, working capital, and capex
2. **Sources and uses**: Calculate the total acquisition cost (enterprise value + fees + expenses) and identify funding sources (equity, senior debt, subordinated debt, rollover)
3. **Debt schedule**: Model each debt tranche separately — draw amount, interest rate (fixed or floating + margin), amortization, maturity, prepayment, ECF sweep
4. **Cash flow waterfall**: EBITDA → interest → taxes → capex → working capital change → mandatory amortization → ECF sweep → discretionary prepayment
5. **Credit metrics**: Calculate leverage, coverage, and liquidity ratios at each period. Verify covenant compliance
6. **Exit analysis**: Model the exit at target date using a range of multiples. Calculate equity proceeds, MOIC, and IRR
7. **Returns sensitivity**: Build a matrix varying entry multiple, exit multiple, leverage, EBITDA growth, and hold period
8. **Value creation bridge**: Decompose returns into EBITDA growth, multiple expansion, and deleveraging

## Templates

### Sources and Uses

```
USES                              $M        SOURCES                           $M
Enterprise Value                  1,000     Revolving Credit Facility          —
  Equity Value                    (400)     Term Loan A                       100
  + Net Debt Assumed              (600)     Term Loan B                       450
Transaction Fees                    25      Second Lien / Mezzanine           100
Financing Fees                      15      High Yield Notes                  150
Working Capital Adjustment          10      Total Debt                        800
Refinanced Existing Debt           600      Sponsor Equity                    350
                                            Management Rollover                50
                                            Cash on Balance Sheet              50
                                            Total Equity                      450
Total Uses                       1,050      Total Sources                   1,050

Entry leverage: 800 / 200 EBITDA = 4.0x senior, 5.0x total
Equity check: $350M sponsor + $50M rollover = $400M = 38% of TEV
```

### Debt Schedule Summary (Year 1-5)

```
                    Y0      Y1      Y2      Y3      Y4      Y5
EBITDA                      200     215     232     250     265
Senior Debt         550     520     485     445     400     350
Subordinated        250     250     250     250     250     200
Total Debt          800     770     735     695     650     550
Cash                 50      55      60      70      80      95
Net Debt            750     715     675     625     570     455

Leverage (Net/EBITDA)       3.58x   3.14x   2.69x   2.28x   1.72x
Interest Coverage           3.85x   4.30x   4.85x   5.50x   6.20x
FCCR                        1.25x   1.40x   1.58x   1.78x   2.05x
```

### Returns Sensitivity Matrix

```
IRR Sensitivity: Exit Multiple vs. EBITDA at Exit

                    Exit EBITDA ($M)
Exit Multiple   230     250     265     280     300
  8.0x         12.5%   15.8%   17.8%   19.7%   22.2%
  9.0x         16.0%   19.1%   21.0%   22.8%   25.2%
 10.0x         19.1%   22.0%   23.8%   25.5%   27.8%
 11.0x         21.8%   24.5%   26.3%   27.9%   30.1%
 12.0x         24.2%   26.8%   28.5%   30.0%   32.1%

Base case: 10.0x exit, $265M EBITDA → 23.8% IRR, 2.5x MOIC
Downside: 8.0x exit, $230M EBITDA → 12.5% IRR, 1.6x MOIC
Upside: 12.0x exit, $300M EBITDA → 32.1% IRR, 4.0x MOIC
```

### Value Creation Bridge

```
                                    $M          % of Total
Entry Equity                        400
EBITDA Growth (200 → 265)           650         48%
Multiple Expansion (10x → 10.5x)   133         10%
Deleveraging (750 → 455 net)        295         22%
Cash Generation (dividends/other)   —           —
Fees and Costs                      (28)        (2%)
Total Value Created                 1,050       —
Exit Equity                         1,450
MOIC                                2.5x (on $400M invested after fees)
Gross IRR                           23.8%
Net IRR (after carry/fees)          ~18%
```

## Quality Gate

- [ ] Operating model built with bottom-up revenue and cost assumptions, not just top-line growth rates
- [ ] Sources and uses balance; all fees and expenses accounted for
- [ ] Each debt tranche modeled separately with correct terms (rate, amortization, maturity, covenants)
- [ ] Cash flow waterfall correctly prioritizes mandatory payments before discretionary prepayment
- [ ] ECF sweep calculated per the credit agreement definition and applied to the correct tranches
- [ ] Credit metrics (leverage, coverage, FCCR) pass covenant tests in all periods including downside scenarios
- [ ] Exit assumptions grounded in comparable transaction multiples and IPO market analysis
- [ ] Returns sensitivity matrix covers entry/exit multiple, EBITDA, leverage, and hold period dimensions
- [ ] Value creation decomposed into EBITDA growth, multiple expansion, and deleveraging — must reconcile to total
- [ ] Management equity terms modeled: rollover, sweet equity, vesting, leaver provisions
- [ ] Downside case demonstrates debt can be serviced with 20-30% EBITDA decline
- [ ] Model has been independently checked (formulas, circular references, balance sheet balances)
