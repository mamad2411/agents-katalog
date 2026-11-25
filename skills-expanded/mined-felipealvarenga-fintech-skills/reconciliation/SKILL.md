---
name: reconciliation
description: >-
  Use when code compares two or more records of the same money: ledger against processor report,
  processor against bank statement, invoices against payments, internal balances against a
  partner's. Covers normalizing each source, tiered deterministic matching (reference first, then
  amount and date window, then explicit grouping rules), one-to-one by default, breaks with reason
  codes and owners, immutable run results, and the metrics that show whether reconciliation is
  healthy. Triggers on a payout or settlement report, a bank feed, a "the numbers do not match"
  ticket, a month-end close task. Not for deciding the accounting treatment of a break; it routes
  the break to a person.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Reconciliation

Reconciliation is how a system proves its books agree with the outside world. Done badly, it is
a spreadsheet someone fixes by hand every month. Done well, it is a deterministic job that
matches what it can, explains what it cannot, and never edits a record on its own.

## When to use

- A processor settlement or payout report arrives and must be tied to captured payments.
- A bank statement or feed must be tied to expected payouts and fees.
- Invoices must be matched with incoming payments.
- A partner, marketplace or custodian sends a balance or activity report.
- Month-end close, or any "our number is X, theirs is Y" problem.

## Rules

1. **Normalize every source into the same line shape.** `source, id, date, amount_minor,
   currency, reference, description, raw`. Keep `raw` so a human can see the original. Do the
   normalization in one adapter per source with its own tests.
2. **Match in tiers, in a fixed order, deterministically.** Tier 1: same reference, amount and
   currency. Tier 2: same amount and currency, date within an explicit window (for example two
   business days), earliest first. Tier 3: explicit grouping rules only (one payout equals many
   captures minus fees), written as code with a name. The output names the tier that matched
   each pair. Sort inputs before matching so two runs on the same data give the same result.
3. **One-to-one by default.** A line matches at most one line on the other side. Duplicated
   amounts match duplicated amounts, never one line twice. Many-to-one happens only in a named
   tier 3 rule.
4. **Tolerances are explicit and small.** A date window is a parameter. An amount tolerance,
   if any, is a parameter with a reason (FX rounding on a specific source) and shows up in the
   match record. "Close enough" is never a default.
5. **Breaks carry a reason code and an owner.** `timing` (expected to clear), `fee` (known
   deduction not yet booked), `fx` (rate difference), `missing_ours`, `missing_theirs`,
   `duplicate`, `unknown`. A break has an age. Unknown breaks older than the window page a
   person.
6. **The job never writes to the ledger.** It produces matches and breaks. A human, or a
   separately approved rule, posts the correcting entry, which references the break.
7. **Every run is a record.** Store the inputs' hashes, the parameters, the matched pairs, the
   breaks and the metrics, immutable, with the run time. The month-end evidence is that record.
8. **Run daily, on the whole open window.** A break that was `timing` yesterday may be
   `missing_theirs` today. Rerunning on the full window keeps reason codes honest and keeps
   the oldest-break age visible.
9. **Publish four metrics.** Match rate by count and by amount, break count by reason, oldest
   open break age, and amount in `unknown`. These go on a dashboard and have thresholds.
10. **Fees and FX are lines, not noise.** A processor report nets fees inside the payout; book
    the fee line so the payout matches gross captures minus booked fees. Same for FX
    differences: a separate line with the rate, never a tolerance that hides it.

## How to apply

1. Get one real file from each source (with real data removed or masked) and write the
   adapter and its tests first.
2. Define the window, the tiers and the grouping rules for this pair of sources in a small
   config object, checked into the repo.
3. Implement `reconcile(ours, theirs, config) -> RunResult` as a pure function. No database,
   no clock, no network inside it.
4. Write the tests in the **Tests** section. The vectors in `evals/vectors/` cover the
   matching invariants.
5. Wire the run to storage and to the dashboard. Add the oldest-break alert before shipping.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Reference match beats a date match when both are possible.
- Date window: inside matches, one day outside does not.
- Two identical amounts on each side produce two matches, not one line matched twice.
- Currency mismatch never matches, even with equal amounts.
- Shuffled input gives the same matches and breaks as sorted input.
- Every id appears at most once across matches and unmatched lists; nothing is lost.
- A fee line nets a payout against its captures in a named tier 3 rule.
- Reference vectors: `skills/reconciliation/evals/vectors/test_reconcile.py` with
  `RECON_SOLUTION` pointing at your module.

## Review checklist

- Is the matching pure and deterministic? Where is the sort?
- Can a line match twice? Where is that prevented?
- What is the date window, and who approved it?
- Which reason codes exist, and which one pages a person?
- Does the job write anywhere except its own run record?
- Where are the four metrics, and what are the thresholds?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Fuzzy amount tolerance by default | Real breaks hidden | Explicit per-source tolerance with a reason |
| Matching by amount only | Wrong pairs when amounts repeat | Reference tier first, date window second |
| Auto-posting adjustments | Ledger edited by a heuristic | Breaks routed to a person; entries reference the break |
| Spreadsheet export as the record | No audit trail, not repeatable | Immutable run record with input hashes |
| Monthly run only | Breaks age a month before anyone looks | Daily run over the open window |
| Fees netted into "difference" | Revenue and cost both wrong | Book fee lines; match gross minus fees |

## References

- Processor settlement and payout report documentation (Stripe balance transactions, Adyen settlement details) for the shape of real inputs.
- Internal audit guidance on account reconciliations: preparer, reviewer, evidence, aging of reconciling items.
