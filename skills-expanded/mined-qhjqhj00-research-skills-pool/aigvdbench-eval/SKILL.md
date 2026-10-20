---
name: aigvdbench-eval
description: Evaluates the ability of AI-generated video detectors to distinguish between real and synthetically generated videos across diverse generation models, tasks (T2V, I2V, V2V), and temporal/spatial artifacts. Use when the user wants to benchmark on AIGVDBench, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.11035
  bibtex_key: ma2026aigvdbench
  confidence: high
---

# aigvdbench-eval

> Your One-Stop Solution for AI-Generated Video Detection — Long Ma et al. (2026) (arXiv:2601.11035, 2026)

## What this evaluates

Evaluates the ability of AI-generated video detectors to distinguish between real and synthetically generated videos across diverse generation models, tasks (T2V, I2V, V2V), and temporal/spatial artifacts.

## Datasets

- **AIGVDBench** — total 440000; splits: test (-1); repo https://github.com/LongMa-2025/AIGVDBench

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard binary classification accuracy: the proportion of correctly classified videos (real vs. AI-generated) out of the total evaluated. Calculated as correct predictions divided by total predictions.

## Input / output format

**Input**: Videos preprocessed by uniformly sampling 32 frames from the first 128 frames (or all frames if <128), center-cropped, resized to 256×256, and saved as PNG. For inference/training, only the first 8 sampled frames are used.

**Output**: Binary classification label indicating whether the video is real or AI-generated (or probability scores if supported by the detector).

## Scoring recipe

```python
def calculate_accuracy(predictions, labels):
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return correct / len(labels)
```

## Common pitfalls

- Using all 32 sampled frames for inference instead of the specified first 8 frames, which violates the benchmark's evaluation protocol.
- Assuming that higher objective quality of the generation model directly leads to lower detection accuracy, as the paper explicitly finds no consistent positive correlation.
- Evaluating Vision-Language Models (VLMs) solely on hard label outputs without probability thresholds, which complicates accurate performance assessment.

## Evidence (verbatim from paper)

> We preprocess each video by uniformly sampling 32 frames from its first 128 frames (or all available frames if the total is fewer than 128). Each frame is center-cropped along the shorter side and resized to 256×256 resolution. To maintain format consistency, all frames are saved in PNG format. In model training and inference, only the first 8 of the 32 sampled frames are used. ... A key limitation is their output of only labels rather than probabilities, complicating accuracy assessment.

## Citation

```bibtex
@misc{ma2026aigvdbench,
  title={Your One-Stop Solution for AI-Generated Video Detection},
  author={Long Ma et al. (2026)},
  year={2026},
  note={arXiv:2601.11035}
}
```

- arXiv: 2601.11035
