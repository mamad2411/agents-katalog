# Spatial Transcriptomics

Processing and analysis of spatially resolved transcriptomics across sequencing-based (Visium, Visium HD, Slide-seq, Stereo-seq) and imaging-based (Xenium, MERSCOPE, CosMx) platforms. Covers loading, QC, normalization, and spatially variable gene detection. Dual-language: Python (squidpy/SpatialData) and R (SpatialExperiment/Seurat v5).

## When to Use This Skill

Activate when the user requests:
- Visium or Visium HD data loading and quality control
- Xenium, MERSCOPE, CosMx, or Stereo-seq processing
- Spatial quality control and artifact detection
- Spatially variable gene (SVG) detection
- Spatial autocorrelation (Moran's I, Geary's C)
- Conversion between spatial data containers
- Any analysis where transcript measurements carry coordinates

## Platform Types

The single most important distinction. It determines every downstream choice.

```
Sequencing-based (spot/bin resolution, whole transcriptome):
  Visium        55 um spots, ~1-10 cells per spot, ~18k genes
  Visium HD     2 um bins (binned to 8/16 um), subcellular grid, whole transcriptome
  Slide-seq V2  10 um beads
  Stereo-seq    220 nm DNB, binned
  -> Spots mix cell types. You need DECONVOLUTION.

Imaging-based (single-cell/subcellular, targeted panel):
  Xenium        ~5k genes max (Prime 5K), segmented cells
  MERSCOPE      ~500-1000 genes
  CosMx         ~1000-6000 genes
  -> Cells are already segmented. You need CELL TYPING, not deconvolution.
     Segmentation quality is the dominant error source.
```

## Inputs

| Platform | Format | Reader |
|----------|--------|--------|
| Visium | Space Ranger `outs/` (h5 + `tissue_positions.csv` + images) | `squidpy.read.visium`, `VisiumIO::TENxVisium` |
| Visium HD | Space Ranger `outs/` with `binned_outputs/`, `tissue_positions.parquet` | `spatialdata_io.visium_hd`, `VisiumIO::TENxVisiumHD` |
| Xenium | Xenium Onboard Analysis output bundle | `spatialdata_io.xenium`, `XeniumIO::TENxXenium` |
| MERSCOPE | Vizgen output (`cell_by_gene.csv`, `cell_metadata.csv`) | `spatialdata_io.merscope` |
| CosMx | NanoString flat files | `spatialdata_io.cosmx`, `readCosmxSXE` |
| Stereo-seq | STOmics GEF/GEM (v7.x only) | `spatialdata_io.stereoseq` |

---

## Environment

Version pins that matter. The spatial stack moved fast and broke things.

```
Python (all require Python >= 3.12 as of squidpy 1.8.3 / spatialdata 0.8.0)
  squidpy         1.8.3
  spatialdata     0.8.0
  spatialdata-io  0.7.1
  scanpy          1.12.3
  anndata         0.13.2

R (Bioconductor 3.23, R 4.6)
  SpatialExperiment       1.22.0
  SpatialFeatureExperiment 1.14.0
  Voyager                 1.14.0
  VisiumIO / XeniumIO     1.8.0 / 1.4.0
  SpotSweeper             1.8.0
  nnSVG                   1.16.1
  Seurat                  5.5.1
```

Python 3.11 was dropped in squidpy 1.8.3 and spatialdata 0.8.0. `zarr>=3` is required.

---

## Loading Data

### Deprecations to know first

| Deprecated | Since | Use instead |
|------------|-------|-------------|
| `scanpy.read_visium` | scanpy 1.11.0 | `squidpy.read.visium` |
| `scanpy.pl.spatial` | scanpy 1.11.0 | `squidpy.pl.spatial_scatter` |
| `scanpy.datasets.visium_sge` | scanpy 1.11.0 | `squidpy.datasets.visium` |
| `SpatialExperiment::read10xVisium` | SpatialExperiment 1.15.2 | `VisiumIO::TENxVisium` |

Scanpy adopted the SPEC-0 deprecation schedule in 1.12.0, so these are on a removal clock. Treat them as dead code in new pipelines.

### Visium (Python)

```python
import squidpy as sq

adata = sq.read.visium(
    "path/to/outs",
    counts_file="filtered_feature_bc_matrix.h5",  # note: counts_file, not count_file
    load_images=True,
)
adata.var_names_make_unique()
```

`squidpy.read.visium` parses `tissue_positions.csv` only. It does not read `tissue_positions.parquet`, so it cannot load Visium HD. Space Ranger v1/v2/v3 position-file variants are handled automatically (header presence is sniffed at runtime).

### Visium HD (Python)

```python
import spatialdata_io as sdio

sdata = sdio.visium_hd(
    "path/to/outs",
    bin_size=8,                      # pass 2, 8, or 16 explicitly; None loads ALL bins
    bins_as_squares=True,            # False draws circles, which is geometrically wrong
    load_segmentations_only=False,   # set explicitly: default flips to True in a future release
)

# Table for a given bin lives in sdata.tables
adata = sdata.tables["square_008um"]
```

```
Bin size selection:
  2 um   subcellular grid, mostly empty, only for segmentation input
  8 um   default working resolution, roughly one cell
  16 um  use when 8 um is too sparse for your panel or tissue
```

Space Ranger 4.0.1+ runs nucleus and cell segmentation by default on H&E, using a custom StarDist implementation. `bin2cell` is now only needed for IF rather than H&E images, reprocessing pre-4.0 outputs, or custom bin-joining logic.

### Xenium, MERSCOPE, CosMx, Stereo-seq (Python)

```python
import spatialdata_io as sdio

sdata = sdio.xenium("path/to/xenium_out", gex_only=False)   # gex_only=False keeps control probes
sdata = sdio.merscope("path/to/merscope_out")
sdata = sdio.cosmx("path/to/cosmx_out")
sdata = sdio.stereoseq("path/to/stereoseq_out")             # v7.x only, v8.x unsupported
```

Three Xenium reader behaviours that cause silent problems:

```
gex_only=True is the DEFAULT.
  It drops negative control probes, unassigned codewords, and antisense features.
  You need those to compute the false-discovery rate. Pass gex_only=False.

cells_as_circles default changed to False in spatialdata-io 0.7.0.
  The table region key follows it:
    cells_as_circles=True  -> region "cell_circles"
    cells_as_circles=False -> region "cell_labels"
  Code matching on obs["region"] == "cell_circles" breaks across that version boundary.

n_jobs= is a deprecated no-op since 0.7.0.
```

### SpatialData as the container

`SpatialData` is the current standard for Python spatial work: OME-NGFF/Zarr for images and labels, Parquet for shapes and points, AnnData for tables.

```python
sdata.write("sample.zarr")

import spatialdata as sd
sdata = sd.read_zarr("sample.zarr")

# Provenance: reader name and spatialdata-io version are stamped in since 0.7.0
print(sdata.attrs)
```

Use `squidpy.read.*` when you want a flat `AnnData` for plain Visium. Use `spatialdata_io` for everything else, and whenever images need to be first-class elements.

### R

```r
library(VisiumIO)

# Visium
spe <- TENxVisium(
  spacerangerOut = "path/to/outs",
  processing = "filtered",
  images = "lowres"
) |> import()

# Visium HD — bin_size is a ZERO-PADDED character vector
spe <- TENxVisiumHD(
  spacerangerOut = "path/to/outs",
  bin_size = "008"
) |> import()

# Xenium
library(XeniumIO)
spe <- TENxXenium(xeniumOut = "path/to/xenium_out") |> import()
```

When you need negative control probes kept as `altExps` (the cleanest route to control-probe QC in R):

```r
library(SpatialExperimentIO)
spe <- readXeniumSXE(
  dirName = "path/to/xenium_out",
  altExps = c("NegControlProbe", "UnassignedCodeword", "NegControlCodeword", "antisense", "BLANK")
)
```

### Seurat v5

```r
library(Seurat)  # 5.5.1

obj <- Load10X_Spatial("path/to/outs")                    # Visium
obj <- Load10X_Spatial("path/to/outs", bin.size = c(8, 16))  # Visium HD
obj <- LoadXenium("path/to/xenium_out", mols.qv.threshold = 20)
obj <- LoadVizgen("path/to/merscope_out", fov = "fov")
```

```
Seurat 5.4.0 changed the binned Visium coordinate convention:
  x now maps to imagecol, y to imagerow, origin top-left, matching 10x.
  Plots and hand-written coordinate math from Seurat <= 5.3.x are transposed.
  Re-derive coordinates if you are porting old code.

LoadVizgen hard-codes filter = "^Blank-", removing blank codewords before you
see them. Read them separately if you need a blank-codeword FDR.
```

---

## Quality Control

### Sequencing-based platforms

The standard four metrics are library size, detected genes, mitochondrial proportion, and (where segmentation exists) cells per spot.

The practice that changed: **global thresholds are no longer recommended.** A tissue section has regionally varying cell density and RNA content. A global cutoff removes whole anatomical regions (low-cellularity white matter, necrotic cores) rather than low-quality spots. Spatially local outlier detection compares each spot against its own neighbourhood.

```r
library(SpotSweeper)
library(scrapper)

is_mito <- grepl("^MT-", rowData(spe)$symbol)
spe <- quickRnaQc.se(spe, subsets = list(mito = is_mito))
# adds colData: sum, detected, subset.proportion.mito

spe <- localOutliers(spe, metric = "sum",      direction = "lower",  log = TRUE)
spe <- localOutliers(spe, metric = "detected", direction = "lower",  log = TRUE)
spe <- localOutliers(spe, metric = "subset.proportion.mito", direction = "higher", log = FALSE)

# Detect technical artifacts (edge/hangnail effects) rather than biological variation
spe <- findArtifacts(spe, mito_percent = "expr_chrM_ratio", n_order = 7, shape = "hexagonal")
```

`localOutliers` defaults to `n_neighbors = 36` and `cutoff = 3` MADs computed within the local neighbourhood. `findArtifacts` defaults to `n_order = 5`; OSTA uses 7.

Illustrative global thresholds, for reference only (DLPFC Visium): <600 UMI, <400 genes, mito >0.28.

### Imaging-based platforms

Different failure modes, so different metrics. Segmentation errors dominate.

```
What actually goes wrong:
  Over-segmentation   one cell split into fragments -> low counts, small area
  Under-segmentation  two cells merged -> mixed profiles, large area, high counts
  Transcript bleed    signal assigned to a neighbouring cell
  FOV border effects  partial cells at field-of-view edges

Metrics that catch these:
  cell area, signal density (transcripts/um2), aspect ratio,
  negative-control fraction, distance to FOV border
```

```r
library(SpaceTrooper)

spe <- spatialPerCellQC(spe, micronConvFact = 0.12)
# adds: Area_um, log2SignalDensity, log2AspectRatio, log2Ctrl_total_ratio, dist_border

spe <- computeQCScore(spe)
spe <- computeQCScoreFlags(spe, qsThreshold = 0.5)
spe <- computeSpatialOutlier(spe)   # FOV-border rule
```

A stricter rule for Xenium, using transcript density normalized by cell area:

```r
nc <- spe$total_counts / spe$cell_area
ol <- scuttle::isOutlier(nc, log = TRUE, type = "lower", nmads = 3)
discard <- ol | spe$control_probe_counts > 0 | spe$control_codeword_counts > 0
```

This flags roughly 16% of cells on a typical Xenium run. That is expected, not a sign of a bad experiment.

### Negative-control FDR (Xenium)

Xenium panels carry dedicated negative controls: 20 negative control targets on v1 pre-designed panels (27 on the Mouse Brain base panel), 40 on Prime panels, plus negative control codewords and genomic control probes.

```
Estimated false positives per cell =
  (negative control probe counts / n_negative_control_probes / n_cells) x n_target_genes

Only Q-Score >= 20 transcripts enter analysis.
```

10x publishes no numeric pass/fail threshold. Report the run's control-derived FDR, compare across runs on the same panel, and treat any cell with nonzero control counts as suspect rather than chasing an absolute cutoff.

### Image QC

```python
import squidpy as sq

sq.experimental.im.qc_image(
    sdata, image_key="morphology_focus",
    is_hne=False, detect_tissue=True, detect_outliers=True,
)
```

Computes sharpness (Tenengrad, variance of Laplacian, FFT high-frequency energy), intensity, H&E stain separation, tissue fold fraction, and tissue coverage. This API is under `experimental` and may change.

---

## Normalization

```
Which normalization?

  Visium / Visium HD (spots contain multiple cells)
    -> Library-size normalization + log1p. Same as scRNA-seq.
    -> sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
    -> SCTransform also works and is common in Seurat spatial workflows.

  Imaging-based (segmented cells, targeted panel)
    -> Normalize by total counts, but DO NOT assume a fixed target sum matched
       to whole-transcriptome data. The panel is targeted, so total counts
       reflect panel composition, not library complexity.
    -> Consider normalizing by cell volume/area instead of counts when
       segmentation quality is high.

  Never
    -> TPM/FPKM. Spatial UMI counts are not length-biased.
```

```python
adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
```

Keep raw counts. Deconvolution methods (cell2location, RCTD) and pseudobulk DE all require them.

---

## Spatially Variable Genes

A spatially variable gene has expression structured by location beyond what cell type composition alone explains. This is the spatial analogue of highly variable gene selection.

### Method selection

```
Which SVG method?

  Default, Python, any dataset size
    -> Moran's I via sq.gr.spatial_autocorr(mode="moran")
    -> Competitive with dedicated methods in benchmarks, fast, maintained.

  Need calibrated p-values
    -> SPARK-X (R). The only method besides SPARK with well-calibrated p-values.
    -> Caveat: GitHub-only, unmaintained since 2022.

  Need to regress out covariates
    -> nnSVG (Bioconductor, X= argument). The only actively maintained,
       properly distributed method in the top-performing group.
    -> Slower; keep the dataset modest.

  Very large dataset, memory constrained
    -> SOMDE (best memory + runtime) or SPARK-X.

  Do NOT use
    -> SpatialDE (PyPI 1.1.3, abandoned since 2019; ~150 GB at 40k spots)
    -> SPARK proper (~250 GB at 20k spots)
```

### The p-value problem

Benchmarking of 14 SVG methods (Li et al., Genome Biology 2025;26:285) found p-value calibration broken for most methods: only SPARK and SPARK-X produced well-calibrated p-values, six were over-conservative, and four failed to control type I error.

```
Consequence for practice:
  Select SVGs by a fixed RANK cutoff (e.g. top 2000 by score),
  not by FDR-adjusted significance.

Overall ranking: SPARK-X (4.3) > SpaGFT (5.4) > Moran's I (third).
For downstream spatial domain detection specifically, Moran's I ranked
best (6.5), then SpatialDE2 (6.6), then nnSVG (6.8).

Known shared failure: most methods (SPARK-X, nnSVG, Moran's I, Spanve)
do poorly on genes expressed highly in a small area and absent elsewhere.
```

### Moran's I (Python)

```python
# sq.gr.spatial_neighbors is deprecated since squidpy 1.7.0 and is removed in
# 1.9.0. Use the mode-specific builders.
sq.gr.spatial_neighbors_grid(adata, n_neighs=6)        # Visium hex grid
sq.gr.spatial_autocorr(adata, mode="moran", n_perms=100, n_jobs=4)

svgs = adata.uns["moranI"].head(2000).index    # rank, do not threshold on p
```

```
Graph builder by platform:
  Visium (hex grid)     spatial_neighbors_grid(n_neighs=6)
  Visium HD (square)    spatial_neighbors_grid(n_neighs=4)   8 with diagonals
  Imaging-based         spatial_neighbors_delaunay()  or  spatial_neighbors_knn(n_neighs=6)
  Fixed physical range   spatial_neighbors_radius(radius=30)   radius in coordinate units

Replacements for the deprecated call:
  spatial_neighbors_knn, spatial_neighbors_radius, spatial_neighbors_delaunay,
  spatial_neighbors_grid, spatial_neighbors_from_builder, plus mask_graph.

When passing a SpatialData object, table_key is REQUIRED and keyword-only.
```

squidpy 1.8.2 changed the Geary's C variance calculation to use normality assumptions. Geary's C p-values from 1.8.1 and earlier are not comparable to 1.8.2+.

### nnSVG (R)

```r
library(nnSVG)

spe <- spe[, colSums(counts(spe)) > 0]
spe <- logNormCounts(spe)

# X = model matrix of covariates to regress out (e.g. known domain labels)
spe <- nnSVG(spe, X = NULL, n_neighbors = 10, n_threads = 4)

svgs <- rownames(spe)[order(rowData(spe)$rank)][1:2000]
```

### Seurat

```r
obj <- FindSpatiallyVariableFeatures(
  obj, assay = "Spatial", layer = "scale.data",
  selection.method = "moransi", nfeatures = 2000
)
```

Seurat offers only `markvariogram` and `moransi`, neither in the benchmark's top tier. `slot=` was soft-deprecated in favour of `layer=` in 5.3.0. Bugs in this function were fixed in 5.3.0 and 5.5.0, so results from 5.2.x and earlier are suspect.

---

## Deconvolution

Only for sequencing-based platforms. A Visium spot holds 1-10 cells, so every spot is a mixture. Deconvolution estimates the cell type proportions per spot from a single-cell reference.

Imaging-based platforms do not have this problem and do not need this section. Skip to *Cell Typing on Segmented Data*.

### Method selection

```
Which deconvolution method?

  Default first choice, Visium
    -> RCTD (rctd_mode="full"). Wins or ties on real-data comparisons,
       fastest of the accurate methods, CPU-parallel, no GPU needed.

  Multi-sample spatial data with real platform/batch effects, rare cell types,
  and a GPU available
    -> cell2location. Model the reference batch structure explicitly.
       Run detection_alpha at both 20 and 200 and compare.

  Composition expected to vary smoothly across the tissue
    -> CARDspa (CAR prior) or SONAR.

  >200k spots, or Visium HD at 2 um
    -> RCTD or FlashDeconv. cell2location becomes impractical at that scale.

  ALWAYS, alongside whichever you pick
    -> An NNLS or marker-signature-scoring baseline.
```

### Why the baseline is not optional

Two independent benchmarks found simple methods competitive with dedicated ones.

```
Spotless (eLife 2024;12:RP88431), 11 methods, 63 silver + 3 gold standards:
  "a simple regression model outperforms almost half of the dedicated
   spatial deconvolution methods"
  All other methods ranked worse than NNLS on at least one metric.
  Top performers: RCTD and cell2location.

Sun et al. (bioRxiv 2026, doi:10.64898/2026.01.13.699379):
  "a simple marker gene signature scoring approach performs competitively,
   often outperforming more complex models, particularly for rare cell types"
  Works without a matched single-cell reference.

spDDB (bioRxiv 2026, doi:10.64898/2026.05.11.724248), 21 methods, 37 datasets:
  Cell2location, RCTD, and SONAR top across tissue types, but performance
  "varied substantially based on tissue architecture, spatial technology,
   dataset scale, and cell type diversity."
```

Run the baseline. Accept the sophisticated method only when it beats it on your data.

### RCTD: two packages share the name

This trips up anyone following older tutorials.

| | Bioconductor `spacexr` 1.4.0 | GitHub `dmcable/spacexr` 2.2.1 |
|---|---|---|
| API | `createRctd()` / `runRctd()` | `create.RCTD()` / `run.RCTD()` |
| Objects | SpatialExperiment in and out | custom `SpatialRNA` / `Reference` |
| CSIDE | not ported | included |
| Weights orientation | cell types x pixels | pixels x cell types |

Old `create.RCTD` code does not run against the Bioconductor package, and the weights matrix is transposed between them.

```r
library(spacexr)  # Bioconductor 1.4.0

rctd_data <- createRctd(
  spatial_experiment  = spe,
  reference_experiment = ref_sce,
  cell_type_col = "cell_type"
)

spe_out <- runRctd(rctd_data, rctd_mode = "full", max_cores = 4)

# weights assay is cell types x pixels; columns sum to 1 except rejected pixels
props <- assay(spe_out, "weights")
```

```
Mode selection:
  full     any number of cell types per pixel. Use for Visium proportions.
  doublet  at most two types, classified singlet/doublet. Use at ~cell scale
           (Slide-seq, MERFISH, 16 um HD bins) when you want a discrete call.
  multi    greedy fit of up to max_multi_types (default 4). Sparse discrete set.
```

`doublet` mode has a second use on imaging platforms: a pixel called "doublet" is a signal that segmentation fused two cells.

### cell2location

Two-step: fit reference signatures with a negative binomial regression, then map to space.

```python
import cell2location
from cell2location.models import RegressionModel, Cell2location
from cell2location.utils.filtering import filter_genes

# Step 0: gene filtering. Package defaults are 15 / 0.05 / 1.12; the official
# tutorial loosens them to keep rare-cell-type markers.
selected = filter_genes(adata_ref, cell_count_cutoff=5,
                        cell_percentage_cutoff2=0.03, nonz_mean_cutoff=1.12)
adata_ref = adata_ref[:, selected].copy()

# Step 1: reference signatures. Declaring batch structure here is what removes
# reference platform effects. Skipping it is a common cause of bad output.
RegressionModel.setup_anndata(
    adata_ref, layer="counts",
    batch_key="sample",                       # donor / technical batch
    labels_key="cell_type",
    categorical_covariate_keys=["method"],    # chemistry / protocol
)
ref_mod = RegressionModel(adata_ref)
ref_mod.train(max_epochs=250, accelerator="gpu", devices=1)
adata_ref = ref_mod.export_posterior(adata_ref)

signatures = adata_ref.varm["means_per_cluster_mu_fg"]

# Step 2: spatial mapping
Cell2location.setup_anndata(adata_vis, layer="counts", batch_key="sample")
mod = Cell2location(
    adata_vis, cell_state_df=signatures,
    N_cells_per_location=30,   # count nuclei in 10-20 spots on the paired H&E
    detection_alpha=20,        # 20 for high within-slide technical variation, 200 for low
)
mod.train(max_epochs=30000, batch_size=None, train_size=1,
          accelerator="gpu", devices=1)
adata_vis = mod.export_posterior(adata_vis)

props = adata_vis.obsm["q05_cell_abundance_w_sf"]
```

```
use_gpu=True is an ERROR, not a warning.
  scvi-tools deprecated it in 1.0.4 and REMOVED it in 1.1.0.
  Much of the published cell2location tutorial material still uses it.
  Pass accelerator="gpu", devices=1 instead.

Never hold out data: train_size=1. You need an abundance estimate at
every location, so there is no validation split to make.
```

### Tangram

```python
# PyPI tangram-sc is frozen at 1.0.4 (2023-02-09). The refinement regularizers
# merged to master in 2025 were never released.
import scvi
model = scvi.external.Tangram(mdata)     # PyTorch backend since scvi-tools 1.5.0
model.train(max_epochs=1000, accelerator="auto")
mapper = model.get_mapper_matrix()
```

`scvi.external.Tangram` supports only `cells` and `constrained` modes. It has no `clusters` mode, so it is not a drop-in for the cheap cluster-level Visium workflow that `tangram-sc` offers.

### SPOTlight

```r
library(SPOTlight)

# mgs comes from scran::scoreMarkers. This seeding dominates output quality.
res <- SPOTlight(x = sce, y = spe, groups = sce$cell_type, mgs = mgs,
                 gene_id = "gene", group_id = "cluster", weight_id = "weight")
props <- res$mat
```

Make sure `groups` is not a factor. SPOTlight is the only one of these four that accepts pre-normalized input.

### Reference atlas requirements

```
Counts format
  Raw, integer, untransformed counts for RCTD and cell2location.
  RCTD errors outright on non-integers (require_int = TRUE).
  Do not log-transform, scale, or subset to HVGs before deconvolution.
  SPOTlight is the exception and accepts normalized input.

Hard minimums encoded in RCTD
  >= 25 cells per cell type      types below this are silently DROPPED
  <= 10,000 cells per type       downsampled above this
  >= 100 UMI per reference cell
  >= 100 UMI per spatial pixel
  gene observed in >= 3 pixels

Annotation granularity
  Match it to the question. A 40-subtype reference on 55 um spots produces
  proportions you cannot defend. Use RCTD's class_df for a coarse fallback.

Reference choice
  Same tissue, condition, and ideally cohort. Multi-patient same-indication
  atlases hold up well; cross-patient references degrade accuracy.
  Even small references work: "even small reference datasets can yield
  accurate deconvolution results" (bioRxiv 2026, doi:10.64898/2026.01.09.698566).
```

Treat output proportions as **relative and comparative, not absolute**. The same study found prominent types are spatially localized correctly but "systematically under- or over-estimated" in magnitude. Compare a cell type across regions or conditions, not against its true percentage.

---

## Cell Typing on Segmented Data

For Xenium, MERSCOPE, and CosMx. The dominant error source is segmentation, not typing.

### Segmentation

| Tool | Approach | Notes |
|------|----------|-------|
| Xenium Ranger v4.0 | boundary stain, then interior stain, then DAPI expansion | `--expansion-distance` default 5 um since v2.0. v4.0 adds `--segment-large-cells` |
| Proseg 3.2.0 | cellular Potts model over transcript positions | Best average performance in the CRISP benchmark. Needs a prior segmentation for cell count and location |
| Baysor 0.8.3 | Bayesian, transcript-only or with nuclear prior | C++ port since 0.8.0; the Julia line ended at 0.7.1 |
| segger | heterogeneous GNN, transcript-to-cell link prediction | GPU recommended, not required |
| bin2cell | StarDist on H&E, expanded into 2 um HD bins | CPU only, ~15 min on the demo |

```
The CRISP benchmark (bioRxiv 2026, doi:10.64898/2026.04.16.718947), five
approaches across ten mouse tissues on a 5,006-gene Xenium panel:

  "Proseg achieved the highest average performance across tissues, though
   the magnitude of its advantage varies with tissue architecture."

  "segmentation algorithms face a fundamental tradeoff between maximizing
   transcript capture and maintaining cell purity, and the severity of this
   tradeoff is tissue-dependent."

There is no universally correct segmentation. Check purity on your tissue.
```

### Contamination correction

Transcripts get assigned to the wrong cell regardless of method. Correct it rather than ignoring it.

```python
import scvi
scvi.external.RESOLVI    # generative correction of misassigned molecules,
                         # background, and batch effects. scvi-tools >= 1.3.0
```

`SPLIT` (R, RCTD-driven) separates primary from spillover signal. `MisTIC` corrects misassignment without resegmentation.

### Label transfer

```r
# SingleR was the best reference-based annotator for Xenium in a head-to-head
# comparison against Azimuth, RCTD, scPred, and scmapCell
# (Cheng et al., BMC Bioinformatics 2025;26:22)
library(SingleR)
pred <- SingleR(test = spe, ref = ref_sce, labels = ref_sce$cell_type)
```

Python: scANVI, popV (ensemble with ontology voting and uncertainty scores), CellTypist.

Subset the reference to the panel genes before training. A 5,000-gene Xenium panel cannot support annotation granularity that depends on genes it does not measure.

### Visium HD sits in between

```
2 um bins   sub-cellular. Do NOT deconvolve. Reconstruct cells (bin2cell or a
            segmented workflow), then annotate.
8 um bins   10x's recommended unit, still multi-cell. Deconvolve.
16 um bins  deconvolve; RCTD doublet mode works well here.

Resolution horizon (FlashDeconv, bioRxiv doi:10.64898/2025.12.22.696108):
  bins dominated by a single cell type (>80%) fall from 61.5% at 8 um
  to 13.3% at 16 um.
  Cell-cell correlations can INVERT with bin size: Paneth-Goblet
  r = -0.12 at 8 um becomes +0.80 at 64 um.

Bin size is not a display choice. It changes the biology you infer.
```

---

## Spatial Domains and Niches

### Domain is not niche

These get conflated and they are different questions.

```
Spatial domain    contiguous tissue region with a shared expression profile
                  (cortical layer, germinal center, tumor core)
                  -> spatially smooth, few large regions

Cellular niche    local cell-type composition around a cell, which can recur
                  in disconnected places across the tissue
                  -> not necessarily contiguous

A method tuned for domains will merge recurrent niches into one region.
A method tuned for niches will fragment a smooth domain.
Pick by which question you are asking, not by which tool is popular.
```

### Method selection

The benchmarks disagree, and the disagreement is structured: it tracks resolution, gene panel size, and tissue architecture.

| Setting | Use | Avoid |
|---------|-----|-------|
| Visium / spot-level, layered tissue | GraphST, STAGATE, PROST, BayesSpace | BANKSY, CellCharter (aggregation hurts at low resolution) |
| Imaging-based single-cell | BANKSY, BASS, SpaceFlow, CellCharter | GraphST, SpatialPCA (fragile to heterogeneity) |
| Small panel (<500 genes) | SpaceFlow, SpaDo, BASS, CCST | BANKSY (<~1000 genes), CellCharter (<~100 genes) |
| Tumor / irregular architecture | CCST, PROST, IRIS | BASS (assumes spatial homogeneity) |
| Atlas scale (>500k cells) | MENDER, NicheCompass, CellCharter, TACCO | GraphST, SpaGCN, SEDR (fail above ~20k) |
| Multi-sample with batch effects | CellCharter, BASS, PRECAST, TACCO | most GNN methods have no batch handling |

```
The sobering result (Descoeudres et al., bioRxiv 2026,
doi:10.64898/2026.03.12.710462 — 26 methods, 63 sections, 6 technologies):

  "Nearly one-third of methods (9 of 26) perform worse overall than a simple
   spatial smoothing applied to the scanpy clustering output"

Spatial gains are modest on Visium (max delta-ARI 0.16) and large at high
resolution (delta-ARI 0.48 MERFISH, 0.32 Slide-seq).

Cellular heterogeneity within a domain, not the algorithm, is the dominant
determinant of accuracy.

Also: swapping the neural network out of GNN methods changed results little.
"preprocessing strategies and final clustering choices exert a substantially
 stronger influence" than the architecture.
```

Run Leiden with spatial smoothing as your baseline, exactly as with deconvolution.

### BANKSY

Augments each cell's feature vector with a spatially weighted mean of its neighbours. One parameter switches the objective.

```
lambda = 0     non-spatial, ordinary clustering
lambda = 0.2   spatial CELL TYPING
lambda = 0.8   spatial DOMAIN SEGMENTATION
```

```r
library(Banksy)

spe <- computeBanksy(spe, assay_name = "normcounts", compute_agf = TRUE, k_geom = c(15, 30))
# lambda and k_geom are vectorized: fit several at once and compare
spe <- runBanksyPCA(spe, use_agf = TRUE, lambda = c(0.2, 0.8), npcs = 20)
spe <- clusterBanksy(spe, use_agf = TRUE, lambda = c(0.2, 0.8), resolution = 1)
spe <- connectClusters(spe)
spe <- smoothLabels(spe, k = 15L)
```

Seurat users: `RunBanksy` lives in **SeuratWrappers**, not Seurat core, and `lambda` is required with no default.

```
Never call ScaleData after RunBanksy.

RunBanksy populates scale.data with the scaled BANKSY matrix. ScaleData then
does gene-wise z-scaling and negates the effect of lambda entirely.
```

BANKSY is the fastest method at scale (~1 min on 100k cells) but degrades sharply below ~1000 genes. Do not use it on a 300-gene panel.

### CellCharter

scVI embedding, then neighbourhood aggregation, then a Gaussian mixture. Handles multi-sample batch effects natively via the scVI `batch_key`, which most graph methods do not.

```python
import cellcharter as cc
import scvi

scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="sample")
model = scvi.model.SCVI(adata)
model.train()
adata.obsm["X_scVI"] = model.get_latent_representation()

sq.gr.spatial_neighbors_delaunay(adata)
cc.gr.aggregate_neighbors(adata, n_layers=3, use_rep="X_scVI", out_key="X_cellcharter")

# Pick the number of domains by stability, not by eye
autok = cc.tl.ClusterAutoK(n_clusters=(2, 15), max_runs=10)
autok.fit(adata, use_rep="X_cellcharter")
```

### squidpy neighbourhood statistics

```python
sq.gr.spatial_neighbors_delaunay(adata)

sq.gr.nhood_enrichment(adata, cluster_key="cell_type", n_perms=1000)
sq.gr.co_occurrence(adata, cluster_key="cell_type")
sq.gr.interaction_matrix(adata, cluster_key="cell_type", normalized=True)
sq.gr.ripley(adata, cluster_key="cell_type", mode="F")
```

```
What each one actually answers:

nhood_enrichment   are A and B adjacent more than chance, AT THE SCALE OF
                   YOUR GRAPH. Entirely determined by the graph you built.
                   Change n_neighs and the answer changes.
co_occurrence      the same question as a function of distance, graph-free.
                   Scales poorly; subsample or use sq.tl.sliding_window.
interaction_matrix the raw contingency table of adjacencies.
ripley             single-cluster spatial pattern, not pairwise.
```

`co_occurrence` was reimplemented in squidpy 1.6.6, so results are not bit-identical to 1.6.5 and earlier.

### Niche calling in one call

```python
sq.gr.calculate_niche(adata, flavor="cellcharter", distance=3,
                      aggregation="mean", n_components=10)
# flavors: "neighborhood", "utag", "cellcharter", "spatialleiden"
# each requires a different argument set; "spatialleiden" needs sc.pp.neighbors() first
```

---

## Spatially Resolved Cell-Cell Communication

### Method selection

```
Cell-type-pair level, "which types talk to which"
  -> LIANA+ or CellChat v2 spatial mode.

Per-spot / per-cell local interaction maps
  -> LIANA+ bivariate (li.mt.bivariate). Subsumes SpatialDM's bivariate
     Moran's R as one local_name option.

Single-cell-resolution data, want maximum benchmarked accuracy
  -> SpaCCI, CellPhoneDB v3, or CellChat v2.

Do NOT build new pipelines on
  -> NCEM (unmaintained since 2023), COMMOT via PyPI (0.0.3 is from 2022;
     install from GitHub if you need it).
```

```
Benchmark (Ku et al., Genome Biology 2026;27:163), 9 methods:

  Single-cell-resolution simulations (normalized F1):
    SpaCCI 92.7 > CellPhoneDB v3 77.4 > CellChat v2 69.6 > SpaTalk 62.2
  Spot-level simulations:
    SpaCCI 82.1 > SpaTalk 72.4 > SpatialDM 49.6

  "No single method is universally optimal across all datasets, spatial
   resolutions, and evaluation criteria."

Distance behaviour splits the methods:
  proximal-biased  CellChat v2, SpaTalk, SpatialDM, NicheDE, SpaCCI
  distal-biased    CellPhoneDB v3, COMMOT, SCOTIA

LIANA+ was not in this benchmark. It is recommended here anyway because it is
the only actively developed framework covering the full range, but that is a
maintenance argument, not an accuracy claim.
```

### LIANA+ bivariate

```python
import liana as li

# Bandwidth is in coordinate units. For Visium, 150-200 pixels covers roughly
# the first hexagonal ring (6 neighbours).
li.ut.spatial_neighbors(adata, bandwidth=200, cutoff=0.1,
                        kernel="gaussian", set_diag=True)   # set_diag for multi-cell spots

lrdata = li.mt.bivariate(
    adata, resource_name="consensus",
    local_name="cosine",     # "morans" reproduces SpatialDM
    global_name="morans",
    n_perms=100, mask_negatives=False, add_categories=True, nz_prop=0.2,
)
# lrdata.X = local scores, .layers["pvals"], .layers["cats"], .var = global summaries

li.mu.nmf(lrdata, k_range=range(1, 11))    # factorize into interaction programs
```

Use `li.ut.query_bandwidth` to pick the bandwidth from your coordinates rather than guessing.

### CellChat v2 spatial

```r
# Convert pixels to microns first. Getting this wrong silently rescales every
# distance threshold below.
spot.size <- 65                                                  # Visium spot diameter, um
conversion.factor <- spot.size / scalefactors$spot_diameter_fullres
spatial.factors <- data.frame(ratio = conversion.factor, tol = spot.size / 2)

cellchat <- createCellChat(object = data.input, meta = meta, group.by = "labels",
                           datatype = "spatial", coordinates = spatial.locs,
                           spatial.factors = spatial.factors)

cellchat <- computeCommunProb(
  cellchat, type = "truncatedMean", trim = 0.1,
  distance.use = TRUE, interaction.range = 250,   # um, caps secreted signalling
  scale.distance = 0.01,
  contact.dependent = TRUE, contact.range = 100   # 100 um Visium; 10 um for imaging
)
```

`contact.range` is 100 um for Visium and 10 um (one cell diameter) for single-cell-resolution platforms. `scale.factors` was renamed `spatial.factors` in CellChat 2.1.1, so older objects need `updateCellChat()`.

---

## Niche-Specific Differential Expression

Three different questions get called "niche DE". Only one of them is inferential.

```
(A) "Which genes mark domain D vs the rest, in one sample?"
    A cluster-marker problem. Effective n = 1. Report effect sizes.
    Do not attach p-values and call it DE.

(B) "Does domain D differ between conditions across samples?"
    Pseudobulk by sample x domain, then test the condition:domain
    interaction term. This is the one with real inference.

(C) "Within cell type X, which genes change with the neighbourhood?"
    niche-DE proper. Use smiDE (imaging) or niche-DE (spot-level).
```

### (B) Pseudobulk with an interaction term

```r
library(DESpace)

dsp <- dsp_test(spe, sample_col = "sample_id", condition_col = "condition",
                cluster_col = "domain", verbose = TRUE)
dsp$gene_results
```

```python
import decoupler as dc          # 2.2.0

# dc.get_pseudobulk was REMOVED in decoupler 2.0.
pdata = dc.pp.pseudobulk(adata, sample_col="sample_id", groups_col="domain",
                         layer="counts", mode="sum")
# min_cells / min_counts moved out of pseudobulk into filter_samples
dc.pp.filter_samples(pdata, min_cells=10, min_counts=1000)
# then PyDESeq2 with design "~ condition + domain + condition:domain"
```

Aggregate raw counts. Keep sample as the replication unit. Drop tiny (sample, domain) pseudobulks.

### Why cell-level tests fail here

```
smiDE (Genome Biology 2026;27:21) measured type-I error for cell-level
approaches on spatial data:
  DESeq2 0.95, MAST / Seurat / NB-GLM ~0.90, C-SIDE 0.86

On a 426-gene neuron panel:
  C-SIDE            252 DE genes
  niche-DE          269 (NB) / 241 (Gaussian)
  smiDE naive       178 (Bonferroni) / 262 (FDR)
  smiDE spatial       3

Segmentation bleed and spatial autocorrelation both manufacture significance.
Neighbouring cells are not independent observations.
```

Never run Wilcoxon across conditions at spot or cell level.

---

## Common Pitfalls

### Loading
1. **Using `scanpy.read_visium`**: deprecated since scanpy 1.11.0 and on a removal clock. Use `squidpy.read.visium`, and note the argument is `counts_file`, not `count_file`.
2. **Trying to load Visium HD with `squidpy.read.visium`**: it parses CSV position files only, and HD ships `tissue_positions.parquet`. Use `spatialdata_io.visium_hd` or `VisiumIO::TENxVisiumHD`.
3. **Leaving `bin_size=None` on Visium HD**: this loads every bin size at once and blows up memory. Always pass the bin size you want.
4. **Keeping `gex_only=True` on Xenium then trying to compute control-probe FDR**: the default drops exactly the features you need. Pass `gex_only=False`.
5. **Matching on `obs["region"] == "cell_circles"`**: the `cells_as_circles` default flipped to `False` in spatialdata-io 0.7.0, changing the region key to `cell_labels`. Pin the version or set the argument explicitly.
6. **Porting Seurat binned-Visium coordinate code across 5.4.0**: x/y mapping was corrected to match 10x. Older hand-rolled coordinate math is transposed.

### QC
7. **Global QC thresholds on tissue sections**: a fixed UMI cutoff removes low-cellularity anatomy (white matter, adipose, necrosis) rather than bad spots. Use spatially local outlier detection (`SpotSweeper::localOutliers`).
8. **Treating imaging-based data like sequencing-based data**: for Xenium/MERSCOPE/CosMx the dominant error is segmentation, not sequencing depth. Check cell area, aspect ratio, and signal density, not just counts.
9. **Ignoring FOV borders**: cells clipped by field-of-view edges have systematically truncated counts. Flag cells within one mean cell radius of a border.
10. **Chasing an absolute negative-control threshold**: 10x publishes none. Compare control-derived FDR across runs on the same panel.

### SVG detection
11. **Thresholding SVGs on adjusted p-values**: p-value calibration is broken for most methods. Use a fixed rank cutoff.
12. **Using SpatialDE at modern scale**: unmaintained since 2019 and needs ~150 GB at 40k spots. SpatialDE2 was never released to PyPI.
13. **Wrong neighbourhood graph for the platform**: Visium is a hex grid (`n_neighs=6`). Using a generic k-NN graph on grid data, or a grid assumption on imaging data, distorts every spatial statistic downstream.
14. **Comparing Geary's C across squidpy 1.8.2**: the variance calculation changed. Re-run rather than compare.

### Deconvolution
15. **Skipping the simple baseline**: two independent benchmarks found NNLS and marker-signature scoring competitive with dedicated methods, and better than several of them. Run one, and justify the sophisticated method against it.
16. **Following an old RCTD tutorial against the Bioconductor package**: `create.RCTD`/`run.RCTD` and `createRctd`/`runRctd` are different APIs in two different packages that share the name `spacexr`. The weights matrix is also transposed between them.
17. **Passing `use_gpu=True` to cell2location**: removed from scvi-tools in 1.1.0, so it raises rather than warns. Much published tutorial material still uses it. Pass `accelerator="gpu", devices=1`.
18. **Log-transforming or HVG-subsetting before deconvolution**: RCTD and cell2location need raw integer counts. RCTD errors on non-integers; cell2location silently produces nonsense.
19. **Not declaring reference batch structure in cell2location**: the `RegressionModel` step is where platform and donor effects get removed. Omitting `batch_key` and `categorical_covariate_keys` is a common cause of poor mapping.
20. **Cell types with fewer than 25 reference cells**: RCTD drops them silently. Check which types survived rather than assuming your full annotation was used.
21. **Reading proportions as absolute percentages**: they are reliable for comparing a cell type across regions or conditions, and systematically biased in magnitude. Do not report them as true composition.
22. **Deconvolving single-cell-resolution data**: Xenium, MERSCOPE, and CosMx need segmentation and cell typing. The one legitimate use is RCTD doublet mode as a read-out for segmentation fusion.
23. **Treating Visium HD bin size as a display setting**: single-cell-type bin fraction drops from 61.5% at 8 um to 13.3% at 16 um, and cell-cell correlations can change sign. Pick the bin size before interpreting anything.

### Domains and niches
24. **Using `sq.gr.spatial_neighbors`**: deprecated since squidpy 1.7.0 and removed in 1.9.0. Use `spatial_neighbors_knn`, `_radius`, `_delaunay`, or `_grid`. When passing a `SpatialData` object, `table_key` is required.
25. **Skipping the smoothed-Leiden baseline**: nearly a third of published domain methods scored worse than spatial smoothing applied to plain scanpy clustering. Spatial gains on Visium are small; they are large only at single-cell resolution.
26. **Running BANKSY on a small panel**: accuracy drops sharply below ~1000 genes, and CellCharter below ~100. On a 300-gene panel use SpaceFlow, SpaDo, BASS, or CCST.
27. **Calling `ScaleData` after `RunBanksy`**: it overwrites the scaled BANKSY matrix with gene-wise z-scores and cancels the `lambda` weighting entirely.
28. **Reading `nhood_enrichment` as a property of the tissue**: it is a property of the graph you built. Changing `n_neighs` or the builder changes the result. Report the graph alongside the statistic.
29. **Choosing a domain method tuned for the wrong objective**: domain methods merge recurrent niches; niche methods fragment smooth domains. Decide which question you are asking first.
30. **Getting the pixel-to-micron conversion wrong in CellChat**: every distance threshold (`interaction.range`, `contact.range`) is in microns. A wrong `ratio` silently rescales all of them.

### Niche differential expression
31. **Wilcoxon across conditions at spot or cell level**: measured type-I error is ~0.90-0.95. Neighbouring spots are not independent. Pseudobulk by sample x domain and test the interaction term.
32. **Attaching p-values to single-sample domain markers**: with one sample the effective n is 1. Report effect sizes, or get more samples.
33. **Using `dc.get_pseudobulk`**: removed in decoupler 2.0. It is `dc.pp.pseudobulk`, and `min_cells`/`min_counts` moved to `dc.pp.filter_samples`.
34. **Ignoring segmentation bleed in imaging-based DE**: transcripts assigned to the wrong cell manufacture differential expression. A spatially aware model found 3 genes where naive models found 178-262 on the same panel.

## Related Skills

- `single-cell-atlas`: reference atlas construction, the input to spatial deconvolution
- `cancer-multiomics`: bulk expression analysis and TCGA retrieval

## Public Datasets for Testing

| Dataset | Platform | Access |
|---------|----------|--------|
| Mouse brain sagittal | Visium | `squidpy.datasets.visium("V1_Adult_Mouse_Brain")` |
| Mouse brain H&E | Visium | `squidpy.datasets.visium_hne_adata()` |
| Human breast cancer | Visium | 10x Genomics public datasets |
| Human lymph node | Visium | 10x Genomics; standard cell2location benchmark |
| Mouse brain | Xenium | 10x Genomics public datasets |
