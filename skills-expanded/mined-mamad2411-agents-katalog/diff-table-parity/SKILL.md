---
name: diff-table-parity
description: Compares two tables or query results and diagnoses exactly how they differ — row counts, key set differences, per-column value mismatches — for migration and refactor validation.
when_to_use: When the user must prove two datasets match (or explain why they don't) — validate a data migration, regression-check an ETL change, or confirm a query refactor returns identical results, going past 'counts differ' to where/why/whether-expected.
---

## When to Use

Reach for this when the question is "are A and B the same data, and if not, exactly how do they differ?" Concrete triggers:

- Validating a data migration (old store -> new store) before cutover.
- Regression-checking an ETL/pipeline change: same inputs should yield same outputs.
- Confirming a query/view refactor returns identical results to the original.
- A `COUNT(*)` already differs and you need where + why, not just the delta number.

NOT this skill: asserting business rules on a single dataset (non-null, ranges, uniqueness, referential integrity) — that is validate-data-quality. This skill always compares **two** datasets against each other; it never decides whether either is "correct" in isolation.

## Steps

1. **Pin the comparison contract.** Before touching data, write down: the join key(s) that uniquely identify a row in both sides, the column set to compare, and the side names (call them A = baseline/source, B = candidate/target). If a natural key does not exist, find a deterministic composite key — never compare by row position/ordinal, ORDER BY is not a contract.

2. **Reconcile schemas first.** List columns on each side. Note columns only in A, only in B, and renamed pairs. Decide per column: compare, ignore (e.g. audit timestamps, surrogate auto-IDs), or normalize before compare (cast, trim, round). Comparing a `numeric(10,2)` against a `float8` raw will produce noise — align types now, not after you see mismatches.

3. **Row-set diff on the key.** Produce three buckets and their counts:
   - keys only in A (dropped/missing in B)
   - keys only in B (added/extra in B)
   - keys in both (candidates for value comparison)
   Use a `FULL OUTER JOIN ... ON a.key = b.key` and branch on `a.key IS NULL` / `b.key IS NULL`, or set operations (`EXCEPT` both directions). Capture a sample (10–20) of each non-empty bucket, not just the count.

4. **Column-value diff on the intersection.** For the in-both keys, compare each chosen column. For every column report: mismatch count, mismatch % of intersection, and 5–10 sample `(key, a_value, b_value)` triples. Use null-safe comparison (`IS DISTINCT FROM`, or `COALESCE` to a sentinel) so NULL-vs-NULL counts as equal and NULL-vs-value counts as a mismatch. Rank columns by mismatch % so the worst offender surfaces first.

5. **Classify every diff as expected or defect.** A raw mismatch list is not a verdict. Bucket each pattern:
   - **Expected/benign:** type coercion (`"1.0"` vs `1`), rounding/precision, timezone or `timestamptz` rendering, whitespace/case/collation, NULL-vs-empty-string, stable-but-different sort. Note the rule and move on.
   - **Real defect:** value drift, truncation, wrong mapping, dropped/duplicated rows, encoding corruption. These block parity.
   State the classification rule you applied so it is auditable, don't hand-wave "looks like rounding."

6. **Emit a parity verdict with evidence.** End with one of: PARITY (zero unexplained diffs), PARITY-WITH-NOTES (all diffs classified expected, list the rules), or FAIL (defects remain, list them with sample rows). Always attach the numbers: total A, total B, only-A, only-B, in-both, and per-column mismatch counts. A bare "tables match" is not an acceptable output.

7. **Scale for large tables.** Don't pull millions of rows into the agent. Tier the work:
   - Cheap gate: compare `COUNT(*)` and per-column aggregates (`SUM`, `MIN`, `MAX`, `COUNT(DISTINCT)`) — if these match, deep diff is often unnecessary.
   - Block hashing: `md5`/`xxhash` of concatenated normalized columns per row, then diff the hash sets; only materialize full rows for the keys whose hashes differ.
   - Sampling: if even hashing is too heavy, diff a deterministic sample (`WHERE abs(hashtext(key)) % 100 = 0`) and report it as a sample, not a proof.

## Common Errors

- **Float / precision false positives.** `=` on floating point flags rows that are equal to business precision. Round to the contract's scale (`round(x, 2)`) or compare `abs(a - b) < epsilon` before declaring a defect. The same trap hits `numeric` vs `double precision` and currency stored at different scales.
- **Plain `=` swallows NULL rows.** `a.col = b.col` is NULL (not true) when either side is NULL, so genuinely-differing NULL rows silently vanish from the mismatch count. Use `IS DISTINCT FROM` everywhere.
- **Key collision / non-unique join key.** If the "key" is not unique on one side, the join fans out and inflates both counts and mismatches — a 1:N join makes a clean migration look broken. Verify `COUNT(*) = COUNT(DISTINCT key)` on **both** sides before trusting any downstream number.
- **Non-deterministic ordering treated as a diff.** Two queries returning the same set in different order are at parity; comparing by position reports 100% mismatch. Always diff on the key, never on row order, and never assume `LIMIT` without `ORDER BY` is stable.
- **Collation / encoding / trailing whitespace.** `'café'` vs `'cafe'`, `'A '` vs `'A'`, or different Unicode normalization read as value defects. Normalize (trim, casefold, NFC) per the contract before classifying.
- **Comparing across a snapshot skew.** If A and B are read at different times and the source is still mutating, "diffs" are just new writes. Pin both reads to the same snapshot/transaction or a frozen extract.

## Verify

- Sanity arithmetic holds: `only_A + in_both = total_A` and `only_B + in_both = total_B`. If not, the join key is wrong or non-unique — stop and fix step 1/3.
- Re-run on identical input (A vs A) → must report PARITY with zero diffs. If a self-compare shows mismatches, your normalization or null-handling is broken, not the data.
- Every column flagged as defect has at least one concrete sample `(key, a_value, b_value)` attached; every column dismissed as expected names the classification rule.
- The final verdict is one of PARITY / PARITY-WITH-NOTES / FAIL with the full count table — never ship just a single number or "matches".
