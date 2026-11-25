---
name: money-arithmetic
description: >-
  Use when code stores, adds, multiplies, allocates, converts, rounds, parses or formats amounts
  of money. Covers integer minor units with an explicit currency, ISO 4217 exponents (0, 2 and 3
  decimals), one named rounding policy applied at one point, largest-remainder allocation so the
  parts always sum to the whole, rate application, currency conversion, and the wire format for
  amounts. Triggers on a new amount, price, balance, fee or rate column, field or type; on
  splitting an amount between parties; on an amount that is off by one cent. Not for tax or
  statutory rounding rules, which depend on the jurisdiction and belong to an accountant.
  Use it also when the request says to keep floats or to patch a cent drift with round().
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Money arithmetic

Money bugs are silent. A sum drifts by one cent, a split loses a unit, a three-decimal currency
is treated as two decimals, and nobody sees it until a reconciliation or a customer complaint.
This skill fixes the representation and the arithmetic once, so the rest of the system can trust
them.

## When to use

- A change adds or touches a column, field or type that holds an amount, price, balance, fee or rate.
- Amounts are summed, multiplied by a rate, split between parties, converted between currencies,
  parsed from input or formatted for display.
- A new currency is added, or an amount crosses a boundary: an API, a file, a queue, a report.
- A figure is "off by a cent" or a reconciliation shows a sub-unit difference.

## Rules

1. **An amount is an integer count of minor units plus a currency code.** Never a float, at any
   hop: not in memory, not in the database, not in JSON, not in an analytics job. A `Decimal`
   with explicit scale is acceptable inside a calculation; the stored and transported form is the
   integer.
2. **The exponent comes from ISO 4217, per currency.** USD, EUR and BRL have 2 decimals. JPY,
   KRW and CLP have 0. BHD, KWD and TND have 3. Keep the table in one module and refuse an
   unknown currency at validation. Never hardcode "cents" or "divide by 100".
3. **Pick the scale once.** A ledger that stores 2 decimals cannot later store 3 without a
   migration of every row. If any product needs sub-cent precision (interest accrual, FX, usage
   billing), store a higher fixed scale from day one and round only at the presentation or
   settlement boundary.
4. **One rounding policy, named, applied at one point.** Say `ROUND_HALF_EVEN` or
   `ROUND_HALF_UP` in the code and in the spec. Round when a value leaves the calculation (an
   installment, a fee, a converted amount), not in the middle of it. Two roundings in one flow
   produce a drift that no test catches by accident.
5. **Allocation keeps the sum.** To split 100 into three equal parts, do not compute 33.33 three
   times. Use the largest-remainder method: floor every share, then hand the leftover units one
   by one to the shares with the largest remainders, ties broken by position. The parts sum to
   the whole every time, for every currency, for negative amounts too.
6. **Rates are decimals from a string, never floats.** `Decimal("0.0315")`, not `0.0315`.
   Apply the rate to the integer amount inside a `Decimal` context, then round once.
7. **Conversion is an explicit step with a recorded rate.** Store the rate, its source and its
   timestamp beside the converted amount. Never compare or add amounts of different currencies.
   The type system or a runtime check must refuse it.
8. **Validate at the boundary.** Parsing `"12.345"` as USD is an error, not a rounding. Reject
   more decimals than the exponent allows, reject `NaN` and infinities, reject amounts outside the
   business range.
9. **The wire format is unambiguous.** Send `{"amount": 1234, "currency": "USD"}` (integer minor
   units) or `{"amount": "12.34", "currency": "USD"}` (decimal string). Never a JSON number with
   a decimal point. Document which one the API uses and keep it.
10. **Formatting is the last step and is locale work.** `from_minor(1234, "USD")` gives `"12.34"`;
    a locale layer turns it into `US$ 12,34` or `$12.34`. Never parse a formatted string back into
    an amount.

## How to apply

1. Find every place the change touches an amount. Grep for `float`, `/ 100`, `* 100`, `round(`,
   `toFixed`, `parseFloat`, `Number(` near money names.
2. Put the currency table and the arithmetic in one module (`money.py`, `money.ts`). Everything
   else imports it.
3. Write the tests from the **Tests** section before the implementation. Use the vectors in
   `evals/vectors/` of this skill as a start; they are language-neutral cases.
4. Implement against the integer representation. Convert at the edges only.
5. Run the tests. Then grep again for the patterns in step 1 and remove every float path.

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

- Round trip: `to_minor(from_minor(x, ccy), ccy) == x` for currencies with 0, 2 and 3 decimals.
- Parsing refuses too many decimals: `to_minor("12.345", "USD")` raises.
- Unknown currency is refused at validation.
- Allocation: for random amounts (including negatives) and random ratio lists, the parts sum to
  the whole and each part is within one unit of its exact share. Zero ratios get zero.
- Mixed currency addition raises.
- Rate application rounds with the named policy: `apply_rate(1000, "0.0325")` is 32 under
  HALF_EVEN and 33 under HALF_UP. Both assertions in the suite, so the policy is visible.
- Conversion returns an integer in the target exponent: 1000 USD minor at 150.5 JPY/USD is
  1505 JPY.
- The reference vectors: `skills/money-arithmetic/evals/vectors/test_money.py`. Point the
  `MONEY_SOLUTION` environment variable at your module and run `pytest`. TypeScript:
  `money.test.ts` with `MONEY_SOLUTION_TS` and `npx vitest run`.

## Review checklist

- Where is the exponent table, and is it the only one?
- Which rounding policy, and where is the single rounding point?
- Does any allocation use plain division?
- Can two currencies meet in an `add` or a comparison without an explicit conversion?
- Is there a float anywhere between input and storage? Including the ORM default type?
- Does the API document integer minor units or decimal strings, and does it stay consistent?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| `amount: float` in a model | 0.1 + 0.2 is not 0.3; sums drift | `amount_minor: int` plus `currency: str` |
| `total / 3` for a split | Lost or invented cents | Largest-remainder allocation |
| `round(x, 2)` in several places | Double rounding, drift | One named policy at one point |
| `cents = dollars * 100` for every currency | JPY and BHD are wrong | Exponent from the ISO table |
| JSON `12.34` | Parsed as a float downstream | Integer `1234` or string `"12.34"` |
| Rate as a float literal | `0.0315` is not exactly representable | `Decimal("0.0315")` |
| Comparing USD and BRL balances | Meaningless result | Type or runtime check refuses it |

## References

- ISO 4217 currency codes and minor unit exponents, maintained by SIX Financial Information.
- Martin Fowler, *Patterns of Enterprise Application Architecture*, the Money pattern and allocation.
- Stripe API: amounts are integers in the smallest currency unit; zero-decimal currencies are listed.
