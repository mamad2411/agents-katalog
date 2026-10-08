---
name: domain-video
description: "Use for video understanding: action or activity recognition, video classification, temporal action detection or localization in untrimmed video, gesture recognition, and general video analysis. Picks the right video model and the correct video-level split and metric. Triggers on 'video classification', 'action recognition', 'activity recognition', 'temporal action detection', 'video understanding', 'recognize actions', 'gesture', 'video dataset'."
---

# Video Understanding - Method Selection

Prefer models pretrained on large video datasets (Kinetics). Video is compute-heavy, so use mixed precision and clip-based training.

## Decision table
| Task | Recommended (recent, 2021-2025) | Notes |
|---|---|---|
| Action or video classification | VideoMAE or VideoMAEv2 (self-supervised pretrain, then fine-tune), Video Swin, UniFormerV2 | Kinetics-pretrained. Metric is top-1 and top-5 accuracy. |
| Efficient or low-budget | adapt a strong image backbone with temporal modules (AIM), or a small MoViNet | cheaper than a full video transformer. |
| Temporal action detection (localize actions in long untrimmed video) | ActionFormer, TadTR | metric is mAP at temporal IoU. |
| General-purpose video features | InternVideo family | strong for many downstream tasks. |

## Cross-cutting practice
- Sample frames (uniform or dense), train on short clips, and average multiple clips at test time.
- Augment with temporal cropping, per-frame flip and light photometric jitter. Keep flips label-safe.
- Leakage: split by VIDEO or subject, never by frame or by clips taken from the same video.
- Metrics: top-1 and top-5 accuracy for trimmed classification; mAP at temporal IoU for detection. Not frame accuracy.
- Explainability: per-frame Grad-CAM or spatiotemporal attention; show which frames the model attended to.
- Improve accuracy: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation`.
