# Working Capital Optimization

> DSO, DPO, DIO, cash conversion cycle — managing accounts receivable, inventory, and payables for optimal liquidity.

## When to Activate

- Analyzing or optimizing the cash conversion cycle
- Accounts receivable management and DSO reduction
- Inventory optimization strategies
- Accounts payable strategy and DPO management
- Supply chain finance program evaluation
- Factoring or reverse factoring assessment
- Working capital benchmarking against industry peers
- Cash flow forecasting related to operating working capital
- Treasury dashboard design for working capital metrics

## Core Concepts

### Cash Conversion Cycle (CCC)

The CCC measures how many days it takes to convert working capital investments into cash:

```
CCC = DSO + DIO - DPO
```

| Component | Formula | Meaning |
|-----------|---------|---------|
| DSO (Days Sales Outstanding) | (Accounts Receivable / Revenue) x 365 | How long customers take to pay |
| DIO (Days Inventory Outstanding) | (Inventory / COGS) x 365 | How long inventory sits before being sold |
| DPO (Days Payable Outstanding) | (Accounts Payable / COGS) x 365 | How long the company takes to pay suppliers |

**Interpretation:**
- Lower CCC = less cash tied up in operations = better liquidity
- Negative CCC = company collects from customers before paying suppliers (e.g., Amazon, supermarkets)
- CCC varies dramatically by industry

**CCC benchmarks by industry:**

| Industry | Typical CCC | DSO | DIO | DPO |
|----------|-------------|-----|-----|-----|
| Retail (grocery) | -10 to +5 days | 3-5 | 20-30 | 30-45 |
| Technology (software) | 30-60 days | 40-70 | 0-10 | 30-50 |
| Manufacturing | 40-90 days | 40-60 | 50-80 | 40-60 |
| Construction | 60-120 days | 60-90 | 20-40 | 40-60 |
| Pharma/Healthcare | 80-150 days | 50-70 | 80-120 | 40-60 |

### Accounts Receivable Management

**Credit policy components:**
- Credit terms: Net 30, Net 60, 2/10 Net 30 (2% discount for payment within 10 days)
- Credit scoring: Internal scoring model based on payment history, financial strength, industry
- Credit limits: Maximum outstanding balance per customer
- Collection process: Dunning schedule (reminder, warning, collection, legal)

**DSO reduction levers:**
1. Tighten credit terms (shorter payment periods)
2. Offer early payment discounts (evaluate cost: 2/10 net 30 = 36.7% annualized cost)
3. Improve invoicing speed (invoice on delivery, electronic invoicing)
4. Implement systematic dunning process
5. Reduce billing errors and disputes (root cause of slow payments)
6. Segment customers by payment behavior and tailor approach
7. Automate cash application (matching payments to invoices)

**Early payment discount economics:**
```
Annualized cost of discount = (Discount% / (100% - Discount%)) x (365 / (Full term - Discount period))
Example: 2/10 Net 30 = (2/98) x (365/20) = 37.2% annualized
```
If company's cost of capital < discount cost, it is cheaper to borrow and pay early.

### Inventory Optimization

**Inventory categories:**
- Raw materials: Inputs awaiting processing
- Work-in-progress (WIP): Partially completed goods
- Finished goods: Ready for sale
- Safety stock: Buffer against demand/supply variability

**DIO reduction levers:**
1. Implement demand forecasting (statistical, ML-based)
2. ABC analysis: Focus optimization on A-items (80% of value, 20% of SKUs)
3. Just-in-Time (JIT): Reduce buffer stocks, increase delivery frequency
4. Vendor-Managed Inventory (VMI): Shift inventory ownership to supplier
5. Reduce lead times through supplier collaboration
6. Eliminate obsolete and slow-moving inventory (regular write-down review)
7. Postponement strategy: Delay customization until order received

**Economic Order Quantity (EOQ):**
```
EOQ = sqrt(2 x D x S / H)
```
- D = Annual demand (units)
- S = Fixed cost per order (ordering cost)
- H = Holding cost per unit per year

**Safety stock calculation:**
```
Safety stock = z x sigma_d x sqrt(L) + z x d_avg x sigma_L
```
- z = Service level factor (e.g., 1.65 for 95%)
- sigma_d = Standard deviation of daily demand
- L = Lead time (days)
- sigma_L = Standard deviation of lead time
- d_avg = Average daily demand

### Accounts Payable Strategy

**DPO management principles:**
- Extend payment terms without damaging supplier relationships
- Negotiate terms based on purchasing power (volume, strategic importance)
- Centralize AP to gain visibility and negotiate better terms
- Use full payment terms (do not pay early unless discount economics justify it)
- Dynamic discounting: Offer early payment at a sliding discount rate

**DPO extension levers:**
1. Renegotiate payment terms with suppliers (30 to 45 to 60 days)
2. Implement supply chain finance (reverse factoring) — pay suppliers early via bank, extend own DPO
3. Centralize payables and standardize terms
4. Align payment runs to optimize cash position (fewer, larger payment runs)
5. P-cards (purchasing cards) for small purchases (extends float by billing cycle)

**Ethical considerations:**
- Aggressive DPO extension can harm small suppliers financially
- Prompt Payment Code (UK) and similar frameworks set expectations
- EU Late Payment Directive: 30 days standard for B2G, 60 days for B2B
- Reputation risk from being known as a slow payer

### Supply Chain Finance (SCF)

**Reverse factoring (approved payables finance):**
```
Supplier ships goods → Buyer approves invoice → Bank pays supplier early (at discount)
→ Buyer pays bank at extended maturity
```
- Supplier benefit: Early payment at buyer's credit risk (lower discount rate)
- Buyer benefit: Extended DPO without harming supplier
- Bank benefit: Low-risk lending (investment-grade buyer)
- Accounting: Typically remains as trade payable (but scrutiny increasing — see Greensill)

**Factoring (receivables finance):**
- Recourse factoring: Seller retains credit risk; lower cost
- Non-recourse factoring: Factor assumes credit risk; higher cost
- Cost: Typically 1-3% of invoice value (annualized: 5-15%)
- Invoice discounting: Confidential — customers unaware of factor involvement

**Other SCF instruments:**
- Purchase order finance: Funding against purchase orders (pre-shipment)
- Inventory finance: Borrowing against warehouse receipts
- Distributor finance: Financing extended to distributors/dealers
- Dynamic discounting: Buyer uses own cash to offer sliding-scale discounts

### Working Capital Metrics Dashboard

**Primary metrics (monthly tracking):**
- CCC: Target vs. actual, trend over 12 months
- DSO, DIO, DPO: Individual trends and drivers
- Net Working Capital: AR + Inventory - AP (absolute and as % of revenue)
- Working Capital / Revenue ratio: Trending over time

**Secondary metrics:**
- Overdue AR as % of total AR (aging bucket analysis)
- Inventory turnover (COGS / Avg inventory)
- Inventory obsolescence rate (write-downs / Avg inventory)
- AP aging profile (% within terms, % overdue)
- Cash flow from operations (proxy for WC efficiency)

## Methodology

### Working Capital Diagnostic

1. **Baseline measurement**: Calculate CCC, DSO, DIO, DPO from last 4 quarters
2. **Trend analysis**: Plot 12-month rolling metrics, identify deterioration or improvement
3. **Benchmarking**: Compare to industry peers (Bloomberg, S&P Capital IQ, annual reports)
4. **Root cause analysis**: Why is DSO high? (terms? disputes? collection process?)
5. **Quantify opportunity**: Each day of CCC improvement = Revenue / 365 x 1 day of freed cash
6. **Prioritize levers**: Quick wins (process improvements) vs. structural changes (terms renegotiation, SCF)
7. **Implementation plan**: Timeline, responsibilities, IT requirements
8. **Monitor**: Monthly dashboard with targets and actuals

### Cash Impact Calculation

```
Cash freed by 1 day CCC improvement = Annual Revenue / 365

Example:
Revenue: € 500M
Current CCC: 65 days
Target CCC: 55 days (10-day improvement)
Cash freed: € 500M / 365 x 10 = € 13.7M
```

At a WACC of 8%, the annual value of freeing € 13.7M = € 1.1M.

### AR Aging Analysis

```
Aging Bucket    Amount (€)    % of Total    # Invoices    Action
Current (0-30)   _________      ____%         _____       Monitor
31-60 days       _________      ____%         _____       Reminder
61-90 days       _________      ____%         _____       Escalation
91-120 days      _________      ____%         _____       Collection
>120 days        _________      ____%         _____       Write-down review
Total AR         _________      100%          _____
```

## Templates

### Working Capital Dashboard

```
Period: _______________     Company: _______________

                    Q-4      Q-3      Q-2      Q-1      Current   Target
DSO (days)          ____     ____     ____     ____      ____      ____
DIO (days)          ____     ____     ____     ____      ____      ____
DPO (days)          ____     ____     ____     ____      ____      ____
CCC (days)          ____     ____     ____     ____      ____      ____

Net Working Capital (€m)
  Accounts Receivable  ____     ____     ____     ____      ____
  Inventory            ____     ____     ____     ____      ____
  Accounts Payable    (____    (____    (____    (____     (____
  Net WC               ____     ____     ____     ____      ____
  NWC / Revenue         ____%    ____%    ____%    ____%     ____%

Cash freed vs prior Q: € ____________
Annualized value at WACC: € ____________
```

### SCF Program Evaluation

```
Program type: [ ] Reverse factoring  [ ] Factoring  [ ] Dynamic discounting

Eligible volume:            € ____________ / year
Expected participation:        ____________%
Active volume:              € ____________ / year

Buyer perspective:
  DPO extension (days):        ____________
  Cash freed:               € ____________
  Annual benefit at WACC:   € ____________
  Program cost:             € ____________ / year
  Net benefit:              € ____________ / year

Supplier perspective:
  Days paid earlier:           ____________
  Discount rate (annualized):    ____________%
  Cost vs. own financing:        ____________% savings

Accounting treatment:
  [ ] Trade payable (on-balance)
  [ ] Bank borrowing (reclassification risk)
  Rationale: _______________
```

## Quality Gate

- [ ] CCC is calculated correctly (DSO + DIO - DPO) with consistent formulas
- [ ] Metrics are benchmarked against relevant industry peers
- [ ] Root causes for metric deviations are identified (not just symptoms)
- [ ] Cash impact of improvements is quantified in absolute terms
- [ ] AR aging analysis is current and collection actions are escalated appropriately
- [ ] Inventory includes ABC classification and obsolescence review
- [ ] AP terms are optimized without damaging critical supplier relationships
- [ ] SCF programs are evaluated for both buyer and supplier benefit
- [ ] Accounting treatment of SCF is reviewed (trade payable vs. debt reclassification)
- [ ] Working capital targets are set and monitored monthly
- [ ] Cash flow forecast incorporates working capital movements
