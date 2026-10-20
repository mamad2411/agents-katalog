---
name: aratable-eval
description: This benchmark probes large language models' ability to reason over and understand Arabic tabular data across three core tasks: direct question answering, fact verification, and complex reasoning. It specifically tests whether models can extract, compare, and synthesize information from structured Arabic tables while adhering to linguistic and formatting nuances. Use when the user wants to benchmark on AraTable, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2507.18442
  bibtex_key: alshaikh2025aratable
  confidence: high
---

# aratable-eval

> AraTable: Benchmarking LLMs' Reasoning and Understanding of Arabic Tabular Data — Alshaikh et al. (2025) (arXiv:2507.18442, 2025)

## What this evaluates

This benchmark probes large language models' ability to reason over and understand Arabic tabular data across three core tasks: direct question answering, fact verification, and complex reasoning. It specifically tests whether models can extract, compare, and synthesize information from structured Arabic tables while adhering to linguistic and formatting nuances.

## Datasets

- **AraTable** — total ?; splits: test (-1); repo https://github.com/rana-alshaikh/AraTable-Benchmark

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Proportion of model responses marked TRUE by human or LLM judges after applying a relaxed semantic rubric. Calculated as (number of TRUE evaluations) / (total number of evaluated instances).

## Input / output format

**Input**: Arabic questions derived from tabular data, ground-truth answers, and a detailed evaluation rubric specifying tolerance rules for wording, numbers, lists, and formatting.

**Output**: Free-form Arabic responses to the questions. No strict structural constraints are imposed on the model's generation, but outputs are evaluated against a relaxed semantic rubric.

## Scoring recipe

```python
def evaluate(prediction, ground_truth):
    pred = normalize_text(prediction)
    gt = normalize_text(ground_truth)
    if semantic_match(pred, gt): return True
    if is_boolean(gt):
        if any(p in pred for p in TRUE_PHRASES): return True
        if any(p in pred for p in FALSE_PHRASES): return False
    if is_numeric(gt):
        if abs(float(pred) - float(gt)) <= 0.005: return True
    if is_list(gt):
        if set(normalize_list(pred)) == set(normalize_list(gt)): return True
    if requires_arabic_entity(gt) and not is_arabic(pred): return False
    return False
accuracy = sum(evaluate(p, g) for p, g in zip(predictions, ground_truths)) / len(predictions)
```

## Common pitfalls

- Unconstrained free-form outputs lead to high verbosity and formatting inconsistencies, making exact string matching or embedding similarity unreliable for scoring.
- Models are highly sensitive to question numbering and listing order, sometimes missing questions or outputting unordered answers if formatting changes.
- Models may filter responses based on trigger words or switch to English mid-answer, indicating over-reliance on pre-training data rather than the provided table.

## Evidence (verbatim from paper)

> This design enabled (a) evaluation of the accuracy of the human-extracted response from Jais’ verbose output and comparison of human evaluation consistency when presented with the same answer in both concise (Model 4) and verbose (Model 5) forms – ideally, both should yield the same accuracy, as the core answer remains unchanged; and (b) the assessment of the robustness of our automated evaluation method in understanding and evaluating the LLMs’ responses that exhibited verbosity.

## Citation

```bibtex
@misc{alshaikh2025aratable,
  title={AraTable: Benchmarking LLMs' Reasoning and Understanding of Arabic Tabular Data},
  author={Alshaikh et al. (2025)},
  year={2025},
  note={arXiv:2507.18442}
}
```

- arXiv: 2507.18442
