---
name: nnunet
description: "No New U-Net — self-configuring framework for medical image segmentation. Automatically adapts to any dataset. Top performer on biomedical segmentation benchmarks (BraTS, KiTS, etc.)."
tags: [medical-imaging, segmentation, unet, deep-learning, pytorch, zorai]
---
## Overview

nnUNet (No New U-Net) is a self-configuring framework for medical image segmentation that automatically adapts to any dataset. Consistently top-performing on benchmarks like BraTS, KiTS, and AMOS.

## Installation

```bash
uv pip install nnunetv2
```

## Plan and Preprocess

```bash
nnUNetv2_plan_and_preprocess -d DATASET_ID -pl nnUNetPlanner
```

## Train

```bash
nnUNetv2_train DATASET_ID CONFIG 0  # CONFIG: 2d, 3d_fullres, 3d_lowres
```

## Inference

```bash
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG
```

## Python API

```python
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor

predictor = nnUNetPredictor()
predictor.initialize_from_trained_model_folder("nnUNet_results/DatasetXYZ", "3d_fullres")
predictor.predict_from_files("input_images", "output_segmentations")
```

## Workflow

1. Prepare dataset in nnUNet format (imagesTr, labelsTr, dataset.json)
2. Run `nnUNetv2_plan_and_preprocess` for automatic configuration
3. Train with `nnUNetv2_train`
4. Predict with `nnUNetv2_predict` or Python API
5. Ensemble multiple configurations for best accuracy
