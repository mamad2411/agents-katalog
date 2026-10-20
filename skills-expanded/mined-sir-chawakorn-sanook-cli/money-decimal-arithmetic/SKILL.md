---
name: money-decimal-arithmetic
description: Implements correct monetary and decimal arithmetic using integer minor units or arbitrary-precision decimals — per-currency exponents (ISO 4217), explicit rounding modes (banker's vs half-up), largest-remainder allocation that sums exactly, FX triangulation, NUMERIC storage, and locale-aware formatting — to eliminate float drift and off-by-a-penny totals.
when_to_use: Code does financial math — prices, totals, tax/VAT, discounts, interest, invoicing, splitting a charge across line items, multi-currency conversion, or rounding to cents; money is stored as float or summed with ad-hoc Math.round; totals are off by a cent; or you're choosing a money/decimal type (BigDecimal, Python decimal, dinero.js, rust_decimal). Distinct from numeric-precision-units (general float/units correctness, not currency-exponent/allocation/FX rules) and payments-billing-integration (drives PSP charge/subscription state, then calls this skill for the totals).
---

## When to Use

Reach for this skill when the bug or task is about **numeric correctness of money**, not throughput, schema, or float/units in general:

- "Total is off by a cent" / "tax doesn't add up to the sum of line items"
- "Split this $100 charge across 3 items / refund proportionally"
- "Store and compute prices, discounts, VAT, interest, invoice rounding"
- "Convert USD→JPY→EUR, what rate precision and rounding?"
- "We store amounts as `float`/`DOUBLE` — is that safe?" (no)
- Choosing a money/decimal type: `BigDecimal`, Python `decimal.Decimal`, `dinero.js`, `rust_decimal`, `js-joda`-style money libs

NOT this skill:
- General float pitfalls (epsilon/ULP compare, Kahan summation, NaN/Inf guards) or non-money unit conversion (metric/imperial, data sizes, angles) → numeric-precision-units (this skill is the money-specific specialization: ISO 4217 exponents, allocation, FX)
- Integrating a PSP, idempotent charges, subscription/proration, payment webhooks → payments-billing-integration (it owns billing *state*; it calls this skill for the rounding/allocation/FX math)
- Making a slow aggregate query fast → optimize-sql-query
- Detecting nulls/outliers/dupes in a dataset → validate-data-quality
- Picking column types / running a safe ALTER on a money column → db-migration-safety
- Reshaping/cleaning numeric columns in a dataframe → wrangle-tabular-data
- Serialization contract for an API field's type → rest-graphql-contract
- Writing the property tests themselves as a test suite → write-tests (this skill specifies *which* invariants; that one structures the suite)

## Steps

1. **Never use binary float for money. Pick the representation by language, not by habit.** Floats can't represent `0.10` exactly, so `0.1 + 0.2 === 0.30000000000000004` and `0.1 * 3 !== 0.3`. Two safe representations:

   | Representation | What it is | Use when | Watch out |
   |---|---|---|---|
   | **Integer minor units** | store cents as `int`/`bigint` (`$12.34` → `1234`) | default for fixed exponent, transactional ledgers, money over the wire | must track currency to know the exponent; intermediate math (interest, %) still needs a decimal/round step |
   | **Arbitrary-precision decimal** | base-10 type: Python `Decimal`, Java `BigDecimal`, .NET `decimal`, `rust_decimal`, JS `decimal.js`/`big.js` | rates, %, interest, tax with sub-cent intermediates, accounting needing >2 dp | set a context/precision; still must round to currency exponent at the boundary |

   Per language: **JS/TS** → `dinero.js` v2 or `big.js` (never `Number`); **Python** → `decimal.Decimal` (never `float`); **Java/Kotlin** → `BigDecimal` (never `double`); **.NET** → `decimal`; **Rust** → `rust_decimal::Decimal`; **Go** → `int64` minor units or `shopspring/decimal`; **Postgres** → `NUMERIC` (never `FLOAT`/`REAL`/`DOUBLE`).

2. **Model amount + currency as one value; respect the per-currency exponent.** A bare number is not money — `100` is meaningless without a currency, and the exponent varies by ISO 4217:

   | Currency | Exponent (minor digits) | `1.00` unit = |
   |---|---|---|
   | USD, EUR, GBP | 2 | 100 cents |
   | JPY, KRW, CLP | **0** | 1 (no cents) |
   | BHD, KWD, TND | **3** | 1000 fils |

   ```ts
   type Money = { amount: bigint; currency: string }; // amount in MINOR units
   // $12.34 → { amount: 1234n, currency: "USD" }  exponent 2
   // ¥1234  → { amount: 1234n, currency: "JPY" }  exponent 0
   // 1.234 BD → { amount: 1234n, currency: "BHD" } exponent 3
   ```
   Reject any binary op on two `Money` of different currencies — throw, don't coerce. Drive the exponent from an ISO 4217 table, never hardcode `2`.

3. **Decide and document ONE rounding mode; round only at boundaries.** The default sources disagree, so state it explicitly:
   - **Banker's rounding (half-to-even, `ROUND_HALF_EVEN`)** — default for statistical/aggregate fairness; removes the upward bias of always rounding `.5` up. Use for interest, large batches, GAAP/IFRS contexts. `2.5→2`, `3.5→4`.
   - **Half-up (`ROUND_HALF_UP`, "arithmetic")** — what invoices and most tax authorities expect for a single bill line. `2.5→3`. Many VAT rules mandate this per line.

   Pick **half-even as the engine default**, override to **half-up where a tax/billing rule requires it**, and write the chosen mode next to the code. **Carry full precision through the calculation; round exactly once, at the point you produce a displayable/storable currency amount** — never round intermediates, or errors compound.

4. **Allocate with largest-remainder so the parts sum EXACTLY to the whole.** Splitting `$100 / 3` as `33.33 × 3 = 99.99` leaks a penny. Distribute the remainder deterministically:

   ```python
   def allocate(total_minor: int, ratios: list[int]) -> list[int]:
       s = sum(ratios)
       shares = [total_minor * r // s for r in ratios]   # floor each
       remainder = total_minor - sum(shares)              # pennies left over
       # hand out the leftover pennies, one each, by largest fractional part
       order = sorted(range(len(ratios)),
                      key=lambda i: (total_minor * ratios[i]) % s, reverse=True)
       for i in order[:remainder]:
           shares[i] += 1
       return shares
   # allocate(10000, [1,1,1]) -> [3334, 3333, 3333]  sums to 10000 exactly
   ```
   Invariant: `sum(allocate(total, ratios)) == total`, always, for any total and ratios. Use this for splitting charges, proportional refunds, tax-inclusive line breakdowns.

5. **Fix tax/discount ordering and the rounding points — they change the total.** Decide and document:
   - **Discount before tax** (typical retail): `taxable = price − discount`, then `tax = round(taxable × rate)`.
   - **Round per line vs round on total**: per-line rounding (round each line's tax, then sum) and total rounding (sum exact line taxes, round once) can differ by cents. Most invoice/VAT regimes require **round per line**; pick one, document it, keep it consistent across the whole invoice.
   - **Tax-inclusive (gross) prices**: extract tax with `tax = round(gross × rate / (1 + rate))`; the net is `gross − tax` so the parts reconcile exactly.

6. **FX conversion — fix precision, direction, triangulation, and one round.** A rate is a high-precision decimal, not money. Rules:
   - Store rates at **≥6 significant decimal places** (`decimal`, not float); know the direction (`USD→EUR` rate vs its reciprocal — they are not 1/x to display precision).
   - Compute in full decimal precision: `target_minor = source_major × rate`, scaled to the **target** currency's exponent, then **round once** (half-even) to target minor units.
   - **Triangulate** through a base when no direct pair exists (`THB→base→JPY`); apply both legs in full precision and round only the final result, never the intermediate base amount.
   - Never round the source before converting; never reuse a stale/averaged rate when an exact contractual rate is required.

7. **Compare and test equality on the exact integer/decimal — never a float epsilon.** With minor units / decimals, `a == b` is exact; `abs(a−b) < 1e-9` is a code smell signaling float crept in. Equality must include currency: `{1234,"USD"} != {1234,"JPY"}`. Sort/compare amounts only within the same currency.

8. **Store as exact types; serialize as string, not float JSON.** Postgres `NUMERIC(precision, scale)` or `BIGINT` minor units — **never `FLOAT`/`DOUBLE`/`REAL`** (lossy) and never `MONEY` (locale-fragile, fixed scale). Over JSON, emit amounts as a **string** (`"12.34"`) or as integer minor units + currency code — a JSON number is an IEEE-754 double and silently corrupts ≥16-digit and some 2-dp values. Set the column scale to the currency's max exponent (3 to be safe across BHD/KWD).

9. **Display and parse via the locale layer, separate from the math.** Format only at the edge with `Intl.NumberFormat(locale, {style:'currency', currency})` (JS) / `babel.numbers.format_currency` (Python) / `NumberFormat.getCurrencyInstance` (Java) — these place the symbol, group separators, and minor digits per locale (`-1.234,56 €` vs `($1,234.56)`). When parsing user input, strip locale separators back to a canonical decimal/minor-unit value before any arithmetic; never `parseFloat` a formatted string.

10. **Lock the invariants with property tests** (delegate suite structure to write-tests; assert these properties): allocation sums to the whole; round-trip format→parse is identity in canonical units; conversion+inverse stays within one minor unit; commutativity/associativity of addition in the same currency; no operation produces a fractional minor unit.

## Common Errors

- **`float`/`double` anywhere in the money path.** `0.1 + 0.2 != 0.3`; sums drift over many rows. Fix: integer minor units or a base-10 decimal type end to end.
- **Hardcoding exponent `2`.** Breaks JPY (0) and BHD/KWD (3) — `¥1234` becomes `¥12.34`. Fix: read the exponent from an ISO 4217 table.
- **Rounding intermediates.** Rounding each step before the final means errors accumulate. Fix: full precision through the calc, round exactly once at the output boundary.
- **Naïve split (`total/n`, round each).** `100/3 → 33.33×3 = 99.99`, a penny vanishes. Fix: largest-remainder allocation (step 4); assert `sum == total`.
- **Mixing currencies in one operation.** Adding USD to JPY silently yields garbage. Fix: type `Money` with currency; throw on mismatch.
- **Unspecified/mixed rounding mode.** Half-even in one place, half-up in another → reconciliation gaps. Fix: one documented mode, override only where a tax rule mandates.
- **Float JSON for amounts.** `12.34` over the wire becomes `12.339999999999`. Fix: serialize as string or integer minor units + currency.
- **`FLOAT`/`MONEY` SQL columns.** Lossy or locale-fragile storage. Fix: `NUMERIC(p,s)` or `BIGINT` minor units.
- **`parseFloat` on a formatted string.** `"1.234,56"` (de-DE) parses to `1.234`. Fix: locale-aware parse to canonical units before math.
- **Float epsilon comparison.** `abs(a-b) < 1e-9` for money means float leaked in. Fix: exact integer/decimal compare, including currency.
- **Reciprocal FX assumption.** Treating `EUR→USD` as exactly `1/(USD→EUR)` introduces drift. Fix: store/quote each direction; round only the final converted amount.

## Verify

1. **No float in the money path:** grep the diff — no `float`/`double`/`Number(`/`parseFloat`/`FLOAT`/`DOUBLE` on monetary values; types are minor-unit integers or a base-10 decimal. Schema columns are `NUMERIC`/`BIGINT`, not `FLOAT`/`MONEY`.
2. **Exponent correctness:** format `1234` minor units in USD→`$12.34`, JPY→`¥1234`, BHD→`1.234` — the exponent comes from the currency, not a constant.
3. **Allocation sums exactly:** property test `sum(allocate(total, ratios)) == total` for thousands of random totals and ratio vectors, including `total/3`, `/7`, zero ratios, and a single element. Zero penny leaks.
4. **Single rounding boundary:** a chained calc (price × qty × (1−discount) × (1+tax)) rounds once and equals a hand-computed full-precision-then-round figure; intermediates carry sub-minor precision.
5. **Tax reconciles:** sum of per-line taxes equals the documented invoice total under the chosen per-line/total rule; tax-inclusive extraction satisfies `net + tax == gross` exactly.
6. **FX round-trip bounded:** convert `A→B→A` for many amounts; result is within 1 minor unit of the original (rounding only, no drift), and a triangulated path rounds only the final leg.
7. **Equality is exact:** money equality/compare uses no epsilon and treats different currencies as unequal; tests assert `{1234,"USD"} != {1234,"JPY"}`.
8. **Serialization is lossless:** amounts cross JSON/DB boundaries as string or minor-unit integer + currency; a `12.34`-as-float anywhere fails the check.
9. **Format/parse identity:** for a set of locales, `parse(format(x)) == x` in canonical units.

Done = no binary float touches money anywhere, every currency uses its ISO 4217 exponent, allocation/tax/FX sum to the whole with zero penny leak, rounding mode is documented and applied exactly once at each boundary, and amounts are stored and serialized as exact (NUMERIC/minor-unit/string) values — all proven by the property tests in checks 3–9.
