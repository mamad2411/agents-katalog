---
name: neurophysiological-consumer-meta-analysis
description: Use when designing or interpreting neuromarketing studies, setting expectations for neuro-measure effect sizes, pre-testing ads with physiological measures, or explaining to clients why EEG/eye-tracking/GSR findings are complementary rather than universal predictors of consumer behavior.
---

# Neurophysiological Consumer Response Meta-Analysis (PRISMA, Aug 2026)

**Source:** Pamfili, Karakoç & Varol-Ülker, "Neurophysiological Correlates of Consumer Responses: A PRISMA-Based Meta-Analysis," Journal of Neurobehavioral Sciences 13(2), Aug 31 2026 (Türkiye). PRISMA 2020: 3,109 records screened → 22 primary studies (2010–2024). Two independent effect pools: SMD and Fisher-z correlations, REML with Knapp-Hartung adjustment. This is the first cross-modal quantitative synthesis covering EEG, eye-tracking, GSR, and multimodal measures against consumer outcomes (purchase intention, brand attitude, ad evaluation, preference).

## Core Numbers

- **Pooled effects are moderate, not magical:** SMD d = 0.47 [0.18, 0.75]; correlation r ≈ 0.33 [0.07, 0.61].
- **Heterogeneity is the headline:** I² = 77.3–84.1%. The pooled effect is a distribution, not a constant.
- **No moderator survived FDR correction** — stimulus characteristics, measurement modality, and experimental design all matter but none is the single driver.
- **Publication bias detected in the SMD pool** — corrected estimates remain significant but shrink.

## The Practical Rule

Neurophysiological measures are **complementary, not universal** predictors. Their explanatory value depends on (1) stimulus characteristics, (2) measurement modality, (3) experimental design. An r ≈ 0.33 means roughly 11% shared variance: useful in a multi-metric battery, useless as a standalone decision.

**Decision rule for pre-testing:** never certify an ad's success from a neuro measure alone. Use neuro metrics to (a) rank variants of the same ad, (b) localize failing segments, (c) flag over-attention (cf. sustained-attention paradox), (d) complement, never replace, behavioral and sales endpoints. Demand confirmatory follow-up before any large budget allocation.

## How It Updates the Library

This is the field-level evidence check that the library's individual neuromarketing skills needed:

| Library skill | Meta-analysis contribution |
|---|---|
| `neuromarketing-market-evidence-2026` | Confirms "real but context-dependent" at pooled-effect level |
| `sustained-attention-purchase-paradox` | Explains the sign-flipping individual-study results: I² near 80% |
| `neuromarketing-three-layer-discipline` | Supplies the effect-size ceiling each layer should claim |
| `discount-clarity-memorization-fixation` | Calibration for single-study predictors (fixation r values live inside a heterogeneous pool) |

## Cross-Links

- `neuromarketing-reality-check-2026` — same honesty posture, pre-meta-analysis
- `llm-personalized-ads-reality-check` — parallel pattern in AI personalization claims
- `nudge-effectiveness-reality-check` — behavioral-intervention analog

## A-Tech Fit

- **Open science:** PRISMA protocol + REML/Knapp-Hartung methods are replicable; effect pools can be re-computed on any new corpus.
- **Privacy:** reinforces "aggregate neuro-metrics only, never neural inference on individuals."
- **Financial freedom:** prevents wasting budget on single-EEG-study claims; the 11%-of-variance ceiling is a defensible procurement number.
- **Practical:** gives every client engagement a citable, quantified expectation ("r ≈ 0.33, I² ≈ 80%") that survives cross-examination.