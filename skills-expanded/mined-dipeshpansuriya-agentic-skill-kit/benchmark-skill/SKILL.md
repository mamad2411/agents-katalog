---
name: benchmark-skill
description: Score a skill against a baseline with a results CSV and scripted verdict (SHIP, FIX, KEEP) on triggers, quality, consistency and cost. Use when the user asks to benchmark, A/B compare, or regression-check a skill.
disable-model-invocation: true
---

# Benchmark a Skill (Advanced)

Prove, with numbers, whether version **B** is better than baseline **A**. Output: a filled results sheet, a scored report, and a verdict.

## Phase 1: Define the comparison
| Question | Options |
|---|---|
| What is **A** (baseline)? | No skill · previous version · separate skills (for merges) |
| What is **B** (candidate)? | New skill · edited version · merged skill |
| Goal? | New-skill value · regression check · merge decision |

Freeze both versions: label them (e.g. `A=v1.2`, `B=v1.3`) and don't edit during the run.

## Phase 2: Build the test set
Follow `references/test-set-design.md`. Minimum **15 cases**, mix:
- ~40% single-task · ~20% multi-task / multi-source · ~20% near-miss (must NOT trigger) · ~20% edge cases
- Pick 3 cases for **consistency** (run 3× each)
- Write the **expected result** for each case *before* running

Generate the results sheet (columns as in `templates/results-template.csv`):
```bash
python scripts/build_results_sheet.py <skill>/evals/test-cases.md --versions A B --repeat 3 --repeat-cases 1,2,3 -o results.csv
```

## Phase 3: Run
1. Run every case against A and B in **fresh sessions** (no carry-over context).
2. Record per run: triggered (1/0), routed correctly (1/0/blank), tokens, seconds.
3. Save every output (e.g. `outputs/<version>/<case>-<run>.md`) for grading and audit.
4. If available, use the `skill-creator` skill's eval runner to automate runs and variance.

## Phase 4: Grade
Use `references/grading-rubric.md`, 5 binary checks (0/1 each):
`q_format, q_facts, q_no_invent, q_rules, q_usable`
- Grade **blind** where possible: hide which version produced the output.
- Near-miss cases: quality columns blank; only trigger matters.
- Any invented fact means `q_no_invent = 0` **and** flag as a critical failure.

## Phase 5: Score & decide
```bash
python scripts/score_benchmark.py results.csv --baseline A --candidate B
```
The script computes trigger accuracy, precision, recall, false-trigger rate, routing accuracy, average quality, consistency, cost, per-type breakdown, and applies the decision rules in `references/metrics.md`.

## Phase 6: Report
Fill `templates/report-template.md`:
- Verdict first (SHIP / FIX & RETEST / KEEP BASELINE) with the 1–2 numbers that decided it
- Scorecard table, per-type breakdown, critical failures
- Top 3 fixes, each tied to failing case IDs
- Save the test set + results with date and version labels (the regression baseline for next time)

## Rules
- Never declare a winner from fewer than 15 cases or without near-miss cases.
- Never grade with knowledge of the version if a blind option exists.
- Any critical failure (invented data, leaked internal info, wrong audience) blocks SHIP regardless of averages.
- Report absolute numbers **and** differences (e.g. "4.2 → 4.6, +0.4").
- Differences of < 0.2 quality or < 5% trigger accuracy on small sets count as a **tie**; say so.
- Every recommended fix must cite the failing case IDs.
- Keep all raw outputs; the report must be reproducible.

## Self-check
- [ ] ≥ 15 cases, all 4 types present, expected results written first
- [ ] Both versions frozen and labelled
- [ ] Consistency runs done (3×3)
- [ ] Script run; numbers in report match its output
- [ ] Critical failures listed (or "None")
- [ ] Verdict follows `references/metrics.md` decision rules
