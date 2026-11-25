---
name: analyze
description: Full analysis workflow for a business problem — scoping the decision, profiling data, cross-database joins, segmentation/cohort/funnel/trend analysis, pressure-testing, and a written findings report. Use for any substantive business question.
---

# Analyze — Business Problem Investigation

Primary owner: `bi-analyst`. Args carry the question, e.g. `/analyze why is enterprise churn rising`.

## Procedure

1. **Frame the decision.** Restate as: "We are deciding ___; this analysis informs it by ___; the answer would change the decision if ___." If the user's question is exploratory ("tell me about our customers"), propose 3 sharp sub-questions and confirm direction.

2. **Plan.** Create `analyses/YYYY-MM-DD-<slug>/` with a `PLAN.md`: hypothesis tree, data needed, join strategy, expected outputs. Make each hypothesis **falsifiable** and rank them by expected impact × ease of checking — test the cheapest decisive one first rather than boiling the ocean. For multi-day-scale work, share the plan before executing.

3. **Find the source — by tier, in order.** (1) Does the question map to a metric in `knowledge/metrics-catalog.md`? Then get its SQL with `python scripts/run_metric.py "<name>"` (add `--segment <name>` for a defined population) and build on that — do not retype it. (2) If not, read the domain doc in `knowledge/domains/` for the governed mart, its grain, its standard hygiene filter, and its gotchas. (3) Only if neither covers it, go to staging or raw tables — and record that you did, because it sets the provenance tier. Don't bail to a lower tier early: "it needs a custom date range" or "it needs a join" are reasons to adapt the catalog SQL, not to abandon it. Check `knowledge/governance-policy.md` before selecting anything about people: aggregate in the warehouse, and never pull a `restricted` column row-level.

4. **Gather & profile.** Pull from sources per `knowledge/data-sources.md`. Profile every dataset before use: row counts, date coverage, key uniqueness, null rates. For **cross-database joins**: identify join keys, measure and report match rates, characterise the unmatched population (bias check). Materialise intermediates (local DuckDB/sqlite/parquet is fine) instead of repeated cross-system pulls.

5. **Analyse.** Apply the appropriate toolkit — trend with seasonality control, cohort, funnel, segmentation (cut by the dimensions that matter to {{COMPANY_NAME}}), contribution/mix-shift, benchmark vs target/prior/peer. Use canonical metric definitions from `knowledge/metrics-catalog.md` only. If the question is "did X cause Y" or "what was the impact of", a before/after comparison is not an answer — hand it to `/causal-analysis`, or label the finding as correlational (`analytics.md` Part 4).

6. **Pressure-test before reporting.** Different date window, different segment cut, denominator artifacts, Simpson's paradox on ratio comparisons, outlier sensitivity. Run the trap checklist in `analytics.md` Part 1 (Simpson's, base rate, inspection/collider sampling bias, regression to the mean) and the reporting hygiene checklist in `standards/reporting-standards.md` — including median-not-mean for skewed data and causal-vs-correlational labelling. Note which checks were run.

7. **Write `FINDINGS.md`** (per `standards/reporting-standards.md`):
   - **Answer** (1–3 sentences, decision-relevant)
   - **Key findings** (each: claim + quantified evidence)
   - **So what / recommendation**
   - **Methodology & queries** (everything reproducible from the folder)
   - **Caveats & open questions**
   - **Flagged side-findings** (anything important spotted off-topic)
   - **Provenance footer** — source tier (the *least* governed one used), data-through date and when freshness was checked, owner, review status

8. **Independent review.** Hand the folder to `analysis-reviewer` when the finding is leadership-bound or external, when it is surprising, when it rests on raw tables, or when money moves on it. Fix what it blocks, then update the footer's `Review:` field with the verdict and date. For a quick internal answer, self-check and say so in the footer (`Review: self-checked`) — never claim a review that did not happen.

9. **Hand off as needed.** Stakeholder-grade packaging → `insights-communicator` (`/make-deliverable`). Recurring need → propose a dashboard or summary table. Modelling opportunity → note it for `data-scientist`.

10. **Update memory.** New data quirks → `knowledge/data-sources.md` and the domain doc in `knowledge/domains/`. Methodological choices → `knowledge/decision-log.md`. If a stakeholder corrected the answer, that is an eval: `/eval add`.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
