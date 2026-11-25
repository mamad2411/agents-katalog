---
name: expense-reconciliation
description: Reconciles submitted expense claims against the receipts and statements sitting in the mailbox, lists what is missing or unmatched, and drafts the chaser to each claimant. Use when the user asks to reconcile expenses, check expense claims, find missing receipts, chase expense documentation, or prepare the expense pack before a close.
---

# Expense Reconciliation

Finds the gap between what was claimed and what was evidenced, before someone else does.

## Inputs
- Mailbox, through **Email**, for receipts, card statements and claim confirmations
- A claims export the user supplies, through **Excel**
- `references/config.md` for the period, the materiality threshold and the policy rules to check

## Procedure
1. **Load the claims export.** If none is supplied, say so and stop: reconciliation without the
   claim side is not reconciliation, it is a receipt hunt. Offer that instead.
2. **Gather evidence** from the mailbox over the period: receipts, invoices, card statements.
3. **Match** each claim to evidence on amount, date within the config tolerance, and merchant.
   Record the match confidence as exact, probable or none.
4. **Classify every row**: `Matched`, `Amount differs`, `No receipt`, `Receipt with no claim`,
   `Possible duplicate`.
5. **Check policy** only against the rules written in config. Never invent a policy rule.
6. **Write** `/Documents/Cowork/output/expense-recon-<period>.xlsx`, unmatched rows first.
7. **Draft one chaser per claimant** covering all their gaps in a single message, not one per row.

## Output
| Claim ref | Claimant | Date | Amount | Merchant | Evidence | Match | Status | Policy flag | Source |

Then: counts by status, total value unmatched, claimants to chase, drafts prepared.

## Definition of done
Every claim carries a status, every unmatched row says why, and every claimant with a gap has one
drafted message.

**A clean reconciliation is the best outcome.** If everything matches, say that in one line with
the totals. Do not manufacture a policy flag to show effort.

## When there is no data
- No claims export: stop and say what is needed.
- Mailbox evidence missing for a period: state the window actually covered. Never present a
  partial period as complete.
- A statement is a PDF you cannot parse: list it as unread evidence rather than ignoring it.

## Boundaries
- **Draft, never send.** Chasers are drafts.
- Never approve, reject or adjust a claim. Never state a reimbursable amount as final.
- The expense system and the finance ledger are the source of truth. This reads mail.
- Never share a claimant's detail with anyone but the user and that claimant.

## Self-check
- Does every unmatched row name the missing evidence?
- Is every policy flag traceable to a rule in config?
- One chaser per claimant, not one per row?
- If it all matched, did I say so plainly?
