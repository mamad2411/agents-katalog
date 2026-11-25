---
name: fa-accrual-schedule
version: 1.0.0
description: Build and maintain fund-level accrual schedules — management fees, admin and audit fees, and amortized expenses — so each daily or monthly NAV carries the correct expense and the payment trues up to zero.
author: matrixx0070
tags: [fund-accounting, accruals, management-fee, expense-cap, nav, close]
capabilities: []
---

# Accrual Schedule

## When to use
Use this to build the accrual for a recurring fund expense — management fee, fund administration fee, audit or tax-prep fee, directors' fees, insurance — so the NAV expenses it smoothly over the period instead of taking a lumpy hit when the invoice lands. Also use it to true up an existing accrual when the invoice, rate, or asset base changes.

**Not for:** allocating a booked expense across share classes or investors (that is a series/equalization task), or explaining why the accrued figure moved period over period (hand that to fa-variance-commentary). This produces the *schedule and the entry*, not the commentary.

## Method
1. **Define the accrual.** Name the expense, the agreement clause it comes from, the rate or fixed amount, the base it applies to, and the accrual frequency (daily for a daily-NAV fund, monthly otherwise).
2. **Pick the day-count and base convention.** Decision point: management fees usually accrue on NAV or committed/invested capital using Actual/365 (or Actual/360 for some debt-style vehicles); fixed fees (audit, admin minimum) accrue straight-line over the service period. Get the base right — gross assets, net assets, or NAV-before-fee changes the answer.
3. **Compute the periodic accrual.** For a rate: base × rate × (days / day-count basis). For a fixed fee: annual amount ÷ periods. Watch the circularity — a management fee charged on *net* assets depends on the fee itself; solve it (NAV_pre-fee × rate) or iterate.
4. **Post the accrual entry.** Dr expense, Cr accrued-expense liability, each accrual period.
5. **True up on invoice or reset.** When the actual invoice arrives, Dr accrued liability, Cr cash for the payment; book any difference between accrued-to-date and invoiced amount to the current period (a catch-up), and reset the go-forward accrual if the rate or estimate changed.
6. **Reconcile the liability.** The accrued-expense balance must equal accrued-to-date minus paid-to-date. Decision point: if the liability doesn't tie, either an accrual period was missed or a payment hit the wrong account — trace before you close.
7. **Roll forward.** Carry the ending liability and the go-forward rate into the next period's schedule.

## Example
$120M net-asset fund, management fee 1.50%/yr on net assets, daily NAV, Actual/365, month of April (30 days). Daily accrual ≈ 120,000,000 × 0.015 × (1/365) = $4,931.51/day; April accrual ≈ $147,945. Because the fee is on *net* assets it is charged on NAV-before-fee each day, so as NAV drifts the daily figure moves — recompute per day, don't multiply one day by 30. Audit fee is a fixed $60,000 for the year → accrue $5,000/month straight-line regardless of NAV. When the admin invoices $61,500 for the year (a $1,500 increase), true up the under-accrual as a current-month catch-up and reset the monthly accrual to $5,125.

## Pitfalls
- **Circular management fee.** Charging the fee on net assets *after* the fee double-counts; charge on NAV-before-fee or solve the fixed point.
- **Wrong day-count.** Mixing Actual/365 and Actual/360, or forgetting a leap day, produces a small persistent drift that an auditor will footnote.
- **Straight-lining a usage-based fee.** Admin fees with per-transaction or per-holding components are not flat — accrue on the driver, not on twelfths.
- **Ignoring the expense cap.** If the fund has an expense ratio cap with a fee waiver/reimbursement, accrue the *capped* expense and book the manager's waiver receivable; accruing the gross fee overstates expenses and understates NAV.
- **Lumpy true-ups hitting one investor.** A large catch-up on a daily-NAV fund penalizes whoever holds on that day; size accruals so true-ups stay immaterial.

## Output format
```
Expense: <name> | Agreement clause: <ref>
Basis: <rate/fixed> | Base: <gross/net/commitment> | Day-count: <Act/365...> | Frequency: <daily/monthly>
Period: <start–end> (<days> days)
Accrual this period: <$>  [formula shown]
Entry: Dr <expense acct> / Cr <accrued-liability acct>  <$>
Accrued-to-date: <$> | Paid-to-date: <$> | Liability balance: <$>  [ties: Y/N]
True-up / reset: <catch-up $, new rate>
Go-forward accrual: <$/period>
```

## Reference

### Accrual accounting principle
An accrual matches expense to the period that consumed the service, independent of when cash moves. Each period: `Dr expense / Cr accrued liability`. At payment: `Dr accrued liability / Cr cash`. The liability is a running balance of "recognized but not yet paid," and it must always equal accrued-to-date − paid-to-date. Over- and under-accruals are corrected prospectively as catch-ups unless material enough to restate.

### Management-fee mechanics
- **Base:** committed capital (common in closed-end/PE during the investment period), invested/NAV capital (post-investment period and most hedge funds), or gross vs net assets. The LPA / offering document dictates which.
- **Formula:** `fee = base × annual_rate × (days / day-count)`. Daily-NAV funds accrue every valuation day on that day's applicable base.
- **Net-asset circularity:** a fee on net assets is self-referential. Standard practice charges it on NAV *before* the current-period fee accrual, avoiding an iterative solve; some agreements specify the iterative net figure — read the clause.
- **Day-count conventions:** Actual/365 (fixed), Actual/360, and 30/360 are the common bases; the wrong one creates a systematic drift (Act/360 accrues ~1.4% more than Act/365).

### Expense caps, waivers, and the expense ratio
Many funds cap the total expense ratio (TER). When gross expenses exceed the cap, the manager waives fees or reimburses the fund: accrue the *net* (capped) expense, and record the waiver as a contra to management-fee expense with a corresponding receivable from the manager if reimbursable. Some caps are subject to **recapture** — the manager can claw back prior waivers within a window (often 3 years) if the fund later runs under the cap; track the recapturable balance off-ledger.

### Common fund accruals and their driver
| Accrual | Typical basis | Driver / base |
|---|---|---|
| Management fee | Rate | Committed / invested / net assets |
| Performance fee/carry | Rate on gains | Above hurdle, subject to high-water mark |
| Administration fee | Rate + minimum | NAV, holdings count, or flat minimum |
| Audit / tax | Fixed | Annual fee ÷ 12, straight-line |
| Custody | Rate + per-txn | AUM bps + transaction count |
| Directors / insurance | Fixed | Annual ÷ periods |
| Organizational costs | Amortized | Straight-line over ≤60 months (US GAAP: expense as incurred; some funds amortize per offering doc) |

### Prepaid vs accrued
A **prepaid** (paid before consumed) amortizes an *asset* to expense: `Dr expense / Cr prepaid`. An **accrued** (consumed before paid) builds a *liability*. Insurance paid annually in advance is a prepaid; an audit fee billed after year-end is an accrued. Getting the sign of the balance-sheet item right is the tell that you understood the timing.

### Materiality and NAV impact
Express the accrual's daily NAV impact in basis points and cents-per-share. A true-up that moves NAV by more than ~1 bp on a daily fund should be investigated before posting, because it means the ongoing accrual rate was wrong, not just late. Keep individual accrual estimates tight enough that catch-ups never distort a single day's NAV.
