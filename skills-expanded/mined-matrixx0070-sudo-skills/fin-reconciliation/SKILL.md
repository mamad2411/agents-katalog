---
name: fin-reconciliation
version: 1.0.0
description: Reconcile a GL account to a bank statement, subledger, or third-party source, prove the tie-out bridge, and clear differences.
author: matrixx0070
tags: [finance, reconciliation, gl, bank-rec, subledger, close]
---

# Reconciliation

## When to use
Use this to reconcile a general-ledger account to a supporting source — bank statement, subledger (AR/AP), or third-party report — to explain a difference, or to produce a signed reconciliation for the close.

**Not for:** drafting the correcting entry itself in full detail (hand the item to fin-journal-entry), or explaining an actual-vs-budget variance (fin-variance-analysis). This proves *GL agrees to source*, not plan.

## Method
1. **Define the reconciliation.** Name the GL account, the supporting source, the as-of date, and both starting balances.
2. **Compute the raw difference.** GL − source. Decision point: if zero and both balances are complete, note it and sign off — no reconciling items needed.
3. **Identify reconciling items.** Work the usual categories: timing (outstanding checks, deposits in transit, unposted receipts), errors, omissions, and one-sided items.
4. **Quantify and categorize each item.** Capture amount, direction (which side it adjusts), category, and root cause.
5. **Prove the tie-out.** Adjusted GL (GL ± its items) must equal adjusted source (source ± its items); show the bridge. Decision point: if the bridge doesn't tie, you are missing an item — do not sign off on a residual you can't name.
6. **Resolve.** Propose the correcting entry or action for each item that needs one; flag aged or unexplained items.
7. **Sign off.** State reconciled / not reconciled with any residual unexplained amount.

## Example
Cash account 1000 vs bank statement, 3/31. GL $84,200; bank $86,050; raw diff −$1,850. Items: (a) two outstanding checks −$2,300 (reduce bank), (b) deposit in transit +$500 (add to bank), (c) unrecorded bank fee −$50 (reduce GL). Bridge: adjusted bank = 86,050 − 2,300 + 500 = $84,250; adjusted GL = 84,200 − 50 = $84,150... off by $100 → missing item found: a $100 unposted customer receipt. Corrected, both sides = $84,250. Correcting entry: book fee and receipt to GL. Reconciled, $0 residual.

## Pitfalls
- **Signing off with an unexplained residual.** "Reconciled except $100" is not reconciled — an unnamed gap is a potential error or fraud.
- **Reconciling to an incomplete source.** A bank statement missing the last day understates cash; confirm the source covers the full period.
- **Miscoding item direction.** Adding an outstanding check instead of subtracting flips the bridge and hides the real difference.
- **Letting items age silently.** A reconciling item outstanding three months is usually an error you never booked, not timing.

## Output format
```
Account: <GL#> | Source: <...> | As-of: <date>
Balances: GL <...> | source <...> | raw diff <...>
Reconciling items:
  | item | amount | side (GL/source ±) | category | root cause | action |
Bridge: adjusted GL <...> = adjusted source <...>  [pass/fail]
Correcting entries proposed: <...>
Aged / unexplained flags: <...>
Conclusion: reconciled / not | residual: <$> | sign-off: <who/date>
```

## Reference

### The bank reconciliation bridge (two-column proof)
Adjust each side for the items the *other* side already knows about, then both must equal the true cash balance.

| Book (GL) side | Bank side |
|---|---|
| Balance per books | Balance per bank |
| + Interest / credits earned not booked | + Deposits in transit (recorded, not yet cleared) |
| − Bank fees / NSF charges not booked | − Outstanding checks (issued, not yet cleared) |
| ± Book errors | ± Bank errors |
| = **Adjusted book balance** | = **Adjusted bank balance** |

The two adjusted balances must be identical. Only book-side items generate a journal entry (fees, interest, NSF, book errors); bank-side items are timing and self-clear next period. Rule of thumb: **checks reduce the bank side, deposits add to it; unbooked fees reduce the book side, unbooked credits add to it.**

### Reconciling-item taxonomy
- **Timing:** outstanding checks, deposits in transit, unposted receipts, in-transit intercompany. Self-clears; monitor aging.
- **Errors:** transposition (difference divisible by 9 — e.g., 540 vs 450 = 90), wrong account, duplicate, sign flip.
- **Omissions:** fee, interest, NSF, auto-debit, wire never booked.
- **Unidentified:** treat as a potential error/fraud until named; never sign off on it.

Diagnostic tricks: a difference divisible by **9** signals a transposition; a difference that is exactly **2×** a known item signals a sign flip (you added what you should have subtracted); an even, round difference often points to a duplicated or omitted whole entry.

### Reconciliation types and their source of truth
| Account | Reconcile GL to | Typical items |
|---|---|---|
| Cash | Bank statement | Outstanding checks, DIT, fees |
| AR | AR aging / subledger | Unapplied cash, credit memos, timing of billing |
| AP | AP aging / vendor statements | Received-not-invoiced (GRNI), disputes, timing |
| Inventory | Perpetual system / count | Shrinkage, in-transit, costing differences |
| Fixed assets | FA subledger / roll-forward | Additions, disposals, depreciation posting |
| Debt | Amortization schedule / lender statement | Interest split, principal paydown |
| Intercompany | Counterparty balance | In-transit, FX, mismatched postings |

### Roll-forward format (balance-sheet recs)
`Beginning balance + additions − reductions ± adjustments = ending balance`, and ending must equal the GL. This is the standard for FA, debt, allowance, accrual, and prepaid accounts — the movement, not just the point balance, is what an auditor tests.

### Aging thresholds and rigor
Classify reconciling items by age: **current** (this period, expected to clear), **30–60 days** (investigate), **60–90+** (presumed error, book or escalate). A stale timing item is almost always a missed entry. Match reconciliation rigor to account risk: high-risk / high-volume (cash, revenue-linked AR) get detailed line-level recs and independent review; low-risk stable accounts can use a review-type rec (analytic reasonableness) at lower frequency.

### Sign-off standard
"Reconciled" means residual = $0 **or** every residual dollar is a named, categorized, aged item with an owner and clearing plan. "Reconciled except $X" with no name is *not reconciled*. Segregate: the preparer and the reviewer/approver must be different people.
