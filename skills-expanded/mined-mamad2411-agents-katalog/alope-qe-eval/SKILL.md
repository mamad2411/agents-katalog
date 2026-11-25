---
name: alope-qe-eval
description: This evaluation probes the ability of LLM-based frameworks to estimate translation quality in a reference-free setting by predicting continuous quality scores for source-target sentence pairs across multiple low-resource language directions. It specifically tests how intermediate Transformer layer representations and adaptive regression heads improve cross-lingual alignment and quality prediction compared to standard fine-tuning or zero-shot prompting. Use when the user wants to benchmark on Low-resource QE language pairs (En-Gu, En-Hi, En-Mr, En-Ta, En-Te, Et-En, Ne-En, Si-En), or asks about evaluating this task. Reports Spearman correlation.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.07484
  bibtex_key: sindhujan2025alope
  confidence: high
---

# alope-qe-eval

> ALOPE: Adaptive Layer Optimization for Translation Quality Estimation using Large Language Models — Sindhujan et al. (2025) (arXiv:2508.07484, 2025)

## What this evaluates

This evaluation probes the ability of LLM-based frameworks to estimate translation quality in a reference-free setting by predicting continuous quality scores for source-target sentence pairs across multiple low-resource language directions. It specifically tests how intermediate Transformer layer representations and adaptive regression heads improve cross-lingual alignment and quality prediction compared to standard fine-tuning or zero-shot prompting.

## Datasets

- **Low-resource QE language pairs (En-Gu, En-Hi, En-Mr, En-Ta, En-Te, Et-En, Ne-En, Si-En)** — total ?; splits: test (-1); repo https://github.com/surrey-nlp/ALOPE

## Metrics

- `Spearman correlation` **(primary)** — range: other
  - Spearman rank correlation coefficient measuring the monotonic relationship between predicted quality scores and human/reference quality scores. Computed as 1 - (6 * sum(d_i^2)) / (n * (n^2 - 1)), where d_i is the difference between the ranks of predicted and gold scores.

## Input / output format

**Input**: Source sentence and its machine-translated target sentence.

**Output**: A single continuous regression score representing estimated translation quality.

## Scoring recipe

```python
def compute_spearman(pred_scores, gold_scores):
    n = len(pred_scores)
    rank_pred = sorted(range(n), key=lambda i: pred_scores[i])
    rank_gold = sorted(range(n), key=lambda i: gold_scores[i])
    d_sq = sum((rank_pred[i] - rank_gold[i])**2 for i in range(n))
    return 1 - (6 * d_sq) / (n * (n**2 - 1))
```

## Common pitfalls

- Placing the regression head at the final Transformer layer (TL-1) instead of intermediate layers (TL-7 or TL-11) significantly degrades correlation scores.
- Assuming larger model parameter size directly correlates with better QE performance; smaller models like LLaMA 3.2-3B can outperform larger ones when using optimal layer adaptation.
- Confusing zero-shot evaluation results with fine-tuned (SIFT/ALOPE) results, as zero-shot performance is substantially lower across all language pairs.

## Evidence (verbatim from paper)

> Table[3.3.2] reports the Spearman correlation scores obtained under zero-shot evaluation, alongside the results from the ALOPE framework with regression heads placed at various Transformer layers (See section[3.3] ). The table also highlights cases where ALOPE yields improvements over standard instruction fine-tuning (SIFT) results with LLMs. Notably, the performance under zero-shot settings is substantially lower across all eight low-resource language pairs when compared to both SIFT and ALOPE. When benchmarked against the best Spearman scores from SIFT, ALOPE obtains the best correlation scores for all evaluated language pairs.

## Citation

```bibtex
@misc{sindhujan2025alope,
  title={ALOPE: Adaptive Layer Optimization for Translation Quality Estimation using Large Language Models},
  author={Sindhujan et al. (2025)},
  year={2025},
  note={arXiv:2508.07484}
}
```

- arXiv: 2508.07484
