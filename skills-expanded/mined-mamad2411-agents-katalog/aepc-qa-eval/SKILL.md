---
name: aepc-qa-eval
description: This benchmark evaluates large language models' ability to retain and apply specialized domain knowledge in Quebec's civil law insurance sector. It probes both closed-book knowledge retention and the effectiveness of retrieval-augmented generation (RAG) pipelines under jurisdiction-specific, high-stakes regulatory scenarios. Use when the user wants to benchmark on AEPC-QA, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.07825
  bibtex_key: beauchemin2026quebecinsurance
  confidence: high
---

# aepc-qa-eval

> Benchmarking Large Language Models for Quebec Insurance: From Closed-Book to Retrieval-Augmented Generation — Beauchemin et al. (2026) (arXiv:2603.07825, 2026)

## What this evaluates

This benchmark evaluates large language models' ability to retain and apply specialized domain knowledge in Quebec's civil law insurance sector. It probes both closed-book knowledge retention and the effectiveness of retrieval-augmented generation (RAG) pipelines under jurisdiction-specific, high-stakes regulatory scenarios.

## Datasets

- **AEPC-QA** — total 807; splits: full (807)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - The proportion of correctly answered multiple-choice questions out of the total number of questions. Calculated as (number of correct predictions) / (total questions).

## Input / output format

**Input**: A multiple-choice question with four options (a, b, c, d) and a single correct answer. In the RAG setting, the query is augmented with the top-5 retrieved document chunks processed by a context compressor.

**Output**: The model must select exactly one of the four provided choices (a, b, c, or d).

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for pred, gold in zip(predictions, gold_labels) if pred == gold)
    return correct / len(gold_labels)

# predictions: list of model outputs (e.g., 'a', 'b', 'c', 'd')
# gold_labels: list of correct answer keys
accuracy = calculate_accuracy(predictions, gold_labels)
```

## Common pitfalls

- The dataset is private due to copyright restrictions, preventing independent replication or contamination checks.
- RAG performance is highly unstable across models; while it boosts weaker models, it can cause catastrophic failures in stronger ones due to context distraction.
- The four-choice format sets a random baseline at ~25%, so scores must be interpreted relative to this floor rather than absolute thresholds.

## Evidence (verbatim from paper)

> The resulting dataset contains 807 multiple-choice questions, each with 4 choices and a single, objectively correct answer accepted by the regulator. Performance is measured by accuracy on multiple-choice questions. This evaluation protocol is a proxy for assessing domain knowledge retention and reasoning capabilities.

## Citation

```bibtex
@misc{beauchemin2026quebecinsurance,
  title={Benchmarking Large Language Models for Quebec Insurance: From Closed-Book to Retrieval-Augmented Generation},
  author={Beauchemin et al. (2026)},
  year={2026},
  note={arXiv:2603.07825}
}
```

- arXiv: 2603.07825
