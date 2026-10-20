---
name: adversarial-nli-eval
description: Evaluates natural language inference models on adversarially crafted examples designed to expose reasoning brittleness and spurious pattern reliance. It probes whether models can generalize to novel, difficult inference cases that specifically target known model weaknesses across iterative rounds of human-and-model-in-the-loop data collection. Use when the user wants to benchmark on ANLI, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1910.14599
  bibtex_key: nie2019adversarialnli
  confidence: high
---

# adversarial-nli-eval

> Adversarial NLI: A New Benchmark for Natural Language Understanding — Nie et al. (2019) (arXiv:1910.14599, 2019)

## What this evaluates

Evaluates natural language inference models on adversarially crafted examples designed to expose reasoning brittleness and spurious pattern reliance. It probes whether models can generalize to novel, difficult inference cases that specifically target known model weaknesses across iterative rounds of human-and-model-in-the-loop data collection.

## Datasets

- **ANLI** — total ?; splits: train (-1), test (-1), test-exclusive (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - The proportion of correctly predicted labels (entailment, contradiction, neutral) out of the total number of instances in the test set.

## Input / output format

**Input**: A premise sentence and a hypothesis sentence.

**Output**: A single classification label: 'entailment', 'contradiction', or 'neutral'.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Models may exploit spurious artifacts present only in the hypothesis text rather than performing true logical inference over the premise-hypothesis pair.
- Performance can be heavily influenced by the specific model architecture's training data, leading to architecture-specific vulnerabilities that are not mitigated by simply increasing dataset size.
- Base models for later rounds are evaluated on ensembles, so their performance is not necessarily zero but still falls well below chance.

## Evidence (verbatim from paper)

> We show test set performance on the ANLI test sets per round, the total ANLI test set, and the exclusive test subset (examples from test-set-exclusive workers). We also show accuracy on the SNLI test set and the MNLI development set (for the purpose of comparing between different model configurations across table rows).

## Citation

```bibtex
@misc{nie2019adversarialnli,
  title={Adversarial NLI: A New Benchmark for Natural Language Understanding},
  author={Nie et al. (2019)},
  year={2019},
  note={arXiv:1910.14599}
}
```

- arXiv: 1910.14599
