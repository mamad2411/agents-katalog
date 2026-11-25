---
name: avrobustbench-eval
description: Evaluates the robustness of audio-visual recognition models when subjected to simultaneous, correlated corruptions across both audio and video modalities at test-time. It measures how well models maintain classification accuracy under 75 distinct bimodal distributional shifts ranging from mild to extreme severity. Use when the user wants to benchmark on AudioSet-2C, VGGSound-2C, Kinetics-2C, EpicKitchens-2C, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.00358
  bibtex_key: maharana2025avrobustbench
  confidence: high
---

# avrobustbench-eval

> $\texttt{AVROBUSTBENCH}$: Benchmarking the Robustness of Audio-Visual Recognition Models at Test-Time — Maharana et al. (2025) (arXiv:2506.00358, 2025)

## What this evaluates

Evaluates the robustness of audio-visual recognition models when subjected to simultaneous, correlated corruptions across both audio and video modalities at test-time. It measures how well models maintain classification accuracy under 75 distinct bimodal distributional shifts ranging from mild to extreme severity.

## Datasets

- **AudioSet-2C** — total 16742; splits: test (16742)
- **VGGSound-2C** — total 14046; splits: test (14046)
- **Kinetics-2C** — total 3111; splits: test (3111)
- **EpicKitchens-2C** — total 205; splits: test (205)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard classification accuracy: the proportion of correctly predicted class labels out of the total number of test samples.

## Input / output format

**Input**: Corrupted audio-visual pairs (video frames and corresponding audio tracks) with 15 corruption types applied at 5 severity levels each.

**Output**: Predicted class label(s) for the audio-visual input.

## Scoring recipe

```python
correct = 0
for pred, gold in zip(predictions, gold_labels):
    if pred == gold:
        correct += 1
return correct / len(gold_labels)
```

## Common pitfalls

- Corruptions are applied simultaneously to both modalities (bimodal shifts), unlike prior benchmarks that shift only one modality.
- Severity is controlled via SNR for audio and specific parameters for video, which may be misinterpreted as independent rather than correlated distributional shifts.
- Dataset durations vary significantly (e.g., 10 seconds vs. 7.4 minutes for EpicKitchens-2C), requiring careful temporal alignment or segmentation during evaluation.

## Evidence (verbatim from paper)

> We formally introduce AVRobustBench, a comprehensive suite of 75 AV corruptions (15 corruptions, 5 severities) designed to evaluate AV model robustness under realistic distributional shifts, with a strong focus on real-world deployment, i.e, at test-time. State-of-the-art supervised and self-supervised models show significant performance drops under increasing corruption severity, with minimal gains from existing online test-time adaptation (TTA) methods under bimodal shifts.

## Citation

```bibtex
@misc{maharana2025avrobustbench,
  title={$\texttt{AVROBUSTBENCH}$: Benchmarking the Robustness of Audio-Visual Recognition Models at Test-Time},
  author={Maharana et al. (2025)},
  year={2025},
  note={arXiv:2506.00358}
}
```

- arXiv: 2506.00358
