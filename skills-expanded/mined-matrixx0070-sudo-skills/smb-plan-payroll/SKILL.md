---
name: smb-plan-payroll
version: 1.0.0
description: Forecast cash to the next payroll date, judge coverage, and rank collectible invoices so payroll can run with confidence.
author: matrixx0070
tags: [small-business, payroll, cash, collections, planning, coverage]
capabilities: []
---

# Plan Payroll

## When to use
Use this in the days before a payroll run when the owner needs certainty that cash will cover it — and, if it's tight, a prioritized list of collections and levers that would close the gap.

**Not for:** general 30-day cash outlook (use smb-month-heads-up); running payroll or actually chasing invoices — this produces a plan the owner approves and acts on.

## Method
1. **Set the payroll target.** Payroll date and total due, including employer taxes and any contractor payments.
2. **Project cash to that date.** Start from today's balance, add expected inflows (AR by realistic pay date), subtract non-payroll obligations due before then.
3. **Compute coverage.** Compare projected available cash on payroll date vs the amount due; state surplus or gap and the buffer left. Decision point: if the buffer is thin (say under one week of expenses), treat it as "at-risk," not "go."
4. **Rank collectible invoices.** If tight, sort overdue invoices by (likelihood-to-collect-fast × amount) to show which follow-ups most improve coverage.
5. **List other levers.** Delay discretionary AP, draw on a line of credit, owner contribution — each with an amount.
6. **Give a clear call.** Go / at-risk, in plain words. Do not chase invoices, delay payments, or draw credit yourself — payroll and money decisions are the owner's to approve.

## Example
Payroll $14,000 due Friday. Today $9,500; expected inflow retainer $4,000 (Thu); rent $2,800 due Wed. Projected available Friday = $10,700 → gap of $3,300, buffer negative. Ranked collections: Invoice #188 $5,000 (30 days over, customer reliable — high collect-fast), #191 $2,200 (slow payer — low). Levers: delay $1,500 supplier AP to next week; $2,000 credit line. Call: at-risk — chasing #188 alone closes the gap.

## Pitfalls
- Booking AR on due date instead of a realistic pay date, so coverage looks better than it is.
- Forgetting employer payroll taxes or contractor payments in the amount due.
- Calling "go" on a razor-thin buffer that one late payment would wipe out.
- Acting on collections or credit draws directly — present the plan, let the owner pull the levers.

## Output format
- **Payroll date / amount due** (incl. taxes + contractors).
- **Cash projection to date:** starting | inflows | outflows | available.
- **Coverage verdict:** surplus/gap | buffer | go / at-risk.
- **Ranked collection targets:** invoice | amount | collect-fast likelihood.
- **Other levers:** option | amount.
- **Recommendation (for owner approval).**

## Reference

### Cash-timing checklist (build the projection in this order)
1. **Confirm the payroll number is gross-plus.** Net wages are only ~70-75% of the real cash out. Add: employer FICA (7.65% of gross), federal + state unemployment, any 401(k) match, workers' comp accrual, and the payroll processor's fee.
2. **Age your AR realistically.** Book each invoice on its *likely* pay date, not its due date. Rule of thumb: current invoices land near due date; 1-30 days late slip another ~2 weeks; 60+ days late do not count toward this run's coverage.
3. **Subtract everything senior to payroll or due first:** rent, loan/card autopays, sales-tax remittance, and any check already mailed.
4. **Hold a floor.** Never plan to drain the account to zero on payroll day — keep at least one week of operating expenses as buffer.

### Coverage verdict thresholds
| Buffer after payroll | Verdict | Action |
|----------------------|---------|--------|
| > 2 weeks opex | GO | Run as scheduled |
| 1-2 weeks opex | GO (watch) | Run; flag one late payment as the risk |
| < 1 week opex | AT-RISK | Pull a lever before committing |
| Negative | STOP | Close the gap first; do not run blind |

### Payroll-tax deposit reminders
- **Deposit schedule is IRS-assigned:** most SMBs are *monthly* depositors (due the 15th of the next month); larger payrolls are *semiweekly*. Missing the schedule triggers Failure-to-Deposit penalties (2% at 1-5 days late, escalating to 10%+, 15% after IRS notice).
- **The $100,000 next-day rule:** if accrued payroll-tax liability hits $100k on any day, deposit by the next business day regardless of your normal schedule.
- **Form cadence:** Form 941 quarterly (Apr 30 / Jul 31 / Oct 31 / Jan 31); Form 940 (FUTA) annually by Jan 31; W-2s to employees and SSA by Jan 31.
- **Trust-fund warning:** withheld employee taxes are not the business's money. The Trust Fund Recovery Penalty can hold an owner *personally* liable. Never "borrow" withholding to cover net wages.

### Collections-priority scoring
Rank overdue invoices by **(likelihood-to-collect-fast × amount)**, not amount alone:
- **High collect-fast:** reliable customer, invoice < 45 days over, a quick call or resend usually works.
- **Medium:** good customer but 45-90 days over, or a disputed line item.
- **Low:** chronic slow payer, 90+ days, or relationship already strained — do not count these toward this run.
A polite "just flagging invoice #X is past due — can you release payment this week?" collects more than a formal dunning letter for a first nudge.

### Levers to close a gap (fastest to slowest, cheapest to costliest)
1. Collect the top-ranked overdue invoice (free, days).
2. Delay discretionary AP — non-critical suppliers, with a heads-up (free, days).
3. Offer an early-pay discount to a large customer (2/10 net 30 costs ~36% annualized — use sparingly).
4. Draw on an existing line of credit (interest cost, same-day).
5. Owner capital contribution (no interest, but personal cash).
6. Short-term factoring / MCA — treat as last resort; effective APRs often exceed 40%.

### Owner-approval boundary
This skill produces a plan. It never chases invoices, delays a supplier, draws credit, or runs payroll on its own — every lever is the owner's to pull.
