---
name: pf-debt-payoff
version: 1.0.0
description: Plan a debt payoff using the avalanche or snowball method and produce a month-by-month schedule.
author: matrixx0070
tags: [debt, payoff, avalanche, snowball, personal-finance]
capabilities: []
---

## When to use

Use this when the owner has multiple debts (cards, loans, buy-now-pay-later) and wants a concrete plan to clear them. Good for choosing an order, seeing a payoff date, and quantifying interest saved.

**Not for:** budgeting the monthly surplus itself (see pf-budget), bankruptcy or debt-settlement decisions, or negotiating with creditors on the owner's behalf. Those are hard stops requiring the owner and, where stakes are high, a professional.

This skill provides education and structure, not individualized financial or legal advice. For settlement, consolidation, or hardship decisions, recommend a licensed advisor or nonprofit credit counselor.

## Method

1. List every debt: balance, APR, and minimum payment.
2. Determine the monthly amount available above the sum of all minimums (the "attack" amount).
3. Decision point — pick a method: **avalanche** (attack highest APR first) minimizes total interest; **snowball** (attack smallest balance first) maximizes early wins and motivation.
4. Pay all minimums always; direct the full attack amount to the one target debt per the chosen order.
5. When a debt clears, roll its entire payment (minimum + attack) into the next target — the payment size snowballs.
6. Build the schedule month by month until each balance hits zero; record the payoff month and total interest.
7. Decision point — is any APR above ~20% and eligible for a lower-rate transfer or consolidation? Note it as an option to research (do not execute).

## Example

Debts: Card A $2,000 @ 24%, Card B $5,000 @ 18%, min payments $50 + $100. Attack amount $300/mo. Avalanche targets Card A first ($350/mo to A, $100 min to B). Card A clears ~month 6; roll $350 into B → B gets $450/mo, clears ~month 17. Total interest ≈ $1,050. Snowball would also clear A first here (it is both smallest and highest-rate), so the orders coincide.

## Pitfalls

- Skipping a minimum on a non-target debt — triggers fees and credit damage that dwarf the interest saved.
- Choosing avalanche on paper but abandoning it emotionally. If motivation is the real risk, snowball's wins may finish the job faster.
- Adding new debt mid-plan. Pause new borrowing or the schedule never converges.
- Ignoring a 0%-transfer window's expiry — unpaid balances snap back to high APR.

## Output format

```
DEBT PAYOFF PLAN — [owner]
Method: [avalanche | snowball]   Attack: $[x]/mo above minimums

ORDER
1. [debt] — $[bal] @ [APR]% — payoff ~[month]
2. [debt] — $[bal] @ [APR]% — payoff ~[month]

DEBT-FREE DATE: [month/year]
TOTAL INTEREST PAID: ~$[x]

OPTIONS TO RESEARCH
- [balance transfer / consolidation note]

Next: keep minimums automatic; send $[attack] to target #1 each month.
```

## Reference

Educational rules-of-thumb below — general working knowledge, not individualized financial or legal advice.

### Avalanche vs snowball, side by side

Both methods pay **every minimum every month** and throw one extra "attack" amount at a single target debt. They differ only in which debt is the target first.

| | **Avalanche** | **Snowball** |
|---|---|---|
| Order by | Highest APR first | Smallest balance first |
| Optimizes | Total interest (mathematically cheapest) | Motivation / early wins |
| Best when | You'll stick to a plan regardless | You need momentum to keep going |
| Risk | Top debt may be large → slow first win | Pays more interest overall |

### Worked comparison

Three debts, $250/mo total minimums, plus a **$300/mo attack**:

| Debt | Balance | APR | Minimum |
|------|---------|-----|---------|
| Store card | $1,200 | 26% | $40 |
| Credit card | $6,000 | 19% | $150 |
| Auto loan | $9,000 | 6% | $60 |

**Avalanche** targets 26% store card → 19% card → 6% auto. It clears the two high-rate balances before touching the cheap auto loan. Approximate total interest over the payoff: **~$2,050**, debt-free in roughly **~30 months**.

**Snowball** targets $1,200 store card → $6,000 card → $9,000 auto. Here the smallest balance is *also* the highest rate, so the first two targets coincide with avalanche; the difference is small in this example (**~$2,150**, similar timeline). When the smallest balance is a *low*-rate debt (say a $600 loan at 4%), snowball diverges and can cost noticeably more interest — the trade you accept for a fast psychological win.

**Rule of thumb:** the gap between the two methods is usually a few hundred dollars on typical consumer debt. If that gap won't change whether you finish, pick the one you'll actually stick to. Snowball's completed plan beats avalanche's abandoned one.

### The rollover ("why it snowballs")

When a debt clears, its **entire** payment (minimum + attack) rolls onto the next target. Each payoff makes the next payment larger, so the schedule accelerates toward the end — the last debt gets the sum of every prior payment.

### Interest and APR mechanics

- Monthly interest ≈ `balance × (APR ÷ 12)`. A $6,000 balance at 19% accrues ~$95 in interest the first month — that's how much of a minimum payment can vanish before touching principal.
- Credit cards typically compound daily on average balance; carrying any balance forfeits the grace period on new purchases.
- **Minimum-payment trap:** paying only the minimum on a high-rate card can stretch payoff to a decade-plus and cost more in interest than the original balance.

### Payoff options to *research, not execute*

- **Balance transfer:** move high-APR card debt to a 0%-intro-APR card. Watch the transfer fee (typically 3-5%) and the expiry date — unpaid balances snap back to a high rate.
- **Debt consolidation loan:** one fixed-rate personal loan replacing several cards; helps only if the new rate and total cost beat the current mix and no new card debt reaccumulates.
- **Nonprofit credit counseling / Debt Management Plan:** structured repayment, sometimes reduced rates.
- **Hardship / settlement / bankruptcy:** hard stops with credit and legal consequences — route to a licensed advisor or nonprofit counselor, never a DIY step.

### Guardrails

- Never miss a minimum on a *non-target* debt; late fees and credit damage dwarf interest saved.
- Pause new borrowing during payoff or the schedule never converges.
- Keep a small cash buffer so an emergency doesn't restart the debt cycle.
- Watch every 0%-intro window's expiry date.
