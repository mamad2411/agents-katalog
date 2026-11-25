---
name: bv-expert
description: >
  BrainVoyager expert knowledge base and natural language assistant. Provides
  conceptual explanations, capability overviews, User's Guide chapter references,
  coordinate systems, file format summaries, and workflow guidance. Use when the
  user asks what is X in BV, how does BV do Y, explain coregistration/GLM/normalization,
  what can BV do, BV pipeline help, or any conceptual neuroimaging analysis question.
  Also activates alongside pipeline skills as overarching reference knowledge.
---

## ⚠️ CRITICAL: Reference-First Policy (Anti-Hallucination)

When the user asks ANY question about BV workflows, tools, limitations,
constraints, or procedures, you MUST consult the official documentation
BEFORE answering:

1. **First**, open `guide-urls.md` (alongside this file) and find the
   relevant page URL.
2. **Then**, `fetch()` that page from the User's Guide.
3. **Only then**, answer — and base your answer on what the fetched page
   actually says.

**DO NOT** answer from general knowledge, training data, or assumptions
about how BV "probably works" or "should work." BrainVoyager has documented
limitations (e.g., auto AC-PC fails on sub-mm VMRs, Talairach has no
isovoxel requirement unlike MNI) that directly contradict common
neuroimaging assumptions.

**Examples of questions that REQUIRE a fetch:**
- "Can I do X on a Y mm VMR?"
- "What's the minimum/maximum resolution for Z?"
- "Does tool A work with constraint B?"
- "What's the correct order of steps for W?"
- "What parameters does procedure P accept?"

When in doubt: **FETCH FIRST, answer second.** The only exception is
truly general questions like "what can BV do?" or questions already
covered in full by this SKILL.md or another pipeline skill.

## Role

This skill provides expert context and reference knowledge. It does NOT initiate pipeline execution. Answer questions using the knowledge below — and the Reference-First Policy above.

Only when the user explicitly asks you to DO something (preprocess my data, coregister these runs) should pipeline skills be activated.

## Using the User's Guide

The complete BrainVoyager User's Guide is available online. A URL index of all ~190
pages is in `guide-urls.md` alongside this skill.

**When the user asks a detailed question about a BV concept, tool, or workflow:**
1. Look up the relevant section in `guide-urls.md`
2. Fetch the full page with `fetch()` using the URL
   (base: `https://download.brainvoyager.com/bv/doc/UsersGuide/`)
3. Answer with direct reference to the official documentation

**When the user asks a general question** ("what can BV do?") or a pipeline question
covered by another skill, answer from the knowledge below without fetching.

**Note**: The guide pages contain HTML tables and structure — focus on extracting
the text content. Images in the guide cannot be rendered but the textual descriptions
of GUI workflows are complete.

## BV Capability Map

### Data Import
DICOM rename/anonymize/scan → bv-dicom-setup. FMR/VMR/DMR from DICOM. BIDS NIfTI export. DICOM defacing.

### Anatomical Preprocessing
VMR creation, MP2RAGE denoising, IIHC, isovoxel, MNI-152 normalization, AC-PC/Talairach transform, defacing → bv-anatomical-pipeline.

### fMRI Preprocessing
FMR creation, slice timing, motion correction, HPF, spatial smoothing, EPI distortion correction (FSL topup) → bv-fmri-preprocessing.

### Coregistration & Normalization
BBR + intensity-based coregistration, VTC creation in native/MNI/Tal space, VTC post-processing, MDM group setup → bv-coregistration-vtc.

### Cortex Segmentation & Surfaces
Automatic cortex segmentation, mesh reconstruction (marching cubes), smoothing, inflation, shrink-wrap, DNN segmentation. BBR auto-segmentation.

### Statistical Analysis
Single-subject GLM, multi-run GLM, RFX group GLM, ANOVA (1/2/3 factor, repeated measures, mixed), GLMsingle, contrast maps, multiple comparison correction (FDR, Bonferroni, cluster).

### Advanced Analysis
MVPA (SVM, searchlight, RFE), RSA, pRF, ICA (single/group), ISC, cortical thickness, CBA, DTI/fiber tracking, EEG/MEG (EMEG suite), event-related averaging, probabilistic maps, laminar/columnar analysis.

## MCP Tool Landscape

| Server | Tools | Role |
|--------|-------|------|
| bv_core_server | 27 | Doc open/close/save, DICOM ops, exec_bv_python, run_bv_shell_command |
| bv_anatomy_server | 31 | VMR pipeline, IIHC, MNI/Tal, mesh morphing, MP2RAGE |
| bv_fmri_server | 22 | FMR preprocessing, VTC coreg/creation, MDM |
| bv_assistant_server | 4 | BV launch, widget introspection (bv_query/bv_act), coordinate nav |

## Pipeline Skill Routing

| User asks... | Activate |
|-------------|----------|
| rename/anonymize/scan DICOMs | bv-dicom-setup |
| process anatomy/VMR/IIHC/MNI/Tal | bv-anatomical-pipeline |
| preprocess fMRI/slice timing/MC/HPF/smooth/distortion | bv-fmri-preprocessing |
| coregister/create VTC/MNI/Tal space | bv-coregistration-vtc |
| read/write BV files/bvbabel | bv-file-formats |
| what is X / how does Y work / BV capabilities | bv-expert |

## Key Concepts

### Coordinate Systems
BV radiological: X=left→right, Y=posterior→anterior, Z=inferior→superior.
BV↔Tal: BV X = Tal Y, BV Y = Tal Z, BV Z = Tal X.
BV↔NIfTI: flip [::-1,::-1,::-1], transpose (0,2,1).

### Preprocessing Order (Critical)
Slice timing FIRST → motion correction → HPF → smoothing.
Why: MC assumes simultaneous slices (fixed by step 1). HPF needs stationary brain (after step 2). Smoothing last (smooth data harder to align).

### BBR vs Intensity Coregistration
BBR: auto-segments WM/GM boundary → creates mesh → aligns EPI to boundary gradient. More accurate, first run slow.
Intensity: maximizes mutual information. Fallback when BBR mesh fails. Uses T1-saturated first volume for best contrast.

### MNI vs Talairach
MNI: affine + nonlinear warp to MNI-152. Modern standard. Requires ≥1mm isovoxel.
Talairach: AC-PC alignment + 12 sub-volumes with independent scaling. Legacy, compatible with older databases.

### Document Types
VMR (.vmr) = uint8 3D anatomy. V16 (.v16) = uint16 3D anatomy (for IIHC/MP2RAGE). FMR (.fmr) = text header + .stc binary. STC = 4D binary [T,Z,Y,X]. VTC (.vtc) = 4D in 3D reference space. SRF = surface mesh. TRF (.trf) = text transform matrix. PRT = protocol/events. SDM = design matrix. MDM = multi-design matrix (group). VMP/SMP = statistical maps. VOI/POI = ROIs.

## User's Guide Quick Finder

| Topic | Chapter |
|-------|---------|
| Getting started, GUI | Getting Started |
| DICOM import, FMR/VMR creation | Getting Started → DICOM to Documents |
| Coordinate systems | Coordinates and Transformations |
| NIfTI | NIfTI Files |
| Python scripting, plugins | Scripts and Plugins |
| Data Analysis Manager | Data Analysis Manager |
| Slice timing, MC, HPF, distortion | Data Preprocessing |
| BBR, intensity coregistration | Coregistration |
| MNI, Talairach, VTC creation | Transformation to Normalized Space |
| GLM, ANOVA, group analysis | Statistical Data Analysis |
| Cortex segmentation, mesh | Brain and Cortex Segmentation |
| VOI/POI | Regions-Of-Interest |
| CBA | Cortex-Based Alignment |
| MVPA, RSA, pRF, ICA, ISC | Multi-Voxel Pattern Analysis / RSA / pRF / Functional Connectivity |
| DTI, fiber tracking | Diffusion-Weighted Imaging Analysis |
| EEG/MEG | EEG/MEG Analysis: The EMEG Suite |

Full guide: https://download.brainvoyager.com/bv/doc/UsersGuide/BrainVoyagerUsersGuide.html
