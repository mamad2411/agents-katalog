---
name: numeric-precision-units
description: Prevents numeric-precision and units defects by enforcing epsilon/ULP/relative float comparison, Kahan/Welford stable accumulation, NaN/Inf and div-by-zero guards, checked/saturating integer arithmetic, lossless int64/decimal transport across JSON/JS/DB boundaries, and explicit unit-typed conversions with consistent rounding.
when_to_use: Code does scientific/statistical math, accumulates many floats, compares floats with ==, converts units (metric/imperial, time, data sizes, angles), or moves large integers/decimals across JSON/JS/DB/language boundaries; or bugs involve flaky float equality, NaN/Inf, silent overflow, or lost int64→double precision. Distinct from money-decimal-arithmetic (monetary rounding/allocation correctness) and validate-data-quality (schema/null/range checks).
---

## When to Use

Reach for this skill when the defect is about **the number itself** — its representation, precision, or unit — not its monetary rounding, schema, or business validity:

- "These two floats are equal but `a == b` returns false" / flaky test on a computed total
- "Summing a million values gives a different answer depending on order"
- "Mean/variance is wrong / NaN on large or near-equal data"
- "My int64 ID comes back rounded after a round-trip through JSON/JS"
- "A big integer turned into `1.0000000000000002e18` in the browser / spreadsheet"
- "Counter wrapped to a negative number" / `i32` overflow / cast truncated a value
- "We mixed meters and feet / ms and seconds / radians and degrees / KB(1000) and KiB(1024)"
- Division by a value that can be zero; `0.1 + 0.2 != 0.3`; signed-zero or `-0.0` surprises

NOT this skill:
- Monetary correctness — cents/`Decimal`, banker's rounding, splitting a charge so it sums exactly, FX → **money-decimal-arithmetic** (this skill keeps money *out* of binary float and intact across boundaries; that one does the rounding/allocation math)
- Duration/clock precision, monotonic vs wall-clock, leap seconds, DST math → **datetime-timezone-correctness** (this skill stores time as an integer; that one interprets it)
- Checking a field is present / in range / right type at ingest → **validate-data-quality**
- Configuring the compiler/linter to forbid implicit numeric coercion (tsconfig, mypy, clippy) → **type-safety-strict**
- Choosing `NUMERIC` vs `BIGINT` column types for a *schema migration* → **db-migration-safety**
- Declaring the wire shape of a number in an API (string vs int64 in the contract) → **rest-graphql-contract**
- Writing the test harness/property-test scaffolding itself → **write-tests**
- Making a `SUM` aggregate query fast → **optimize-sql-query**

## Steps

1. **Decide the representation first — float is a default, not a law.**

   | Domain | Use | Never |
   |---|---|---|
   | IDs, counts, timestamps (ns/ms) | integer (`int64`) | `double` (loses precision > 2^53) |
   | Physical/scientific measurement | `float64` (`double`) | `float32` unless memory-bound and tolerance allows |
   | Exact fractions / ratios | rational type or scaled integer | float |
   | Probabilities, weights, signals | `float64` | `float32` |
   | Money / currency | → defer to **money-decimal-arithmetic** | binary `float`/`double` |

   Rule: if two values must compare *exactly equal*, they must not be binary floats.

2. **Never `==` floats. Pick the tolerance by scale.** Absolute epsilon fails for large magnitudes; relative fails near zero. Use a combined check:

   ```python
   def close(a, b, rel=1e-9, abs_tol=1e-12):
       if a == b:                       # exact / both inf same sign
           return True
       if math.isnan(a) or math.isnan(b):
           return False                  # NaN is never close to anything
       return abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_tol)
   ```
   - Library defaults: Python `math.isclose(a, b, rel_tol=1e-9)`, NumPy `np.isclose`/`allclose`, Rust `approx::relative_eq!`, JS — write the above (no stdlib equivalent).
   - **Near zero, relative tolerance collapses** — that's why `abs_tol` exists; set it to the smallest difference you consider zero in your domain.
   - ULP comparison (`a` and `b` within N representable steps) only for low-level kernels where you control rounding mode — overkill for app code; use relative+abs.

3. **Accumulate stably — order and algorithm change the answer.** Naive left-to-right `sum` accumulates rounding error ∝ n·ε and suffers **catastrophic cancellation** when subtracting near-equal large numbers.
   - Summation: use **pairwise** (NumPy's `np.sum` already does this) or **Kahan/Neumaier compensated** summation for long running totals:
     ```python
     def kahan_sum(xs):
         s = 0.0; c = 0.0          # c = running compensation
         for x in xs:
             y = x - c
             t = s + y
             c = (t - s) - y
             s = t
         return s
     ```
   - Mean/variance: **never** `sum(x²)/n - mean²` (cancellation → negative variance / NaN). Use **Welford's online** algorithm:
     ```python
     n = 0; mean = 0.0; M2 = 0.0
     for x in data:
         n += 1
         d = x - mean; mean += d / n
         M2 += d * (x - mean)
     var = M2 / n            # population; M2/(n-1) for sample
     ```
   - Sort ascending by magnitude before summing wildly different scales if you can't use compensated summation.

4. **Guard special values at the source, not three layers downstream.**
   - Before any `/`: reject or branch on a zero/near-zero divisor (`if abs(d) < abs_tol: raise/return sentinel`). Float `x/0.0` yields `±inf`/`nan` *silently*; integer `/0` traps/UB.
   - Treat `NaN`/`Inf` as poison: one `NaN` propagates through every subsequent op and **every comparison with it is false** (including `nan == nan`). Validate inputs with `math.isfinite(x)` at boundaries; assert finiteness on outputs.
   - `-0.0 == 0.0` is true but `1/-0.0 == -inf` while `1/0.0 == +inf`; normalize with `x + 0.0` or `x == 0.0 ? 0.0 : x` when sign of zero leaks into results.
   - `log`/`sqrt`/`acos` domain: clamp inputs (`acos(min(1, max(-1, x)))`) — rounding can push a value to `1.0000000002` and yield `NaN`.

5. **Integer arithmetic: assume it overflows, prove it doesn't.** Fixed-width ints wrap (C/Go/Rust release/Java) or trap (Rust debug) or silently promote (Python/JS bignum-ish). Choose explicit semantics:

   | Need | Rust | Go/C | Java | Generic |
   |---|---|---|---|---|
   | Detect overflow | `checked_add` → `Option` | compare after op / `bits.Add64` | `Math.addExact` (throws) | check before/after |
   | Clamp at bound | `saturating_add` | manual `min`/`max` | manual | manual |
   | Intentional wrap | `wrapping_add` | default `+` | default `+` | mask |
   - **Narrowing casts lose data silently**: `(int32)bigLong`, `i64 as i32`, `Number → Int32`. Range-check before narrowing; never cast a length/ID down.
   - Multiplication overflows long before addition — `a*b` for two `int32` near 2^16 already wraps; widen to `int64` *before* multiplying.
   - `INT_MIN / -1` and `-INT_MIN` overflow; `abs(INT_MIN)` is still negative.

6. **Cross-boundary precision: the 2^53 trap is the #1 silent corruption.** JSON has one number type; JS `Number` is `float64` with exact integers only up to `2^53-1` (9007199254740991). Any `int64` above that **loses its low bits** the instant a JS/JSON parser touches it — no error.
   - **Send large ints and exact decimals as JSON strings.** Contract: `{"id": "9223372036854775807", "ratio": "12345.6789"}`. Parse to `BigInt`/`int64`/`Decimal` explicitly on each side.
   - Guard in JS: `Number.isSafeInteger(x)` before trusting any integer; use `BigInt` + a string-aware parser (`json-bigint`) when you can't change the wire format.
   - DB: `DOUBLE`/`FLOAT` columns are binary — IDs and exact decimals go in `NUMERIC(p,s)`/`DECIMAL`/`BIGINT`. Read them through a driver path that returns `Decimal`/string, not float (many drivers default to float for `NUMERIC` — configure it off).
   - Language interop (protobuf/Thrift/FFI): `int64`→language `long`/`BigInt`, never `double`; protobuf JSON mapping *already* encodes `int64` as string — keep it.

7. **Units: make the unit part of the type or the name — no bare numbers cross a function boundary.**
   - Suffix every quantity: `timeout_ms`, `dist_m`, `angle_rad`, `size_bytes`, `temp_c`. A parameter named `timeout` is a bug waiting to happen.
   - Convert through one explicit factor table; round **once, at the conversion**, to the target's precision — don't let conversions compound. Conventions that bite:

     | Domain | Trap | Rule |
     |---|---|---|
     | Data size | KB=1000 vs KiB=1024 | use IEC (`KiB/MiB`) for binary; label which |
     | Angle | trig functions take **radians** | convert `deg * π/180` at the edge |
     | Temperature | C/F is **affine** (offset), not a ratio | `F = C*9/5 + 32`, never `*9/5` alone |
     | Time | ms vs s vs ns | store epoch as int ns/ms; never float seconds |
     | Imperial | 1 mi = 1609.344 m (exact) | keep full-precision factors, round at end |
   - Dimensional consistency: only add/subtract same-unit quantities; multiply/divide changes the dimension (m/s · s = m). If a units library exists (`pint`, `uom`, `js-quantities`), use it; otherwise centralize factors in one module and unit-test round-trips.

## Common Errors

- **`if x == 0.1 + 0.2`** — false; `0.1+0.2 == 0.30000000000000004`. Use a tolerance compare (step 2).
- **`abs(a-b) < 1e-9` as a universal epsilon** — passes for tiny numbers, fails for `1e12`. Scale tolerance relatively (step 2).
- **`sum(sq)/n - mean**2` for variance** — catastrophic cancellation gives negative/NaN variance. Use Welford (step 3).
- **`json.parse` of `{"id": 9007199254740993}` in JS** — silently becomes `...992`. Send IDs as strings; `Number.isSafeInteger` guards.
- **Storing an int64 ID in `FLOAT`/`double`** — loses the low bits above 2^53 on round-trip. Use `BIGINT`/`NUMERIC` and an integer/string driver path (step 6).
- **`(int) (a * b)` with two int32s** — overflows before the cast even runs. Widen to int64 before multiplying (step 5).
- **`while (n != target)` on a float loop counter** — may never hit `target` exactly; loop forever. Iterate with an integer index, compute the float.
- **`nan == nan` to detect NaN** — always false. Use `isnan`/`isFinite`; sort/min/max with NaN present is also undefined.
- **`Math.sqrt(neg)` / `acos(1.0000001)`** — returns `NaN` from rounding overshoot. Clamp domain before the call (step 4).
- **Passing `deg` to `Math.sin`** — silently wrong, no error. Sin takes radians; convert at the boundary.
- **`°C → °F` as a pure scale (`*9/5`)** — drops the `+32` offset; temperature conversions are affine, not linear.
- **Mixing 1000- and 1024-based sizes** — "5 GB" disk vs "5 GiB" RAM differ by ~7%. Label and use IEC binary units.
- **Casting a `length`/`count`/`id` to a narrower int** — truncates above the bound with no error. Range-check or keep it wide.

## Verify

1. **Float equality:** every float comparison in the diff uses a tolerance helper (or compares a quantity that is provably integer/decimal). `grep -nE '==|!=' ` over float paths returns no bare float `==`.
2. **Accumulation:** sum a 1e6-element array forwards vs reversed vs Kahan — Kahan matches a higher-precision (`Decimal`/`float128`) reference within tolerance; naive may not. Variance of near-equal large values is ≥ 0 and finite (Welford), not NaN.
3. **Special values:** feed `0`, `-0.0`, `NaN`, `+Inf`, `-Inf`, and a near-zero divisor through each public function — none crash silently; divide-by-zero is rejected or returns a documented sentinel; outputs pass an `isfinite` assertion.
4. **Integer bounds:** test at `MAX`, `MAX-1`, `MIN`, `0`, `MIN/-1` for every fixed-width arithmetic op — overflow is detected/saturated/intentionally-wrapped per the chosen semantics, never an undocumented wrap. Narrowing casts reject or clamp out-of-range input.
5. **Boundary round-trip:** serialize the value `9223372036854775807` (`int64` max) and a `12345.6789` decimal to JSON, parse on the other side (especially JS) → byte-identical value restored. `Number.isSafeInteger` is checked on any JS integer path.
6. **DB round-trip:** write `NUMERIC(38,9)` max-precision values and an int64-max ID, read back → equal as `Decimal`/integer/string (not float-coerced). No ID or exact-decimal column is `FLOAT`/`DOUBLE`.
7. **Units:** round-trip every conversion (`m→ft→m`, `C→F→C`, `KiB→bytes→KiB`) returns the original within rounding tolerance; trig inputs are radians; affine conversions keep their offset; mismatched-unit add/subtract is impossible (typed) or covered by a failing-on-mix test.
8. **Property tests:** generators include extremes (`±MAX`, `±0.0`, `NaN`, `Inf`, subnormals, near-epsilon pairs, overflow boundaries) — not just typical mid-range values.

Done = no bare float `==`, no ID/exact-decimal in binary float, every cross-boundary int64/decimal survives a JSON/JS/DB round-trip bit-for-bit, all fixed-width integer ops have defined overflow behavior, divide-by-zero and NaN/Inf are guarded at the boundary, and every unit-bearing quantity is named/typed with its unit and round-trips through conversion within tolerance.
