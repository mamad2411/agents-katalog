---
name: bv-fmri-preprocessing
description: >
  Full fMRI preprocessing in BrainVoyager: FMR creation from DICOM, slice timing
  correction, 3D motion correction, temporal high-pass filtering (GLM Fourier/DCT),
  spatial smoothing, and EPI distortion correction (FSL topup with AP/PA blip-up/down
  acquisitions). Use when the user needs to preprocess fMRI data, create FMR, correct
  slice timing, motion correct, high-pass filter, spatially smooth, or correct EPI
  distortions. Assumes DICOMs are already renamed.
---

## Overview
Takes renamed functional DICOMs and produces fully preprocessed FMR files ready for coregistration. Covers FMR creation, the standard preprocessing chain, and optional EPI distortion correction.

## Core Pipeline
```
Renamed DICOM → [1] FMR Creation → [2] Slice Timing → [3] Motion Correction → [4] High-Pass Filter → [5] Spatial Smooth
                                                                    ↑
                              [Distortion Correction — after MC, before HPF]
```

## Prerequisites
- DICOMs renamed to BV format (bv-dicom-setup skill)
- For distortion correction: FSL installed (topup, applytopup, fslmerge), AP/PA acquisitions
- Python: bvbabel + nibabel + numpy for NIfTI conversion

## Step 1: FMR Creation

Preferred: `create_fmr_from_bv_dicom(file_of_series, fmr_stc_filename, target_folder)` — auto-detects mosaic/single-image/enhanced DICOM. Only one DICOM file needed.

For old mosaic DICOMs where auto-detect fails: use `bv.create_mosaic_fmr()` inside `exec_bv_python`.

Naming: `{subject}_{task}_{run}_{signal}` e.g. `Pilot_LetterImagery_run01_M`

Multi-band/SMS: auto-detected from DICOM. No special params needed.

AMR: BV auto-creates an AMR from the first volume (useful for coregistration).

ALWAYS ask: noise volumes to skip? NV at start can be skipped during creation. NV at end: create full FMR, note usable range.

## Step 2: Slice Timing Correction

MUST be first preprocessing step. `fmr_correct_slice_timing(interpolation_method=3)`.

Uses DICOM timing table — handles single-band and multi-band correctly. Interpolation: 1=trilinear, 2=cubic, 3=sinc. Output suffix: `_SCSTBL`.

## Step 3: Motion Correction

3D rigid-body (6 params). `fmr_correct_motion(timeout_seconds=300)` aligns all volumes to volume 1.

Framewise Displacement: BV logs motion params to .log file. FD = sum of abs(Δtranslation) + abs(Δrotation × 50mm). FD > 0.5mm flags a volume for scrutiny.

Across-run MC: For multi-run GLM, align all runs to first volume of first run with `fmr_correct_motion_to_vol(target_vol_idx=0)`. BV replaces linked AMR with `_CoregFirstVol.amr`. FMR-VMR coregistration then only needed once.

Output suffix: `_3DMCTS`.

## Step 4: Temporal High-Pass Filtering

Removes scanner drift. Two methods:
- GLM Fourier: `fmr_filter_highpass_glm_fourier(n_cycles=2-3)` — sine/cosine pairs
- GLM DCT: `fmr_filter_highpass_glm_dct(n_basis_functions=2)`
- Cutoff ≈ n_cycles / (n_volumes × TR). 3 cycles on 600s run ≈ 0.005 Hz ≈ 200s.
- For resting-state: use VTC-level FFT instead (`vtc_filter_highpass_fft(0.008, "Hz")`)

Output suffix: `_THPGLMF` (Fourier) or `_THPGLMD` (DCT).

## Step 5: Spatial Smoothing

3D Gaussian. `fmr_smooth_spatial(gauss_fwhm=4.0, fwhm_unit="mm")`.
- 2-3mm: high-res / laminar
- 4mm: standard 2-3mm voxel fMRI
- 6-8mm: low SNR, group-level

Smoothing at VTC level often preferable (avoids interpolating already-smoothed data through transforms).

Output suffix: `_SD3DSS`.

## EPI Distortion Correction (optional, FSL topup)

Place AFTER motion correction, BEFORE high-pass filter.

Steps:
1. Convert AP/PA + all runs to NIfTI (use BV's doc.save_as for mosaic FMRs, bvbabel otherwise)
2. `fslmerge -t APPA.nii.gz AP.nii.gz PA.nii.gz`
3. Create acqparams.txt: 4th column = total readout time = (PE_lines - 1) × echo_spacing / MB_factor. Typical: 0.02-0.05s.
4. Create b02b0.cnf config (standard FSL config)
5. `topup --imain=APPA.nii.gz --datain=acqparams.txt --config=b02b0.cnf --out=APPA_topup`
6. `applytopup -i run.nii.gz -a acqparams.txt -t APPA_topup -x 1 -m jac -o run_topup`
7. Convert corrected NIfTI back to FMR: NIfTI [X,Y,Z,T] → STC [T,Z,Y,X], clone FMR header with updated prefix
8. Continue with HPF on corrected FMRs

Alternative: BV has built-in EPI distortion correction (GUI only, no MCP tool yet).

## Gotchas
- Order matters: slice timing before MC, MC before HPF, HPF before smoothing
- Close documents between steps
- Filename chain: _SCSTBL → _3DMCTS → _THPGLMF → _SD3DSS. Don't rename intermediates.
- Long ops (FMR creation, MC): may time out but complete in background. NEVER retry without verifying on disk.
- Mosaic FMRs have DimX=DimY=DimZ=0 → bvbabel fails. Use BV's NIfTI export.
- Reverse-PE scans: preprocess same way as main runs, skip HPF, don't trim noise volumes
- STC and FMR must stay together in same directory
