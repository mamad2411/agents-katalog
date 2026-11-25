---
name: experiment-workflow
description: Use when designing, running, or comparing a repeatable experiment where a decision question, controlled variables, baselines, measurements, and raw evidence matter. Not for ordinary unit tests or one-off checks.
---

# Experiment workflow

One stated question at a time, with enough evidence for someone else to rerun it and judge the conclusion.

1. **Decision.** State the decision the experiment informs and the result that would change it. One precise question; say what it cannot establish.
2. **Variables.** Name the independent variable, outcomes, fixed conditions, baseline and known confounders. Change one variable at a time when you claim a cause; if several must move together, call it a comparison.
3. **Setup.** Record exact inputs, versions, configuration, hardware, seeds and preprocessing; keep them fixed unless one is the variable.
4. **Measures, set before running.** Units, method, pass threshold, repetitions, aggregation, and how failures and outliers count. Use the smallest sample that answers honestly; claim no certainty the design cannot carry.
5. **Run and keep evidence.** Commands, raw outputs, failures and deviations, with baseline and variant side by side.
6. **Judge.** Separate observation from interpretation, compare against the threshold, state uncertainty and the decision the evidence supports. This run is the next one's baseline.

For retrieval or RAG, keep the query set, retrieved passages, ranks, latency, chunking settings and corpus identity. A semantic/keyword/hybrid query suite is one useful stress test, sized to the corpus (about 10 of each type for a medium-to-large one).
