---
name: causal-analysis
description: Estimate the causal effect of a change that was not run as an experiment — a price change, a launch, a policy, a campaign — using difference-in-differences, synthetic control, interrupted time series, regression discontinuity, or matching, with the identifying assumption tested and the conclusion worded to the strength of the evidence. Use for "did X cause Y", "what was the impact of", and "what would have happened without".
---

# Causal Analysis — What Did The Change Actually Do?

Owner: `data-scientist`, with `bi-analyst` for the data and `analysis-reviewer` before it ships. Args name the change and the outcome, e.g. `/causal-analysis impact of the March Starter price rise on churn`.

Read `analytics.md` Part 4 first. It is the method reference; this skill is the procedure.

**If the change has not happened yet, stop and use `/experiment`.** A randomised test answers the question directly, and every method below is a substitute for one. Say so before doing anything else.

## Procedure

1. **Frame the decision.** What will be done differently depending on the answer — roll back, extend, repeat? If nothing, a descriptive before/after labelled as such is enough; say so and stop.

2. **Write the three lines** in `analyses/YYYY-MM-DD-<slug>/PLAN.md`:
   - **Treatment:** exactly what changed, for which units, on what date. Get this from the change ledger in `knowledge/business-context.md` and `knowledge/decision-log.md`, not from memory. A treatment date that is off by a week moves the answer.
   - **Counterfactual:** what will stand in for "no change".
   - **Identifying assumption:** the one thing that must be true, in plain English.

3. **Data before method.** Confirm with `data-quality-engineer` that the outcome metric is trustworthy across the whole window — freshness, row counts, definition changes, tracking changes. A tracking change on the treatment date is the most common "effect". Use the catalog definition of the outcome.

4. **Choose the design from how the change was rolled out** — not from which method is familiar:

   | The change reached… | Design |
   |---|---|
   | some groups and not others, at one time | difference-in-differences |
   | groups at different times | staggered difference-in-differences (compare to not-yet-treated) |
   | one unit or a few (a country, a region) | synthetic control |
   | units above or below a threshold | regression discontinuity |
   | everyone at once, with a comparison series unaffected | difference-in-differences against that series |
   | everyone at once, no comparison at all | interrupted time series — the weakest; say so |
   | units that self-selected | matching / regression adjustment — rung 3 evidence at best |

   If no design fits, report that the effect cannot be identified from this data, and what would make it identifiable (a holdout next time, a staggered rollout). That is a real finding.

5. **Test the assumption before estimating anything.** Plot the pre-period. For DiD: parallel pre-trends and a placebo date. For synthetic control: pre-period fit. For RDD: no bunching at the threshold. For matching: overlap and balance. **If the assumption fails, do not proceed to an estimate** — change the design, change the comparison group, or stop.

6. **Estimate.** Effect size with an interval, in business units ("1.8 points of monthly churn, range 0.9 to 2.7"), not a coefficient. Cluster uncertainty at the level the treatment was assigned. Prefer a simple, inspectable estimate — a two-by-two table of means that anyone can check — alongside any regression.

7. **Refute.** Run at least two of: placebo treatment date, placebo outcome, dose-response, leave-one-out (`analytics.md` Part 4). Record each with its result, including the ones that weakened the finding.

8. **Check who was affected.** Split the effect by the obvious segments. A flat average can hide one segment hit hard and another helped (Simpson's paradox, `analytics.md` Part 1). Label post-hoc segment effects as hypotheses.

9. **Word it to the evidence ladder** (`analytics.md` Part 4). The headline verb is chosen by the design and whether its checks passed, not by how confident the result feels. State the identifying assumption in the first paragraph, not the appendix.

10. **Write `FINDINGS.md`:**
    - **Answer:** the effect, its range, and the confidence level (high / medium / low) with the reason
    - **Design and why**, in two sentences a non-statistician can follow
    - **The assumption, and the evidence it holds** — with the pre-period chart
    - **Refutation checks** run, and their results
    - **What it does not tell you:** scope limits (local to the threshold, this period, these units)
    - **What would change the conclusion**
    - **Recommendation**, and how to get rung 1 evidence next time
    - The provenance footer (`standards/reporting-standards.md`)

11. **Review.** `analysis-reviewer` checks it before it goes anywhere. Causal claims are where confident-and-wrong is most expensive.

12. **Update memory.** The effect estimate and its caveats go in `knowledge/decision-log.md`; the dated change goes in the change ledger if it was missing. Recommend a holdout or staged rollout for the next change of this kind — the cheapest causal analysis is the one designed in advance.

## Environment

Difference-in-differences, interrupted time series, and a placebo test need only SQL and arithmetic. Synthetic control, matching, and regression need Python — {{ML_ENVIRONMENT}} — with `statsmodels` or similar; install on demand and pin versions in the analysis folder. Reach for a library when the method needs it, not before.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
