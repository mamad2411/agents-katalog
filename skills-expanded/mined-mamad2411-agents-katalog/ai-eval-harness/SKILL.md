---
name: ai-eval-harness
version: 1.0.0
description: Build an eval suite for an LLM feature with datasets, graders, and regression gates that block bad releases.
author: matrixx0070
tags: [eval, testing, llm-judge, regression, ci]
---

## When to use

Use this when an LLM feature is real enough that a silent quality regression would hurt users, and "it looked fine when I tried it" is no longer acceptable proof.

**Not for:** the first prompt sketch (iterate by hand first, see `ai-prompt-design`), or pure latency/cost tuning (see `ai-cost-latency`).

## Method

1. Collect a dataset from real traffic and known failures, not invented cases. Aim for 50-200 items; label each with the expected outcome or a rubric.
2. Split into a dev set (you tune against) and a frozen holdout (you only measure). Never tune on the holdout.
3. Pick a grader per case type. Decision point: exact/enum/JSON → programmatic assertion; open-ended → LLM-as-judge with a rubric; factual → check against a reference. Prefer the cheapest grader that is trustworthy.
4. Validate the LLM judge itself: have it grade 20 human-labeled items; if agreement is low, tighten the rubric before trusting it.
5. Compute aggregate metrics (accuracy, pass rate, per-category breakdown) plus a list of individual failures for inspection.
6. Set a regression gate: a threshold that must hold in CI before a prompt/model change merges. Decision point: block on holdout pass-rate drop OR any critical-category failure.
7. Re-run on every prompt, model, or retrieval change; archive scores per version.

## Example

Feature: invoice field extraction. Dataset: 120 real invoices, expected JSON per invoice.

```
grader = exact_match(pred["total"], gold["total"])
        and iso_date(pred["due_date"]) == gold["due_date"]
```

Baseline (prompt v3): 108/120. Candidate (v4, added a few-shot example): 116/120, but 2 NEW failures in the "foreign currency" category. Gate rule "no category may regress" blocks the merge until v5 fixes currency, reaching 119/120.

## Pitfalls

- **Vibes as eval.** Eyeballing a few outputs. If it is not scored on a frozen set, it is not an eval.
- **Trusting an unvalidated judge.** LLM judges have biases (length, position). Calibrate against human labels first.
- **Aggregate blindness.** A steady average hides a tanked subcategory. Always break down by category.
- **Leaky holdout.** Tuning until the holdout passes turns it into a training set. Touch it only to measure.

## Output format

```
# Eval Suite: <feature>
DATASET: <n> items | source | dev/holdout split
LABELS: <expected outcome or rubric>
GRADERS:
- <case type> -> <programmatic | llm-judge | reference>
JUDGE CALIBRATION: agreement=<x> on <n> human labels
METRICS: overall=<x> | per-category={...}
GATE: block merge if holdout<<t> OR any category regresses
RESULTS: v<n> <score> | failures=[...]
```
