---
name: validate-data-quality
description: Defines and runs rule-based data-quality checks — completeness, uniqueness, freshness, range, referential integrity — using Great Expectations-style assertion frameworks.
when_to_use: When the user wants to guard data correctness with explicit rules — assert no nulls/dupes in key columns, enforce value ranges or referential integrity, check freshness/timeliness, or wire data-quality gates into a pipeline that fail loudly.
---

## When to Use

Use when the contract is known and you want to **assert** it, not discover it:

- Key columns must have **no nulls** / **no dupes** (PK or business key).
- Values must stay in a **range / enum / regex** (e.g. `price >= 0`, `status in (...)`, ISO date format).
- A child table must not reference **missing parent keys** (referential integrity), or a derived column must agree with its source (cross-column consistency).
- A table/feed must be **fresh** (max timestamp within SLA) or have an **expected row count** (volume not collapsed/exploded).
- You need a **gate** that blocks a bad load and exits non-zero in CI/the pipeline.

Distinct from exploratory profiling (`profile-dataset`): that one **describes** unknown data; this one **enforces** a known contract and fails. If you don't yet know the rules, profile first, then encode findings here as expectations.

## Steps

1. **Derive expectations, don't guess.** Pull rules from: (a) the schema/DDL (NOT NULL, UNIQUE, FK, CHECK, types), (b) stated business rules, (c) a prior profile run for value distributions. Write each as one named assertion with an explicit expected value. Resist "looks fine" smoke tests — every column in scope gets at least one rule or an explicit decision to skip it.

2. **Pick the engine, keep it native to the data location.**
   - Tabular / pandas / Spark, or you want a docs site + history → **Great Expectations** (`great_expectations`): build a `Validator` on a `Batch`, attach expectations, run a `Checkpoint`.
   - Warehouse-resident data → push rules down as **SQL** (`dbt test`, or hand-written `COUNT(*) WHERE <violation>`) so you never extract the full table.
   - Small/embedded → lightweight custom asserts (a list of `(name, fn, severity)` over the frame). Don't pull a heavy framework for 5 checks on a CSV.

3. **Map each rule to a check family + assertion:**
   - Completeness → `expect_column_values_to_not_be_null` (or `SELECT count(*) WHERE col IS NULL`). Report **null %**, not just a boolean.
   - Uniqueness → `expect_column_values_to_be_unique` / `expect_compound_columns_to_be_unique` for composite keys; or `GROUP BY key HAVING count(*) > 1`.
   - Validity → `expect_column_values_to_be_between` (range), `expect_column_values_to_match_regex`, `expect_column_values_to_be_in_set` (enum), `expect_column_values_to_be_of_type`.
   - Consistency / referential → `expect_column_pair_values_*`, or anti-join `child LEFT JOIN parent ... WHERE parent.key IS NULL`; cross-column `expect_multicolumn_sum_to_equal` / explicit predicate.
   - Freshness / volume → `expect_column_max_to_be_between(now - SLA, now)` on the timestamp; `expect_table_row_count_to_be_between(min, max)` for volume drift.

4. **Set severity per rule: hard-fail vs threshold.** A broken PK/FK is a **hard fail** (block). A "warn" tolerance (e.g. `mostly=0.99`, allow 1% null in a soft column) is a **threshold** — log it loud but optionally non-blocking. Be explicit about which rules are which; default new rules to hard-fail until proven noisy.

5. **Emit an actionable report.** For every failure include: rule name, expected vs observed, **violation count + %**, and a **sample of offending rows / values** (cap at ~5–10, never dump the table). Output machine-readable (JSON) so the gate can parse it, plus a human summary line. Aggregate to one final `PASS`/`FAIL`.

6. **Wire it as a gate.** The runner must **exit non-zero on any hard-fail** so the pipeline stops before the bad data lands. Run validation on the **post-transform / pre-load** batch (a staging table), not after it's already committed to the target. In dbt, fail the build; in a script, `sys.exit(1)`.

7. **Root-cause guardrail (mandatory).** When a check fails, fix the **data or the upstream producer** — never relax the assertion, widen the range, bump `mostly` down, or comment out the test to go green. A weakened assertion is a silent production bug. If a rule is genuinely wrong, change it deliberately with a recorded reason, not to dodge a red run.

## Common Errors

- **`mostly` masks real breakage.** `mostly=0.95` lets 5% violations pass silently. Use it only for known-soft columns; PK/FK/critical fields get `mostly=1.0`.
- **Nulls slip past range/regex checks.** Most validity expectations **skip nulls** by design. A column can pass `be_between` and `match_regex` while full of nulls — pair every validity rule with an explicit completeness rule.
- **Float / numeric-type range checks false-fail.** Comparing `Decimal` vs `float`, or NaN (`NaN` is never `>= 0`), throws off `be_between`. Normalize dtypes and decide NaN policy before asserting.
- **Uniqueness on a single column when the key is composite.** `(date, user_id)` unique ≠ `user_id` unique. Use the compound expectation or the dupes pass undetected.
- **Timezone-naive freshness.** `now()` local vs UTC timestamps makes a fresh feed look stale (or vice versa). Compare in one explicit tz.
- **Referential check on the wrong direction / before the parent loads.** Validate the child after parents are present, and anti-join child→parent (not the reverse), or you'll flag valid rows.
- **Validating the whole warehouse table in pandas.** Pulling millions of rows to assert in memory is slow and OOMs — push the check down as SQL `COUNT WHERE violation`.
- **Gate that reports FAIL but still exits 0.** The pipeline keeps going and the bad load lands anyway. Verify the exit code, not just the printed verdict.
- **Stale expectation suite after a schema change.** A renamed/dropped column makes the rule error or silently no-op. Treat the suite as code: update it with the schema, version it.

## Verify

1. **Inject a violation, confirm it's caught.** Add a known null/dupe/out-of-range/orphan-FK row (or use a tampered fixture); the runner must report it **and exit non-zero**. A suite that never fails on bad data proves nothing.
2. **Confirm clean data passes** — run on a known-good batch and get `PASS` with exit 0 (guards against an over-strict rule that fails everything).
3. **Check the count math:** reported violation count = an independent `SELECT count(*) WHERE <violation>`. They must match.
4. **Inspect the offending-row sample** in the report — the rows shown actually violate the rule (not a formatting artifact).
5. **Test the gate in place:** run inside the pipeline/CI with bad data and confirm the downstream load is **blocked**, not just logged.
6. **Grep the diff for weakened assertions** — no newly-lowered `mostly`, widened ranges, or commented-out checks were added to make the run green.
