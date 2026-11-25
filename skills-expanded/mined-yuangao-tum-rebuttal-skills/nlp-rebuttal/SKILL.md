---
name: nlp-rebuttal
description: Scenario playbook for answering a SPECIFIC reviewer concern in an NLP/ML/AI rebuttal — 28 concern types (novelty, simple combination, unclear motivation, weak baselines, marginal gains, missing ablations, no significance, data leakage, no human eval, reproducibility, and more), each with a bad-answer anti-pattern and a recommended-answer template. Use when drafting a reply to a concrete review comment, when the user quotes a reviewer ("the reviewer says...", "R2 complains..."), asks which strategy fits a concern, or asks for a rebuttal reply template. Complements write-rebuttal (overall process and tactics); this skill picks the response strategy per concern.
---

# NLP Rebuttal Scenario Playbook

Translated and adapted from [MLNLP-World/Paper-Rebuttal-Tips](https://github.com/MLNLP-World/Paper-Rebuttal-Tips).
28 recurring reviewer-concern scenarios. Each has four parts: the concern,
a bad answer that backfires, a recommended answer template, and the takeaway.

**Good rebuttal = Respect + Evidence + Clarity.**

## How to use

1. Classify each reviewer comment with the router below.
2. Load ONLY the reference file(s) for the matched tips.
3. Adapt the recommended-answer template: replace every placeholder (XXX, A/B/C,
   Table X) with the paper's real content and freshly computed numbers. Never
   ship a template verbatim.
4. For overall response structure, ordering, and tone, use the
   `write-rebuttal` skill (itemize → brain-dump → draft → revise, the 18
   tactics, the neutral-third-party test). These two skills compose: that one
   shapes the whole response, this one shapes each answer.

## Concern router

| Reviewer concern sounds like | Tip | Reference |
| --- | --- | --- |
| "Too complex", "bag of tricks", "which component matters?" | 1 | [innovation-theory.md](references/innovation-theory.md) |
| "Not novel", "similar to prior work A" | 2 | innovation-theory.md |
| "Just a combination of existing techniques" | 3 | innovation-theory.md |
| "Contributions unclear" | 4 | innovation-theory.md |
| "Motivation unclear", "why is this problem important?" | 5 | innovation-theory.md |
| "No theoretical analysis", "why does it work?" | 6 | innovation-theory.md |
| "Limitations discussion is superficial" | 7 | innovation-theory.md |
| "Related work missing/insufficient" | 8 | [communication-writing.md](references/communication-writing.md) |
| "Writing/notation unclear" | 9 | communication-writing.md |
| Reviewer misunderstood the method | 10 | communication-writing.md |
| Vague, low-quality negative review | 11 | communication-writing.md |
| Tempted to reply "we will add..." | 12 | communication-writing.md |
| "Missing/weak baselines" | 13 | [experiments-evidence.md](references/experiments-evidence.md) |
| "Improvements are marginal" | 14 | experiments-evidence.md |
| "Unfair experimental setup" | 15 | experiments-evidence.md |
| "Missing ablations" | 16 | experiments-evidence.md |
| "Too much computational overhead" | 17 | experiments-evidence.md |
| Asked for experiments too large for the rebuttal window | 18 | experiments-evidence.md |
| "Dataset too small" | 19 | experiments-evidence.md |
| "Generalization not shown" (few datasets/models/tasks) | 20 | experiments-evidence.md |
| "No variance / significance / seeds" | 21 | experiments-evidence.md |
| "Possible train/test leakage or contamination" | 22 | experiments-evidence.md |
| "Hyperparameter sensitivity?" ("why k=40?") | 23 | experiments-evidence.md |
| "Wrong/missing evaluation metrics" | 24 | experiments-evidence.md |
| "No human evaluation" | 25 | experiments-evidence.md |
| "Intermediate outputs never evaluated directly" | 26 | experiments-evidence.md |
| Claims "continual/online" but experiments are one-shot offline | 27 | experiments-evidence.md |
| "No code, seeds, or hyperparameters — not reproducible" | 28 | experiments-evidence.md |

A single comment often maps to several tips (e.g. "marginal gains and no
significance testing" = 14 + 21). Load all matches and merge their strategies
into one answer.

## Cross-cutting rules (from the 28 scenarios)

- **Act, don't promise** (Tip 12): run the number/analysis now and put it in
  the rebuttal. "We will add X in the revision" alone convinces nobody.
- **Never blame the reviewer** (Tips 4, 9, 10): if they misread, the fix is a
  clarification plus a pointer to the line, stated neutrally.
- **Answer head-on** (Tips 2, 3): name exactly where the difference or novelty
  lies — motivation, mechanism, role — not just that it exists.
- **Evidence over adjectives** (Tips 13-28): every disputed claim gets a table,
  an ablation, a test, or an honest statement of infeasibility with a
  scaled-down proxy result (Tip 18).
- **Concede real weaknesses gracefully** (Tips 7, 14, 19): bound the claim,
  show the trend, explain what the paper still establishes.

## Anti-patterns (never do)

- Asserting all components are necessary without per-component ablation (Tip 1).
- "We are the first to apply X to Y" as the whole novelty defense (Tip 3).
- Repeating the introduction as the answer to a motivation question (Tip 5).
- "Experiments show it works" as the answer to a theory question (Tip 6).
- Calling the setup fair without matching compute/tuning budgets (Tip 15).
- Dismissing a metric request instead of adding the metric (Tip 24).
