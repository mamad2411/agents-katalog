---
name: 3d-multimodal-eval
description: Evaluates a 3D large multimodal model's ability to understand spatial scenes and generate accurate text responses. It probes free-form question answering about 3D environments and object-centric dense captioning grounded in 3D coordinates. Use when the user wants to benchmark on ScanQA, SQA3D, ScanRefer, Nr3D, or asks about evaluating this task. Reports CiDEr.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.23153
  bibtex_key: mei2026efficient
  confidence: high
---

# 3d-multimodal-eval

> Efficient Encoder-Free Fourier-based 3D Large Multimodal Model — Guofeng Mei et al. (arXiv:2602.23153, 2026)

## What this evaluates

Evaluates a 3D large multimodal model's ability to understand spatial scenes and generate accurate text responses. It probes free-form question answering about 3D environments and object-centric dense captioning grounded in 3D coordinates.

## Datasets

- **ScanQA** — total 41400; splits: val (-1)
- **SQA3D** — total 33400; splits: test (-1)
- **ScanRefer** — total ?; splits: test (-1)
- **Nr3D** — total ?; splits: test (-1)

## Metrics

- `CiDEr` **(primary)** — range: percent
  - Consensus-based Image Description Evaluation. Computes n-gram similarity between generated and reference captions using IDF weighting to penalize common words.
- `BLEU-4` — range: percent
  - Bilingual Evaluation Understudy. Measures n-gram precision up to 4-grams with a brevity penalty.
- `METEOR` — range: percent
  - Metric for Evaluation of Translation with Explicit ORdering. Matches words using synonymy, stemming, and exact matching, then computes harmonic mean of precision and recall.
- `ROUGE-L` — range: percent
  - Recall-Oriented Understudy for Gisting Evaluation. Measures the longest common subsequence between generated and reference text.
- `EM@1` — range: [0, 1]
  - Exact Match at top-1. Returns 1 if the generated answer exactly matches the reference answer, 0 otherwise. Averaged over the dataset.
- `m@kIoU` — range: percent
  - For dense captioning, evaluates localization quality by computing metric m (CiDEr, BLEU-4, METEOR, or ROUGE-L) only for predictions with Intersection over Union (IoU) ≥ k (typically 0.5).

## Input / output format

**Input**: Text prompt/question paired with a 3D point cloud scene (uniformly sampled to 50k points, aggregated into 256 superpoint tokens, and processed via an FFT enhancer).

**Output**: Free-form natural language text (answers or object descriptions).

## Scoring recipe

```python
def compute_metrics(predictions, references):
    bleu4 = nltk.translate.bleu_score.corpus_bleu(references, predictions, weights=(0.25, 0.25, 0.25, 0.25))
    meteor = compute_meteor(references, predictions)
    rouge_l = compute_rouge_l(references, predictions)
    cider = compute_cider(references, predictions)
    em1 = sum(1 for p, r in zip(predictions, references) if p.strip() == r.strip()) / len(predictions)
    return {'BLEU-4': bleu4, 'METEOR': meteor, 'ROUGE-L': rouge_l, 'CiDEr': cider, 'EM@1': em1}
```

## Common pitfalls

- Confusing the IoU threshold `k` in `m@kIoU` for dense captioning (typically 0.5).
- Failing to distinguish between evaluation with an external segmenter (Mask3D) vs. graph-based proposals.
- Mixing up ScanQA (validation split) and SQA3D (test split) results.
- Reporting #Params and FLOPs as performance metrics rather than efficiency/compute metrics.

## Evidence (verbatim from paper)

> We use the abbreviations C, B-4, M and R for CiDEr, BLEU-4, METEOR, and Rouge-L, respectively. We report #Params, indicating the number of parameters activated for 3D scene tokenization, and FLOP as an efficiency measure.

## Citation

```bibtex
@misc{mei2026efficient,
  title={Efficient Encoder-Free Fourier-based 3D Large Multimodal Model},
  author={Guofeng Mei et al.},
  year={2026},
  note={arXiv:2602.23153}
}
```

- arXiv: 2602.23153
