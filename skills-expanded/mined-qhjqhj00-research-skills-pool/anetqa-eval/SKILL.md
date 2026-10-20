---
name: anetqa-eval
description: Evaluates fine-grained compositional reasoning over untrimmed videos by requiring models to interpret spatio-temporal scene graphs and answer complex questions involving attributes, actions, and temporal relationships. Use when the user wants to benchmark on ANetQA, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2305.02519
  bibtex_key: yu2023anetqa
  confidence: high
---

# anetqa-eval

> ANetQA: A Large-scale Benchmark for Fine-grained Compositional Reasoning over Untrimmed Videos — Zhou Yu et al. (2023) (arXiv:2305.02519, 2023)

## What this evaluates

Evaluates fine-grained compositional reasoning over untrimmed videos by requiring models to interpret spatio-temporal scene graphs and answer complex questions involving attributes, actions, and temporal relationships.

## Datasets

- **ANetQA** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Calculated as the percentage of correctly predicted answers out of the total number of questions. Per-type accuracies are also reported under four taxonomies: question structures, question semantics, reasoning skills, and answer types.

## Input / output format

**Input**: Untrimmed video and a natural language question.

**Output**: A single predicted answer (binary choice, open-ended text, or one of four choices: [A], [B], both, or none).

## Scoring recipe

```python
correct = 0
total = 0
for pred, gold in zip(predictions, gold_answers):
    if pred == gold:
        correct += 1
    total += 1
accuracy = (correct / total) * 100
```

## Common pitfalls

- Models may over-rely on language priors rather than visual reasoning, though balancing strategies are used to mitigate this.
- Frame sampling strategy heavily impacts performance; insufficient or non-uniform sampling often misses critical temporal cues needed for fine-grained reasoning.
- Open-ended and attribute-oriented questions are significantly harder than binary/choice questions, leading to sharp accuracy drops.

## Evidence (verbatim from paper)

> Besides the overall accuracy, we follow [[9]] to report the per-type accuracies under different taxonomies, i.e., question structures, question semantics, reasoning skills, and answer types.

## Citation

```bibtex
@misc{yu2023anetqa,
  title={ANetQA: A Large-scale Benchmark for Fine-grained Compositional Reasoning over Untrimmed Videos},
  author={Zhou Yu et al. (2023)},
  year={2023},
  note={arXiv:2305.02519}
}
```

- arXiv: 2305.02519
