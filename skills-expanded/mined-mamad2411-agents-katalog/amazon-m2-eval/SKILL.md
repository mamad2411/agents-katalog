---
name: amazon-m2-eval
description: Evaluates session-based recommendation and text generation capabilities across multiple languages and locales. It probes a model's ability to predict the next product in a shopping session, transfer knowledge across domain-shifted locales, and generate product titles from session context. Use when the user wants to benchmark on Amazon-M2, or asks about evaluating this task. Reports next-product prediction.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2307.09688
  bibtex_key: jin2023amazonm2
  confidence: medium
---

# amazon-m2-eval

> Amazon-M2: A Multilingual Multi-locale Shopping Session Dataset for Recommendation and Text Generation — Wei Jin et al. (2023) (arXiv:2307.09688, 2023)

## What this evaluates

Evaluates session-based recommendation and text generation capabilities across multiple languages and locales. It probes a model's ability to predict the next product in a shopping session, transfer knowledge across domain-shifted locales, and generate product titles from session context.

## Datasets

- **Amazon-M2** — total 3967908; splits: train (3606249), test (361659); repo https://github.com/HaitaoMao/Amazon-M2

## Metrics

- `next-product prediction` **(primary)** — range: [0, 1]
  - Not explicitly defined in the provided text; standard session-based recommendation metrics (e.g., Recall@K, MRR) are implied for Tasks 1 & 2, and lexical/semantic overlap metrics for Task 3.

## Input / output format

**Input**: A chronological sequence of product IDs (and optionally textual attributes like title, brand, color) representing a user's shopping session.

**Output**: For Tasks 1 & 2: The ID of the next product to be interacted with. For Task 3: The textual title of the next product to be interacted with.

## Scoring recipe

```python
def evaluate(predictions, golds, k=10):
    hits = 0
    for pred, gold in zip(predictions, golds):
        # pred is a ranked list of candidate product IDs
        if gold in pred[:k]:
            hits += 1
    return hits / len(golds)
# For Task 3, replace hit check with exact string match or ROUGE/BLEU score.
```

## Common pitfalls

- Domain shift between large locales (UK, DE, JP) and underrepresented ones (ES, IT, FR) requires careful transfer learning setup; models trained only on large locales will fail on test splits.
- Test set products for title generation are held-out (cold-start), making exact match or lexical overlap metrics potentially misleading without semantic evaluation.
- Multilingual product attributes require models to handle cross-lingual context, which standard monolingual recommenders may fail to capture.

## Evidence (verbatim from paper)

> Given a user session, the goal of this task is to predict the next product that the user will interact with. ... practitioners are required to perform pretraining on a large pretraining dataset (user sessions from JP, UK, and DE) and then finetune and make predictions on the downstream datasets of underrepresented locales (user sessions from ES, IT, and FR). ... This is a brand-new task designed for session datasets with textual attributes, and it aims to predict the title of the next product that the user will interact with within the current session.

## Citation

```bibtex
@misc{jin2023amazonm2,
  title={Amazon-M2: A Multilingual Multi-locale Shopping Session Dataset for Recommendation and Text Generation},
  author={Wei Jin et al. (2023)},
  year={2023},
  note={arXiv:2307.09688}
}
```

- arXiv: 2307.09688
