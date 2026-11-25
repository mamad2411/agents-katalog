---
name: bv-anatomical-pipeline
description: >
  Full BrainVoyager anatomical preprocessing pipeline: VMR creation from DICOM,
  MP2RAGE denoising (UNI/INV1/INV2 to uniden), intensity inhomogeneity correction
  (IIHC) with brain extraction, isovoxel resampling, MNI normalization, Talairach
  transformation, and defacing. Use when the user needs to process anatomical data,
  create VMR, denoise MP2RAGE, correct bias field, normalize to MNI, AC-PC transform,
  or prepare anatomy for coregistration.
---

## Overview
Processes raw anatomical DICOM into a normalized, analysis-ready VMR. Minimum steps: VMR creation → IIHC → isovoxel → MNI. MP2RAGE denoising and Talairach/defacing are optional.

## Workflow
```
Anatomical DICOM → VMR → [MP2RAGE denoise] → IIHC → Isovoxel → [Sagittal] → MNI → [Talairach] → [Deface]
```

## Prerequisites
- DICOMs renamed (bv-dicom-setup skill)
- For MP2RAGE: UNI, INV1, INV2 must be V16 files, NOT VMR (VMR = uint8, V16 = uint16 needed for math)
- V16 auto-created when VMR is opened in BV

## Step 1: Create VMR
- `create_vmr_from_bv_dicom(file_of_series=first_dicom)` — auto-detects all params
- Save with descriptive name: `Subj01_UNI.vmr`

## Step 2: MP2RAGE denoising (optional)
- `run_mp2rage_denoise(chosen_factor=10.0, path_uni/INV1/INV2)` 
- Removes salt-and-pepper background noise from UNI image
- chosen_factor: 5-10 conservative, 10-20 aggressive, 10 default
- Must pass .v16 paths, not .vmr

## Step 3: IIHC (intensity inhomogeneity correction)
- `correct_bv_vmr_intensity_inhomogeneities()` — standard: 3 cycles, includes brain extraction
- For 7T or severe inhomogeneity: `correct_bv_vmr_intensity_inhomogeneities_ext(n_cycles=6-8)`
- Algorithm: fits smooth polynomial bias field, iteratively refines, brain extraction via region-growing from WM
- After IIHC: WM ~150, GM ~100, CSF ~60 in uint8 VMR
- Output: `*_IIHC.vmr`

## Step 4: Isovoxel resampling
- ALWAYS ask user for target resolution
- Layer-dependent fMRI: keep native sub-mm (manual AC-PC needed, auto tools require ≥1mm)
- Standard: `transform_bv_vmr_to_std_isovoxel(interpolation_method=3)` — 1mm iso, 256³
- Custom: `transform_bv_vmr_to_isovoxel(target_res=0.8, framing_cube_dim=320)`
- Interpolation: 1=trilinear, 2=cubic, 3=sinc (best)

## Step 5: Reorient to sagittal (optional)
- `transform_bv_vmr_to_std_sag()` — to radiological convention
- Skip if already acquired in sagittal (most modern 3D MPRAGE/MP2RAGE)

## Step 6: MNI normalization
- `normalize_bv_vmr_to_mni_space()` — affine + nonlinear warp to MNI-152
- Requires IIHC-completed VMR (uses brain mask from IIHC)
- Requires isovoxel ≥ 1mm
- Output: `*_MNI.vmr` + `*_MNI.trf`

## Step 7: AC-PC and Talairach (optional)
- `auto_acpc_tal_bv_vmr_transformation()`
- Detects mid-sagittal plane, AC/PC points, cerebral borders
- Talairach: 12 sub-volumes each with independent scaling (unlike MNI's single nonlinear warp)
- Outputs: `*_ACPC.vmr/.trf`, `*_TAL.vmr/.tal`

## Step 8: Deface (optional)
- `deface_bv_vmr()` — requires 1mm isovoxel
- Alternative at DICOM level: `deface_bv_anatomical_dicoms()`

## Gotchas
- IIHC needs V16 alongside VMR
- MNI normalization fails with poor brain extraction → re-run IIHC
- Sub-mm voxels → manual AC-PC required before auto normalization
- Disk space: full pipeline ~200MB per subject. Clean intermediates.
