---
name: total-segmentator
description: "Tool for robust segmentation of 104+ anatomical structures in CT images. Uses nnUNet-based models for whole-body, organ, and bone segmentation. One-line CLI for comprehensive body-part segmentation."
tags: [medical-image-segmentation, ct-anatomy-segmentation, whole-body-ct, nnunet-inference, total-segmentator]
---
## Overview

TotalSegmentator segments 104+ anatomical structures in CT images using nnUNet-based models. Run full-body, organ, or bone segmentation with a single CLI command.

## Installation

```bash
uv pip install TotalSegmentator
```

## CLI Usage

```bash
# Full body segmentation (all 104 structures)
TotalSegmentator -i input_ct.nii.gz -o output_seg.nii.gz

# Organ-only segmentation (liver, kidneys, spleen, etc.)
TotalSegmentator -i input_ct.nii.gz -o organ_seg.nii.gz -ta organ

# Appendicular bones
TotalSegmentator -i input_ct.nii.gz -o bone_seg.nii.gz -ta appendicular_bones
```

## Python API

```python
from totalsegmentator.python_api import totalsegmentator

segmentation = totalsegmentator("input_ct.nii.gz", "output_seg.nii.gz")
```

## Workflow

1. Obtain CT scan in NIfTI format
2. Run `TotalSegmentator -i input.nii.gz -o output.nii.gz`
3. Task types: `total` (104 structures), `organ`, `vertebra`, `ribs`, `appendicular_bones`
4. Output is a multi-label segmentation mask
5. Extract volumes per label for quantitative analysis
