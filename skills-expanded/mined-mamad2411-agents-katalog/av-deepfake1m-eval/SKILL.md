---
name: av-deepfake1m-eval
description: Evaluates models on detecting and temporally localizing audio-visual deepfakes in realistic, LLM-generated content. It probes robustness against multimodal manipulations like face reenactment and text-to-speech, testing both video-level classification and frame/segment-level localization. Use when the user wants to benchmark on AV-Deepfake1M, or asks about evaluating this task. Reports AP@0.5.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.15308
  bibtex_key: cai2023avdeepfake1m
  confidence: high
---

# av-deepfake1m-eval

> AV-Deepfake1M: A Large-Scale LLM-Driven Audio-Visual Deepfake Dataset — Cai et al. (2023) (arXiv:2311.15308, 2023)

## What this evaluates

Evaluates models on detecting and temporally localizing audio-visual deepfakes in realistic, LLM-generated content. It probes robustness against multimodal manipulations like face reenactment and text-to-speech, testing both video-level classification and frame/segment-level localization.

## Datasets

- **AV-Deepfake1M** — total 1000000; splits: fullset (-1), subset V (-1), subset A (-1); repo https://github.com/ControlNet/AV-Deepfake1M

## Metrics

- `AP@0.5` **(primary)** — range: percent
  - Average Precision at Intersection over Union (IoU) threshold of 0.5 for temporal segment localization. Computed by matching predicted fake segments to ground truth segments with IoU >= 0.5, then calculating precision-recall curve area.
- `AUC` — range: [0, 1]
  - Area Under the Receiver Operating Characteristic Curve for video-level deepfake classification. Measures the trade-off between true positive rate and false positive rate across all classification thresholds.

## Input / output format

**Input**: Audio-visual video clips (full multimodal set, or unimodal video/audio subsets). Models receive synchronized video frames and audio tracks.

**Output**: For localization: temporal segment boundaries or frame/segment-level fake probability scores. For detection: video-level binary classification or fake probability score.

## Scoring recipe

```python
def compute_ap_at_iou(pred_segments, gt_segments, iou_thresh=0.5):
    ious = compute_iou(pred_segments, gt_segments)
    matches = (ious >= iou_thresh).nonzero()
    return average_precision(matches, ious)

def compute_auc(scores, labels):
    fpr, tpr, _ = roc_curve(labels, scores)
    return auc(fpr, tpr)

# Aggregation for frame/segment predictions to video-level:
video_score = max(frame_scores)  # Optimal strategy per paper
```

## Common pitfalls

- Aggregation strategy for frame/segment predictions to video-level scores significantly impacts detection performance; the paper finds max pooling optimal over average or top-5 average.
- Models trained only on video-level labels perform poorly on temporal localization; fine-grained segment/frame labels are required for meaningful performance.
- Unimodal subsets (V and A) show different performance characteristics compared to the full multimodal set, so evaluating only on one modality may misrepresent robustness.

## Evidence (verbatim from paper)

> The frame- and segment-based deepfake detection methods can only produce frame- and segment-level predictions. Thus, a suitable aggregation strategy is required to generate the video-level predictions. We investigated several popular aggregation strategies, such as max (e.g., [6]), average (e.g., [15, 23, 63]), and the average of the highest 5 scores (e.g., [37]) for video-level predictions. The results of the experiment are presented in Table 9. The results show that max is the optimal aggregation strategy on AV-Deepfake1M for the considered deepfake detection methods. However, even with the frame-level labels provided during training, the AUC of the best-performing methods is less than 70, due to the multimodal modifications present in AV-Deepfake1M.

## Citation

```bibtex
@misc{cai2023avdeepfake1m,
  title={AV-Deepfake1M: A Large-Scale LLM-Driven Audio-Visual Deepfake Dataset},
  author={Cai et al. (2023)},
  year={2023},
  note={arXiv:2311.15308}
}
```

- arXiv: 2311.15308
