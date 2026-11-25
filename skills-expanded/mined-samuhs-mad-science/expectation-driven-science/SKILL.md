---
name: expectation-driven-science
description: Development guided by the scientific method and explicit expectations. Use when the user wants to build or validate an analysis/model test-first, states a "hypothesis", "expectation" or "assumption" about the data, or asks for a principled data-science workflow (hypothesis → prediction → verification).
---

# Expectation-Driven Science

This is the discipline that turns data exploration from an implicit process into a verifiable **hypothesis → prediction → verification** loop. It is the data-science equivalent of TDD's red→green: the same root principle — *put the expectation before the trust* — applied to three distinct objects (hypothesis in the business, premise in the data, function in the code). This skill is the reference that makes that loop produce analyses worth keeping: what a good expectation is, where it lives, the anti-patterns, and the rules of the loop.

When exploring the domain, read the project's context documentation (if it exists) so hypothesis names, metrics, and interfaces match the business domain language, and respect the ADRs in the area you're touching.

## What a good expectation (hypothesis/prediction) is

An expectation declares **what the observer believes to be true about the world before looking at the data**, and can therefore be confirmed or refuted. It reads like a research question: *"customers with abandoned carts have lower long-term savings"* tells you exactly which relationship you're testing — and it survives model swaps, column changes, or tool changes, because it depends on the relationship of interest, not on the internal mechanism of implementation.

A good expectation must be **falsifiable** (it can be proven wrong) and **quantifiable** (it has a threshold/acceptance limit defined before running). When the expectation fails, treat the deviation as information, not failure. See the Rule of the loop below.

## Seams: where expectations live

A **seam** is the *object* on which you declare an expectation — the point where you observe reality without "reaching inside" it. Expectations live at seams, never against internal details.

**Only declare expectations at pre-agreed seams.** Before writing any hypothesis, write down the seams under test and confirm them with the user. No expectation is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how verification effort lands on the critical hypotheses and complex logic instead of every edge case.

There are three seam families, aligned with the three layers on which a data scientist relies:

| Seam | Object of the expectation | What to expect (examples) |
|---|---|---|
| **Business hypothesis** | Causal/associative relations in the domain | "3-month retention increase → higher LTV" |
| **Data premise** | Data state/quality/schema | "`created_at` never null", "ratio ≥ 0", "schema versioned" |
| **Function/pipeline** | Code behavior (~TDD) | "the imputer preserves the mean", "transformation is idempotent" |

Ask: "What is the business question, and at which seams should we declare an expectation?" Give each proposed seam a one-line note on what it catches and what it misses.

When the shape of the question itself is in question (what the analysis intends to prove, where the hypothesis boundary lies, which metric is the source of truth), refine the hypothesis before declaring expectations — the clarity of the question decides the usefulness of every verification that follows.

## Anti-patterns

- **Hindsight (post-hoc rationalization)**: the prediction is written *after* seeing the result, so it always "matches". The tell: the expectation shapes itself to the data instead of the data judging the expectation. Expected values must come from an independent source of truth — prior knowledge, literature, a definition set before the experiment, or domain understanding — not by re-deriving what the data itself showed.
- **Tautological**: the deviation is computed the same way the analysis computes it (e.g. expecting `mean == sum/n`), so it passes by construction. The source of truth must be external: a known benchmark, a domain reference value, a hand-worked case.
- **Horizontal slicing**: declaring all hypotheses first, then running all of them. Bulk verifications test *imagined* relationships: you test the *shape* of things rather than the behavior of interest, the expectations go insensitive to real changes, and you commit to a structure before understanding the data. Work in **vertical slices** instead: one hypothesis → one verification → iterate, each slice a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Expectation before trust (red).** Declare the hypothesis/prediction *before* looking at the result and running the verification, then only enough analysis/pipeline to pass it. Don't anticipate future hypotheses or add speculative checks.
- **One slice at a time.** One seam, one expectation, one minimal verification per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the hypothesis loop.
- **Deviation is information, not failure.** When the expectation fails, the next step is not "make it pass at all costs": it is to **investigate** whether the deviation is (a) bad data / pipeline error, or (b) a wrong premise by the scientist. Classifying correctly decides whether the fix is technical or whether the expectation needs to be revised with justification.
- **Separate exploratory from confirmatory.** Exploratory discovers hypotheses and is free-form; confirmatory tests hypotheses and is rigid (expectation pre-registered before collection). Don't treat exploratory analysis as confirmatory — that classic error fabricates conclusions without support.