---
name: fintech-ledger
description: Ledger specialist. Owns double-entry accounting, postings, balances, multi-currency, and ledger invariants. Auto-invoked for any code that posts to the ledger, computes balances, or models money movement.
---

# Fintech Ledger

The ledger is the source of truth for money, and money bugs compound silently
until reconciliation day. Every money event is two or more entries that sum to
zero; the journal is append-only; balances are derived, never authoritative.

## When to reach for this

- Designing or extending a chart of accounts or posting rules
- Writing code that posts entries, reverses transactions, or computes balances
- Adding multi-currency support, FX revaluation, or rounding logic
- Reviewing a money-movement feature for ledger invariant violations

## Principles

1. **Append-only journal — no UPDATE, no DELETE, ever.** Enforce at the database
   layer (revoke UPDATE/DELETE, or a trigger that raises), not by convention.
2. **Balances are projections.** Compute from entries; a cached balance is an
   optimization with a verification job, never the source of truth.
3. **Integers in minor units.** Store amounts as integers of the currency's
   smallest unit using the ISO 4217 exponent (USD: 2, JPY: 0, BHD: 3). Floats
   in a money path are a defect, full stop.
4. **Every posting balances per currency.** Debits = credits within each
   transaction *and each currency*; cross-currency moves go through explicit FX
   conversion accounts, never an implicit rate baked into one entry.
5. **Idempotent posting API.** A client-supplied idempotency key with a unique
   constraint; replay returns the original result, not a duplicate posting.
6. **Reversals post, never delete.** A reversal is a new compensating
   transaction that links to the original. History shows both.
7. **Rounding is a written policy applied once.** Pick the rule (banker's vs
   half-up), pick the layer, and route remainders to a dedicated rounding
   account so the books still sum to zero.

## Posting spec per event type

For each money event, write the spec before the code:

| Event | Debit | Credit | Idempotency key source |
|---|---|---|---|
| Customer deposit | `cash:settlement` | `liability:customer:{id}` | provider transfer ID |
| Internal transfer | `liability:customer:{from}` | `liability:customer:{to}` | client request ID |
| Fee charged | `liability:customer:{id}` | `revenue:fees` | invoice line ID |
| Reversal | mirror of original | mirror of original | `reversal:{original_tx_id}` |

A worked double-entry schema (accounts, transactions, entries, the sum-to-zero
and append-only constraints, balance queries, and an invariant test checklist)
is in [`references/double-entry-schema.md`](references/double-entry-schema.md).

## Pitfalls

- Storing a mutable `balance` column and treating it as truth (derive it; verify caches against the journal)
- Floating-point or decimal-string arithmetic in posting paths
- One-sided "adjustment" entries that make the books stop summing to zero
- Idempotency implemented as check-then-insert instead of a unique constraint (race window = double posting)
- FX conversion as a single two-leg entry at an undocumented rate — no audit path for where the spread went
- Tests that assert balances but never assert the per-transaction sum-to-zero invariant

---
*Related: `fintech-audit-trail` (immutable record of who posted),
`fintech-compliance` (postings that trip monitoring rules), `fintech-risk`
(exposure computed from balances) · domain agent: `fintech-architect` (rails and
money-movement topology) · output/ADR format: `playbook-conventions`*
