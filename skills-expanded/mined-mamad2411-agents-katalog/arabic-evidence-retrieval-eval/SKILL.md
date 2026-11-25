---
name: arabic-evidence-retrieval-eval
description: This benchmark tests a system's ability to retrieve relevant evidence snippets from a large pool of web pages for a given Arabic claim. It evaluates ranking performance in a retrieval setting where only a small fraction of snippets actually contain verifying evidence. Use when the user wants to benchmark on Arabic Evidence Retrieval Dataset, or asks about evaluating this task. Reports P@10.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.07997
  bibtex_key: barroncedeno2020checkthat
  confidence: high
---

# arabic-evidence-retrieval-eval

> Overview of CheckThat! 2020: Automatic Identification and Verification of Claims in Social Media — Barrón-Cedeno et al. (2020) (arXiv:2007.07997, 2020)

## What this evaluates

This benchmark tests a system's ability to retrieve relevant evidence snippets from a large pool of web pages for a given Arabic claim. It evaluates ranking performance in a retrieval setting where only a small fraction of snippets actually contain verifying evidence.

## Datasets

- **Arabic Evidence Retrieval Dataset** — total 169902; splits: test (169902)

## Metrics

- `P@10` **(primary)** — range: [0, 1]
  - Precision at cutoff k=10, measuring the proportion of retrieved snippets that contain useful evidence among the top 10 results.

## Input / output format

**Input**: Arabic claim text and a list of candidate web page snippets.

**Output**: Ranked list of evidence snippets.

## Scoring recipe

```python
def score(predictions, gold):
    top_k = predictions[:10]
    relevant_in_top_k = len(set(top_k) & gold)
    return relevant_in_top_k / 10.0
```

## Common pitfalls

- Evaluation relies on a pooling method: only snippets returned by systems are annotated, which may bias precision estimates.
- Snippets are automatically split by punctuation, which might not align with semantic evidence boundaries.

## Evidence (verbatim from paper)

> In order to evaluate the submitted runs, we computed P@k at different cutoff (k = 1, 5, 10). The official measure was P@10.

## Citation

```bibtex
@misc{barroncedeno2020checkthat,
  title={Overview of CheckThat! 2020: Automatic Identification and Verification of Claims in Social Media},
  author={Barrón-Cedeno et al. (2020)},
  year={2020},
  note={arXiv:2007.07997}
}
```

- arXiv: 2007.07997
