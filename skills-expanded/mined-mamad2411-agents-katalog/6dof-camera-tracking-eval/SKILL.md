---
name: 6dof-camera-tracking-eval
description: Evaluates the tracking accuracy of a 6-DoF autonomous camera algorithm in a simulated surgical environment. It also measures how different camera control strategies impact human rater accuracy when assessing surgical skill from video. Use when the user wants to benchmark on da Vinci wire chaser simulation, or asks about evaluating this task. Reports assessment_error.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2012.02836
  bibtex_key: abdelaal2020orientation
  confidence: high
---

# 6dof-camera-tracking-eval

> Orientation Matters: 6-DoF Autonomous Camera Movement for Minimally Invasive Surgery — Alaa Eldin Abdelaal et al. (arXiv:2012.02836, 2020)

## What this evaluates

Evaluates the tracking accuracy of a 6-DoF autonomous camera algorithm in a simulated surgical environment. It also measures how different camera control strategies impact human rater accuracy when assessing surgical skill from video.

## Datasets

- **da Vinci wire chaser simulation** — total ?; splits: test (-1)

## Metrics

- `image_centering_error` — range: other
  - Euclidean distance in pixels between the target feature center and the image center.
- `3d_centering_error` — range: other
  - Euclidean distance in millimeters between the target feature and the camera's optical axis at a fixed distance.
- `orientation_error` — range: other
  - Angular difference in degrees between the camera's optical axis and the target feature's normal vector.
- `assessment_error` **(primary)** — range: other
  - Absolute difference between the ground truth error provided by the simulator and the error score reported by a human rater.

## Input / output format

**Input**: Simulated camera state and target feature trajectories for algorithm testing; video feeds of surgical tasks for human raters.

**Output**: 6-DoF camera pose (position and orientation) for tracking; human-assigned error scores for skill assessment.

## Scoring recipe

```python
# Tracking metrics
image_centering_error = distance(pixel_coords(target), pixel_coords(image_center))
3d_centering_error = distance(3d_coords(target), camera_position + camera_orientation * fixed_distance)
orientation_error = angle_between(camera_optical_axis, target_normal_vector)

# User study metric
assessment_error = abs(subject_reported_error - simulator_ground_truth_error)
```

## Common pitfalls

- Orientation error spikes during motion planning segments when orientation constraints are relaxed to keep features in view.
- User study results exclude participants who fail attention checks and remove statistical outliers before comparing conditions.

## Evidence (verbatim from paper)

> We compute the three metrics: centering error with respect to the left image space, centering error in the 3D space, and orientation error... Assessment errors refer to the absolute difference between ground truth errors (which we get from the simulator) and the reported errors by each subject.

## Citation

```bibtex
@misc{abdelaal2020orientation,
  title={Orientation Matters: 6-DoF Autonomous Camera Movement for Minimally Invasive Surgery},
  author={Alaa Eldin Abdelaal et al.},
  year={2020},
  note={arXiv:2012.02836}
}
```

- arXiv: 2012.02836
