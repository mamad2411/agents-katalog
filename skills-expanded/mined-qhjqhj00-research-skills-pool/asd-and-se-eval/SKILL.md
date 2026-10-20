---
name: asd-and-se-eval
description: Evaluates a unified audio-visual model's ability to detect which speaker is actively speaking in multi-person video scenes and to enhance speech signals by removing background noise and interference. Use when the user wants to benchmark on AVA-ActiveSpeaker, LRS2, TalkSet, Columbia, MUSAN, or asks about evaluating this task. Reports mAP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2203.02216
  bibtex_key: xiong2022looklisten
  confidence: high
---

# asd-and-se-eval

> Look\&Listen: Multi-Modal Correlation Learning for Active Speaker Detection and Speech Enhancement — Junwen Xiong et al. (arXiv:2203.02216, 2022)

## What this evaluates

Evaluates a unified audio-visual model's ability to detect which speaker is actively speaking in multi-person video scenes and to enhance speech signals by removing background noise and interference.

## Datasets

- **AVA-ActiveSpeaker** — total 262; splits: train (120), val (33), test (109)
- **LRS2** — total ?; splits: train (-1), val (-1), test (-1)
- **TalkSet** — total 150000; splits: train (-1), val (-1), test (-1)
- **Columbia** — total ?; splits: test (-1)
- **MUSAN** — total ?; splits: (unstated)

## Metrics

- `mAP` **(primary)** — range: [0, 1]
  - Mean Average Precision across all frames/classes.
- `AUC` — range: [0, 1]
  - Area Under the Receiver Operating Characteristic curve.
- `F1` — range: [0, 1]
  - Harmonic mean of precision and recall.
- `SDR` — range: dB
  - Signal-to-Distortion Ratio measuring the quality of the enhanced audio relative to the clean reference.
- `PESQ` — range: [0, 5]
  - Perceptual Evaluation of Speech Quality, a standardized objective measure of perceived speech quality.

## Input / output format

**Input**: Audio: 13-channel MFCC features extracted with a 25ms window and 10ms stride. Visual: 112×112 cropped face images.

**Output**: Detection: per-frame active speaker probability/binary label. Enhancement: time-domain enhanced audio waveform.

## Scoring recipe

```python
def evaluate(predictions, labels, clean_audio, enhanced_audio):
    mAP = compute_mean_average_precision(predictions, labels)
    AUC = compute_roc_auc(predictions, labels)
    F1 = compute_f1_score(predictions, labels)
    SDR = compute_sdr(enhanced_audio, clean_audio)
    PESQ = compute_pesq(clean_audio, enhanced_audio)
    return {'mAP': mAP, 'AUC': AUC, 'F1': F1, 'SDR': SDR, 'PESQ': PESQ}
```

## Common pitfalls

- AVA-ActiveSpeaker test set is contest-exclusive; experiments are conducted on the validation set instead.
- MUSAN is used for noise augmentation during training, not as a direct test set for detection.
- Metrics cover two distinct tasks (detection vs. enhancement) and should not be averaged together.

## Evidence (verbatim from paper)

> To compare with the prior methods, five common-used metrics are employed for active speaker detection and speech enhancement evaluation. For detection, we choose to mean precision (mAP), area under the ROC curve (AUC) and F1 to measure the model performance. For speech enhancement, the metrics of SDR and perceptual evaluation of speech quality (PESQ) are employed to reflect the quality of enhanced speech signals.

## Citation

```bibtex
@misc{xiong2022looklisten,
  title={Look\&Listen: Multi-Modal Correlation Learning for Active Speaker Detection and Speech Enhancement},
  author={Junwen Xiong et al.},
  year={2022},
  note={arXiv:2203.02216}
}
```

- arXiv: 2203.02216
