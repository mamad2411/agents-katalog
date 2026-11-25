---
name: accuracy
description: Probes the pairwise ranking accuracy of an AI judge system when evaluating generated commit messages against a heuristic ground truth derived from multiple automatic text generation metrics. Use when the user has predictions and gold and needs to compute accuracy.
metadata:
  skill_kind: metric
  source_arxiv: 2411.17793
  bibtex_key: lin2024engineeringaijudge
  confidence: high
---

# accuracy

> Engineering AI Judge Systems — Lin et al. (2024) (arXiv:2411.17793, 2024)

## What this evaluates

Probes the pairwise ranking accuracy of an AI judge system when evaluating generated commit messages against a heuristic ground truth derived from multiple automatic text generation metrics.

## Datasets

- **MCMD** — total 100000; splits: studied_set (1889)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Accuracy = (1/n) * Σ I[MetricVote(p_i) == JudgeVote(p_i)] for i=1 to n. MetricVote is a ground-truth heuristic based on majority voting of 5 automatic metrics (BLEU, ROUGE-L, CiDEr, METEOR, BLEURT) comparing pairs of commit messages. JudgeVote is derived from the AI judge system's summed principle scores.

## Input / output format

**Input**: Code diff and a generated commit message for each data point.

**Output**: A numerical score between 0 and 1 per principle, summed to a final score for the commit message.

## Scoring recipe

```python
pairs = all_combinations(data_points, r=2)
correct = 0
for a, b in pairs:
    lar_cnt_a = count_metrics_where_a_better(a, b, metrics=[BLEU, ROUGE_L, CiDEr, METEOR, BLEURT])
    lar_cnt_b = count_metrics_where_b_better(a, b, metrics=[BLEU, ROUGE_L, CiDEr, METEOR, BLEURT])
    gt = a if lar_cnt_a > lar_cnt_b else (b if lar_cnt_b > lar_cnt_a else None)
    score_a = judge_system_score(a)
    score_b = judge_system_score(b)
    pred = a if score_a > score_b else (b if score_b > score_a else None)
    if gt == pred: correct += 1
accuracy = correct / len(pairs)
```

## Common pitfalls

- The ground truth is not human-annotated but derived from a majority-vote heuristic of 5 automatic metrics, which may not perfectly align with human preference.
- Evaluation is performed on pairwise comparisons (~71K pairs per language) rather than direct absolute scoring, making accuracy sensitive to tie-breaking rules.
- The dataset sample size per language is small (~377-379) due to resource constraints, though paired comparisons amplify the evaluation scale.

## Evidence (verbatim from paper)

> Finally, we calculate the accuracy of an AI judge system following: Accuracy = \frac{\sum_{i\=1}^{n}\mathbb{I}[\operatorname{MetricVote}(p_{i})\=\operatorname{JudgeVote}(p_{i})]}{n} where n is the total number of pairs in \mathcal{P}.

## Citation

```bibtex
@misc{lin2024engineeringaijudge,
  title={Engineering AI Judge Systems},
  author={Lin et al. (2024)},
  year={2024},
  note={arXiv:2411.17793}
}
```

- arXiv: 2411.17793
