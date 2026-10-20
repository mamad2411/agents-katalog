---
name: artvip-eval
description: Evaluates the visual realism and physical fidelity of articulated digital assets for robot learning. It measures geometric detail, reconstruction quality, visual feature alignment with real-world data, and joint motion accuracy under external forces. Use when the user wants to benchmark on ArtVIP, or asks about evaluating this task. Reports joint displacement discrepancy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.04941
  bibtex_key: zhao2025artvip
  confidence: high
---

# artvip-eval

> ArtVIP: Articulated Digital Assets of Visual Realism, Modular Interaction, and Physical Fidelity for Robot Learning — Zhao Jin et al. (2025) (arXiv:2506.04941, 2025)

## What this evaluates

Evaluates the visual realism and physical fidelity of articulated digital assets for robot learning. It measures geometric detail, reconstruction quality, visual feature alignment with real-world data, and joint motion accuracy under external forces.

## Datasets

- **ArtVIP** — total 206; splits: full (206)

## Metrics

- `triangular faces` — range: other
  - Counts the number of triangular faces in the mesh to quantify geometric detail and surface smoothness.
- `VGGT reconstruction fidelity` — range: other
  - Evaluates structural fidelity and detail preservation using the VGGT multi-view reconstruction method on rendered assets.
- `CLIP feature distribution` — range: other
  - Extracts CLIP features from rendered simulation images and real-world photos, then visualizes their distribution via t-SNE to assess semantic and visual consistency.
- `joint displacement discrepancy` **(primary)** — range: other
  - Measures the spatial trajectory difference between real-world joint motion (tracked via optical system) and simulated joint motion under applied forces (1N–2.5N).

## Input / output format

**Input**: Rendered multi-view images of 3D assets; simulated and real-world joint trajectories under applied forces.

**Output**: Triangular face counts; reconstructed 3D models; t-SNE feature plots; spatial displacement trajectories of drawer keypoints.

## Scoring recipe

```python
tri_count = mesh.triangles.count
real_traj = track_joint_trajectory(real_world_video, optical_tracker)
sim_traj = run_simulation(asset, force=1.0) # repeat for 1.5, 2.0, 2.5
discrepancy = np.linalg.norm(real_traj - sim_traj, axis=1).mean()
sim_imgs = render_asset_in_isaac_sim(asset, viewpoints)
real_imgs = capture_real_world_images(asset)
sim_features = clip_model.encode(sim_imgs)
real_features = clip_model.encode(real_imgs)
# Alignment assessed via t-SNE visualization
```

## Common pitfalls

- PartNet-Mobility is excluded from texture/material comparisons due to URDF-to-USD conversion losing material info.
- CLIP alignment is assessed qualitatively via t-SNE visualization rather than a single scalar metric like FID.
- Physical fidelity requires matching exact force magnitudes (1N-2.5N) and pulley setups between real and sim.

## Evidence (verbatim from paper)

> To evaluate them objectively, we use the amount of triangular faces to quantify the geometric details for the mesh aspect and evaluate the quality of texture and material by visualizing the sim-to-real domain gap rendered by Isaac sim.

## Citation

```bibtex
@misc{zhao2025artvip,
  title={ArtVIP: Articulated Digital Assets of Visual Realism, Modular Interaction, and Physical Fidelity for Robot Learning},
  author={Zhao Jin et al. (2025)},
  year={2025},
  note={arXiv:2506.04941}
}
```

- arXiv: 2506.04941
