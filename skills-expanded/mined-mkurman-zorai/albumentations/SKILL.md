---
name: albumentations
description: "Fast image augmentation library (Albumentations). 70+ transforms for classification, segmentation, object detection, keypoints, and pose estimation. Optimized OpenCV-based pipeline with unified API across all CV tasks. Supports images, masks, bounding boxes, and keypoints simultaneously. Note: classic Albumentations (MIT) is no longer maintained; successor AlbumentationsX uses AGPL-3.0. For torchvision-native augmentations, use torchvision.transforms.v2."
license: MIT license
tags: [image-augmentation, object-detection, semantic-segmentation, keypoint-augmentation, albumentations]
metadata:
    skill-author: K-Dense Inc.
-------|---------------|----------|
| **Pixel-level** | BrightnessContrast, Gamma, HueSaturationValue, CLAHE, Blur, GaussNoise, ISONoise, RGBShift, ChannelShuffle, ToGray, Solarize, Posterize, Equalize, ColorJitter | Color/lighting variation |
| **Spatial-level** | RandomCrop, CenterCrop, Resize, Rotate, Flip, ShiftScaleRotate, Affine, ElasticTransform, GridDistortion, OpticalDistortion, Perspective, PiecewiseAffine | Geometric variation |
| **Weather** | RandomRain, RandomSnow, RandomFog, RandomSunFlare | Adverse conditions |
| **Advanced** | CoarseDropout, Cutout, MixUp, Mosaic | Regularization, domain gap |
| **Special** | CLAHE, Emboss, Sharpen, Superpixels, FDA, HistogramMatching, PixelDistributionAdaptation | Medical, domain adaptation |

### 5. Probability and OneOf Composition

```python
# OneOf: apply exactly one transform from a list
transform = A.Compose([
    A.OneOf([
        A.RandomBrightnessContrast(p=1.0),
        A.RandomGamma(p=1.0),
        A.HueSaturationValue(p=1.0),
    ], p=0.8),
    A.HorizontalFlip(p=0.5),
])

# SomeOf: apply up to N transforms from a list
transform = A.Compose([
    A.SomeOf([
        A.GaussNoise(p=1.0),
        A.ISONoise(p=1.0),
        A.MultiplicativeNoise(p=1.0),
    ], n=2, replace=False, p=0.5),
])

# Per-transform probability
transform = A.Compose([
    A.RandomCrop(256, 256, p=1.0),       # Always applied
    A.HorizontalFlip(p=0.5),             # 50% chance
    A.RandomBrightnessContrast(p=0.2),    # 20% chance
])
```

### 6. Bounding Box Formats

```python
# Supported formats:
# pascal_voc: [x_min, y_min, x_max, y_max] (pixels)
# albumentations: normalized [x_center, y_center, width, height]
# coco: [x_min, y_min, width, height] (pixels)
# yolo: normalized [x_center, y_center, width, height]

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
], bbox_params=A.BboxParams(
    format="coco",
    min_visibility=0.3,      # Drop bboxes <30% visible after transform
    label_fields=["class_labels", "class_ids"],  # Extra fields to transform
))
```

### 7. Replay Mode (Reproducible Augmentations)

Apply identical augmentation parameters to multiple images:
```python
transform = A.Compose([
    A.RandomCrop(256, 256),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
])

# Apply to first image, get replay params
data = transform(image=image1, mask=mask1)
replay_params = data["replay"]

# Reapply IDENTICAL transforms to second image
data2 = A.ReplayCompose.replay(replay_params, image=image2, mask=mask2)
```

### 8. Serialization (Save/Load Pipelines)

```python
import albumentations as A

transform = A.Compose([
    A.RandomCrop(256, 256),
    A.HorizontalFlip(p=0.5),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Save to YAML/JSON
A.save(transform, "augmentation_pipeline.yaml")
A.save(transform, "augmentation_pipeline.json")

# Load back
loaded = A.load("augmentation_pipeline.yaml")
```

### 9. PyTorch Integration

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

train_transform = A.Compose([
    A.RandomResizedCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, p=0.5),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),  # Convert HWC numpy → CHW tensor
])

val_transform = A.Compose([
    A.Resize(256, 256),
    A.CenterCrop(224, 224),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

# In PyTorch Dataset:
class MyDataset(Dataset):
    def __getitem__(self, idx):
        image = cv2.imread(self.images[idx])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented["image"]

        return image, self.labels[idx]
```

### 10. Advanced Transforms

**MixUp (alpha blending two images):**
```python
transform = A.Compose([
    A.MixUp(reference_data=reference_dataset, alpha=0.4, p=0.5),
    A.HorizontalFlip(p=0.5),
])
```

**CoarseDropout (Cutout regularization):**
```python
transform = A.Compose([
    A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=0.5),
])
```

**FDA (Fourier Domain Adaptation):**
```python
# Swap low-frequency components between source and target domain images
transform = A.Compose([
    A.FDA(reference_images=target_domain_images, beta_limit=0.1, p=0.5),
])
```

## Key Patterns

1. **Always convert BGR to RGB** when using OpenCV — Albumentations works in RGB
2. **Use `A.Compose` with probabilities** to control augmentation strength
3. **Use `OneOf`** for mutually exclusive transforms (e.g., pick one blur method)
4. **Normalize at the END** of the pipeline — after all other transforms
5. **Use `ToTensorV2()`** for seamless PyTorch conversion
6. **Replay mode** for consistent augmentations across image pairs (stereo, temporal)
7. **Save/Load pipelines** for reproducibility across training runs
8. **Albumentations is MIT-licensed but unmaintained** — consider AlbumentationsX for active projects

## References

- [Albumentations Documentation](https://albumentations.ai/docs/)
- [Transform Gallery](https://explore.albumentations.ai/) — interactive demo
- [Benchmark Results](https://albumentations.ai/docs/benchmarks/image-benchmarks/)
- [Examples Gallery](https://albumentations.ai/docs/examples/)
- [AlbumentationsX (successor)](https://github.com/albumentations-team/AlbumentationsX)
