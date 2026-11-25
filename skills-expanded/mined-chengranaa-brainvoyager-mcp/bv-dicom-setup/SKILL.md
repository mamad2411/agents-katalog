---
name: bv-dicom-setup
description: >
  Rename, anonymize, and discover DICOM datasets for BrainVoyager fMRI preprocessing.
  Use when the user needs to organize raw DICOM directories, standardize file names,
  anonymize patient data, or auto-discover functional and anatomical series to build
  project dictionaries for batch processing. Triggers on mentions of "DICOM setup,"
  "rename DICOMs," "anonymize DICOMs," "scan DICOM directory," or "organize raw data."
---

## Overview

Organize raw DICOM directories into BrainVoyager's naming convention, anonymize
patient identifiers, and auto-discover functional/anatomical series. Output is
cleanly renamed DICOMs plus project dictionaries (JSON) ready for downstream
FMR/VMR creation and batch processing.

## Workflow

```
Copy raw DICOMs → Rename → Anonymize → Discover series → Verify params
```

## Step 1: Copy and rename

- **Always work on a COPY** of the raw data — never modify originals.
- Use `rename_bv_dicoms(directory)` to rename files to the BV pattern:
  `PatientName-SeriesNumber-VolumeNumber-ImageNumber.dcm`
- For anonymization in one step: `anonymize_bv_dicoms(directory, anonymized_patient_name="Subj01")`
- **Gotcha**: When the anonymized name is shorter than the original, BV pads
  filenames with spaces. Always run a whitespace cleanup after anonymization:
  ```bash
  for f in *.dcm; do mv "$f" "$(echo $f | tr -s ' ' | sed 's/ -/-/g')"; done
  ```

## Step 2: Discover series

- **ALWAYS present a FULL inventory to the user before any processing.**
  DICOM series can be messy — runs unnamed, descriptions misleading, SE pairs
  shared or per-run, and unexpected acquisitions hiding under generic names.
- Use `exec_bv_python` with `pydicom` to parse headers. Key tags:

  | Tag | Field | Purpose |
  |-----|-------|---------|
  | (0010,0010) | PatientName | Subject ID |
  | (0020,0011) | SeriesNumber | Group volumes into series |
  | (0008,103E) | SeriesDescription | Run label ("Run_01", "T1_Images") |
  | (0008,0008) | ImageType | `M`=magnitude, `P`=phase (skip phase) |
  | (0019,100A) | NrOfSlices | Siemens slice count |
  | (0018,0080) | TR | Repetition time (ms) |
  | (0018,0081) | TE | Echo time (ms) |
  | (0018,1312) | InPlanePhaseEncodingDirection | `COL` or `ROW` for AP/PA ID |
  | (0018,0086) | EchoNumber | Multi-echo: each echo is a separate entry |

- **BV classifier labels**: `DWI/FUNC` = short reverse-PE acquisitions (for
  topup), `FUNC/DWI` = main functional runs. Use these as hints but always
  confirm manually with the `InPlanePhaseEncodingDirection` tag.
- **Phase images** (`ImageType[2]='P'`): skip unless explicitly needed.
- **Multi-echo**: check `EchoNumber` — treat each echo as a separate series
  entry in project dictionaries.
- Save results as a JSON project dictionary for downstream pipelines.

## Step 3: Verify parameters

Before creating FMRs or VMRs, verify key acquisition parameters from the
first volume of each series: TR, TE, flip angle (0018,1314), voxel size
(0028,0030), slice thickness (0018,0050), and slice count. Flag any deviation
from the expected protocol — wrong TR breaks slice timing, mismatched slice
count means incomplete acquisition, etc.

## Step 4: Always ask the user

Present the full DICOM inventory and ask two things:

1. **Confirm series classification** — which are main runs, reverse-PE runs,
   anatomicals? Any series to skip?
2. **What analysis are you planning?** (standard GLM, layer-dependent,
   retinotopy/pRF, resting-state) — this determines noise-volume handling,
   resolution choices, and whether distortion correction is needed.

## Gotchas

- **BV changes working directory** — always `os.chdir()` to your data directory
  before any DICOM operation.
- **Large directories** — never `os.listdir()`; use `glob` patterns and
  `len(glob(...))` to count files.
- **Mosaic vs single-image** — Siemens mosaics use different dimension tags
  than single-slice DICOMs. The `create_fmr_from_bv_dicom` tool handles this
  automatically.
- **Anonymization whitespace** — shorter anonymized names produce space-padded
  filenames. Always run the cleanup one-liner from Step 1.
- **Phase images** — `ImageType[2]='P'` are coil phase data, not anatomical or
  functional magnitude. Skip them.
- **Multi-echo** — same `SeriesDescription`, different `EchoNumber`. Each echo
  gets its own project dict entry (e.g., `echo1`, `echo2`).
