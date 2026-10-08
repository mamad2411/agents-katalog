---
name: domain-medical-imaging
description: "Use for medical-image AI: tumor/cancer detection & classification, brain tumor MRI, mammography (benign vs malignant), chest X-ray, CT, histopathology, retinal/fundus, ultrasound, dermoscopy. Encodes hard-won rigor: patient-level splits (no leakage), medical preprocessing (CLAHE, ROI/organ cropping, artifact/pectoral removal), clinical operating points (high sensitivity), probability calibration, and skepticism toward inflated ROI-crop/leaky benchmark numbers. Triggers on 'detect cancer/tumor', 'MRI/CT/X-ray/mammogram/histopathology classification', 'benign vs malignant', 'medical images'."
---

# Medical Imaging - Method Selection & Rigor

High stakes + small, leaky-prone datasets. Rigor matters more than architecture.

## Decision table
| Sub-task | Recommended | Notes |
|---|---|---|
| 2D scan classification (mammo, X-ray, derm, fundus) | **EfficientNet(-B3..B5) / ConvNeXt**, ImageNet-pretrained | Modern-but-not-huge backbones win on low/medium-quality medical data; giant models often don't transfer better. |
| Whole-image with tiny lesions | **Weakly-supervised localization (GMIC-style)** or **patch-pretrain then whole-image (Shen-style)** | Best whole-image ceiling; also yields saliency maps for clinicians. |
| Multi-view study (e.g., CC+MLO mammo) | **Two-view / multi-input fusion** | Biggest research-backed lever over single view. |
| 3D volumes (CT/MRI) | **3D U-Net / nnU-Net (seg)**, 2.5D or 3D CNN (classify) | nnU-Net is a very strong segmentation default. |
| Histopathology WSI | **MIL / CLAM on tiles** | Gigapixel images, so tile them and use multiple-instance learning. |
| Lesion/organ segmentation | **U-Net / nnU-Net / SegFormer** | Dice/IoU. |

## Non-negotiable rigor (this is where most medical ML fails)
- **PATIENT-LEVEL split.** All images/views/slices of one patient in ONE split. Use the dataset's **official split** when it exists (often encoded in the ID). Add asserts (`data-rigor-and-leakage`). Random per-image splitting is the classic fake-accuracy trap.
- **Whole-image vs ROI-crop honesty.** Cropped-lesion ROI classification is an easier, different problem; ~98-99% papers are usually ROI-crop and/or leaky. Report which one you are doing and never conflate.
- **Medical preprocessing:** CLAHE for contrast; crop to the organ/breast (largest connected component) to drop background/labels/tape; remove confounders (e.g., pectoral muscle on mammogram MLO - verify the model isn't attending to it via Grad-CAM); intensity normalization (windowing for CT, z-score for MRI). Apply identically at inference (parity).
- **Clinical operating point:** report **sensitivity AND specificity**; prefer a **high-sensitivity** threshold (recall ≥ ~0.90) chosen on validation - missing cancer >> a false alarm. Don't ship a 0.5 or Youden threshold blindly.
- **Calibration:** temperature-scale probabilities so "78% malignant" is trustworthy for decision support.
- **Framing:** decision-support / second-reader, NOT autonomous diagnosis; prototype needs clinical + regulatory validation (`deployment-explainability`).

## Realistic ceilings (whole-image, rigorous)
State honest targets from `literature-review` rather than chasing leaderboard peaks (e.g., CBIS-DDSM whole-image benign-vs-malignant ≈ 0.83 AUC single-view, ~0.86 two-view; higher numbers are typically ROI/leaky). Use `accuracy-improvement-loop` to push toward the ceiling.
