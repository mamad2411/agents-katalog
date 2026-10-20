---
name: animationbench-eval
description: This benchmark evaluates video generation models on character-centric animation capabilities, specifically probing IP preservation, motion expressiveness, deformation accuracy, and multi-angle consistency. It operationalizes animation principles into measurable dimensions to identify gaps missed by standard realism-focused benchmarks. Use when the user wants to benchmark on AnimationBench, or asks about evaluating this task. Reports AnimationBench score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.15299
  bibtex_key: wu2026animationbench
  confidence: medium
---

# animationbench-eval

> AnimationBench: Are Video Models Good at Character-Centric Animation? — Leyi Wu et al. (2026) (arXiv:2604.15299, 2026)

## What this evaluates

This benchmark evaluates video generation models on character-centric animation capabilities, specifically probing IP preservation, motion expressiveness, deformation accuracy, and multi-angle consistency. It operationalizes animation principles into measurable dimensions to identify gaps missed by standard realism-focused benchmarks.

## Datasets

- **AnimationBench** — total 360; splits: test (360)

## Metrics

- `AnimationBench score` **(primary)** — range: [0, 1]
  - Automated scoring via Qwen3-VL-MAX VLM across multiple animation dimensions (e.g., IP consistency, deformation, 360-degree consistency, expression control, semantic extension, anticipation). Scores are computed per dimension and aggregated into an overall metric.
- `win-ratio` — range: [0, 1]
  - Human preference metric calculated as (wins + 0.5 * ties) / total comparisons for each dimension.
- `Spearman correlation` — range: [-1, 1]
  - Rank-based correlation coefficient measuring alignment between automatic AnimationBench scores and human win-ratios.

## Input / output format

**Input**: A source image (synthesized from character profiles/reference sheets or LLM-generated descriptions) paired with a text video prompt.

**Output**: A generated video clip.

## Scoring recipe

```python
def compute_animationbench_scores(predictions, prompts, dimensions):
    dim_scores = {dim: [] for dim in dimensions}
    for video, prompt in zip(predictions, prompts):
        for dim in dimensions:
            score = vlm_scorer.evaluate(video=video, prompt=prompt, dimension=dim)
            dim_scores[dim].append(score)
    # Aggregate per dimension, then compute overall score
    overall = {dim: sum(dim_scores[dim]) / len(dim_scores[dim]) for dim in dimensions}
    return overall
```

## Common pitfalls

- VLM evaluators may inherit training data biases for popular characters; the benchmark mitigates this by including 30 self-designed IPs, but evaluators still require careful prompt engineering to avoid memorization artifacts.
- The benchmark supports both close-set (reproducible comparison) and open-set (diagnostic refinement) modes; results are not directly comparable across modes without accounting for the optimization step applied in open-set evaluation.
- Human alignment is measured via win-ratio and Spearman correlation, which capture relative preference and rank consistency but do not quantify absolute quality gaps or magnitude of differences.

## Evidence (verbatim from paper)

> We quantified human preference using a win-ratio metric (1 for wins, 0 for losses, 0.5 for ties). The per-dimension and overall correlations between the automatic AnimationBench scores and human win ratios, shown in Fig. 8, confirm the reliability of our evaluation framework. Spearman’s correlation coefficient was used to measure the consistency between AnimationBench’s per-dimension evaluations and human judgments.

## Citation

```bibtex
@misc{wu2026animationbench,
  title={AnimationBench: Are Video Models Good at Character-Centric Animation?},
  author={Leyi Wu et al. (2026)},
  year={2026},
  note={arXiv:2604.15299}
}
```

- arXiv: 2604.15299
