---
name: monai
description: "Medical Open Network for AI (MONAI). Framework for deep learning in medical imaging: segmentation, classification, detection, registration. Supports DICOM, NIfTI, PNG. Built on PyTorch with GPU acceleration."
tags: [medical-imaging, deep-learning, pytorch, segmentation, radiology, dicom, zorai]
---
## Overview

MONAI is the standard PyTorch-based framework for medical imaging deep learning. Use it for segmentation, classification, registration, preprocessing, and training pipelines on DICOM, NIfTI, and other medical image formats.

## Installation

```bash
uv pip install monai
# optional extras as needed
uv pip install monai[all]
```

## Core strengths

MONAI gives you:
- medical-image-aware transforms
- domain-specific architectures like UNet, UNETR, SwinUNETR
- losses like DiceLoss and DiceCELoss
- metrics like Dice and Hausdorff distance
- dataset and engine utilities for training loops

## Basic 3D segmentation model

```python
import torch
from monai.networks.nets import UNet
from monai.networks.layers import Norm

model = UNet(
    spatial_dims=3,
    in_channels=1,
    out_channels=3,
    channels=(16, 32, 64, 128, 256),
    strides=(2, 2, 2, 2),
    num_res_units=2,
    norm=Norm.BATCH,
).cuda()
```

## Preprocessing transforms

```python
from monai.transforms import (
    Compose, LoadImaged, EnsureChannelFirstd, Spacingd,
    Orientationd, ScaleIntensityRanged, CropForegroundd,
    RandCropByPosNegLabeld, RandFlipd, EnsureTyped,
)

train_transforms = Compose([
    LoadImaged(keys=['image', 'label']),
    EnsureChannelFirstd(keys=['image', 'label']),
    Orientationd(keys=['image', 'label'], axcodes='RAS'),
    Spacingd(keys=['image', 'label'], pixdim=(1.5, 1.5, 2.0), mode=('bilinear', 'nearest')),
    ScaleIntensityRanged(keys=['image'], a_min=-200, a_max=300, b_min=0.0, b_max=1.0, clip=True),
    CropForegroundd(keys=['image', 'label'], source_key='image'),
    RandCropByPosNegLabeld(keys=['image', 'label'], label_key='label', spatial_size=(96, 96, 96), num_samples=4),
    RandFlipd(keys=['image', 'label'], prob=0.5, spatial_axis=0),
    EnsureTyped(keys=['image', 'label']),
])
```

## Loss + metric

```python
from monai.losses import DiceCELoss
from monai.metrics import DiceMetric

loss_fn = DiceCELoss(to_onehot_y=True, softmax=True)
dice_metric = DiceMetric(include_background=False, reduction='mean')
```

## Workflow

1. Normalize image orientation and spacing first.
2. Use label-safe transform modes: bilinear for images, nearest for labels.
3. Start with MONAI reference architectures before inventing custom ones.
4. Verify voxel spacing assumptions before training.
5. Track Dice per class, not just aggregate loss.
6. Save preprocessing config with the model so inference matches training.
