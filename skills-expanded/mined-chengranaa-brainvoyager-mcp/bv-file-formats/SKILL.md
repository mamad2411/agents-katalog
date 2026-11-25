---
name: bv-file-formats
description: >
  Complete reference for all BrainVoyager file formats — binary structures, field
  specifications, axis conventions, and bvbabel read/write patterns. Covers VMR, V16,
  FMR/STC, VTC, TRF, PRT, SDM, MDM, GLM, VMP, SMP, SRF, MSK, MTC, GTC, POI, VOI, SSM,
  DMR/DWI. Use when the user needs to read/write BV files, understand file format fields,
  convert between formats, parse headers, debug file I/O, use bvbabel, or inspect binary
  data. Activate alongside pipeline skills whenever file-level operations are needed.
---

## Format Categories

| Category | Formats | Type | bvbabel |
|----------|---------|------|---------|
| Anatomical 3D | VMR, V16 | binary | vmr, v16 |
| Functional raw | FMR + STC | text + binary | fmr, stc |
| Functional 3D | VTC | binary | vtc |
| Diffusion | DMR, DWI, FBR | binary | dmr (read-only), dwi |
| Surface mesh | SRF | binary | srf |
| Surface data | MTC, GTC | binary | mtc, gtc |
| Statistical maps | VMP, GLM, SMP | binary | vmp, glm (wip), smp |
| Mask | MSK | binary | msk |
| Transform | TRF, TAL, LOG | text | trf |
| Design | PRT, SDM, MDM | text | prt, sdm, mdm |
| ROI | VOI, POI | binary/text | voi, poi |
| Sphere mapping | SSM | binary | ssm |

## Axis Convention

BV radiological: X=left→right, Y=posterior→anterior, Z=inferior→superior.
BV ↔ Talairach: BV X = Tal Y, BV Y = Tal Z, BV Z = Tal X.
BV LIP+ ↔ NIfTI RAS+: flip `[::-1, ::-1, ::-1]` then transpose `(0, 2, 1)`.

STC on disk: `[T, Z, Y, X]`, X varies fastest in C order.
NIfTI: `[X, Y, Z, T]` → transpose to `(3, 2, 1, 0)` for conversion.

## Per-Format Quick Reference

### VMR — 3D Anatomical (uint8)
- Pre-data header: 4 bytes DimX, 4 bytes DimY (both int32, big-endian)
- Data: DimZ × DimY × DimX bytes (uint8, 0-225)
- Post-data header: voxel resolution, coordinate origin, Talairach info, etc.
- bvbabel: `bvbabel.vmr.read_vmr(path)` → (header, data), `write_vmr(path, header, data)`

### V16 — 3D Anatomical (uint16)
- Header: 2 bytes DimX, 2 bytes DimY (uint16, little-endian), 2 reserved bytes
- Data: DimZ × DimY × DimX × 2 bytes (uint16, 0-4095)
- Needed for IIHC math, MP2RAGE denoising
- bvbabel: `bvbabel.v16.read_v16(path)` → (header, data), `write_v16(path, header, data)`

### FMR + STC — Functional (text header + binary data)
- FMR: text file with `key: value` pairs. Key fields: FileVersion, Prefix, DataType, NrOfVolumes, NrOfSlices, DimX/Y/Z, ResolutionX/Y, SliceThickness, TR, TE
- STC: raw binary, layout `[T, Z, Y, X]`, dtype from DataType (1=int16→2 bytes, 2=float32→4 bytes)
- bvbabel: `bvbabel.fmr.read_fmr(path)` → (header, data), `read_stc(stc_path, data_type, dims)` → data
- Mosaic FMRs have DimX=DimY=DimZ=0 → bvbabel conversion fails. Use BV's NIfTI export instead.
- FMR header has optional sub-sections for position info, transformation info, and multiband info.

### VTC — Volume Time Course (binary)
- Header: version, DimX/Y/Z, NrOfVolumes, resolution, TR, coordinate offsets, reference space flags
- Data: NrOfVolumes × DimZ × DimY × DimX × bytes (from DataType)
- bvbabel: `bvbabel.vtc.read_vtc(path)` → (header, data), `write_vtc(path, header, data)`

### TRF — Transformation (text, INI-style)
- `[SourceFile]`, `[TargetFile]` sections reference documents
- `[Transform]` section: `Row0=... Row1=... Row2=... Row3=...` = 4×4 affine matrix
- Naming: `FMRname-TO-VMRname_IA.trf` (IA), `FMRname-TO-VMRname_FA.trf` (FA)

### PRT — Protocol (text)
- Conditions with start/stop times (ms) or volumes. Header: NrOfConditions, ExperimentName.
- bvbabel: `bvbabel.prt.read_prt(path)` → (header, conditions)

### SDM — Design Matrix (text)
- Predictor time courses. Header: NrOfPredictors, NrOfDataPoints, IncludesConstant.
- bvbabel: `bvbabel.sdm.read_sdm(path)` → (header, data), `write_sdm(path, header, data)`

### MDM — Multi-Design Matrix (text/XML)
- Links VTCs for group GLM. Per-study: VTC path, SDM path, subject, transformation matrix.
- bvbabel: `bvbabel.mdm.read_mdm(path)` → (header, studies)

### VMP — Volumetric Map (binary)
- Multiple statistical maps in one file. Header: version, NrOfMaps, DimX/Y/Z.
- Per-map: map type (t/F/r), df1/df2, threshold min/max, cluster size.
- bvbabel: `bvbabel.vmp.read_vmp(path)` → (header, data), `write_vmp(path, header, data)`

### SMP — Surface Map (binary)
- Like VMP but on mesh vertices. Header: NrOfMaps, NrOfVertices, mesh filename.
- bvbabel: `bvbabel.smp.read_smp(path)` → (header, data), `write_smp(path, header, data)`

### GLM — Design Matrix + Results (binary)
- Header: version, NrOfPredictors, NrOfTimePoints, NrOfStudies, etc.
- Data arrays: design matrix, betas, residuals, contrasts (t/F).
- Formulas: t = beta / se, F = (R·beta)' · inv(R·C·R') · (R·beta) / rank(R)
- bvbabel: `bvbabel.glm` (work in progress)

### SRF — Surface Mesh (binary)
- Vertices (float32 × 3 coords), normals, triangles (int32 × 3 indices), neighbor lists.
- bvbabel: `bvbabel.srf.read_srf(path)` → (header, vertices, normals, triangles), write wip

### MSK — Mask (binary)
- Byte mask aligned to a VMR. bvbabel: `bvbabel.msk.read_msk(path)` → (header, data)

### MTC — Mesh Time Course (binary)
- Vertex time courses: NrOfVertices × NrOfTimePoints × float32. bvbabel mtc module.

### GTC — Grid Time Course (binary)
- Depth-grid time courses for laminar analysis. bvbabel gtc module.

### VOI — Volume of Interest (binary)
- Voxel coordinates + label. bvbabel: `bvbabel.voi.read_voi(path)` → (header, data)

### POI — Patch of Interest (text)
- Vertices on a mesh. bvbabel: `bvbabel.poi.read_poi(path)` → (header, patches)

### SSM — Sphere-to-Sphere Mapping (binary)
- Cortex-based alignment mappings. bvbabel ssm module.

## Cross-Reference: Which Pipeline Skills Produce Each Format

| Format | Produced by |
|--------|-------------|
| VMR, V16 | bv-anatomical-pipeline |
| FMR, STC | bv-fmr-creation, bv-fmri-preprocessing |
| VTC | bv-coregistration-vtc |
| TRF | bv-coregistration-vtc |
| PRT | user-created; bv-fmri-preprocessing uses for GLM |
| SDM | bv-fmri-preprocessing (GLM Fourier/DCT) |
| MDM | bv-coregistration-vtc (VTC linking) |
| VMP, SMP, GLM | GLM processing (post-VTC) |
| FMR (AP/PA) | bv-distortion-correction interop |

## Common bvbabel Patterns

```python
import bvbabel

# Read
header, data = bvbabel.vmr.read_vmr("anatomy.vmr")
header, data = bvbabel.v16.read_v16("anatomy.v16")
header, data = bvbabel.fmr.read_fmr("run.fmr")
header, data = bvbabel.vtc.read_vtc("run.vtc")
header, conditions = bvbabel.prt.read_prt("protocol.prt")
header, data = bvbabel.sdm.read_sdm("design.sdm")
header, studies = bvbabel.mdm.read_mdm("group.mdm")
header, data = bvbabel.vmp.read_vmp("stats.vmp")
header, data = bvbabel.smp.read_smp("stats.smp")
header, vertices, normals, triangles = bvbabel.srf.read_srf("mesh.srf")
header, data = bvbabel.msk.read_msk("mask.msk")
header, data = bvbabel.voi.read_voi("roi.voi")
header, patches = bvbabel.poi.read_poi("patches.poi")
header, data = bvbabel.trf.read_trf("coreg.trf")

# Write
bvbabel.vmr.write_vmr("out.vmr", header, data)
bvbabel.v16.write_v16("out.v16", header, data)
bvbabel.vtc.write_vtc("out.vtc", header, data)
bvbabel.sdm.write_sdm("out.sdm", header, data)
bvbabel.vmp.write_vmp("out.vmp", header, data)
bvbabel.smp.write_smp("out.smp", header, data)
```

### STC Read/Write (given FMR header)

```python
# Read STC from FMR header info
fmr_header, _ = bvbabel.fmr.read_fmr("run.fmr")
dims = [fmr_header["DimX"], fmr_header["DimY"],
        fmr_header["DimZ"], fmr_header["NrOfVolumes"]]
data = bvbabel.fmr.read_stc("run.stc", fmr_header["DataType"], dims)

# Write STC
bvbabel.fmr.write_stc("out.stc", data, data_type=2)  # 2=float32
```

### FMR → NIfTI (via STC)

```python
import nibabel as nib
import numpy as np

fmr_header, _ = bvbabel.fmr.read_fmr("run.fmr")
dims = [fmr_header["DimX"], fmr_header["DimY"],
        fmr_header["DimZ"], fmr_header["NrOfVolumes"]]
data = bvbabel.fmr.read_stc("run.stc", fmr_header["DataType"], dims)
# STC [T, Z, Y, X] → NIfTI [X, Y, Z, T]
data_nii = np.transpose(data, (3, 2, 1, 0))
affine = np.diag([fmr_header["ResolutionX"], fmr_header["ResolutionY"],
                   fmr_header["SliceThickness"], 1])
nii = nib.Nifti1Image(data_nii, affine)
nib.save(nii, "run.nii.gz")
```

### NIfTI → STC

```python
nii = nib.load("run.nii.gz")
data_nii = nii.get_fdata()  # [X, Y, Z, T]
data_stc = np.transpose(data_nii, (3, 2, 1, 0)).astype(np.float32)
bvbabel.fmr.write_stc("out.stc", data_stc, data_type=2)
```

### VMR ↔ V16 Conversion

```python
# VMR → V16
vmr_header, vmr_data = bvbabel.vmr.read_vmr("anatomy.vmr")
v16_header = bvbabel.v16.create_v16()
v16_header["DimX"] = vmr_header["DimX"]
v16_header["DimY"] = vmr_header["DimY"]
v16_data = vmr_data.astype(np.uint16)
bvbabel.v16.write_v16("anatomy.v16", v16_header, v16_data)

# V16 → VMR
v16_header, v16_data = bvbabel.v16.read_v16("anatomy.v16")
vmr_header = bvbabel.vmr.create_vmr()
vmr_header["DimX"] = v16_header["DimX"]
vmr_header["DimY"] = v16_header["DimY"]
vmr_data = v16_data.astype(np.uint8)
bvbabel.vmr.write_vmr("anatomy.vmr", vmr_header, vmr_data)
```

## Gotchas

- STC data type mismatch: check FMR DataType field. DataType=1 → int16 (2 bytes), DataType=2 → float32 (4 bytes)
- Mosaic FMRs: DimX/DimY/DimZ=0 → bvbabel can't convert. Use BV's internal NIfTI export instead.
- TRF files: text INI-style with `[Section]` headers, not binary.
- VMR uses big-endian int32 for pre-data header; V16 uses little-endian uint16. Do not mix endianness.
- `read_stc()` is on `bvbabel.fmr`, not a separate `bvbabel.stc` module.
- bvbabel GLM support is work-in-progress; prefer BV GUI for GLM I/O when possible.
- VMR data range 0-225 (not 0-255); V16 data range 0-4095.
- FMR header keys are case-sensitive; use exact names as output by bvbabel.
