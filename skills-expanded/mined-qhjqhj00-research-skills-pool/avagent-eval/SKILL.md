---
name: avagent-eval
description: Evaluates the quality of audio-visual joint representations by testing downstream capabilities including classification, sound source localization, segmentation, and source separation. It measures how well an agentic workflow aligns audio and video modalities to improve cross-modal recognition and spatial/temporal synchronization. Use when the user wants to benchmark on VGGSound-Music, VGGSound-Instruments, MUSIC, Flickr-SoundNet, AVSBench, VGGSound-All, AudioSet, or asks about evaluating this task. Reports Top-1 Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.23230
  bibtex_key: mo2024avagent
  confidence: high
---

# avagent-eval

> Aligning Audio-Visual Joint Representations with an Agentic Workflow — Mo et al. (2024) (arXiv:2410.23230, 2024)

## What this evaluates

Evaluates the quality of audio-visual joint representations by testing downstream capabilities including classification, sound source localization, segmentation, and source separation. It measures how well an agentic workflow aligns audio and video modalities to improve cross-modal recognition and spatial/temporal synchronization.

## Datasets

- **VGGSound-Music** — total 42109; splits: train (40908), test (1201)
- **VGGSound-Instruments** — total 32000; splits: (unstated)
- **MUSIC** — total 448; splits: train (358), test (90)
- **Flickr-SoundNet** — total 5000; splits: train (4500), test (500)
- **AVSBench** — total 4932; splits: train (3452), val (740), test (740)
- **VGGSound-All** — total ?; splits: (unstated)
- **AudioSet** — total ?; splits: (unstated)

## Metrics

- `Top-1 Accuracy` **(primary)** — range: percent
  - Percentage of correctly predicted class labels out of total instances. Computed separately for linear probing and fine-tuning protocols.
- `Precision, AP, F1` — range: percent
  - Precision is true positives over predicted positives. AP is the area under the precision-recall curve. F1 is the harmonic mean of precision and recall. Used for sound source localization.
- `mIoU, F1` — range: percent
  - mIoU is the mean intersection-over-union across all classes for pixel-wise segmentation masks. F1 is the harmonic mean of precision and recall at the pixel level.
- `SDR, SAR` — range: dB
  - Signal-to-Distortion Ratio (SDR) measures overall quality of separated audio against ground truth. Signal-to-Artifact Ratio (SAR) measures the level of artifacts introduced during separation.

## Input / output format

**Input**: Per instance: an image resized to 224×224 and a 3-second audio clip sampled at 8kHz. The audio is converted to a 128×128 log spectrogram tensor using STFT (50ms window, 25ms hop).

**Output**: Task-specific: class labels for classification, bounding boxes or probability maps for localization, pixel-wise masks for segmentation, and separated audio waveforms for source separation.

## Scoring recipe

```python
def score(predictions, gold, task):
    if task == 'classification':
        return (predictions == gold).mean() * 100
    elif task == 'localization':
        prec = tp / (tp + fp)
        f1 = 2 * prec * recall / (prec + recall)
        ap = average_precision(gold, predictions)
        return prec, ap, f1
    elif task == 'segmentation':
        ious = intersection_over_union(predictions, gold)
        return ious.mean(), f1_score(gold, predictions)
    elif task == 'separation':
        return sdr(gold, predictions), sar(gold, predictions)
```

## Common pitfalls

- Using the full original MUSIC dataset (448 videos) instead of the paper's reduced split (358 train / 90 test) due to unavailable videos.
- Confusing VGGSound-Music (49 classes) with VGGSound-All (221 classes) when reporting classification results.
- Applying standard AVSBench splits instead of the fixed 3,452/740/740 train/val/test split mandated by the paper.
- Mixing up SDR (Signal-to-Distortion Ratio) and SAR (Signal-to-Artifact Ratio) for source separation evaluation.

## Evidence (verbatim from paper)

> Following the prior work, we use the Precision and F1 scores defined in[mo2022SLAVC] for visual source localization. For source separation, following[zhao2018the], we use Signal-to-Distortion Ratio (SDR) and Signal-to-Artifact Ratio (SAR). For audio-visual segmentation, we apply mIoU and F1 scores as evaluation metrics, following the previous work. Linear-prob and fine-tuning classification evaluations are based on top-1 accuracy, which measures the class difference from the ground-truth labels.

## Citation

```bibtex
@misc{mo2024avagent,
  title={Aligning Audio-Visual Joint Representations with an Agentic Workflow},
  author={Mo et al. (2024)},
  year={2024},
  note={arXiv:2410.23230}
}
```

- arXiv: 2410.23230
