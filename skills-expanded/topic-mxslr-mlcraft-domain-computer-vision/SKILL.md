---
name: domain-computer-vision
description: "Use for computer-vision tasks on natural/general images: image classification, object detection (vehicles, faces, people, products), face recognition/verification, semantic/instance segmentation, keypoints/pose, OCR. Picks the best architecture per sub-task and the right transfer-learning + augmentation recipe. Triggers on 'detect objects/faces/vehicles', 'classify images', 'segment', 'bounding boxes', 'recognize faces', 'image dataset'."
---

# Computer Vision - Method Selection

Pick by sub-task, then apply `training-optimization` + `rigorous-evaluation`. Prefer pretrained backbones; train from scratch only with very large data.

## Decision table
| Sub-task | Recommended (strong default, then heavier option) | Notes |
|---|---|---|
| Image classification | **EfficientNet / ConvNeXt**, then ViT/Swin (needs more data) | ConvNeXt/EffNet are strong, data-efficient. Match input resolution to the backbone. |
| Object detection | **YOLO (v8/11) / RT-DETR**, then DINO-DETR or Faster R-CNN | YOLO for speed/deploy; DETR-family for accuracy. Use mAP@IoU. |
| Face detection | **RetinaFace / YOLO-face / MTCNN** | Detection ≠ recognition. |
| Face recognition/verification | **ArcFace / CosFace embeddings** + similarity | Metric-learning, not softmax classification. Evaluate with verification (ROC/EER), gallery split by identity. |
| Semantic segmentation | **U-Net / DeepLabv3+ / SegFormer** | Dice/IoU. Watch class imbalance. |
| Instance segmentation | **Mask R-CNN / YOLO-seg** | |
| Promptable / zero-shot seg | **SAM / SAM2** | Great for annotation & few-shot. |
| Keypoints / pose | **HRNet / YOLO-pose / ViTPose** | |
| OCR | **detector + recognizer (DBNet + CRNN) / TrOCR / PaddleOCR** | |

## Cross-cutting CV practice
- **Transfer learning** from ImageNet; two-phase fine-tune; discriminative LR (see `training-optimization`).
- **Augmentation matched to the task**: flips only if label-invariant (a horizontally-flipped digit/letter is different!); mild rotation/scale/color; MixUp/CutMix help classification but can hurt localization and fine textures.
- **Resolution is a top accuracy lever** - small objects need higher resolution or tiling/patching; don't downsample away the signal.
- **Detection data**: verify box format (xywh vs xyxy, normalized?), anchor/scale sizing, and NMS thresholds.
- **Leakage**: split by source/scene/identity, not by frame - consecutive frames or same-identity images must not cross splits (`data-rigor-and-leakage`).
- **Explainability**: Grad-CAM for classifiers; overlay predicted boxes/masks for detection/segmentation.
- **Improve accuracy**: use `accuracy-improvement-loop`. For tiny objects in big images, consider tiling or weakly-supervised localization.
