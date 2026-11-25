---
name: activitynet-comp-eval
description: Evaluates fine-grained temporal and compositional alignment in video-text models by testing their ability to distinguish between videos and captions that contain subtle structural disruptions. It probes sensitivity to temporal reordering, action word replacement, and segment-level misalignment, as well as the model's robustness to combined disruptions. Use when the user wants to benchmark on ActivityNet-Comp, YouCook2-Comp, or asks about evaluating this task. Reports binary classification accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.03970
  bibtex_key: kim2025videocomp
  confidence: high
---

# activitynet-comp-eval

> VideoComp: Advancing Fine-Grained Compositional and Temporal Alignment in Video-Text Models — Dahun Kim et al. (2025) (arXiv:2504.03970, 2025)

## What this evaluates

Evaluates fine-grained temporal and compositional alignment in video-text models by testing their ability to distinguish between videos and captions that contain subtle structural disruptions. It probes sensitivity to temporal reordering, action word replacement, and segment-level misalignment, as well as the model's robustness to combined disruptions.

## Datasets

- **ActivityNet-Comp** — total ?; splits: test (-1); repo https://github.com/google-deepmind/video_comp
- **YouCook2-Comp** — total ?; splits: test (-1); repo https://github.com/google-deepmind/video_comp

## Metrics

- `binary classification accuracy` **(primary)** — range: percent
  - Percentage of correctly identified matching text candidates in a binary choice setup where one positive and one negative caption are randomly shuffled.
- `comprehensive score` — range: percent
  - Multiplicative combination of binary accuracy scores across temporal reordering, action replacement, and segment mismatch disruption types.
- `Recall@1` — range: percent
  - Percentage of queries where the correct video or text appears in the top-1 retrieval result.

## Input / output format

**Input**: A video (16 uniformly sampled frames) paired with two text candidates (one positive, one negative), randomly shuffled.

**Output**: For classification: the digit '1' or '2' indicating the matching text candidate. For retrieval: a similarity score or ranked list.

## Scoring recipe

```python
def score_binary_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    return correct / len(gold) * 100

def score_comprehensive(acc_temp, acc_action, acc_seg):
    return acc_temp * acc_action * acc_seg
```

## Common pitfalls

- Random guessing baseline is 50% for individual disruption types but drops to 12.5% for the comprehensive multiplicative score, which can mislead comparisons if not accounted for.
- Models often rely on object/action-level semantics rather than temporal structure, leading to inflated accuracy on action replacement tasks compared to temporally sensitive tasks like reordering.
- Retrieval performance on compositional benchmarks may not correlate with classification accuracy due to different training objectives (contrastive vs. pairwise preference).

## Evidence (verbatim from paper)

> We also report a comprehensive score, computed as the multiplicative combination of binary accuracy scores for all disruption types, as described in Sec.[3.4]. Table 2: Evaluation of compositional understanding with our methods CompLoss and CompPretrain, on ActivityNet-Comp and YouCook2-Comp benchmarks. We report binary classification accuracy (%). Note a random prediction results in a baseline score of 50.0%.

## Citation

```bibtex
@misc{kim2025videocomp,
  title={VideoComp: Advancing Fine-Grained Compositional and Temporal Alignment in Video-Text Models},
  author={Dahun Kim et al. (2025)},
  year={2025},
  note={arXiv:2504.03970}
}
```

- arXiv: 2504.03970
