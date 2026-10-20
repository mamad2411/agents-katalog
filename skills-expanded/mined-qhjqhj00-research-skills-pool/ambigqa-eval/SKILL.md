---
name: ambigqa-eval
description: This benchmark evaluates a model's ability to identify ambiguous open-domain questions, generate multiple plausible answer spans, and produce disambiguated question rewrites that distinguish between different interpretations of the same query. Use when the user wants to benchmark on AMBIGNQ, or asks about evaluating this task. Reports F1ans.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.10645
  bibtex_key: min2020ambigqa
  confidence: high
---

# ambigqa-eval

> AmbigQA: Answering Ambiguous Open-domain Questions — Min et al. (2020) (arXiv:2004.10645, 2020)

## What this evaluates

This benchmark evaluates a model's ability to identify ambiguous open-domain questions, generate multiple plausible answer spans, and produce disambiguated question rewrites that distinguish between different interpretations of the same query.

## Datasets

- **AMBIGNQ** — total 14042; splits: dev (-1), test (-1)

## Metrics

- `F1ans` **(primary)** — range: [0, 100]
  - Computes the F1 score between the set of predicted answer spans and the set of gold answer spans. Reported separately for all questions (F1ans all) and only for questions with multiple gold answers (F1ans multi).
- `F1BLEU` — range: [0, 100]
  - BLEU score computed between the generated disambiguated question sequence and the gold disambiguated question sequence, scaled to an F1-like range.
- `F1EDIT-F1` — range: [0, 100]
  - F1 score based on edit distance between the generated disambiguated question and the original prompt question, used to measure semantic divergence rather than exact string match.

## Input / output format

**Input**: Open-domain question q, optionally with reference passages or gold answers for ablation studies.

**Output**: A set of answer spans y1...yn and/or a sequence of disambiguated questions x1...xn separated by [SEP].

## Scoring recipe

```python
def compute_f1ans(pred_spans, gold_spans):
    pred_set = set(normalize(s) for s in pred_spans)
    gold_set = set(normalize(s) for s in gold_spans)
    if not pred_set and not gold_set: return 1.0
    if not pred_set or not gold_set: return 0.0
    tp = len(pred_set & gold_set)
    return 2 * tp / (len(pred_set) + len(gold_set))

def compute_f1bleu(pred_q, gold_q):
    bleu = sentence_bleu(gold_q, pred_q)
    return 2 * bleu / (1 + bleu)

def compute_f1edit(pred_q, prompt_q):
    edit_dist = levenshtein(pred_q, prompt_q)
    max_len = max(len(pred_q), len(prompt_q))
    sim = 1 - (edit_dist / max_len) if max_len > 0 else 1.0
    return sim * 100
```

## Common pitfalls

- F1BLEU can be artificially inflated by simply copying the prompt question, which is why F1EDIT-F1 is required to measure actual semantic disambiguation.
- Evaluating only on single-answer questions masks the difficulty of the task; F1ans (multi) specifically measures performance on questions with multiple plausible interpretations.
- Significant performance gaps between dev and test splits arise from distributional shifts in the source NQ-OPEN dataset, not model degradation.

## Evidence (verbatim from paper)

> Table 3 reports the performance of our baselines... SPANSEQGEN also obtains the best performance in F1BLEU and F1EDIT-F1, although their absolute values are low in general... F1ans on examples with multiple question-answer pairs (multi) are lower, indicating that predicting all plausible answers is more challenging than predicting a single answer, as expected.

## Citation

```bibtex
@misc{min2020ambigqa,
  title={AmbigQA: Answering Ambiguous Open-domain Questions},
  author={Min et al. (2020)},
  year={2020},
  note={arXiv:2004.10645}
}
```

- arXiv: 2004.10645
