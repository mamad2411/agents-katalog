---
name: accflow-eval
description: Evaluates a model's ability to estimate long-range dense optical flow between distant video frames, specifically testing robustness to large motions and severe occlusions. It measures how well the model accumulates flow over multiple steps while correcting misalignments and occlusion artifacts. Use when the user wants to benchmark on CVO, HS-Sintel, or asks about evaluating this task. Reports EPE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2308.13133
  bibtex_key: wu2023accflow
  confidence: high
---

# accflow-eval

> AccFlow: Backward Accumulation for Long-Range Optical Flow — Guangyang Wu et al. (arXiv:2308.13133, 2023)

## What this evaluates

Evaluates a model's ability to estimate long-range dense optical flow between distant video frames, specifically testing robustness to large motions and severe occlusions. It measures how well the model accumulates flow over multiple steps while correcting misalignments and occlusion artifacts.

## Datasets

- **CVO** — total 1000; splits: test_clean (500), test_final (500)
- **HS-Sintel** — total 19; splits: test (19)

## Metrics

- `EPE` **(primary)** — range: other (pixels)
  - Average L2 distance between predicted and ground-truth flow vectors: EPE = (1/N) Σ ||F_pred - F_gt||_2. Reported separately for all pixels (ALL), non-occluded pixels (NOC), and occluded pixels (OCC) using standard occlusion masks.

## Input / output format

**Input**: Sequences of video frames (typically 7 frames of 512×512 resolution) representing the start and intermediate frames for flow estimation.

**Output**: Dense optical flow field (H×W×2 displacement vectors) representing the motion from the first frame to the target frame.

## Scoring recipe

```python
def compute_epe(pred_flow, gt_flow, occlusion_mask=None):
    error = torch.sqrt(torch.sum((pred_flow - gt_flow)**2, dim=-1))
    if occlusion_mask is not None:
        error = error[occlusion_mask]
    return error.mean()
```

## Common pitfalls

- HS-Sintel uses 1008 FPS video sequences but evaluates with 24 FPS ground-truth flows, which underestimates the true motion magnitude for long-range estimation.
- EPE must be computed separately for ALL, NOC, and OCC regions using proper occlusion masks; reporting a single averaged EPE hides performance degradation in occluded areas.
- Inference time is highly dependent on frame count and resolution; comparisons must standardize to 7 frames at 512×512 on the same GPU (e.g., GTX 3090) to be fair.

## Evidence (verbatim from paper)

> We compare the existing methods in terms of the average End-Point-Error (EPE) applied to all pixels (ALL) and occlusion regions (OCC). In Table 1, we compare our AccFlow with previous methods on two benchmarks, and our AccFlow outperforms all the previous methods by a large margin especially for occluded regions.

## Citation

```bibtex
@misc{wu2023accflow,
  title={AccFlow: Backward Accumulation for Long-Range Optical Flow},
  author={Guangyang Wu et al.},
  year={2023},
  note={arXiv:2308.13133}
}
```

- arXiv: 2308.13133
