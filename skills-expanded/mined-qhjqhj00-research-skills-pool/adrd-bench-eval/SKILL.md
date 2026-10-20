---
name: adrd-bench-eval
description: Evaluates LLMs on domain-specific knowledge and clinical reasoning for Alzheimer's Disease and Related Dementias (ADRD), as well as practical daily caregiving scenarios. It probes both factual recall and error detection capabilities in a medical context. Use when the user wants to benchmark on ADRD-Bench, or asks about evaluating this task. Reports exact match accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.11460
  bibtex_key: zhao2026adrdbench
  confidence: high
---

# adrd-bench-eval

> ADRD-Bench: A Preliminary LLM Benchmark for Alzheimer's Disease and Related Dementias — Guangxin Zhao et al. (2026) (arXiv:2602.11460, 2026)

## What this evaluates

Evaluates LLMs on domain-specific knowledge and clinical reasoning for Alzheimer's Disease and Related Dementias (ADRD), as well as practical daily caregiving scenarios. It probes both factual recall and error detection capabilities in a medical context.

## Datasets

- **ADRD-Bench** — total 1501; splits: test (1501); repo https://github.com/IIRL-ND/ADRD-Bench

## Metrics

- `exact match accuracy` **(primary)** — range: [0, 1]
  - Calculated as the fraction of instances where the model's predicted option exactly matches the ground-truth label. No partial credit is awarded.

## Input / output format

**Input**: Discrete-choice questions in multiple-choice, True/False, or error sentence detection formats.

**Output**: A single selected option (e.g., A, B, C, D, True, False, or the specific sentence to flag) that exactly matches the ground-truth label.

## Scoring recipe

```python
correct = 0
total = len(predictions)
for pred, gold in zip(predictions, gold_labels):
    if pred.strip() == gold.strip():
        correct += 1
return correct / total
```

## Common pitfalls

- Error detection tasks require identifying hallucinated sentences within a text, not just answering a direct question.
- Exact match is strictly enforced; models that provide correct reasoning but format the answer differently will be scored as incorrect.
- Caregiving QA focuses on practical, non-clinical scenarios, so models trained primarily on medical literature may underperform despite high clinical knowledge.

## Evidence (verbatim from paper)

> For quantitative evaluation, given that all tasks in our benchmark are formulated as discrete-choice questions, including multiple-choice, True/False, and error sentence detection formats, we adopt exact match accuracy as the primary metric. A model’s prediction is considered correct if and only if the selected option exactly matches the ground-truth label.

## Citation

```bibtex
@misc{zhao2026adrdbench,
  title={ADRD-Bench: A Preliminary LLM Benchmark for Alzheimer's Disease and Related Dementias},
  author={Guangxin Zhao et al. (2026)},
  year={2026},
  note={arXiv:2602.11460}
}
```

- arXiv: 2602.11460
