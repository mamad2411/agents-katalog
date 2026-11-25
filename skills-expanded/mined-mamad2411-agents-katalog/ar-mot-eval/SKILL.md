---
name: ar-mot-eval
description: Evaluates a model's ability to track multiple visual objects in video sequences using auditory referring expressions instead of text. It probes cross-modal alignment, robustness to varying weather and video quality conditions, and handling of complex, unconstrained traffic dynamics. Use when the user wants to benchmark on Echo-KITTI, Echo-KITTI+, Echo-BDD, or asks about evaluating this task. Reports HOTA.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.18302
  bibtex_key: lin2024echotrack
  confidence: high
---

# ar-mot-eval

> EchoTrack: Auditory Referring Multi-Object Tracking for Autonomous Driving — Lin et al. (2024) (arXiv:2402.18302, 2024)

## What this evaluates

Evaluates a model's ability to track multiple visual objects in video sequences using auditory referring expressions instead of text. It probes cross-modal alignment, robustness to varying weather and video quality conditions, and handling of complex, unconstrained traffic dynamics.

## Datasets

- **Echo-KITTI** — total ?; splits: train (15), test (3); repo https://github.com/lab206/EchoTrack
- **Echo-KITTI+** — total ?; splits: train (15), test (3); repo https://github.com/lab206/EchoTrack
- **Echo-BDD** — total ?; splits: train (42), test (8); repo https://github.com/lab206/EchoTrack

## Metrics

- `HOTA` **(primary)** — range: [0, 100]
  - Higher-Order Tracking Accuracy (HOTA) jointly evaluates detection and association performance across thresholds. It combines Detection Accuracy (DetA) and Association Accuracy (AsscA) into a single metric: HOTA = sqrt(DetA * AsscA).

## Input / output format

**Input**: Video frames (spatiotemporal sequence) paired with a single audio referring expression describing target object(s).

**Output**: Per-frame bounding boxes for all tracked objects that match the audio expression, including track IDs across frames.

## Scoring recipe

```python
def compute_hota(predictions, ground_truth):
    # predictions: list of dicts with frame_id, track_id, bbox, score
    # ground_truth: list of dicts with frame_id, track_id, bbox, is_dontcare
    # Align predictions and ground truth tracks using Hungarian algorithm or greedy matching
    # Compute DetA (detection accuracy) and AsscA (association accuracy) across IoU thresholds
    # HOTA = sqrt(DetA * AsscA)
    return official_hota_evaluator(predictions, ground_truth)
```

## Common pitfalls

- Audio expressions may refer to multiple objects or a single object may be referred to by multiple expressions, requiring many-to-many matching rather than strict one-to-one pairing.
- Models must handle significant variations in weather (fog, rain, snow) and video quality (blur, exposure) without degradation, which many baselines fail to do.
- Expression complexity varies (short vs. long); models trained only on short expressions often fail on Echo-KITTI+ where average length doubles.

## Evidence (verbatim from paper)

> Evaluated on large-scale benchmarks (Echo-KITTI, Echo-KITTI+, Echo-BDD), EchoTrack outperforms existing text-based and general MOT methods in HOTA metrics, demonstrating superior performance in real-world traffic scenarios with complex, unconstrained dynamics.

## Citation

```bibtex
@misc{lin2024echotrack,
  title={EchoTrack: Auditory Referring Multi-Object Tracking for Autonomous Driving},
  author={Lin et al. (2024)},
  year={2024},
  note={arXiv:2402.18302}
}
```

- arXiv: 2402.18302
