---
name: bv-coregistration-vtc
description: >
  Coregister preprocessed FMR data to anatomical VMR and create VTC files in native,
  MNI, or Talairach space. Covers BBR (boundary-based registration) and intensity-based
  coregistration, VTC creation with full parameter control, VTC-level filtering/smoothing,
  and linking VTCs to MDM group design matrices. Use when the user needs to coregister
  functional to anatomical, create VTC, transform to MNI, transform to Talairach, link
  VTC, or set up group analysis. Assumes anatomical VMR is preprocessed (IIHC + isovoxel)
  and FMR is preprocessed (slice timing + motion correction).
---

## Overview
Aligns preprocessed functional data to anatomy (coregistration), then transforms the 4D time series into a 3D reference space (VTC creation) in native, MNI, or Talairach space.

## Workflow
```
Preprocessed FMR + IIHC VMR → IA → FA → VTC (native/MNI/Tal) → Link → Post-process
```

## Prerequisites
- FMR: minimum slice-timing + motion-corrected. HPF and smoothing optional (can do at VTC level).
- VMR: IIHC-corrected (preferred — better brain extraction → better BBR). Must be isovoxel.
- For MNI VTC: `*_MNI.trf` from anatomical pipeline. For Tal VTC: `*_ACPC.trf` + `*_TAL.tal`.

## Step 1: Coregistration

Two methods. BBR is preferred.

### BBR (recommended)
`vtc_coregister_fmr_to_vmr_bbr(fmr_file, timeout_seconds=300)` — VMR must be open.
- How it works: auto-segments VMR to find WM/GM boundary → creates mesh (.srf) → aligns EPI by maximizing intensity gradient at the boundary
- "Invert intensities" is ON by default (T2* EPI → appears T1-like for gradient alignment)
- Segmentation is automatic, different from full cortex segmentation pipeline
- First run slow (mesh creation), subsequent runs reuse mesh
- Produces: `FMRname-TO-VMRname_IA.trf` and `FMRname-TO-VMRname_FA.trf`

### Intensity-based (fallback)
`vtc_coregister_fmr_to_vmr(fmr_file, iihc_func=False, timeout_seconds=300)`
- IA (Initial Alignment): mathematically exact for same-session DICOM using scanner geometry headers
- FA (Fine-Tuning): iterative gradient-driven (trilinear → sinc)
- Optimal source: UNpreprocessed FMR (T1-saturated first volume gives best contrast via linked AMR)
- For multi-run across-run MC data: use preprocessed FMR (BV replaces AMR with `_CoregFirstVol.amr`)
- `iihc_func=True`: apply IIHC to first functional volume (7T or severe bias field)

Multiple runs: coregister each individually. VMR must stay open.

## Step 2: Create VTC

### Native space
`vtc_create_in_native_space(fmr_file, ia_trf, fa_trf, vtc_file, res_to_anat, interpolation, bbox_threshold, data_type)`

### MNI space
`vtc_create_in_mni_space(fmr_file, ia_trf, fa_trf, mni_trf_file, vtc_file, ...)` — requires `*_MNI.trf`

### Talairach space
`vtc_create_in_tal_space(fmr_file, ia_trf, fa_trf, acpc_trf_file, tal_file, vtc_file, ...)` — requires `*_ACPC.trf` + `*_TAL.tal`

### Parameter guide

| Parameter | Options | Recommendation |
|-----------|---------|----------------|
| res_to_anat | 1=same, 2=double, 3=triple | 2 for standard fMRI, 1 for high-res |
| interpolation | 1=trilinear, 2=cubic, 3=sinc | 2 (standard), 3 (publication) |
| bbox_threshold | 50-150 | 100 default (WM~150, GM~100, CSF~60) |
| data_type | 1=uint8, 2=uint16, 3=float32 | 2 (standard fMRI), 3 (exact float values) |

## Step 3: VTC Post-processing
- Link: `vtc_link(vtc_file)` — view in BV
- HPF: `vtc_filter_highpass_fft(highpass=0.008, highpass_unit="Hz")` — preferred for resting-state
- Smooth: `vtc_smooth_spatial(gauss_fwhm=4.0, fwhm_unit="mm")` — preferred over FMR-level smoothing

## Step 4: Group Analysis Setup
- MDM (Multi-Design Matrix): links multiple VTCs for group GLM
- `get_vtcs_of_mdm(mdm_file)` — query which VTCs are referenced

## Gotchas
- VMR must stay open during coregistration AND VTC creation
- BBR mesh reuse: delete old .srf if VMR changed
- TRF naming: `FMRname-TO-VMRname_IA.trf` (not just FMRname_IA.trf)
- Bounding box: too low = includes skull, too high = cuts brain
- Transform chain quality: coregister (trilinear OK) → VTC create (sinc) → smooth (Gaussian)
- Create VTC in native space first to inspect alignment before MNI/Tal
