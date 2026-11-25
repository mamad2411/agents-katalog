---
name: double-entry-ledger
description: >-
  Use when designing or changing a ledger, wallet, balance, journal, posting or account model, or
  any table that answers "how much does X hold or owe". Covers immutable journal entries, postings
  that balance per currency, balances derived from postings, account types and normal balances,
  period close, corrections by reversal, external references for idempotent posting, and a sample
  chart of accounts for a payments product. Triggers on a balance column, an UPDATE of an amount,
  a wallet or credits feature, a settlement or payout flow, a "balance is wrong" bug. Not for
  statutory accounting policy or tax treatment, which belong to an accountant.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Double-entry ledger

A balance column that gets updated in place is a cache without a source of truth. When it
drifts, nobody can say which transaction did it. A ledger records every movement as a balanced
entry, never edits it, and derives balances from the record. The invariant is cheap to enforce
and catches a whole class of bugs at the database.

## When to use

- A feature holds, moves or owes money or credits: wallets, balances, payouts, refunds, fees,
  prepaid credits, escrow, split payments.
- A table has a `balance`, `amount` or `credits` column that code updates in place.
- A bug report says a balance is wrong, negative, or does not match the processor.
- A settlement, payout or month-end process reads balances.

## Rules

1. **Journal entries are immutable.** No `UPDATE` or `DELETE` on entries or postings. A mistake
   is corrected by a reversal entry plus a new correct entry, both linked to the original. The
   database user that the application uses must not have update or delete rights on those tables.
2. **Every entry balances, per currency.** For each currency in an entry,
   `sum(debit amounts) == sum(credit amounts)`. Enforce it in code before the write and in the
   database (a deferred constraint trigger, or an append-only table with a nightly check that
   pages someone). An entry has at least two postings.
3. **A posting is a positive amount, a side and an account.** Store `amount_minor > 0` plus
   `side in ('debit', 'credit')`. Signed amounts invite sign bugs; if the codebase already uses
   them, document the convention once and enforce it with a check constraint.
4. **Balances are derived.** `balance(account) = sum(debits) - sum(credits)` for debit-normal
   accounts (assets, expenses) and the reverse for credit-normal accounts (liabilities, equity,
   revenue). A materialized balance is a cache: it has a rebuild job and a reconciler that
   compares it with the derived value and alerts on any difference.
5. **One currency per account.** A BRL wallet and a USD wallet are two accounts. Conversion is
   two entries through an FX account, with the rate recorded on the entry.
6. **Two dates on every entry.** `effective_date` is when the movement belongs in the books;
   `recorded_at` is when the system wrote it. Reports use the effective date. Late arrivals
   are visible because the two differ.
7. **Period close is a lock, not a report.** Keep `closed_through` per ledger. An entry with
   `effective_date <= closed_through` is refused. Adjustments post into the open period and
   reference the original. Reopening a period is a logged administrative action.
8. **Every entry carries an external reference.** The source event id, the processor
   transaction id or an idempotency key, with a unique index. Posting the same reference twice
   is a no-op that returns the existing entry.
9. **Model the real counterparties.** A payments product needs at least: cash at processor,
   receivable from processor, fees expense, in-transit or pending, customer liabilities, revenue.
   A payment is not "cash in"; it is a receivable until the processor settles it.
10. **Tenant isolation is an invariant.** Entries carry the tenant. Balances, reports and
    reconciliations never cross tenants. Test it.

### Sample chart for a payments product

| Code | Account | Type | Normal balance | Holds |
|---|---|---|---|---|
| 1010 | Cash at bank | Asset | Debit | Settled money in your bank |
| 1020 | Receivable from processor | Asset | Debit | Captured, not yet paid out to you |
| 1030 | In transit | Asset | Debit | Payout sent, bank not yet credited |
| 2010 | Customer balances | Liability | Credit | Money you hold for customers |
| 2020 | Refunds payable | Liability | Credit | Refunds approved, not yet sent |
| 4010 | Revenue | Revenue | Credit | Your fees earned |
| 5010 | Processor fees | Expense | Debit | Fees the processor charged you |

A card capture of 100.00 with a 2.90 processor fee, where you keep 5.00:
debit 1020 Receivable 97.10, debit 5010 Fees 2.90, credit 2010 Customer balance 95.00,
credit 4010 Revenue 5.00. Debits 100.00, credits 100.00.

## How to apply

1. Read the current model. List every column that stores an amount and every code path that
   writes it. Grep for `UPDATE ... SET balance`, `balance +=`, `amount =`.
2. Write the chart of accounts for the feature before any code. Name the accounts, their type
   and normal balance. Walk one happy path and one refund through it on paper until it balances.
3. Implement `post(entry)` with validation (rules 2, 3, 7, 8) as the only write path. No other
   code writes postings.
4. Implement `balance(account, as_of)` from postings. If a cached balance exists, add the
   reconciler before you ship.
5. Write the tests in the **Tests** section first. The vectors in `evals/vectors/` cover the
   invariants in a language-neutral way.
6. Migrate existing balances with an opening entry per account against an equity or
   migration account, dated the cutover date, with the old balance as the external reference.

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

- A balanced entry posts; an unbalanced one raises; an entry with one posting raises.
- Balanced per currency passes; balanced in total but not per currency raises.
- Zero or negative posting amounts raise.
- Entries and postings cannot be mutated after posting.
- Reversal: original plus reversal nets every account to its prior balance.
- Posting into a closed period raises; the adjustment in the open period succeeds.
- Same external reference twice returns the first entry and writes nothing.
- Trial balance: after random balanced entries, total debits equal total credits.
- Reference vectors: `skills/double-entry-ledger/evals/vectors/test_ledger.py` with
  `LEDGER_SOLUTION` pointing at your module. TypeScript: `ledger.test.ts` with `LEDGER_SOLUTION_TS`.

## Review checklist

- Is there exactly one write path for postings, and does it validate balance per currency?
- Can anything update or delete an entry? Including migrations and admin tools?
- Where do balances come from? If cached, where is the reconciler and what does it do on drift?
- Does a refund reverse through the same accounts the payment used?
- Is the processor modeled as a receivable, or does "paid" jump straight to cash?
- Is the external reference unique, and is the replay path tested?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| `UPDATE wallets SET balance = balance - 10` | No history, races, drift | Post an entry; derive the balance |
| Editing an entry to fix a typo | Audit trail lies | Reversal plus new entry |
| One `transactions` table with signed amounts and no counter-account | Cannot prove anything balances | Postings with two sides |
| Capture credited straight to cash | Cash overstated until payout | Receivable from processor |
| Balance check only in application code | Bypassed by a script or a bug | Database constraint or append-only plus checker |
| Period close as a flag nobody reads | Backdated entries change closed reports | Refuse writes before `closed_through` |

## References

- Martin Fowler, *Accounting Patterns*: Account, Entry, Accounting Transaction, Posting Rule.
- TigerBeetle documentation on double-entry data modeling: immutable transfers, two-phase transfers.
- Modern Treasury ledgers documentation: ledger accounts, entries, normal balances.
