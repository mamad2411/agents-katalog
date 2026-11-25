---
name: ai4arctic-sod-eval
description: This benchmark evaluates pixel-wise sea ice stage of development (SOD) segmentation using dual-polarized SAR imagery. It probes a model's ability to accurately classify ice types under varying quantization levels and measures hardware efficiency across different computing platforms. Use when the user wants to benchmark on AI4Arctic Sea Ice Dataset, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.03075
  bibtex_key: alkoutayni2026tinyicenet
  confidence: high
---

# ai4arctic-sod-eval

> TinyIceNet: Low-Power SAR Sea Ice Segmentation for On-Board FPGA Inference — Al Koutayni et al. (2026) (arXiv:2603.03075, 2026)

## What this evaluates

This benchmark evaluates pixel-wise sea ice stage of development (SOD) segmentation using dual-polarized SAR imagery. It probes a model's ability to accurately classify ice types under varying quantization levels and measures hardware efficiency across different computing platforms.

## Datasets

- **AI4Arctic Sea Ice Dataset** — total ?; splits: test (20)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall calculated per SOD class and averaged (macro-F1). Computed on resized 512×512 scenes.
- `Frame Rate` — range: other
  - Number of full-resolution 512×512 scenes processed per second during end-to-end inference.
- `Energy per scene` — range: other
  - Total energy consumed (in millijoules) to process a single 512×512 scene from input to output segmentation map.

## Input / output format

**Input**: Dual-polarized (HH and HV) Sentinel-1 SAR scenes resized to 512×512 pixels, with pixel values normalized to [-1, 1], NaN values replaced, and invalid pixels (value 255) masked.

**Output**: A pixel-wise segmentation map assigning a Stage of Development (SOD) class label to each pixel in the 512×512 input scene.

## Scoring recipe

```python
def compute_f1(pred_map, gold_map, num_classes):
    f1_scores = []
    for c in range(num_classes):
        tp = ((pred_map == c) & (gold_map == c)).sum()
        fp = ((pred_map == c) & (gold_map != c)).sum()
        fn = ((pred_map != c) & (gold_map == c)).sum()
        prec = tp / (tp + fp + 1e-8)
        rec = tp / (tp + fn + 1e-8)
        f1_c = 2 * prec * rec / (prec + rec + 1e-8)
        f1_scores.append(f1_c)
    return sum(f1_scores) / len(f1_scores)
```

## Common pitfalls

- Post-training quantization (PTQ) severely degrades accuracy below 10-bit weights; evaluating only PTQ without quantization-aware training (QAT) yields misleadingly low scores.
- Energy efficiency comparisons must be normalized per processed scene (mJ/scene) rather than per frame or per watt, as hardware platforms differ drastically in throughput and thermal design power.
- Input preprocessing steps (normalization to [-1,1], NaN replacement, and masking invalid pixels at 255) are mandatory for consistent evaluation and are often omitted in reproduction attempts.

## Evidence (verbatim from paper)

> The full-precision FP32 model achieves an F1 score of 75.168%. PTQ shows a clear dependency on weight bitwidth: extremely low-precision weights (7–9 bits) severely degrade performance (13.19%–43.52%), whereas accuracy improves rapidly beyond 10 bits. Starting from 12 bits onward, PTQ stabilizes around 70–71% F1, maintaining within 4–5% of the baseline. The best PTQ performance is observed at 15 bits with 71.672%.

## Citation

```bibtex
@misc{alkoutayni2026tinyicenet,
  title={TinyIceNet: Low-Power SAR Sea Ice Segmentation for On-Board FPGA Inference},
  author={Al Koutayni et al. (2026)},
  year={2026},
  note={arXiv:2603.03075}
}
```

- arXiv: 2603.03075
