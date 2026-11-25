---
name: atrw-reid-eval
description: Evaluates Amur tiger re-identification in the wild by measuring how well models can match tiger identities across different camera views and detection/pose conditions. It probes robustness to non-rigid body deformation, extreme pose variation, and domain shifts between controlled (plain) and uncontrolled (wild) environments. Use when the user wants to benchmark on ATRW, or asks about evaluating this task. Reports mAP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1906.05586
  bibtex_key: li2019atrw
  confidence: high
---

# atrw-reid-eval

> ATRW: A Benchmark for Amur Tiger Re-identification in the Wild — Li et al. (2019) (arXiv:1906.05586, 2019)

## What this evaluates

Evaluates Amur tiger re-identification in the wild by measuring how well models can match tiger identities across different camera views and detection/pose conditions. It probes robustness to non-rigid body deformation, extreme pose variation, and domain shifts between controlled (plain) and uncontrolled (wild) environments.

## Datasets

- **ATRW** — total ?; splits: train (-1), val (-1)

## Metrics

- `mAP` **(primary)** — range: [0, 1]
  - Mean Average Precision computed over the ranked list of candidate identities for each query. In re-ID, it is typically calculated as the average of precision at each recall level, or equivalently the mean of 1/rank for single-positive queries.
- `top-1` — range: [0, 1]
  - Accuracy at rank 1, representing the percentage of queries where the correct identity is the top-ranked match.
- `top-5` — range: [0, 1]
  - Accuracy at rank 5, representing the percentage of queries where the correct identity appears within the top 5 ranked matches.

## Input / output format

**Input**: RGB images of tigers. For detection: full scene images. For pose: full scene images. For re-ID: cropped tiger images normalized to 256×128 (plain case) or automatically cropped using bounding boxes and pose keypoints (wild case).

**Output**: For detection: bounding box coordinates. For pose: 2D keypoint coordinates. For re-ID: ranked list of candidate identity IDs with similarity scores.

## Scoring recipe

```python
def compute_reid_metrics(predictions, gold):
    top1_correct = 0
    top5_correct = 0
    ap_scores = []
    for q_id, candidates in predictions.items():
        true_id = gold[q_id]
        ranks = [i for i, (cand_id, _) in enumerate(candidates) if cand_id == true_id]
        if ranks:
            rank = ranks[0]
            if rank == 0: top1_correct += 1
            if rank < 5: top5_correct += 1
            ap_scores.append(1.0 / (rank + 1))
    n = len(predictions)
    return {
        'top-1': top1_correct / n,
        'top-5': top5_correct / n,
        'mAP': sum(ap_scores) / n
    }
```

## Common pitfalls

- Confusing the 'plain' case (manually annotated bounding boxes) with the 'wild' case (automatically detected boxes + pose keypoints), which causes significant performance drops and misleads ablation studies.
- Assuming standard human pose estimators work out-of-the-box; tiger skeletons require custom annotation and code modification, as OpenPose failed to converge on this dataset.
- Ignoring the cross-camera vs. single-camera distinction, as performance degrades drastically in cross-camera wild settings, making single-camera results unrepresentative of real deployment.

## Evidence (verbatim from paper)

> Table 9 lists the mAP and top-k (k=1,5) results for all the compared baseline methods. For the wild case, we evaluate PPbM with bounding boxes provided by SSD-MobileNet-v2, and pose provided by the HRNet. Figure 12 further illustrates the recognition rate vs rank through the Cumulative Match Curve (CMC).

## Citation

```bibtex
@misc{li2019atrw,
  title={ATRW: A Benchmark for Amur Tiger Re-identification in the Wild},
  author={Li et al. (2019)},
  year={2019},
  note={arXiv:1906.05586}
}
```

- arXiv: 1906.05586
