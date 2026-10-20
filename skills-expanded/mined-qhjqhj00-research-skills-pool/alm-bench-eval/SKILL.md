---
name: alm-bench-eval
description: This benchmark evaluates the cultural and linguistic reasoning capabilities of large multimodal models across 100 languages. It probes visual understanding and cultural knowledge through generic and culturally specific domains, testing both closed-form and open-ended question answering. Use when the user wants to benchmark on ALM-bench, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2411.16508
  bibtex_key: vayani2024alllanguagesmatter
  confidence: high
---

# alm-bench-eval

> All Languages Matter: Evaluating LMMs on Culturally Diverse 100 Languages — Vayani et al. (2024) (arXiv:2411.16508, 2024)

## What this evaluates

This benchmark evaluates the cultural and linguistic reasoning capabilities of large multimodal models across 100 languages. It probes visual understanding and cultural knowledge through generic and culturally specific domains, testing both closed-form and open-ended question answering.

## Datasets

- **ALM-bench** — total 22763; splits: test (22763)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Calculated as the proportion of correctly answered questions out of the total. For multiple-choice and true/false questions, the model must predict the entire chosen option rather than just the leading alphabet.

## Input / output format

**Input**: An image paired with a question in one of 100 languages. Questions are formatted as multiple-choice (MCQ), true/false, short answer, or long answer.

**Output**: For MCQ and true/false: the full text of the chosen option. For open-ended: a generated text response.

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    correct = 0
    for pred, gold in zip(predictions, golds):
        if pred.strip().lower() == gold.strip().lower():
            correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- For MCQ and true/false questions, evaluators must predict the entire chosen option rather than just the leading alphabet, as specified in the protocol.
- Performance varies significantly across language resource levels; high-resource language results do not generalize to low-resource languages, requiring per-language and cross-lingual analysis.

## Evidence (verbatim from paper)

> The performance is represented as an average accuracy across all questions in a language. ... We also evaluate with shuffled orders, predicting the entire chosen option rather than just the leading alphabet.

## Citation

```bibtex
@misc{vayani2024alllanguagesmatter,
  title={All Languages Matter: Evaluating LMMs on Culturally Diverse 100 Languages},
  author={Vayani et al. (2024)},
  year={2024},
  note={arXiv:2411.16508}
}
```

- arXiv: 2411.16508
