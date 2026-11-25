---
name: nibabel
description: "Read and write neuroimaging file formats: NIfTI, GIFTI, CIFTI, MGH, Minc, Analyze, SPM. Core I/O for fMRI, diffusion MRI, structural MRI pipelines. Use when handling brain imaging data."
tags: [neuroimaging, nifti, fmri, mri, medical-imaging, python, zorai]
---
## Overview

NiBabel is the core Python library for neuroimaging file I/O. Use it to read and write NIfTI, GIFTI, CIFTI, MGH, MINC, and Analyze files, inspect affine metadata, and move data between imaging tools and NumPy.

## Installation

```bash
uv pip install nibabel
```

## Load a NIfTI volume

```python
import nibabel as nib

img = nib.load('brain_t1.nii.gz')
data = img.get_fdata()
affine = img.affine
header = img.header

print(data.shape)
print(header.get_zooms())
print(affine)
```

## Save a modified image

```python
import numpy as np

masked = (data > data.mean()).astype(np.float32)
out = nib.Nifti1Image(masked, affine, header)
nib.save(out, 'brain_mask.nii.gz')
```

## 4D fMRI example

```python
fmri = nib.load('rest_bold.nii.gz')
arr = fmri.get_fdata()   # shape like (x, y, z, t)
tr = fmri.header.get_zooms()[-1]
print(arr.shape, tr)
```

## Coordinate handling

NiBabel stores the affine transform from voxel coordinates to world coordinates. Do not ignore it if you are mixing tools, resampling data, or comparing scans across sessions.

## Workflow

1. Load with `nib.load()`.
2. Inspect shape, affine, voxel spacing, and orientation assumptions.
3. Use `.get_fdata()` when you want floating-point arrays.
4. When saving derived outputs, preserve affine/header unless intentionally changing them.
5. For resampling/reorientation, combine with Nilearn, DIPY, or ANTs/SimpleITK workflows rather than hacking the array blindly.
