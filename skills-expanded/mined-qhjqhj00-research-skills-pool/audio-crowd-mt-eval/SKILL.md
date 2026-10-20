---
name: audio-crowd-mt-eval
description: This protocol evaluates machine translation quality by comparing crowd-sourced human judgments of text-only outputs versus multimodal (text + audio) outputs. It probes whether audio-based assessments improve inter-rater consistency and reveal system-level differences through prosodic and expressive features unavailable in text. Use when the user wants to benchmark on WMT German-English, or asks about evaluating this task. Reports standardized score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.14023
  bibtex_key: ulhaq2025audiobased
  confidence: high
---

# audio-crowd-mt-eval

> Audio-Based Crowd-Sourced Evaluation of Machine Translation Quality — Sami Ul Haq et al. (2025) (arXiv:2509.14023, 2025)

## What this evaluates

This protocol evaluates machine translation quality by comparing crowd-sourced human judgments of text-only outputs versus multimodal (text + audio) outputs. It probes whether audio-based assessments improve inter-rater consistency and reveal system-level differences through prosodic and expressive features unavailable in text.

## Datasets

- **WMT German-English** — total ?; splits: test (-1)

## Metrics

- `standardized score` **(primary)** — range: other
  - Per-worker normalized score: z = (x - μ_worker) / σ_worker. The system-level metric is the average of z across all segments assigned to that system.
- `raw average score` — range: other
  - Simple arithmetic mean of raw human assessment scores across all segments for a system.
- `Pearson correlation (r)` — range: [-1, 1]
  - Pearson correlation coefficient between initial and self-replicated judgment scores to measure consistency.
- `Wilcoxon rank-sum p-value` — range: [0, 1]
  - One-sided Wilcoxon rank-sum test comparing standardized score distributions between system pairs to assess statistical significance.

## Input / output format

**Input**: Human evaluators receive source text and machine-translated output in either text-only or multimodal (text + audio) format.

**Output**: Continuous quality score per instance. Scores are filtered based on quality control criteria (bad_reference, ask_again) before aggregation.

## Scoring recipe

```python
# Per-worker normalization
mu_w = mean([s for s in scores if s.worker == w])
sigma_w = std([s for s in scores if s.worker == w])
z = [(s - mu_w) / sigma_w for s in scores if s.worker == w]
# System-level aggregation
system_score = mean([z_i for z_i in z if z_i.system == sys])
# Ranking
ranked = sort_by(system_score, descending=True)
# Tie-breaker: average raw score
```

## Common pitfalls

- Raw scores and standardized scores produce different system rankings; relying solely on raw averages misrepresents relative performance.
- Crowd workers often rank literal human translations lower than MT outputs due to preference for straightforward phrasing.
- The evaluation uses a smaller judgment set per system than official WMT, limiting direct comparability with official rankings.

## Evidence (verbatim from paper)

> To compute the standardized score for each system, individual scores are first normalized using each worker’s mean and standard deviation (as per equation [1]). The standardized scores for all segments corresponding to a system are then averaged to obtain the system-level score (Graham et al., [2014]).

## Citation

```bibtex
@misc{ulhaq2025audiobased,
  title={Audio-Based Crowd-Sourced Evaluation of Machine Translation Quality},
  author={Sami Ul Haq et al. (2025)},
  year={2025},
  note={arXiv:2509.14023}
}
```

- arXiv: 2509.14023
