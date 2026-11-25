---
name: experiment
description: Design or read out a controlled experiment (A/B test) — hypothesis, power analysis, pre-registered primary metric, guardrails, randomisation unit, then sample-ratio and effect-size analysis with a clear ship/no-ship decision. Use to plan a test before launch or to analyse one after it ends.
---

# Experiment — A/B Test Design & Readout

Owner: `data-scientist`, with `metrics-steward` on metric definitions and `analytics-engineer`
for the analysis dataset. Args name the test and mode, e.g. `/experiment design new checkout flow`
or `/experiment readout pricing-page test`.

This skill has two modes. **Design** runs before launch; **Readout** runs after the test ends.
Default to design if no results exist yet.

## Mode A — Design (before launch)

1. **Frame the decision.** What ships if it wins? What's the cost of a false positive? If the
   answer doesn't change a decision, an experiment may be overkill — say so.

2. **State the hypothesis** as a directional, testable claim: "Changing X will increase
   [primary metric] by at least [MDE] for [population]." The **minimum detectable effect (MDE)**
   is the smallest change worth shipping, set with the business — not whatever turns out
   significant.

3. **Pick the primary metric — one — from `knowledge/metrics-catalog.md`.** Pre-register it.
   Add 1–3 **guardrail metrics** (things that must not get worse: latency, refunds, churn).
   Picking the winner after the fact from many metrics is how teams ship noise.

4. **Choose the unit of randomisation** (user, account, session, cluster) and confirm the
   analysis unit matches it. Mismatch (e.g. randomise by user, analyse by session) breaks the
   statistics. Watch for cross-unit contamination/network effects.

5. **Power analysis.** Compute required sample size and run duration from: baseline rate (from
   the catalog/marts), MDE, significance level (default α=0.05), and power (default 80%). State
   the assumptions. If the required duration is implausible, the MDE is too small — renegotiate,
   don't peek early. Two ways to need less traffic, both decided now, not after the result
   (`analytics.md` Part 5):
   - **Variance reduction (CUPED).** If the metric has a pre-experiment history per unit, plan
     to adjust for it; the sample needed falls by the squared correlation between the pre-period
     and in-experiment values. Record the covariate and its window in the design.
   - **A capped metric** for heavy-tailed outcomes (revenue per user): pre-register the
     winsorisation percentile.

6. **Decide how the test will be monitored.** People will look at the dashboard before the
   end. Pick one and write it down: **fixed horizon** (interim looks are for guardrails and
   broken assignment only — no decisions), **group-sequential** (a stated number of looks with
   an alpha-spending rule), or **always-valid** intervals (safe to check any time, at the cost
   of width). An unplanned early stop on a significant-looking interim result is not a result.

7. **Check for interference.** If one unit's treatment can change another's outcome —
   marketplaces, shared inventory, pricing, social features — randomise clusters or use a
   switchback, and size the test for the number of clusters, not the number of users.

8. **Write `experiments/YYYY-MM-DD-<slug>/DESIGN.md`:** hypothesis, primary + guardrail metrics
   (with catalog links), randomisation unit, MDE, sample size, planned duration, the monitoring
   method and stop rules, any variance-reduction covariate, how secondary metrics and segments
   will be corrected for multiple comparisons, and what decision each outcome triggers. If the
   test collects or uses personal data in a new way, run `/privacy-review` first. For high-stakes or customer-affecting tests, confirm the
   design with the user before launch. Add a row to `experiments/README.md`.

## Mode B — Readout (after the test ends)

1. **Check sample ratio mismatch (SRM) first.** If the actual split deviates from the intended
   allocation beyond chance, the assignment is broken — **stop and diagnose; do not interpret
   the result.**

2. **Profile the data** per `standards/sql-and-data-standards.md`: exposure counts per arm,
   date coverage, dedup at the randomisation unit, exclusions (and why).

3. **Estimate the effect** on the pre-registered primary metric: point estimate **with a
   confidence interval**, at the randomisation unit. Report effect size in business terms, not
   just a p-value. Check every guardrail metric. Use exactly the analysis the design
   registered: the CUPED adjustment if one was planned (and say how much it narrowed the
   interval), the sequential boundary if looks were planned. If the metric is a ratio whose
   unit differs from the randomisation unit (clicks per session, revenue per order), get the
   variance from the delta method or a bootstrap over randomisation units — a row-level test
   understates it.

4. **Pressure-test** (run the `analytics.md` Part 1 traps and Part 5): **Twyman's law first —
   a surprisingly large effect is a bug until shown otherwise**, so check logging, assignment,
   and the join before believing it; no peeking-based early calls; secondary metrics and
   segment cuts corrected for multiple comparisons (Holm for a confirmatory family,
   Benjamini–Hochberg for exploration) and labelled as hypotheses, not results;
   segment heterogeneity (does one segment drive it — Simpson's paradox?); novelty/primacy
   effects; outlier sensitivity on skewed metrics (report robust/median where the metric is
   heavy-tailed). Distinguish "no effect" from "underpowered."
   - **Incremental effect, not just averages.** The treated-vs-control gap *is* the causal lift — the raw treated rate is not. When the effect varies across segments, that heterogeneity is the seed of **uplift modelling**: the clean control group lets `data-scientist` model *who is persuadable* (largest incremental effect) so future targeting spends only where the treatment actually moves the needle.

5. **Decide and write `experiments/YYYY-MM-DD-<slug>/RESULTS.md`:**
   - **Verdict:** ship / don't ship / inconclusive — with the effect estimate + CI and a
     confidence level.
   - Guardrail check, segment notes, and any caveats that change the conclusion.
   - **Impact if shipped** (quantified) and what to monitor post-launch (hand to
     `performance-monitor`).
   - For customer-affecting decisions, note the **fairness trade-off** explicitly (`analytics.md`
     Part 1) — equal error rates and equal predictive value can't both hold when base rates differ.
   - The provenance footer (`standards/reporting-standards.md`). A ship decision goes to
     `analysis-reviewer` before it is announced.

6. **Close the loop.** Update `experiments/README.md` with the decision, log the ruling in
   `knowledge/decision-log.md`, and if the test changed a metric's interpretation, route it to
   `metrics-steward`.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
