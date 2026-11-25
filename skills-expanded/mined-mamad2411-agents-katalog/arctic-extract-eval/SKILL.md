---
name: arctic-extract-eval
description: Evaluates a multimodal document understanding model across visual QA, multilingual text comprehension, English reading comprehension, and table extraction tasks. It probes the model's ability to process long-context documents, answer questions from images or text, and extract structured tabular data from unstructured layouts. Use when the user wants to benchmark on SQuAD2.0, DocVQA, Arctic-TILT, MLQA, xQuAD, or asks about evaluating this task. Reports ANLS*.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.16470
  bibtex_key: chilinski2025arcticextract
  confidence: high
---

# arctic-extract-eval

> Arctic-Extract Technical Report — Chiliński et al. (2025) (arXiv:2511.16470, 2025)

## What this evaluates

Evaluates a multimodal document understanding model across visual QA, multilingual text comprehension, English reading comprehension, and table extraction tasks. It probes the model's ability to process long-context documents, answer questions from images or text, and extract structured tabular data from unstructured layouts.

## Datasets

- **SQuAD2.0** — total ?; splits: test (-1)
- **DocVQA** — total ?; splits: test (-1)
- **Arctic-TILT** — total ?; splits: test (-1)
- **MLQA** — total ?; splits: test (-1)
- **xQuAD** — total ?; splits: test (-1)

## Metrics

- `ANLS*` **(primary)** — range: [0, 1]
  - Average Normalized Levenshtein Similarity. Computes the normalized edit distance between predicted and ground-truth answers. Scores below a threshold (typically 0.5) are set to zero to penalize poor matches.
- `Exact Match` — range: [0, 1]
  - Binary metric that returns 1 if the model's prediction exactly matches the ground-truth answer (case-insensitive, stripped), and 0 otherwise.
- `DocVQA score` — range: [0, 1]
  - Average normalized Levenshtein similarity over the DocVQA benchmark test set, measuring character-level overlap between predicted and reference answers.

## Input / output format

**Input**: Document images paired with natural language questions, or raw text documents for multilingual/English tasks. For table extraction, images or unstructured text containing tabular layouts.

**Output**: Natural language answers to questions, or structured tabular data (rows/columns) extracted from the input document.

## Scoring recipe

```python
def compute_anls(pred, gold, threshold=0.5):
    lev = normalized_levenshtein_similarity(pred, gold)
    return 0.0 if lev < threshold else lev

def compute_exact_match(pred, gold):
    return 1.0 if pred.strip().lower() == gold.strip().lower() else 0.0

def aggregate_scores(predictions, golds, metric_fn):
    scores = [metric_fn(p, g) for p, g in zip(predictions, golds)]
    return sum(scores) / len(scores) if scores else 0.0
```

## Common pitfalls

- Approximately 20-50% of datapoints are excluded from main results when models fail to process inputs due to size constraints, which may inflate reported scores compared to full-dataset evaluation.
- ANLS* penalizes partial matches below a threshold (usually 0.5) by setting them to 0, which can drastically lower scores for slightly misaligned OCR or formatting.
- API-based models were evaluated via a third-party platform (Cortex AI), introducing potential pipeline differences that affect direct comparability with open-weight models.

## Evidence (verbatim from paper)

> All comparisons utilize ANLS* as the primary evaluation metric, as it is most appropriate for document question answering tasks. Looking at the SQuAD2.0 evaluation table (Table [2]), it presents a performance comparison of 9 different language models on the SQuAD2.0 dataset, showing two key metrics: ANLS* (a document understanding metric) and Exact Match scores.

## Citation

```bibtex
@misc{chilinski2025arcticextract,
  title={Arctic-Extract Technical Report},
  author={Chiliński et al. (2025)},
  year={2025},
  note={arXiv:2511.16470}
}
```

- arXiv: 2511.16470
