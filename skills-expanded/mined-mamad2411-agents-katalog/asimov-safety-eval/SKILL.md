---
name: asimov-safety-eval
description: This benchmark evaluates the semantic safety and ethical reasoning of vision-language models in robotics. It probes whether models can correctly identify desirable versus undesirable actions across multimodal scenes, real-world injury scenarios, and hypothetical ethical dilemmas. Use when the user wants to benchmark on ASIMOV, or asks about evaluating this task. Reports classification accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.08663
  bibtex_key: sermanet2025asimov
  confidence: high
---

# asimov-safety-eval

> Generating Robot Constitutions & Benchmarks for Semantic Safety — Sermanet et al. (2025) (arXiv:2503.08663, 2025)

## What this evaluates

This benchmark evaluates the semantic safety and ethical reasoning of vision-language models in robotics. It probes whether models can correctly identify desirable versus undesirable actions across multimodal scenes, real-world injury scenarios, and hypothetical ethical dilemmas.

## Datasets

- **ASIMOV** — total ?; splits: train (2942060), val (2273), test (-1)

## Metrics

- `classification accuracy` **(primary)** — range: [0, 1]
  - Proportion of correct binary or multiple-choice predictions out of total instances. Calculated as (number of correct predictions) / (total number of predictions).
- `desirability alignment` — range: [0, 1]
  - Agreement between human evaluations of desirability and model evaluations, capturing a continuous landscape of preferences rather than a binary safety outcome.

## Input / output format

**Input**: Multimodal: images paired with text instructions/contexts. Text-only: narrative contexts or ethical dilemma descriptions. Each instance presents a scenario with an action or question asking whether the outcome is desirable/safe or violates a constitution.

**Output**: Binary choice (desirable/undesirable or safe/unsafe) for most subsets; multiple-choice for ASIMOV-Dilemmas-SciFi.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Desirability is highly context-dependent and subjective, requiring careful human voting to resolve ambiguity.
- Auto-generated data may inherit biases from the VLM and image generation pipeline used in the 'imagination process'.
- The recursive LLM difficulty-amplification pushes questions to the decision boundary, potentially creating ambiguous or unanswerable instances.

## Evidence (verbatim from paper)

> Alignment results are reported simply as classification accuracy. While notions of desirability can be subjective, we mitigate this ambiguity through a round of human voting at the end to identify the truly preferred label. Note that evaluation sets are disjoint from the "training" set for images, context, instructions and rules, i.e. constitutions are only learnt from the training set.

## Citation

```bibtex
@misc{sermanet2025asimov,
  title={Generating Robot Constitutions & Benchmarks for Semantic Safety},
  author={Sermanet et al. (2025)},
  year={2025},
  note={arXiv:2503.08663}
}
```

- arXiv: 2503.08663
