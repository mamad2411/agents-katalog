---
name: interest-and-amortization
description: >-
  Use when code computes interest, installments, amortization schedules, accruals, late charges or
  an effective rate. Covers nominal versus effective rates, day-count conventions,
  constant-installment (Price) and constant-amortization (SAC) schedules, rounding each
  installment with the residual on the last one so principal sums exactly, accruing at a higher
  scale and rounding only when posting, prepayments, and the fields a total-cost disclosure needs.
  Triggers on a loan, BNPL, credit line, subscription proration, deposit yield or late fee
  feature, or an installment table that does not sum to the principal. Not for the legal formula
  of a jurisdiction's disclosed rate; an accountant or lawyer confirms that.
  Use it also when a schedule is said to be only for display, or when asked to force the last balance to zero.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Interest and amortization

Installment math goes wrong in three places: the rate is converted carelessly, the day count is
implicit, and each installment is rounded on its own so the schedule no longer sums to the
principal. Each error is a few cents per contract and a support ticket per customer.

## When to use

- A loan, credit line, buy-now-pay-later, financing or installment feature.
- Interest accrual on balances, deposits or arrears.
- Proration of a subscription or fee over a partial period.
- An installment table whose principal parts do not add up, or whose last installment is odd.
- A disclosure of total cost or effective rate.

## Rules

1. **Say what kind of rate it is.** A nominal annual rate of 12% compounded monthly gives a
   monthly rate of 1%. An effective annual rate of 12% gives `(1.12)^(1/12) - 1 = 0.9489%` a
   month. The contract and the code must name which one. Store the periodic rate as a decimal
   string with its basis.
2. **Name the day-count convention.** `ACT/365`, `ACT/360` and `30/360` give different
   interest for the same days. Pick one per product, write it in the contract type, and test it
   with a leap-year case.
3. **Compute in decimals at a scale higher than money.** Keep at least 10 decimal places during
   the calculation. Round only the values that become postings: an installment, an interest
   charge, an accrual at period end.
4. **Round per installment, settle the residual on the last one.** Round each installment with
   the named policy. The principal parts must sum to the principal exactly, so the last
   installment absorbs the rounding residual. The residual grows with the term and the rate
   (a 60-month schedule at 3.5% a month can differ by close to one currency unit on the last
   installment); show it in the schedule, never hide it. Test `sum(principal_parts) ==
   principal` and `final_balance == 0`.
5. **Price schedule (constant installment).** `pmt = P * i / (1 - (1 + i)^-n)`. For each
   period: `interest = round(balance * i)`, `principal = pmt - interest`, `balance -= principal`.
   The last period pays the remaining balance plus its interest.
6. **SAC schedule (constant amortization).** `amortization = round(P / n)` for all periods but
   the last, which pays the remainder. Interest per period is `round(balance * i)`. Installments
   decrease over time.
7. **Accrue daily, post at a boundary.** Daily accrual keeps a higher-scale running total; the
   posting at month end or at settlement rounds once. Never round the daily accrual and then sum
   the rounded values.
8. **Prepayment regenerates the schedule.** A partial prepayment reduces the balance; then
   either the term shortens or the installment drops. The contract says which. The new schedule
   starts from the actual balance and the actual date.
9. **Penalties and late interest are separate lines.** A late fee, a penalty rate and ordinary
   interest are different accounts with different rules. Never fold them into one number.
10. **Disclosure needs every cost.** Where the jurisdiction requires a total effective cost
    (APR in the US, CET in Brazil), fees, insurance and taxes enter the rate. The engineering
    part is to keep every cost as a separate, dated line so the disclosure can be computed and
    audited. The formula and the rounding of the disclosed figure are confirmed by an
    accountant or lawyer, not chosen by the engineer.

## How to apply

1. Write the contract type first: principal, periodic rate and its kind, day count, schedule
   type, number of periods, first due date, rounding policy. Everything the schedule needs and
   nothing it does not.
2. Implement the schedule as a pure function from the contract type to a list of rows:
   period, due date, installment, interest, principal, remaining balance. No I/O, no clock.
3. Write the tests in the **Tests** section first; the vectors in `evals/vectors/` give known
   values.
4. Post from the schedule rows. The ledger entry references the contract and the period.
5. Add the leap-year, the prepayment and the single-period cases before shipping.

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

- Price: principal 1,000.00 at 1% a month for 12 periods gives an installment of 88.85 under
  HALF_UP; principal parts sum to 1,000.00; the final balance is 0.
- SAC: the same contract gives amortization 83.33 for 11 periods and 83.37 in the last; first
  interest 10.00; first installment 93.33.
- Simple interest: 1,000.00 at 12% a year, ACT/365, for 30 days is 9.86.
- Single period: one installment equal to principal plus one period of interest.
- Leap year under ACT/365 versus ACT/360 gives different amounts, both asserted.
- Rounding policy visible: one case where HALF_UP and HALF_EVEN differ.
- Reference vectors: `skills/interest-and-amortization/evals/vectors/test_amortization.py` with
  `AMORT_SOLUTION` pointing at your module.

## Review checklist

- Which rate kind and which day count, and are both written in the contract type?
- Where is the single rounding point for each posted value?
- Does the schedule prove `sum(principal) == principal`?
- What happens on a prepayment, and is it tested?
- Are penalties, fees and interest separate accounts?
- Is the schedule a pure function, so it can be regenerated and compared?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| `annual / 12` for an effective annual rate | Overcharges by the compounding gap | Convert with `(1 + r)^(1/12) - 1` |
| Rounding each principal part independently | Schedule does not sum to principal | Residual on the last installment |
| Floats in the installment formula | Off by a cent on long terms | Decimal with high precision |
| Days computed as "30 per month" everywhere | Wrong on 28-, 29- and 31-day months | Explicit day-count convention |
| Interest, fee and penalty in one `charges` number | Cannot disclose or dispute | Separate lines and accounts |
| Schedule stored once and edited on prepayment | History lost | Regenerate from the new balance; keep both |

## References

- Day-count conventions as defined by ISDA (ACT/365 Fixed, ACT/360, 30/360).
- Standard annuity formula for constant-installment loans; constant-amortization schedules.
- Regulators' disclosure concepts: APR (US Truth in Lending), CET (Brazil, Banco Central).
