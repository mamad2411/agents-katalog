---
name: simpleitk
description: "Simplified interface to the Insight Toolkit (ITK) for medical image processing. Segmentation, registration, filtering, resampling, morphological operations. Supports DICOM, NIfTI, NRRD, dozens of formats."
tags: [medical-image-processing, registration, dicom-workflows, itk-wrappers, simpleitk]
---
## Overview

SimpleITK simplifies the Insight Toolkit (ITK) for medical image processing: segmentation, registration, filtering, resampling, and morphological operations. Supports DICOM, NIfTI, NRRD, and 50+ file formats.

## Installation

```bash
uv pip install SimpleITK
```

## Basic Image Operations

```python
import SimpleITK as sitk
import numpy as np

image = sitk.ReadImage("ct_scan.nii.gz")
print(image.GetSize(), image.GetSpacing(), image.GetOrigin())

array = sitk.GetArrayFromImage(image)
print(array.shape)  # (z, y, x)
```

## Segmentation

```python
binary = sitk.BinaryThreshold(image, lower=200, upper=500, insideValue=1, outsideValue=0)
cc = sitk.ConnectedComponent(binary)
stats = sitk.LabelIntensityStatisticsImageFilter()
stats.Execute(cc, image)

for label in stats.GetLabels():
    print(f"Label {label}: mean={stats.GetMean(label):.1f}")
```

## Registration

```python
fixed = sitk.ReadImage("template.nii.gz")
moving = sitk.ReadImage("moving.nii.gz")

R = sitk.ImageRegistrationMethod()
R.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
R.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
R.SetInitialTransform(sitk.CenteredTransformInitializer(fixed, moving, sitk.Euler3DTransform()))
final_transform = R.Execute(fixed, moving)
resampled = sitk.Resample(moving, fixed, final_transform, sitk.sitkLinear)
```

## Workflow

1. Read images with `sitk.ReadImage()` (auto-detects format)
2. Preprocess: `BinaryThreshold`, `MedianFilter`, `ResampleImageFilter`
3. Segment with thresholding, watershed, or connected components
4. Register with `ImageRegistrationMethod` + transform
5. Measure volumes with `LabelStatisticsImageFilter`
6. Write results with `sitk.WriteImage()`
