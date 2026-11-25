---
name: audio-turing-test-eval
description: Evaluates the human-likeness of Chinese text-to-speech systems using a Turing-test-inspired protocol where human listeners classify audio as human, unclear, or machine. It also benchmarks an automatic LLM-based evaluator against human judgments and traditional MOS prediction models to measure alignment and trap-item detection capability. Use when the user wants to benchmark on ATT-Corpus, or asks about evaluating this task. Reports HLS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.11200
  bibtex_key: wang2025audioturingtest
  confidence: high
---

# audio-turing-test-eval

> Audio Turing Test: Benchmarking the Human-likeness of Large Language Model-based Text-to-Speech Systems in Chinese — Wang et al. (2025) (arXiv:2505.11200, 2025)

## What this evaluates

Evaluates the human-likeness of Chinese text-to-speech systems using a Turing-test-inspired protocol where human listeners classify audio as human, unclear, or machine. It also benchmarks an automatic LLM-based evaluator against human judgments and traditional MOS prediction models to measure alignment and trap-item detection capability.

## Datasets

- **ATT-Corpus** — total ?; splits: test (-1)

## Metrics

- `HLS` **(primary)** — range: [0, 1]
  - Human-likeness Score (HLS) is the mean of human ratings per clip, where [Human]=1.0, [Unclear]=0.5, and [Machine]=0.0.
- `F1 score` — range: [0, 1]
  - Binary classification F1 on trap items (human vs synthetic) using a 0.5 decision threshold on predicted scores.
- `Kendall τ distance` — range: [0, 1]
  - Rank correlation distance between predicted HLS and human evaluation rankings; lower values indicate better alignment.

## Input / output format

**Input**: Audio clips (synthesized TTS output or human speech) presented to human evaluators or processed by Auto-ATT/Qwen2-Audio-Instruct.

**Output**: Human: single-choice label ([Human], [Unclear], [Machine]) plus written justification. Auto-ATT: continuous HLS prediction score.

## Scoring recipe

```python
def compute_hls(human_choices):
    ratings = [1.0 if c == 'Human' else 0.5 if c == 'Unclear' else 0.0 for c in human_choices]
    return sum(ratings) / len(ratings)

def compute_f1_auto_att(auto_scores, gold_labels):
    preds = [1 if s >= 0.5 else 0 for s in auto_scores]
    return f1_score(gold_labels, preds)

def compute_kendall_tau(pred_rankings, human_rankings):
    return kendalltau(pred_rankings, human_rankings).correlation
```

## Common pitfalls

- Confusing HLS with traditional Mean Opinion Score (MOS); HLS is more sensitive to subtle synthetic artifacts and reveals capability gaps MOS misses.
- Misinterpreting Kendall τ direction; the paper reports it as a 'distance' where lower values indicate better alignment, unlike standard correlation where higher is better.
- Assuming black-box vs white-box evaluation settings introduce systematic bias; the paper shows performance gaps are uniform across both.

## Evidence (verbatim from paper)

> Auto-ATT vastly outperformed the baselines, achieving an F1 score of 0.92, while UTMOSv2 reached only 0.14 and DNSMOSPro collapsed to 0.00 at the 0.5 decision threshold.

## Citation

```bibtex
@misc{wang2025audioturingtest,
  title={Audio Turing Test: Benchmarking the Human-likeness of Large Language Model-based Text-to-Speech Systems in Chinese},
  author={Wang et al. (2025)},
  year={2025},
  note={arXiv:2505.11200}
}
```

- arXiv: 2505.11200
