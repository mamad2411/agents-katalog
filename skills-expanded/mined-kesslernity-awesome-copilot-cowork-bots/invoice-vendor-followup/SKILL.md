---
name: invoice-vendor-followup
description: Finds invoice and payment threads in the mailbox that have gone unanswered, ages them, and drafts the follow-up to each counterparty. Use when the user asks what invoices are outstanding, which vendors have not replied, to chase payment or payment queries, or to prepare the aged follow-up list before a finance review.
---

# Invoice & Vendor Follow-up

Finds the invoice threads that stopped, with age and amount, and drafts the nudge.

## Inputs
- Mailbox, through **Email**
- `references/config.md` for the ageing buckets, the chase ladder and who is never chased

## Procedure
1. **Find invoice threads** over the window: invoices sent or received, payment queries, disputes,
   remittance advice.
2. **Determine the state of each thread** from the last message only: awaiting their reply,
   awaiting ours, resolved, or ambiguous. Ambiguous is a valid answer and must not be guessed.
3. **Age** from the last message in the thread, not from the invoice date, and bucket by config.
4. **Extract** counterparty, invoice reference, amount as written, direction (we owe / they owe),
   last contact date, who spoke last, and the source link.
5. **Rank** by age within direction. Money we owe sits above money owed to us, because a missed
   payable costs a relationship and a late receivable costs interest.
6. **Draft one follow-up per counterparty**, at the ladder step matching the age bucket.

## Output
| Counterparty | Ref | Amount | Direction | Last contact | Age | Waiting on | Ladder step | Source |

Then: totals by direction and bucket, threads marked ambiguous and why, drafts prepared.

## Definition of done
Every open thread is aged and attributed to a side, ambiguous ones are named rather than forced,
and every counterparty due a chase has one draft.

**Nothing outstanding is a good week.** Say it in one line.

## When there is no data
- No invoice threads in the window: say so, state the window, stop.
- A thread with no amount anywhere: list it with amount UNKNOWN rather than dropping it.
- A thread where the last message is an automated receipt: treat as awaiting their reply and say
  the attribution came from an automated message.

## Boundaries
- **Draft, never send.** Especially never send a chase to a counterparty on the config exclusion
  list, which exists for relationships being handled by a person.
- Never state an amount as owed. The ledger is the source of truth.
- Never escalate a ladder step on your own. The user chooses the step.
- Never contact anyone outside the organization without approval.

## Self-check
- Is every age measured from the last message, not the invoice date?
- Is every ambiguous thread labelled rather than guessed?
- Did I keep exclusions out entirely?
