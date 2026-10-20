---
name: airscape-6dof-eval
description: Evaluates a generative world model's ability to predict first-person future video observations under specified 6DoF aerial motion intentions. It probes spatio-temporal consistency, motion alignment, and counterfactual reasoning in 3D aerial environments. Use when the user wants to benchmark on AirScape Dataset, or asks about evaluating this task. Reports IAR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2507.08885
  bibtex_key: zhaobaining2025airscape
  confidence: high
---

# airscape-6dof-eval

> AirScape: An Aerial Generative World Model with Motion Controllability — Zhao et al. (2025) (arXiv:2507.08885, 2025)

## What this evaluates

Evaluates a generative world model's ability to predict first-person future video observations under specified 6DoF aerial motion intentions. It probes spatio-temporal consistency, motion alignment, and counterfactual reasoning in 3D aerial environments.

## Datasets

- **AirScape Dataset** — total 11000; splits: train (9900), test (1100)

## Metrics

- `FID` — range: other
  - Fréchet Inception Distance measuring frame-wise distribution differences between generated and ground truth videos. Requires cropping and resizing predicted frames to match ground truth resolution.
- `FVD` — range: other
  - Fréchet Video Distance evaluating temporal distribution differences. Requires uniformly downsampling generated and ground truth videos to the same number of frames.
- `IAR` **(primary)** — range: percent
  - Intention Alignment Rate, the percentage of generated videos judged by human raters to be semantically aligned with the input motion intention. Evaluated via binary choice.

## Input / output format

**Input**: Motion intention text (translation, rotation, or compound) and a starting frame or context video, plus ground truth future video for evaluation.

**Output**: A sequence of predicted future frames (video) representing the first-person perspective under the given motion intention.

## Scoring recipe

```python
def compute_metrics(pred_video, gt_video, intention):
    pred_frames = crop_resize(pred_video, gt_video.resolution)
    pred_frames = downsample(pred_frames, num_frames=gt_video.frames)
    gt_frames = downsample(gt_video, num_frames=gt_video.frames)
    fid = compute_frechet_inception_distance(pred_frames, gt_frames)
    fvd = compute_frechet_video_distance(pred_frames, gt_frames)
    
    aligned_count = 0
    for pred_video, intention in test_set:
        if human_judge_binary(intention, pred_video) == 'aligned':
            aligned_count += 1
    iar = (aligned_count / len(test_set)) * 100
    return fid, fvd, iar
```

## Common pitfalls

- FID and FVD require strict preprocessing: predicted frames must be cropped/resized to match ground truth resolution, and both must be downsampled to the same frame count before computing distribution distances.
- IAR is a human-evaluated metric, not automated; relying on VLMs for semantic alignment yields poor results as noted in the paper.
- Evaluations are split by motion type (Translation, Rotation, Compound), so reporting a single average without specifying the split can be misleading.

## Evidence (verbatim from paper)

> We evaluate the quality of the world model’s predictive embodied observations from two perspectives: (1) the spatio-temporal distribution differences between the generated videos and the ground truth, and (2) the semantic alignment between the generated videos and the input intention. Automatic Evaluation: FID is used to measure the frame-wise distribution differences between the generated videos and the ground truth videos. For FID evaluation, we crop and resize the predicted frames to match the resolution of the ground truth. FVD evaluates the distribution differences in the temporal dimension. For FVD evaluation, all generated videos and ground truth videos are uniformly downsampled to the same number of frames. Human Evaluation: ... The average intention alignment rate (IAR) is then calculated across the entire test set.

## Citation

```bibtex
@misc{zhaobaining2025airscape,
  title={AirScape: An Aerial Generative World Model with Motion Controllability},
  author={Zhao et al. (2025)},
  year={2025},
  note={arXiv:2507.08885}
}
```

- arXiv: 2507.08885
