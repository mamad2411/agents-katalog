---
name: autovivqa-eval
description: This benchmark evaluates Vietnamese vision-language models on visual question answering, probing their ability to ground textual queries in images and generate semantically accurate, linguistically fluent responses. It specifically tests reasoning complexity across five levels (recognition, relational, compositional, causal, text-in-image) and measures both exact-match accuracy and generation quality. Use when the user wants to benchmark on AutoViVQA, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.09689
  bibtex_key: nguyen2026autovivqa
  confidence: high
---

# autovivqa-eval

> AutoViVQA: A Large-Scale Automatically Constructed Dataset for Vietnamese Visual Question Answering — Nguyen Anh Tuong et al. (2026) (arXiv:2603.09689, 2026)

## What this evaluates

This benchmark evaluates Vietnamese vision-language models on visual question answering, probing their ability to ground textual queries in images and generate semantically accurate, linguistically fluent responses. It specifically tests reasoning complexity across five levels (recognition, relational, compositional, causal, text-in-image) and measures both exact-match accuracy and generation quality.

## Datasets

- **AutoViVQA** — total 37000; splits: train (-1), val (-1), test (-1)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Exact match ratio: fraction of test instances where the model's generated answer exactly matches the ground-truth answer.
- `F1` — range: [0, 1]
  - Harmonic mean of token-level Precision and Recall computed between predicted and reference answers.
- `BLEU` — range: [0, 1]
  - Geometric mean of modified n-gram precisions (typically up to 4-grams) with a brevity penalty, measuring n-gram overlap.
- `ROUGE-L` — range: [0, 1]
  - F-measure based on the longest common subsequence between predicted and reference answers, capturing fluency and recall.
- `METEOR` — range: [0, 1]
  - Precision-recall F-score incorporating synonymy, stemming, and word order penalties, weighted more heavily toward recall than BLEU.
- `CIDEr` — range: [0, 1]
  - TF-IDF weighted n-gram similarity between predictions and references, designed to correlate with human judgment for image captioning/VQA.

## Input / output format

**Input**: A single image paired with a Vietnamese question.

**Output**: A single Vietnamese text answer.

## Scoring recipe

```python
def compute_metrics(predictions, references):
    acc = sum(1 for p, r in zip(predictions, references) if p.strip() == r.strip()) / len(predictions)
    # Tokenize for string-matching metrics
    preds_tok = [p.split() for p in predictions]
    refs_tok = [[r.split()] for r in references]
    bleu = corpus_bleu(refs_tok, preds_tok)
    rouge_l = fmeasure_longest_common_subsequence(references, predictions)
    meteor = compute_meteor(references, predictions)
    prec = token_precision(references, predictions)
    rec = token_recall(references, predictions)
    f1 = 2 * prec * rec / (prec + rec + 1e-8)
    cider = tfidf_ngram_similarity(references, predictions)
    return {'Accuracy': acc, 'F1': f1, 'BLEU': bleu, 'ROUGE-L': rouge_l, 'METEOR': meteor, 'CIDEr': cider}
```

## Common pitfalls

- Open-ended answers are evaluated with string-matching metrics (BLEU, ROUGE) that penalize valid paraphrases or alternative correct phrasings.
- Human validation is only performed on a 1,000-sample subset; the full test set relies entirely on automatic metrics, risking undetected systematic biases from LLM-generated data.
- No prompt tuning or decoding optimization is applied, so performance differences may reflect architectural priors rather than pure data quality effects.

## Evidence (verbatim from paper)

> Performance is assessed using standard automatic metrics, including Accuracy, Precision, Recall, F1, BLEU, ROUGE-L, METEOR, and CIDEr, capturing complementary aspects of generation quality and grounding.

## Citation

```bibtex
@misc{nguyen2026autovivqa,
  title={AutoViVQA: A Large-Scale Automatically Constructed Dataset for Vietnamese Visual Question Answering},
  author={Nguyen Anh Tuong et al. (2026)},
  year={2026},
  note={arXiv:2603.09689}
}
```

- arXiv: 2603.09689
