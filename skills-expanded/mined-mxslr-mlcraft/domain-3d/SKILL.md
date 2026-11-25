---
name: domain-3d
description: "Use for 3D and point cloud tasks: point cloud classification, 3D semantic or instance segmentation, 3D object detection from LiDAR, and depth or mesh analysis, including autonomous-driving and indoor-scan settings. Picks the right 3D backbone, representation, and scene-level split and metric. Triggers on 'point cloud', '3D', 'LiDAR', 'mesh', 'depth', '3D detection', '3D segmentation', 'ScanNet', 'KITTI', 'ModelNet', 'autonomous driving perception'."
---

# 3D and Point Cloud - Method Selection

Choose a representation first: raw points, or sparse voxels for large scenes. Normalize and center the cloud.

## Decision table
| Task | Recommended (recent, 2022-2025) | Notes |
|---|---|---|
| Point cloud classification | PointNeXt or Point Transformer v3; PointNet++ as a baseline | ModelNet-style. Metric is overall and mean-class accuracy. |
| Semantic segmentation (indoor or outdoor) | Point Transformer v3 (SOTA 2024) or sparse convolution (MinkowskiNet) | ScanNet, S3DIS. Metric is mIoU. |
| 3D object detection (driving) | sparse-voxel detectors (CenterPoint, VoxelNeXt) or transformer detectors | KITTI, nuScenes. Metric is mAP and NDS. |
| Efficiency-critical or very large clouds | Point Mamba (linear-time, 2024-2025) or sparse convolution | trade a little accuracy for speed and memory. |

## Cross-cutting practice
- Augment with rotation, jitter, scaling, and random point dropout. Voxelize for large outdoor scenes.
- Leakage: split by scene or scan, never by cropped block within the same scene.
- Metrics: overall accuracy for classification, mIoU for segmentation, mAP and NDS for detection.
- Explainability: per-point saliency; highlight the points that drove the prediction.
- Improve accuracy: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation`.
