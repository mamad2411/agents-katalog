---
name: fortax-reconciliation
description: Reconcile two sets of records that should agree and explain every difference before any adjustment - books vs return (GSTR-1/3B/2B vs registers, 26AS/AIS vs books), control account vs subledger (debtors, creditors, fixed asset register, stock), bank vs books, related-party / group balances, a trial balance that does not tie. Narrows the gap to rows, tests one cause at a time, categorises reconciling items, ages them and states what stays open. Typical asks - "difference nikalo", "2B aur books me farak kyun hai", "26AS match nahi ho raha", "TB tally nahi ho raha", "debtors ledger aur control account alag hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Reconciliation types, item categories, ageing and escalation adapted from anthropics/knowledge-work-plugins, https://github.com/anthropics/knowledge-work-plugins (Apache-2.0)"
---

# Reconciliation — find the difference, then explain it

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Verdict first: two records agree, or they differ by an exact amount made of named items plus an
unexplained balance. This skill helps prepare the working; the CA reviews and signs it off.

## The rule

**No adjustment before the cause is known.** A difference that is plugged, rounded away, or
"adjusted to match" is not reconciled — it is hidden, and it will surface in a notice.

This applies hardest when the difference is small. A Rs 118 gap is a wrong tax rate somewhere; a Rs 1
gap is a rounding rule you have not identified yet. Size is not evidence of harmlessness.

## Use an engine where one exists

| Pair | Do this |
|---|---|
| GSTR-2B vs purchase register | `fortax-gstr2b-reconciliation` (`fortax.py gstr2b`) — it matches; you judge its `_pairs_to_judge.json` |
| GSTR-1 / 3B vs sales register | `fortax-gstr1-and-3b` (`fortax.py gstr1`) |
| Bank statement vs books | `fortax-bank-statement-to-books` (`fortax.py bank`, then its BRS part) |
| Everything else | this skill, with the matching done in a script or a workbook with formulas (`fortax-xlsx-manipulation`) |

Numbers come from code: never add a column, compute a difference or count items by eye.

## When to use

Any two records that should agree and do not:

- GSTR-2B against the purchase register; GSTR-1 against the sales register; 3B against both.
- 26AS / AIS / TIS against the books or the computation.
- A trial balance that does not tie; a control account against its subsidiary ledger.
- A portal figure that differs from the working paper.
- Balances between related entities (holding / subsidiary, group companies, branches).
- A total that changed between two versions of your own file.

## Step 1 — state the difference exactly

Before anything else, write one line:

> As per <source A> Rs X; as per <source B> Rs Y; difference Rs Z (A - B), for <entity>, <period>.

Get the period, the entity and the sign right. Half of all "differences" are two documents covering
different months, or one figure inclusive of tax and the other not.

## Step 2 — narrow it before you explain it

Split the difference until it is a small set of rows, not one number:

- By month, then by party, then by invoice.
- By tax head — IGST, CGST, SGST, cess separately. A gap that vanishes when heads are separated is a
  classification issue, not a value issue.
- By status — matched, unmatched in A, unmatched in B, matched but different value.

Stop splitting when each remaining row can be explained on its own.

## Step 3 — the usual causes, checked in order

Check these before inventing a theory. Each is a fact you can confirm from the files:

| Cause | How you confirm it |
|---|---|
| Timing | The invoice exists in both, in different periods |
| Not filed by the supplier | Present in the register, absent from 2B; the supplier's return status says so |
| Wrong GSTIN or PAN | The party's identifier differs between the two records |
| Reverse charge, or ineligible credit | The entry is correctly excluded from one side by rule |
| Rate or head applied differently | Same taxable value, different tax split |
| Debit or credit note not carried through | One side nets it, the other does not |
| Rounding | The gap is under Rs 1 per line and matches the line count |
| Duplicate | The same invoice number appears twice on one side |

Typical causes by type of reconciliation are in the next section.

## Step 4 — one hypothesis at a time

State it in writing: "I think Rs Z is <cause>, because <the rows that show it>." Then test only that,
against the source document — not against your own earlier working. If it does not hold, say so and
take the next hypothesis. Never stack two guesses.

## Step 5 — when it still does not tie

After three explanations that do not hold, stop. Do not keep adjusting. Write the CA a short note: the
exact difference, the rows you isolated, what you ruled out and how, and what you would need to settle
it — usually a document, a supplier or party confirmation, or a portal download. An honest open
difference is a working paper. A forced tie is a liability.

## Reconciliation types

### Control account vs subledger

Compare the ledger control balance to the detailed subsidiary balance at the same date.

- Sundry debtors (control vs party-wise ageing), sundry creditors (control vs party-wise ageing).
- Fixed assets (ledger vs fixed asset register — Companies Act and Income-tax blocks separately).
- Inventory (stock ledger vs valuation / stock statement given to the bank).
- Prepaid expenses (ledger vs amortisation schedule); provisions and outstanding expenses (ledger vs
  the detail schedules).

Process: pull the control balance at period end; pull the subledger detail at the same date; compare
totals (they should match if posting is real-time); investigate differences.

Common causes: a journal passed directly to the control account and not in the subledger; subledger
transactions not yet posted to the ledger; timing of batch posting; a reclassification in the ledger
without the subledger; an import or interface error.

### Bank vs books

Use `fortax-bank-statement-to-books` Part B. In brief: bank balance; add deposits in transit; less
cheques issued not presented; add/less bank errors = adjusted bank balance. Book balance; add interest
and credits not recorded; less charges not recorded; add/less book errors = adjusted book balance.
Difference must be 0.00.

### Related-party and group balances

Balances between related entities should net to zero on consolidation and agree for the related-party
disclosure (AS 18 / Ind AS 24, s.188 Companies Act).

1. Pull the receivable/payable for each entity pair.
2. Compare A's receivable from B with B's payable to A.
3. Identify and resolve differences; confirm every transaction is recorded on both sides.
4. Check the elimination entries used for consolidation.

Common causes: one entity recorded it, the other has not yet (timing); different exchange rates;
classified as third-party on one side; disputed amounts or unapplied payments; different cut-off
practice; TDS deducted by the payer shown net on one side and gross on the other.

### Tax records vs books

- 26AS / AIS vs books: TDS credit by deductor TAN and section; income shown in AIS that is not in books;
  a deductor who deducted but filed against a wrong PAN. Confirm with the deductor's Form 16A.
- GST returns vs books: see the table above; for the annual view see `fortax-gst-annual-return`.

## Categorise every reconciling item

**Category 1 — timing differences.** Clear on their own in the normal cycle; no entry needed:
cheques issued not presented, deposits in transit, items posted in one system and pending in the other,
transactions awaiting approval. Expected to clear within a few working days.

**Category 2 — adjustment required.** Need a journal entry (prepare it with `fortax-journal-entry`):
unrecorded bank charges, unrecorded interest, recording errors (wrong amount, wrong ledger, duplicate),
missing entries, classification errors.

**Category 3 — requires investigation.** Cannot be explained yet: unidentified differences, disputed
items, aged items that should have cleared, the same unexplained difference every period. Investigate
the root cause, document it, escalate if unresolved.

## Ageing of open items

| Age | Status | Action |
|---|---|---|
| 0-30 days | Current | Monitor — within the normal cycle |
| 31-60 days | Ageing | Investigate — why has it not cleared |
| 61-90 days | Overdue | Escalate to the reviewer; document the investigation |
| 90+ days | Stale | Escalate to the CA / management; possible write-off or adjustment |

Report format:

| Item # | Description | Amount (Rs) | Date originated | Age (days) | Category | Status | Owner |
|---|---|---|---|---|---|---|---|

Compute the age with a formula (`=<period end> - <date>`), not by counting.

Trending: compare total open items with last period; flag if the total exceeds the materiality level,
if the count grows period on period, or if the same item recurs every period (a process problem).

## Escalation thresholds (illustrative — set with the CA for each client's size)

| Trigger | Example threshold | Escalate to |
|---|---|---|
| Single item | above Rs 1 lakh | Reviewer |
| Single item | above Rs 10 lakh | CA / partner |
| Total reconciling items | above Rs 25 lakh | CA / partner |
| Item age | over 60 days | Reviewer follow-up |
| Item age | over 90 days | CA / management |
| Unexplained difference | any amount | Cannot close — resolve or document as open |
| Growing trend | 3+ consecutive periods | Process fix |

## Good practice

1. **On time:** finish within the close timetable (typically 3-5 working days after period end, and
   before the return that depends on it).
2. **Complete:** reconcile every balance sheet account on a set frequency — monthly for material ones,
   quarterly for the rest.
3. **Documented:** preparer, reviewer, date, and a clear explanation of every reconciling item.
4. **Segregated:** whoever reconciles should not be the person who posts to that account.
5. **Followed through:** track open items to resolution; do not carry them forward indefinitely.
6. **Root cause:** for recurring items, fix the process that causes them.
7. **Standard:** the same template for every account.
8. **Retained:** keep reconciliations and support for the statutory period (books of account: 8 years
   under s.128 Companies Act; confirm for the entity and the tax law).

## Output

Into the client folder next to the inputs (`<Client>/<FY>/<GST|ITR|Bank|Audit>/`), with entity and
period in the name:

- A reconciliation sheet: matched, unmatched each way, value differences, with a `Source` column on
  every row and the category and age of every open item.
- A difference statement: opening gap, each explained item with its cause and amount, closing
  unexplained gap — all by formula.
- **Any unexplained balance is a blocker in your summary to the CA, not a footnote.**

## Credit

Reconciliation types, item categories, ageing and escalation are adapted from
anthropics/knowledge-work-plugins (Apache-2.0). Changed by Fortax: rewritten for Indian practice
(GST, 26AS, Companies Act, rupee thresholds) and merged with Fortax's find-the-difference method.
