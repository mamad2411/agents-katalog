---
name: activity-recognition-eval
description: Evaluates a model's ability to recognize human activities in real-time by simultaneously learning from skeletal pose data and object attributes. It probes the integration of multi-modal cues (color, shape, distance, or object probabilities) for accurate and efficient activity classification in robotics scenarios. Use when the user wants to benchmark on Cornell Activity Dataset (CAD-60), MSR Daily Activity 3D Dataset, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.03453
  bibtex_key: reily2020simultaneous
  confidence: high
---

# activity-recognition-eval

> Simultaneous Learning from Human Pose and Object Cues for Real-Time Activity Recognition — Reily et al. (2020) (arXiv:2004.03453, 2020)

## What this evaluates

Evaluates a model's ability to recognize human activities in real-time by simultaneously learning from skeletal pose data and object attributes. It probes the integration of multi-modal cues (color, shape, distance, or object probabilities) for accurate and efficient activity classification in robotics scenarios.

## Datasets

- **Cornell Activity Dataset (CAD-60)** — total ?; splits: test (-1)
- **MSR Daily Activity 3D Dataset** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly identified activity executions out of the total number of executions.
- `Processing Speed (Hz)` — range: other
  - Number of recognition processing cycles per second, calculated as 1 divided by time per frame.

## Input / output format

**Input**: Per instance: color and depth images, annotated 3D skeleton joint positions (15 joints for CAD-60, 20 for MSR), and object attributes (RGB histograms, HOG features, 3D object-joint distances, or YOLO-derived object category probabilities).

**Output**: Activity class label (classification) and a weight matrix U indicating the importance of each object attribute to the predicted activity.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100

def compute_speed(time_per_frame_sec):
    return 1.0 / time_per_frame_sec
```

## Common pitfalls

- Dataset train/val/test splits are not explicitly defined in the paper.
- Object attributes must be extracted using specific modalities (RGB histograms, HOG, or YOLO probabilities) rather than raw images.
- Real-time speed benchmarks are hardware-dependent (tested on Intel i5 with 4GB RAM).

## Evidence (verbatim from paper)

> It is observed that our approach achieves an activity recognition accuracy of 97.71%.

## Citation

```bibtex
@misc{reily2020simultaneous,
  title={Simultaneous Learning from Human Pose and Object Cues for Real-Time Activity Recognition},
  author={Reily et al. (2020)},
  year={2020},
  note={arXiv:2004.03453}
}
```

- arXiv: 2004.03453
